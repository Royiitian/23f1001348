from io import BytesIO
from flask import Blueprint, current_app, make_response, abort, send_file, request, jsonify, Response
import jwt
import bcrypt
import datetime
from utils import get_db_connection, token_required

# Define the blueprint for users
user_management = Blueprint('user_management', __name__)


# Authenticate user
@user_management.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get("username")
    password = request.json.get("password")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT pass_hash, role, user_id, full_name, pin_code, approval FROM Users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password.encode('utf-8'), result['pass_hash'].encode('utf-8')):
        token = jwt.encode({
            'user_id': result['user_id'],
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)
        }, current_app.config['SECRET_KEY'])
        return jsonify({
            "success": True,
            "message": "Authentication successful",
            "token": token,
            "role": result['role'],
            "user_id": result['user_id'],
            "full_name": result['full_name'],
            "pin_code": result['pin_code'],
            "approval": result['approval']
        }), 200
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Register user
@user_management.route('/create-user', methods=['POST'])
def create_user():
    action = request.form.get("action")
    username = request.form.get("username")
    password = request.form.get("password")
    mail = request.form.get("mail")
    mobile = request.form.get("mobile")
    full_name = request.form.get("full_name")
    address = request.form.get("address")
    pin_code = request.form.get("pin_code")
    date_created = datetime.datetime.utcnow().date()

    if action == "service_reg":
        service = request.form.get("subservice")
        exp = request.form.get("experience")
        experience = int(exp) if exp else None
        portfolio_file = request.files.get('portfolio')
        portfolio = portfolio_file.read() if portfolio_file else None

    pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return jsonify({"success": False, "message": "Username already exists"}), 409

    cursor.execute('SELECT COUNT(*) FROM Users WHERE mail = ?', (mail,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return jsonify({"success": False, "message": "Email already exists"}), 409

    if action == "cust_reg":
        cursor.execute('INSERT INTO Users (username, pass_hash, role, mail, mobile, full_name, address, pin_code, date_created) VALUES (?,?,?,?,?,?,?,?,?)',
                       (username, pass_hash, "customer", mail, mobile, full_name, address, pin_code, date_created))
    elif action == "service_reg":
        cursor.execute('INSERT INTO Users (username, pass_hash, role, mail, mobile, full_name, address, pin_code, date_created, service, experience, portfolio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                       (username, pass_hash, "serviceman", mail, mobile, full_name, address, pin_code, date_created, service, experience, portfolio))
    else:
        return jsonify({"success": False, "message": "Invalid action"}), 400

    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "User created successfully"}), 200

# Fetch all servicemen
@user_management.route('/fetch-servicemen', methods=['GET'])
@token_required
def fetch_servicemen():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, full_name, service, Rating, experience, pin_code, approval, date_created FROM Users WHERE role = 'serviceman'")
        servicemen = cursor.fetchall()
        conn.close()

        if not servicemen:
            return jsonify({"success": False, "message": "No servicemen found"}), 404

        result = [{
            "user_id": row[0],
            "full_name": row[1],
            "service": row[2],
            "rating": row[3],
            "experience": row[4],
            "pin_code": row[5],
            "approval": row[6],
            "date_created": row[7]
        } for row in servicemen]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Fetch all customers
@user_management.route('/fetch-customers', methods=['GET'])
@token_required
def fetch_customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, full_name, mail, mobile, pin_code, approval, username, date_created FROM Users WHERE role = 'customer'")
        customers = cursor.fetchall()
        conn.close()

        if not customers:
            return jsonify({"success": False, "message": "No customers found"}), 404

        result = [{
            "user_id": row[0],
            "full_name": row[1],
            "mail": row[2],
            "mobile": row[3],
            "pin_code": row[4],
            "approval": row[5],
            "username": row[6],
            "date_created": row[7]
        } for row in customers]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Update user profile
@user_management.route('/modify-profile', methods=['PUT'])
@token_required
def modify_profile():
    data = request.form
    user_id = request.token_data['user_id']
    role = request.token_data['role']

    conn = get_db_connection()
    cursor = conn.cursor()

    updates = {}
    common_fields = ['password', 'mail', 'mobile', 'full_name', 'address', 'pin_code']
    for field in common_fields:
        if field in data:
            if field == 'password':
                updates['pass_hash'] = bcrypt.hashpw(data[field].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                updates[field] = data[field]

    if role == 'serviceman':
        if 'experience' in data:
            updates['experience'] = data['experience']
        if 'portfolio' in request.files:
            updates['portfolio'] = request.files['portfolio'].read()
        if 'subservice' in data:
            updates['service'] = data['subservice']

    update_fields = ', '.join([f"{k} = ?" for k in updates.keys()])
    query = f"UPDATE Users SET {update_fields} WHERE user_id = ?"

    try:
        cursor.execute(query, list(updates.values()) + [user_id])
        conn.commit()
        return jsonify({"success": True, "message": "Profile updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

# Fetch PDF portfolio
@user_management.route('/fetch-portfolio/<int:serviceman_id>', methods=['GET'])
def fetch_portfolio(serviceman_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT portfolio FROM Users WHERE user_id = ?", (serviceman_id,))
        result = cursor.fetchone()

        if not result or result[0] is None:
            return jsonify({"success": False, "message": "PDF not found"}), 404

        pdf_file = BytesIO(result[0])
        return send_file(pdf_file, mimetype='application/pdf', as_attachment=True, download_name=f'serviceman_{serviceman_id}.pdf')
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# Update approval status
@user_management.route('/update-status/<int:user_id>', methods=['PUT'])
@token_required
def update_status(user_id):
    data = request.json
    role = request.token_data['role']

    if role != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    if data.get('approval') == 'true':
        cursor.execute("UPDATE Users SET approval = true WHERE user_id = ?", (user_id,))
    elif data.get('approval') == 'false':
        cursor.execute("UPDATE Users SET approval = false WHERE user_id = ?", (user_id,))
    else:
        return jsonify({"success": False, "message": "Invalid approval status"}), 400

    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Approval status updated"}), 200

# Fetch individual serviceman
@user_management.route('/fetch-serviceman/<int:serviceman_id>', methods=['GET'])
@token_required
def fetch_serviceman(serviceman_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, full_name, address, service, experience, pin_code, date_created, mail, mobile FROM Users WHERE user_id = ?", (serviceman_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"success": False, "message": "Serviceman not found"}), 404

        serviceman = {
            "user_id": result[0],
            "full_name": result[1],
            "address": result[2],
            "service": result[3],
            "experience": result[4],
            "pin_code": result[5],
            "date_created": result[6],
            "mail": result[7],
            "mobile": result[8]
        }
        return jsonify(serviceman), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Fetch individual customer
@user_management.route('/fetch-customer/<int:customer_id>', methods=['GET'])
@token_required
def fetch_customer(customer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, mail, mobile, pin_code, address FROM Users WHERE user_id = ?", (customer_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"success": False, "message": "Customer not found"}), 404

        customer = {
            "full_name": result[0],
            "mail": result[1],
            "mobile": result[2],
            "pin_code": result[3],
            "address": result[4]
        }
        return jsonify(customer), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
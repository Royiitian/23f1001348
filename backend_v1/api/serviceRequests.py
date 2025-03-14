import datetime
from flask import Blueprint, jsonify, request
from utils import get_db_connection, token_required

# Define the blueprint for service operations
service_operations = Blueprint('service_ops', __name__)

# Route to fetch services assigned to a specific serviceman
@service_operations.route('/fetchServices/<int:serviceman_id>', methods=['GET'])
@token_required
def fetch_services(serviceman_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        fetch_query = """
        SELECT serviceRequest_id, customer_id, serviceman_id, status, service, 
               customer_name, customer_address, rating, request_begin_date, request_end_date
        FROM ServiceRequests
        WHERE serviceman_id = ?
        """
        cursor.execute(fetch_query, (serviceman_id,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        if not records:
            return jsonify({"message": "No services found for this serviceman"}), 404

        services_list = [{
            "serviceRequest_id": record[0],
            "customer_id": record[1],
            "serviceman_id": record[2],
            "status": record[3],
            "service": record[4],
            "customer_name": record[5],
            "customer_address": record[6],
            "rating": record[7],
            "request_begin_date": record[8],
            "request_end_date": record[9]
        } for record in records]

        return jsonify(services_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch services requested by a specific customer
@service_operations.route('/fetchCustomerServices/<int:customer_id>', methods=['GET'])
@token_required
def fetch_customer_services(customer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        fetch_query = """
        SELECT serviceRequest_id, customer_id, serviceman_id, serviceman_name, status, service, rating, request_begin_date, request_end_date
        FROM ServiceRequests
        WHERE customer_id = ?
        """
        cursor.execute(fetch_query, (customer_id,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        if not records:
            return jsonify({"message": "No services found for this customer"}), 404

        services_list = [{
            "serviceRequest_id": record[0],
            "customer_id": record[1],
            "serviceman_id": record[2],
            "serviceman_name": record[3],
            "status": record[4],
            "service": record[5],
            "rating": record[6],
            "request_begin_date": record[7],
            "request_end_date": record[8]
        } for record in records]

        return jsonify(services_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add a new service request
@service_operations.route('/createServiceRequest', methods=['POST'])
@token_required
def create_service_request():
    try:
        data = request.get_json()
        required_fields = ['customer_id', 'serviceman_id', 'status', 'service', 'customer_name', 'customer_address', 'subservice_id']
        if not all(data.get(field) for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM ServiceRequests
        WHERE serviceman_id = ? AND customer_id = ? AND (status = ? OR status = ?)
        """, (data['serviceman_id'], data['customer_id'], "requested", "active"))

        if cursor.fetchone()[0] > 0:
            conn.close()
            return jsonify({"message": "Existing service request found"}), 400

        insert_query = """
        INSERT INTO ServiceRequests (customer_id, serviceman_id, serviceman_name, status, service, customer_name, customer_address, SubService_id, request_begin_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (data['customer_id'], data['serviceman_id'], data.get('serviceman_Fullname'), data['status'], data['service'], data['customer_name'], data['customer_address'], data['subservice_id'], datetime.datetime.utcnow().date()))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Service request created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to modify an existing service request
@service_operations.route('/modifyServiceRequest', methods=['PUT', 'OPTIONS'])
@token_required
def modify_service_request():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        data = request.token_data
        request_data = request.json
        service_id = request_data.get('serviceRequest_id')
        new_status = request_data.get('status')
        current_date = datetime.datetime.utcnow().date()

        conn = get_db_connection()
        cursor = conn.cursor()

        if data['role'] == "customer" and new_status in ["completed", "withdrawn"]:
            if new_status == "completed":
                rating = request_data.get('rating')
                cursor.execute("""
                    UPDATE ServiceRequests
                    SET status = ?, rating = ?, request_end_date = ?
                    WHERE serviceRequest_id = ?
                    """, (new_status, rating, current_date, service_id))
            else:
                cursor.execute("""
                    UPDATE ServiceRequests
                    SET status = ?, request_end_date = ?
                    WHERE serviceRequest_id = ?
                    """, (new_status, current_date, service_id))
            conn.commit()
            conn.close()
            return jsonify({"message": f"Service updated successfully -- Service {new_status.capitalize()}"}), 200

        elif data['role'] == "serviceman" and new_status in ["rejected", "active"]:
            if new_status == "rejected":
                cursor.execute("""
                    UPDATE ServiceRequests
                    SET status = ?, request_end_date = ?
                    WHERE serviceRequest_id = ?
                    """, (new_status, current_date, service_id))
            else:
                cursor.execute("""
                    UPDATE ServiceRequests
                    SET status = ?
                    WHERE serviceRequest_id = ?
                    """, (new_status, service_id))
            conn.commit()
            conn.close()
            return jsonify({"message": f"Service updated successfully -- Service {new_status.capitalize()}"}), 200
        else:
            return jsonify({"message": "Invalid role or status submitted"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch all services
@service_operations.route('/fetchAllServices', methods=['GET'])
@token_required
def fetch_all_services():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        fetch_query = """
        SELECT serviceRequest_id, customer_id, serviceman_id, status, service, 
               customer_name, customer_address, rating, serviceman_name, request_begin_date, request_end_date
        FROM ServiceRequests
        """
        cursor.execute(fetch_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        services_list = [{
            "serviceRequest_id": record[0],
            "customer_id": record[1],
            "serviceman_id": record[2],
            "status": record[3],
            "service": record[4],
            "customer_name": record[5],
            "customer_address": record[6],
            "rating": record[7],
            "serviceman_name": record[8],
            "request_begin_date": record[9],
            "request_end_date": record[10]
        } for record in records]

        return jsonify(services_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to calculate the average rating of a serviceman
@service_operations.route('/calculateAverageRating/<int:serviceman_id>', methods=['GET'])
@token_required
def calculate_average_rating(serviceman_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        avg_query = """
        SELECT AVG(rating) as average_rating
        FROM ServiceRequests
        WHERE serviceman_id = ? AND status = 'completed'
        """
        cursor.execute(avg_query, (serviceman_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        avg_rating = result[0] if result and result[0] is not None else "No ratings available"

        return jsonify({"serviceman_id": serviceman_id, "average_rating": avg_rating}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
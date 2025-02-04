from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_security import auth_required, current_user, roles_required
from application.modeles import db, User, Role, Service, Booking, ServiceProfessional
from flask_restful import Resource, reqparse
from application.resources import ServiceAPI, BookingAPI

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard"))
    return render_template("index.html")  # Serve index.html as login page

@routes.route("/dashboard", methods=["GET"])
@auth_required("token")
def dashboard():
    if current_user.has_role('admin'):
        return jsonify({"message": "Welcome to Admin Dashboard"})
    elif current_user.has_role('customer'):
        return jsonify({"message": "Welcome to Customer Dashboard"})
    elif current_user.has_role('service_professional'):
        return jsonify({"message": "Welcome to Service Professional Dashboard"})
    else:
        return jsonify({"message": "Invalid Role"}), 403
    
@routes.route("/api/services", methods=["GET", "POST"])
@routes.route("/api/services/<int:service_id>", methods=["GET"])
def services(service_id=None):
    return ServiceAPI().dispatch_request(service_id)

@routes.route("/api/bookings", methods=["GET", "POST"])
def bookings():
    return BookingAPI().dispatch_request()

@routes.route("/api/user-role")
@auth_required("token")
def user_role():
    return jsonify({"role": current_user.roles[0].name})
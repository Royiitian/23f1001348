from flask_restful import Resource, reqparse
from flask_security import auth_required, roles_required, current_user
from application.modeles import db, User, Role, Service, Booking, ServiceProfessional, ProfessionalServices
from datetime import datetime

class RegisterAPI(Resource):
    def post(self):
        # Registration logic here
        return {"message": "Registration successful"}

class LoginAPI(Resource):
    def post(self):
        # Login logic here
        return {"message": "Login successful"}
    
class ServiceAPI(Resource):
    @auth_required('token')
    def get(self, service_id=None):
        if service_id:
            service = Service.query.get_or_404(service_id)
            return {'id': service.id, 'name': service.name, 'description': service.description, 'price': service.price}
        services = Service.query.all()
        return [{'id': s.id, 'name': s.name, 'description': s.description, 'price': s.price} for s in services]

    @auth_required('token')
    @roles_required('admin')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('price', type=float, required=True)
        args = parser.parse_args()
        
        new_service = Service(name=args['name'], description=args['description'], price=args['price'])
        db.session.add(new_service)
        db.session.commit()
        return {'message': 'Service created successfully'}, 201

class BookingAPI(Resource):
    @auth_required('token')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service_id', type=int, required=True)
        parser.add_argument('date', type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'), required=True)
        args = parser.parse_args()
        
        new_booking = Booking(user_id=current_user.id, service_id=args['service_id'], date=args['date'])
        db.session.add(new_booking)
        db.session.commit()
        return {'message': 'Booking created successfully'}, 201

    @auth_required('token')
    def get(self):
        if current_user.has_role('customer'):
            bookings = Booking.query.filter_by(user_id=current_user.id).all()
        elif current_user.has_role('service_professional'):
            professional = ServiceProfessional.query.filter_by(user_id=current_user.id).first()
            bookings = Booking.query.join(Service, Booking.service_id == Service.id)\
                .join(ProfessionalServices, Service.id == ProfessionalServices.service_id)\
                .filter(ProfessionalServices.professional_id == professional.id).all()
        else:
            return {'message': 'Unauthorized'}, 403
        
        return [{'id': b.id, 'service': b.service.name, 'date': b.date.isoformat(), 'status': b.status} for b in bookings]
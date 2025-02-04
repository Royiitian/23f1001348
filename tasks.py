from celery import Celery
from application.modeles import db, Booking
from datetime import datetime, timedelta

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def check_upcoming_bookings():
    tomorrow = datetime.now() + timedelta(days=1)
    upcoming_bookings = Booking.query.filter(Booking.date == tomorrow.date()).all()
    for booking in upcoming_bookings:
        # Send reminder email to user and service professional
        send_reminder_email(booking)

def send_reminder_email(booking):
    # Implement email sending logic here
    pass

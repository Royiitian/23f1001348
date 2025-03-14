from celery_config import app
from mail_sender import send_email
from utils import get_db_connection


@app.task
def notify_pending_service_requests():
    # Establish database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch servicemen with pending requests - removed service_type as it doesn't exist
    cursor.execute("""
        SELECT 
            u.mail,
            u.full_name,
            COUNT(sr.serviceman_id) as pending_count
        FROM ServiceRequests sr
        INNER JOIN Users u ON sr.serviceman_id = u.user_id
        WHERE sr.status = 'requested'
        GROUP BY u.mail, u.full_name;
    """)

    pending_requests = cursor.fetchall()
    conn.close()

    for record in pending_requests:
        recipient_email = record['mail']
        name = record['full_name']
        request_total = record['pending_count']

        email_body = generate_notification_email(name, request_total)
        email_subject = create_email_subject(request_total)

        # Send notification
        send_email(recipient_email, email_subject, email_body)

    print(f"Successfully sent notifications to {len(pending_requests)} service providers")


def create_email_subject(count):
    return f"Action Required: {count} Service Request{'s' if count > 1 else ''} Awaiting Response"


def generate_notification_email(provider_name, request_count):
    return f"""
    <html>
    <body style="margin: 0; padding: 20px; background-color: #f5f5f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; padding: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; font-size: 24px; margin: 0;">Service Request Update</h1>
                <div style="width: 50px; height: 3px; background-color: #3498db; margin: 15px auto;"></div>
            </div>

            <div style="color: #34495e; line-height: 1.6;">
                <p>Hello {provider_name},</p>

                <div style="background-color: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 16px;">
                        You have <strong>{request_count}</strong> new service request{'' if request_count == 1 else 's'} 
                        waiting for your review.
                    </p>
                </div>

                <div style="margin: 25px 0;">
                    <p>Quick actions needed:</p>
                    <ul style="list-style-type: none; padding: 0;">
                        <li style="margin: 10px 0;">
                            ✓ Review request details
                        </li>
                        <li style="margin: 10px 0;">
                            ✓ Accept or decline requests
                        </li>
                        <li style="margin: 10px 0;">
                            ✓ Update your availability if needed
                        </li>
                    </ul>
                </div>

                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:8080/dashboard" 
                       style="display: inline-block; padding: 12px 25px; background-color: #3498db; 
                              color: #ffffff; text-decoration: none; border-radius: 5px; 
                              font-weight: bold; text-transform: uppercase; font-size: 14px;">
                        View Requests
                    </a>
                </div>

                <p style="color: #7f8c8d; font-size: 13px; margin-top: 30px; text-align: center;">
                    This is an automated message. Please do not reply directly to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
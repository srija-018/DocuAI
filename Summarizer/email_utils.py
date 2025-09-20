from dotenv import load_dotenv
import os
from django.core.mail import EmailMessage, get_connection

load_dotenv() 


# ----------------------------------- SEND SUMMARY EMAIL FUNCTION -----------------------------------
def send_summary_email(to_email, subject, body, file_path):
    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=587,
            username=os.getenv("EMAIL_USER"),
            password=os.getenv("EMAIL_PASS"),
            use_tls=True
        )

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=os.getenv("EMAIL_USER"),
            to=[to_email],
            connection=connection
        )

        email.attach_file(file_path)
        email.send()
        return True
    except Exception as e:
        return str(e)

import logging
import os
import django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shaxzodbek.settings")
django.setup()
logging.basicConfig(level=logging.INFO)


def send_email(recipient, context):
    logging.info(f"Sending email to {recipient}")
    subject = "Subject"
    message = "Message"
    template_name = "email.html"
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
        subject, message, settings.DEFAULT_FROM_EMAIL, [recipient]
    )
    email.attach_alternative(html_content, "text/html")
    logging.info(f"Email subject: {subject}")
    logging.info(f"Email message: {message}")
    logging.info(f"Email from: {settings.DEFAULT_FROM_EMAIL}")
    logging.info(f"Email to: {recipient}")
    try:
        email.send()
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
    return True


if __name__ == "__main__":
    logging.info("Starting email sending process")
    result = send_email(
        "shermatovjasur800@gmail.com",
        {"name": "Shaxzodbek", "content": "QAnday eeee jasur", "sign_up": True},
    )
    logging.info(f"Email sending process finished with result: {result}")

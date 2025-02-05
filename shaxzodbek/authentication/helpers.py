import logging
import os
import random

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
    try:
        email.send()
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {e}")
        return False
    return True


if __name__ == "__main__":

    logging.info("Starting email sending process")
    result = send_email(
        "muxtorovshaxzodbek16@gmail.com",
        {
            "name": "Shaxzodbek",
            "content": f"{random.randint(10000, 1000000)}",
            "sign_up": True,
        },
    )
    logging.info(f"Email sending process finished with result: {result}")

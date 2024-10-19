import requests
from requests.auth import HTTPBasicAuth
from celery import shared_task
from app.models import User
from email.mime.text import MIMEText

import aiosmtplib

import app.database
from app.config import SENDER_EMAIL, SMTP_HOST, SMTP_PORT, SMTP_PASS


@shared_task
async def send_email_message(user_id, subject, message):
    user = app.database.get_user_db(app.database.get_session, user_id)
    email = user.email
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    email_client = aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True)
    await email_client.connect()
    await email_client.login(SENDER_EMAIL, SMTP_PASS)
    await email_client.send_message(msg)
    await email_client.quit()
    
    return f"Email sent successfully to receiver."
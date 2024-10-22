import requests
from requests.auth import HTTPBasicAuth
from celery import shared_task
from app.models import User
from email.mime.text import MIMEText

import aiosmtplib


import app.database as database
from app.config import SENDER_EMAIL, SMTP_HOST, SMTP_PORT, SMTP_PASS, SMS_SENDER_EMAIL, SMS_API, SMS_SIGN, SMS_URL


@shared_task
async def send_email_message(user_id, subject, message):
    async with database.get_session() as session:
        user = await database.get_user_db_by_id(session, user_id)
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
    
    return f'Email sent successfully to receiver.'


@shared_task
async def send_sms(user_id, message):
    async with database.get_session() as session:
        user = await database.get_user_by_id_db(session, user_id)
        phone = user.phone
        headers = {
            'accept': 'application/json'
        }
        params = {
            'number': phone,
            'text': message,
            'sign': SMS_SIGN
        }
        response = requests.get(
            SMS_URL,
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(SMS_SENDER_EMAIL, SMS_API)
        )
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print("Ошибка:", response.status_code, response.text)

import httpx
import aiosmtplib

import redis
from celery import shared_task
from email.mime.text import MIMEText

from .. import config
from .. import database


@shared_task
async def send_maintenance_to_admins():
    redis_tool = redis.StrictRedis(host='localhost', port=6379, db=1) 
    async with database.get_session() as session:
        admins_id = await database.get_admins_id()
        for id in admins_id:
            user = await database.get_user_by_id_db(session, id)
            email = user.email
            msg = MIMEText(
                f'Необходимо записать следующие машины (id в таблице) на обслуживание: {
                    redis_tool.get("vehicles_for_maintenance").decode("utf-8")
                }'
            )
            msg['Subject'] = 'Weekly vehicles maintenance'
            msg['From'] = config.SENDER_EMAIL
            msg['To'] = email

            email_client = aiosmtplib.SMTP(
                hostname=config.SMTP_HOST, port=config.SMTP_PORT, use_tls=True
            )
            await email_client.connect()
            await email_client.login(config.SENDER_EMAIL, config.SMTP_PASS)
            await email_client.send_message(msg)
            await email_client.quit()

    return 'Email sent successfully to receiver.'


@shared_task
async def send_email_message(users_id, subject, message):
    async with database.get_session() as session:
        for user_id in users_id:
            user = await database.get_user_by_id_db(session, user_id)
            email = user.email
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = config.SENDER_EMAIL
            msg['To'] = email

            email_client = aiosmtplib.SMTP(
                hostname=config.SMTP_HOST, port=config.SMTP_PORT, use_tls=True
            )
            await email_client.connect()
            await email_client.login(config.SENDER_EMAIL, config.SMTP_PASS)
            await email_client.send_message(msg)
            await email_client.quit()

    return 'Emails sent successfully to receivers.'




@shared_task
async def send_sms(user_id, message):
    async with database.get_session() as session:
        user = await database.get_user_by_id_db(session, user_id)
        phone = user.phone
        if not phone:
            raise ValueError("Телефон пользователя не найден.")
        headers = {
            'accept': 'application/json'
        }
        params = {
            'number': phone,
            'text': message,
            'sign': config.SMS_SIGN
        }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            config.SMS_URL,
            headers=headers,
            params=params,
            auth=(config.SMS_SENDER_EMAIL, config.SMS_API)
        )
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Ошибка:", response.status_code, response.text)

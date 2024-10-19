import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')

DB_URL = os.getenv('DB_URL')

SMTP_HOST = os.getenv('SMTP_HOST')

SMTP_PORT = os.getenv('SMTP_PORT')

SMTP_PASS = os.getenv('SMTP_PASS')
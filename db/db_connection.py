import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("EMAIL_DB_HOST", "localhost"),
        user=os.getenv("EMAIL_DB_USER", "root"),
        password=os.getenv("EMAIL_DB_PASSWORD", ""),
        database=os.getenv("EMAIL_DB_NAME", "email_db"),
        port=int(os.getenv("EMAIL_DB_PORT", 3306))
    )

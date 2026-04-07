import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    print("DATABASE_URL =", database_url)

    if not database_url:
        raise ValueError("DATABASE_URL が読み込めていません")

    return psycopg.connect(database_url)

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
conn.autocommit = True
cur = conn.cursor()

with open("main.sql", "r") as f:
    sql = f.read()

cur.execute(sql)
print("Schema created successfully.")

cur.close()
conn.close()
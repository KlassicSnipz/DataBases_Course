import os
import psycopg2
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")

load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
conn.autocommit = True
cur = conn.cursor()

with open(os.path.join(BASE_DIR, "merge_procedures.sql"), "r") as f:
    cur.execute(f.read())
print("MERGE procedures created successfully.")

cur.execute("CALL target.merge_country_dim();")
cur.execute("CALL target.merge_customer_dim();")
cur.execute("CALL target.merge_product_dim();")
cur.execute("CALL target.merge_sales_transactions_fact();")
print("All tables merged successfully.")

for table in ["country_dim", "customer_dim", "product_dim", "sales_transactions_fact"]:
    cur.execute(f"SELECT COUNT(*) FROM target.{table};")
    count = cur.fetchone()[0]
    print(f"target.{table}: {count} rows")

cur.close()
conn.close()
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

# Create the procedures
with open(os.path.join(BASE_DIR, "truncate_insert_procedures.sql"), "r") as f:
    cur.execute(f.read())
print("Procedures created successfully.")

# Call them in dependency order: dims first, fact last
cur.execute("CALL target.load_country_dim();")
cur.execute("CALL target.load_customer_dim();")
cur.execute("CALL target.load_product_dim();")
cur.execute("CALL target.load_sales_transactions_fact();")
print("All tables loaded successfully.")

# Verify row counts
for table in ["country_dim", "customer_dim", "product_dim", "sales_transactions_fact"]:
    cur.execute(f"SELECT COUNT(*) FROM target.{table};")
    count = cur.fetchone()[0]
    print(f"target.{table}: {count} rows")

cur.close()
conn.close()
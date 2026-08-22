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

for filename in ["error_log_setup.sql", "pkg_full_load.sql", "pkg_merge_load.sql"]:
    with open(os.path.join(BASE_DIR, filename), "r") as f:
        cur.execute(f.read())
    print(f"{filename} executed successfully.")

cur.execute("CALL pkg_full_load.load_country_dim();")
cur.execute("CALL pkg_full_load.load_customer_dim();")
cur.execute("CALL pkg_full_load.load_product_dim();")
cur.execute("CALL pkg_full_load.load_sales_transactions_fact();")
print("pkg_full_load executed successfully.")

cur.execute("CALL pkg_merge_load.merge_country_dim();")
cur.execute("CALL pkg_merge_load.merge_customer_dim();")
cur.execute("CALL pkg_merge_load.merge_product_dim();")
cur.execute("CALL pkg_merge_load.merge_sales_transactions_fact();")
print("pkg_merge_load executed successfully.")

cur.close()
conn.close()
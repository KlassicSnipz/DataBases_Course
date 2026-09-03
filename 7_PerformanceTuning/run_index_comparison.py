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

query = """
EXPLAIN ANALYZE
SELECT customer_key, customer_name, customer_type
FROM target.customer_dim
WHERE customer_id = 'C0100';
"""

cur.execute("DROP INDEX IF EXISTS target.idx_customer_id;")
print("Ensured no pre-existing index (clean baseline).")

print("\n=== BEFORE INDEX ===")
cur.execute(query)
for row in cur.fetchall():
    print(row[0])

cur.execute("CREATE INDEX idx_customer_id ON target.customer_dim(customer_id);")
print("\nIndex created: idx_customer_id")

print("\n=== AFTER INDEX ===")
cur.execute(query)
for row in cur.fetchall():
    print(row[0])

cur.close()
conn.close()

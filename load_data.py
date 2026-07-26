import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

# Order matters: parents before children (foreign key dependencies)
tables = ["country", "product", "customer", "sales_transaction"]
file_map = {
    "country": "data/country.csv",
    "product": "data/product.csv",
    "customer": "data/customer.csv",
    "sales_transaction": "data/sales_transactions.csv"
}

for table in tables:
    df = pd.read_csv(file_map[table])
    df.to_sql(table, engine, schema="stage", if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into stage.{table}")

print("All data loaded.")
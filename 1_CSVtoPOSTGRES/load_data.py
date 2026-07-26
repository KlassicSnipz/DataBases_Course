import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")

load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

data_dir = os.path.join(ROOT_DIR, "data")

tables = ["country", "product", "customer", "sales_transaction"]
file_map = {
    "country": os.path.join(data_dir, "country.csv"),
    "product": os.path.join(data_dir, "product.csv"),
    "customer": os.path.join(data_dir, "customer.csv"),
    "sales_transaction": os.path.join(data_dir, "sales_transactions.csv")
}

for table in tables:
    df = pd.read_csv(file_map[table])
    df.to_sql(table, engine, schema="stage", if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into stage.{table}")

print("All data loaded.")
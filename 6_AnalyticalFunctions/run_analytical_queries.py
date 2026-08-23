import os
import pandas as pd
from sqlalchemy import create_engine
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

queries = {
    "Part 2: Total Sales per Country": """
        SELECT DISTINCT
            cd.country_name,
            COALESCE(SUM(stf.total_amount) OVER (PARTITION BY cd.country_key), 0) AS total_sales
        FROM target.country_dim cd
        LEFT JOIN target.sales_transactions_fact stf ON cd.country_key = stf.country_key
        ORDER BY total_sales DESC;
    """,
    "Part 3: Country Sales Rank": """
        WITH top_country AS (
            SELECT DISTINCT cd.country_name,
                   SUM(stf.total_amount) OVER (PARTITION BY cd.country_key) AS total_sales
            FROM target.sales_transactions_fact stf
            JOIN target.country_dim cd ON cd.country_key = stf.country_key
        )
        SELECT country_name, total_sales,
               RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
        FROM top_country
        ORDER BY sales_rank;
    """,
    "Part 4: Highest Transaction per Country": """
        WITH ranked_transactions AS (
            SELECT cd.country_name, stf.transaction_id, stf.total_amount,
                   ROW_NUMBER() OVER (PARTITION BY cd.country_key ORDER BY stf.total_amount DESC) AS rn
            FROM target.sales_transactions_fact stf
            JOIN target.country_dim cd ON cd.country_key = stf.country_key
        )
        SELECT country_name, transaction_id, total_amount
        FROM ranked_transactions
        WHERE rn = 1
        ORDER BY total_amount DESC;
    """,
    "Part 5: Top 2 Customers per Country": """
        WITH customer_totals AS (
            SELECT cd.country_name, c.customer_name, SUM(stf.total_amount) AS total_sales,
                   ROW_NUMBER() OVER (PARTITION BY cd.country_key ORDER BY SUM(stf.total_amount) DESC) AS rn
            FROM target.sales_transactions_fact stf
            JOIN target.customer_dim c ON c.customer_key = stf.customer_key
            JOIN target.country_dim cd ON cd.country_key = stf.country_key
            GROUP BY cd.country_key, cd.country_name, c.customer_key, c.customer_name
        )
        SELECT country_name, customer_name, total_sales
        FROM customer_totals
        WHERE rn <= 2
        ORDER BY country_name, rn;
    """,
    "Part 6: Total Sales per Product": """
        SELECT DISTINCT pd.product_name,
               SUM(stf.total_amount) OVER (PARTITION BY pd.product_key) AS total_sales
        FROM target.sales_transactions_fact stf
        JOIN target.product_dim pd ON pd.product_key = stf.product_key
        ORDER BY total_sales DESC;
    """,
    "Part 7: Most Sold Product per Country": """
        WITH product_totals AS (
            SELECT cd.country_name, pd.product_name, SUM(stf.quantity) AS total_quantity,
                   ROW_NUMBER() OVER (PARTITION BY cd.country_key ORDER BY SUM(stf.quantity) DESC) AS rn
            FROM target.sales_transactions_fact stf
            JOIN target.product_dim pd ON pd.product_key = stf.product_key
            JOIN target.country_dim cd ON cd.country_key = stf.country_key
            GROUP BY cd.country_key, cd.country_name, pd.product_key, pd.product_name
        )
        SELECT country_name, product_name, total_quantity
        FROM product_totals
        WHERE rn = 1
        ORDER BY country_name;
    """
}

for title, query in queries.items():
    print(f"\n=== {title} ===")
    df = pd.read_sql(query, engine)
    print(df.to_string(index=False))
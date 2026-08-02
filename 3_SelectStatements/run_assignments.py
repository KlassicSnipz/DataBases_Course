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

# Assignment 1: Customers with Above Average Sales
query1 = """
with customer_total_sales as (
	select cd.customer_name,coalesce(sum(stf.total_amount),0) as total_sales from target.customer_dim cd
	left join target.sales_transactions_fact stf
	on stf.customer_key = cd.customer_key
	group by cd.customer_name
)
select customer_name , total_sales  from customer_total_sales
where total_sales > (select avg(total_sales) from customer_total_sales)
order by total_sales desc;
"""
df1 = pd.read_sql(query1, engine)
print("\n=== Assignment 1: Customers with Above Average Sales ===")
print(df1.to_string(index=False))

# Assignment 2: Top-Selling Product
query2 = """
select pd.product_name, coalesce(sum(stf.total_amount),0) as total_sales from target.product_dim pd
left join target.sales_transactions_fact stf on stf.product_key = pd.product_key
group by pd.product_name
order by total_sales desc
limit 1;
"""
df2 = pd.read_sql(query2, engine)
print("\n=== Assignment 2: Top-Selling Product ===")
print(df2.to_string(index=False))

# Assignment 3: Country-wise Sales Summary Using CTE
query3 = """
with country_sales as (
    select cd.country_name, coalesce(sum(stf.total_amount),0) as total_sales
    from target.country_dim cd
    left join target.sales_transactions_fact stf on cd.country_key = stf.country_key
    group by cd.country_name
)
select country_name, total_sales
from country_sales
order by total_sales desc;
"""
df3 = pd.read_sql(query3, engine)
print("\n=== Assignment 3: Country-wise Sales Summary ===")
print(df3.to_string(index=False))

# Assignment 4: Customers Who Bought More Than 5 Products
query4 = """
select cd.customer_name, count(stf.sales_trans_key) as number_of_purchases from target.customer_dim cd
left join target.sales_transactions_fact stf on cd.customer_key = stf.customer_key
group by cd.customer_name
having count(stf.sales_trans_key) > 5
order by number_of_purchases desc;
"""
df4 = pd.read_sql(query4, engine)
print("\n=== Assignment 4: Customers Who Bought More Than 5 Products ===")
print(df4.to_string(index=False))
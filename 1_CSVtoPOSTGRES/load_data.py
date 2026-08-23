import os
#Used to create file paths
from sqlalchemy import create_engine 
#Used to connect to the database 
import pandas as pd 
#Used to read the csv files
from dotenv import load_dotenv
#Used to read the .env file and load the environment variables into the system

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")
#Path to file directory and root directory


load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env")) 
#Loading the .env file

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
#Pulling all connection variables from the .env file

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}") 
#Creating the engine to connect to the database

data_dir = os.path.join(ROOT_DIR, "data") 
#Path to the data directory

tables = ["country", "product", "customer", "sales_transaction"]
file_map = {
    "country": os.path.join(data_dir, "country.csv"),
    "product": os.path.join(data_dir, "product.csv"),
    "customer": os.path.join(data_dir, "customer.csv"),
    "sales_transaction": os.path.join(data_dir, "sales_transactions.csv")
} #Creating a dictionary to map the table names to the csv files

for table in tables: #Looping through the tables
    df = pd.read_csv(file_map[table]) #Reading the csv file
    df.to_sql(table, engine, schema="stage", if_exists="append", index=False) #Writing the data to the database
    print(f"Loaded {len(df)} rows into stage.{table}") #Printing the number of rows loaded

print("All data loaded.")
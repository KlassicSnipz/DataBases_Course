import os 
#This is used to create a path to the file
import psycopg2
#This is used to connect to the database and talk to Postrge
from dotenv import load_dotenv
#This is used to read the .env file and load the environment variables into the system



BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #Path to this file from any machine
ROOT_DIR = os.path.join(BASE_DIR, "..") #Path to the root directory from BASE_DIR

load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env")) 
#Locating the .env file using the path from ROOT_DIR

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
) #Connecting to the database using the environment variables
conn.autocommit = True #Setting the autocommit to true so that the changes are committed automatically
cur = conn.cursor() #Creating a cursor to interact with the database

with open(os.path.join(BASE_DIR, "stage_schema.sql"), "r") as f: #Opening the stage_schema.sql file
    sql = f.read() #Reading the file

cur.execute(sql) #Executing the SQL statement
print("Stage schema created successfully.")

cur.close() #Closing the cursor
conn.close() #Closing the connection
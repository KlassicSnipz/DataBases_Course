CREATE SCHEMA IF NOT EXISTS stage;

CREATE TABLE stage.country (
   country_code VARCHAR(2) PRIMARY KEY,
   country_name VARCHAR(50),
   region VARCHAR(50)

);

CREATE TABLE stage.customer (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_name VARCHAR(50),
    country_code VARCHAR(2) REFERENCES stage.country(country_code),
    customer_type VARCHAR(50)
);

CREATE TABLE stage.product (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    standard_price DECIMAL(10,2)
);


Create table stage.sales_transaction (
    transaction_id INT PRIMARY KEY,
    transaction_date DATE,
    customer_id VARCHAR(10)  REFERENCES stage.customer(customer_id),
    product_id VARCHAR(10)  REFERENCES stage.product(product_id),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_mode VARCHAR(50)
);


CREATE SCHEMA IF NOT EXISTS target;

CREATE TABLE target.country_dim (
    country_key SERIAL PRIMARY KEY,
    country_code VARCHAR(2) NOT NULL,
    country_name VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL
);

CREATE TABLE target.customer_dim (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    customer_name VARCHAR(50) NOT NULL,
    customer_type VARCHAR(50) NOT NULL
);

CREATE TABLE target.product_dim (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(10) NOT NULL,
    product_name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    standard_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE target.sales_transactions_fact (
    sales_trans_key SERIAL PRIMARY KEY,
    transaction_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    customer_key INT NOT NULL REFERENCES target.customer_dim(customer_key),
    product_key INT NOT NULL REFERENCES target.product_dim(product_key),
    country_key INT NOT NULL REFERENCES target.country_dim(country_key),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_mode VARCHAR(50) NOT NULL
);
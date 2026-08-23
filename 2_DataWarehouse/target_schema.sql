CREATE SCHEMA IF NOT EXISTS target;


create table target.country_dim (
    country_key serial primary key,
    country_code varchar(2) not null,
    country_name varchar(50) not null,
    region varchar(50) not null

)
create table target.customer_dim (
    customer_key serial primary key,
    customer_id varchar(10) not null,
    customer_name varchar(50) not null,
    customer_type varchar(50) not null
)


create table target.product_dim (
    product_key serial primary key,
    product_id varchar(10) not null,
    product_name varchar(50) not null,
    category varchar(50) not null,
    standard_price decimal(10,2) not null
)



create table target.sales_transactions_fact (
    transaction_id int primary key,
    customer_key int not null references target.customer_dim(customer_key),
    product_key int not null references target.product_dim(product_key),
    country_key int not null references target.country_dim(country_key),
    transaction_date date,
    quantity int not null,
    unit_price decimal(10,2) not null,
    total_amount decimal(10,2) not null,
    payment_mode varchar(50) not null
)






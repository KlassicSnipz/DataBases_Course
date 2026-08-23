create schema if not exists stage;

create table stage.country (
    country_code varchar(2) primary key,
    country_name varchar(50),
    region varchar(50)

)

create table stage.customer (
    customer_id varchar(10) primary key,
    customer_name varchar(50),
    country_code varchar(2) references stage.country(country_code),
    customer_type varchar(50)
)


create table stage.product (
    product_id varchar(10) primary key,
    product_name varchar(50),
    category varchar(50),
    standard_price decimal(10,2)
)

create table stage.sales_transaction (
    transaction_id int primary key,
    transaction_date date,
    customer_id varchar(10)  references stage.customer(customer_id),
    product_id varchar(10)  references stage.product(product_id),
    quantity int,
    unit_price decimal(10,2),
    total_amount decimal(10,2),
    payment_mode varchar(50)
)


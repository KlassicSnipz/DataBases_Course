insert into target.country_dim (country_code, country_name, region)
select country_code, country_name, region
from stage.country;

insert into target.customer_dim (customer_id, customer_name, customer_type)
select customer_id, customer_name, customer_type
from stage.customer;

insert into target.product_dim (product_id, product_name, category, standard_price)
select product_id, product_name, category, standard_price
from stage.product;

insert into target.sales_transactions_fact
(transaction_id, transaction_date, customer_key, product_key, country_key,
 quantity, unit_price, total_amount, payment_mode)
select
    st.transaction_id,
    st.transaction_date,
    cd.customer_key,
    pd.product_key,
    cod.country_key,
    st.quantity,
    st.unit_price,
    st.total_amount,
    st.payment_mode
from stage.sales_transaction st
join stage.customer sc on st.customer_id = sc.customer_id
join target.customer_dim cd on sc.customer_id = cd.customer_id
join target.product_dim pd on st.product_id = pd.product_id 
join target.country_dim cod on sc.country_code = cod.country_code;




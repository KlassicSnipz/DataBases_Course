INSERT INTO target.country_dim (country_code, country_name, region)
SELECT country_code, country_name, region
FROM stage.country;

INSERT INTO target.customer_dim (customer_id, customer_name, customer_type)
SELECT customer_id, customer_name, customer_type
FROM stage.customer;

INSERT INTO target.product_dim (product_id, product_name, category, standard_price)
SELECT product_id, product_name, category, standard_price
FROM stage.product;

INSERT INTO target.sales_transactions_fact
    (transaction_id, transaction_date, customer_key, product_key, country_key,
     quantity, unit_price, total_amount, payment_mode)
SELECT
    st.transaction_id,
    st.transaction_date,
    cd.customer_key,
    pd.product_key,
    cod.country_key,
    st.quantity,
    st.unit_price,
    st.total_amount,
    st.payment_mode
FROM stage.sales_transaction st
JOIN stage.customer sc ON st.customer_id = sc.customer_id
JOIN target.customer_dim cd ON sc.customer_id = cd.customer_id
JOIN target.product_dim pd ON st.product_id = pd.product_id
JOIN target.country_dim cod ON sc.country_code = cod.country_code;
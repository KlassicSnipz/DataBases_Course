CREATE OR REPLACE PROCEDURE target.merge_country_dim()
LANGUAGE plpgsql
AS $$
BEGIN
    MERGE INTO target.country_dim AS tgt
    USING stage.country AS src
    ON tgt.country_code = src.country_code
    WHEN MATCHED THEN
        UPDATE SET country_name = src.country_name,
                   region = src.region
    WHEN NOT MATCHED THEN
        INSERT (country_code, country_name, region)
        VALUES (src.country_code, src.country_name, src.region);

    COMMIT;
END;
$$;

CREATE OR REPLACE PROCEDURE target.merge_customer_dim()
LANGUAGE plpgsql
AS $$
BEGIN
    MERGE INTO target.customer_dim AS tgt
    USING stage.customer AS src
    ON tgt.customer_id = src.customer_id
    WHEN MATCHED THEN
        UPDATE SET customer_name = src.customer_name,
                   customer_type = src.customer_type
    WHEN NOT MATCHED THEN
        INSERT (customer_id, customer_name, customer_type)
        VALUES (src.customer_id, src.customer_name, src.customer_type);

    COMMIT;
END;
$$;

CREATE OR REPLACE PROCEDURE target.merge_product_dim()
LANGUAGE plpgsql
AS $$
BEGIN
    MERGE INTO target.product_dim AS tgt
    USING stage.product AS src
    ON tgt.product_id = src.product_id
    WHEN MATCHED THEN
        UPDATE SET product_name = src.product_name,
                   category = src.category,
                   standard_price = src.standard_price
    WHEN NOT MATCHED THEN
        INSERT (product_id, product_name, category, standard_price)
        VALUES (src.product_id, src.product_name, src.category, src.standard_price);

    COMMIT;
END;
$$;

CREATE OR REPLACE PROCEDURE target.merge_sales_transactions_fact()
LANGUAGE plpgsql
AS $$
BEGIN
    MERGE INTO target.sales_transactions_fact AS tgt
    USING (
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
        JOIN target.country_dim cod ON sc.country_code = cod.country_code
    ) AS src
    ON tgt.transaction_id = src.transaction_id
    WHEN MATCHED THEN
        UPDATE SET transaction_date = src.transaction_date,
                   customer_key = src.customer_key,
                   product_key = src.product_key,
                   country_key = src.country_key,
                   quantity = src.quantity,
                   unit_price = src.unit_price,
                   total_amount = src.total_amount,
                   payment_mode = src.payment_mode
    WHEN NOT MATCHED THEN
        INSERT (transaction_id, transaction_date, customer_key, product_key, country_key,
                quantity, unit_price, total_amount, payment_mode)
        VALUES (src.transaction_id, src.transaction_date, src.customer_key, src.product_key, src.country_key,
                src.quantity, src.unit_price, src.total_amount, src.payment_mode);

    COMMIT;
END;
$$;
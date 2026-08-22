CREATE SCHEMA IF NOT EXISTS admin;

CREATE TABLE IF NOT EXISTS admin.error_log (
    log_id SERIAL PRIMARY KEY,
    procedure_name VARCHAR(100),
    error_code VARCHAR(20),
    error_message TEXT,
    logged_at TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE PROCEDURE admin.log_error(
    p_procedure_name VARCHAR,
    p_error_code VARCHAR,
    p_error_message TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO admin.error_log (procedure_name, error_code, error_message)
    VALUES (p_procedure_name, p_error_code, p_error_message);
END;
$$;
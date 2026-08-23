CREATE SCHEMA IF NOT EXISTS admin;

CREATE TABLE IF NOT EXISTS admin.execution_log (
    execution_id SERIAL PRIMARY KEY,
    procedure_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds NUMERIC,
    rows_affected INT,
    status VARCHAR(20),
    logged_at TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE PROCEDURE admin.log_execution(
    p_procedure_name VARCHAR,
    p_start_time TIMESTAMP,
    p_end_time TIMESTAMP,
    p_rows_affected INT,
    p_status VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO admin.execution_log
        (procedure_name, start_time, end_time, duration_seconds, rows_affected, status)
    VALUES
        (p_procedure_name, p_start_time, p_end_time,
         EXTRACT(EPOCH FROM (p_end_time - p_start_time)), p_rows_affected, p_status);
END;
$$;
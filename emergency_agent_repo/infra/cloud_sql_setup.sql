-- Example SQL to initialize Postgres schema for logs
CREATE TABLE IF NOT EXISTS encrypted_logs (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(128),
  payload BYTEA,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

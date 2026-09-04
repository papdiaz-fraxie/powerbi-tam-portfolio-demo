-- Synthetic BigQuery-style data quality checks.
SELECT
  COUNT(*) AS total_records,
  COUNTIF(first_name IS NULL OR TRIM(first_name) = '') AS missing_first_name,
  COUNTIF(last_name IS NULL OR TRIM(last_name) = '') AS missing_last_name,
  COUNTIF(email IS NULL OR TRIM(email) = '') AS missing_email,
  COUNTIF(
    email IS NOT NULL
    AND NOT REGEXP_CONTAINS(LOWER(TRIM(email)), r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
  ) AS invalid_email_format,
  COUNT(*) - COUNT(DISTINCT LOWER(TRIM(email))) AS duplicate_email_rows
FROM `portfolio.raw_contacts`;

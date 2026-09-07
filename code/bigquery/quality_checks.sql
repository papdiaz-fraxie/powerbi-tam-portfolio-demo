-- Synthetic BigQuery-style data quality checks.
-- Illustrates the additional programmatic QA performed after human review.
-- No production schemas or client data are exposed.

WITH prepared AS (
  SELECT
    *,
    LOWER(TRIM(email)) AS email_clean,
    LOWER(REGEXP_REPLACE(TRIM(linkedin_url), r'/$', '')) AS linkedin_clean,
    CASE
      WHEN LOWER(TRIM(country)) IN ('au', 'aus', 'australia') THEN 'Australia'
      WHEN LOWER(TRIM(country)) IN ('nz', 'new zealand') THEN 'New Zealand'
      ELSE TRIM(country)
    END AS country_clean
  FROM `portfolio.staged_contacts`
)
SELECT
  COUNT(*) AS total_records,
  COUNTIF(first_name IS NULL OR TRIM(first_name) = '') AS missing_first_name,
  COUNTIF(last_name IS NULL OR TRIM(last_name) = '') AS missing_last_name,
  COUNTIF(company IS NULL OR TRIM(company) = '') AS missing_company,
  COUNTIF(job_title IS NULL OR TRIM(job_title) = '') AS missing_job_title,
  COUNTIF(country_clean IS NULL OR country_clean = '') AS missing_country,
  COUNTIF(email_clean IS NULL OR email_clean = '') AS missing_email,
  COUNTIF(
    email_clean IS NOT NULL
    AND email_clean != ''
    AND NOT REGEXP_CONTAINS(email_clean, r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
  ) AS invalid_email_format,
  COUNTIF(linkedin_clean IS NULL OR linkedin_clean = '') AS missing_linkedin,
  COUNT(*) - COUNT(DISTINCT NULLIF(email_clean, '')) AS duplicate_email_rows,
  COUNT(*) - COUNT(DISTINCT NULLIF(linkedin_clean, '')) AS duplicate_linkedin_rows
FROM prepared;

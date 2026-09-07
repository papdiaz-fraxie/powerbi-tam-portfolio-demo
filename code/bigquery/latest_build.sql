-- Synthetic BigQuery example: retain history but select the latest researched build.
-- `contact_key` and `research_date` are illustrative public fields, not production schema.

WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY contact_key
      ORDER BY research_date DESC, loaded_at DESC
    ) AS build_rank
  FROM `portfolio.contact_history`
)
SELECT
  * EXCEPT(build_rank)
FROM ranked
WHERE build_rank = 1;

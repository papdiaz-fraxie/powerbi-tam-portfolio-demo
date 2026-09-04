-- Example: select one canonical record per email using a window function.
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY LOWER(TRIM(email))
      ORDER BY updated_at DESC
    ) AS record_rank
  FROM `portfolio.raw_contacts`
  WHERE email IS NOT NULL AND TRIM(email) != ''
)
SELECT * EXCEPT(record_rank)
FROM ranked
WHERE record_rank = 1;

-- SQLite
SELECT
    note,
    COUNT(*) AS record_count
FROM
    transactions
WHERE
    note LIKE "% "
    AND deletedOn IS NULL
GROUP BY
    1
ORDER BY
    2 DESC
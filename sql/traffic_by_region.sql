SELECT
    p.region,
    SUM(f.count_views) AS total_views
FROM fact_pageviews f
JOIN dim_project p
ON f.id_project = p.id_project
GROUP BY p.region
ORDER BY total_views DESC;
SELECT
    t.dia_semana,
    SUM(f.count_views) AS total_views
FROM fact_pageviews f
JOIN dim_time t
ON f.id_time = t.id_time
GROUP BY t.dia_semana;
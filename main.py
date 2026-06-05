from src.extract import extract_last_days
from src.transform import transform_data
from src.load import load_data
from src.analytics import execute_query

# EXTRACT
df_raw = extract_last_days(days=30)

df_raw.to_csv(
    "data/raw/pageviews_raw.csv",
    index=False
)

# TRANSFORM
df_clean = transform_data(df_raw)

df_clean.to_csv(
    "data/processed/pageviews_clean.csv",
    index=False
)

print("RAW:", len(df_raw))
print("CLEAN:", len(df_clean))

# LOAD
load_data(df_clean)
query = """
SELECT
    p.page_title,
    SUM(f.count_views) AS total_views
FROM fact_pageviews f
JOIN dim_page p
ON f.id_page = p.id_page
GROUP BY p.page_title
ORDER BY total_views DESC
LIMIT 10
"""

result = execute_query(query)

print(result)
from src.extract import extract_last_days
from src.transform import transform_data
from src.load import load_data

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
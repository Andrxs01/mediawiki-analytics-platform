import pandas as pd

REGIONS = {
    "es": "Latinoamérica",
    "en": "Norteamérica",
    "fr": "Europa",
    "de": "Europa",
    "pt": "Sudamérica"
}


def transform_data(df):

    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["idioma"] = df["project"].str.split(".").str[0]

    df["dia_semana"] = df["timestamp"].dt.day_name()

    df["mes"] = df["timestamp"].dt.month

    df["anio"] = df["timestamp"].dt.year

    df["region"] = df["idioma"].map(REGIONS)

    bad_patterns = [
        "Wikipedia:",
        "Especial:",
        "Special:",
        "Template:",
        "Category:",
        "File:"
    ]

    for pattern in bad_patterns:
        df = df[
            ~df["page_title"].str.startswith(
                pattern,
                na=False
            )
        ]

    return df
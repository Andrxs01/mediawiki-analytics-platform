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
        "Wikipédia:",
        "Especial:",
        "Special:",
        "Spezial:",
        "Template:",
        "Category:",
        "File:",
        "Portal:",
        "Help:",
        "Ayuda:"
    ]

    for pattern in bad_patterns:
        df = df[
            ~df["page_title"].str.startswith(
                pattern,
                na=False
            )
        ]

    # eliminar páginas conocidas
    bad_pages = [
        ".xxx",
        "Main_Page",
        "Accueil_principal",
        "Página_principal"
    ]

    df = df[
        ~df["page_title"].isin(bad_pages)
    ]
    
    df = df[
    ~df["page_title"].str.contains(
        "Recherche|Buscar|Suche",
        case=False,
        na=False
    )
  ]
    return df
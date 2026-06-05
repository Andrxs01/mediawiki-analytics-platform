import sqlite3
import pandas as pd


DB_PATH = "database/mediawiki.db"


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_project(
        id_project INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT UNIQUE,
        idioma TEXT,
        region TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_page(
        id_page INTEGER PRIMARY KEY AUTOINCREMENT,
        page_title TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_time(
        id_time INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT UNIQUE,
        dia_semana TEXT,
        mes INTEGER,
        anio INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_pageviews(
        id_fact INTEGER PRIMARY KEY AUTOINCREMENT,
        count_views INTEGER,
        id_project INTEGER,
        id_page INTEGER,
        id_time INTEGER,

        FOREIGN KEY(id_project)
            REFERENCES dim_project(id_project),

        FOREIGN KEY(id_page)
            REFERENCES dim_page(id_page),

        FOREIGN KEY(id_time)
            REFERENCES dim_time(id_time)
    )
    """)

    conn.commit()


def load_data(df):

    conn = create_connection()

    create_tables(conn)

    cursor = conn.cursor()

    print("Cargando DimProject...")

    dim_project = (
        df[
            ["project", "idioma", "region"]
        ]
        .drop_duplicates()
    )

    dim_project.to_sql(
        "dim_project",
        conn,
        if_exists="append",
        index=False
    )

    print("Cargando DimPage...")

    dim_page = (
        df[
            ["page_title"]
        ]
        .drop_duplicates()
    )

    dim_page.to_sql(
        "dim_page",
        conn,
        if_exists="append",
        index=False
    )

    print("Cargando DimTime...")

    dim_time = (
        df[
            [
                "timestamp",
                "dia_semana",
                "mes",
                "anio"
            ]
        ]
        .drop_duplicates()
    )

    dim_time.to_sql(
        "dim_time",
        conn,
        if_exists="append",
        index=False
    )

    print("Construyendo Fact Table...")

    project_ids = pd.read_sql(
        "SELECT * FROM dim_project",
        conn
    )

    page_ids = pd.read_sql(
        "SELECT * FROM dim_page",
        conn
    )

    time_ids = pd.read_sql(
        "SELECT * FROM dim_time",
        conn
    )
    time_ids["timestamp"] = pd.to_datetime(
    time_ids["timestamp"]
    )

    fact = df.merge(
        project_ids,
        on=["project", "idioma", "region"]
    )

    fact = fact.merge(
        page_ids,
        on="page_title"
    )

    fact = fact.merge(
        time_ids,
        on=[
            "timestamp",
            "dia_semana",
            "mes",
            "anio"
        ]
    )

    fact = fact[
        [
            "count_views",
            "id_project",
            "id_page",
            "id_time"
        ]
    ]

    fact.to_sql(
        "fact_pageviews",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print("Data Warehouse cargado correctamente.")
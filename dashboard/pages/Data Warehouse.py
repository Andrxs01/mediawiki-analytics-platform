import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Data Warehouse",
    page_icon="🗄️",
    layout="wide"
)

# -------------------------------------
# CSS
# -------------------------------------

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top left,#1e293b,transparent 40%),
    radial-gradient(circle at bottom right,#0f172a,transparent 40%),
    linear-gradient(135deg,#020617,#0f172a,#1e293b);
}

.card{
    background:rgba(255,255,255,0.08);
    border-radius:20px;
    padding:20px;
}

.schema{
    background:rgba(255,255,255,0.08);
    border-left:5px solid #38bdf8;
    padding:20px;
    border-radius:15px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------
# CONNECTION
# -------------------------------------

conn = sqlite3.connect(
    "database/mediawiki.db",
    check_same_thread=False
)

# -------------------------------------
# TITLE
# -------------------------------------

st.title("🗄️ Data Warehouse")

st.caption(
    "Modelo dimensional construido a partir del proceso ETL."
)

st.divider()

# -------------------------------------
# TABLE COUNTS
# -------------------------------------

dim_project = pd.read_sql(
    "SELECT COUNT(*) total FROM dim_project",
    conn
)

dim_page = pd.read_sql(
    "SELECT COUNT(*) total FROM dim_page",
    conn
)

dim_time = pd.read_sql(
    "SELECT COUNT(*) total FROM dim_time",
    conn
)

fact = pd.read_sql(
    "SELECT COUNT(*) total FROM fact_pageviews",
    conn
)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "🌎 DimProject",
    f"{int(dim_project.iloc[0,0]):,}"
)

c2.metric(
    "📄 DimPage",
    f"{int(dim_page.iloc[0,0]):,}"
)

c3.metric(
    "📅 DimTime",
    f"{int(dim_time.iloc[0,0]):,}"
)

c4.metric(
    "📊 FactPageviews",
    f"{int(fact.iloc[0,0]):,}"
)

st.divider()

# -------------------------------------
# STAR SCHEMA
# -------------------------------------

st.subheader("⭐ Modelo Estrella")

st.markdown("""
<div class="schema">

FACT_PAGEVIEWS

⬇️

count_views

id_project

id_page

id_time

<br><br>

DIM_PROJECT

• project

• idioma

• region

<br><br>

DIM_PAGE

• page_title

<br><br>

DIM_TIME

• timestamp

• dia_semana

• mes

• anio

</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------
# ETL FLOW
# -------------------------------------

st.subheader("⚙️ Flujo ETL")

st.markdown("""
<div class="schema">

Wikimedia API

⬇️

Raw Dataset

⬇️

Transformación y Limpieza

⬇️

Data Warehouse SQLite

⬇️

Consultas SQL

⬇️

Dashboard Streamlit

</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------
# SAMPLE DATA
# -------------------------------------

st.subheader("📄 Vista previa de Fact Table")

sample = pd.read_sql("""

SELECT *
FROM fact_pageviews
LIMIT 20

""", conn)

st.dataframe(
    sample,
    use_container_width=True
)

st.divider()

# -------------------------------------
# QUALITY METRICS
# -------------------------------------

st.subheader("✅ Calidad de Datos")

quality = pd.DataFrame({
    "Métrica":[
        "Registros Fact",
        "Proyectos",
        "Páginas",
        "Fechas"
    ],
    "Cantidad":[
        int(fact.iloc[0,0]),
        int(dim_project.iloc[0,0]),
        int(dim_page.iloc[0,0]),
        int(dim_time.iloc[0,0])
    ]
})

st.dataframe(
    quality,
    use_container_width=True
)

conn.close()
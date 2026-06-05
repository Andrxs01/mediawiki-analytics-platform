import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Insights",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top left,#1e293b,transparent 40%),
    radial-gradient(circle at bottom right,#0f172a,transparent 40%),
    linear-gradient(135deg,#020617,#0f172a,#1e293b);
}

.insight-card{
    background:rgba(255,255,255,0.08);
    border-radius:20px;
    padding:20px;
    margin-bottom:15px;
    border-left:5px solid #38bdf8;
}

.big-number{
    font-size:40px;
    font-weight:bold;
    color:#38bdf8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

conn = sqlite3.connect(
    "database/mediawiki.db",
    check_same_thread=False
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📈 Insights & Executive Summary")

st.caption(
    "Hallazgos automáticos generados a partir del Data Warehouse."
)

st.divider()

# --------------------------------------------------
# TOP PAGE
# --------------------------------------------------

top_page = pd.read_sql("""

SELECT
    p.page_title,
    SUM(f.count_views) total_views

FROM fact_pageviews f

JOIN dim_page p
ON f.id_page = p.id_page

GROUP BY p.page_title

ORDER BY total_views DESC

LIMIT 1

""", conn)

# --------------------------------------------------
# TOP LANGUAGE
# --------------------------------------------------

top_language = pd.read_sql("""

SELECT
    idioma,
    SUM(f.count_views) total_views

FROM fact_pageviews f

JOIN dim_project p
ON f.id_project = p.id_project

GROUP BY idioma

ORDER BY total_views DESC

LIMIT 1

""", conn)

# --------------------------------------------------
# TOP REGION
# --------------------------------------------------

top_region = pd.read_sql("""

SELECT
    region,
    SUM(f.count_views) total_views

FROM fact_pageviews f

JOIN dim_project p
ON f.id_project = p.id_project

GROUP BY region

ORDER BY total_views DESC

LIMIT 1

""", conn)

# --------------------------------------------------
# TOP DAY
# --------------------------------------------------

top_day = pd.read_sql("""

SELECT
    dia_semana,
    SUM(f.count_views) total_views

FROM fact_pageviews f

JOIN dim_time t
ON f.id_time = t.id_time

GROUP BY dia_semana

ORDER BY total_views DESC

LIMIT 1

""", conn)

# --------------------------------------------------
# KPI INSIGHTS
# --------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "🏆 Página líder",
    top_page.iloc[0]["page_title"]
)

c2.metric(
    "🌎 Idioma líder",
    top_language.iloc[0]["idioma"]
)

c3.metric(
    "🗺️ Región líder",
    top_region.iloc[0]["region"]
)

c4.metric(
    "📅 Día pico",
    top_day.iloc[0]["dia_semana"]
)

st.divider()

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.subheader("📋 Resumen Ejecutivo")

st.markdown(f"""
<div class="insight-card">

### Hallazgo 1

La página con mayor tráfico durante el período analizado fue:

<b>{top_page.iloc[0]['page_title']}</b>

acumulando aproximadamente

<b>{int(top_page.iloc[0]['total_views']):,}</b> visualizaciones.

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-card">

### Hallazgo 2

El idioma con mayor participación fue:

<b>{top_language.iloc[0]['idioma']}</b>

demostrando una concentración importante del tráfico.

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-card">

### Hallazgo 3

La región dominante fue:

<b>{top_region.iloc[0]['region']}</b>

con el mayor volumen agregado de consultas.

</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-card">

### Hallazgo 4

El día con más actividad fue:

<b>{top_day.iloc[0]['dia_semana']}</b>

lo que evidencia patrones temporales en el consumo de contenido.

</div>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# TOP 15 ARTICLES
# --------------------------------------------------

st.subheader("🏆 Ranking Global")

top15 = pd.read_sql("""

SELECT
    p.page_title,
    SUM(f.count_views) total_views

FROM fact_pageviews f

JOIN dim_page p
ON f.id_page = p.id_page

GROUP BY p.page_title

ORDER BY total_views DESC

LIMIT 15

""", conn)

fig = px.bar(
    top15,
    x="total_views",
    y="page_title",
    orientation="h",
    title="Top 15 artículos más consultados"
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# CONCLUSIONS
# --------------------------------------------------

st.subheader("🎯 Conclusiones")

st.success("""
El pipeline ETL permitió integrar datos públicos de Wikimedia,
aplicar procesos de transformación y construir un modelo dimensional
orientado al análisis.
""")

st.info("""
La utilización de un Data Warehouse facilita la generación
de indicadores de negocio y consultas analíticas complejas.
""")

st.warning("""
Los patrones identificados muestran diferencias significativas
entre idiomas, regiones y períodos de tiempo.
""")

conn.close()
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CSS PERSONALIZADO (Animaciones y Glassmorphism)
# --------------------------------------------------

st.markdown("""
<style>

/* Animación de entrada suave */
@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Fondo principal sincronizado con la app */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #334155 100%
    );
}

/* Estilización de los KPIs nativos de Streamlit */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeInUp 0.6s ease-out forwards;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    background: rgba(255, 255, 255, 0.08);
}

/* Estilización de las tarjetas de Insights */
.insight {
    background: rgba(255, 255, 255, 0.05);
    border-left: 5px solid #38bdf8;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    animation: fadeInUp 1s ease-out forwards;
    color: white;
}

.insight:hover {
    transform: scale(1.02);
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 16px rgba(56, 189, 248, 0.15);
}

/* Animación para los contenedores de las gráficas */
.stPlotlyChart {
    animation: fadeInUp 0.8s ease-out forwards;
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
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Filtros")

languages = pd.read_sql("""
SELECT DISTINCT idioma
FROM dim_project
ORDER BY idioma
""", conn)

language_options = ["Todos"] + languages["idioma"].tolist()

selected_language = st.sidebar.selectbox(
    "Idioma",
    language_options
)

where_clause = ""

if selected_language != "Todos":
    where_clause = f"WHERE p.idioma = '{selected_language}'"

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Wikimedia Traffic Dashboard")

st.caption(
    "Análisis interactivo de tráfico Wikimedia basado en Data Warehouse"
)

# --------------------------------------------------
# KPIs
# --------------------------------------------------

kpi_query = f"""
SELECT
SUM(f.count_views) total_views,
COUNT(DISTINCT pg.id_page) total_pages,
COUNT(DISTINCT p.idioma) total_languages,
COUNT(DISTINCT p.region) total_regions
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
JOIN dim_page pg ON f.id_page = pg.id_page
{where_clause}
"""

kpi = pd.read_sql(kpi_query, conn)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👀 Total Views",
    f"{int(kpi['total_views'][0]):,}"
)

c2.metric(
    "📄 Pages",
    f"{int(kpi['total_pages'][0]):,}"
)

c3.metric(
    "🌎 Languages",
    f"{int(kpi['total_languages'][0]):,}"
)

c4.metric(
    "🗺️ Regions",
    f"{int(kpi['total_regions'][0]):,}"
)

st.divider()

# --------------------------------------------------
# TOP PAGES
# --------------------------------------------------

top_pages = pd.read_sql(f"""
SELECT
pg.page_title,
SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_page pg ON f.id_page = pg.id_page
JOIN dim_project p ON f.id_project = p.id_project
{where_clause}
GROUP BY pg.page_title
ORDER BY total_views DESC
LIMIT 10
""", conn)

fig_top = px.bar(
    top_pages,
    x="total_views",
    y="page_title",
    orientation="h",
    title="🏆 Top 10 páginas más visitadas"
)

# Fondo transparente para integrar con el CSS
fig_top.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# --------------------------------------------------
# LANGUAGE DISTRIBUTION
# --------------------------------------------------

lang_df = pd.read_sql("""
SELECT
idioma,
SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
GROUP BY idioma
""", conn)

fig_lang = px.pie(
    lang_df,
    names="idioma",
    values="total_views",
    title="🌍 Distribución por idioma"
)

fig_lang.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# --------------------------------------------------
# REGION DISTRIBUTION
# --------------------------------------------------

region_df = pd.read_sql("""
SELECT
region,
SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
GROUP BY region
""", conn)

fig_region = px.bar(
    region_df,
    x="region",
    y="total_views",
    title="🗺️ Tráfico por región"
)

fig_region.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# --------------------------------------------------
# DAY OF WEEK
# --------------------------------------------------

day_df = pd.read_sql("""
SELECT
t.dia_semana,
SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_time t ON f.id_time = t.id_time
GROUP BY t.dia_semana
""", conn)

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_df["dia_semana"] = pd.Categorical(
    day_df["dia_semana"],
    categories=days,
    ordered=True
)

day_df = day_df.sort_values("dia_semana")

fig_day = px.line(
    day_df,
    x="dia_semana",
    y="total_views",
    markers=True,
    title="📈 Tráfico por día de la semana"
)

fig_day.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_top,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig_lang,
        use_container_width=True
    )

left2, right2 = st.columns(2)

with left2:
    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

with right2:
    st.plotly_chart(
        fig_day,
        use_container_width=True
    )

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader("🔎 Insights Automáticos")

top_article = top_pages.iloc[0]["page_title"]
top_views = int(top_pages.iloc[0]["total_views"])

top_language = lang_df.sort_values(
    "total_views",
    ascending=False
).iloc[0]["idioma"]

st.markdown(f"""
<div class="insight">
<b>Página líder:</b> {top_article}
<br><br>
Acumuló aproximadamente <b>{top_views:,}</b> visualizaciones.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight">
<b>Idioma dominante:</b> {top_language}
<br><br>
Es el idioma con mayor volumen de tráfico dentro del período analizado.
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.divider()

st.subheader("📄 Top artículos")

st.dataframe(
    top_pages,
    use_container_width=True
)

conn.close()
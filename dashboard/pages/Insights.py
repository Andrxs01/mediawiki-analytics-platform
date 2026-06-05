import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
 
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
 
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');
 
.stApp {
    background:
        radial-gradient(ellipse at 10% 20%, rgba(56,189,248,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(99,102,241,0.08) 0%, transparent 50%),
        linear-gradient(160deg, #020617 0%, #0f172a 50%, #1e293b 100%);
    font-family: 'Sora', sans-serif;
}
 
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 15% 25%, rgba(148,163,184,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 60%, rgba(148,163,184,0.3) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 60% 15%, rgba(56,189,248,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 50%, rgba(148,163,184,0.3) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 25% 80%, rgba(99,102,241,0.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 88%, rgba(148,163,184,0.3) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
    animation: twinkle 9s ease-in-out infinite alternate;
}
@keyframes twinkle { 0% { opacity:0.5; } 100% { opacity:1; } }
 
/* ── Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 16px;
    padding: 20px 24px !important;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    animation: fadeSlideUp 0.6s ease both;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(56,189,248,0.15), 0 0 0 1px rgba(56,189,248,0.4);
    border-color: rgba(56,189,248,0.5);
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.06), transparent);
    animation: shimmer 3.5s ease-in-out infinite;
}
[data-testid="metric-container"]:nth-child(2)::before { animation-delay: 0.6s; }
[data-testid="metric-container"]:nth-child(3)::before { animation-delay: 1.2s; }
[data-testid="metric-container"]:nth-child(4)::before { animation-delay: 1.8s; }
@keyframes shimmer { 0% { left:-100%; } 100% { left:200%; } }
 
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em;
    color: rgba(148,163,184,0.9) !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
 
h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #f1f5f9 !important;
    animation: fadeSlideUp 0.5s ease both;
}
 
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
 
hr {
    border: none !important;
    border-top: 1px solid rgba(56,189,248,0.12) !important;
    margin: 2rem 0 !important;
}
 
/* ── Insight Cards ── */
.insight-card {
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 14px;
    border-left: 4px solid #38bdf8;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    animation: fadeSlideUp 0.6s ease both;
}
.insight-card:nth-child(2) { animation-delay:0.1s; border-left-color:#818cf8; }
.insight-card:nth-child(3) { animation-delay:0.2s; border-left-color:#34d399; }
.insight-card:nth-child(4) { animation-delay:0.3s; border-left-color:#fbbf24; }
 
.insight-card:hover {
    transform: translateX(5px);
    box-shadow: -4px 0 24px rgba(56,189,248,0.12);
    border-left-width: 6px;
}
 
.insight-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 100%;
    background: linear-gradient(to left, rgba(56,189,248,0.03), transparent);
    pointer-events: none;
}
 
.insight-card h3 {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.15em;
    color: #38bdf8 !important;
    text-transform: uppercase;
    margin-bottom: 8px;
    animation: none !important;
}
.insight-card:nth-child(2) h3 { color: #818cf8 !important; }
.insight-card:nth-child(3) h3 { color: #34d399 !important; }
.insight-card:nth-child(4) h3 { color: #fbbf24 !important; }
 
.insight-card p {
    font-family: 'Sora', sans-serif;
    font-size: 14px;
    color: rgba(203,213,225,0.85);
    line-height: 1.7;
    margin: 0;
}
.insight-card b {
    color: #f1f5f9;
    font-weight: 700;
}
 
/* ── Conclusion boxes ── */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: none !important;
    animation: fadeSlideUp 0.6s ease both;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
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
st.caption("Hallazgos automáticos generados a partir del Data Warehouse.")
st.divider()
 
# --------------------------------------------------
# QUERIES
# --------------------------------------------------
 
top_page = pd.read_sql("""
SELECT p.page_title, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_page p ON f.id_page = p.id_page
GROUP BY p.page_title ORDER BY total_views DESC LIMIT 1
""", conn)
 
top_language = pd.read_sql("""
SELECT idioma, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
GROUP BY idioma ORDER BY total_views DESC LIMIT 1
""", conn)
 
top_region = pd.read_sql("""
SELECT region, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
GROUP BY region ORDER BY total_views DESC LIMIT 1
""", conn)
 
top_day = pd.read_sql("""
SELECT dia_semana, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_time t ON f.id_time = t.id_time
GROUP BY dia_semana ORDER BY total_views DESC LIMIT 1
""", conn)
 
# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
 
c1,c2,c3,c4 = st.columns(4)
c1.metric("🏆 Página líder",  top_page.iloc[0]["page_title"])
c2.metric("🌎 Idioma líder",  top_language.iloc[0]["idioma"])
c3.metric("🗺️ Región líder", top_region.iloc[0]["region"])
c4.metric("📅 Día pico",      top_day.iloc[0]["dia_semana"])
 
st.divider()
 
# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------
 
st.subheader("📋 Resumen Ejecutivo")
 
st.markdown(f"""
<div class="insight-card">
<h3>Hallazgo 1 — Página Líder</h3>
<p>La página con mayor tráfico durante el período analizado fue
<b>{top_page.iloc[0]['page_title']}</b>,
acumulando aproximadamente
<b>{int(top_page.iloc[0]['total_views']):,}</b> visualizaciones.</p>
</div>
""", unsafe_allow_html=True)
 
st.markdown(f"""
<div class="insight-card">
<h3>Hallazgo 2 — Idioma Dominante</h3>
<p>El idioma con mayor participación fue
<b>{top_language.iloc[0]['idioma']}</b>,
demostrando una concentración importante del tráfico en esa lengua.</p>
</div>
""", unsafe_allow_html=True)
 
st.markdown(f"""
<div class="insight-card">
<h3>Hallazgo 3 — Región Líder</h3>
<p>La región dominante fue
<b>{top_region.iloc[0]['region']}</b>,
con el mayor volumen agregado de consultas a lo largo del período.</p>
</div>
""", unsafe_allow_html=True)
 
st.markdown(f"""
<div class="insight-card">
<h3>Hallazgo 4 — Patrón Temporal</h3>
<p>El día con más actividad fue
<b>{top_day.iloc[0]['dia_semana']}</b>,
lo que evidencia patrones temporales claros en el consumo de contenido.</p>
</div>
""", unsafe_allow_html=True)
 
st.divider()
 
# --------------------------------------------------
# TOP 15 ARTICLES
# --------------------------------------------------
 
st.subheader("🏆 Ranking Global")
 
top15 = pd.read_sql("""
SELECT p.page_title, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_page p ON f.id_page = p.id_page
GROUP BY p.page_title ORDER BY total_views DESC LIMIT 15
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
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora, sans-serif", color="#cbd5e1"),
    title_font=dict(size=16, color="#f1f5f9"),
    yaxis=dict(
        categoryorder="total ascending",
        tickfont=dict(family="Space Mono, monospace", size=11)
    ),
    xaxis=dict(gridcolor="rgba(56,189,248,0.08)"),
)
fig.update_traces(
    marker_color=[
        f"rgba({int(56 + (99-56)*i/14)},{int(189 + (102-189)*i/14)},{int(248 + (241-248)*i/14)},0.85)"
        for i in range(15)
    ],
    hovertemplate="<b>%{y}</b><br>Views: %{x:,}<extra></extra>"
)
 
st.plotly_chart(fig, use_container_width=True)
 
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

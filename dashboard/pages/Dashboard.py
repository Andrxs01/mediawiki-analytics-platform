import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

/* ── Base ── */
.stApp {
    background:
        radial-gradient(ellipse at 10% 20%, rgba(56,189,248,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(99,102,241,0.07) 0%, transparent 50%),
        linear-gradient(160deg, #020617 0%, #0f172a 55%, #1e293b 100%);
    font-family: 'Sora', sans-serif;
}
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 8%  12%, rgba(148,163,184,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 35% 55%, rgba(148,163,184,0.25) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 60% 18%, rgba(56,189,248,0.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 78% 70%, rgba(148,163,184,0.25) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 22% 85%, rgba(99,102,241,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 40%, rgba(148,163,184,0.35) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
    animation: twinkle 10s ease-in-out infinite alternate;
}
@keyframes twinkle { 0% { opacity:0.5; } 100% { opacity:1; } }

hr {
    border: none !important;
    border-top: 1px solid rgba(56,189,248,0.12) !important;
    margin: 2rem 0 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 16px;
    padding: 20px 22px !important;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    animation: fadeSlideUp 0.6s ease both;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 36px rgba(56,189,248,0.14), 0 0 0 1px rgba(56,189,248,0.4);
    border-color: rgba(56,189,248,0.45);
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 55%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.06), transparent);
    animation: shimmer 3.5s ease-in-out infinite;
}
[data-testid="stMetric"]:nth-child(2)::before { animation-delay: 0.7s; }
[data-testid="stMetric"]:nth-child(3)::before { animation-delay: 1.4s; }
[data-testid="stMetric"]:nth-child(4)::before { animation-delay: 2.1s; }
@keyframes shimmer { 0% { left:-100%; } 100% { left:200%; } }

[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em;
    color: rgba(148,163,184,0.85) !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Titles ── */
h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #f1f5f9 !important;
    animation: fadeSlideUp 0.5s ease both;
}

@keyframes fadeSlideUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── Sidebar (CORREGIDO: Sin selectores universales que rompan iconos nativos) ── */
[data-testid="stSidebar"] {
    background: rgba(2,6,23,0.85) !important;
    border-right: 1px solid rgba(56,189,248,0.1) !important;
}
[data-testid="stSidebar"] h1 {
    font-size: 15px !important;
    font-family: 'Space Mono', monospace !important;
    color: #38bdf8 !important;
    letter-spacing: 0.05em;
}
[data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] p {
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stSelectbox"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em;
    color: rgba(148,163,184,0.8) !important;
    text-transform: uppercase;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(56,189,248,0.15);
    animation: fadeSlideUp 0.7s ease both;
    transition: box-shadow 0.3s ease;
}
[data-testid="stDataFrame"]:hover {
    box-shadow: 0 6px 28px rgba(56,189,248,0.09);
}

/* ── Plotly charts wrapper ── */
[data-testid="stPlotlyChart"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(56,189,248,0.1);
    animation: fadeSlideUp 0.8s ease both;
    transition: box-shadow 0.3s ease;
    background: rgba(255,255,255,0.02);
}
[data-testid="stPlotlyChart"]:hover {
    box-shadow: 0 8px 32px rgba(56,189,248,0.1);
    border-color: rgba(56,189,248,0.2);
}

/* ── Insight cards ── */
.insight {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #38bdf8;
    border-top: 1px solid rgba(255,255,255,0.07);
    border-right: 1px solid rgba(255,255,255,0.07);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 20px 24px;
    border-radius: 14px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeSlideUp 0.7s ease both;
    color: #e2e8f0;
    font-family: 'Sora', sans-serif;
    font-size: 14px;
    line-height: 1.7;
}
.insight:nth-child(2) { border-left-color: #818cf8; animation-delay: 0.1s; }
.insight:hover {
    transform: translateX(5px);
    background: rgba(56,189,248,0.07);
    box-shadow: -4px 0 20px rgba(56,189,248,0.1);
    border-left-width: 6px;
}
.insight b { color: #f1f5f9; font-weight: 700; }

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    color: rgba(148,163,184,0.5) !important;
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
SELECT DISTINCT idioma FROM dim_project ORDER BY idioma
""", conn)

language_options = ["Todos"] + languages["idioma"].tolist()

selected_language = st.sidebar.selectbox("Idioma", language_options)

where_clause = ""
if selected_language != "Todos":
    where_clause = f"WHERE p.idioma = '{selected_language}'"

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Wikimedia Traffic Dashboard")
st.caption("Análisis interactivo de tráfico Wikimedia basado en Data Warehouse")

# --------------------------------------------------
# KPIs
# --------------------------------------------------

kpi = pd.read_sql(f"""
SELECT
    SUM(f.count_views)         total_views,
    COUNT(DISTINCT pg.id_page) total_pages,
    COUNT(DISTINCT p.idioma)   total_languages,
    COUNT(DISTINCT p.region)   total_regions
FROM fact_pageviews f
JOIN dim_project p  ON f.id_project = p.id_project
JOIN dim_page    pg ON f.id_page    = pg.id_page
{where_clause}
""", conn)

c1,c2,c3,c4 = st.columns(4)
c1.metric("👀 Total Views",  f"{int(kpi['total_views'][0]):,}")
c2.metric("📄 Pages",        f"{int(kpi['total_pages'][0]):,}")
c3.metric("🌎 Languages",    f"{int(kpi['total_languages'][0]):,}")
c4.metric("🗺️ Regions",     f"{int(kpi['total_regions'][0]):,}")

st.divider()

# --------------------------------------------------
# QUERIES
# --------------------------------------------------

top_pages = pd.read_sql(f"""
SELECT pg.page_title, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_page    pg ON f.id_page    = pg.id_page
JOIN dim_project p  ON f.id_project = p.id_project
{where_clause}
GROUP BY pg.page_title ORDER BY total_views DESC LIMIT 10
""", conn)

lang_df = pd.read_sql("""
SELECT idioma, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
GROUP BY idioma
""", conn)

region_df = pd.read_sql("""
SELECT region, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_project p ON f.id_project = p.id_project
GROUP BY region
""", conn)

day_df = pd.read_sql("""
SELECT t.dia_semana, SUM(f.count_views) total_views
FROM fact_pageviews f
JOIN dim_time t ON f.id_time = t.id_time
GROUP BY t.dia_semana
""", conn)

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_df["dia_semana"] = pd.Categorical(day_df["dia_semana"], categories=days, ordered=True)
day_df = day_df.sort_values("dia_semana")

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

LAYOUT_BASE = dict(
    template="plotly_dark",
    height=480,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora, sans-serif", color="#cbd5e1", size=12),
    title_font=dict(size=15, color="#f1f5f9", family="Sora, sans-serif"),
    margin=dict(l=16, r=16, t=48, b=16),
)

# Top pages
fig_top = px.bar(top_pages, x="total_views", y="page_title",
                 orientation="h", title="🏆 Top 10 páginas más visitadas")
fig_top.update_layout(**LAYOUT_BASE,
    yaxis=dict(categoryorder="total ascending",
               tickfont=dict(family="Space Mono, monospace", size=10)),
    xaxis=dict(gridcolor="rgba(56,189,248,0.07)"))
fig_top.update_traces(
    marker_color=[
        f"rgba({int(56+(99-56)*i/9)},{int(189+(102-189)*i/9)},{int(248+(241-248)*i/9)},0.82)"
        for i in range(len(top_pages))
    ],
    hovertemplate="<b>%{y}</b><br>Views: %{x:,}<extra></extra>"
)

# Language pie
fig_lang = px.pie(lang_df, names="idioma", values="total_views",
                  title="🌍 Distribución por idioma",
                  color_discrete_sequence=px.colors.sequential.Blues_r)
fig_lang.update_layout(**LAYOUT_BASE)
fig_lang.update_traces(textfont=dict(family="Space Mono, monospace", size=11),
                       hovertemplate="<b>%{label}</b><br>%{value:,}<extra></extra>")

# Region bar
fig_region = px.bar(region_df, x="region", y="total_views",
                    title="🗺️ Tráfico por región",
                    color="total_views",
                    color_continuous_scale=[[0,"rgba(99,102,241,0.5)"],
                                            [1,"rgba(56,189,248,0.9)"]])
fig_region.update_layout(**LAYOUT_BASE,
    coloraxis_showscale=False,
    xaxis=dict(tickfont=dict(family="Space Mono, monospace", size=10)),
    yaxis=dict(gridcolor="rgba(56,189,248,0.07)"))
fig_region.update_traces(hovertemplate="<b>%{x}</b><br>Views: %{y:,}<extra></extra>")

# Day line
fig_day = px.line(day_df, x="dia_semana", y="total_views",
                  markers=True, title="📈 Tráfico por día de la semana")
fig_day.update_layout(**LAYOUT_BASE,
    xaxis=dict(tickfont=dict(family="Space Mono, monospace", size=10)),
    yaxis=dict(gridcolor="rgba(56,189,248,0.07)"))
fig_day.update_traces(
    line=dict(color="#38bdf8", width=2.5),
    marker=dict(size=8, color="#818cf8",
                line=dict(color="#38bdf8", width=2)),
    hovertemplate="<b>%{x}</b><br>Views: %{y:,}<extra></extra>"
)

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------

left, right = st.columns(2)
with left:  st.plotly_chart(fig_top,    use_container_width=True)
with right: st.plotly_chart(fig_lang,   use_container_width=True)

left2, right2 = st.columns(2)
with left2:  st.plotly_chart(fig_region, use_container_width=True)
with right2: st.plotly_chart(fig_day,    use_container_width=True)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.divider()
st.subheader("🔎 Insights Automáticos")

top_article = top_pages.iloc[0]["page_title"]
top_views   = int(top_pages.iloc[0]["total_views"])
top_language = lang_df.sort_values("total_views", ascending=False).iloc[0]["idioma"]

st.markdown(f"""
<div class="insight">
<b>Página líder:</b> {top_article}<br><br>
Acumuló aproximadamente <b>{top_views:,}</b> visualizaciones durante el período analizado.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight">
<b>Idioma dominante:</b> {top_language}<br><br>
Es el idioma con mayor volumen de tráfico dentro del período analizado.
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.divider()
st.subheader("📄 Top artículos")
st.dataframe(top_pages, use_container_width=True)

conn.close()
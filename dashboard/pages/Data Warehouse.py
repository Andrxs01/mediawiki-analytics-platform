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
        radial-gradient(1px 1px at 10% 15%, rgba(148,163,184,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 45%, rgba(148,163,184,0.3) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 55% 20%, rgba(56,189,248,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 60%, rgba(148,163,184,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 10%, rgba(148,163,184,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 20% 80%, rgba(99,102,241,0.4) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
    animation: twinkle 8s ease-in-out infinite alternate;
}

@keyframes twinkle {
    0%   { opacity: 0.5; }
    100% { opacity: 1; }
}

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
    animation: shimmer 3s ease-in-out infinite;
}
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
    font-size: 2rem !important;
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

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(56,189,248,0.15);
    animation: fadeSlideUp 0.7s ease both;
    transition: box-shadow 0.3s ease;
}
[data-testid="stDataFrame"]:hover {
    box-shadow: 0 8px 32px rgba(56,189,248,0.1);
}

hr {
    border: none !important;
    border-top: 1px solid rgba(56,189,248,0.12) !important;
    margin: 2rem 0 !important;
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── HTML Star Schema styles (A PRUEBA DE FALLOS) ── */
.schema-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0;
    animation: fadeSlideUp 0.8s ease both;
}
.schema-row {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: nowrap;
}
@media (max-width: 768px) {
    .schema-row { flex-direction: column; }
    .conn-wrapper-h { transform: rotate(90deg); margin: 20px 0; }
}
.schema-box {
    background: rgba(15,23,42,0.9);
    border-radius: 14px;
    padding: 16px 22px;
    text-align: center;
    position: relative;
    z-index: 2;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.schema-box:hover {
    transform: translateY(-4px);
}
.dim-box {
    border: 1px solid rgba(148,163,184,0.3);
    width: 170px;
}
.dim-box:hover {
    border-color: rgba(56,189,248,0.5);
    box-shadow: 0 8px 25px rgba(56,189,248,0.1);
}
.fact-box {
    background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95));
    border: 2px solid #38bdf8;
    width: 210px;
    box-shadow: 0 0 20px rgba(56,189,248,0.15);
}
.fact-box:hover {
    box-shadow: 0 0 30px rgba(56,189,248,0.3);
}
.box-tag {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    color: #38bdf8;
    margin-bottom: 4px;
}
.box-title {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #f1f5f9;
    margin-bottom: 8px;
}
.box-divider {
    margin: 8px 0;
    border: none;
    border-top: 1px solid rgba(148,163,184,0.2);
}
.box-field {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: rgba(148,163,184,0.8);
    margin: 4px 0;
}
.fact-field {
    color: rgba(199,210,254,0.9);
    font-weight: 600;
}

/* Conectores Animados */
.conn-wrapper-v {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    height: 60px;
    width: 100px;
}
.conn-label-v {
    position: absolute;
    left: 55%;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #38bdf8;
    background: rgba(15,23,42,0.8);
    padding: 2px 6px;
    border-radius: 4px;
}
.conn-wrapper-h {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    width: 70px;
    height: 50px;
}
.conn-label-h {
    position: absolute;
    top: -5px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #38bdf8;
    background: rgba(15,23,42,0.8);
    padding: 2px 6px;
    border-radius: 4px;
}
.conn-v {
    height: 100%; width: 2px;
    background: linear-gradient(to bottom, #38bdf8 50%, transparent 50%);
    background-size: 100% 12px;
    animation: flow-v 1s linear infinite;
    opacity: 0.8;
}
.conn-h-left {
    width: 100%; height: 2px;
    background: linear-gradient(to right, #38bdf8 50%, transparent 50%);
    background-size: 12px 100%;
    animation: flow-h-left 1s linear infinite;
    opacity: 0.8;
}
.conn-h-right {
    width: 100%; height: 2px;
    background: linear-gradient(to left, #38bdf8 50%, transparent 50%);
    background-size: 12px 100%;
    animation: flow-h-right 1s linear infinite;
    opacity: 0.8;
}

@keyframes flow-v { from { background-position: 0 0; } to { background-position: 0 12px; } }
@keyframes flow-h-left { from { background-position: 0 0; } to { background-position: 12px 0; } }
@keyframes flow-h-right { from { background-position: 0 0; } to { background-position: 12px 0; } }

/* ── ETL Pipeline ── */
.etl-pipe {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    padding: 10px 0;
    animation: fadeSlideUp 0.8s ease both;
}
.etl-node {
    width: 100%;
    max-width: 520px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 14px;
    padding: 14px 22px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: all 0.3s ease;
    cursor: default;
}
.etl-node:hover {
    background: rgba(56,189,248,0.09);
    border-color: rgba(56,189,248,0.55);
    transform: translateX(6px);
    box-shadow: -4px 0 24px rgba(56,189,248,0.13);
}
.etl-icon {
    width: 42px; height: 42px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(56,189,248,0.18), rgba(99,102,241,0.18));
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.etl-text { font-family:'Sora',sans-serif; font-size:14px; font-weight:600; color:#e2e8f0; }
.etl-sub  { font-family:'Space Mono',monospace; font-size:11px; color:rgba(148,163,184,0.6); margin-top:2px; }

.etl-arrow {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 38px;
    position: relative;
    overflow: visible;
}
.etl-line {
    width: 2px; flex: 1;
    background: linear-gradient(to bottom, rgba(56,189,248,0.6), rgba(99,102,241,0.5));
    position: relative; overflow: hidden;
}
.etl-dot {
    position: absolute;
    width: 6px; height: 6px;
    background: #38bdf8;
    border-radius: 50%;
    left: -2px;
    animation: flowDot 2s ease-in-out infinite;
}
@keyframes flowDot {
    0%   { top:0%;   opacity:0; }
    10%  { opacity:1; }
    90%  { opacity:1; }
    100% { top:100%; opacity:0; }
}
.etl-tip {
    width:0; height:0;
    border-left:5px solid transparent;
    border-right:5px solid transparent;
    border-top:7px solid rgba(56,189,248,0.65);
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
st.caption("Modelo dimensional construido a partir del proceso ETL.")
st.divider()

# -------------------------------------
# TABLE COUNTS
# -------------------------------------

dim_project = pd.read_sql("SELECT COUNT(*) total FROM dim_project", conn)
dim_page    = pd.read_sql("SELECT COUNT(*) total FROM dim_page", conn)
dim_time    = pd.read_sql("SELECT COUNT(*) total FROM dim_time", conn)
fact        = pd.read_sql("SELECT COUNT(*) total FROM fact_pageviews", conn)

c1,c2,c3,c4 = st.columns(4)
c1.metric("🌎 DimProject",   f"{int(dim_project.iloc[0,0]):,}")
c2.metric("📄 DimPage",      f"{int(dim_page.iloc[0,0]):,}")
c3.metric("📅 DimTime",      f"{int(dim_time.iloc[0,0]):,}")
c4.metric("📊 FactPageviews",f"{int(fact.iloc[0,0]):,}")

st.divider()

# -------------------------------------
# STAR SCHEMA
# -------------------------------------

st.subheader("⭐ Modelo Estrella")

# Despliegue optimizado de la imagen remota manteniendo la estética limpia
st.image("https://i.postimg.cc/8cbnq6zw/modeloestrella.jpg", use_container_width=True)

st.divider()

# -------------------------------------
# ETL FLOW
# -------------------------------------

st.subheader("⚙️ Flujo ETL")

def etl_arrow(delay):
    return f"""
<div class="etl-arrow">
  <div class="etl-line">
    <div class="etl-dot" style="animation-delay:{delay}s;"></div>
  </div>
  <div class="etl-tip"></div>
</div>"""

etl_nodes = [
    ("🌐", "Wikimedia API",             "Fuente pública de datos de pageviews"),
    ("📦", "Raw Dataset",               "Extracción y almacenamiento temporal de datos crudos"),
    ("⚗️",  "Transformación y Limpieza", "Normalización, deduplicación y mapeo de dimensiones"),
    ("🗄️", "Data Warehouse SQLite",     "Carga al modelo estrella: fact + dimensiones"),
    ("🔍", "Consultas SQL",             "Agregaciones y análisis sobre el warehouse"),
    ("📊", "Dashboard Streamlit",       "Visualización interactiva del modelo dimensional"),
]

etl_html = '<div class="etl-pipe">'
for i, (icon, title, sub) in enumerate(etl_nodes):
    etl_html += f"""
<div class="etl-node">
  <div class="etl-icon">{icon}</div>
  <div>
    <div class="etl-text">{title}</div>
    <div class="etl-sub">{sub}</div>
  </div>
</div>"""
    if i < len(etl_nodes) - 1:
        etl_html += etl_arrow(i * 0.35)

etl_html += "</div>"
st.markdown(etl_html, unsafe_allow_html=True)

st.divider()

# -------------------------------------
# SAMPLE DATA
# -------------------------------------

st.subheader("📄 Vista previa de Fact Table")

sample = pd.read_sql("SELECT * FROM fact_pageviews LIMIT 20", conn)
st.dataframe(sample, use_container_width=True)

st.divider()

# -------------------------------------
# QUALITY METRICS
# -------------------------------------

st.subheader("✅ Calidad de Datos")

quality = pd.DataFrame({
    "Métrica":  ["Registros Fact", "Proyectos", "Páginas", "Fechas"],
    "Cantidad": [
        int(fact.iloc[0,0]),
        int(dim_project.iloc[0,0]),
        int(dim_page.iloc[0,0]),
        int(dim_time.iloc[0,0])
    ]
})

st.dataframe(quality, use_container_width=True)

conn.close()
import streamlit as st

st.set_page_config(
    page_title="MediaWiki Analytics Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700;800&display=swap');

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
        radial-gradient(1px 1px at 8%  12%, rgba(148,163,184,0.45) 0%, transparent 100%),
        radial-gradient(1px 1px at 28% 55%, rgba(148,163,184,0.25) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 52% 18%, rgba(56,189,248,0.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 73% 65%, rgba(148,163,184,0.25) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 8%,  rgba(148,163,184,0.45) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 18% 82%, rgba(99,102,241,0.35) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
    animation: twinkle 9s ease-in-out infinite alternate;
}
@keyframes twinkle { 0% { opacity:0.5; } 100% { opacity:1; } }

hr {
    border: none !important;
    border-top: 1px solid rgba(56,189,248,0.12) !important;
    margin: 2rem 0 !important;
}

@keyframes fadeInUp {
    from { opacity:0; transform:translateY(28px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes shimmer { 0% { left:-100%; } 100% { left:200%; } }

/* Contenedor Hero para asegurar centrado absoluto */
.hero-container {
    text-align: center;
    width: 100%;
    margin: 0 auto;
}

.main-title {
    text-align: center;
    font-family: 'Sora', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f1f5f9 30%, #38bdf8 65%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeInUp 0.7s ease-out forwards;
    letter-spacing: -0.5px;
    line-height: 1.15;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.subtitle {
    text-align: center;
    color: rgba(148,163,184,0.9);
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 300;
    animation: fadeInUp 0.9s ease-out forwards;
    max-width: 800px;
    margin: 14px auto 0;
    line-height: 1.65;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(56,189,248,0.15);
    padding: 28px 28px 24px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    color: white;
    margin-top: 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    animation: fadeInUp 1s ease-out forwards;
    font-family: 'Sora', sans-serif;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 55%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.05), transparent);
    animation: shimmer 4s ease-in-out infinite;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.35), 0 0 0 1px rgba(56,189,248,0.3);
    border-color: rgba(56,189,248,0.35);
}
.card h2 {
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 12px;
}
.card p { font-size:14px; color:rgba(203,213,225,0.82); line-height:1.7; }

/* Architecture pipeline */
.arch-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 28px 16px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 18px;
    animation: fadeInUp 1.1s ease-out forwards;
    gap: 0;
}
.arch-node {
    width: 100%;
    max-width: 460px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 12px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 13px;
    transition: all 0.3s ease;
    cursor: default;
}
.arch-node:hover {
    background: rgba(56,189,248,0.08);
    border-color: rgba(56,189,248,0.5);
    transform: translateX(5px);
    box-shadow: -3px 0 20px rgba(56,189,248,0.12);
}
.arch-icon {
    width: 38px; height: 38px;
    border-radius: 9px;
    background: linear-gradient(135deg, rgba(56,189,248,0.18), rgba(99,102,241,0.18));
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.arch-text { font-family:'Sora',sans-serif; font-size:14px; font-weight:600; color:#e2e8f0; }
.arch-sub  { font-family:'Space Mono',monospace; font-size:10px; color:rgba(148,163,184,0.55); margin-top:2px; }

/* SVG arrow connector between nodes */
.arch-connector {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 38px;
    width: 100%;
    max-width: 460px;
}

/* Tech cards */
.tech-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.14);
    padding: 16px 12px;
    border-radius: 14px;
    text-align: center;
    color: #e2e8f0;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.05em;
    transition: all 0.3s ease;
    animation: fadeInUp 1.2s ease-out forwards;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: 110px;
}
.tech-card:hover {
    transform: translateY(-5px) scale(1.04);
    border-color: rgba(56,189,248,0.45);
    box-shadow: 0 10px 28px rgba(0,0,0,0.3), 0 0 0 1px rgba(56,189,248,0.2);
    background: rgba(56,189,248,0.07);
}
.tech-logo { width:42px; height:42px; object-fit:contain; filter:drop-shadow(0 2px 6px rgba(56,189,248,0.2)); }
.wiki-logo { width:56px; margin-bottom:6px; filter:drop-shadow(0 2px 8px rgba(56,189,248,0.25)); }

[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    animation: fadeInUp 0.8s ease-out both;
}
h2 {
    font-family: 'Sora', sans-serif !important;
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    animation: fadeInUp 0.5s ease both;
}
[data-testid="stCaptionContainer"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    color: rgba(148,163,184,0.45) !important;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO (CORREGIDO: Centrado Absoluto)
# -------------------------

st.markdown("""
<div class="hero-container">
    <h1 class="main-title">
        <img src="https://d3ogvqw9m2inp7.cloudfront.net/assets/dynamic/assets/recruiters/images/1233996/logo.png"
             style="width:54px; vertical-align:middle; margin-right:14px; filter:drop-shadow(0 0 12px rgba(56,189,248,0.4));">
        MediaWiki Analytics Platform
    </h1>
    <p class="subtitle" style="text-align: center;">
     Plataforma de análisis de tráfico Wikimedia basada en ETL automatizado, Data Warehouse y Business Intelligence.
</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------
# PRESENTACIÓN
# -------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="card">
    <h2>🚀 Objetivo del Proyecto</h2>
    <p>
    Extraer, transformar y analizar información pública proveniente de Wikimedia
    utilizando un pipeline ETL automatizado.<br><br>
    Los datos son obtenidos desde la API oficial de Wikimedia, procesados mediante
    Pandas y almacenados en un Data Warehouse SQLite para su posterior explotación analítica.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="text-align:center;">
    <h2>📊 Fuente</h2>
    <img src="https://d3ogvqw9m2inp7.cloudfront.net/assets/dynamic/assets/recruiters/images/1233996/logo.png"
         class="wiki-logo"><br>
    <span style="font-family:'Space Mono',monospace;font-size:13px;color:#38bdf8;font-weight:700;">Wikimedia API</span>
    <br><br>
    <span style="font-size:13px;color:rgba(148,163,184,0.8);">Actualización automática</span>
    <br>
    <span style="font-size:13px;color:rgba(148,163,184,0.8);">Datos reales</span>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# ARQUITECTURA
# -------------------------

st.markdown("## ⚙️ Arquitectura del Proyecto")

def svg_arrow(delay_ms: int) -> str:
    return f"""
<div class="arch-connector">
  <svg viewBox="0 0 40 38" xmlns="http://www.w3.org/2000/svg"
       style="width:40px;height:38px;overflow:visible;">
    <defs>
      <linearGradient id="ag{delay_ms}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%"   stop-color="#38bdf8" stop-opacity="0.7"/>
        <stop offset="100%" stop-color="#818cf8" stop-opacity="0.7"/>
      </linearGradient>
    </defs>
    <line x1="20" y1="2" x2="20" y2="26"
          stroke="url(#ag{delay_ms})" stroke-width="2"
          stroke-dasharray="5 3">
      <animate attributeName="stroke-dashoffset" from="0" to="-16"
               dur="1.4s" repeatCount="indefinite"/>
    </line>
    <polygon points="14,24 26,24 20,34"
             fill="rgba(56,189,248,0.65)"/>
    <circle r="3" fill="#38bdf8" opacity="0">
      <animateMotion path="M20,2 L20,26" dur="1.4s"
                     begin="{delay_ms}ms" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0" dur="1.4s"
               begin="{delay_ms}ms" repeatCount="indefinite"/>
    </circle>
  </svg>
</div>"""

arch_steps = [
    ("🌐", "API Wikimedia",          "Fuente de datos pública"),
    ("📥", "Extract",                "Llamadas HTTP a la REST API"),
    ("🔬", "Transform",              "Limpieza y normalización con Pandas"),
    ("🗄️", "SQLite Data Warehouse",  "Modelo estrella persistente"),
    ("🔍", "SQL Analytics",          "Consultas agregadas y KPIs"),
    ("📊", "Streamlit Dashboard",    "Visualización interactiva"),
]

arch_html = '<div class="arch-wrap">'
for i, (icon, title, sub) in enumerate(arch_steps):
    arch_html += f"""
<div class="arch-node">
  <div class="arch-icon">{icon}</div>
  <div>
    <div class="arch-text">{title}</div>
    <div class="arch-sub">{sub}</div>
  </div>
</div>"""
    if i < len(arch_steps) - 1:
        arch_html += svg_arrow(i * 250)
arch_html += "</div>"

st.markdown(arch_html, unsafe_allow_html=True)

# -------------------------
# TECNOLOGÍAS
# -------------------------

st.markdown("## 🛠️ Tecnologías Utilizadas")

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    st.markdown('''<div class="tech-card">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" class="tech-logo">
    Python</div>''', unsafe_allow_html=True)
with c2:
    st.markdown('''<div class="tech-card">
    <img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" class="tech-logo">
    Pandas</div>''', unsafe_allow_html=True)
with c3:
    st.markdown('''<div class="tech-card">
    <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg" class="tech-logo" style="width:72px;">
    SQLite</div>''', unsafe_allow_html=True)
with c4:
    st.markdown('''<div class="tech-card">
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/Plotly_logo_for_digital_final_%286%29.png" class="tech-logo">
    Plotly</div>''', unsafe_allow_html=True)
with c5:
    st.markdown('''<div class="tech-card">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Wikimedia-logo.svg/1024px-Wikimedia-logo.svg.png" class="tech-logo">
    API</div>''', unsafe_allow_html=True)
with c6:
    st.markdown('''<div class="tech-card">
    <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" class="tech-logo">
    Streamlit</div>''', unsafe_allow_html=True)

# -------------------------
# CARACTERÍSTICAS
# -------------------------

st.markdown("## 📌 Características")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**ETL Automatizado**\n\nExtracción y transformación automática de datos.")
with col2:
    st.success("**Data Warehouse**\n\nModelo estrella para consultas analíticas.")
with col3:
    st.warning("**Business Intelligence**\n\nVisualización interactiva mediante dashboards.")

st.divider()

st.caption(
    "MediaWiki Analytics Platform · Ingeniería de Datos  |  "
    "Powered by Python · Pandas · SQLite · Plotly · Streamlit"
)
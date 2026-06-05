import streamlit as st

st.set_page_config(
    page_title="MediaWiki Analytics Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CSS PERSONALIZADO (Animaciones e Imágenes)
# -------------------------

st.markdown("""
<style>

/* --- Animaciones --- */
@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(30px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #334155 100%
    );
}

.main-title {
    text-align: center;
    color: white;
    font-size: 4rem;
    font-weight: bold;
    animation: fadeInUp 0.8s ease-out forwards;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.3rem;
    animation: fadeInUp 1s ease-out forwards;
}

.card {
    background-color: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    margin-top: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeInUp 1.2s ease-out forwards;
}

/* Efecto hover para las tarjetas principales */
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.4);
    background-color: rgba(255,255,255,0.12);
}

.tech-card {
    background-color: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
    transition: all 0.3s ease;
    animation: fadeInUp 1.4s ease-out forwards;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    height: 120px;
}

/* Efecto hover para las tarjetas de tecnología */
.tech-card:hover {
    transform: scale(1.08);
    background-color: rgba(255,255,255,0.15);
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}

/* Clases para controlar el tamaño de las imágenes */
.tech-logo {
    width: 45px;
    height: 45px;
    object-fit: contain;
}

.wiki-logo {
    width: 60px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO SECTION
# -------------------------

st.markdown(
    """
    <h1 class="main-title">
    <img src="https://d3ogvqw9m2inp7.cloudfront.net/assets/dynamic/assets/recruiters/images/1233996/logo.png" style="width: 60px; vertical-align: middle; margin-right: 15px;">
    MediaWiki Analytics Platform
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="subtitle">
    Plataforma de análisis de tráfico Wikimedia basada en 
    ETL automatizado, Data Warehouse y Business Intelligence.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------
# PRESENTACIÓN
# -------------------------

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    <div class="card">
    <h2>🚀 Objetivo del Proyecto</h2>
    
    Extraer, transformar y analizar información pública 
    proveniente de Wikimedia utilizando un pipeline ETL 
    automatizado.
    
    Los datos son obtenidos desde la API oficial de Wikimedia, 
    procesados mediante Pandas y almacenados en un Data Warehouse 
    SQLite para su posterior explotación analítica.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h2>📊 Fuente</h2>
    <img src="https://d3ogvqw9m2inp7.cloudfront.net/assets/dynamic/assets/recruiters/images/1233996/logo.png" class="wiki-logo"><br>
    Wikimedia API
    <br><br>
    Actualización automática
    <br><br>
    Datos reales
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# ARQUITECTURA
# -------------------------

st.markdown("## ⚙️ Arquitectura del Proyecto")

st.markdown("""
<div class="card">
API Wikimedia <br>⬇️<br>
Extract <br>⬇️<br>
Transform <br>⬇️<br>
SQLite Data Warehouse <br>⬇️<br>
SQL Analytics <br>⬇️<br>
Streamlit Dashboard
</div>
""", unsafe_allow_html=True)

# -------------------------
# TECNOLOGÍAS
# -------------------------

st.markdown("## 🛠️ Tecnologías Utilizadas")

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(
        '''<div class="tech-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" class="tech-logo">
        Python
        </div>''',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        '''<div class="tech-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" class="tech-logo">
        Pandas
        </div>''',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        '''<div class="tech-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg" class="tech-logo" style="width: 80px;">
        SQLite
        </div>''',
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        '''<div class="tech-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/Plotly_logo_for_digital_final_%286%29.png" class="tech-logo">
        Plotly
        </div>''',
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        '''<div class="tech-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Wikimedia-logo.svg/1024px-Wikimedia-logo.svg.png" class="tech-logo">
        API
        </div>''',
        unsafe_allow_html=True
    )

with c6:
    st.markdown(
        '''<div class="tech-card">
        <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" class="tech-logo">
        Streamlit
        </div>''',
        unsafe_allow_html=True
    )

# -------------------------
# MÉTRICAS DEL PROYECTO
# -------------------------

st.markdown("## 📌 Características")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
        **ETL Automatizado**\n
        Extracción y transformación
        automática de datos.
        """
    )

with col2:
    st.success(
        """
        **Data Warehouse**\n
        Modelo estrella para
        consultas analíticas.
        """
    )

with col3:
    st.warning(
        """
        **Business Intelligence**\n
        Visualización interactiva
        mediante dashboards.
        """
    )

st.divider()

# -------------------------
# FOOTER
# -------------------------

st.caption(
    """
    MediaWiki Analytics Platform | Ingeniería de Datos
    
    Powered by Python · Pandas · SQLite · Plotly · Streamlit
    """
)
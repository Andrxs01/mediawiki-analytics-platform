📚 MediaWiki Analytics Platform

Plataforma de Ingeniería de Datos para la extracción, transformación, almacenamiento y análisis de tráfico de Wikimedia utilizando una arquitectura ETL automatizada, Data Warehouse y visualización interactiva.

📖 Descripción del Proyecto

MediaWiki Analytics Platform es una solución integral de análisis de datos construida bajo principios de Ingeniería de Datos.

El proyecto extrae información pública desde la API oficial de Wikimedia, ejecuta procesos ETL para limpiar y transformar los datos, almacena la información en un Data Warehouse con modelo estrella y presenta métricas e indicadores mediante dashboards interactivos.

La plataforma permite analizar tendencias de tráfico, artículos más consultados, distribución geográfica e idioma de navegación dentro del ecosistema Wikimedia.

🎯 Objetivos
Objetivo General

Diseñar e implementar una plataforma de análisis de tráfico Wikimedia mediante una arquitectura ETL automatizada y un Data Warehouse orientado a Business Intelligence.

Objetivos Específicos
Extraer datos desde la API pública de Wikimedia.
Limpiar y normalizar los datos obtenidos.
Aplicar transformaciones analíticas.
Implementar un modelo dimensional tipo estrella.
Construir consultas SQL para análisis exploratorio.
Generar dashboards interactivos para visualización de indicadores.
Automatizar la actualización de datos.

🌐 Fuente de Datos

Datos obtenidos desde:

🔗 https://wikimedia.org/api/rest_v1/

API utilizada:

https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{project}/all-access/{year}/{month}/{day}

Ejemplo:

https://wikimedia.org/api/rest_v1/metrics/pageviews/top/es.wikipedia/all-access/2026/06/01

🏗️ Arquitectura
                 Wikimedia API
                        │
                        ▼
                Extract (Python)
                        │
                        ▼
            Raw Data Storage (CSV)
                        │
                        ▼
             Transform (Pandas)
                        │
                        ▼
           Clean Dataset (CSV)
                        │
                        ▼
          Data Warehouse (SQLite)
                        │
                        ▼
             SQL Analytics Layer
                        │
                        ▼
           Streamlit Dashboard
🔄 Pipeline ETL
Extract

Obtención automática de información desde la API de Wikimedia.

Variables extraídas:

Variable	Tipo
timestamp	Temporal
project	Categórica
page_title	Categórica
count_views	Numérica
Transform

Transformaciones realizadas:

Eliminación de registros inválidos
Limpieza de nombres de artículos
Conversión de fechas
Normalización de variables
Creación de variables derivadas

Variables derivadas:

Variable	Tipo
idioma	Categórica
región	Categórica
dia_semana	Categórica
mes	Numérica
anio	Numérica
Load

Carga de información hacia SQLite.

Tablas generadas:

DimProject
id_project
project
idioma
region
DimPage
id_page
page_title
DimTime
id_time
timestamp
dia_semana
mes
anio
FactPageViews
id_project
id_page
id_time
count_views
⭐ Modelo Estrella
                 DIM_PROJECT
                      │
                      │
                      ▼

DIM_PAGE ─── FACT_PAGEVIEWS ─── DIM_TIME
📊 Indicadores Analizados

La plataforma permite analizar:

Top artículos más visitados
Distribución de tráfico por idioma
Distribución geográfica
Tendencias temporales
Patrones semanales de consulta
Métricas agregadas de tráfico

🛠️ Tecnologías Utilizadas
Herramienta	Uso
Python	Desarrollo ETL
Pandas	Transformación de datos
Requests	Consumo de API
SQLite	Data Warehouse
SQL	Consultas analíticas
Plotly	Visualización
Streamlit	Dashboard
Git	Control de versiones
GitHub	Repositorio

📁 Estructura del Proyecto
mediawiki-analytics-platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── mediawiki.db
│
├── dashboard/
│   ├── MediaWiki.py
│   └── pages/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│
├── main.py
├── requirements.txt
└── README.md

🚀 Ejecución
1. Clonar repositorio
git clone https://github.com/Andrxs01/mediawiki-analytics-platform.git
cd mediawiki-analytics-platform
2. Crear entorno virtual
python -m venv venv

Windows:

venv\Scripts\activate

Linux / Mac:

source venv/bin/activate
3. Instalar dependencias
pip install -r requirements.txt
4. Ejecutar ETL
python main.py
5. Ejecutar Dashboard
streamlit run dashboard/MediaWiki.py
📈 Resultados

El proyecto permite:

Analizar miles de registros diarios de Wikimedia.
Detectar artículos con mayor tráfico.
Identificar patrones por idioma y región.
Generar métricas automatizadas para Business Intelligence.
Mantener una arquitectura escalable y reutilizable.
🎓 Proyecto Académico

Asignatura: Ingeniería de Datos

Temáticas aplicadas:

ETL
Data Warehousing -> Calidad de Datos->Modelado Dimensional->SQL Analytics->Business Intelligence->Visualización de Datos

AUTORES:
Adrian Bohorquez
Jesus Vilardi
Luis David Rubio 





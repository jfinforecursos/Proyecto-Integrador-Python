import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# --- CONFIGURACIÓN ---
USER = "admin"
PASS = "admin123"
BASIC_AUTH = HTTPBasicAuth(USER, PASS)
BASE_URL = "https://pi-deploy-ouni.onrender.com/api"

st.set_page_config(page_title="Adopciones Cesde - Analytics", layout="wide")

# --- FUNCIONES API ---
@st.cache_data(ttl=60) # Cacheamos 1 minuto para no saturar el servidor
def fetch_all(endpoint):
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}", auth=BASIC_AUTH)
        return res.json() if res.status_code == 200 else []
    except: return []

# --- INTERFAZ ---
st.sidebar.title("🐾 Navegación")
menu = ["Gestión General", "Dashboard & Estadísticas"]
choice = st.sidebar.radio("Ir a:", menu)

if choice == "Gestión General":
    st.info("Aquí iría el código anterior de CRUD de Mascotas, Adoptantes y Solicitudes.")

elif choice == "Dashboard & Estadísticas":
    st.title("📊 Análisis de Datos del Sistema")
    
    # Carga de datos
    mascotas_raw = fetch_all("mascotas")
    solicitudes_raw = fetch_all("solicitudes")
    
    if not mascotas_raw:
        st.warning("No hay datos suficientes para generar el dashboard.")
        st.stop()

    # --- PROCESAMIENTO CON PANDAS ---
    df_m = pd.DataFrame(mascotas_raw)
    
    # Filtros en el Sidebar para los datos
    st.sidebar.header("Filtros de Búsqueda")
    search_nombre = st.sidebar.text_input("Buscar mascota por nombre", "")
    filtro_tamano = st.sidebar.multiselect("Tamaño", options=df_m["tamano"].unique(), default=df_m["tamano"].unique())
    edad_max = st.sidebar.slider("Edad máxima", 0, int(df_m["edad"].max()), int(df_m["edad"].max()))

    # Aplicando filtros de Pandas
    df_filtered = df_m[
        (df_m["nombre"].str.contains(search_nombre, case=False)) &
        (df_m["tamano"].isin(filtro_tamano)) &
        (df_m["edad"] <= edad_max)
    ]

    # --- MÉTRICAS RÁPIDAS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Mascotas", len(df_m))
    m2.metric("Mascotas Filtradas", len(df_filtered))
    m3.metric("Promedio Edad", f"{df_filtered['edad'].mean():.1f} años")

    st.divider()

    # --- GRÁFICOS ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Distribución por Especie")
        # Conteo rápido con Pandas
        especie_counts = df_filtered["especie"].value_counts()
        st.bar_chart(especie_counts, color="#FF4B4B")

    with col_chart2:
        st.subheader("Estado de Mascotas")
        # Gráfico de áreas o líneas (ejemplo visual)
        estado_counts = df_filtered["estado"].value_counts()
        st.area_chart(estado_counts, color="#29B5E8")

    st.divider()

    # --- ANÁLISIS DE SOLICITUDES ---
    st.subheader("🔍 Detalle de Mascotas Filtradas")
    if not df_filtered.empty:
        # Estilizando el dataframe con Pandas Styler
        st.dataframe(df_filtered.style.highlight_max(axis=0, subset=['edad'], color='#f5cba7'), use_container_width=True)
    else:
        st.write("No hay resultados para los filtros seleccionados.")

    # Ejemplo de gráfico de dispersión (Edad vs Tamaño)
    st.subheader("Relación Edad vs Tamaño")
    st.scatter_chart(data=df_filtered, x="tamano", y="edad", color="especie")
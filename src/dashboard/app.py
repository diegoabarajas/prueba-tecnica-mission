import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configurar página
st.set_page_config(
    page_title="TravelCorp RPA Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Título principal
st.title("🌍 TravelCorp - Monitoreo de Condiciones de Viaje")
st.markdown("Sistema RPA para evaluación de viabilidad de viajes corporativos")

# Cargar datos más recientes
def cargar_datos_recientes():
    """Carga el archivo JSON más reciente generado"""
    output_dir = "data/outputs"
    if not os.path.exists(output_dir):
        return []
    
    archivos = [f for f in os.listdir(output_dir) if f.startswith("reporte_ciudades") and f.endswith(".json")]
    if not archivos:
        return []
    
    archivo_reciente = sorted(archivos)[-1]  # Más reciente
    with open(os.path.join(output_dir, archivo_reciente), 'r', encoding='utf-8') as f:
        return json.load(f)

# Cargar datos
datos = cargar_datos_recientes()

if not datos:
    st.warning("No se encontraron datos recientes. Ejecuta el sistema primero.")
    st.stop()

# Sidebar con filtros
st.sidebar.title("Filtros")
ciudad_seleccionada = st.sidebar.selectbox(
    "Seleccionar Ciudad:",
    [ciudad['ciudad'] for ciudad in datos]
)

# Encontrar datos de la ciudad seleccionada
ciudad_data = next((item for item in datos if item['ciudad'] == ciudad_seleccionada), None)

# --- VISTA GENERAL ---
st.header("Vista General")

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Color según IVV
    color_ivv = {
        "BAJO": "🟢",
        "MEDIO": "🟡", 
        "ALTO": "🟠",
        "CRÍTICO": "🔴"
    }.get(ciudad_data['nivel_riesgo'], "⚪")
    
    st.metric(
        label="Índice de Viabilidad (IVV)",
        value=f"{ciudad_data['ivv_score']}",
        delta=ciudad_data['nivel_riesgo'],
        delta_color="off"
    )

with col2:
    st.metric(
        label="Temperatura Actual",
        value=f"{ciudad_data['clima']['temperatura_actual']}°C"
    )

with col3:
    st.metric(
        label="Tipo de Cambio",
        value=f"1 USD = {ciudad_data['finanzas']['tipo_cambio_actual']}"
    )

with col4:
    st.metric(
        label="Alertas Activas",
        value=len(ciudad_data['alertas'])
    )

# --- MAPA DE RIESGO ---
st.header("Mapa de Riesgo por Ciudad")

# Crear DataFrame para el mapa
df_mapa = pd.DataFrame([
    {
        'Ciudad': item['ciudad'],
        'IVV': item['ivv_score'],
        'Riesgo': item['nivel_riesgo'],
        'Alertas': len(item['alertas']),
        'Temperatura': item['clima']['temperatura_actual']
    }
    for item in datos
])

# Mapa de calor de IVV
fig_mapa = px.bar(
    df_mapa,
    x='Ciudad',
    y='IVV',
    color='Riesgo',
    color_discrete_map={
        'BAJO': '#28a745',
        'MEDIO': '#ffc107', 
        'ALTO': '#fd7e14',
        'CRÍTICO': '#dc3545'
    },
    title="Índice de Viabilidad por Ciudad"
)
st.plotly_chart(fig_mapa, use_container_width=True)

# --- DETALLES DE LA CIUDAD SELECCIONADA ---
st.header(f"Detalles: {ciudad_seleccionada}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Condiciones Climáticas")
    
    # Temperatura
    fig_temp = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = ciudad_data['clima']['temperatura_actual'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Temperatura (°C)"},
        gauge = {
            'axis': {'range': [-10, 50]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-10, 0], 'color': "lightblue"},
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "red"}
            ]
        }
    ))
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.subheader("Condiciones Ambientales")
    
    # Métricas ambientales
    st.metric("Viento", f"{ciudad_data['clima']['viento']} km/h")
    st.metric("Precipitación", f"{ciudad_data['clima']['precipitacion']} mm")
    st.metric("Índice UV", f"{ciudad_data['clima']['uv']}")

# --- ALERTAS ---
if ciudad_data['alertas']:
    st.header("Alertas Activas")
    
    for alerta in ciudad_data['alertas']:
        if alerta['severidad'] == 'ALTA':
            st.error(f"**{alerta['severidad']}**: {alerta['mensaje']}")
        elif alerta['severidad'] == 'MEDIA':
            st.warning(f"**{alerta['severidad']}**: {alerta['mensaje']}")
        else:
            st.info(f"**{alerta['severidad']}**: {alerta['mensaje']}")

# --- INFORMACIÓN FINANCIERA ---
st.header("Información Financiera")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Tipo de Cambio Actual",
        f"1 USD = {ciudad_data['finanzas']['tipo_cambio_actual']}",
        delta=f"{ciudad_data['finanzas']['variacion_diaria']}%"
    )

with col2:
    st.metric("Tendencia 5 Días", ciudad_data['finanzas']['tendencia_5_dias'])

# --- COMPONENTES IVV ---
st.header("Componentes del IVV")

componentes = ciudad_data['componentes_ivv']
df_componentes = pd.DataFrame({
    'Componente': ['Clima', 'Tipo Cambio', 'UV'],
    'Puntaje': [componentes['clima_score'], componentes['cambio_score'], componentes['uv_score']],
    'Peso': [40, 30, 30]
})

fig_componentes = px.bar(
    df_componentes,
    x='Componente',
    y='Puntaje',
    title="Desglose de Componentes del IVV"
)
st.plotly_chart(fig_componentes, use_container_width=True)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(f"*Última actualización: {ciudad_data['timestamp']}*")
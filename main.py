import streamlit as st
from datetime import datetime, timedelta
import pytz

# Configuración inicial
st.set_page_config(page_title="Calculadora MEL", layout="centered")

# Diccionario de meses abreviados en español
meses_abr = {
    1: "ene", 2: "feb", 3: "mar", 4: "abr",
    5: "may", 6: "jun", 7: "jul", 8: "ago",
    9: "sep", 10: "oct", 11: "nov", 12: "dic"
}

def formatear_fecha_compacta(fecha):
    dia = str(fecha.day).zfill(2)
    mes = meses_abr[fecha.month]
    anio = str(fecha.year)[2:] 
    return f"{dia}/{mes}/{anio}"

# --- LÓGICA DE TIEMPO AUTOMÁTICA ---
tz_local = pytz.timezone('America/Bogota')
dt_ahora_local = datetime.now(tz_local)
dt_utc_ahora = dt_ahora_local.astimezone(pytz.utc)

# --- SECCIÓN SUPERIOR: CALCULADORA MEL ---
st.title("✈️ Calculadora MEL")

col_cat, col_opt = st.columns([2, 1])
with col_cat:
    categoria = st.selectbox("Seleccione Categoría:", ["A", "B", "C", "D"], index=1)
with col_opt:
    if categoria == "A":
        dias_sumar = st.number_input("Días:", min_value=1, value=1)
    else:
        plazos = {"B": 3, "C": 10, "D": 120}
        dias_sumar = plazos[categoria]
        st.write(f"**Plazo:** {dias_sumar} días")

# Cálculo de Vencimiento
fecha_inicio_conteo_utc = dt_utc_ahora.date() + timedelta(days=1)
vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=dias_sumar)

st.divider()

# RESULTADO DESTACADO CON DISEÑO PERSONALIZADO
st.subheader(f"Resultado Categoría {categoria}")

# Estilo HTML para fondo rojo claro y letra negrita
fecha_resultado = formatear_fecha_compacta(vencimiento_fecha_utc)
st.markdown(
    f"""
    <div style="
        background-color: #ffe6e6; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #ffb3b3;
        text-align: center;
        ">
        <span style="color: #cc0000; font-size: 20px;">
            El plazo vence el: <b>{fecha_resultado}</b> a las 23:59 UTC
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("") # Espacio estético
st.info(f"Conteo inicia el {formatear_fecha_compacta(fecha_inicio_conteo_utc)} (00:00Z)")

# --- SECCIÓN INFERIOR: REFERENCIA TEMPORAL ---
st.write("")
st.divider()

st.subheader("🌐 Tiempo Actual")
col_local, col_utc = st.columns(2)

with col_local:
    st.write("**Local (Bogotá)**")
    st.metric(label="Fecha", value=formatear_fecha_compacta(dt_ahora_local.date()))
    st.code(dt_ahora_local.strftime("%H:%M:%S"), language=None)

with col_utc:
    st.write("**UTC (Z)**")
    st.metric(label="Fecha", value=formatear_fecha_compacta(dt_utc_ahora.date()))
    st.code(dt_utc_ahora.strftime("%H:%M:%S Z"), language=None)

import streamlit as st
from datetime import datetime, timedelta
import pytz

# Configuración inicial
st.set_page_config(page_title="Calculadora MEL Compacta", layout="centered")

# Diccionario de meses abreviados en español
meses_abr = {
    1: "ene", 2: "feb", 3: "mar", 4: "abr",
    5: "may", 6: "jun", 7: "jul", 8: "ago",
    9: "sep", 10: "oct", 11: "nov", 12: "dic"
}

def formatear_fecha_compacta(fecha):
    # Formato: DD/mes/YY (ej: 28/mar/26)
    dia = str(fecha.day).zfill(2)
    mes = meses_abr[fecha.month]
    anio = str(fecha.year)[2:] # Toma los últimos dos dígitos
    return f"{dia}/{mes}/{anio}"

# --- LÓGICA DE TIEMPO AUTOMÁTICA ---
tz_local = pytz.timezone('America/Bogota')
dt_ahora_local = datetime.now(tz_local)
dt_utc_ahora = dt_ahora_local.astimezone(pytz.utc)

# --- SECCIÓN SUPERIOR: CALCULADORA MEL ---
st.title("✈️ Calculadora de Plazos MEL")

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

# Cálculo de Vencimiento (Día 0 UTC + 1 + Plazo)
fecha_inicio_conteo_utc = dt_utc_ahora.date() + timedelta(days=1)
vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=dias_sumar)

st.divider()

# RESULTADO DESTACADO
st.subheader(f"Resultado Categoría {categoria}")
st.success(f"El plazo vence el: **{formatear_fecha_compacta(vencimiento_fecha_utc)}** a las 23:59 UTC.")
st.info(f"Conteo inicia el {formatear_fecha_compacta(fecha_inicio_conteo_utc)} (00:00Z)")

# --- SECCIÓN INFERIOR: REFERENCIA TEMPORAL ---
st.write("")
st.divider()

st.subheader("🌐 Referencia de Tiempo Actual")
col_local, col_utc = st.columns(2)

with col_local:
    st.write("**Local (Bogotá)**")
    st.metric(label="Fecha", value=formatear_fecha_compacta(dt_ahora_local.date()))
    st.code(dt_ahora_local.strftime("%H:%M:%S"), language=None)

with col_utc:
    st.write("**UTC (Z)**")
    st.metric(label="Fecha", value=formatear_fecha_compacta(dt_utc_ahora.date()))
    st.code(dt_utc_ahora.strftime("%H:%M:%S Z"), language=None)

st.caption("Nota: Formato de fecha optimizado para reportes técnicos (DD/mes/YY).")

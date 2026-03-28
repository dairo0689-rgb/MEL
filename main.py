import streamlit as st
from datetime import datetime, timedelta
import pytz

# Configuración inicial
st.set_page_config(page_title="Calculadora MEL Pro", layout="centered")

# Diccionario de meses en español
meses_es = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def formatear_fecha_es(fecha):
    return f"{fecha.day} de {meses_es[fecha.month]} de {fecha.year}"

# --- LÓGICA DE TIEMPO AUTOMÁTICA ---
tz_local = pytz.timezone('America/Bogota')
dt_ahora_local = datetime.now(tz_local)
dt_utc_ahora = dt_ahora_local.astimezone(pytz.utc)

# --- SECCIÓN SUPERIOR: CALCULADORA MEL ---
st.title("✈️ Calculadora de Plazos MEL")

# Selección de categoría y parámetros
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

# Determinación del Día 0 y Vencimiento
# El Día 0 UTC es la fecha actual en UTC
fecha_inicio_conteo_utc = dt_utc_ahora.date() + timedelta(days=1)
vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=dias_sumar)

st.divider()

# RESULTADO DESTACADO (En la parte superior)
st.subheader(f"Resultado Categoría {categoria}")
st.success(f"El plazo vence el: **{formatear_fecha_es(vencimiento_fecha_utc)}** a las 23:59 UTC.")
st.info(f"El conteo inicia a las 00:00Z del {formatear_fecha_es(fecha_inicio_conteo_utc)}")

# --- SECCIÓN INFERIOR: REFERENCIA TEMPORAL ---
st.write("")
st.write("")
st.write("")
st.divider()

st.subheader("🌐 Referencia de Tiempo Actual")
col_local, col_utc = st.columns(2)

with col_local:
    st.write("**Hora Local (Bogotá)**")
    st.metric(label="Fecha Actual", value=formatear_fecha_es(dt_ahora_local.date()))
    st.code(dt_ahora_local.strftime("%H:%M:%S"), language=None)

with col_utc:
    st.write("**Hora UTC (Z)**")
    st.metric(label="Fecha UTC", value=formatear_fecha_es(dt_utc_ahora.date()))
    st.code(dt_utc_ahora.strftime("%H:%M:%S Z"), language=None)

# Nota al pie
st.caption("Nota: Esta aplicación toma la hora del sistema automáticamente para el cálculo en tiempo real.")

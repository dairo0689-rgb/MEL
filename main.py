import streamlit as st
from datetime import datetime, timedelta
import pytz

# Configuración inicial
st.set_page_config(page_title="Calculadora MEL Automática", layout="wide")

st.title("✈️ Calculadora MEL (Hora Automática)")

# Diccionario de meses en español
meses_es = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def formatear_fecha_es(fecha):
    return f"{fecha.day} de {meses_es[fecha.month]} de {fecha.year}"

# --- LÓGICA DE TIEMPO AUTOMÁTICA ---
# Definir zona horaria por defecto (Bogotá/Colombia)
tz_local = pytz.timezone('America/Bogota')
dt_ahora_local = datetime.now(tz_local)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Configuración")
    categoria = st.selectbox("Categoría MEL:", ["A", "B", "C", "D"], index=1) # B por defecto
    
    if categoria == "A":
        intervalo_a = st.number_input("Días Cat A:", min_value=1, value=1)
    
    st.divider()
    st.write("🕒 **Hora del sistema (Local):**")
    st.info(dt_ahora_local.strftime("%H:%M:%S"))
    
    # Opción por si necesitas editar la hora manualmente
    usar_manual = st.checkbox("Editar hora manualmente")
    if usar_manual:
        fecha_input = st.date_input("Fecha:", dt_ahora_local.date())
        hora_input = st.time_input("Hora:", dt_ahora_local.time())
        dt_local = tz_local.localize(datetime.combine(fecha_input, hora_input))
    else:
        dt_local = dt_ahora_local

# --- CÁLCULOS ---
# 1. Convertir a UTC
dt_utc = dt_local.astimezone(pytz.utc)

# 2. Determinar inicio de conteo (Día 1 es el siguiente a las 00:00Z)
fecha_inicio_conteo_utc = dt_utc.date() + timedelta(days=1)

# 3. Calcular vencimiento
plazos = {"B": 3, "C": 10, "D": 120}
dias_sumar = intervalo_a if categoria == "A" else plazos[categoria]
vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=dias_sumar)

# --- INTERFAZ PRINCIPAL ---
col1, col2 = st.columns(2)

with col1:
    st.metric("Hallazgo Local", formatear_fecha_es(dt_local.date()))
    st.caption(f"Hora: {dt_local.strftime('%H:%M')} (Bogotá)")

with col2:
    # Mostramos la conversión UTC automática
    st.metric("Equivalencia UTC", formatear_fecha_es(dt_utc.date()))
    st.caption(f"Hora: {dt_utc.strftime('%H:%M Z')}")

st.divider()

# Resultado Destacado
st.subheader(f"Resultado Categoría {categoria} ({dias_sumar} días)")
st.success(f"El plazo vence el: **{formatear_fecha_es(vencimiento_fecha_utc)}** a las 23:59 UTC.")

with st.expander("Ver detalles del cálculo"):
    st.write(f"- **Día 0 (UTC):** {formatear_fecha_es(dt_utc.date())}")
    st.write(f"- **Inicio de conteo (00:00Z):** {formatear_fecha_es(fecha_inicio_conteo_utc)}")
    st.write(f"- **Días calendario:** {dias_sumar}")

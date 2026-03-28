import streamlit as st
from datetime import datetime, timedelta, time
import pytz

# Configuración inicial
st.set_page_config(page_title="Calculadora MEL UTC", layout="wide") # Cambiado a wide para columnas

st.title("✈️ Calculadora de Plazos MEL Pro")
st.write("Determine la fecha de vencimiento MEL y la hora UTC del hallazgo.")

# Diccionario de meses en español
meses_es = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# --- BARRA LATERAL (Entrada de Datos) ---
with st.sidebar:
    st.header("Datos del Hallazgo")
    
    # 1. Selección de Categoría
    categoria = st.selectbox("Categoría MEL:", ["A", "B", "C", "D"])
    
    # Información de días
    info_dias = {"A": "Var.", "B": "3 días", "C": "10 días", "D": "120 días"}
    st.caption(f"Plazo estándar Cat {categoria}: {info_dias[categoria]}")

    if categoria == "A":
        intervalo_a = st.number_input("Días Cat A:", min_value=1, value=1)

    st.divider()
    
    # 2. Fecha y Hora Local del Hallazgo
    col_fecha, col_hora = st.columns(2)
    with col_fecha:
        fecha_local = st.date_input("Fecha Local:", datetime.now())
    with col_hora:
        hora_local = st.time_input("Hora Local (HH:MM):", time(12, 0)) # Por defecto mediodía

    # 3. Selección de Zona Horaria Local (Importante para cálculo UTC)
    # Obtenemos una lista común de timezones
    comunes_tz = pytz.common_timezones
    # Intentamos pre-seleccionar una zona común en Latam, si no, UTC
    indice_defecto = comunes_tz.index('America/Bogota') if 'America/Bogota' in comunes_tz else 0
    tz_local_nombre = st.selectbox("Tu Zona Horaria Local:", comunes_tz, index=indice_defecto)
    tz_local = pytz.timezone(tz_local_nombre)

# --- ÁREA PRINCIPAL (Cálculos y Resultados) ---

# A. Procesamiento de Tiempos
# 1. Combinar fecha y hora local
dt_local_naive = datetime.combine(fecha_local, hora_local)
# 2. Localizar el tiempo (añadir info de zona horaria, manejando DST)
dt_local = tz_local.localize(dt_local_naive)
# 3. Convertir a UTC
dt_utc = dt_local.astimezone(pytz.utc)

# B. Lógica de Cálculo MEL (Días calendario UTC)
# El conteo inicia a las 00:00 UTC del día SIGUIENTE al hallazgo UTC.
fecha_inicio_conteo_utc = dt_utc.date() + timedelta(days=1)

if categoria == "A":
    vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=intervalo_a)
elif categoria == "B":
    vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=3)
elif categoria == "C":
    vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=10)
else: # D
    vencimiento_fecha_utc = fecha_inicio_conteo_utc + timedelta(days=120)

# C. Formateo de Fechas (Mes en letras)
def formatear_fecha_es(fecha):
    return f"{fecha.day} de {meses_es[fecha.month]} de {fecha.year}"

fecha_hallazgo_local_str = formatear_fecha_es(fecha_local)
fecha_hallazgo_utc_str = formatear_fecha_es(dt_utc.date())
fecha_vencimiento_utc_str = formatear_fecha_es(vencimiento_fecha_utc)


# --- Visualización ---

# Columna de tiempos del Hallazgo
col1, col2 = st.columns(2)

with col1:
    st.subheader("Registro del Hallazgo")
    st.metric(label="Fecha Local", value=fecha_hallazgo_local_str)
    st.text(f"Hora Local: {dt_local.strftime('%H:%M')} ({tz_local_nombre})")

with col2:
    st.subheader("Equivalencia UTC (Día 0)")
    # Esta es la nueva columna solicitada
    st.metric(label="Fecha UTC", value=fecha_hallazgo_utc_str, help="Fecha base para el conteo MEL")
    st.text(f"Hora UTC: {dt_utc.strftime('%H:%M Z')}")


st.divider()

# Resultado Final
st.subheader(f"Resultado Categoría {categoria}")
st.success(f"El plazo vence el: **{fecha_vencimiento_utc_str}** a las 23:59 UTC.")

st.warning(f"Nota: El conteo de {info_dias[categoria]} inicia a la medianoche (24:00 Z) del {fecha_hallazgo_utc_str}.")

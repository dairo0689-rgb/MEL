import streamlit as st
from datetime import datetime, timedelta
import locale

# Configuración inicial
st.set_page_config(page_title="Calculadora de Plazos MEL", layout="centered")

st.title("✈️ Calculadora de Plazos MEL")
st.write("Determine la fecha de vencimiento según la categoría de diferido.")

# Diccionario de meses en español (para asegurar compatibilidad en la nube de Streamlit)
meses_es = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# Selección de Categoría
categoria = st.selectbox("Seleccione la Categoría MEL:", ["A", "B", "C", "D"])

# Información de días por categoría
info_dias = {
    "A": "Variable (especificado en el MEL)",
    "B": "3 días consecutivos",
    "C": "10 días consecutivos",
    "D": "120 días consecutivos"
}

st.info(f"**Especificación:** La Categoría {categoria} permite un plazo de: {info_dias[categoria]}")

# Entrada de datos (Día 0)
fecha_hallazgo = st.date_input("Fecha del hallazgo (Día 0):", datetime.now())

# Lógica de cálculo
if categoria == "A":
    intervalo = st.number_input("Especifique el intervalo (en días) para Cat A:", min_value=1, value=1)
    vencimiento = fecha_hallazgo + timedelta(days=intervalo)
elif categoria == "B":
    vencimiento = fecha_hallazgo + timedelta(days=3)
elif categoria == "C":
    vencimiento = fecha_hallazgo + timedelta(days=10)
else: # Categoría D
    vencimiento = fecha_hallazgo + timedelta(days=120)

# Formateo de fecha con mes en letras
dia = vencimiento.day
mes_texto = meses_es[vencimiento.month]
anio = vencimiento.year
fecha_formateada = f"{dia} de {mes_texto} de {anio}"

# Mostrar resultados
st.divider()
st.subheader(f"Resultado Categoría {categoria}")
st.success(f"El plazo vence el: **{fecha_formateada}** a las 23:59 UTC.")

st.warning("Nota: El conteo inicia a la medianoche (24:00) del día en que se registró el diferido.")

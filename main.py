import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Calculadora  MEL", layout="centered")

st.title("✈️ Calculadora  MEL")
st.write("Determine la fecha de vencimiento según la categoría de diferido.")

# Selección de Categoría
categoria = st.selectbox("Seleccione la Categoría MEL:", ["A", "B", "C", "D"])

# --- NUEVA SECCIÓN DE INFORMACIÓN DE DÍAS ---
# Definimos los días por categoría para mostrarlos y usarlos en el cálculo
info_dias = {
    "A": "Variable (especificado en el MEL)",
    "B": "3 días consecutivos",
    "C": "10 días consecutivos",
    "D": "120 días consecutivos"
}

st.info(f"**Especificación:** El intervalo {categoria} permite un plazo de: {info_dias[categoria]}")
# --------------------------------------------

# Entrada de datos
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

# Mostrar resultados
st.divider()
st.subheader(f"Resultado Categoría {categoria}")
st.success(f"El plazo vence el: **{vencimiento.strftime('%d/%m/%Y')}** a las 23:59 UTC.")

st.warning("Nota: El conteo inicia a la medianoche (24:00) del día en que se registró el diferido.")

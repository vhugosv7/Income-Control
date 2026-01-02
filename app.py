import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import matplotlib.pyplot as plt

# Conexión DB
conn = sqlite3.connect("negocio.db", check_same_thread=False)
c = conn.cursor()

# Crear tabla
c.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    tipo TEXT,
    monto REAL,
    categoria TEXT,
    fecha TEXT
)
""")
conn.commit()

st.title("Control de Gastos y Utilidad")

# Formulario
st.subheader("Registrar movimiento")

tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
monto = st.number_input("Monto", min_value=0.0, step=1.0)
categoria = st.text_input("Categoría")
fecha = st.date_input("Fecha", value=date.today())

if st.button("Guardar"):
    c.execute(
        "INSERT INTO movimientos VALUES (?, ?, ?, ?)",
        (tipo, monto, categoria, fecha)
    )
    conn.commit()
    st.success("Movimiento guardado")

# Mostrar datos
df = pd.read_sql("SELECT * FROM movimientos", conn)

if not df.empty:
    st.subheader("Resumen")

    ingresos = df[df["tipo"] == "Ingreso"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    utilidad = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"${ingresos:,.2f}")
    col2.metric("Gastos", f"${gastos:,.2f}")
    col3.metric("Utilidad", f"${utilidad:,.2f}")

    st.subheader("Movimientos")
    st.dataframe(df)

    st.subheader("Gráfica")
    resumen = df.groupby("tipo")["monto"].sum()

    fig, ax = plt.subplots()

    ax.bar(
        resumen.index,
        resumen.values,
        color=["green" if x == "Ingreso" else "red" for x in resumen.index])

    ax.set_title("Ingresos vs Gastos")
    ax.set_ylabel("Monto ($)")
    ax.set_xlabel("Tipo")

    st.pyplot(fig)
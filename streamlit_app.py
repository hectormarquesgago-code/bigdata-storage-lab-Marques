import streamlit as st
import pandas as pd
from io import BytesIO

# Importar funciones propias del laboratorio
from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks
from src.transform import normalize_columns, to_silver

st.set_page_config(page_title="Big Data Storage Lab", layout="wide")

st.title("📊 Big Data Storage Lab")
st.write("De CSVs heterogéneos a un almacén analítico confiable")

# --- Sidebar: configuración de mapping ---
st.sidebar.header("Configuración de columnas origen")
col_date = st.sidebar.text_input("Columna fecha (date)", value="date")
col_partner = st.sidebar.text_input("Columna socio (partner)", value="partner")
col_amount = st.sidebar.text_input("Columna monto (amount)", value="amount")

mapping = {
    col_date: "date",
    col_partner: "partner",
    col_amount: "amount",
}

# --- Subida de archivos ---
uploaded_files = st.file_uploader(
    "Sube uno o varios archivos CSV", type=["csv"], accept_multiple_files=True
)

bronze_frames = []

if uploaded_files:
    for f in uploaded_files:
        try:
            # Intentar lectura con utf-8, fallback a latin-1
            try:
                df = pd.read_csv(f)
            except UnicodeDecodeError:
                f.seek(0)
                df = pd.read_csv(f, encoding="latin-1")

            # Normalizar columnas
            df = normalize_columns(df, mapping)

            # Añadir linaje
            df = tag_lineage(df, f.name)

            bronze_frames.append(df)

        except Exception as e:
            st.error(f"Error procesando {f.name}: {e}")

    if bronze_frames:
        bronze = concat_bronze(bronze_frames)
        st.subheader("Bronze Unificado")
        st.dataframe(bronze.head(50))

        # Validaciones
        errors = basic_checks(bronze)
        if errors:
            st.error("⚠️ Errores de validación detectados:")
            for err in errors:
                st.write(f"- {err}")
        else:
            st.success("✅ Validaciones superadas")

            # Derivar capa Silver
            silver = to_silver(bronze)

            st.subheader("Silver (Partner × Mes)")
            st.dataframe(silver.head(50))

            # KPIs simples
            total_amount = silver["amount"].sum()
            top_partner = silver.groupby("partner")["amount"].sum().idxmax()

            st.metric("Monto total (EUR)", f"{total_amount:,.2f}")
            st.metric("Partner con mayor monto", top_partner)

            # Gráfico de barras
            st.subheader("Evolución mensual de Amount")
            chart_data = silver.groupby("month")["amount"].sum().reset_index()
            st.bar_chart(chart_data.set_index("month"))

            # Botones de descarga
            def convert_df(df: pd.DataFrame) -> BytesIO:
                buffer = BytesIO()
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                return buffer

            st.download_button(
                label="⬇️ Descargar Bronze CSV",
                data=convert_df(bronze),
                file_name="bronze.csv",
                mime="text/csv",
            )

            st.download_button(
                label="⬇️ Descargar Silver CSV",
                data=convert_df(silver),
                file_name="silver.csv",
                mime="text/csv",
            )

else:
    st.info("📂 Esperando archivos CSV para procesar...")


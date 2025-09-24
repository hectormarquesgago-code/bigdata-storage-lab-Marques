import pandas as pd
from typing import Dict

def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Renombra y normaliza columnas a esquema canónico:
    - Renombrar según mapping (origen -> canónico: date, partner, amount).
    - Parsear fechas a datetime ISO.
    - Normalizar amount (eliminar '€', comas europeas, convertir a float).
    - Limpiar espacios y normalizar partner.
    """
    # Renombrar columnas según mapping
    df = df.rename(columns=mapping)

    # Normalizar fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.date

    # Normalizar partner
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip()

    # Normalizar amount
    if "amount" in df.columns:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(".", "", regex=False)   # elimina separador miles (p.ej. 1.234,56)
            .str.replace(",", ".", regex=False)  # convierte coma decimal
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df[["date", "partner", "amount"]]


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega dataset Bronze para generar Silver:
    - Suma amount por partner y mes.
    - Crea columna 'month' como inicio de mes (timestamp).
    """
    df = bronze.copy()

    # Crear columna month como primer día de mes
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()

    # Agregar montos por partner y mes
    silver = (
        df.groupby(["partner", "month"], as_index=False)
        .agg({"amount": "sum"})
        .sort_values(["partner", "month"])
    )

    return silver

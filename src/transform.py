import re
from typing import Dict
import pandas as pd


def _parse_amount(value: object) -> float:
    """
    Normaliza un valor monetario a float:
    - elimina símbolos no numéricos (ej. €, espacios),
    - soporta formatos europeos '1.234,56 €' y anglosajones '1234.56',
    - devuelve NaN si no se puede parsear.
    """
    if pd.isna(value):
        return float("nan")

    s = str(value).strip()
    # eliminar todo lo que no sea dígito, coma, punto o signo negativo
    s = re.sub(r"[^\d,.\-]", "", s)
    if s == "":
        return float("nan")

    # Caso: tiene punto y coma -> '.' como miles, ',' como decimal
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        # Si sólo coma -> coma decimal
        if "," in s and "." not in s:
            s = s.replace(",", ".")
        # Si sólo punto -> se mantiene (puede ser decimal)
        # Si sólo dígitos -> se convierte directo

    try:
        return float(s)
    except Exception:
        return float("nan")


def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Renombra y normaliza columnas a esquema canónico:
      - mapping: dict {col_origen: col_canónica}, col_canónica ∈ {'date','partner','amount'}.
      - parsea 'date' a datetime64 (errors -> NaT).
      - normaliza 'amount' a float.
      - limpia 'partner' (strip).
    Devuelve DataFrame con columnas canónicas disponibles.
    """
    df = df.copy()

    # Renombrar columnas según mapping
    df = df.rename(columns=mapping)

    # Normalizar fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Normalizar partner
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip()

    # Normalizar amount
    if "amount" in df.columns:
        df["amount"] = df["amount"].apply(_parse_amount)

    # Devolver solo columnas canónicas que existan
    cols = [c for c in ["date", "partner", "amount"] if c in df.columns]
    return df.loc[:, cols]


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Genera capa Silver desde Bronze:
      - Agrega 'amount' por partner y mes.
      - Crea columna 'month' como inicio de mes (timestamp).
      - Devuelve columnas ['partner','month','amount'].
    """
    df = bronze.copy()

    if "date" not in df.columns:
        raise ValueError("La columna 'date' es necesaria para generar Silver.")

    # Asegurar que 'date' es datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Columna month (primer día de mes como timestamp)
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Agregación
    silver = (
        df.groupby(["partner", "month"], as_index=False)
        .agg({"amount": "sum"})
        .sort_values(["partner", "month"])
    )
    return silver


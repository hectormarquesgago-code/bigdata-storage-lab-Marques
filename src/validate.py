import pandas as pd
from typing import List

def basic_checks(df: pd.DataFrame) -> List[str]:
    """
    Realiza validaciones mínimas:
    - Columnas canónicas presentes.
    - 'amount' numérico y >= 0.
    - 'date' en formato datetime.date.
    Devuelve lista de errores encontrados.
    """
    errors: List[str] = []

    # Columnas esperadas
    required_cols = {"date", "partner", "amount"}
    missing = required_cols - set(df.columns)
    if missing:
        errors.append(f"Faltan columnas requeridas: {missing}")

    # Verificar tipos y valores
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("La columna 'amount' no es numérica.")
        elif (df["amount"] < 0).any():
            errors.append("Existen valores negativos en 'amount'.")

    if "date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df["date"]):
            errors.append("La columna 'date' no está en formato datetime.")

    return errors

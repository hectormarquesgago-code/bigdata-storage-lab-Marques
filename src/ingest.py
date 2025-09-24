import pandas as pd
from datetime import datetime, timezone
from typing import List

def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade columnas de linaje:
    - source_file: nombre de origen.
    - ingested_at: timestamp UTC ISO8601.
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena múltiples DataFrames en esquema Bronze:
    Columnas esperadas: date, partner, amount, source_file, ingested_at.
    """
    if not frames:
        return pd.DataFrame(columns=["date", "partner", "amount", "source_file", "ingested_at"])

    bronze = pd.concat(frames, ignore_index=True)

    # Asegurar orden de columnas
    expected_cols = ["date", "partner", "amount", "source_file", "ingested_at"]
    bronze = bronze[expected_cols]

    return bronze

import pandas as pd
from datetime import datetime, timezone


def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade metadatos de linaje:
      - source_file: nombre del archivo de origen.
      - ingested_at: timestamp UTC ISO8601.
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena DataFrames normalizados y asegura esquema Bronze:
      columnas = ['date','partner','amount','source_file','ingested_at'].
    Si alguna falta en un frame, se rellena con NaN.
    """
    expected_cols = ["date", "partner", "amount", "source_file", "ingested_at"]

    fixed_frames = []
    for f in frames:
        f = f.copy()
        # Asegurar que todas las columnas existan
        for col in expected_cols:
            if col not in f.columns:
                f[col] = pd.NA
        # Reordenar
        f = f[expected_cols]
        fixed_frames.append(f)

    bronze = pd.concat(fixed_frames, ignore_index=True)
    return bronze

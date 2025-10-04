# Optional helper to reproduce cleaning outside the notebook
import pandas as pd, numpy as np
def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "releaseDate" in df.columns:
        df["releaseDate"] = pd.to_datetime(df["releaseDate"], errors="coerce")
        df["releaseYear"] = df["releaseDate"].dt.year
    if "trackTimeMillis" in df.columns:
        df["trackDurationMinutes"] = df["trackTimeMillis"] / 60000.0
    if "collectionPrice" in df.columns:
        df["collectionPrice"] = df["collectionPrice"].replace(-1, np.nan)
    if "trackPrice" in df.columns:
        df["trackPrice_missing"] = df["trackPrice"].isna().astype(int)
        df["trackPrice"] = df["trackPrice"].fillna(df["trackPrice"].median())
    if "isStreamable" in df.columns:
        df["isStreamable"] = (
            df["isStreamable"].astype(str).str.lower().map({"true": True, "false": False})
        ).fillna(False).astype(int)
    drop_cols = [c for c in ["trackName", "collectionName", "artistName", "trackViewUrl", "trackId", "collectionId"]
                 if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)
    return df

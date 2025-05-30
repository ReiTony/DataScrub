import os
import pandas as pd
from uuid import uuid4

def generate_session_id() -> str:
    return uuid4().hex

def get_preview(df: pd.DataFrame, rows: int = 5) -> str:
    """Returns a stringified preview of the dataframe"""
    return df.head(rows).to_markdown()

def create_session_plot_dir(session_id: str) -> str:
    plot_dir = os.path.join("static", "plots", session_id)
    os.makedirs(plot_dir, exist_ok=True)
    return plot_dir
import os
import pandas as pd
from fastapi import UploadFile
from uuid import uuid4

UPLOAD_DIR = "static/uploads"

def save_upload_file(upload_file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_id = uuid4().hex
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{upload_file.filename}")
    
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    
    return file_path

def read_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")
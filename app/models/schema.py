from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    prompt: str
    session_id: str
    config: Optional[Dict[str, str]] = None 

class ChatResponse(BaseModel):
    action: str
    message: Optional[str] = None
    report: Optional[List[str]] = None
    missing_summary: Optional[Dict[str, int]] = None
    summary: Optional[Dict[str, Dict[str, str]]] = None
    plots: Optional[List[str]] = None
    download_url: Optional[str] = None

class UploadResponse(BaseModel):
    session_id: str
    preview: str

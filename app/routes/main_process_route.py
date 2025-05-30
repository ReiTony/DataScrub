from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.models.schema import ChatRequest, ChatResponse, UploadResponse
from app.utils.file_handler import save_upload_file, read_csv
from app.utils.helper import generate_session_id, create_session_plot_dir, get_preview
from app.services.chat_engine import ChatEngine

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
router = APIRouter()
SESSION_DATA = {}


# Upload Route
@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    file_path = save_upload_file(file)
    try:
        df = read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    session_id = generate_session_id()

    SESSION_DATA[session_id] = {"df": df, "filename": file.filename}

    preview = get_preview(df)
    logging.info(f"Upload successful — Session ID: {session_id}")
    logging.info(f"Preview:\n{preview}")

    return UploadResponse(session_id=session_id, preview=preview)

@router.post("/chat", response_model=ChatResponse)
async def chat_handler(chat: ChatRequest, request: Request):
    session_id = chat.session_id
    prompt = chat.prompt

    if session_id not in SESSION_DATA:
        raise HTTPException(
            status_code=404, detail="Session not found. Please upload a CSV first."
        )

    session = SESSION_DATA[session_id]
    df = session["df"]
    original_filename = session.get("filename", "dataset.csv")
    plot_dir = create_session_plot_dir(session_id)

    chatbot = ChatEngine(df, output_dir=plot_dir)
    response = chatbot.handle_prompt(prompt)

    base_url = str(request.base_url).rstrip("/")

    if response.get("action") == "cleaning":
        cleaned_df = chatbot.df
        SESSION_DATA[session_id]["df"] = cleaned_df

        base_name = os.path.splitext(original_filename)[0]
        cleaned_filename = f"{base_name}_cleaned.csv"
        cleaned_path = os.path.join("static", "cleaned", cleaned_filename)
        os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
        cleaned_df.to_csv(cleaned_path, index=False)

        response["download_url"] = f"{base_url}/static/cleaned/{cleaned_filename}"

    if response.get("plots"):
        response["plots"] = [f"{base_url}/{path}" for path in response["plots"]]

    return ChatResponse(**response)


# Preview current DataFrame
@router.get("/session/{session_id}/preview")
async def preview_session_data(session_id: str):
    if session_id not in SESSION_DATA:
        raise HTTPException(status_code=404, detail="Session not found.")

    df = SESSION_DATA[session_id]
    return {"preview": get_preview(df)}

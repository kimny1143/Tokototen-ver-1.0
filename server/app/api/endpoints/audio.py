from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import uuid
from typing import List, Optional
import logging
from app.tasks.audio_analysis import analyze_audio
from app.schemas.audio import AudioAnalysisResponse, AudioUploadResponse

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload an audio file for processing
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving file")
    
    return AudioUploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_path=file_path
    )

@router.post("/analyze/{file_id}", response_model=AudioAnalysisResponse)
async def analyze_audio_file(file_id: str, background_tasks: BackgroundTasks):
    """
    Analyze an uploaded audio file
    """
    for filename in os.listdir(UPLOAD_DIR):
        if filename.startswith(file_id):
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            try:
                analysis_result = analyze_audio(file_path)
                
                return AudioAnalysisResponse(
                    file_id=file_id,
                    key=analysis_result["key"],
                    tempo=analysis_result["tempo"],
                    time_signature=analysis_result["time_signature"],
                    downbeats=analysis_result["downbeats"]
                )
            except Exception as e:
                logger.error(f"Error analyzing file: {str(e)}")
                raise HTTPException(status_code=500, detail="Error analyzing file")
    
    raise HTTPException(status_code=404, detail="File not found")

@router.get("/status/{file_id}")
async def get_analysis_status(file_id: str):
    """
    Get the status of an audio analysis task
    """
    return {"status": "completed", "file_id": file_id}

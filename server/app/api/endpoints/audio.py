from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import uuid
import logging
from datetime import datetime

from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.audio import AudioFile, AnalysisResult
from app.crud.audio import audio_file, analysis_result
from app.tasks.audio_analysis import analyze_audio
from app.schemas.audio import (
    AudioFileCreate,
    AudioFile as AudioFileSchema,
    AnalysisResultCreate,
    AnalysisResult as AnalysisResultSchema,
    AudioUploadResponse,
    AudioAnalysisResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload an audio file for analysis
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_id = str(uuid.uuid4())
    unique_filename = f"{unique_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving file")
    
    file_obj = AudioFileCreate(
        filename=file.filename,
        file_path=file_path,
        file_size=len(contents),
        format=file_extension.lstrip('.'),
        user_id=current_user.id
    )
    
    db_file = audio_file.create(db=db, obj_in=file_obj)
    
    return AudioUploadResponse(
        file_id=str(db_file.id),
        filename=db_file.filename,
        file_path=db_file.file_path
    )


@router.get("/files", response_model=List[AudioFileSchema])
def get_user_audio_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all audio files uploaded by the current user
    """
    files = audio_file.get_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return files


@router.get("/files/{file_id}", response_model=AudioFileSchema)
def get_audio_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific audio file by ID
    """
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_file


@router.post("/analyze/{file_id}", response_model=AudioAnalysisResponse)
async def analyze_audio_file(
    file_id: int,
    background_tasks: BackgroundTasks,
    analysis_type: str = Form("general"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze an audio file
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    existing_analysis = analysis_result.get_by_type(
        db=db, audio_file_id=file_id, analysis_type=analysis_type
    )
    
    if existing_analysis:
        result = existing_analysis.result
        return AudioAnalysisResponse(
            file_id=str(db_file.id),
            key=result.get("key", "C"),
            tempo=result.get("tempo", 120.0),
            time_signature=result.get("time_signature", "4/4"),
            downbeats=result.get("downbeats", [])
        )
    
    try:
        analysis_result_data = analyze_audio(db_file.file_path)
        
        analysis_data = AnalysisResultCreate(
            audio_file_id=file_id,
            analysis_type=analysis_type,
            result=analysis_result_data,
            confidence=0.85,
            processing_time=1.2,
            notes="Audio analysis result"
        )
        
        analysis_obj = analysis_result.create(db=db, obj_in=analysis_data)
        
        return AudioAnalysisResponse(
            file_id=str(db_file.id),
            key=analysis_result_data["key"],
            tempo=analysis_result_data["tempo"],
            time_signature=analysis_result_data["time_signature"],
            downbeats=analysis_result_data["downbeats"]
        )
    except Exception as e:
        logger.error(f"Error analyzing file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing file")


@router.get("/analysis/{file_id}", response_model=List[AnalysisResultSchema])
def get_analysis_results(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all analysis results for a specific audio file
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    results = analysis_result.get_by_audio_file(db=db, audio_file_id=file_id)
    return results


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audio_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an audio file and its analysis results
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        if os.path.exists(db_file.file_path):
            os.remove(db_file.file_path)
    except Exception as e:
        logger.error(f"Error deleting file {db_file.file_path}: {e}")
    
    audio_file.remove(db=db, id=file_id)
    
    return None

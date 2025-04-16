from typing import List, Optional, Dict, Any, Union
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import uuid
import logging
import time
from datetime import datetime

from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.audio import AudioFile, AnalysisResult
from app.crud.audio import audio_file, analysis_result
from app.tasks.audio_analysis import analyze_audio
from app.services.ai_service import get_ai_service
from app.schemas.audio import (
    AudioFileCreate,
    AudioFile as AudioFileSchema,
    AnalysisResultCreate,
    AnalysisResult as AnalysisResultSchema,
    AudioUploadResponse,
    AudioAnalysisResponse,
    MusicTheoryAnalysisResponse,
    ProductionFeedbackResponse,
    ArrangementAnalysisResponse,
    AIAnalysisRequest
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
    analysis_request: AIAnalysisRequest = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze an audio file using AI services
    
    - **analysis_type**: Type of analysis to perform (general, music_theory, production_feedback, arrangement_analysis)
    - **ai_service**: AI service to use (gemini, openai, or None for default)
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    analysis_type = analysis_request.analysis_type
    ai_service_name = analysis_request.ai_service
    
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
            downbeats=result.get("downbeats", []),
            genre=result.get("genre"),
            sound_quality=result.get("sound_quality"),
            suggestions=result.get("suggestions")
        )
    
    try:
        start_time = time.time()
        
        analysis_result_data = analyze_audio(
            file_path=db_file.file_path,
            analysis_type=analysis_type,
            ai_service=ai_service_name
        )
        
        processing_time = time.time() - start_time
        
        analysis_data = AnalysisResultCreate(
            audio_file_id=file_id,
            analysis_type=analysis_type,
            result=analysis_result_data,
            confidence=analysis_result_data.get("confidence", 0.85),
            processing_time=processing_time,
            notes=f"AI analysis using {ai_service_name or 'default'} service"
        )
        
        analysis_obj = analysis_result.create(db=db, obj_in=analysis_data)
        
        return AudioAnalysisResponse(
            file_id=str(db_file.id),
            key=analysis_result_data.get("key", "C Major"),
            tempo=analysis_result_data.get("tempo", 120.0),
            time_signature=analysis_result_data.get("time_signature", "4/4"),
            downbeats=analysis_result_data.get("downbeats", []),
            genre=analysis_result_data.get("genre"),
            sound_quality=analysis_result_data.get("sound_quality"),
            suggestions=analysis_result_data.get("suggestions")
        )
    except Exception as e:
        logger.error(f"Error analyzing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing file: {str(e)}")


@router.post("/analyze/music-theory/{file_id}", response_model=MusicTheoryAnalysisResponse)
async def analyze_music_theory(
    file_id: int,
    background_tasks: BackgroundTasks,
    ai_service: Optional[str] = Query(None, description="AI service to use (gemini, openai, or None for default)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze music theory aspects of an audio file
    
    Returns detailed music theory analysis including:
    - Key and scale identification
    - Chord progression analysis
    - Harmonic structure
    - Suggestions for complementary chords
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    analysis_type = "music_theory"
    
    existing_analysis = analysis_result.get_by_type(
        db=db, audio_file_id=file_id, analysis_type=analysis_type
    )
    
    if existing_analysis:
        result = existing_analysis.result
        return MusicTheoryAnalysisResponse(
            file_id=str(db_file.id),
            key=result.get("key", "C Major"),
            tempo=result.get("tempo", 120.0),
            time_signature=result.get("time_signature", "4/4"),
            downbeats=result.get("downbeats", []),
            scale=result.get("scale"),
            chord_progression=result.get("chord_progression"),
            harmonic_analysis=result.get("harmonic_analysis"),
            suggestions=result.get("suggestions")
        )
    
    try:
        start_time = time.time()
        
        analysis_result_data = analyze_audio(
            file_path=db_file.file_path,
            analysis_type=analysis_type,
            ai_service=ai_service
        )
        
        processing_time = time.time() - start_time
        
        analysis_data = AnalysisResultCreate(
            audio_file_id=file_id,
            analysis_type=analysis_type,
            result=analysis_result_data,
            confidence=analysis_result_data.get("confidence", 0.85),
            processing_time=processing_time,
            notes=f"Music theory analysis using {ai_service or 'default'} service"
        )
        
        analysis_obj = analysis_result.create(db=db, obj_in=analysis_data)
        
        return MusicTheoryAnalysisResponse(
            file_id=str(db_file.id),
            key=analysis_result_data.get("key", "C Major"),
            tempo=analysis_result_data.get("tempo", 120.0),
            time_signature=analysis_result_data.get("time_signature", "4/4"),
            downbeats=analysis_result_data.get("downbeats", []),
            scale=analysis_result_data.get("scale"),
            chord_progression=analysis_result_data.get("chord_progression"),
            harmonic_analysis=analysis_result_data.get("harmonic_analysis"),
            suggestions=analysis_result_data.get("suggestions")
        )
    except Exception as e:
        logger.error(f"Error analyzing music theory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing music theory: {str(e)}")


@router.post("/analyze/production/{file_id}", response_model=ProductionFeedbackResponse)
async def analyze_production(
    file_id: int,
    background_tasks: BackgroundTasks,
    ai_service: Optional[str] = Query(None, description="AI service to use (gemini, openai, or None for default)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze production aspects of an audio file
    
    Returns detailed production feedback including:
    - Mix balance assessment
    - EQ recommendations
    - Dynamic processing suggestions
    - Spatial effects recommendations
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    analysis_type = "production_feedback"
    
    existing_analysis = analysis_result.get_by_type(
        db=db, audio_file_id=file_id, analysis_type=analysis_type
    )
    
    if existing_analysis:
        result = existing_analysis.result
        return ProductionFeedbackResponse(
            file_id=str(db_file.id),
            key=result.get("key", "C Major"),
            tempo=result.get("tempo", 120.0),
            time_signature=result.get("time_signature", "4/4"),
            downbeats=result.get("downbeats", []),
            mix_balance=result.get("mix_balance"),
            eq_recommendations=result.get("eq_recommendations"),
            dynamics_suggestions=result.get("dynamics_suggestions"),
            spatial_recommendations=result.get("spatial_recommendations"),
            suggestions=result.get("suggestions")
        )
    
    try:
        start_time = time.time()
        
        analysis_result_data = analyze_audio(
            file_path=db_file.file_path,
            analysis_type=analysis_type,
            ai_service=ai_service
        )
        
        processing_time = time.time() - start_time
        
        analysis_data = AnalysisResultCreate(
            audio_file_id=file_id,
            analysis_type=analysis_type,
            result=analysis_result_data,
            confidence=analysis_result_data.get("confidence", 0.85),
            processing_time=processing_time,
            notes=f"Production feedback analysis using {ai_service or 'default'} service"
        )
        
        analysis_obj = analysis_result.create(db=db, obj_in=analysis_data)
        
        return ProductionFeedbackResponse(
            file_id=str(db_file.id),
            key=analysis_result_data.get("key", "C Major"),
            tempo=analysis_result_data.get("tempo", 120.0),
            time_signature=analysis_result_data.get("time_signature", "4/4"),
            downbeats=analysis_result_data.get("downbeats", []),
            mix_balance=analysis_result_data.get("mix_balance"),
            eq_recommendations=analysis_result_data.get("eq_recommendations"),
            dynamics_suggestions=analysis_result_data.get("dynamics_suggestions"),
            spatial_recommendations=analysis_result_data.get("spatial_recommendations"),
            suggestions=analysis_result_data.get("suggestions")
        )
    except Exception as e:
        logger.error(f"Error analyzing production: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing production: {str(e)}")


@router.post("/analyze/arrangement/{file_id}", response_model=ArrangementAnalysisResponse)
async def analyze_arrangement(
    file_id: int,
    background_tasks: BackgroundTasks,
    ai_service: Optional[str] = Query(None, description="AI service to use (gemini, openai, or None for default)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze arrangement aspects of an audio file
    
    Returns detailed arrangement analysis including:
    - Structure identification
    - Instrumentation assessment
    - Energy flow analysis
    - Arrangement improvement suggestions
    """
    # Get the audio file
    db_file = audio_file.get(db=db, id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if db_file.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    analysis_type = "arrangement_analysis"
    
    existing_analysis = analysis_result.get_by_type(
        db=db, audio_file_id=file_id, analysis_type=analysis_type
    )
    
    if existing_analysis:
        result = existing_analysis.result
        return ArrangementAnalysisResponse(
            file_id=str(db_file.id),
            key=result.get("key", "C Major"),
            tempo=result.get("tempo", 120.0),
            time_signature=result.get("time_signature", "4/4"),
            downbeats=result.get("downbeats", []),
            structure=result.get("structure"),
            instrumentation=result.get("instrumentation"),
            energy_flow=result.get("energy_flow"),
            suggestions=result.get("suggestions")
        )
    
    try:
        start_time = time.time()
        
        analysis_result_data = analyze_audio(
            file_path=db_file.file_path,
            analysis_type=analysis_type,
            ai_service=ai_service
        )
        
        processing_time = time.time() - start_time
        
        analysis_data = AnalysisResultCreate(
            audio_file_id=file_id,
            analysis_type=analysis_type,
            result=analysis_result_data,
            confidence=analysis_result_data.get("confidence", 0.85),
            processing_time=processing_time,
            notes=f"Arrangement analysis using {ai_service or 'default'} service"
        )
        
        analysis_obj = analysis_result.create(db=db, obj_in=analysis_data)
        
        return ArrangementAnalysisResponse(
            file_id=str(db_file.id),
            key=analysis_result_data.get("key", "C Major"),
            tempo=analysis_result_data.get("tempo", 120.0),
            time_signature=analysis_result_data.get("time_signature", "4/4"),
            downbeats=analysis_result_data.get("downbeats", []),
            structure=analysis_result_data.get("structure"),
            instrumentation=analysis_result_data.get("instrumentation"),
            energy_flow=analysis_result_data.get("energy_flow"),
            suggestions=analysis_result_data.get("suggestions")
        )
    except Exception as e:
        logger.error(f"Error analyzing arrangement: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing arrangement: {str(e)}")


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

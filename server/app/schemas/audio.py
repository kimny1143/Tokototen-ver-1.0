from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class AudioFileBase(BaseModel):
    filename: str
    file_path: str
    file_size: int
    duration: Optional[float] = None
    format: Optional[str] = None
    sample_rate: Optional[int] = None
    user_id: Optional[int] = None


class AudioFileCreate(AudioFileBase):
    pass


class AudioFileUpdate(AudioFileBase):
    pass


class AudioFile(AudioFileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AnalysisResultBase(BaseModel):
    audio_file_id: int
    analysis_type: str
    result: Dict[str, Any]
    confidence: Optional[float] = None
    processing_time: Optional[float] = None
    notes: Optional[str] = None


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultUpdate(AnalysisResultBase):
    pass


class AnalysisResult(AnalysisResultBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AudioUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_path: str


class AudioAnalysisResponse(BaseModel):
    file_id: str
    key: str
    tempo: float
    time_signature: str
    downbeats: List[float]
    genre: Optional[str] = None
    sound_quality: Optional[str] = None
    suggestions: Optional[List[str]] = None


class MusicTheoryAnalysisResponse(AudioAnalysisResponse):
    scale: Optional[List[str]] = None
    chord_progression: Optional[List[str]] = None
    harmonic_analysis: Optional[str] = None


class ProductionFeedbackResponse(AudioAnalysisResponse):
    mix_balance: Optional[str] = None
    eq_recommendations: Optional[List[str]] = None
    dynamics_suggestions: Optional[List[str]] = None
    spatial_recommendations: Optional[List[str]] = None


class ArrangementAnalysisResponse(AudioAnalysisResponse):
    structure: Optional[List[str]] = None
    instrumentation: Optional[str] = None
    energy_flow: Optional[str] = None


class AIAnalysisRequest(BaseModel):
    analysis_type: str = Field(
        default="general",
        description="Type of analysis to perform (general, music_theory, production_feedback, arrangement_analysis)"
    )
    ai_service: Optional[str] = Field(
        default=None,
        description="AI service to use (gemini, openai, or None for default)"
    )

    
class AudioSourceSeparationResponse(BaseModel):
    file_id: str
    stems: List[str]
    
class AudioTranscriptionResponse(BaseModel):
    file_id: str
    midi_file: str
    notes: List[dict]

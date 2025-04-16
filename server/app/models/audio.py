from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    duration = Column(Float, nullable=True)  # Duration in seconds
    format = Column(String, nullable=True)  # File format (mp3, wav, etc.)
    sample_rate = Column(Integer, nullable=True)  # Sample rate in Hz
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="audio_files")
    analysis_results = relationship("AnalysisResult", back_populates="audio_file", cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    audio_file_id = Column(Integer, ForeignKey("audio_files.id"), nullable=False)
    analysis_type = Column(String, nullable=False)  # e.g., "key_detection", "tempo", "structure"
    result = Column(JSON, nullable=False)  # JSON data with analysis results
    confidence = Column(Float, nullable=True)  # Confidence score (0-1)
    processing_time = Column(Float, nullable=True)  # Processing time in seconds
    notes = Column(Text, nullable=True)  # Additional notes or AI insights
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    audio_file = relationship("AudioFile", back_populates="analysis_results")

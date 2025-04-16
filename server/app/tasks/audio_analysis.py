from celery import shared_task
import logging
import os
import time
from typing import Dict, Any, Optional, List

from app.services.ai_service import get_ai_service
from app.services.audio_feature_extraction import (
    extract_audio_features,
    detect_beats,
    detect_segments
)

logger = logging.getLogger(__name__)

@shared_task
def analyze_audio(file_path: str, analysis_type: str = "general", ai_service: str = None) -> Dict[str, Any]:
    """
    Analyze audio file to extract key, tempo, time signature, and other musical features.
    Uses AI services for advanced analysis.
    
    Args:
        file_path: Path to the audio file to analyze
        analysis_type: Type of analysis to perform (general, music_theory, production_feedback, arrangement_analysis)
        ai_service: AI service to use (gemini, openai, or None for default)
        
    Returns:
        dict: Analysis results including key, tempo, time signature, etc.
    """
    logger.info(f"Starting audio analysis for {file_path} with type {analysis_type}")
    start_time = time.time()
    
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return {
                "key": "Unknown",
                "tempo": 0,
                "time_signature": "Unknown",
                "downbeats": [],
                "error": "File not found"
            }
        
        audio_features = extract_audio_features(file_path)
        
        beats = detect_beats(file_path)
        
        segments = detect_segments(file_path)
        
        audio_features["beats"] = beats
        audio_features["segments"] = segments
        
        basic_result = {
            "key": f"{audio_features['detected_key']} {audio_features['detected_scale']}",
            "tempo": audio_features["tempo"],
            "time_signature": "4/4",  # Default, could be improved with better detection
            "downbeats": beats[:10] if beats else []  # First 10 beats as downbeats
        }
        
        if analysis_type == "basic":
            logger.info(f"Completed basic audio analysis for {file_path} in {time.time() - start_time:.2f}s")
            return basic_result
        
        try:
            ai_service_instance = get_ai_service(ai_service)
            
            ai_result = ai_service_instance.analyze_audio_content(audio_features, analysis_type)
            
            result = {**basic_result, **ai_result}
            
            if "key" not in result:
                result["key"] = basic_result["key"]
            if "tempo" not in result:
                result["tempo"] = basic_result["tempo"]
            if "time_signature" not in result:
                result["time_signature"] = basic_result["time_signature"]
            if "downbeats" not in result:
                result["downbeats"] = basic_result["downbeats"]
            
            logger.info(f"Completed AI audio analysis for {file_path} in {time.time() - start_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            logger.info(f"Falling back to basic analysis for {file_path}")
            return basic_result
    
    except Exception as e:
        logger.error(f"Error analyzing audio: {str(e)}")
        return {
            "key": "C Major",
            "tempo": 120,
            "time_signature": "4/4",
            "downbeats": [0.0, 2.0, 4.0],
            "error": str(e)
        }

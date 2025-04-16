"""
AI service integration for audio analysis using Gemini and OpenAI APIs.
"""
import os
import json
import logging
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """Base class for AI service integration."""
    
    def analyze_audio_content(self, audio_data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """
        Analyze audio content using AI.
        
        Args:
            audio_data: Dictionary containing audio metadata and features
            analysis_type: Type of analysis to perform
            
        Returns:
            Dictionary containing analysis results
        """
        raise NotImplementedError("Subclasses must implement this method")


class GeminiService(AIService):
    """Gemini API integration for audio analysis."""
    
    def __init__(self):
        """Initialize Gemini API client."""
        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY not set in environment variables")
            raise ValueError("GEMINI_API_KEY environment variable must be set")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_audio_content(self, audio_data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """
        Analyze audio content using Gemini API.
        
        Args:
            audio_data: Dictionary containing audio metadata and features
            analysis_type: Type of analysis to perform
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            prompt = self._create_prompt(audio_data, analysis_type)
            response = self.model.generate_content(prompt)
            
            result = self._parse_response(response.text, analysis_type)
            return result
        
        except Exception as e:
            logger.error(f"Error analyzing audio with Gemini: {str(e)}")
            return self._get_default_result(analysis_type)
    
    def _create_prompt(self, audio_data: Dict[str, Any], analysis_type: str) -> str:
        """Create a prompt for Gemini based on analysis type."""
        base_prompt = f"""
        You are a professional music producer and audio engineer. 
        Analyze the following audio data and provide insights.
        
        Audio data:
        {json.dumps(audio_data, indent=2)}
        
        Analysis type: {analysis_type}
        """
        
        if analysis_type == "music_theory":
            base_prompt += """
            Provide a detailed music theory analysis including:
            - Key and scale identification
            - Chord progression analysis
            - Harmonic structure
            - Suggestions for complementary chords
            
            Format your response as JSON with the following structure:
            {
                "key": "C Major",
                "scale": ["C", "D", "E", "F", "G", "A", "B"],
                "chord_progression": ["C", "Am", "F", "G"],
                "harmonic_analysis": "The progression follows a I-vi-IV-V pattern...",
                "suggestions": ["Try adding a secondary dominant...", "Consider a modal interchange..."]
            }
            """
        elif analysis_type == "production_feedback":
            base_prompt += """
            Provide production feedback including:
            - Mix balance assessment
            - EQ recommendations
            - Dynamic processing suggestions
            - Spatial effects recommendations
            
            Format your response as JSON with the following structure:
            {
                "mix_balance": "The low-end is slightly overpowering...",
                "eq_recommendations": ["Cut around 200Hz to reduce muddiness", "Boost at 3kHz for clarity"],
                "dynamics_suggestions": ["Apply more compression to the bass", "Consider multiband compression for..."],
                "spatial_recommendations": ["Add a short room reverb", "Pan elements wider for more stereo width"]
            }
            """
        elif analysis_type == "arrangement_analysis":
            base_prompt += """
            Provide arrangement analysis including:
            - Structure identification
            - Instrumentation assessment
            - Energy flow analysis
            - Arrangement improvement suggestions
            
            Format your response as JSON with the following structure:
            {
                "structure": ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Bridge", "Chorus", "Outro"],
                "instrumentation": "The arrangement uses a standard rock band setup with...",
                "energy_flow": "The energy builds gradually through the verses and peaks at...",
                "suggestions": ["Consider adding a pre-chorus to build tension", "The bridge could benefit from..."]
            }
            """
        else:  # general analysis
            base_prompt += """
            Provide a general analysis including:
            - Key and tempo identification
            - Overall sound quality assessment
            - Genre classification
            - General improvement suggestions
            
            Format your response as JSON with the following structure:
            {
                "key": "C Major",
                "tempo": 120,
                "time_signature": "4/4",
                "genre": "Pop/Rock",
                "sound_quality": "Good overall balance with some issues in...",
                "suggestions": ["Consider adjusting the levels of...", "The rhythm section could benefit from..."]
            }
            """
        
        return base_prompt
    
    def _parse_response(self, response_text: str, analysis_type: str) -> Dict[str, Any]:
        """Parse the response from Gemini API."""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                logger.warning("Could not extract JSON from Gemini response")
                return self._get_default_result(analysis_type)
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from Gemini response")
            return self._get_default_result(analysis_type)
    
    def _get_default_result(self, analysis_type: str) -> Dict[str, Any]:
        """Get default result based on analysis type."""
        if analysis_type == "music_theory":
            return {
                "key": "C Major",
                "scale": ["C", "D", "E", "F", "G", "A", "B"],
                "chord_progression": ["C", "Am", "F", "G"],
                "harmonic_analysis": "Unable to analyze harmonic structure",
                "suggestions": ["Consider analyzing with more detailed audio features"]
            }
        elif analysis_type == "production_feedback":
            return {
                "mix_balance": "Unable to analyze mix balance",
                "eq_recommendations": ["Consider professional mixing services"],
                "dynamics_suggestions": ["Apply standard compression techniques"],
                "spatial_recommendations": ["Experiment with different reverb settings"]
            }
        elif analysis_type == "arrangement_analysis":
            return {
                "structure": ["Intro", "Verse", "Chorus", "Outro"],
                "instrumentation": "Unable to analyze instrumentation",
                "energy_flow": "Unable to analyze energy flow",
                "suggestions": ["Consider professional arrangement analysis"]
            }
        else:  # general analysis
            return {
                "key": "C Major",
                "tempo": 120,
                "time_signature": "4/4",
                "genre": "Unknown",
                "sound_quality": "Unable to analyze sound quality",
                "suggestions": ["Consider providing more detailed audio features"]
            }


class OpenAIService(AIService):
    """OpenAI API integration for audio analysis."""
    
    def __init__(self):
        """Initialize OpenAI API client."""
        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not set in environment variables")
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def analyze_audio_content(self, audio_data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """
        Analyze audio content using OpenAI API.
        
        Args:
            audio_data: Dictionary containing audio metadata and features
            analysis_type: Type of analysis to perform
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            prompt = self._create_prompt(audio_data, analysis_type)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional music producer and audio engineer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = self._parse_response(response.choices[0].message.content, analysis_type)
            return result
        
        except Exception as e:
            logger.error(f"Error analyzing audio with OpenAI: {str(e)}")
            return self._get_default_result(analysis_type)
    
    def _create_prompt(self, audio_data: Dict[str, Any], analysis_type: str) -> str:
        """Create a prompt for OpenAI based on analysis type."""
        base_prompt = f"""
        Analyze the following audio data and provide insights.
        
        Audio data:
        {json.dumps(audio_data, indent=2)}
        
        Analysis type: {analysis_type}
        """
        
        if analysis_type == "music_theory":
            base_prompt += """
            Provide a detailed music theory analysis including:
            - Key and scale identification
            - Chord progression analysis
            - Harmonic structure
            - Suggestions for complementary chords
            
            Format your response as JSON with the following structure:
            {
                "key": "C Major",
                "scale": ["C", "D", "E", "F", "G", "A", "B"],
                "chord_progression": ["C", "Am", "F", "G"],
                "harmonic_analysis": "The progression follows a I-vi-IV-V pattern...",
                "suggestions": ["Try adding a secondary dominant...", "Consider a modal interchange..."]
            }
            """
        elif analysis_type == "production_feedback":
            base_prompt += """
            Provide production feedback including:
            - Mix balance assessment
            - EQ recommendations
            - Dynamic processing suggestions
            - Spatial effects recommendations
            
            Format your response as JSON with the following structure:
            {
                "mix_balance": "The low-end is slightly overpowering...",
                "eq_recommendations": ["Cut around 200Hz to reduce muddiness", "Boost at 3kHz for clarity"],
                "dynamics_suggestions": ["Apply more compression to the bass", "Consider multiband compression for..."],
                "spatial_recommendations": ["Add a short room reverb", "Pan elements wider for more stereo width"]
            }
            """
        elif analysis_type == "arrangement_analysis":
            base_prompt += """
            Provide arrangement analysis including:
            - Structure identification
            - Instrumentation assessment
            - Energy flow analysis
            - Arrangement improvement suggestions
            
            Format your response as JSON with the following structure:
            {
                "structure": ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Bridge", "Chorus", "Outro"],
                "instrumentation": "The arrangement uses a standard rock band setup with...",
                "energy_flow": "The energy builds gradually through the verses and peaks at...",
                "suggestions": ["Consider adding a pre-chorus to build tension", "The bridge could benefit from..."]
            }
            """
        else:  # general analysis
            base_prompt += """
            Provide a general analysis including:
            - Key and tempo identification
            - Overall sound quality assessment
            - Genre classification
            - General improvement suggestions
            
            Format your response as JSON with the following structure:
            {
                "key": "C Major",
                "tempo": 120,
                "time_signature": "4/4",
                "genre": "Pop/Rock",
                "sound_quality": "Good overall balance with some issues in...",
                "suggestions": ["Consider adjusting the levels of...", "The rhythm section could benefit from..."]
            }
            """
        
        return base_prompt
    
    def _parse_response(self, response_text: str, analysis_type: str) -> Dict[str, Any]:
        """Parse the response from OpenAI API."""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                logger.warning("Could not extract JSON from OpenAI response")
                return self._get_default_result(analysis_type)
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from OpenAI response")
            return self._get_default_result(analysis_type)
    
    def _get_default_result(self, analysis_type: str) -> Dict[str, Any]:
        """Get default result based on analysis type."""
        if analysis_type == "music_theory":
            return {
                "key": "C Major",
                "scale": ["C", "D", "E", "F", "G", "A", "B"],
                "chord_progression": ["C", "Am", "F", "G"],
                "harmonic_analysis": "Unable to analyze harmonic structure",
                "suggestions": ["Consider analyzing with more detailed audio features"]
            }
        elif analysis_type == "production_feedback":
            return {
                "mix_balance": "Unable to analyze mix balance",
                "eq_recommendations": ["Consider professional mixing services"],
                "dynamics_suggestions": ["Apply standard compression techniques"],
                "spatial_recommendations": ["Experiment with different reverb settings"]
            }
        elif analysis_type == "arrangement_analysis":
            return {
                "structure": ["Intro", "Verse", "Chorus", "Outro"],
                "instrumentation": "Unable to analyze instrumentation",
                "energy_flow": "Unable to analyze energy flow",
                "suggestions": ["Consider professional arrangement analysis"]
            }
        else:  # general analysis
            return {
                "key": "C Major",
                "tempo": 120,
                "time_signature": "4/4",
                "genre": "Unknown",
                "sound_quality": "Unable to analyze sound quality",
                "suggestions": ["Consider providing more detailed audio features"]
            }


def get_ai_service(service_name: str = None) -> AIService:
    """
    Factory function to get the appropriate AI service.
    
    Args:
        service_name: Name of the AI service to use ('gemini' or 'openai')
        
    Returns:
        AIService instance
    """
    if not service_name:
        if settings.GEMINI_API_KEY:
            return GeminiService()
        elif settings.OPENAI_API_KEY:
            return OpenAIService()
        else:
            raise ValueError("No AI service API keys configured")
    
    if service_name.lower() == "gemini":
        return GeminiService()
    elif service_name.lower() == "openai":
        return OpenAIService()
    else:
        raise ValueError(f"Unknown AI service: {service_name}")

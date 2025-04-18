try:
    from app.services.ai_service import get_ai_service, AIService, GeminiService, OpenAIService
    __all__ = ["get_ai_service", "AIService", "GeminiService", "OpenAIService"]
except ImportError:
    __all__ = []

try:
    from app.services.audio_separation import separate_stems
    __all__ += ["separate_stems"]
except ImportError:
    pass

try:
    from app.services.transcription import transcribe_stem, save_midi, transcribe_and_save
    __all__ += ["transcribe_stem", "save_midi", "transcribe_and_save"]
except ImportError:
    pass

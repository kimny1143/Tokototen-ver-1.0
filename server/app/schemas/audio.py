from pydantic import BaseModel
from typing import List, Optional

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
    
class AudioSourceSeparationResponse(BaseModel):
    file_id: str
    stems: List[str]
    
class AudioTranscriptionResponse(BaseModel):
    file_id: str
    midi_file: str
    notes: List[dict]

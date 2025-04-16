"""
Audio feature extraction utilities for AI analysis.
"""
import os
import logging
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import librosa

logger = logging.getLogger(__name__)

def extract_audio_features(file_path: str) -> Dict[str, Any]:
    """
    Extract audio features from an audio file for AI analysis.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary containing extracted audio features
    """
    try:
        y, sr = librosa.load(file_path, sr=None)
        
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
        
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
        
        harmonic, percussive = librosa.effects.hpss(y)
        chroma = librosa.feature.chroma_cqt(y=harmonic, sr=sr).mean(axis=1)
        
        key, scale = detect_key(chroma)
        
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(axis=1)
        
        features = {
            "duration": float(duration),
            "tempo": float(tempo),
            "spectral_centroid": float(spectral_centroid),
            "spectral_bandwidth": float(spectral_bandwidth),
            "spectral_rolloff": float(spectral_rolloff),
            "chroma_features": chroma.tolist(),
            "mfccs": mfccs.tolist(),
            "detected_key": key,
            "detected_scale": scale,
            "file_info": {
                "sample_rate": sr,
                "file_path": file_path,
                "file_name": os.path.basename(file_path)
            }
        }
        
        return features
    
    except Exception as e:
        logger.error(f"Error extracting audio features: {str(e)}")
        return {
            "duration": 0.0,
            "tempo": 120.0,
            "detected_key": "Unknown",
            "detected_scale": "Unknown",
            "file_info": {
                "file_path": file_path,
                "file_name": os.path.basename(file_path)
            },
            "error": str(e)
        }


def detect_key(chroma_features: np.ndarray) -> Tuple[str, str]:
    """
    Detect musical key from chroma features.
    
    Args:
        chroma_features: Chromagram features
        
    Returns:
        Tuple of (key, scale)
    """
    major_template = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
    minor_template = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
    
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    major_correlations = np.zeros(12)
    minor_correlations = np.zeros(12)
    
    for i in range(12):
        shifted_major = np.roll(major_template, i)
        shifted_minor = np.roll(minor_template, i)
        
        major_correlations[i] = np.corrcoef(chroma_features, shifted_major)[0, 1]
        minor_correlations[i] = np.corrcoef(chroma_features, shifted_minor)[0, 1]
    
    max_major_idx = np.argmax(major_correlations)
    max_minor_idx = np.argmax(minor_correlations)
    
    if major_correlations[max_major_idx] > minor_correlations[max_minor_idx]:
        return key_names[max_major_idx], "Major"
    else:
        return key_names[max_minor_idx], "Minor"


def detect_beats(file_path: str) -> List[float]:
    """
    Detect beat positions in an audio file.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        List of beat positions in seconds
    """
    try:
        y, sr = librosa.load(file_path, sr=None)
        
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        return beat_times.tolist()
    
    except Exception as e:
        logger.error(f"Error detecting beats: {str(e)}")
        return []


def detect_segments(file_path: str) -> List[Dict[str, Any]]:
    """
    Detect structural segments in an audio file.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        List of segment dictionaries with start, end, and label
    """
    try:
        y, sr = librosa.load(file_path, sr=None)
        
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        boundary_frames = librosa.segment.agglomerative(mfcc, k=5)
        boundary_times = librosa.frames_to_time(boundary_frames, sr=sr)
        
        segments = []
        for i in range(len(boundary_times) - 1):
            segment = {
                "start": float(boundary_times[i]),
                "end": float(boundary_times[i + 1]),
                "label": f"Segment {i+1}"
            }
            segments.append(segment)
        
        return segments
    
    except Exception as e:
        logger.error(f"Error detecting segments: {str(e)}")
        return []

import os
import shutil
import tempfile
from pathlib import Path
import uuid

import numpy as np
import pytest
import torch
import torchaudio

from app.services.audio_separation import separate_stems


@pytest.fixture
def sample_audio_file():
    """Create a sample audio file for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    
    sample_rate = 44100
    duration = 5  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    frequency = 440  # A4 note
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    audio_data = np.stack([audio_data, audio_data])
    
    audio_tensor = torch.tensor(audio_data)
    
    audio_path = temp_dir / "sample.wav"
    torchaudio.save(audio_path, audio_tensor, sample_rate)
    
    yield audio_path
    
    shutil.rmtree(temp_dir)


def test_separate_stems(sample_audio_file):
    """Test that separate_stems correctly separates audio into stems"""
    output_dir = Path(tempfile.mkdtemp()) / str(uuid.uuid4())
    
    try:
        stem_paths = separate_stems(sample_audio_file, output_dir)
        
        assert len(stem_paths) == 4, f"Expected 4 stems, got {len(stem_paths)}"
        
        expected_stems = ["vocals", "drums", "bass", "other"]
        for stem in expected_stems:
            assert stem in stem_paths, f"Missing {stem} stem"
            assert stem_paths[stem].exists(), f"Stem file {stem_paths[stem]} does not exist"
        
        original_info = torchaudio.info(sample_audio_file)
        original_duration = original_info.num_frames / original_info.sample_rate
        
        for stem, path in stem_paths.items():
            stem_info = torchaudio.info(path)
            stem_duration = stem_info.num_frames / stem_info.sample_rate
            
            assert abs(stem_duration - original_duration) <= 0.5, \
                f"Stem {stem} duration ({stem_duration}s) differs from original ({original_duration}s) by more than 0.5s"
            
            assert stem_info.sample_rate == 44100, \
                f"Expected sample rate 44100, got {stem_info.sample_rate}"
    
    finally:
        if output_dir.exists():
            shutil.rmtree(output_dir.parent)

import os
import shutil
import tempfile
import time
from pathlib import Path
import uuid

import numpy as np
import pytest
import torch
import torchaudio
import pretty_midi
import librosa
import soundfile as sf

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.transcription import transcribe_stem, save_midi, transcribe_and_save, transcribe_and_save_all, transcribe_stems_to_one_midi


@pytest.fixture
def sample_audio_file():
    """Create a sample audio file for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    
    sample_rate = 44100
    duration = 30  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    audio_data = 0.3 * np.sin(2 * np.pi * 440 * t)  # A4
    audio_data += 0.2 * np.sin(2 * np.pi * 554 * t)  # C#5
    audio_data += 0.15 * np.sin(2 * np.pi * 659 * t)  # E5
    
    audio_data = np.stack([audio_data, audio_data])
    
    audio_tensor = torch.tensor(audio_data)
    
    audio_path = temp_dir / "sample_stem.wav"
    torchaudio.save(audio_path, audio_tensor, sample_rate)
    
    yield audio_path
    
    shutil.rmtree(temp_dir)


@pytest.fixture
def output_dir():
    """Create a temporary directory for output files"""
    temp_dir = Path(tempfile.mkdtemp()) / "midi"
    os.makedirs(temp_dir, exist_ok=True)
    
    yield temp_dir
    
    shutil.rmtree(temp_dir.parent)


def test_transcribe_stem(sample_audio_file):
    """Test that transcribe_stem correctly transcribes audio to MIDI"""
    start_time = time.time()
    
    midi = transcribe_stem(sample_audio_file)
    
    end_time = time.time()
    transcription_time = end_time - start_time
    
    assert transcription_time <= 30, f"Transcription took {transcription_time:.2f}s, which exceeds the 30s limit"
    
    assert midi.resolution == 480, f"Expected PPQ of 480, got {midi.resolution}"
    
    assert abs(midi.get_tempo_changes()[1][0] - 120.0) < 1.0, f"Expected tempo of 120 BPM, got {midi.get_tempo_changes()[1][0]}"
    
    assert len(midi.instruments) > 0, "No instruments in MIDI"
    assert sum(len(instrument.notes) for instrument in midi.instruments) > 0, "No notes in MIDI"


def test_save_midi(output_dir):
    """Test that save_midi correctly saves a MIDI file"""
    midi = pretty_midi.PrettyMIDI(initial_tempo=120.0)
    midi.resolution = 480
    
    instrument = pretty_midi.Instrument(program=0)
    note = pretty_midi.Note(velocity=80, pitch=60, start=0.0, end=1.0)
    instrument.notes.append(note)
    midi.instruments.append(instrument)
    
    output_path = output_dir / f"{uuid.uuid4()}.mid"
    saved_path = save_midi(midi, output_path)
    
    assert saved_path.exists(), f"MIDI file {saved_path} does not exist"
    
    loaded_midi = pretty_midi.PrettyMIDI(str(saved_path))
    assert loaded_midi.resolution == 480, f"Expected PPQ of 480, got {loaded_midi.resolution}"
    assert len(loaded_midi.instruments) > 0, "No instruments in loaded MIDI"
    assert len(loaded_midi.instruments[0].notes) > 0, "No notes in loaded MIDI"


def test_transcribe_and_save(sample_audio_file, output_dir):
    """Test that transcribe_and_save correctly transcribes and saves a MIDI file"""
    start_time = time.time()
    
    output_path = transcribe_and_save(sample_audio_file, output_dir)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    assert total_time <= 30, f"Transcription and saving took {total_time:.2f}s, which exceeds the 30s limit"
    
    assert output_path.exists(), f"MIDI file {output_path} does not exist"
    
    midi = pretty_midi.PrettyMIDI(str(output_path))
    
    assert midi.resolution == 480, f"Expected PPQ of 480, got {midi.resolution}"
    
    assert abs(midi.get_tempo_changes()[1][0] - 120.0) < 1.0, f"Expected tempo of 120 BPM, got {midi.get_tempo_changes()[1][0]}"
    
    assert len(midi.instruments) > 0, "No instruments in MIDI"
    assert sum(len(instrument.notes) for instrument in midi.instruments) > 0, "No notes in MIDI"
    
    total_duration = midi.get_end_time()
    assert 29 <= total_duration <= 31, f"Expected duration between 29 and 31 seconds, got {total_duration:.2f}s"


def test_transcription(tmp_path):
    """Test that transcribe_stem correctly transcribes a simple tone to MIDI"""
    wav = librosa.tone(440, duration=3.0, sr=16000)
    sf.write(tmp_path/"tone.wav", wav, 16000)
    
    midi = transcribe_stem(tmp_path/"tone.wav")
    
    assert len(midi.instruments[0].notes) > 0, "No notes in MIDI"
    assert midi.resolution == 480, f"Expected PPQ of 480, got {midi.resolution}"


def test_transcribe_stems_to_one_midi(tmp_path):
    """Test that transcribe_stems_to_one_midi correctly combines multiple stems into a single MIDI file"""
    if os.getenv("CI") == "true":
        pytest.skip("Skipping MT3 test on CI")
    
    stem_dir = tmp_path / "stems"
    os.makedirs(stem_dir, exist_ok=True)
    
    kick_wav = np.sin(2 * np.pi * 100 * np.linspace(0, 3, 48000))  # 3 seconds of 100Hz sine (kick)
    snare_wav = np.sin(2 * np.pi * 300 * np.linspace(0, 3, 48000))  # 3 seconds of 300Hz sine (snare)
    
    sf.write(stem_dir / "kick.wav", kick_wav, 16000)
    sf.write(stem_dir / "snare.wav", snare_wav, 16000)
    
    output_dir = tmp_path / "midi"
    os.makedirs(output_dir, exist_ok=True)
    
    start_time = time.time()
    
    output_path = transcribe_stems_to_one_midi(stem_dir, output_dir / "combined.mid")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    assert total_time <= 30, f"Transcription and combining took {total_time:.2f}s, which exceeds the 30s limit"
    
    assert output_path.exists(), f"Combined MIDI file {output_path} does not exist"
    
    midi = pretty_midi.PrettyMIDI(str(output_path))
    
    assert midi.resolution == 480, f"Expected PPQ of 480, got {midi.resolution}"
    
    assert abs(midi.get_tempo_changes()[1][0] - 120.0) < 1.0, f"Expected tempo of 120 BPM, got {midi.get_tempo_changes()[1][0]}"
    
    assert len(midi.instruments) >= 2, f"Expected at least 2 tracks, got {len(midi.instruments)}"
    
    track_names = [instrument.name for instrument in midi.instruments]
    assert "kick" in track_names, "Missing 'kick' track"
    assert "snare" in track_names, "Missing 'snare' track"
    
    total_notes = sum(len(instrument.notes) for instrument in midi.instruments)
    assert total_notes > 0, "No notes found in the combined MIDI file"

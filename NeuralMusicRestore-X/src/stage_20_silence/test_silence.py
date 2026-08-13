"""
Test Stage 20: Silence Detection and Trimming
"""

import numpy as np
import os
import tempfile
import pytest
from adapter import SilenceAdapter
from stage_01_wav_pcm.adapter import WavAdapter


def test_detect_silence():
    """Test silence detection."""
    # Generate a test signal with silence at the beginning and end
    samplerate = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Silence (first and last 0.5 seconds)
    silence = np.zeros(int(samplerate * 0.5))
    # Audio (middle 2 seconds)
    audio = np.sin(2 * np.pi * 1000 * t[int(samplerate * 0.5):int(samplerate * 2.5)]) * 0.5
    
    # Combine into a single channel
    full_audio = np.concatenate([silence, audio, silence])
    stereo_audio = np.column_stack((full_audio, full_audio))
    
    # Write to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        input_file = tmp_file.name
    
    with WavAdapter(input_file, "w") as wav:
        wav.write(stereo_audio)
    
    # Detect silence
    adapter = SilenceAdapter()
    start, end = adapter.detect_silence(input_file, threshold=-40.0, duration=0.1)
    
    # Verify silence boundaries
    assert start == pytest.approx(0.5, rel=0.1)
    assert end == pytest.approx(2.5, rel=0.1)
    
    # Cleanup
    os.remove(input_file)


def test_trim_silence():
    """Test silence trimming."""
    # Generate a test signal with silence at the beginning and end
    samplerate = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Silence (first and last 0.5 seconds)
    silence = np.zeros(int(samplerate * 0.5))
    # Audio (middle 2 seconds)
    audio = np.sin(2 * np.pi * 1000 * t[int(samplerate * 0.5):int(samplerate * 2.5)]) * 0.5
    
    # Combine into a single channel
    full_audio = np.concatenate([silence, audio, silence])
    stereo_audio = np.column_stack((full_audio, full_audio))
    
    # Write to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_input:
        input_file = tmp_input.name
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_output:
        output_file = tmp_output.name
    
    with WavAdapter(input_file, "w") as wav:
        wav.write(stereo_audio)
    
    # Trim silence
    adapter = SilenceAdapter()
    adapter.trim_silence(input_file, output_file, threshold=-40.0, duration=0.1)
    
    # Verify trimmed audio
    with WavAdapter(output_file, "r") as wav:
        trimmed_audio = wav.read()
    
    # Trimmed audio should match the non-silent section
    assert trimmed_audio.shape[0] == len(audio)
    assert np.allclose(trimmed_audio[:, 0], audio, atol=1e-6)
    
    # Cleanup
    os.remove(input_file)
    os.remove(output_file)


if __name__ == "__main__":
    test_detect_silence()
    test_trim_silence()
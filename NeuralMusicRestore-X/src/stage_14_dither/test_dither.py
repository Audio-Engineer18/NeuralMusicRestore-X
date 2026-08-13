"""
Test Stage 14: Dithering
"""

import numpy as np
import pytest
from adapter import DitherAdapter


def test_dither():
    """Test dithering."""
    # Generate a test signal (1kHz sine wave)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    audio = np.sin(2 * np.pi * 1000 * t) * 0.5  # Low amplitude to test dithering
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply dithering
    adapter = DitherAdapter(samplerate=samplerate, bits_per_sample=24)
    dithered_audio = adapter.process(stereo_audio)
    
    # Verify output type and range
    assert dithered_audio.dtype == np.int32
    assert np.max(np.abs(dithered_audio)) <= 2 ** 23  # 24-bit range


def test_dither_to_float():
    """Test dithering and conversion back to float."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    audio = np.sin(2 * np.pi * 1000 * t) * 0.5
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply dithering and convert back to float
    adapter = DitherAdapter(samplerate=samplerate,    bits_per_sample=24)
    dithered_float = adapter.process_to_float(stereo_audio)
    
    # Verify output type and range
    assert dithered_float.dtype == np.float32
    assert np.max(np.abs(dithered_float)) <= 1.0


if __name__ == "__main__":
    test_dither()
    test_dither_to_float()
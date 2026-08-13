"""
Test Stage 03: RF64 Adapter
"""

import numpy as np
import os
import pytest
from adapter import RF64Adapter


def test_write_and_validate_rf64():
    """Test writing and validating an RF64 file."""
    # Create a large audio buffer (>4GB in theory, but we'll use a smaller chunk for testing)
    samplerate = 44100
    duration = 10.0  # seconds (smaller for testing)
    frequency = 440.0  # Hz (A4 note)
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))  # Stereo
    
    # Write the RF64 file
    test_file = "test_rf64.wav"
    with RF64Adapter(test_file, "w", samplerate=samplerate, channels=2) as rf64:
        rf64.write(stereo_data)
    
    # Validate the RF64 file
    assert RF64Adapter.validate_rf64(test_file)
    
    # Cleanup
    os.remove(test_file)


def test_validate_non_rf64():
    """Test that a non-RF64 file is not validated as RF64."""
    # Create a regular WAV file
    from stage_01_wav_pcm.adapter import WavAdapter
    
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    test_file = "test_regular.wav"
    with WavAdapter(test_file, "w") as wav:
        wav.write(stereo_data)
    
    # Validate that it's not RF64
    assert not RF64Adapter.validate_rf64(test_file)
    
    # Cleanup
    os.remove(test_file)


if __name__ == "__main__":
    test_write_and_validate_rf64()
    test_validate_non_rf64()
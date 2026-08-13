"""
Test Stage 01: WAV/PCM Adapter
"""

import numpy as np
import os
import pytest
from adapter import WavAdapter


def test_read_write_wav():
    """Test reading and writing a WAV file."""
    # Create a test WAV file
    samplerate = 44100
    duration = 1.0  # seconds
    frequency = 440.0  # Hz (A4 note)
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))  # Stereo
    
    # Write the WAV file
    test_file = "test.wav"
    with WavAdapter(test_file, "w") as wav:
        wav.write(stereo_data)
    
    # Read the WAV file
    with WavAdapter(test_file, "r") as wav:
        read_data = wav.read()
        assert read_data.shape == stereo_data.shape
        assert wav.samplerate == samplerate
        assert wav.channels == 2
    
    # Cleanup
    os.remove(test_file)


if __name__ == "__main__":
    test_read_write_wav()
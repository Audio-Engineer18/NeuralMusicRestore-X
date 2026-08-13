"""
Test Stage 05: Channel Layout Engine
"""

import numpy as np
import os
import pytest
from adapter import ChannelAdapter
from stage_01_wav_pcm.adapter import WavAdapter


def test_convert_channels():
    """Test converting stereo to mono."""
    # Create a test WAV file (stereo)
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    test_file = "test_stereo.wav"
    with WavAdapter(test_file, "w") as wav:
        wav.write(stereo_data)
    
    # Convert to mono
    adapter = ChannelAdapter()
    mono_file = "test_mono.wav"
    adapter.convert_channels(test_file, mono_file, output_channels=1, output_layout="mono")
    
    # Verify the output
    with WavAdapter(mono_file, "r") as wav:
        mono_data = wav.read()
        assert mono_data.shape[1] == 1  # Mono
    
    # Cleanup
    os.remove(test_file)
    os.remove(mono_file)


def test_extract_channel():
    """Test extracting a single channel from stereo."""
    # Create a test WAV file (stereo)
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    left_data = np.sin(2 * np.pi * frequency * t)
    right_data = np.sin(2 * np.pi * (frequency + 100) * t)  # Different frequency for right channel
    stereo_data = np.column_stack((left_data, right_data))
    
    test_file = "test_extract.wav"
    with WavAdapter(test_file, "w") as wav:
        wav.write(stereo_data)
    
    # Extract left channel
    adapter = ChannelAdapter()
    left_file = "test_left.wav"
    adapter.extract_channel(test_file, left_file, channel=0)
    
    # Verify the output
    with WavAdapter(left_file, "r") as wav:
        left_extracted = wav.read()
        assert left_extracted.shape[1] == 1  # Mono
        assert np.allclose(left_extracted.flatten(), left_data, atol=1e-6)
    
    # Cleanup
    os.remove(test_file)
    os.remove(left_file)


def test_get_channel_layout():
    """Test detecting channel layout."""
    # Create a test WAV file (stereo)
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    test_file = "test_layout.wav"
    with WavAdapter(test_file, "w") as wav:
        wav.write(stereo_data)
    
    # Get channel layout
    adapter = ChannelAdapter()
    channels, layout = adapter.get_channel_layout(test_file)
    
    assert channels == 2
    assert layout == "stereo"
    
    # Cleanup
    os.remove(test_file)


if __name__ == "__main__":
    test_convert_channels()
    test_extract_channel()
    test_get_channel_layout()
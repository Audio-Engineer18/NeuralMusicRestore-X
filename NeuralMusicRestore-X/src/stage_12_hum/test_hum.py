"""
Test Stage 12: Hum Detection and Notch Filtering
"""

import numpy as np
import pytest
from adapter import HumAdapter


def test_detect_hum():
    """Test hum detection."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Generate a test signal with 50Hz hum
    hum = np.sin(2 * np.pi * 50 * t) * 0.5
    audio = hum + np.random.normal(0, 0.1, len(t))  # Add noise
    stereo_audio = np.column_stack((audio, audio))
    
    # Detect hum
    adapter = HumAdapter(samplerate, notch_freq=50.0)
    assert adapter.detect_hum(stereo_audio, threshold=0.1)


def test_remove_hum():
    """Test hum removal."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Generate a test signal with 60Hz hum
    hum = np.sin(2 * np.pi * 60 * t) * 0.5
    audio = hum + np.sin(2 * np.pi * 1000 * t)  # Add 1kHz tone
    stereo_audio = np.column_stack((audio, audio))
    
    # Remove hum
    adapter = HumAdapter(samplerate, notch_freq=60.0)
    filtered_audio = adapter.remove_hum(stereo_audio)
    
    # Verify that the 60Hz component is attenuated
    fft_original = np.abs(np.fft.fft(audio))
    fft_filtered = np.abs(np.fft.fft(filtered_audio[:, 0]))
    
    hum_bin = int(60 * len(t) / samplerate)
    assert fft_filtered[hum_bin] < fft_original[hum_bin] * 0.1


def test_no_hum_detection():
    """Test that hum is not detected in clean audio."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Generate a clean test signal (1kHz tone)
    audio = np.sin(2 * np.pi * 1000 * t)
    stereo_audio = np.column_stack((audio, audio))
    
    # Detect hum (should not detect)
    adapter = HumAdapter(samplerate, notch_freq=50.0)
    assert not adapter.detect_hum(stereo_audio, threshold=0.1)


if __name__ == "__main__":
    test_detect_hum()
    test_remove_hum()
    test_no_hum_detection()
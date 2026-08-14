"""
Test Stage 23: Music Restoration
"""

import numpy as np
import pytest
import torch
from adapter import MusicRestorationAdapter


def test_music_restoration():
    """Test music restoration on a degraded audio sample."""
    # Generate a test signal (1kHz sine wave with noise and clipping)
    samplerate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t) * 0.8
    noise = np.random.normal(0, 0.1, len(t))
    clipped = np.clip(signal + noise, -0.5, 0.5)  # Simulate clipping
    stereo_audio = np.column_stack((clipped, clipped))
    
    # Apply music restoration
    adapter = MusicRestorationAdapter()
    restored_audio = adapter.process(stereo_audio, samplerate=samplerate)
    
    # Verify output shape
    assert restored_audio.shape == stereo_audio.shape
    
    # Verify restoration (noise and clipping should be reduced)
    noise_reduction = np.mean(np.abs(clipped)) - np.mean(np.abs(restored_audio[:, 0]))
    assert noise_reduction > 0.05  # Noise should be reduced
    assert np.max(np.abs(restored_audio)) <= 0.9  # Clipping should be reduced


def test_music_restoration_high_freq():
    """Test music restoration on high-frequency content."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 8000 * t) * 0.5
    stereo_audio = np.column_stack((signal, signal))
    
    # Apply music restoration
    adapter = MusicRestorationAdapter()
    restored_audio = adapter.process(stereo_audio, samplerate=samplerate)
    
    # Verify output shape
    assert restored_audio.shape == stereo_audio.shape
    
    # Verify high-frequency preservation
    fft_original = np.abs(np.fft.fft(signal))
    fft_restored = np.abs(np.fft.fft(restored_audio[:, 0]))
    high_freq_bin = int(8000 * len(t) / samplerate)
    assert fft_restored[high_freq_bin] > fft_original[high_freq_bin] * 0.8  # HF content preserved


if __name__ == "__main__":
    test_music_restoration()
    test_music_restoration_high_freq()
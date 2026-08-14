"""
Test Stage 24: Vocal Restoration
"""

import numpy as np
import pytest
import torch
from adapter import VocalRestorationAdapter


def test_vocal_restoration():
    """Test vocal restoration on a degraded vocal sample."""
    # Generate a test signal (1kHz sine wave with noise)
    samplerate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    vocal = np.sin(2 * np.pi * 1000 * t) * 0.5
    noise = np.random.normal(0, 0.2, len(t))
    degraded_vocal = vocal + noise
    stereo_audio = np.column_stack((degraded_vocal, degraded_vocal))
    
    # Apply vocal restoration
    adapter = VocalRestorationAdapter()
    restored_audio = adapter.process(stereo_audio, samplerate=samplerate)
    
    # Verify output shape
    assert restored_audio.shape == stereo_audio.shape
    
    # Verify restoration (noise should be reduced)
    noise_reduction = np.mean(np.abs(degraded_vocal)) - np.mean(np.abs(restored_audio[:, 0]))
    assert noise_reduction > 0.1  # Noise should be significantly reduced


def test_vocal_restoration_high_freq():
    """Test vocal restoration on high-frequency content."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    vocal = np.sin(2 * np.pi * 4000 * t) * 0.5  # High-frequency vocal
    stereo_audio = np.column_stack((vocal, vocal))
    
    # Apply vocal restoration
    adapter = VocalRestorationAdapter()
    restored_audio = adapter.process(stereo_audio, samplerate=samplerate)
    
    # Verify output shape
    assert restored_audio.shape == stereo_audio.shape
    
    # Verify high-frequency preservation
    fft_original = np.abs(np.fft.fft(vocal))
    fft_restored = np.abs(np.fft.fft(restored_audio[:, 0]))
    high_freq_bin = int(4000 * len(t) / samplerate)
    assert fft_restored[high_freq_bin] > fft_original[high_freq_bin] * 0.9  # HF content preserved


if __name__ == "__main__":
    test_vocal_restoration()
    test_vocal_restoration_high_freq()
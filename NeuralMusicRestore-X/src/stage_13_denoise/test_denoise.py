"""
Test Stage 13: AI-Powered Denoising
"""

import numpy as np
import pytest
import torch
from adapter import DenoiseAdapter


def test_denoise():
    """Test AI denoising."""
    # Generate a test signal (1kHz sine wave + noise)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t)
    noise = np.random.normal(0, 0.3, len(t))
    audio = signal + noise
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply denoising
    adapter = DenoiseAdapter()
    denoised_audio = adapter.process(stereo_audio, samplerate=samplerate)
    
    # Verify that noise is reduced (simple check)
    noise_reduction = np.mean(np.abs(audio)) - np.mean(np.abs(denoised_audio[:, 0]))
    assert noise_reduction > 0.05  # Noise should be reduced


def test_denoise_different_samplerate():
    """Test denoising with a non-standard sample rate."""
    samplerate = 48000
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t)
    noise = np.random.normal(0, 0.3, len(t))
    audio = signal + noise
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply denoising
    adapter = DenoiseAdapter()
    denoised_audio = adapter.process(stereo_audio, samplerate=samplerate)
    
    # Verify output shape
    assert denoised_audio.shape == stereo_audio.shape


if __name__ == "__main__":
    test_denoise()
    test_denoise_different_samplerate()
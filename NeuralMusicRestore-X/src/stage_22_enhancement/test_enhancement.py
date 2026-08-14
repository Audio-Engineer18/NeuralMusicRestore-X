"""
Test Stage 22: Audio Enhancement
"""

import numpy as np
import pytest
import torch
from adapter import EnhancementAdapter


def test_enhancement():
    """Test audio enhancement on a vocal sample."""
    # Generate a test signal (1kHz sine wave + noise)
    samplerate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t) * 0.5
    noise = np.random.normal(0, 0.1, len(t))
    audio = signal + noise
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply enhancement
    adapter = EnhancementAdapter()
    enhanced_audio = adapter.process(stereo_audio, samplerate=samplerate, denoise=True, enhance=True)
    
    # Verify output shape
    assert enhanced_audio.shape == stereo_audio.shape
    
    # Verify noise reduction (simple check)
    noise_reduction = np.mean(np.abs(audio)) - np.mean(np.abs(enhanced_audio[:, 0]))
    assert noise_reduction > 0.05  # Noise should be reduced


def test_enhancement_no_denoise():
    """Test enhancement without denoising."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t) * 0.5
    stereo_audio = np.column_stack((signal, signal))
    
    # Apply enhancement without denoising
    adapter = EnhancementAdapter()
    enhanced_audio = adapter.process(stereo_audio, samplerate=samplerate, denoise=False, enhance=True)
    
    # Verify output shape
    assert enhanced_audio.shape == stereo_audio.shape
    
    # Verify enhancement (signal should be clearer)
    correlation = np.corrcoef(signal, enhanced_audio[:, 0])[0, 1]
    assert correlation > 0.9  # High correlation (enhanced but not distorted)


if __name__ == "__main__":
    test_enhancement()
    test_enhancement_no_denoise()
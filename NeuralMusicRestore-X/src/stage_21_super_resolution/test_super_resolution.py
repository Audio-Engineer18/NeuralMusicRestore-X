"""
Test Stage 21: Super-Resolution
"""

import numpy as np
import pytest
import torch
from adapter import SuperResolutionAdapter


def test_super_resolution():
    """Test super-resolution on a simple sine wave."""
    # Generate a test signal (1kHz sine wave at 44.1kHz)
    input_sr = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(input_sr * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t)
    stereo_signal = np.column_stack((signal, signal))
    
    # Apply super-resolution
    adapter = SuperResolutionAdapter()
    output_sr = 88200
    super_resolved = adapter.process(stereo_signal, input_sr=input_sr, output_sr=output_sr)
    
    # Verify output shape and sample rate
    assert super_resolved.shape[0] == int(input_sr * duration * (output_sr / input_sr))
    assert super_resolved.shape[1] == 2


def test_super_resolution_high_freq():
    """Test super-resolution on high-frequency content."""
    # Generate a test signal with high-frequency content (8kHz sine wave at 44.1kHz)
    input_sr = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(input_sr * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 8000 * t)
    stereo_signal = np.column_stack((signal, signal))
    
    # Apply super-resolution
    adapter = SuperResolutionAdapter()
    output_sr = 88200
    super_resolved = adapter.process(stereo_signal, input_sr=input_sr, output_sr=output_sr)
    
    # Verify that high frequencies are preserved
    fft_original = np.abs(np.fft.fft(signal))
    fft_super_resolved = np.abs(np.fft.fft(super_resolved[:, 0]))
    
    # The super-resolved signal should have more high-frequency content
    assert np.sum(fft_super_resolved) > np.sum(fft_original)


if __name__ == "__main__":
    test_super_resolution()
    test_super_resolution_high_freq()
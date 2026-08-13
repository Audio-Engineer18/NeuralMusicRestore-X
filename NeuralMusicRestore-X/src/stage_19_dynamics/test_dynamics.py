"""
Test Stage 19: Dynamics Processing
"""

import numpy as np
import pytest
from adapter import DynamicsAdapter


def test_dynamics_processing():
    """Test dynamics processing."""
    # Generate a test signal with varying dynamics
    samplerate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Low-amplitude sine wave
    low_amp = np.sin(2 * np.pi * 1000 * t) * 0.1
    # High-amplitude sine wave
    high_amp = np.sin(2 * np.pi * 1000 * t) * 0.8
    
    # Combine into a single audio signal
    audio = np.concatenate([low_amp, high_amp])
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply dynamics processing
    with DynamicsAdapter(samplerate=samplerate, channels=2) as adapter:
        processed_audio = adapter.process(stereo_audio)
    
    # Verify that dynamics are normalized (low-amplitude section is boosted)
    low_section = processed_audio[:len(low_amp), 0]
    high_section = processed_audio[len(low_amp):, 0]
    
    # Low-amplitude section should be closer to high-amplitude section
    assert np.mean(np.abs(low_section)) > np.mean(np.abs(stereo_audio[:len(low_amp), 0])) * 1.5
    assert np.max(np.abs(processed_audio)) <= 1.0  # No clipping


def test_dynamics_stereo_coupling():
    """Test dynamics processing with stereo coupling."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Left channel: low amplitude, Right channel: high amplitude
    left = np.sin(2 * np.pi * 1000 * t) * 0.1
    right = np.sin(2 * np.pi * 1000 * t) * 0.8
    stereo_audio = np.column_stack((left, right))
    
    # Apply dynamics processing with stereo coupling
    with DynamicsAdapter(samplerate=samplerate, channels=2, channels_coupling=True) as adapter:
        processed_audio = adapter.process(stereo_audio)
    
    # Both channels should have similar dynamics
    left_processed = processed_audio[:, 0]
    right_processed = processed_audio[:, 1]
    
    assert np.mean(np.abs(left_processed)) > np.mean(np.abs(left)) * 1.5
    assert np.abs(np.mean(np.abs(left_processed)) - np.mean(np.abs(right_processed))) < 0.1


if __name__ == "__main__":
    test_dynamics_processing()
    test_dynamics_stereo_coupling()
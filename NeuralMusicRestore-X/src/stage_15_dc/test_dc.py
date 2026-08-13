"""
Test Stage 15: DC Offset Removal
"""

import numpy as np
import pytest
from adapter import DcAdapter


def test_dc_removal():
    """Test DC offset removal."""
    # Generate a test signal with DC offset
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t)
    dc_offset = 0.5
    audio = signal + dc_offset
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply DC removal
    with DcAdapter() as dc_remover:
        processed_audio = dc_remover.process(stereo_audio)
    
    # Verify that DC offset is removed
    assert np.abs(np.mean(processed_audio)) < 0.01  # Near-zero mean


def test_dc_removal_multichannel():
    """Test DC offset removal for multi-channel audio."""
    # Generate a test signal with different DC offsets per channel
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t)
    dc_offset_left = 0.3
    dc_offset_right = -0.2
    left_channel = signal + dc_offset_left
    right_channel = signal + dc_offset_right
    stereo_audio = np.column_stack((left_channel, right_channel))
    
    # Apply DC removal
    with DcAdapter() as dc_remover:
        processed_audio = dc_remover.process(stereo_audio)
    
    # Verify that DC offset is removed from both channels
    assert np.abs(np.mean(processed_audio[:, 0])) < 0.01  # Left channel
    assert np.abs(np.mean(processed_audio[:, 1])) < 0.01  # Right channel


if __name__ == "__main__":
    test_dc_removal()
    test_dc_removal_multichannel()
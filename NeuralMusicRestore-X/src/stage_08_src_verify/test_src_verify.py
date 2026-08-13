"""
Test Stage 08: Sample Rate Conversion (SRC) Verification
"""

import numpy as np
import pytest
from adapter import SrcVerifyAdapter


def test_verify_src():
    """Test verifying sample rate conversion."""
    # Generate a test signal (440Hz sine wave at 44.1kHz)
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    # Resample to 48kHz using soxr
    target_samplerate = 48000
    with SrcVerifyAdapter(samplerate, target_samplerate, channels=2) as verifier:
        resampled_data = verifier.process(stereo_data)
        
        # Verify the resampled data
        assert verifier.verify_src(stereo_data, resampled_data)


def test_verify_invalid_src():
    """Test detecting invalid sample rate conversion."""
    # Generate a test signal (440Hz sine wave at 44.1kHz)
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    # Create invalid resampled data (wrong shape)
    invalid_data = np.zeros((100, 2), dtype=np.float32)
    
    # Verify the invalid data
    with SrcVerifyAdapter(samplerate, 48000, channels=2) as verifier:
        assert not verifier.verify_src(stereo_data, invalid_data)


if __name__ == "__main__":
    test_verify_src()
    test_verify_invalid_src()
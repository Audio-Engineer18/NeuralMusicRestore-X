"""
Test Stage 09: Advanced Sample Rate Conversion (SRC)
"""

import numpy as np
import pytest
from adapter import AdvancedSrcAdapter


def test_advanced_src():
    """Test advanced sample rate conversion."""
    # Generate a test signal (440Hz sine wave at 44.1kHz)
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    # Resample to 48kHz
    target_samplerate = 48000
    with AdvancedSrcAdapter(samplerate, target_samplerate, channels=2) as src:
        resampled_data = src.process(stereo_data.astype(np.float64))
    
    # Verify the output shape
    expected_samples = int(len(data) * target_samplerate / samplerate)
    assert resampled_data.shape[0] == pytest.approx(expected_samples, rel=1e-2)
    assert resampled_data.shape[1] == 2


def test_advanced_src_downsample():
    """Test downsampling (48kHz -> 44.1kHz)."""
    samplerate = 48000
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    # Resample to 44.1kHz
    target_samplerate = 44100
    with AdvancedSrcAdapter(samplerate, target_samplerate, channels=2) as src:
        resampled_data = src.process(stereo_data.astype(np.float64))
    
    # Verify the output shape
    expected_samples = int(len(data) * target_samplerate / samplerate)
    assert resampled_data.shape[0] == pytest.approx(expected_samples, rel=1e-2)
    assert resampled_data.shape[1] == 2


if __name__ == "__main__":
    test_advanced_src()
    test_advanced_src_downsample()
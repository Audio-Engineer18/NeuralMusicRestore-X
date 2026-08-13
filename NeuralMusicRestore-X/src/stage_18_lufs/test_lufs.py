"""
Test Stage 18: LUFS Loudness Metering
"""

import numpy as np
import pytest
from adapter import LufsAdapter


def test_lufs_measurement():
    """Test LUFS loudness measurement."""
    # Generate a test signal (pink noise at -23 LUFS)
    samplerate = 44100
    duration = 5.0  # Longer duration for accurate short-term measurement
    samples = int(samplerate * duration)
    
    # Pink noise (approximate -23 LUFS)
    white = np.random.normal(0, 0.1, samples)
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
    a = [1, -2.494956002, 2.017265875, -0.522189400]
    pink = np.zeros(samples)
    for i in range(samples):
        pink[i] = white[i]
        if i >= 1:
            pink[i] += a[1] * pink[i-1] + b[1] * white[i-1]
        if i >= 2:
            pink[i] += a[2] * pink[i-2] + b[2] * white[i-2]
        if i >= 3:
            pink[i] += a[3] * pink[i-3] + b[3] * white[i-3]
    
    stereo_pink = np.column_stack((pink, pink))
    
    # Measure loudness
    with LufsAdapter(samplerate=samplerate, channels=2) as adapter:
        global_lufs, momentary_lufs, shortterm_lufs = adapter.measure_loudness(stereo_pink)
    
    # Verify loudness values (approximate)
    assert global_lufs == pytest.approx(-23.0, rel=0.1)
    assert momentary_lufs == pytest.approx(-23.0, rel=0.2)
    assert shortterm_lufs == pytest.approx(-23.0, rel=0.2)


def test_lufs_silence():
    """Test LUFS measurement for silence."""
    samplerate = 44100
    duration = 1.0
    silence = np.zeros((int(samplerate * duration), 2), dtype=np.float32)
    
    # Measure loudness
    with LufsAdapter(samplerate=samplerate, channels=2) as adapter:
        global_lufs, momentary_lufs, shortterm_lufs = adapter.measure_loudness(silence)
    
    # Silence should measure as -inf LUFS
    assert global_lufs == float("-inf")
    assert momentary_lufs == float("-inf")
    assert shortterm_lufs == float("-inf")


if __name__ == "__main__":
    test_lufs_measurement()
    test_lufs_silence()
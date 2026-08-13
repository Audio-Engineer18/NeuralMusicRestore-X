"""
Test Stage 07: 64-bit Floating-Point DSP
"""

import numpy as np
import pytest
from adapter import Float64Adapter


def test_to_float64():
    """Test conversion to float64."""
    audio = np.array([1.0, 0.5, -0.5, -1.0], dtype=np.float32)
    audio_float64 = Float64Adapter.to_float64(audio)
    assert audio_float64.dtype == np.float64
    assert np.allclose(audio_float64, audio)


def test_normalize():
    """Test audio normalization."""
    audio = np.array([0.5, -0.5, 0.25, -0.25], dtype=np.float64)
    normalized = Float64Adapter.normalize(audio, target_peak=1.0)
    assert np.max(np.abs(normalized)) == 1.0


def test_apply_gain():
    """Test applying gain."""
    audio = np.array([0.5, -0.5], dtype=np.float64)
    amplified = Float64Adapter.apply_gain(audio, gain_db=6.0)  # 6 dB gain
    expected = np.array([1.0, -1.0], dtype=np.float64)
    assert np.allclose(amplified, expected)


def test_mix():
    """Test mixing two audio signals."""
    audio1 = np.array([1.0, 0.0], dtype=np.float64)
    audio2 = np.array([0.0, 1.0], dtype=np.float64)
    mixed = Float64Adapter.mix(audio1, audio2, weight1=0.5, weight2=0.5)
    expected = np.array([0.5, 0.5], dtype=np.float64)
    assert np.allclose(mixed, expected)


def test_resample():
    """Test resampling audio."""
    audio = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]], dtype=np.float64)
    resampled = Float64Adapter.resample(audio, original_rate=4, target_rate=2)
    expected = np.array([[1.0, 0.0], [-1.0, 0.0]], dtype=np.float64)
    assert np.allclose(resampled, expected)


def test_fade_in_out():
    """Test fade-in and fade-out."""
    audio = np.ones((10, 2), dtype=np.float64)
    faded = Float64Adapter.fade_in_out(audio, fade_duration=0.1, samplerate=10)
    assert faded[0, 0] == 0.0  # Fade-in start
    assert faded[-1, 0] == 0.0  # Fade-out end
    assert faded[5, 0] == 1.0  # Middle (no fade)


if __name__ == "__main__":
    test_to_float64()
    test_normalize()
    test_apply_gain()
    test_mix()
    test_resample()
    test_fade_in_out()
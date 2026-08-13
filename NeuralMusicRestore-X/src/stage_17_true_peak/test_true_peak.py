"""
Test Stage 17: True Peak Detection
"""

import numpy as np
import pytest
from adapter import TruePeakAdapter


def test_true_peak_detection():
    """Test true peak detection."""
    # Generate a test signal (sine wave at 0 dBFS)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t) * 0.99  # Near 0 dBFS
    stereo_signal = np.column_stack((signal, signal))
    
    # Detect true peak
    with TruePeakAdapter(samplerate=samplerate, channels=2) as adapter:
        global_peak, per_channel_peaks = adapter.detect_true_peak(stereo_signal)
    
    # Verify true peak is close to 0 dBFS
    assert global_peak > 0.98  # Slightly below 0 dBFS due to oversampling
    assert np.all(per_channel_peaks > 0.98)


def test_true_peak_clipping():
    """Test true peak detection for clipped audio."""
    # Generate a clipped test signal
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t) * 1.1  # Clipped
    stereo_signal = np.column_stack((signal, signal))
    
    # Detect true peak
    with TruePeakAdapter(samplerate=samplerate, channels=2) as adapter:
        global_peak, per_channel_peaks = adapter.detect_true_peak(stereo_signal)
    
    # Verify true peak exceeds 0 dBFS
    assert global_peak > 1.0  # True peak should detect clipping


if __name__ == "__main__":
    test_true_peak_detection()
    test_true_peak_clipping()
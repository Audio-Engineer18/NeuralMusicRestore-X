"""
Test Stage 11: Linear FIR Filtering
"""

import numpy as np
import pytest
from adapter import LinearFirAdapter


def test_linear_fir_filter():
    """Test linear FIR filtering."""
    # Generate a test signal (1kHz sine wave + 5kHz sine wave)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    low_freq = np.sin(2 * np.pi * 1000 * t)  # 1kHz
    high_freq = np.sin(2 * np.pi * 5000 * t)  # 5kHz
    audio = low_freq + high_freq
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply FIR filter (cutoff at 2kHz)
    adapter = LinearFirAdapter(samplerate, cutoff=2000.0, numtaps=511)
    filtered_audio = adapter.process(stereo_audio)
    
    # Verify that the 5kHz component is attenuated
    fft_original = np.abs(np.fft.fft(audio))
    fft_filtered = np.abs(np.fft.fft(filtered_audio[:, 0]))
    
    # The 5kHz bin should be significantly smaller
    high_freq_bin = int(5000 * len(t) / samplerate)
    assert fft_filtered[high_freq_bin] < fft_original[high_freq_bin] * 0.5


def test_zero_phase_fir():
    """Test zero-phase FIR filtering."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    audio = np.sin(2 * np.pi * 1000 * t)  # 1kHz sine wave
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply zero-phase FIR filter (cutoff at 2kHz)
    adapter = LinearFirAdapter(samplerate, cutoff=2000.0, numtaps=511)
    filtered_audio = adapter.process_zero_phase(stereo_audio)
    
    # The filtered audio should be nearly identical to the original (no phase distortion)
    correlation = np.corrcoef(audio, filtered_audio[:, 0])[0, 1]
    assert correlation > 0.99


if __name__ == "__main__":
    test_linear_fir_filter()
    test_zero_phase_fir()
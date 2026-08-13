"""
Test Stage 10: Subsonic Filtering
"""

import numpy as np
import pytest
from adapter import SubsonicAdapter


def test_subsonic_filter():
    """Test subsonic filtering."""
    # Generate a test signal (20Hz sine wave + 1kHz sine wave)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    subsonic = np.sin(2 * np.pi * 20 * t)  # 20Hz (subsonic)
    audible = np.sin(2 * np.pi * 1000 * t)  # 1kHz (audible)
    audio = subsonic + audible
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply subsonic filter (cutoff at 30Hz)
    with SubsonicAdapter(samplerate, cutoff=30.0) as filter:
        filtered_audio = filter.process(stereo_audio)
    
    # Verify that the 20Hz component is attenuated
    subsonic_original = np.abs(np.fft.fft(audio)[:100])
    subsonic_filtered = np.abs(np.fft.fft(filtered_audio[:, 0])[:100])
    
    # The filtered subsonic component should be significantly smaller
    assert np.mean(subsonic_filtered) < np.mean(subsonic_original) * 0.5


def test_zero_phase():
    """Test that the filter is zero-phase (no phase distortion)."""
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    audio = np.sin(2 * np.pi * 1000 * t)  # 1kHz sine wave
    stereo_audio = np.column_stack((audio, audio))
    
    # Apply subsonic filter (cutoff at 30Hz, should not affect 1kHz)
    with SubsonicAdapter(samplerate, cutoff=30.0) as filter:
        filtered_audio = filter.process(stereo_audio)
    
    # The filtered audio should be nearly identical to the original
    correlation = np.corrcoef(audio, filtered_audio[:, 0])[0, 1]
    assert correlation > 0.99  # High correlation (no phase distortion)


if __name__ == "__main__":
    test_subsonic_filter()
    test_zero_phase()
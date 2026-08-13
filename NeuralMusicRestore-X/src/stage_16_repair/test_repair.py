"""
Test Stage 16: Click/Clip Repair
"""

import numpy as np
import os
import tempfile
import pytest
from adapter import RepairAdapter
from stage_01_wav_pcm.adapter import WavAdapter


def test_repair_clicks():
    """Test click repair."""
    # Generate a test signal with artificial clicks
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t)
    
    # Add clicks (impulses)
    click_positions = [1000, 5000, 10000]
    signal[click_positions] = 1.0  # Large spikes
    stereo_signal = np.column_stack((signal, signal))
    
    # Write to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_input:
        input_file = tmp_input.name
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_output:
        output_file = tmp_output.name
    
    with WavAdapter(input_file, "w") as wav:
        wav.write(stereo_signal)
    
    # Repair clicks
    adapter = RepairAdapter()
    adapter.repair_clicks(input_file, output_file)
    
    # Verify repair
    with WavAdapter(output_file, "r") as wav:
        repaired_signal = wav.read()
    
    # Clicks should be reduced
    assert np.max(np.abs(repaired_signal)) < 0.9  # No large spikes
    
    # Cleanup
    os.remove(input_file)
    os.remove(output_file)


def test_repair_clipping():
    """Test clipping repair."""
    # Generate a test signal with clipping
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * 1000 * t) * 1.2  # Clipped signal
    stereo_signal = np.column_stack((signal, signal))
    
    # Write to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_input:
        input_file = tmp_input.name
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_output:
        output_file = tmp_output.name
    
    with WavAdapter(input_file, "w") as wav:
        wav.write(stereo_signal)
    
    # Repair clipping
    adapter = RepairAdapter()
    adapter.repair_clipping(input_file, output_file)
    
    # Verify repair
    with WavAdapter(output_file, "r") as wav:
        repaired_signal = wav.read()
    
    # Clipping should be reduced
    assert np.max(np.abs(repaired_signal)) <= 1.0  # No clipping
    
    # Cleanup
    os.remove(input_file)
    os.remove(output_file)


if __name__ == "__main__":
    test_repair_clicks()
    test_repair_clipping()
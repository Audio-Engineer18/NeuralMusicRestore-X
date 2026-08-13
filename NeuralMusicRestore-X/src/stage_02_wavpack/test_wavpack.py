"""
Test Stage 02: WavPack Adapter
"""

import numpy as np
import os
import pytest
from adapter import WavPackAdapter
from stage_01_wav_pcm.adapter import WavAdapter


def test_decode_wavpack():
    """Test decoding a WavPack file to WAV."""
    # Create a test WAV file
    samplerate = 44100
    duration = 1.0  # seconds
    frequency = 440.0  # Hz (A4 note)
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))  # Stereo
    
    # Write the WAV file
    test_wav = "test.wav"
    with WavAdapter(test_wav, "w") as wav:
        wav.write(stereo_data)
    
    # Encode to WavPack (using wavpack CLI)
    test_wv = "test.wv"
    subprocess.run(["wavpack", test_wav, "-o", test_wv], check=True)
    
    # Decode WavPack back to WAV
    adapter = WavPackAdapter()
    decoded_wav = adapter.decode_to_wav(test_wv)
    
    # Verify the decoded WAV
    with WavAdapter(decoded_wav, "r") as wav:
        read_data = wav.read()
        assert read_data.shape == stereo_data.shape
        assert wav.samplerate == samplerate
        assert wav.channels == 2
    
    # Cleanup
    os.remove(test_wav)
    os.remove(test_wv)
    os.remove(decoded_wav)


def test_get_audio_info():
    """Test extracting metadata from a WavPack file."""
    # Create a test WAV file
    test_wav = "test_info.wav"
    samplerate = 48000
    duration = 2.0
    frequency = 500.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    with WavAdapter(test_wav, "w") as wav:
        wav.write(stereo_data)
    
    # Encode to WavPack
    test_wv = "test_info.wv"
    subprocess.run(["wavpack", test_wav, "-o", test_wv], check=True)
    
    # Extract metadata
    adapter = WavPackAdapter()
    info = adapter.get_audio_info(test_wv)
    
    assert info["samplerate"] == samplerate
    assert info["channels"] == 2
    assert info["duration"] == pytest.approx(duration, rel=1e-2)
    
    # Cleanup
    os.remove(test_wav)
    os.remove(test_wv)


if __name__ == "__main__":
    test_decode_wavpack()
    test_get_audio_info()
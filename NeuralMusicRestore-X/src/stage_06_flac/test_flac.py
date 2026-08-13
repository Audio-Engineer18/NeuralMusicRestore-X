"""
Test Stage 06: FLAC Archive + Verification
"""

import numpy as np
import os
import pytest
from adapter import FLACAdapter
from stage_01_wav_pcm.adapter import WavAdapter


def test_encode_decode_flac():
    """Test encoding a WAV file to FLAC and decoding back to WAV."""
    # Create a test WAV file
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    test_wav = "test_flac.wav"
    with WavAdapter(test_wav, "w") as wav:
        wav.write(stereo_data)
    
    # Encode to FLAC
    adapter = FLACAdapter()
    flac_file = "test_flac.flac"
    adapter.encode_to_flac(test_wav, flac_file, samplerate=samplerate, channels=2)
    
    # Verify FLAC
    assert adapter.verify_flac(flac_file)
    
    # Decode back to WAV
    decoded_wav = "test_decoded.wav"
    adapter.decode_to_wav(flac_file, decoded_wav)
    
    # Verify the decoded WAV
    with WavAdapter(decoded_wav, "r") as wav:
        decoded_data = wav.read()
        assert decoded_data.shape == stereo_data.shape
        assert np.allclose(decoded_data, stereo_data, atol=1e-3)
    
    # Cleanup
    os.remove(test_wav)
    os.remove(flac_file)
    os.remove(decoded_wav)


def test_verify_corrupt_flac():
    """Test verifying a corrupt FLAC file."""
    # Create a valid FLAC file
    samplerate = 44100
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    stereo_data = np.column_stack((data, data))
    
    test_wav = "test_corrupt.wav"
    with WavAdapter(test_wav, "w") as wav:
        wav.write(stereo_data)
    
    adapter = FLACAdapter()
    flac_file = "test_corrupt.flac"
    adapter.encode_to_flac(test_wav, flac_file, samplerate=samplerate, channels=2)
    
    # Corrupt the FLAC file
    with open(flac_file, "r+b") as f:
        f.seek(100)
        f.write(b"corrupt")
    
    # Verify the corrupt file
    assert not adapter.verify_flac(flac_file)
    
    # Cleanup
    os.remove(test_wav)
    os.remove(flac_file)


if __name__ == "__main__":
    test_encode_decode_flac()
    test_verify_corrupt_flac()
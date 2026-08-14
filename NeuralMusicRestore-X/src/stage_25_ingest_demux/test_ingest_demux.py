"""
Test Stage 25: Ingest/Demux
"""

import numpy as np
import os
import tempfile
import pytest
from adapter import IngestDemuxAdapter


def test_list_streams():
    """Test listing audio streams in a multimedia file."""
    # Create a test multimedia file (WAV with 2 streams)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Stream 0: 1kHz sine wave
    stream0 = np.sin(2 * np.pi * 1000 * t)
    # Stream 1: 2kHz sine wave
    stream1 = np.sin(2 * np.pi * 2000 * t)
    
    # Write to a temporary WAV file (simulating a multimedia file)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        input_file = tmp_file.name
    
    from stage_01_wav_pcm.adapter import WavAdapter
    with WavAdapter(input_file, "w") as wav:
        wav.write(np.column_stack((stream0, stream1)))
    
    # List streams
    adapter = IngestDemuxAdapter()
    streams = adapter.list_streams(input_file)
    
    # Verify stream info
    assert len(streams) == 1  # WAV files typically have 1 stream with 2 channels
    assert streams[0]["sample_rate"] == samplerate
    assert streams[0]["channels"] == "stereo"
    
    # Cleanup
    os.remove(input_file)


def test_extract_stream():
    """Test extracting an audio stream to a file."""
    # Create a test multimedia file (WAV with 2 channels)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Channel 0: 1kHz sine wave
    channel0 = np.sin(2 * np.pi * 1000 * t)
    # Channel 1: 2kHz sine wave
    channel1 = np.sin(2 * np.pi * 2000 * t)
    
    # Write to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_input:
        input_file = tmp_input.name
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_output:
        output_file = tmp_output.name
    
    from stage_01_wav_pcm.adapter import WavAdapter
    with WavAdapter(input_file, "w") as wav:
        wav.write(np.column_stack((channel0, channel1)))
    
    # Extract the first "stream" (channel)
    adapter = IngestDemuxAdapter()
    adapter.extract_stream(input_file, output_file, stream_index=0)
    
    # Verify the extracted file
    with WavAdapter(output_file, "r") as wav:
        extracted_audio = wav.read()
        assert extracted_audio.shape[0] == len(channel0)
        assert np.allclose(extracted_audio[:, 0], channel0, atol=1e-6)
    
    # Cleanup
    os.remove(input_file)
    os.remove(output_file)


def test_extract_to_numpy():
    """Test extracting an audio stream to a numpy array."""
    # Create a test multimedia file (WAV with 2 channels)
    samplerate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    
    # Channel 0: 1kHz sine wave
    channel0 = np.sin(2 * np.pi * 1000 * t)
    # Channel 1: 2kHz sine wave
    channel1 = np.sin(2 * np.pi * 2000 * t)
    
    # Write to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        input_file = tmp_file.name
    
    from stage_01_wav_pcm.adapter import WavAdapter
    with WavAdapter(input_file, "w") as wav:
        wav.write(np.column_stack((channel0, channel1)))
    
    # Extract to numpy array
    adapter = IngestDemuxAdapter()
    audio, extracted_sr = adapter.extract_to_numpy(input_file, stream_index=0)
    
    # Verify the extracted audio
    assert extracted_sr == samplerate
    assert audio.shape[0] == len(channel0)
    assert np.allclose(audio[:, 0], channel0, atol=1e-6)
    
    # Cleanup
    os.remove(input_file)


if __name__ == "__main__":
    test_list_streams()
    test_extract_stream()
    test_extract_to_numpy()
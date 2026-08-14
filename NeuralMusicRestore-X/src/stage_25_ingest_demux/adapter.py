"""
Stage 25: Ingest/Demux
----------------------
Uses FFmpeg to extract audio streams from multimedia files.

Dependencies:
- FFmpeg (https://github.com/FFmpeg/FFmpeg)
"""

import subprocess
import numpy as np
import os
import tempfile
from typing import Optional, Tuple, List


class IngestDemuxAdapter:
    """Python adapter for audio stream extraction using FFmpeg."""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg_path = ffmpeg_path
        self._validate_ffmpeg()

    def _validate_ffmpeg(self):
        """Check if FFmpeg is available."""
        try:
            subprocess.run(
                [self.ffmpeg_path, "-version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ImportError(
                "FFmpeg not found. Install it from: https://github.com/FFmpeg/FFmpeg"
            )

    def list_streams(self, input_file: str) -> List[dict]:
        """List all audio streams in the input file.
        
        Args:
            input_file: Path to the input multimedia file.
            
        Returns:
            List of dictionaries containing stream info (index, codec, channels, sample_rate).
        """
        result = subprocess.run(
            [
                self.ffmpeg_path,
                "-i", input_file,
                "-hide_banner",
                "-f", "null",
                "-",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        streams = []
        for line in result.stderr.splitlines():
            if "Stream #" in line and "Audio:" in line:
                parts = line.split()
                stream_info = {
                    "index": int(parts[1].split(":")[1].rstrip(",")),
                    "codec": parts[4].rstrip(","),
                    "sample_rate": int(parts[5].rstrip("Hz,")),
                    "channels": parts[7].rstrip(","),
                }
                streams.append(stream_info)
        
        return streams

    def extract_stream(
        self,
        input_file: str,
        output_file: str,
        stream_index: int = 0,
        output_format: str = "wav",
    ) -> str:
        """Extract an audio stream from the input file.
        
        Args:
            input_file: Path to the input multimedia file.
            output_file: Path to the output audio file.
            stream_index: Index of the audio stream to extract.
            output_format: Output format (e.g., "wav", "flac").
            
        Returns:
            Path to the extracted output file.
        """
        subprocess.run(
            [
                self.ffmpeg_path,
                "-i", input_file,
                "-map", f"0:{stream_index}",
                "-c:a", "copy",
                "-y",  # Overwrite output file if it exists
                output_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        return output_file

    def extract_to_numpy(
        self,
        input_file: str,
        stream_index: int = 0,
        samplerate: Optional[int] = None,
    ) -> Tuple[np.ndarray, int]:
        """Extract an audio stream directly to a numpy array.
        
        Args:
            input_file: Path to the input multimedia file.
            stream_index: Index of the audio stream to extract.
            samplerate: Target sample rate (resamples if provided).
            
        Returns:
            Tuple of (audio_array, sample_rate).
        """
        # Create a temporary output file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_file = tmp_file.name
        
        # Extract the stream
        self.extract_stream(input_file, output_file, stream_index)
        
        # Read the audio file
        from stage_01_wav_pcm.adapter import WavAdapter
        with WavAdapter(output_file, "r") as wav:
            audio = wav.read()
            original_samplerate = wav.samplerate
        
        # Resample if needed
        if samplerate is not None and samplerate != original_samplerate:
            from stage_04_vhq_src.adapter import VHQSrcAdapter
            with VHQSrcAdapter(original_samplerate, samplerate, channels=audio.shape[1]) as src:
                audio = src.process(audio)
        
        # Cleanup
        os.remove(output_file)
        
        return audio, original_samplerate if samplerate is None else samplerate
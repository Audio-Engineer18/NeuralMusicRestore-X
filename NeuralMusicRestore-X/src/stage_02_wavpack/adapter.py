"""
Stage 02: WavPack Adapter
-----------------------
Uses `wvunpack` to decode WavPack (.wv) files into WAV/PCM.

Dependencies:
- WavPack (https://github.com/dbry/WavPack)
"""

import subprocess
import numpy as np
import os
import tempfile
from typing import Optional


class WavPackAdapter:
    """Python adapter for WavPack (wvunpack)."""

    def __init__(self, wavpack_path: str = "wvunpack"):
        self.wavpack_path = wavpack_path
        self._validate_wavpack()

    def _validate_wavpack(self):
        """Check if wvunpack is available."""
        try:
            subprocess.run(
                [self.wavpack_path, "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ImportError(
                "wvunpack not found. Install WavPack from: https://github.com/dbry/WavPack"
            )

    def decode_to_wav(self, wv_file: str, wav_file: Optional[str] = None) -> str:
        """Decode a WavPack file to WAV/PCM.
        
        Args:
            wv_file: Path to the input WavPack file.
            wav_file: Path to the output WAV file. If None, a temporary file is used.
            
        Returns:
            Path to the decoded WAV file.
        """
        if wav_file is None:
            _, wav_file = tempfile.mkstemp(suffix=".wav")
        
        subprocess.run(
            [self.wavpack_path, wv_file, wav_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return wav_file

    def get_audio_info(self, wv_file: str) -> dict:
        """Extract audio metadata from a WavPack file.
        
        Args:
            wv_file: Path to the input WavPack file.
            
        Returns:
            Dictionary containing:
            - samplerate: Sample rate (Hz).
            - channels: Number of channels.
            - duration: Duration in seconds.
            - bits_per_sample: Bit depth.
        """
        result = subprocess.run(
            [self.wavpack_path, "-s", wv_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        info = {}
        for line in result.stdout.splitlines():
            if "samplerate" in line.lower():
                info["samplerate"] = int(line.split()[-1])
            elif "channels" in line.lower():
                info["channels"] = int(line.split()[-1])
            elif "duration" in line.lower():
                time_str = line.split()[-1]
                minutes, seconds = map(float, time_str.split(":"))
                info["duration"] = minutes * 60 + seconds
            elif "bits per sample" in line.lower():
                info["bits_per_sample"] = int(line.split()[-1])
        
        return info
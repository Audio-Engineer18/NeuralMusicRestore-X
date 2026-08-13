"""
Stage 20: Silence Detection and Trimming
--------------------------------------
Uses silan (https://github.com/x42/silan) for boundary analysis and silence trimming.

Dependencies:
- silan (https://github.com/x42/silan)
"""

import subprocess
import numpy as np
import os
import tempfile
from typing import Optional, Tuple


class SilenceAdapter:
    """Python adapter for silence detection and trimming using silan."""

    def __init__(self, silan_path: str = "silan"):
        self.silan_path = silan_path
        self._validate_silan()

    def _validate_silan(self):
        """Check if silan is available."""
        try:
            subprocess.run(
                [self.silan_path, "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ImportError(
                "silan not found. Install it from: https://github.com/x42/silan"
            )

    def detect_silence(
        self,
        input_file: str,
        threshold: float = -60.0,
        duration: float = 0.1,
    ) -> Tuple[float, float]:
        """Detect silence boundaries in the audio file.
        
        Args:
            input_file: Path to the input audio file.
            threshold: Silence threshold in dB (default: -60 dB).
            duration: Minimum silence duration in seconds (default: 0.1).
            
        Returns:
            Tuple of (start_time, end_time) in seconds.
        """
        result = subprocess.run(
            [
                self.silan_path,
                "-t", str(threshold),
                "-d", str(duration),
                input_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        # Parse silan output
        output = result.stdout.strip()
        if not output:
            return 0.0, float("inf")  # No silence detected
        
        # Example output: "0.000 1.234" (start and end times)
        start, end = map(float, output.split())
        return start, end

    def trim_silence(
        self,
        input_file: str,
        output_file: str,
        threshold: float = -60.0,
        duration: float = 0.1,
    ) -> str:
        """Trim silence from the audio file.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output audio file.
            threshold: Silence threshold in dB (default: -60 dB).
            duration: Minimum silence duration in seconds (default: 0.1).
            
        Returns:
            Path to the trimmed output file.
        """
        start, end = self.detect_silence(input_file, threshold, duration)
        
        # Use FFmpeg to trim the audio
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_file,
                "-ss", str(start),
                "-to", str(end),
                "-c", "copy",
                "-y",  # Overwrite output file if it exists
                output_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        return output_file

    def process(self, audio: np.ndarray, samplerate: int = 44100) -> np.ndarray:
        """Trim silence from a numpy array (in-memory).
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            samplerate: Sample rate of the input audio.
            
        Returns:
            Trimmed audio as a numpy float32 array.
        """
        # Write audio to a temporary WAV file
        from stage_01_wav_pcm.adapter import WavAdapter
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_input:
            input_file = tmp_input.name
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_output:
            output_file = tmp_output.name
        
        # Write input audio
        with WavAdapter(input_file, "w") as wav:
            wav.write(audio)
        
        # Trim silence
        self.trim_silence(input_file, output_file)
        
        # Read trimmed audio
        with WavAdapter(output_file, "r") as wav:
            trimmed_audio = wav.read()
        
        # Cleanup
        os.remove(input_file)
        os.remove(output_file)
        
        return trimmed_audio
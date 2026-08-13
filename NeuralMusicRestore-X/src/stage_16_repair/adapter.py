"""
Stage 16: Click/Clip Repair
--------------------------
Uses FFmpeg to repair clicks and clipping in audio.

Dependencies:
- FFmpeg (https://github.com/FFmpeg/FFmpeg)
"""

import subprocess
import numpy as np
import os
import tempfile
from typing import Optional


class RepairAdapter:
    """Python adapter for click/clip repair using FFmpeg."""

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

    def repair_clicks(self, input_file: str, output_file: str) -> str:
        """Repair clicks in the audio using FFmpeg's arls filter.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output audio file.
            
        Returns:
            Path to the repaired output file.
        """
        subprocess.run(
            [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "arls=n=5:r=0.01:m=0.5",  # Adaptive repair filter
                "-y",  # Overwrite output file if it exists
                output_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output_file

    def repair_clipping(self, input_file: str, output_file: str, threshold: float = 0.95) -> str:
        """Repair clipping in the audio using FFmpeg's loudnorm filter.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output audio file.
            threshold: Clipping threshold (default: 0.95).
            
        Returns:
            Path to the repaired output file.
        """
        subprocess.run(
            [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", f"loudnorm=I=-16:LRA=11:TP={threshold}",  # Loudness normalization
                "-y",  # Overwrite output file if it exists
                output_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output_file

    def process(self, audio: np.ndarray, samplerate: int = 44100) -> np.ndarray:
        """Repair clicks/clipping in a numpy array (in-memory).
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            samplerate: Sample rate of the input audio.
            
        Returns:
            Repaired audio as a numpy float32 array.
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
        
        # Repair clicks and clipping
        self.repair_clicks(input_file, output_file)
        self.repair_clipping(output_file, output_file)
        
        # Read repaired audio
        with WavAdapter(output_file, "r") as wav:
            repaired_audio = wav.read()
        
        # Cleanup
        os.remove(input_file)
        os.remove(output_file)
        
        return repaired_audio
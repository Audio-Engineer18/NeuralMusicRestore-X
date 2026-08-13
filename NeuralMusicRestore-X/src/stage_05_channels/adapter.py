"""
Stage 05: Channel Layout Engine
--------------------------------
Uses FFmpeg to manipulate audio channel layouts (e.g., stereo to 5.1).

Dependencies:
- FFmpeg (https://github.com/FFmpeg/FFmpeg)
"""

import subprocess
import numpy as np
import os
import tempfile
from typing import Optional, Tuple


class ChannelAdapter:
    """Python adapter for audio channel layout manipulation using FFmpeg."""

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

    def convert_channels(
        self,
        input_file: str,
        output_file: str,
        output_channels: int = 2,
        output_layout: str = "stereo",
    ) -> str:
        """Convert audio to a target channel layout.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output audio file.
            output_channels: Number of output channels (e.g., 2 for stereo).
            output_layout: Output channel layout (e.g., "stereo", "5.1", "7.1").
            
        Returns:
            Path to the output file.
        """
        # FFmpeg channel layout mapping
        layout_map = {
            "mono": "mono",
            "stereo": "stereo",
            "5.1": "5.1",
            "7.1": "7.1",
        }
        
        if output_layout not in layout_map:
            raise ValueError(f"Unsupported channel layout: {output_layout}")
        
        subprocess.run(
            [
                self.ffmpeg_path,
                "-i", input_file,
                "-ac", str(output_channels),
                "-channel_layout", layout_map[output_layout],
                "-y",  # Overwrite output file if it exists
                output_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        return output_file

    def extract_channel(
        self,
        input_file: str,
        output_file: str,
        channel: int = 0,
    ) -> str:
        """Extract a single channel from the input audio.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output audio file.
            channel: Index of the channel to extract (0-based).
            
        Returns:
            Path to the output file.
        """
        subprocess.run(
            [
                self.ffmpeg_path,
                "-i", input_file,
                "-map_channel", f"0.0.{channel}",
                "-y",  # Overwrite output file if it exists
                output_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        return output_file

    def get_channel_layout(self, input_file: str) -> Tuple[int, str]:
        """Get the channel layout of an audio file.
        
        Args:
            input_file: Path to the input audio file.
            
        Returns:
            Tuple of (number of channels, channel layout).
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
        
        # Parse FFmpeg output for channel info
        for line in result.stderr.splitlines():
            if "Audio:" in line:
                parts = line.split()
                for part in parts:
                    if "Hz" in part:
                        continue
                    if "ch" in part:
                        channels = int(part.replace("ch", ""))
                    if "stereo" in line:
                        layout = "stereo"
                    elif "5.1" in line:
                        layout = "5.1"
                    elif "7.1" in line:
                        layout = "7.1"
                    elif "mono" in line:
                        layout = "mono"
                    else:
                        layout = "unknown"
                return channels, layout
        
        raise RuntimeError("Could not determine channel layout.")
"""
Stage 27: Artwork Removal
------------------------
Uses exiftool (https://github.com/exiftool/exiftool) to remove artwork from audio files.

Dependencies:
- exiftool (https://github.com/exiftool/exiftool)
"""

import subprocess
import os
from typing import Optional


class ArtworkAdapter:
    """Python adapter for artwork removal using exiftool."""

    def __init__(self, exiftool_path: str = "exiftool"):
        self.exiftool_path = exiftool_path
        self._validate_exiftool()

    def _validate_exiftool(self):
        """Check if exiftool is available."""
        try:
            subprocess.run(
                [self.exiftool_path, "-ver"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ImportError(
                "exiftool not found. Install it from: https://github.com/exiftool/exiftool"
            )

    def remove_artwork(self, input_file: str, output_file: Optional[str] = None) -> str:
        """Remove artwork from the input file.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output file. If None, overwrites the input file.
            
        Returns:
            Path to the output file.
        """
        if output_file is None:
            output_file = input_file
        
        subprocess.run(
            [
                self.exiftool_path,
                "-overwrite_original",
                "-P",  # Preserve file modification date
                "-all=",  # Remove all metadata
                "-TagsFromFile", "@",  # Recover essential tags
                "-Artist", "-Album", "-Title", "-Track", "-Year",  # Keep these tags
                "-o", output_file,  # Output file
                input_file,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        return output_file

    def has_artwork(self, input_file: str) -> bool:
        """Check if the input file contains artwork.
        
        Args:
            input_file: Path to the input audio file.
            
        Returns:
            True if artwork is detected.
        """
        result = subprocess.run(
            [
                self.exiftool_path,
                "-Picture", "-b",  # Extract picture data
                input_file,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        return len(result.stdout) > 0
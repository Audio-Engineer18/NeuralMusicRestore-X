"""
Stage 26: Metadata Handling
--------------------------
Uses mutagen (https://github.com/quodlibet/mutagen) for metadata removal and editing.

Dependencies:
- mutagen (https://github.com/quodlibet/mutagen)
"""

from mutagen import File
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TDRC
from typing import Optional, Dict
import os


class MetadataAdapter:
    """Python adapter for metadata handling using mutagen."""

    def __init__(self):
        pass

    def remove_metadata(self, input_file: str, output_file: Optional[str] = None) -> str:
        """Remove all metadata from the input file.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output file. If None, overwrites the input file.
            
        Returns:
            Path to the output file.
        """
        if output_file is None:
            output_file = input_file
        
        # Load the audio file
        audio = File(input_file)
        if audio is None:
            raise ValueError(f"Unsupported file format: {input_file}")
        
        # Remove metadata
        if audio.tags is not None:
            audio.tags.clear()
            audio.save(output_file)
        else:
            # If no tags exist, copy the file as-is
            if input_file != output_file:
                import shutil
                shutil.copy2(input_file, output_file)
        
        return output_file

    def edit_metadata(
        self,
        input_file: str,
        output_file: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> str:
        """Edit metadata of the input file.
        
        Args:
            input_file: Path to the input audio file.
            output_file: Path to the output file. If None, overwrites the input file.
            metadata: Dictionary of metadata fields (e.g., {"title": "Song", "artist": "Artist"}).
            
        Returns:
            Path to the output file.
        """
        if output_file is None:
            output_file = input_file
        
        if metadata is None:
            metadata = {}
        
        # Load the audio file
        audio = File(input_file)
        if audio is None:
            raise ValueError(f"Unsupported file format: {input_file}")
        
        # Initialize tags if they don't exist
        if audio.tags is None:
            audio.add_tags()
        
        # Update metadata
        for key, value in metadata.items():
            audio.tags[key] = value
        
        audio.save(output_file)
        return output_file

    def get_metadata(self, input_file: str) -> Dict[str, str]:
        """Get metadata from the input file.
        
        Args:
            input_file: Path to the input audio file.
            
        Returns:
            Dictionary of metadata fields.
        """
        audio = File(input_file)
        if audio is None or audio.tags is None:
            return {}
        
        return dict(audio.tags)
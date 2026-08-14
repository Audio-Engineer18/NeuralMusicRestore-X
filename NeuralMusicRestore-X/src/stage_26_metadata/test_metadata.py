"""
Test Stage 26: Metadata Handling
"""

import os
import tempfile
import pytest
from adapter import MetadataAdapter


def test_remove_metadata():
    """Test metadata removal."""
    # Create a test WAV file with metadata
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        input_file = tmp_file.name
    
    # Write a dummy WAV file (mutagen doesn't support WAV metadata, so we'll use FLAC)
    with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as tmp_flac:
        flac_file = tmp_flac.name
    
    from stage_06_flac.adapter import FLACAdapter
    adapter = FLACAdapter()
    # Create a dummy FLAC file with metadata
    adapter.encode_to_flac(
        input_file.replace(".wav", ".dummy"),  # Dummy input
        flac_file,
        samplerate=44100,
        channels=2,
    )
    
    # Add metadata
    metadata_adapter = MetadataAdapter()
    metadata_adapter.edit_metadata(flac_file, metadata={"title": "Test Song", "artist": "Test Artist"})
    
    # Remove metadata
    metadata_adapter.remove_metadata(flac_file)
    
    # Verify metadata is removed
    metadata = metadata_adapter.get_metadata(flac_file)
    assert len(metadata) == 0
    
    # Cleanup
    os.remove(flac_file)


def test_edit_metadata():
    """Test metadata editing."""
    # Create a test FLAC file
    with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as tmp_file:
        flac_file = tmp_file.name
    
    from stage_06_flac.adapter import FLACAdapter
    adapter = FLACAdapter()
    adapter.encode_to_flac(
        flac_file.replace(".flac", ".dummy"),  # Dummy input
        flac_file,
        samplerate=44100,
        channels=2,
    )
    
    # Edit metadata
    metadata_adapter = MetadataAdapter()
    metadata_adapter.edit_metadata(
        flac_file,
        metadata={"title": "Test Song", "artist": "Test Artist", "album": "Test Album"},
    )
    
    # Verify metadata
    metadata = metadata_adapter.get_metadata(flac_file)
    assert metadata["title"] == "Test Song"
    assert metadata["artist"] == "Test Artist"
    assert metadata["album"] == "Test Album"
    
    # Cleanup
    os.remove(flac_file)


def test_get_metadata():
    """Test metadata retrieval."""
    # Create a test FLAC file
    with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as tmp_file:
        flac_file = tmp_file.name
    
    from stage_06_flac.adapter import FLACAdapter
    adapter = FLACAdapter()
    adapter.encode_to_flac(
        flac_file.replace(".flac", ".dummy"),  # Dummy input
        flac_file,
        samplerate=44100,
        channels=2,
    )
    
    # Add metadata
    metadata_adapter = MetadataAdapter()
    metadata_adapter.edit_metadata(
        flac_file,
        metadata={"title": "Test Song", "artist": "Test Artist"},
    )
    
    # Get metadata
    metadata = metadata_adapter.get_metadata(flac_file)
    assert metadata["title"] == "Test Song"
    assert metadata["artist"] == "Test Artist"
    
    # Cleanup
    os.remove(flac_file)


if __name__ == "__main__":
    test_remove_metadata()
    test_edit_metadata()
    test_get_metadata()
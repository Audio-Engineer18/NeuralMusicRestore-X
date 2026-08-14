"""
Test Stage 27: Artwork Removal
"""

import os
import tempfile
import pytest
from adapter import ArtworkAdapter


def test_remove_artwork():
    """Test artwork removal."""
    # Create a test file with artwork (using a dummy image)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        input_file = tmp_file.name
    
    # Create a dummy image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        img_file = tmp_img.name
        with open(img_file, "wb") as f:
            f.write(b"dummy image data")
    
    # Add the image as artwork to the MP3 file (using ffmpeg)
    subprocess.run(
        ["ffmpeg", "-i", input_file, "-i", img_file, "-map", "0", "-map", "1", "-c", "copy", "-disposition:v", "attached_pic", "-y", input_file],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Remove artwork
    adapter = ArtworkAdapter()
    adapter.remove_artwork(input_file)
    
    # Verify artwork is removed
    assert not adapter.has_artwork(input_file)
    
    # Cleanup
    os.remove(input_file)
    os.remove(img_file)


def test_has_artwork():
    """Test artwork detection."""
    # Create a test file without artwork
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        input_file = tmp_file.name
    
    adapter = ArtworkAdapter()
    assert not adapter.has_artwork(input_file)
    
    # Add artwork (using ffmpeg)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        img_file = tmp_img.name
        with open(img_file, "wb") as f:
            f.write(b"dummy image data")
    
    subprocess.run(
        ["ffmpeg", "-i", input_file, "-i", img_file, "-map", "0", "-map", "1", "-c", "copy", "-disposition:v", "attached_pic", "-y", input_file],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Verify artwork is detected
    assert adapter.has_artwork(input_file)
    
    # Cleanup
    os.remove(input_file)
    os.remove(img_file)


if __name__ == "__main__":
    test_remove_artwork()
    test_has_artwork()
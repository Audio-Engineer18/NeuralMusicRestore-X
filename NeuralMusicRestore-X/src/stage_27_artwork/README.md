# Stage 27: Artwork Removal

## Overview
- **Purpose**: Remove artwork from audio files using exiftool.
- **Upstream**: [exiftool](https://github.com/exiftool/exiftool)
- **Implementation**: Python adapter for artwork removal.

---

## Usage
```python
from adapter import ArtworkAdapter

# Initialize the adapter
adapter = ArtworkAdapter()

# Check if artwork exists
has_artwork = adapter.has_artwork("input.mp3")
print(f"Has artwork: {has_artwork}")

# Remove artwork
adapter.remove_artwork("input.mp3", "output.mp3")
```

---

## Dependencies
- `exiftool` (install via package manager or build from source).
- Python packages: None.

---

## Testing
Run the test script:
```bash
python test_artwork.py
```
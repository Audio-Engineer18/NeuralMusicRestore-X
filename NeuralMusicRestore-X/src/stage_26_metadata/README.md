# Stage 26: Metadata Handling

## Overview
- **Purpose**: Metadata removal and editing using mutagen.
- **Upstream**: [mutagen](https://github.com/quodlibet/mutagen)
- **Implementation**: Python adapter for metadata operations.

---

## Usage
```python
from adapter import MetadataAdapter

# Initialize the adapter
adapter = MetadataAdapter()

# Remove metadata
adapter.remove_metadata("input.flac", "output.flac")

# Edit metadata
adapter.edit_metadata("input.flac", metadata={"title": "Song", "artist": "Artist"})

# Get metadata
metadata = adapter.get_metadata("input.flac")
print(metadata)
```

---

## Dependencies
- Python packages: `mutagen`.
- Install mutagen:
  ```bash
  pip install mutagen
  ```

---

## Testing
Run the test script:
```bash
python test_metadata.py
```
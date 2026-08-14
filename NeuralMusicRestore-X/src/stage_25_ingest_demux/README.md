# Stage 25: Ingest/Demux

## Overview
- **Purpose**: Extract audio streams from multimedia files using FFmpeg.
- **Upstream**: [FFmpeg](https://github.com/FFmpeg/FFmpeg)
- **Implementation**: Python adapter for stream extraction.

---

## Usage
```python
from adapter import IngestDemuxAdapter

# Initialize the adapter
adapter = IngestDemuxAdapter()

# List all audio streams in a file
streams = adapter.list_streams("input.mp4")
print(f"Available streams: {streams}")

# Extract a stream to a file
adapter.extract_stream("input.mp4", "output.wav", stream_index=0)

# Extract a stream to a numpy array
audio, samplerate = adapter.extract_to_numpy("input.mp4", stream_index=0)
```

---

## Dependencies
- `FFmpeg` (install via package manager or build from source).
- Python packages: None.

---

## Testing
Run the test script:
```bash
python test_ingest_demux.py
```
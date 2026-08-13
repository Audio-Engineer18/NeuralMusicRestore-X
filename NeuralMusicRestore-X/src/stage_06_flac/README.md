# Stage 06: FLAC Archive + Verification

## Overview
- **Purpose**: Encode, decode, and verify FLAC files using `libFLAC`.
- **Upstream**: [FLAC](https://github.com/xiph/flac)
- **Implementation**: Python/C adapter for FLAC support.

---

## Usage
```python
from adapter import FLACAdapter

# Initialize the adapter
adapter = FLACAdapter()

# Encode a WAV file to FLAC
adapter.encode_to_flac("input.wav", "output.flac", samplerate=44100, channels=2)

# Decode a FLAC file to WAV
adapter.decode_to_wav("input.flac", "output.wav")

# Verify a FLAC file
is_valid = adapter.verify_flac("input.flac")
print(f"Is valid: {is_valid}")
```

---

## Dependencies
- `libFLAC` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_flac.py
```
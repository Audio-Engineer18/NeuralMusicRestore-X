# Stage 03: RF64

## Overview
- **Purpose**: Validate and write RF64 WAV files (supports >4GB) using `libsndfile`.
- **Upstream**: [libsndfile](https://github.com/libsndfile/libsndfile)
- **Implementation**: Python/C adapter for RF64 support.

---

## Usage
```python
from adapter import RF64Adapter

# Write an RF64 file
with RF64Adapter("output_rf64.wav", "w", samplerate=44100, channels=2) as rf64:
    rf64.write(audio_data)  # audio_data is a numpy float32 array

# Validate an RF64 file
is_rf64 = RF64Adapter.validate_rf64("output_rf64.wav")
print(f"Is RF64: {is_rf64}")
```

---

## Dependencies
- `libsndfile` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_rf64.py
```
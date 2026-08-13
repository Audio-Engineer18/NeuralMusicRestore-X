# Stage 12: Hum Detection and Notch Filtering

## Overview
- **Purpose**: Detect and remove 50/60Hz hum using `iir1`.
- **Upstream**: [iir1](https://github.com/berndporr/iir1)
- **Implementation**: Python adapter for hum detection and notch filtering.

---

## Usage
```python
from adapter import HumAdapter

# Initialize the adapter
adapter = HumAdapter(samplerate=44100, notch_freq=50.0)

# Detect hum
has_hum = adapter.detect_hum(audio_data, threshold=0.1)
print(f"Hum detected: {has_hum}")

# Remove hum
filtered_audio = adapter.remove_hum(audio_data)
```

---

## Dependencies
- `libiir1` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_hum.py
```
# Stage 10: Subsonic Filtering

## Overview
- **Purpose**: Zero-phase subsonic filtering using `iir1`.
- **Upstream**: [iir1](https://github.com/berndporr/iir1)
- **Implementation**: Python/C adapter for IIR filtering.

---

## Usage
```python
from adapter import SubsonicAdapter

# Initialize the filter
with SubsonicAdapter(samplerate=44100, cutoff=20.0) as filter:
    filtered_audio = filter.process(audio_data)  # audio_data is a numpy float64 array
```

---

## Dependencies
- `libiir1` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_subsonic.py
```
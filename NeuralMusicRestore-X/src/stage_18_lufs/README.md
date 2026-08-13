# Stage 18: LUFS Loudness Metering

## Overview
- **Purpose**: EBU R128 loudness metering using libebur128.
- **Upstream**: [libebur128](https://github.com/jiixyj/libebur128)
- **Implementation**: Python adapter for LUFS measurement.

---

## Usage
```python
from adapter import LufsAdapter

# Initialize the adapter
with LufsAdapter(samplerate=44100, channels=2) as adapter:
    global_lufs, momentary_lufs, shortterm_lufs = adapter.measure_loudness(audio_data)
    print(f"Global LUFS: {global_lufs}")
    print(f"Momentary LUFS: {momentary_lufs}")
    print(f"Short-term LUFS: {shortterm_lufs}")
```

---

## Dependencies
- `libebur128` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_lufs.py
```
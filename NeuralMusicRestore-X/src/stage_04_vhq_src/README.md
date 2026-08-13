# Stage 04: VHQ Sample Rate Conversion (SRC)

## Overview
- **Purpose**: High-quality sample rate conversion using `soxr`.
- **Upstream**: [soxr](https://github.com/chirlu/soxr)
- **Implementation**: Python/C adapter for VHQ SRC.

---

## Usage
```python
from adapter import VHQSrcAdapter

# Initialize the SRC adapter
with VHQSrcAdapter(input_rate=44100, output_rate=48000, channels=2) as src:
    resampled_audio = src.process(audio_data)  # audio_data is a numpy float32 array
```

---

## Dependencies
- `libsoxr` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_vhq_src.py
```
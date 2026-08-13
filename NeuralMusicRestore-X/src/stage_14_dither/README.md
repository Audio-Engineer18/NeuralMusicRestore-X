# Stage 14: Dithering

## Overview
- **Purpose**: Apply dithering for 24-bit quantization using SSRC.
- **Upstream**: [SSRC](https://github.com/shibatch/SSRC)
- **Implementation**: Python adapter for dithering.

---

## Usage
```python
from adapter import DitherAdapter

# Initialize the adapter
adapter = DitherAdapter(samplerate=44100, bits_per_sample=24)

# Apply dithering
dithered_audio = adapter.process(audio_data)  # Returns int32

# Apply dithering and convert back to float
dithered_float = adapter.process_to_float(audio_data)  # Returns float32
```

---

## Dependencies
- `libssrc` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_dither.py
```
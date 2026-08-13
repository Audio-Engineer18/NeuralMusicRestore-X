# Stage 09: Advanced Sample Rate Conversion (SRC)

## Overview
- **Purpose**: High-performance sample rate conversion using KFR.
- **Upstream**: [KFR](https://github.com/kfrlib/kfr)
- **Implementation**: Python/C adapter for native KFR SRC.

---

## Usage
```python
from adapter import AdvancedSrcAdapter

# Initialize the resampler
with AdvancedSrcAdapter(input_rate=44100, output_rate=48000, channels=2) as src:
    resampled_audio = src.process(audio_data)  # audio_data is a numpy float64 array
```

---

## Dependencies
- `libkfr` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_advanced_src.py
```
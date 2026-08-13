# Stage 07: 64-bit Floating-Point DSP

## Overview
- **Purpose**: High-precision (float64) digital signal processing using `numpy`.
- **Upstream**: [NumPy](https://github.com/numpy/numpy)
- **Implementation**: Python adapter for float64 DSP operations.

---

## Usage
```python
from adapter import Float64Adapter

# Convert audio to float64
audio_float64 = Float64Adapter.to_float64(audio_data)

# Normalize audio
normalized = Float64Adapter.normalize(audio_float64, target_peak=1.0)

# Apply gain
gained = Float64Adapter.apply_gain(audio_float64, gain_db=6.0)

# Mix two audio signals
mixed = Float64Adapter.mix(audio1, audio2, weight1=0.5, weight2=0.5)

# Resample audio
resampled = Float64Adapter.resample(audio_float64, original_rate=44100, target_rate=48000)

# Apply fade-in/fade-out
faded = Float64Adapter.fade_in_out(audio_float64, fade_duration=2.0, samplerate=44100)
```

---

## Dependencies
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_float64.py
```
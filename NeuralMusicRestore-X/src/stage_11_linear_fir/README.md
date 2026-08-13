# Stage 11: Linear FIR Filtering

## Overview
- **Purpose**: Design and apply 511-tap FIR filters using `scipy`.
- **Upstream**: [SciPy](https://github.com/scipy/scipy)
- **Implementation**: Python adapter for linear and zero-phase FIR filtering.

---

## Usage
```python
from adapter import LinearFirAdapter

# Initialize the FIR filter
adapter = LinearFirAdapter(samplerate=44100, cutoff=2000.0, numtaps=511)

# Apply linear FIR filtering
filtered_audio = adapter.process(audio_data)  # audio_data is a numpy float64 array

# Apply zero-phase FIR filtering
zero_phase_audio = adapter.process_zero_phase(audio_data)
```

---

## Dependencies
- Python packages: `scipy`, `numpy`.

---

## Testing
Run the test script:
```bash
python test_linear_fir.py
```
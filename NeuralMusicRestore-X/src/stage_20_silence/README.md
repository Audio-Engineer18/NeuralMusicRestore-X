# Stage 20: Silence Detection and Trimming

## Overview
- **Purpose**: Boundary analysis and silence trimming using silan.
- **Upstream**: [silan](https://github.com/x42/silan)
- **Implementation**: Python adapter for silence detection and trimming.

---

## Usage
```python
from adapter import SilenceAdapter

# Initialize the adapter
adapter = SilenceAdapter()

# Detect silence boundaries
detect_start, detect_end = adapter.detect_silence("input.wav", threshold=-60.0, duration=0.1)
print(f"Silence boundaries: {detect_start}s to {detect_end}s")

# Trim silence from a file
adapter.trim_silence("input.wav", "output_trimmed.wav", threshold=-60.0, duration=0.1)

# Trim silence from a numpy array
trimmed_audio = adapter.process(audio_data, samplerate=44100)
```

---

## Dependencies
- `silan` (install via package manager or build from source).
- Python packages: None.

---

## Testing
Run the test script:
```bash
python test_silence.py
```
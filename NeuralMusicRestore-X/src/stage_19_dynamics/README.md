# Stage 19: Dynamics Processing

## Overview
- **Purpose**: Conservative leveling using DynamicAudioNormalizer.
- **Upstream**: [DynamicAudioNormalizer](https://github.com/lordmulder/DynamicAudioNormalizer)
- **Implementation**: Python adapter for dynamics normalization.

---

## Usage
```python
from adapter import DynamicsAdapter

# Initialize the adapter
with DynamicsAdapter(samplerate=44100, channels=2) as adapter:
    processed_audio = adapter.process(audio_data)
```

---

## Dependencies
- `libDynamicAudioNormalizer` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_dynamics.py
```
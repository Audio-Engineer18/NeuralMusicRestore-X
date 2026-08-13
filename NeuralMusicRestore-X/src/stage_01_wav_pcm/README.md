# Stage 01: WAV/PCM

## Overview
- **Purpose**: Read/write WAV/PCM files using `libsndfile`.
- **Upstream**: [libsndfile](https://github.com/libsndfile/libsndfile)
- **Implementation**: Python/C adapter.

---

## Usage
```python
from adapter import WavAdapter

# Read a WAV file
with WavAdapter("input.wav", "r") as wav:
    data = wav.read()
    print(f"Sample rate: {wav.samplerate}")
    print(f"Channels: {wav.channels}")

# Write a WAV file
with WavAdapter("output.wav", "w") as wav:
    wav.write(data)
```

---

## Dependencies
- `libsndfile` (install via package manager or build from source).
- Python packages: `numpy`, `cffi`.

---

## Testing
Run the test script:
```bash
python test_wav_pcm.py
```
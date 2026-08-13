# Stage 02: WavPack

## Overview
- **Purpose**: Decode/encode WavPack (.wv) files using `wvunpack`.
- **Upstream**: [WavPack](https://github.com/dbry/WavPack)
- **Implementation**: Python adapter for `wvunpack`.

---

## Usage
```python
from adapter import WavPackAdapter

# Initialize the adapter
adapter = WavPackAdapter()

# Decode a WavPack file to WAV
wav_file = adapter.decode_to_wav("input.wv")

# Extract metadata
info = adapter.get_audio_info("input.wv")
print(f"Sample rate: {info['samplerate']}")
print(f"Channels: {info['channels']}")
```

---

## Dependencies
- `wvunpack` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_wavpack.py
```

**Note**: Requires `wavpack` CLI tool to be installed for encoding/decoding.
# Stage 15: DC Offset Removal

## Overview
- **Purpose**: Remove per-channel DC offset using Essentia.
- **Upstream**: [Essentia](https://github.com/MTG/essentia)
- **Implementation**: Python adapter for DC offset removal.

---

## Usage
```python
from adapter import DcAdapter

# Initialize the adapter
with DcAdapter() as dc_remover:
    processed_audio = dc_remover.process(audio_data)
```

---

## Dependencies
- `libessentia` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_dc.py
```
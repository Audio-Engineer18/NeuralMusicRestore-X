# Stage 17: True Peak Detection

## Overview
- **Purpose**: Oversampled true peak detection using libebur128.
- **Upstream**: [libebur128](https://github.com/jiixyj/libebur128)
- **Implementation**: Python adapter for true peak detection.

---

## Usage
```python
from adapter import TruePeakAdapter

# Initialize the adapter
with TruePeakAdapter(samplerate=44100, channels=2) as adapter:
    global_peak, per_channel_peaks = adapter.detect_true_peak(audio_data)
    print(f"Global true peak: {global_peak} dBFS")
    print(f"Per-channel true peaks: {per_channel_peaks} dBFS")
```

---

## Dependencies
- `libebur128` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_true_peak.py
```
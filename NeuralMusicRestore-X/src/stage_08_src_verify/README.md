# Stage 08: Sample Rate Conversion (SRC) Verification

## Overview
- **Purpose**: Verify the accuracy of sample rate conversion using `soxr`.
- **Upstream**: [soxr](https://github.com/chirlu/soxr)
- **Implementation**: Python adapter for SRC verification.

---

## Usage
```python
from adapter import SrcVerifyAdapter

# Initialize the verifier
verifier = SrcVerifyAdapter(input_rate=44100, output_rate=48000, channels=2)

# Verify resampled audio
is_accurate = verifier.verify_src(original_audio, resampled_audio)
print(f"Is accurate: {is_accurate}")
```

---

## Dependencies
- `libsoxr` (install via package manager or build from source).
- Python packages: `numpy`.

---

## Testing
Run the test script:
```bash
python test_src_verify.py
```
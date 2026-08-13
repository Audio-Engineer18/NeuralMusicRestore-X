# Stage 05: Channel Layout Engine

## Overview
- **Purpose**: Manipulate audio channel layouts (e.g., stereo to 5.1) using FFmpeg.
- **Upstream**: [FFmpeg](https://github.com/FFmpeg/FFmpeg)
- **Implementation**: Python adapter for channel layout conversion.

---

## Usage
```python
from adapter import ChannelAdapter

# Initialize the adapter
adapter = ChannelAdapter()

# Convert stereo to mono
adapter.convert_channels("input.wav", "output_mono.wav", output_channels=1, output_layout="mono")

# Extract a single channel
adapter.extract_channel("input.wav", "left_channel.wav", channel=0)

# Get channel layout
channels, layout = adapter.get_channel_layout("input.wav")
print(f"Channels: {channels}, Layout: {layout}")
```

---

## Dependencies
- `FFmpeg` (install via package manager or build from source).
- Python packages: None.

---

## Testing
Run the test script:
```bash
python test_channels.py
```
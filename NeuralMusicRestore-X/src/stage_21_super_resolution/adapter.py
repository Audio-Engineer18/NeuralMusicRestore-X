"""
Stage 21: Super-Resolution
-------------------------
Uses Versatile Audio Super Resolution (VASR) for adaptive high-frequency reconstruction.

Dependencies:
- VASR (https://github.com/haoheliu/versatile_audio_super_resolution)
"""

import numpy as np
import torch
import torchaudio
from typing import Optional
import os

# Check if VASR is available
try:
    from vasr import VASR
    from vasr.utils import load_model
except ImportError:
    raise ImportError(
        "VASR not found. Install it from: https://github.com/haoheliu/versatile_audio_super_resolution"
    )


class SuperResolutionAdapter:
    """Python adapter for super-resolution using VASR."""

    def __init__(self, model_path: Optional[str] = None, device: str = "auto"):
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self._load_model(model_path)

    def _load_model(self, model_path: Optional[str] = None):
        """Load the VASR model."""
        if model_path is None:
            model_path = os.path.expanduser("~/.cache/vasr/model.pth")
        
        self.model = load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

    def process(
        self,
        audio: np.ndarray,
        input_sr: int = 44100,
        output_sr: int = 88200,
        batch_size: int = 4,
    ) -> np.ndarray:
        """Apply super-resolution to the input audio.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            input_sr: Input sample rate (Hz).
            output_sr: Output sample rate (Hz).
            batch_size: Batch size for processing.
            
        Returns:
            Super-resolved audio as a numpy float32 array.
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Convert to torch tensor and move to device
        audio_tensor = torch.from_numpy(audio).to(self.device)
        audio_tensor = audio_tensor.permute(1, 0)  # [channels, samples]
        
        # Resample to model's expected input rate if needed
        if input_sr != 44100:
            resampler = torchaudio.transforms.Resample(
                orig_freq=input_sr, new_freq=44100
            ).to(self.device)
            audio_tensor = resampler(audio_tensor)
        
        # Process in batches
        super_resolved = []
        with torch.no_grad():
            for i in range(0, audio_tensor.shape[1], batch_size):
                batch = audio_tensor[:, i:i + batch_size]
                batch_sr = self.model(batch.unsqueeze(0))
                super_resolved.append(batch_sr.squeeze(0))
        
        # Concatenate batches
        super_resolved_tensor = torch.cat(super_resolved, dim=1)
        
        # Resample to desired output rate
        if output_sr != 88200:
            resampler = torchaudio.transforms.Resample(
                orig_freq=88200, new_freq=output_sr
            ).to(self.device)
            super_resolved_tensor = resampler(super_resolved_tensor)
        
        # Convert back to numpy
        super_resolved_audio = super_resolved_tensor.permute(1, 0).cpu().numpy()
        return super_resolved_audio
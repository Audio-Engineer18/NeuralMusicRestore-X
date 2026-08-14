"""
Stage 23: Music Restoration
--------------------------
Uses Apollo (https://github.com/JusperLee/Apollo) for primary music restoration.

Dependencies:
- Apollo (https://github.com/JusperLee/Apollo)
"""

import numpy as np
import torch
import torchaudio
from typing import Optional
import os

# Check if Apollo is available
try:
    from apollo import ApolloModel
    from apollo.utils import load_pretrained_model
except ImportError:
    raise ImportError(
        "Apollo not found. Install it from: https://github.com/JusperLee/Apollo"
    )


class MusicRestorationAdapter:
    """Python adapter for music restoration using Apollo."""

    def __init__(self, model_path: Optional[str] = None, device: str = "auto"):
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self._load_model(model_path)

    def _load_model(self, model_path: Optional[str] = None):
        """Load the Apollo model."""
        if model_path is None:
            model_path = os.path.expanduser("~/.cache/apollo/model.pth")
        
        self.model = load_pretrained_model(model_path)
        self.model.to(self.device)
        self.model.eval()

    def process(
        self,
        audio: np.ndarray,
        samplerate: int = 44100,
        batch_size: int = 4,
    ) -> np.ndarray:
        """Apply music restoration to the input audio.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            samplerate: Sample rate of the input audio.
            batch_size: Batch size for processing.
            
        Returns:
            Restored audio as a numpy float32 array.
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Convert to torch tensor and move to device
        audio_tensor = torch.from_numpy(audio).to(self.device)
        audio_tensor = audio_tensor.permute(1, 0)  # [channels, samples]
        
        # Resample to model's expected input rate if needed
        if samplerate != 44100:
            resampler = torchaudio.transforms.Resample(
                orig_freq=samplerate, new_freq=44100
            ).to(self.device)
            audio_tensor = resampler(audio_tensor)
        
        # Process in batches
        restored = []
        with torch.no_grad():
            for i in range(0, audio_tensor.shape[1], batch_size):
                batch = audio_tensor[:, i:i + batch_size]
                batch_restored = self.model(batch.unsqueeze(0))
                restored.append(batch_restored.squeeze(0))
        
        # Concatenate batches
        restored_tensor = torch.cat(restored, dim=1)
        
        # Resample back to original sample rate if needed
        if samplerate != 44100:
            resampler = torchaudio.transforms.Resample(
                orig_freq=44100, new_freq=samplerate
            ).to(self.device)
            restored_tensor = resampler(restored_tensor)
        
        # Convert back to numpy
        restored_audio = restored_tensor.permute(1, 0).cpu().numpy()
        return restored_audio
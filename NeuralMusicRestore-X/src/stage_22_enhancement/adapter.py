"""
Stage 22: Audio Enhancement
--------------------------
Uses Resemble Enhance (https://github.com/resemble-ai/resemble-enhance) for conditional vocal enhancement.

Dependencies:
- Resemble Enhance (https://github.com/resemble-ai/resemble-enhance)
"""

import numpy as np
import torch
import torchaudio
from typing import Optional
import os

# Check if Resemble Enhance is available
try:
    from resemble_enhance import Enhancer
    from resemble_enhance.utils import load_model
except ImportError:
    raise ImportError(
        "Resemble Enhance not found. Install it from: https://github.com/resemble-ai/resemble-enhance"
    )


class EnhancementAdapter:
    """Python adapter for audio enhancement using Resemble Enhance."""

    def __init__(self, model_path: Optional[str] = None, device: str = "auto"):
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self._load_model(model_path)

    def _load_model(self, model_path: Optional[str] = None):
        """Load the Resemble Enhance model."""
        if model_path is None:
            model_path = os.path.expanduser("~/.cache/resemble_enhance/model.pth")
        
        self.model = load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

    def process(
        self,
        audio: np.ndarray,
        samplerate: int = 44100,
        denoise: bool = True,
        enhance: bool = True,
        batch_size: int = 4,
    ) -> np.ndarray:
        """Apply conditional vocal enhancement to the input audio.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            samplerate: Sample rate of the input audio.
            denoise: Whether to apply denoising.
            enhance: Whether to apply enhancement.
            batch_size: Batch size for processing.
            
        Returns:
            Enhanced audio as a numpy float32 array.
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
        enhanced = []
        with torch.no_grad():
            for i in range(0, audio_tensor.shape[1], batch_size):
                batch = audio_tensor[:, i:i + batch_size]
                batch_enhanced = self.model.enhance(
                    batch.unsqueeze(0),
                    denoise=denoise,
                    enhance=enhance,
                )
                enhanced.append(batch_enhanced.squeeze(0))
        
        # Concatenate batches
        enhanced_tensor = torch.cat(enhanced, dim=1)
        
        # Resample back to original sample rate if needed
        if samplerate != 44100:
            resampler = torchaudio.transforms.Resample(
                orig_freq=44100, new_freq=samplerate
            ).to(self.device)
            enhanced_tensor = resampler(enhanced_tensor)
        
        # Convert back to numpy
        enhanced_audio = enhanced_tensor.permute(1, 0).cpu().numpy()
        return enhanced_audio
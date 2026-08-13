"""
Stage 13: AI-Powered Denoising
------------------------------
Uses DeepFilterNet (https://github.com/Rikorose/DeepFilterNet) for mid-channel AI denoising.

Dependencies:
- DeepFilterNet (https://github.com/Rikorose/DeepFilterNet)
"""

import numpy as np
import torch
import torchaudio
from typing import Optional
import os

# Check if DeepFilterNet is available
try:
    from deepfilternet import DeepFilterNet
except ImportError:
    raise ImportError(
        "DeepFilterNet not found. Install it from: https://github.com/Rikorose/DeepFilterNet"
    )


class DenoiseAdapter:
    """Python adapter for AI-powered denoising using DeepFilterNet."""

    def __init__(self, model_base_dir: Optional[str] = None):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model(model_base_dir)

    def _load_model(self, model_base_dir: Optional[str] = None):
        """Load the DeepFilterNet model."""
        if model_base_dir is None:
            model_base_dir = os.path.expanduser("~/.cache/DeepFilterNet")
        
        self.model = DeepFilterNet(model_base_dir=model_base_dir)
        self.model.to(self.device)
        self.model.eval()

    def process(self, audio: np.ndarray, samplerate: int = 44100) -> np.ndarray:
        """Apply AI denoising to the input audio.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            samplerate: Sample rate of the input audio.
            
        Returns:
            Denoised audio as a numpy float32 array.
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Convert to torch tensor and move to device
        audio_tensor = torch.from_numpy(audio).to(self.device)
        audio_tensor = audio_tensor.permute(1, 0)  # [channels, samples]
        
        # Resample if necessary
        if samplerate != 48000:
            resampler = torchaudio.transforms.Resample(
                orig_freq=samplerate, new_freq=48000
            ).to(self.device)
            audio_tensor = resampler(audio_tensor)
        
        # Apply denoising
        with torch.no_grad():
            denoised_tensor = self.model(audio_tensor.unsqueeze(0))[0]
        
        # Resample back to original sample rate if needed
        if samplerate != 48000:
            resampler = torchaudio.transforms.Resample(
                orig_freq=48000, new_freq=samplerate
            ).to(self.device)
            denoised_tensor = resampler(denoised_tensor)
        
        # Convert back to numpy
        denoised_audio = denoised_tensor.squeeze(0).permute(1, 0).cpu().numpy()
        return denoised_audio
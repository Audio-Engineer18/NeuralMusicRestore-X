"""
Stage 07: 64-bit Floating-Point DSP
----------------------------------
Uses `numpy` for high-precision (float64) digital signal processing.
"""

import numpy as np
from typing import Optional, Tuple


class Float64Adapter:
    """Python adapter for 64-bit floating-point DSP operations."""

    @staticmethod
    def to_float64(audio: np.ndarray) -> np.ndarray:
        """Convert audio data to float64.
        
        Args:
            audio: Input audio as a numpy array (any dtype).
            
        Returns:
            Audio data as float64.
        """
        return audio.astype(np.float64)

    @staticmethod
    def normalize(audio: np.ndarray, target_peak: float = 1.0) -> np.ndarray:
        """Normalize audio to a target peak amplitude.
        
        Args:
            audio: Input audio as a numpy array (float64).
            target_peak: Target peak amplitude (default: 1.0).
            
        Returns:
            Normalized audio.
        """
        current_peak = np.max(np.abs(audio))
        if current_peak == 0:
            return audio
        return audio * (target_peak / current_peak)

    @staticmethod
    def apply_gain(audio: np.ndarray, gain_db: float) -> np.ndarray:
        """Apply gain to audio in decibels.
        
        Args:
            audio: Input audio as a numpy array (float64).
            gain_db: Gain in decibels.
            
        Returns:
            Audio with applied gain.
        """
        gain_linear = 10 ** (gain_db / 20)
        return audio * gain_linear

    @staticmethod
    def mix(audio1: np.ndarray, audio2: np.ndarray, weight1: float = 0.5, weight2: float = 0.5) -> np.ndarray:
        """Mix two audio signals with given weights.
        
        Args:
            audio1: First audio signal (float64).
            audio2: Second audio signal (float64).
            weight1: Weight for the first signal (default: 0.5).
            weight2: Weight for the second signal (default: 0.5).
            
        Returns:
            Mixed audio signal.
        """
        return (audio1 * weight1) + (audio2 * weight2)

    @staticmethod
    def resample(audio: np.ndarray, original_rate: int, target_rate: int) -> np.ndarray:
        """Resample audio using linear interpolation.
        
        Args:
            audio: Input audio as a numpy array (float64).
            original_rate: Original sample rate (Hz).
            target_rate: Target sample rate (Hz).
            
        Returns:
            Resampled audio.
        """
        if original_rate == target_rate:
            return audio
        
        # Calculate resampling ratio
        ratio = target_rate / original_rate
        original_indices = np.arange(len(audio))
        target_indices = np.linspace(0, len(audio) - 1, num=int(len(audio) * ratio))
        
        # Resample each channel
        resampled = np.zeros((len(target_indices), audio.shape[1]), dtype=np.float64)
        for channel in range(audio.shape[1]):
            resampled[:, channel] = np.interp(target_indices, original_indices, audio[:, channel])
        
        return resampled

    @staticmethod
    def fade_in_out(audio: np.ndarray, fade_duration: float, samplerate: int) -> np.ndarray:
        """Apply fade-in and fade-out to audio.
        
        Args:
            audio: Input audio as a numpy array (float64).
            fade_duration: Duration of fade-in/fade-out in seconds.
            samplerate: Sample rate (Hz).
            
        Returns:
            Audio with fade-in and fade-out applied.
        """
        fade_samples = int(fade_duration * samplerate)
        if fade_samples * 2 > len(audio):
            raise ValueError("Fade duration is too long for the audio.")
        
        # Fade-in (linear)
        fade_in = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] = audio[:fade_samples] * fade_in[:, np.newaxis]
        
        # Fade-out (linear)
        fade_out = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] = audio[-fade_samples:] * fade_out[:, np.newaxis]
        
        return audio
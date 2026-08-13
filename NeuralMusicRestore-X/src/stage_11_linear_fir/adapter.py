"""
Stage 11: Linear FIR Filtering
------------------------------
Uses `scipy` to design and apply 511-tap FIR filters.

Dependencies:
- scipy (https://github.com/scipy/scipy)
"""

import numpy as np
from scipy import signal
from typing import Optional


class LinearFirAdapter:
    """Python adapter for linear FIR filtering using scipy."""

    def __init__(
        self,
        samplerate: float,
        cutoff: float = 1000.0,
        numtaps: int = 511,
    ):
        self.samplerate = samplerate
        self.cutoff = cutoff
        self.numtaps = numtaps
        self.filter_coeffs = self._design_filter()

    def _design_filter(self) -> np.ndarray:
        """Design a lowpass FIR filter using the window method.
        
        Returns:
            Filter coefficients as a numpy array.
        """
        nyquist = 0.5 * self.samplerate
        cutoff_normalized = self.cutoff / nyquist
        return signal.firwin(self.numtaps, cutoff_normalized)

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply the FIR filter to the input audio.
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            
        Returns:
            Filtered audio as a numpy float64 array.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        # Apply filtering to each channel
        filtered = np.zeros_like(audio)
        for channel in range(audio.shape[1]):
            filtered[:, channel] = signal.lfilter(
                self.filter_coeffs, 1.0, audio[:, channel]
            )
        
        return filtered

    def process_zero_phase(self, audio: np.ndarray) -> np.ndarray:
        """Apply zero-phase FIR filtering (forward-backward).
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            
        Returns:
            Zero-phase filtered audio as a numpy float64 array.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        # Apply forward-backward filtering to each channel
        filtered = np.zeros_like(audio)
        for channel in range(audio.shape[1]):
            filtered[:, channel] = signal.filtfilt(
                self.filter_coeffs, 1.0, audio[:, channel]
            )
        
        return filtered
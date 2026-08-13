"""
Stage 12: Hum Detection and Notch Filtering
----------------------------------------
Uses `iir1` (https://github.com/berndporr/iir1) to detect and remove 50/60Hz hum.

Dependencies:
- iir1 (https://github.com/berndporr/iir1)
"""

import ctypes
import numpy as np
import os
from typing import Optional, Tuple

# Load libiir1
try:
    libiir = ctypes.CDLL("libiir1.so")
except OSError:
    raise ImportError(
        "libiir1 not found. Install it from: https://github.com/berndporr/iir1"
    )

# Define C types and function prototypes
libiir.iir_notch_create.argtypes = [
    ctypes.c_double,  # sample rate
    ctypes.c_double,  # notch frequency
    ctypes.c_double,  # Q factor
]
libiir.iir_notch_create.restype = ctypes.c_void_p

libiir.iir_filter_process.argtypes = [
    ctypes.c_void_p,  # filter instance
    ctypes.POINTER(ctypes.c_double),  # input
    ctypes.POINTER(ctypes.c_double),  # output
    ctypes.c_size_t,  # number of samples
]
libiir.iir_filter_process.restype = None

libiir.iir_filter_delete.argtypes = [ctypes.c_void_p]
libiir.iir_filter_delete.restype = None


class HumAdapter:
    """Python adapter for 50/60Hz hum detection and notch filtering using iir1."""

    def __init__(
        self,
        samplerate: float,
        notch_freq: float = 50.0,
        q_factor: float = 30.0,
    ):
        self.samplerate = samplerate
        self.notch_freq = notch_freq
        self.q_factor = q_factor
        self.notch_filter = None
        self._create_notch_filter()

    def _create_notch_filter(self):
        """Initialize the notch filter."""
        self.notch_filter = libiir.iir_notch_create(
            self.samplerate, self.notch_freq, self.q_factor
        )
        if not self.notch_filter:
            raise RuntimeError("Failed to create notch filter")

    def detect_hum(self, audio: np.ndarray, threshold: float = 0.1) -> bool:
        """Detect the presence of hum in the audio.
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            threshold: Magnitude threshold for hum detection.
            
        Returns:
            True if hum is detected.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        # Compute FFT and check for peak at notch frequency
        fft_magnitude = np.abs(np.fft.fft(audio[:, 0]))
        freq_bin = int(self.notch_freq * len(audio) / self.samplerate)
        
        return fft_magnitude[freq_bin] > threshold

    def remove_hum(self, audio: np.ndarray) -> np.ndarray:
        """Apply notch filtering to remove hum.
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            
        Returns:
            Filtered audio as a numpy float64 array.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        filtered = np.empty_like(audio)
        for channel in range(audio.shape[1]):
            input_ptr = audio[:, channel].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
            output_ptr = filtered[:, channel].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
            libiir.iir_filter_process(self.notch_filter, input_ptr, output_ptr, audio.shape[0])
        
        return filtered

    def close(self):
        """Clean up the notch filter."""
        if self.notch_filter:
            libiir.iir_filter_delete(self.notch_filter)
            self.notch_filter = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
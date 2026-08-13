"""
Stage 10: Subsonic Filtering
----------------------------
Uses `iir1` (https://github.com/berndporr/iir1) for zero-phase subsonic filtering.

Dependencies:
- iir1 (https://github.com/berndporr/iir1)
"""

import ctypes
import numpy as np
import os
from typing import Optional

# Load libiir1
try:
    libiir = ctypes.CDLL("libiir1.so")
except OSError:
    raise ImportError(
        "libiir1 not found. Install it from: https://github.com/berndporr/iir1"
    )

# Define C types and function prototypes
libiir.iir_filter_create.argtypes = [
    ctypes.c_int,    # filter type (0 = butterworth)
    ctypes.c_int,    # order
    ctypes.c_double, # sample rate
    ctypes.c_double, # cutoff frequency
    ctypes.c_double, # bandwidth (unused for lowpass)
]
libiir.iir_filter_create.restype = ctypes.c_void_p

libiir.iir_filter_process.argtypes = [
    ctypes.c_void_p,  # filter instance
    ctypes.POINTER(ctypes.c_double),  # input
    ctypes.POINTER(ctypes.c_double),  # output
    ctypes.c_size_t,  # number of samples
]
libiir.iir_filter_process.restype = None

libiir.iir_filter_delete.argtypes = [ctypes.c_void_p]
libiir.iir_filter_delete.restype = None


class SubsonicAdapter:
    """Python adapter for zero-phase subsonic filtering using iir1."""

    def __init__(
        self,
        samplerate: float,
        cutoff: float = 20.0,
        order: int = 4,
    ):
        self.samplerate = samplerate
        self.cutoff = cutoff
        self.order = order
        self.filter = None
        self._create_filter()

    def _create_filter(self):
        """Initialize the IIR filter."""
        self.filter = libiir.iir_filter_create(
            0,  # 0 = Butterworth lowpass
            self.order,
            self.samplerate,
            self.cutoff,
            0.0,  # Unused for lowpass
        )
        if not self.filter:
            raise RuntimeError("Failed to create IIR filter")

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply zero-phase subsonic filtering.
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            
        Returns:
            Filtered audio as a numpy float64 array.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        # Apply filtering to each channel
        filtered = np.empty_like(audio)
        for channel in range(audio.shape[1]):
            input_ptr = audio[:, channel].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
            output_ptr = filtered[:, channel].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
            libiir.iir_filter_process(self.filter, input_ptr, output_ptr, audio.shape[0])
        
        return filtered

    def close(self):
        """Clean up the filter."""
        if self.filter:
            libiir.iir_filter_delete(self.filter)
            self.filter = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
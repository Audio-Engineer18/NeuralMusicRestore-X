"""
Stage 09: Advanced Sample Rate Conversion (SRC)
-------------------------------------------
Uses KFR (https://github.com/kfrlib/kfr) for high-performance native SRC.

Dependencies:
- KFR (https://github.com/kfrlib/kfr)
"""

import ctypes
import numpy as np
import os
from typing import Optional

# Load libkfr
try:
    libkfr = ctypes.CDLL("libkfr.so")
except OSError:
    raise ImportError(
        "libkfr not found. Install it from: https://github.com/kfrlib/kfr"
    )

# Define C types and function prototypes
libkfr.kfr_resample_create.argtypes = [
    ctypes.c_double,  # input sample rate
    ctypes.c_double,  # output sample rate
    ctypes.c_size_t,  # channels
]
libkfr.kfr_resample_create.restype = ctypes.c_void_p

libkfr.kfr_resample_process.argtypes = [
    ctypes.c_void_p,  # resampler instance
    np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),  # input
    ctypes.c_size_t,  # input samples
    np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),  # output
    ctypes.c_size_t,  # output buffer size
    ctypes.POINTER(ctypes.c_size_t),  # output samples written
]
libkfr.kfr_resample_process.restype = None

libkfr.kfr_resample_delete.argtypes = [ctypes.c_void_p]
libkfr.kfr_resample_delete.restype = None


class AdvancedSrcAdapter:
    """Python adapter for advanced sample rate conversion using KFR."""

    def __init__(
        self,
        input_rate: float,
        output_rate: float,
        channels: int = 2,
    ):
        self.input_rate = input_rate
        self.output_rate = output_rate
        self.channels = channels
        self.resampler = None
        self._create_resampler()

    def _create_resampler(self):
        """Initialize the KFR resampler."""
        self.resampler = libkfr.kfr_resample_create(
            self.input_rate, self.output_rate, self.channels
        )
        if not self.resampler:
            raise RuntimeError("Failed to create KFR resampler")

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Resample audio using KFR.
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            
        Returns:
            Resampled audio as a numpy float64 array.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        input_samples = audio.shape[0]
        output_samples = int(input_samples * self.output_rate / self.input_rate) + 100
        
        output = np.empty((output_samples, self.channels), dtype=np.float64)
        output_written = ctypes.c_size_t()
        
        libkfr.kfr_resample_process(
            self.resampler,
            audio,
            input_samples,
            output,
            output_samples,
            ctypes.byref(output_written),
        )
        
        return output[:output_written.value]

    def close(self):
        """Clean up the resampler."""
        if self.resampler:
            libkfr.kfr_resample_delete(self.resampler)
            self.resampler = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
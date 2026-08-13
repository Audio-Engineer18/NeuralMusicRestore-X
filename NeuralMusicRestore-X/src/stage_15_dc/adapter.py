"""
Stage 15: DC Offset Removal
-------------------------
Uses Essentia (https://github.com/MTG/essentia) for per-channel DC offset removal.

Dependencies:
- Essentia (https://github.com/MTG/essentia)
"""

import numpy as np
import ctypes
import os
from typing import Optional

# Load libessentia
try:
    libessentia = ctypes.CDLL("libessentia.so")
except OSError:
    raise ImportError(
        "libessentia not found. Install it from: https://github.com/MTG/essentia"
    )

# Define C types and function prototypes
libessentia.essentia_dc_remove_create.argtypes = []
libessentia.essentia_dc_remove_create.restype = ctypes.c_void_p

libessentia.essentia_dc_remove_process.argtypes = [
    ctypes.c_void_p,  # dc remover instance
    ctypes.POINTER(ctypes.c_float),  # input
    ctypes.POINTER(ctypes.c_float),  # output
    ctypes.c_size_t,  # number of samples
    ctypes.c_size_t,  # number of channels
]
libessentia.essentia_dc_remove_process.restype = None

libessentia.essentia_dc_remove_delete.argtypes = [ctypes.c_void_p]
libessentia.essentia_dc_remove_delete.restype = None


class DcAdapter:
    """Python adapter for DC offset removal using Essentia."""

    def __init__(self):
        self.dc_remover = None
        self._create_dc_remover()

    def _create_dc_remover(self):
        """Initialize the DC remover."""
        self.dc_remover = libessentia.essentia_dc_remove_create()
        if not self.dc_remover:
            raise RuntimeError("Failed to create DC remover")

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Remove DC offset from the input audio.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            
        Returns:
            Audio with DC offset removed as a numpy float32 array.
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        output = np.empty_like(audio)
        input_ptr = audio.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        output_ptr = output.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        
        libessentia.essentia_dc_remove_process(
            self.dc_remover, input_ptr, output_ptr, audio.shape[0], audio.shape[1]
        )
        
        return output

    def close(self):
        """Clean up the DC remover."""
        if self.dc_remover:
            libessentia.essentia_dc_remove_delete(self.dc_remover)
            self.dc_remover = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
"""
Stage 14: Dithering
-------------------
Uses SSRC (https://github.com/shibatch/SSRC) for 24-bit quantization dithering.

Dependencies:
- SSRC (https://github.com/shibatch/SSRC)
"""

import ctypes
import numpy as np
import os
from typing import Optional

# Load libssrc
try:
    libssrc = ctypes.CDLL("libssrc.so")
except OSError:
    raise ImportError(
        "libssrc not found. Install it from: https://github.com/shibatch/SSRC"
    )

# Define C types and function prototypes
libssrc.ssrc_init.argtypes = [
    ctypes.c_int,    # sample rate
    ctypes.c_int,    # bits per sample
    ctypes.c_int,    # dither type (0 = none, 1 = rectangular, 2 = triangular)
]
libssrc.ssrc_init.restype = None

libssrc.ssrc_process.argtypes = [
    ctypes.POINTER(ctypes.c_float),  # input
    ctypes.POINTER(ctypes.c_int32),  # output
    ctypes.c_int,                    # number of samples
]
libssrc.ssrc_process.restype = None


class DitherAdapter:
    """Python adapter for dithering using SSRC."""

    def __init__(
        self,
        samplerate: int = 44100,
        bits_per_sample: int = 24,
        dither_type: int = 2,  # Triangular dither
    ):
        self.samplerate = samplerate
        self.bits_per_sample = bits_per_sample
        self.dither_type = dither_type
        self._init_ssrc()

    def _init_ssrc(self):
        """Initialize SSRC for dithering."""
        libssrc.ssrc_init(self.samplerate, self.bits_per_sample, self.dither_type)

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply dithering to the input audio.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            
        Returns:
            Dithered audio as a numpy int32 array.
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Process each channel
        dithered = np.empty_like(audio, dtype=np.int32)
        for channel in range(audio.shape[1]):
            input_ptr = audio[:, channel].ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            output_ptr = dithered[:, channel].ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
            libssrc.ssrc_process(input_ptr, output_ptr, audio.shape[0])
        
        return dithered

    def process_to_float(self, audio: np.ndarray) -> np.ndarray:
        """Apply dithering and convert back to float32.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            
        Returns:
            Dithered audio as a numpy float32 array (normalized to [-1, 1]).
        """
        dithered = self.process(audio)
        return dithered.astype(np.float32) / (2 ** (self.bits_per_sample - 1))
"""
Stage 19: Dynamics Processing
----------------------------
Uses DynamicAudioNormalizer (https://github.com/lordmulder/DynamicAudioNormalizer) for conservative leveling.

Dependencies:
- DynamicAudioNormalizer (https://github.com/lordmulder/DynamicAudioNormalizer)
"""

import ctypes
import numpy as np
import os
from typing import Optional

# Load libDynamicAudioNormalizer
try:
    libdan = ctypes.CDLL("libDynamicAudioNormalizer.so")
except OSError:
    raise ImportError(
        "libDynamicAudioNormalizer not found. Install it from: https://github.com/lordmulder/DynamicAudioNormalizer"
    )

# Define C types and function prototypes
libdan.DynamicAudioNormalizer_init.argtypes = [
    ctypes.c_uint,   # channels
    ctypes.c_uint,   # sample rate
    ctypes.c_uint,   # frame length
    ctypes.c_uint,   # filter size
    ctypes.c_double, # peak value
    ctypes.c_double, # max gain
    ctypes.c_double, # target RMS
    ctypes.c_bool,   # channels coupling
    ctypes.c_bool,   # enable DC correction
]
libdan.DynamicAudioNormalizer_init.restype = ctypes.c_void_p

libdan.DynamicAudioNormalizer_process.argtypes = [
    ctypes.c_void_p,  # instance
    ctypes.POINTER(ctypes.c_double),  # input
    ctypes.POINTER(ctypes.c_double),  # output
    ctypes.c_size_t,  # number of samples
]
libdan.DynamicAudioNormalizer_process.restype = None

libdan.DynamicAudioNormalizer_free.argtypes = [ctypes.c_void_p]
libdan.DynamicAudioNormalizer_free.restype = None


class DynamicsAdapter:
    """Python adapter for dynamics processing using DynamicAudioNormalizer."""

    def __init__(
        self,
        samplerate: int = 44100,
        channels: int = 2,
        frame_length: int = 500,
        filter_size: int = 31,
        peak_value: float = 0.95,
        max_gain: float = 10.0,
        target_rms: float = 0.0,
        channels_coupling: bool = True,
        enable_dc_correction: bool = False,
    ):
        self.samplerate = samplerate
        self.channels = channels
        self.frame_length = frame_length
        self.filter_size = filter_size
        self.peak_value = peak_value
        self.max_gain = max_gain
        self.target_rms = target_rms
        self.channels_coupling = channels_coupling
        self.enable_dc_correction = enable_dc_correction
        self.dan = None
        self._init_dan()

    def _init_dan(self):
        """Initialize the DynamicAudioNormalizer."""
        self.dan = libdan.DynamicAudioNormalizer_init(
            self.channels,
            self.samplerate,
            self.frame_length,
            self.filter_size,
            self.peak_value,
            self.max_gain,
            self.target_rms,
            self.channels_coupling,
            self.enable_dc_correction,
        )
        if not self.dan:
            raise RuntimeError("Failed to initialize DynamicAudioNormalizer")

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply dynamics processing to the input audio.
        
        Args:
            audio: Input audio as a numpy float64 array (shape: [samples, channels]).
            
        Returns:
            Processed audio as a numpy float64 array.
        """
        if audio.dtype != np.float64:
            audio = audio.astype(np.float64)
        
        # Flatten multi-channel audio for processing
        samples = audio.shape[0]
        input_flat = audio.flatten()
        output_flat = np.empty_like(input_flat)
        
        # Process audio
        input_ptr = input_flat.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        output_ptr = output_flat.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        libdan.DynamicAudioNormalizer_process(self.dan, input_ptr, output_ptr, samples)
        
        # Reshape back to multi-channel
        return output_flat.reshape((samples, self.channels))

    def close(self):
        """Clean up the DynamicAudioNormalizer."""
        if self.dan:
            libdan.DynamicAudioNormalizer_free(self.dan)
            self.dan = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
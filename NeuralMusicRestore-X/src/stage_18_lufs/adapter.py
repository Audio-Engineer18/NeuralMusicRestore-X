"""
Stage 18: LUFS Loudness Metering
--------------------------------
Uses libebur128 (https://github.com/jiixyj/libebur128) for EBU R128 loudness metering.

Dependencies:
- libebur128 (https://github.com/jiixyj/libebur128)
"""

import ctypes
import numpy as np
import os
from typing import Optional, Tuple

# Load libebur128
try:
    libebur128 = ctypes.CDLL("libebur128.so")
except OSError:
    raise ImportError(
        "libebur128 not found. Install it from: https://github.com/jiixyj/libebur128"
    )

# Define C types and function prototypes
libebur128.ebur128_init.argtypes = [
    ctypes.c_size_t,  # channels
    ctypes.c_ulong,   # samplerate
    ctypes.c_int,     # mode (EBUR128_MODE_LUFS)
]
libebur128.ebur128_init.restype = ctypes.c_void_p

libebur128.ebur128_add_frames_float.argtypes = [
    ctypes.c_void_p,  # st
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"),  # src
    ctypes.c_size_t,  # frames
]
libebur128.ebur128_add_frames_float.restype = ctypes.c_int

libebur128.ebur128_loudness_global.argtypes = [
    ctypes.c_void_p,  # st
    ctypes.POINTER(ctypes.c_double),  # out
]
libebur128.ebur128_loudness_global.restype = ctypes.c_int

libebur128.ebur128_loudness_momentary.argtypes = [
    ctypes.c_void_p,  # st
    ctypes.POINTER(ctypes.c_double),  # out
]
libebur128.ebur128_loudness_momentary.restype = ctypes.c_int

libebur128.ebur128_loudness_shortterm.argtypes = [
    ctypes.c_void_p,  # st
    ctypes.POINTER(ctypes.c_double),  # out
]
libebur128.ebur128_loudness_shortterm.restype = ctypes.c_int

libebur128.ebur128_destroy.argtypes = [ctypes.c_void_p]
libebur128.ebur128_destroy.restype = None

# Constants
EBUR128_MODE_LUFS = 0


class LufsAdapter:
    """Python adapter for LUFS loudness metering using libebur128."""

    def __init__(self, samplerate: int = 44100, channels: int = 2):
        self.samplerate = samplerate
        self.channels = channels
        self.st = None
        self._init_ebur128()

    def _init_ebur128(self):
        """Initialize the EBU R128 loudness meter."""
        self.st = libebur128.ebur128_init(
            self.channels, self.samplerate, EBUR128_MODE_LUFS
        )
        if not self.st:
            raise RuntimeError("Failed to initialize libebur128")

    def measure_loudness(self, audio: np.ndarray) -> Tuple[float, float, float]:
        """Measure global, momentary, and short-term loudness.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            
        Returns:
            Tuple of (global_lufs, momentary_lufs, shortterm_lufs).
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Add audio frames to the meter
        libebur128.ebur128_add_frames_float(self.st, audio, audio.shape[0])
        
        # Measure loudness
        global_lufs = ctypes.c_double()
        momentary_lufs = ctypes.c_double()
        shortterm_lufs = ctypes.c_double()
        
        libebur128.ebur128_loudness_global(self.st, ctypes.byref(global_lufs))
        libebur128.ebur128_loudness_momentary(self.st, ctypes.byref(momentary_lufs))
        libebur128.ebur128_loudness_shortterm(self.st, ctypes.byref(shortterm_lufs))
        
        return global_lufs.value, momentary_lufs.value, shortterm_lufs.value

    def close(self):
        """Clean up the EBU R128 meter."""
        if self.st:
            libebur128.ebur128_destroy(self.st)
            self.st = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
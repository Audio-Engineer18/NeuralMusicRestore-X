"""
Stage 17: True Peak Detection
---------------------------
Uses libebur128 (https://github.com/jiixyj/libebur128) for oversampled true peak detection.

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
    ctypes.c_int,     # mode (EBUR128_MODE_TRUE_PEAK)
]
libebur128.ebur128_init.restype = ctypes.c_void_p

libebur128.ebur128_add_frames_float.argtypes = [
    ctypes.c_void_p,  # st
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"),  # src
    ctypes.c_size_t,  # frames
]
libebur128.ebur128_add_frames_float.restype = ctypes.c_int

libebur128.ebur128_true_peak.argtypes = [
    ctypes.c_void_p,  # st
    ctypes.c_size_t,  # channel
    ctypes.POINTER(ctypes.c_double),  # out
]
libebur128.ebur128_true_peak.restype = ctypes.c_int

libebur128.ebur128_destroy.argtypes = [ctypes.c_void_p]
libebur128.ebur128_destroy.restype = None

# Constants
EBUR128_MODE_TRUE_PEAK = 256


class TruePeakAdapter:
    """Python adapter for true peak detection using libebur128."""

    def __init__(self, samplerate: int = 44100, channels: int = 2):
        self.samplerate = samplerate
        self.channels = channels
        self.st = None
        self._init_ebur128()

    def _init_ebur128(self):
        """Initialize the EBU R128 true peak detector."""
        self.st = libebur128.ebur128_init(
            self.channels, self.samplerate, EBUR128_MODE_TRUE_PEAK
        )
        if not self.st:
            raise RuntimeError("Failed to initialize libebur128")

    def detect_true_peak(self, audio: np.ndarray) -> Tuple[float, np.ndarray]:
        """Detect true peak values for each channel.
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            
        Returns:
            Tuple of (global_true_peak, per_channel_true_peaks).
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # Add audio frames to the detector
        libebur128.ebur128_add_frames_float(self.st, audio, audio.shape[0])
        
        # Get true peak for each channel
        per_channel_peaks = np.zeros(self.channels, dtype=np.float64)
        for channel in range(self.channels):
            peak = ctypes.c_double()
            libebur128.ebur128_true_peak(self.st, channel, ctypes.byref(peak))
            per_channel_peaks[channel] = peak.value
        
        global_peak = np.max(per_channel_peaks)
        return global_peak, per_channel_peaks

    def close(self):
        """Clean up the EBU R128 detector."""
        if self.st:
            libebur128.ebur128_destroy(self.st)
            self.st = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
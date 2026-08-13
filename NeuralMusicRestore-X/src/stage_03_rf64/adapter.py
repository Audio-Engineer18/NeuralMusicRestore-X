"""
Stage 03: RF64 Validation/Writer
------------------------------
Uses `libsndfile` to validate and write RF64 WAV files (supports >4GB).

Dependencies:
- libsndfile (https://github.com/libsndfile/libsndfile)
"""

import ctypes
import numpy as np
import os
from typing import Optional

# Load libsndfile
try:
    libsndfile = ctypes.CDLL("libsndfile.so.1")
except OSError:
    raise ImportError(
        "libsndfile not found. Install it from: https://github.com/libsndfile/libsndfile"
    )

# Define C types
class SF_INFO(ctypes.Structure):
    _fields_ = [
        ("frames", ctypes.c_int64),
        ("samplerate", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("format", ctypes.c_int),
        ("sections", ctypes.c_int),
        ("seekable", ctypes.c_int),
    ]

# Define function prototypes
libsndfile.sf_open.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(SF_INFO)]
libsndfile.sf_open.restype = ctypes.c_void_p

libsndfile.sf_command.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
libsndfile.sf_command.restype = ctypes.c_int

libsndfile.sf_writef_float.argtypes = [
    ctypes.c_void_p, 
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"), 
    ctypes.c_int64,
]
libsndfile.sf_writef_float.restype = ctypes.c_int64

libsndfile.sf_close.argtypes = [ctypes.c_void_p]
libsndfile.sf_close.restype = ctypes.c_int

# Constants
SFM_RDWR = 0x13
SF_FORMAT_RF64 = 0x00100000
SF_COMMAND_SET_RF64_MODE = 0x10C0


class RF64Adapter:
    """Python adapter for RF64 WAV files using libsndfile."""

    def __init__(self, filepath: str, mode: str = "w", samplerate: int = 44100, channels: int = 2):
        self.filepath = filepath
        self.mode = mode
        self.samplerate = samplerate
        self.channels = channels
        self.sf_info = SF_INFO()
        self.file = None
        
        self._open()

    def _open(self):
        """Open the RF64 file."""
        if self.mode == "w":
            self.sf_info.format = SF_FORMAT_RF64 | 0x0006  # RF64 + WAV + FLOAT
            self.sf_info.samplerate = self.samplerate
            self.sf_info.channels = self.channels
            self.file = libsndfile.sf_open(
                self.filepath.encode("utf-8"), SFM_RDWR, ctypes.byref(self.sf_info)
            )
            # Enable RF64 mode
            libsndfile.sf_command(self.file, SF_COMMAND_SET_RF64_MODE, None, 1)
        else:
            raise ValueError("Only write mode is supported for RF64.")
        
        if not self.file:
            raise IOError(f"Failed to open {self.filepath}")

    def write(self, data: np.ndarray):
        """Write audio data to the RF64 file."""
        if data.dtype != np.float32:
            data = data.astype(np.float32)
        libsndfile.sf_writef_float(self.file, data, data.shape[0])

    def close(self):
        """Close the file."""
        if self.file:
            libsndfile.sf_close(self.file)
            self.file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def validate_rf64(filepath: str) -> bool:
        """Validate if a file is in RF64 format."""
        sf_info = SF_INFO()
        file = libsndfile.sf_open(filepath.encode("utf-8"), 0x10, ctypes.byref(sf_info))
        if not file:
            return False
        
        is_rf64 = (sf_info.format & SF_FORMAT_RF64) == SF_FORMAT_RF64
        libsndfile.sf_close(file)
        return is_rf64
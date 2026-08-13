"""
Stage 01: WAV/PCM Adapter
------------------------
Uses `libsndfile` to read/write WAV/PCM files.

Dependencies:
- libsndfile (https://github.com/libsndfile/libsndfile)
"""

import ctypes
import numpy as np
import os

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

libsndfile.sf_readf_float.argtypes = [
    ctypes.c_void_p, 
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"), 
    ctypes.c_int64,
]
libsndfile.sf_readf_float.restype = ctypes.c_int64

libsndfile.sf_writef_float.argtypes = [
    ctypes.c_void_p, 
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"), 
    ctypes.c_int64,
]
libsndfile.sf_writef_float.restype = ctypes.c_int64

libsndfile.sf_close.argtypes = [ctypes.c_void_p]
libsndfile.sf_close.restype = ctypes.c_int


class WavAdapter:
    """Python adapter for libsndfile."""

    def __init__(self, filepath: str, mode: str = "r"):
        self.filepath = filepath
        self.mode = mode
        self.sf_info = SF_INFO()
        self.file = None
        
        self._open()

    def _open(self):
        """Open the WAV file."""
        mode_map = {"r": 0x10, "w": 0x20, "r+": 0x30}
        self.file = libsndfile.sf_open(
            self.filepath.encode("utf-8"), mode_map[self.mode], ctypes.byref(self.sf_info)
        )
        if not self.file:
            raise IOError(f"Failed to open {self.filepath}")

    def read(self, frames: int = -1) -> np.ndarray:
        """Read audio data as float32 numpy array."""
        if frames == -1:
            frames = self.sf_info.frames
        
        buffer = np.empty((frames, self.sf_info.channels), dtype=np.float32)
        read_frames = libsndfile.sf_readf_float(self.file, buffer, frames)
        return buffer[:read_frames]

    def write(self, data: np.ndarray):
        """Write audio data."""
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

    @property
    def samplerate(self) -> int:
        return self.sf_info.samplerate

    @property
    def channels(self) -> int:
        return self.sf_info.channels

    @property
    def duration(self) -> float:
        return self.sf_info.frames / self.sf_info.samplerate
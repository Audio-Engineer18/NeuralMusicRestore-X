"""
Stage 08: Sample Rate Conversion (SRC) Verification
-----------------------------------------------
Uses `soxr` to verify the accuracy of sample rate conversion.

Dependencies:
- soxr (https://github.com/chirlu/soxr)
"""

import ctypes
import numpy as np
import os
from typing import Optional, Tuple

# Load libsoxr
try:
    libsoxr = ctypes.CDLL("libsoxr.so.0")
except OSError:
    raise ImportError(
        "libsoxr not found. Install it from: https://github.com/chirlu/soxr"
    )

# Define C types
soxr_error_t = ctypes.c_char_p
soxr_io_spec_t = ctypes.c_void_p
soxr_quality_spec_t = ctypes.c_void_p
soxr_runtime_spec_t = ctypes.c_void_p

# Define function prototypes
libsoxr.soxr_create.argtypes = [
    ctypes.c_double,  # input rate
    ctypes.c_double,  # output rate
    ctypes.c_uint,    # num channels
    ctypes.POINTER(soxr_error_t),  # error
    ctypes.POINTER(soxr_io_spec_t),  # io spec
    ctypes.POINTER(soxr_quality_spec_t),  # quality spec
    ctypes.POINTER(soxr_runtime_spec_t),  # runtime spec
]
libsoxr.soxr_create.restype = ctypes.c_void_p

libsoxr.soxr_process.argtypes = [
    ctypes.c_void_p,  # soxr instance
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"),  # input
    ctypes.c_size_t,  # input length
    ctypes.POINTER(ctypes.c_size_t),  # input used
    np.ctypeslib.ndpointer(dtype=np.float32, flags="C_CONTIGUOUS"),  # output
    ctypes.c_size_t,  # output length
    ctypes.POINTER(ctypes.c_size_t),  # output used
]
libsoxr.soxr_process.restype = soxr_error_t

libsoxr.soxr_delete.argtypes = [ctypes.c_void_p]
libsoxr.soxr_delete.restype = None

libsoxr.soxr_quality_spec.argtypes = [ctypes.c_uint, ctypes.c_uint]
libsoxr.soxr_quality_spec.restype = soxr_quality_spec_t

# Quality presets
SOXR_QQ = 0  # Quick
SOXR_LQ = 1  # Low
SOXR_MQ = 2  # Medium
SOXR_HQ = 3  # High
SOXR_VHQ = 4  # Very High


class SrcVerifyAdapter:
    """Python adapter for verifying sample rate conversion using soxr."""

    def __init__(
        self,
        input_rate: float,
        output_rate: float,
        channels: int = 2,
        quality: int = SOXR_VHQ,
    ):
        self.input_rate = input_rate
        self.output_rate = output_rate
        self.channels = channels
        self.quality = quality
        self.soxr = None
        self._create_soxr()

    def _create_soxr(self):
        """Initialize the soxr instance."""
        error = soxr_error_t()
        quality_spec = libsoxr.soxr_quality_spec(self.quality, 0)
        
        self.soxr = libsoxr.soxr_create(
            self.input_rate,
            self.output_rate,
            self.channels,
            ctypes.byref(error),
            None,  # io spec
            ctypes.byref(quality_spec),  # quality spec
            None,  # runtime spec
        )
        
        if error.value:
            raise RuntimeError(f"soxr error: {error.value.decode('utf-8')}")

    def verify_src(
        self,
        original_audio: np.ndarray,
        resampled_audio: np.ndarray,
        tolerance: float = 1e-3,
    ) -> bool:
        """Verify if resampled audio matches the expected output.
        
        Args:
            original_audio: Original audio (float32).
            resampled_audio: Resampled audio (float32).
            tolerance: Allowed error tolerance.
            
        Returns:
            True if the resampled audio is accurate.
        """
        # Resample the original audio using soxr
        expected_audio = self.process(original_audio)
        
        # Compare the resampled audio with the expected output
        if resampled_audio.shape != expected_audio.shape:
            return False
        
        return np.allclose(resampled_audio, expected_audio, atol=tolerance)

    def process(self, audio: np.ndarray) -> np.ndarray:
        """Resample audio using soxr (for verification).
        
        Args:
            audio: Input audio as a numpy float32 array (shape: [samples, channels]).
            
        Returns:
            Resampled audio as a numpy float32 array.
        """
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        input_samples = audio.shape[0]
        output_samples = int(input_samples * self.output_rate / self.input_rate) + 10
        
        output = np.empty((output_samples, self.channels), dtype=np.float32)
        input_used = ctypes.c_size_t()
        output_used = ctypes.c_size_t()
        
        error = libsoxr.soxr_process(
            self.soxr,
            audio,
            input_samples,
            ctypes.byref(input_used),
            output,
            output_samples,
            ctypes.byref(output_used),
        )
        
        if error:
            raise RuntimeError(f"soxr processing error: {error.decode('utf-8')}")
        
        return output[:output_used.value]

    def close(self):
        """Clean up the soxr instance."""
        if self.soxr:
            libsoxr.soxr_delete(self.soxr)
            self.soxr = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
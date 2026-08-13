"""
Stage 06: FLAC Archive + Verification
-----------------------------------
Uses `libFLAC` to encode, decode, and verify FLAC files.

Dependencies:
- libFLAC (https://github.com/xiph/flac)
"""

import ctypes
import numpy as np
import os
from typing import Optional, Tuple

# Load libFLAC
try:
    libflac = ctypes.CDLL("libFLAC.so.8")
except OSError:
    raise ImportError(
        "libFLAC not found. Install it from: https://github.com/xiph/flac"
    )

# Define C types and constants
FLAC__StreamEncoderInitStatus = ctypes.c_int
FLAC__STREAM_ENCODER_INIT_STATUS_OK = 0
FLAC__STREAM_ENCODER_WRITE_STATUS_OK = 0
FLAC__StreamDecoderInitStatus = ctypes.c_int
FLAC__STREAM_DECODER_INIT_STATUS_OK = 0
FLAC__STREAM_DECODER_READ_STATUS_CONTINUE = 0
FLAC__STREAM_DECODER_WRITE_STATUS_CONTINUE = 0
FLAC__STREAM_DECODER_END_OF_STREAM = 1

# Callback types
FLAC__StreamEncoderWriteCallback = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p
)
FLAC__StreamDecoderWriteCallback = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)), ctypes.c_void_p
)
FLAC__StreamDecoderMetadataCallback = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
)
FLAC__StreamDecoderErrorCallback = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p
)


class FLACAdapter:
    """Python adapter for FLAC encoding, decoding, and verification."""

    def __init__(self):
        self.encoder = None
        self.decoder = None
        self._buffer = []
        self._init_encoder()
        self._init_decoder()

    def _init_encoder(self):
        """Initialize the FLAC encoder."""
        self.encoder = libflac.FLAC__stream_encoder_new()
        if not self.encoder:
            raise RuntimeError("Failed to create FLAC encoder")

    def _init_decoder(self):
        """Initialize the FLAC decoder."""
        self.decoder = libflac.FLAC__stream_decoder_new()
        if not self.decoder:
            raise RuntimeError("Failed to create FLAC decoder")

    def encode_to_flac(
        self,
        input_file: str,
        output_file: str,
        samplerate: int = 44100,
        channels: int = 2,
        bits_per_sample: int = 16,
    ) -> bool:
        """Encode a WAV file to FLAC.
        
        Args:
            input_file: Path to the input WAV file.
            output_file: Path to the output FLAC file.
            samplerate: Sample rate (Hz).
            channels: Number of channels.
            bits_per_sample: Bit depth (e.g., 16, 24).
            
        Returns:
            True if encoding succeeded.
        """
        # Set encoder parameters
        libflac.FLAC__stream_encoder_set_verify(self.encoder, True)
        libflac.FLAC__stream_encoder_set_compression_level(self.encoder, 5)
        libflac.FLAC__stream_encoder_set_channels(self.encoder, channels)
        libflac.FLAC__stream_encoder_set_bits_per_sample(self.encoder, bits_per_sample)
        libflac.FLAC__stream_encoder_set_sample_rate(self.encoder, samplerate)
        
        # Initialize encoder
        init_status = libflac.FLAC__stream_encoder_init_file(
            self.encoder, output_file.encode("utf-8"), None, None
        )
        if init_status != FLAC__STREAM_ENCODER_INIT_STATUS_OK:
            raise RuntimeError(f"Failed to initialize FLAC encoder: {init_status}")
        
        # Read WAV file and encode
        from stage_01_wav_pcm.adapter import WavAdapter
        with WavAdapter(input_file, "r") as wav:
            audio = wav.read()
            audio_int = (audio * 32767).astype(np.int16)  # Convert to 16-bit PCM
            
            # Process audio in chunks
            chunk_size = 4096
            for i in range(0, len(audio_int), chunk_size):
                chunk = audio_int[i:i + chunk_size]
                libflac.FLAC__stream_encoder_process_interleaved(
                    self.encoder, chunk.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), len(chunk)
                )
        
        # Finish encoding
        libflac.FLAC__stream_encoder_finish(self.encoder)
        return True

    def decode_to_wav(self, input_file: str, output_file: str) -> bool:
        """Decode a FLAC file to WAV.
        
        Args:
            input_file: Path to the input FLAC file.
            output_file: Path to the output WAV file.
            
        Returns:
            True if decoding succeeded.
        """
        # Initialize decoder
        init_status = libflac.FLAC__stream_decoder_init_file(
            self.decoder, input_file.encode("utf-8"), None, None, None, None
        )
        if init_status != FLAC__STREAM_DECODER_INIT_STATUS_OK:
            raise RuntimeError(f"Failed to initialize FLAC decoder: {init_status}")
        
        # Start decoding
        libflac.FLAC__stream_decoder_process_until_end_of_stream(self.decoder)
        
        # Write decoded audio to WAV
        from stage_01_wav_pcm.adapter import WavAdapter
        with WavAdapter(output_file, "w") as wav:
            audio = np.concatenate(self._buffer, axis=0)
            wav.write(audio)
        
        self._buffer.clear()
        return True

    def verify_flac(self, input_file: str) -> bool:
        """Verify the integrity of a FLAC file.
        
        Args:
            input_file: Path to the input FLAC file.
            
        Returns:
            True if the file is valid.
        """
        # Initialize decoder with verify mode
        init_status = libflac.FLAC__stream_decoder_init_file(
            self.decoder, input_file.encode("utf-8"), None, None, None, None
        )
        if init_status != FLAC__STREAM_DECODER_INIT_STATUS_OK:
            return False
        
        # Verify the file
        result = libflac.FLAC__stream_decoder_process_until_end_of_stream(self.decoder)
        libflac.FLAC__stream_decoder_finish(self.decoder)
        return result

    def __del__(self):
        """Clean up encoder and decoder."""
        if self.encoder:
            libflac.FLAC__stream_encoder_delete(self.encoder)
        if self.decoder:
            libflac.FLAC__stream_decoder_delete(self.decoder)
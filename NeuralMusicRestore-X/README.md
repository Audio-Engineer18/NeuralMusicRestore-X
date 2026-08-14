# NeuralMusicRestore-X

A 27-stage pipeline for **immersive music audio restoration** and enhancement.

---

## Stages
| Stage | Description                          | Status |
|-------|--------------------------------------|--------|
| 01    | WAV/PCM (libsndfile)                 | ✅     |
| 02    | WavPack (wvunpack)                   | ✅     |
| 03    | RF64 (libsndfile)                    | ✅     |
| 04    | VHQ SRC (soxr)                       | ✅     |
| 05    | Channels (FFmpeg)                    | ✅     |
| 06    | FLAC (xiph/flac)                     | ✅     |
| 07    | Float64 (numpy)                      | ✅     |
| 08    | SRC Verify (soxr)                    | ✅     |
| 09    | Advanced SRC (KFR)                   | ✅     |
| 10    | Subsonic (iir1)                      | ✅     |
| 11    | Linear FIR (scipy)                   | ✅     |
| 12    | Hum (iir1)                           | ✅     |
| 13    | Denoise (DeepFilterNet)              | ✅     |
| 14    | Dither (SSRC)                        | ✅     |
| 15    | DC (essentia)                        | ✅     |
| 16    | Repair (FFmpeg)                      | ✅     |
| 17    | True Peak (libebur128)               | ✅     |
| 18    | LUFS (libebur128)                    | ✅     |
| 19    | Dynamics (DynamicAudioNormalizer)    | ✅     |
| 20    | Silence (silan)                      | ✅     |
| 21    | Super-Resolution (VASR)              | ✅     |
| 22    | Enhancement (Resemble Enhance)       | ✅     |
| 23    | Music Restoration (Apollo)           | ✅     |
| 24    | Vocal Restoration (SGMSE)            | ✅     |
| 25    | Ingest/Demux (FFmpeg)                | ✅     |
| 26    | Metadata (mutagen)                   | ✅     |
| 27    | Artwork (exiftool)                   | ✅     |

---

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Audio-Engineer18/NeuralMusicRestore-X.git
   cd NeuralMusicRestore-X
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install system dependencies:
   ```bash
   # For Stage 01 (libsndfile)
   sudo apt-get install libsndfile1
   
   # For Stage 02 (WavPack)
   sudo apt-get install wavpack
   
   # For Stage 04 (VHQ SRC)
   sudo apt-get install libsoxr0
   
   # For Stage 08 (SRC Verify)
   sudo apt-get install libsoxr0
   
   # For Stage 05 (FFmpeg), Stage 16 (Repair), and Stage 25 (Ingest/Demux)
   sudo apt-get install ffmpeg
   
   # For Stage 06 (FLAC)
   sudo apt-get install libflac8
   
   # For Stage 07 (Float64)
   # No system dependencies (pure Python/numpy)
   
   # For Stage 09 (KFR)
   sudo apt-get install libkfr-dev
   
   # For Stage 10 (Subsonic)
   sudo apt-get install libiir1
   
   # For Stage 11 (Linear FIR)
   # No system dependencies (pure Python/scipy)
   
   # For Stage 12 (Hum)
   sudo apt-get install libiir1
   
   # For Stage 13 (Denoise)
   # No system dependencies (pure Python/DeepFilterNet)
   
   # For Stage 14 (Dither)
   sudo apt-get install libssrc
   
   # For Stage 15 (DC)
   sudo apt-get install libessentia2v5
   
   # For Stage 17 (True Peak)
   sudo apt-get install libebur128-dev
   
   # For Stage 18 (LUFS)
   sudo apt-get install libebur128-dev
   
   # For Stage 19 (Dynamics)
   sudo apt-get install libdynamicaudionormalizer
   
   # For Stage 20 (Silence)
   sudo apt-get install silan
   
   # For Stage 21 (Super-Resolution)
   # No system dependencies (pure Python/VASR)
   
   # For Stage 22 (Enhancement)
   # No system dependencies (pure Python/Resemble Enhance)
   
   # For Stage 23 (Music Restoration)
   # No system dependencies (pure Python/Apollo)
   
   # For Stage 24 (Vocal Restoration)
   # No system dependencies (pure Python/SGMSE)
   
   # For Stage 26 (Metadata)
   # No system dependencies (pure Python/mutagen)
   
   # For Stage 27 (Artwork)
   sudo apt-get install exiftool
   ```
4. Build C/C++ dependencies:
   ```bash
   mkdir build && cd build
   cmake ..
   make
   ```
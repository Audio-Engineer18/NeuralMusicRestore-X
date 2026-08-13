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
| 06    | FLAC (xiph/flac)                     | ⏳     |
| ...   | ...                                  | ...    |

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
   
   # For Stage 04 (soxr)
   sudo apt-get install libsoxr0
   
   # For Stage 05 (FFmpeg)
   sudo apt-get install ffmpeg
   ```
4. Build C/C++ dependencies:
   ```bash
   mkdir build && cd build
   cmake ..
   make
   ```
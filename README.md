# Blob Tracking with Python
A Python tool that applies a popular **blob tracking effect** on videos using OpenCV.  
It detects moving objects as blobs, draws bounding boxes around them, and connects these blobs with dynamic tracking lines — creating an engaging visual trace of movement over time.

> [!WARNING]  
> This script is far from perfect, results may vary. Feel free to contribute in order to make it better!

## Features
- Tracks moving objects using background subtraction
- Draws bounding boxes around detected blobs
- Optional pixelation effect inside each bounding box
- Displays coordinates for tracked objects
- Connects objects with:
  - Motion tracking lines between frames
  - Web-style connection lines within the same frame
- Adjustable sensitivity levels: low, medium, high
- Merges the original audio back into the processed video using FFmpeg

## Requirements
- Python 3
- OpenCV
- NumPy
- FFmpeg (must be installed and available in your system’s PATH)

Install Python dependencies with:
```bash
pip install opencv-python numpy
```
Make sure FFmpeg is installed:
```bash
ffmpeg -version
```
If not installed, get it from your distro's official repository. For windows users, try [ffmpeg.org](https://ffmpeg.org/)

## Usage

Run the script:
```bash
python3 motion_tracker.py
```

You'll be prompted for the following (with defaults):
| Parameter                                  | Default      | Description                                                         |
| ------------------------------------------ | ------------ | ------------------------------------------------------------------- |
| Input video filename                       | `input.mp4`  | Path to input video                                                 |
| Output video filename                      | `output.mp4` | Output video path                                                   |
| Max boxes per frame                        | 20           | Max detected blobs per frame                                        |
| Max trace length (frames to track)         | 30           | History length for drawing motion lines                             |
| Max total connection lines per frame       | 5            | Number of connection lines to draw (0 = disable)                    |
| Max pixel jump distance for tracking lines | 20           | Max distance for linking blobs across frames                        |
| Box thickness                              | 1            | Thickness of bounding boxes                                         |
| Line thickness                             | 1            | Thickness of lines between blobs                                    |
| Font scale                                 | 0.5          | Size of text showing coordinates                                    |
| Font thickness                             | 1            | Thickness of coordinate text                                        |
| Show coordinates on boxes?                 | Yes          | Display (x, y) coordinates above each blob                          |
| Enable pixelation effect inside boxes?     | Yes          | Replace region inside boxes with pixelated version                  |
| Pixelation block size                      | 10           | Size of each pixel block in pixelation                              |
| Max box width/height for pixelation        | 100          | Only pixelate boxes smaller than this (0 = no size limit)           |
| Detection sensitivity                      | Medium       | Affects how aggressively the background subtractor detects movement |

### Files
- `motion_tracker.py`: Main script
- `temp_video.mp4`: Temporary output (auto-deleted)
- `output.mp4`: Final video with audio (default name unless changed)

### Tips

- Set `Max total connection lines per frame` to `0` to disable lines entirely.
- Reduce `Max boxes per frame` to improve performance.
- High-contrast, low-motion background videos yield better results.
- "High" sensitivity works well for detecting subtle or fast motion, while "Low" helps reduce noise in stable scenes.

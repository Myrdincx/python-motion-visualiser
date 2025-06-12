# Blob Tracking with Python
A Python tool that applies a popular **blob tracking effect** on videos using OpenCV.  
It detects moving objects as blobs, draws bounding boxes around them, and connects these blobs with dynamic tracking lines — creating an engaging visual trace of movement over time.

> [!WARNING]  
> This script is far from perfect, results may vary. Feel free to contribute in order to make it better!

## Features
- Tracks moving objects using background subtraction
- Draws bounding boxes for the most prominent moving objects
- Optionally draws lines between detected objects to illustrate motion or relationships:
  - Web-like random lines (between objects in the same frame)
- Merges original audio back into the processed video using FFmpeg.

## Requirements
- Python 3
- OpenCV
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
| Parameter                                 | Default      | Description                                     |
| ----------------------------------------- | ------------ | ----------------------------------------------- |
| Input video filename                      | `input.mp4`  | Video to process                                |
| Output video filename                     | `output.mp4` | Result video filename                           |
| Max boxes per frame                       | `20`         | Maximum detected blobs shown per frame          |
| Max trace length (frames to track motion) | `30`         | Number of frames to remember for tracking lines |
| Max total connection lines per frame      | `5`          | Set to `0` to disable lines                     |
| Max jump distance (pixels)                | `20`         | Maximum distance to link blobs between frames   |
| Box thickness                             | `1`          | Thickness of bounding boxes                     |
| Line thickness                            | `1`          | Thickness of connecting lines                   |
| Font scale                                | `0.5`        | Scale of coordinate text                        |
| Font thickness                            | `1`          | Thickness of coordinate text                    |
| Show coordinates on boxes?                | `Yes`        | Toggle coordinate display above bounding boxes  |


### Files
- `motion_tracker.py`: Main script
- `temp_video.mp4`: Temporary output (auto-deleted)
- `output.mp4`: Final video with audio (default name unless changed)

### Tips

- To completely disable drawing lines, just set:
```lua
Max total connection lines per frame: 0
```
- For faster rendering, reduce `Max boxes per frame`.
- Works best with high-contrast, stable background videos.

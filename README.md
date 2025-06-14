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
- OpenCV (see below)
- NumPy (see below)
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
| Parameter                                  | Default      | Description                                                                             |
| ------------------------------------------ | ------------ | --------------------------------------------------------------------------------------- |
| Input video filename                       | `input.mp4`  | Video file to process                                                                   |
| Output video filename                      | `output.mp4` | Output video file name                                                                  |
| Max boxes per frame                        | 20           | Maximum number of detected boxes per frame                                              |
| Max trace length (frames to track)         | 30           | How many frames to keep trace history                                                   |
| Max total connection lines per frame       | 5            | Number of lines to draw connecting detected boxes (0 disables lines)                    |
| Max pixel jump distance for tracking lines | 20           | Maximum pixel distance for connecting tracked objects                                   |
| Max box width/height to display            | 200          | Maximum box size (width or height) to show; bigger boxes are ignored (0 disables limit) |
| Box thickness                              | 1            | Thickness of bounding box lines                                                         |
| Line thickness                             | 1            | Thickness of tracking and web connection lines                                          |
| Font scale                                 | 0.5          | Scale of coordinate text                                                                |
| Font thickness                             | 1            | Thickness of coordinate text                                                            |
| Show coordinates on boxes?                 | Yes          | Whether to display coordinates above bounding boxes                                     |
| Enable pixelation effect inside boxes?     | Yes          | Pixelation is enabled by default                                                        |
| Pixelation block size                      | 10           | Size of pixel blocks when pixelation is enabled                                         |
| Max box width/height for pixelation        | 100          | Pixelation applies only to boxes smaller or equal to this size (0 disables size limit)  |


### Files
- `motion_tracker.py`: Main script
- `temp_video.mp4`: Temporary output (auto-deleted)
- `output.mp4`: Final video with audio (default name unless changed)

### Tips

- Set `Max total connection lines per frame` to `0` to disable lines entirely.
- Reduce `Max boxes per frame` to improve performance.
- High-contrast, low-motion background videos yield better results.
- "High" sensitivity works well for detecting subtle or fast motion, while "Low" helps reduce noise in stable scenes.

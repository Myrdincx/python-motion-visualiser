# Blob Tracking with Python
This Python script analyzes motion in a video, draws bounding boxes around moving objects, optionally connects them with lines, and exports a new video with the original audio.

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
- Input video filename (default: input.mp4)
- Output video filename (default: output.mp4)
- Max boxes per frame (default: 20)
- Max trace length (how many frames to track past motion, default: 30)
- Max total connection lines per frame (set to 0 to disable lines)
- Max jump distance (controls how far objects can move and still be linked, default: 20 pixels)

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

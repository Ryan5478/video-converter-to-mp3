# Video → MP3 Converter

A simple GUI app that converts video files to MP3 using FFmpeg.

## Features
- Clean Tkinter GUI
- Three quality presets (Fast / Balanced / Best)
- Multi-threaded encoding (uses all CPU cores)
- Works with MP4, AVI, MKV, MOV, FLV, WEBM, WMV, M4V

## Requirements
- Python 3.10+
- FFmpeg installed

## Setup

1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
   (`ffmpeg-release-full.zip`).
2. Extract it somewhere, e.g. `C:\ffmpeg-9.0.2-full_build\`.
3. Edit `main.py` and set the `FFMPEG` path to match your install:
   ```python
   FFMPEG = r"C:\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
   ```

## Run

```bash
python main.py
```

## Build a standalone .exe

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "Video to MP3" main.py
```

The app will be in `dist/Video to MP3.exe`.

## License

MIT
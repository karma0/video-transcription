# Video Transcription Tool

Generate SRT subtitle files from video files using OpenAI's Whisper model for local, offline transcription.

## Features

- **Local transcription** - No API calls or internet connection required
- **Multiple video formats** - Supports MP4, AVI, MOV, MKV, WebM, and more
- **Multiple Whisper models** - Choose from tiny to large models based on your needs
- **Language support** - Auto-detect or specify language for transcription
- **GPU acceleration** - Automatic CUDA support for faster processing
- **Clean SRT output** - Properly formatted subtitle files

## Installation

This project uses `uv` for dependency management. First, install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then clone the repository and install dependencies:

```bash
git clone <repository-url>
cd video-transcription
uv sync
```

You'll also need FFmpeg installed on your system:

- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt update && sudo apt install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Basic Usage

```bash
uv run video-transcribe video.mp4
```

This will create `video.srt` in the same directory as the input video.

### Specify Output File

```bash
uv run video-transcribe video.mp4 -o subtitles.srt
```

### Choose Model Size

Available models: `tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`

```bash
# Faster but less accurate
uv run video-transcribe video.mp4 --model tiny

# Slower but more accurate
uv run video-transcribe video.mp4 --model large
```

### Specify Language

```bash
# English
uv run video-transcribe video.mp4 --language en

# Spanish
uv run video-transcribe video.mp4 --language es

# Auto-detect (default)
uv run video-transcribe video.mp4
```

### Other Options

```bash
# Use CPU instead of GPU
uv run video-transcribe video.mp4 --device cpu

# Enable verbose output
uv run video-transcribe video.mp4 --verbose

# See all options
uv run video-transcribe --help
```

## Model Selection Guide

| Model    | Speed      | Accuracy | VRAM Required | Use Case                        |
|----------|------------|----------|---------------|---------------------------------|
| tiny     | Fastest    | Low      | ~1 GB         | Quick drafts, short videos      |
| base     | Fast       | Good     | ~1 GB         | General use (default)           |
| small    | Moderate   | Better   | ~2 GB         | Better accuracy, moderate speed |
| medium   | Slow       | High     | ~5 GB         | High accuracy needed            |
| large    | Slowest    | Best     | ~10 GB        | Maximum accuracy                |

## Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WebM (.webm)
- FLV (.flv)
- WMV (.wmv)
- MPEG (.mpg, .mpeg)
- 3GP (.3gp)
- OGV (.ogv)
- TS (.ts, .mts)

## Performance Tips

1. **Use GPU acceleration**: The tool automatically uses CUDA if available
2. **Choose appropriate model**: Balance speed vs accuracy for your needs
3. **Process in batches**: For multiple videos, consider using smaller models
4. **Close other applications**: Whisper models can be memory-intensive

## Troubleshooting

### "FFmpeg not found" error
Make sure FFmpeg is installed and in your PATH.

### Out of memory errors
Try using a smaller model or the `--device cpu` flag.

### Poor transcription quality
- Try a larger model
- Ensure good audio quality in the source video
- Specify the language instead of using auto-detection

## License

This project is open source and available under the MIT License.
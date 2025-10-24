# VoiceMeet-Sum

A desktop application for transcribing video and audio files using OpenAI's Whisper API.

## Features

- **Video/Audio Support**: Extract audio from video files (.mp4, .mov, .mkv, .avi) or use audio files directly (.mp3, .wav, .m4a, .flac)
- **GPU Acceleration**: Automatically uses CUDA acceleration if available for faster audio extraction
- **OpenAI Whisper API**: High-quality transcription powered by OpenAI's Whisper model
- **Secure API Key Storage**: API key is stored locally in `config.json` and never sent anywhere else
- **Progress Tracking**: Real-time progress updates during extraction and transcription
- **Export Functionality**: Save transcriptions as `.txt` files
- **Error Handling**: Graceful error handling for network issues, invalid API keys, and unsupported files

## Requirements

- Python 3.10 or higher
- FFmpeg (must be installed separately)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) or use chocolatey:
```bash
choco install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg      # CentOS/RHEL
```

## Installation

1. Clone or download this repository
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter your OpenAI API key in the input field
3. Click "Browse" to select a video or audio file
4. Click "Start Transcription" to begin the process
5. Wait for the transcription to complete
6. Click "Save as .txt" to export the transcription

## Configuration

The application automatically creates a `config.json` file to store your API key locally. When you close the application, you'll be asked if you want to save your API key for next time.

**Note**: The API key is stored locally and never sent anywhere except to OpenAI's API.

## Building Standalone Executable

To create a standalone `.exe` file (Windows) or `.app` (macOS) using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name VoiceMeet-Sum main.py
```

The executable will be created in the `dist` folder.

## Troubleshooting

### FFmpeg not found
Make sure FFmpeg is installed and available in your system PATH. You can verify by running:
```bash
ffmpeg -version
```

### API Key errors
- Ensure your OpenAI API key is valid and has sufficient credits
- Check your internet connection
- Verify that the API key has access to the Whisper API

### GPU Acceleration
If you have an NVIDIA GPU with CUDA installed, the application will automatically use GPU acceleration for faster audio extraction. This requires:
- NVIDIA GPU with CUDA support
- CUDA drivers installed
- FFmpeg compiled with CUDA support

## License

This project is provided as-is for personal and educational use.

## Disclaimer

This application uses OpenAI's API, which may incur costs based on your usage. Please review OpenAI's pricing before use.


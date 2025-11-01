# Developer Guide

## 🏗️ Architecture Overview

Voicemeet_sum follows a modular pipeline architecture:

```
Audio File
    ↓
Audio Processor (FFmpeg) → Preprocessed WAV
    ↓
Whisper Service → Transcript
    ↓
Text Processor → Chunks (if needed)
    ↓
Qwen Service → Summary
    ↓
File Handler → Output files
```

## 📦 Core Components

### 1. Configuration (`config/settings.py`)

Central configuration using dataclasses:

```python
from config import TRANSCRIPTION, SUMMARIZATION, FFMPEG, APP
```

### 2. Utils (`src/utils/`)

**logger.py**: Logging utility
```python
from src.utils.logger import setup_logger, logger
logger.info("Message")
```

**file_handler.py**: File operations
```python
from src.utils.file_handler import (
    ensure_dir, save_text_file, get_file_size
)
```

**system_checker.py**: System checks
```python
from src.utils.system_checker import check_system_resources
```

**text_processor.py**: Text processing
```python
from src.utils.text_processor import chunk_text, clean_text
```

### 3. Audio Processing (`src/transcription/audio_processor.py`)

FFmpeg wrapper for preprocessing:

```python
from src.transcription.audio_processor import AudioProcessor

processor = AudioProcessor(config=FFMPEG)
output_path = processor.preprocess(input_path)
```

Features:
- Resample to 16kHz
- Convert to mono
- Normalize volume
- Remove silence

### 4. Transcription (`src/transcription/whisper_service.py`)

Faster-Whisper integration:

```python
from src.transcription.whisper_service import WhisperService

service = WhisperService(config=TRANSCRIPTION)
service.load_model()
transcript = service.transcribe(audio_path)
```

Supported models:
- `tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3`

### 5. Summarization (`src/summarization/qwen_service.py`)

Qwen via Ollama:

```python
from src.summarization.qwen_service import QwenService

service = QwenService(config=SUMMARIZATION)
summary = service.summarize(transcript)
```

### 6. Pipeline (`src/pipeline/meeting_pipeline.py`)

Main orchestration:

```python
from src.pipeline.meeting_pipeline import MeetingPipeline

pipeline = MeetingPipeline()
transcript_path, summary_path = pipeline.process(audio_file)
```

## 🔌 Extending the Pipeline

### Adding a New Model

1. Create service in appropriate module
2. Implement interface:
```python
class NewService:
    def __init__(self, config):
        pass
    
    def process(self, input):
        pass
```

3. Add to pipeline:
```python
class MeetingPipeline:
    def __init__(self):
        self.new_service = NewService()
```

### Adding a New Preprocessing Step

Edit `audio_processor.py`:

```python
def _build_ffmpeg_command(self, input_path, output_path):
    filters.append('new_filter=params')
```

### Custom Summarization Prompt

Edit `qwen_service.py`:

```python
def _build_summary_prompt(self, text, style="complete"):
    prompt = "Your custom prompt here..."
    return prompt
```

## 🧪 Testing

### Unit Tests

```python
import pytest
from src.transcription.whisper_service import WhisperService

def test_whisper_transcribe():
    service = WhisperService()
    # Test code
```

### Integration Tests

```python
from src.pipeline.meeting_pipeline import MeetingPipeline

def test_full_pipeline():
    pipeline = MeetingPipeline()
    # Test with sample audio
```

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_transcription.py

# With coverage
pytest --cov=src

# Watch mode
pytest-watch
```

## 🔍 Debugging

### Enable Debug Logging

```python
from src.utils.logger import setup_logger
import logging

setup_logger(level=logging.DEBUG)
```

### Add Custom Logging

```python
from src.utils.logger import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Inspect Intermediate Results

```python
# In meeting_pipeline.py
transcript = self.whisper_service.transcribe(...)
logger.debug(f"Transcript: {transcript}")  # Save to file if needed
```

## 🚀 Deployment

### Building for Distribution

Using PyInstaller:

```bash
pyinstaller --name=VoicemeetSum --onefile app/gui.py
```

Or create installer with Inno Setup.

### Docker (Future)

```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app/gui.py"]
```

## 📊 Performance Optimization

### Whisper

1. **Model Selection**:
   - `medium`: Best speed/accuracy balance
   - `large-v3`: Best accuracy

2. **Compute Type**:
   - `float16`: GPU (recommended)
   - `int8`: Lower memory

3. **Device**:
   - `cuda`: GPU (fastest)
   - `cpu`: No GPU

### Qwen

1. **Temperature**:
   - `0.0`: More focused
   - `1.0`: More creative

2. **Model Size**:
   - `7b`: Faster
   - `14b`: Better quality

### FFmpeg

1. **Disable unnecessary filters**
2. **Use hardware acceleration** (if available)

## 📝 Code Style

Follow PEP 8:

```bash
# Format with Black
black src/ app/

# Lint with Flake8
flake8 src/ app/

# Type checking with Mypy
mypy src/ app/
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Write tests
4. Submit PR

### PR Checklist

- [ ] Tests pass
- [ ] Code formatted
- [ ] No lint errors
- [ ] Documentation updated
- [ ] Changelog updated

## 🐛 Known Issues

1. **Memory leak**: Unload models after use
2. **File handles**: Close temp files
3. **Ollama timeout**: Set longer timeout for large files

## 📚 Resources

- [Faster-Whisper Docs](https://github.com/guillaumekln/faster-whisper)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [FFmpeg Docs](https://ffmpeg.org/documentation.html)
- [Gradio Docs](https://gradio.app/docs/)

## 🔗 Related Projects

- Whisper: https://github.com/openai/whisper
- Ollama: https://github.com/ollama/ollama
- Gradio: https://github.com/gradio-app/gradio


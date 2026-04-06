# Project Showcase: Smart Meeting Assistant (Voicemeet Sum)

**Role**: Full Stack AI Engineer  
**Timeline**: Dec 2025 - Jan 2026

## 💡 Overview
Developed an enterprise-grade automated meeting minutes generator that processes audio recordings into structured Word documents (DOCX) using local LLMs. The system ensures 100% data privacy by running entirely offline while maintaining high accuracy for Vietnamese language.

## 🛠️ Technology Stack
- **Backend**: Python 3.10, FastAPI, Uvicorn, AsyncIO (Concurrency).
- **AI Core**: 
  - **ASR**: Faster-Whisper (Optimized with CTransl2/Int8 quantization).
  - **LLM**: Qwen 2.5 (via Ollama) for semantic understanding and summarization.
  - **Frameworks**: PyTorch, HuggingFace Transformers.
- **Infrastructure**: Docker, Shell Scripting, Batch Scripting (Cross-platform support for Windows/macOS).
- **Tools**: Git, FD/Ripgrep (workflow optimization).

## 🚀 Key Technical Achievements
1.  **High-Performance Audio Pipeline**:
    - Architected an asynchronous processing pipeline capable of handling multi-hour audio files without blocking the main thread.
    - Implemented smart chunking algorithms to process long contexts within LLM token limits (32k context window management).

2.  **Hardware Optimization**:
    - Engineered a hardware-agnostic detection system that dynamically selects execution backends (CUDA for NVIDIA GPUs, MPS for Apple Silicon, or optimized CPU fallback).
    - Reduced memory footprint by 50% using model quantization techniques.

3.  **Structured Data Extraction**:
    - Designed custom prompt engineering strategies to coerce LLMs into outputting strict JSON schemas.
    - Built a robust validation layer to ensure 99% reliability in extracting actionable items, decisions, and deadlines from unstructured speech.

4.  **System Reliability**:
    - Implemented comprehensive health monitoring (GPU status, disk space, model availability) via REST endpoints.
    - Created a self-healing job manager that handles failures and cleans up resources automatically.

## 📈 Impact
- Delivered a functional MVP capable of reducing meeting documentation time by **90%**.
- Successfully demonstrated offline AI capabilities on consumer-grade hardware (MacBook Air M1, Gaming PCs).

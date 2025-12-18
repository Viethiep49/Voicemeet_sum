"""
FastAPI Backend - Xử lý async, không bị timeout
File: app/backend.py
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import uuid
import json
import time
import asyncio
import shutil
from typing import Dict, Optional
from datetime import datetime
import sys
import subprocess
import os

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.meeting_pipeline import MeetingPipeline
from src.utils.logger import setup_logger, logger
from src.utils.file_handler import is_valid_audio_file, get_file_size, format_file_size, clean_temp_files
from src.utils.system_checker import check_python_version, check_ffmpeg, check_ollama, check_gpu
from config.settings import APP, TRANSCRIPTION, SUMMARIZATION

# Setup
setup_logger("voicemeet_api", APP.logs_dir)
app = FastAPI(title="Voicemeet API", description="API cho dịch vụ chuyển đổi và tóm tắt audio")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Pipeline
pipeline = MeetingPipeline()

# Job storage (in-memory, có thể dùng Redis cho production)
jobs: Dict[str, dict] = {}

# Valid file extensions
VALID_EXTENSIONS = {'.m4a', '.mp4', '.mp3', '.wav', '.flac'}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

def process_job(job_id: str, audio_path: Path):
    """Background task để xử lý audio"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 0
        jobs[job_id]["message"] = "Đang bắt đầu..."
        
        def progress_callback(progress: float, status: str):
            """Update job progress"""
            if job_id in jobs:
                jobs[job_id]["progress"] = progress
                jobs[job_id]["message"] = status
                jobs[job_id]["updated_at"] = time.time()
                logger.info(f"Job {job_id}: {progress:.1f}% - {status}")
        
        # Process
        transcript_path, summary_path, docx_path = pipeline.process(
            audio_file=audio_path,
            progress_callback=progress_callback
        )

        # Update job
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Hoàn thành!"
        jobs[job_id]["transcript"] = str(transcript_path)
        jobs[job_id]["summary"] = str(summary_path)
        jobs[job_id]["docx"] = str(docx_path)
        jobs[job_id]["completed_at"] = time.time()
        
        logger.info(f"Job {job_id} completed successfully")
        
        # Cleanup temp file
        try:
            if audio_path.exists():
                audio_path.unlink()
                logger.info(f"Cleaned up temp file: {audio_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file: {e}")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        if job_id in jobs:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["message"] = f"Lỗi: {str(e)}"
            jobs[job_id]["error"] = str(e)
            jobs[job_id]["failed_at"] = time.time()
        
        # Cleanup temp file on failure
        try:
            if audio_path.exists():
                audio_path.unlink()
        except Exception:
            pass

@app.post("/api/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Upload audio và bắt đầu xử lý"""
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in VALID_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Định dạng file không được hỗ trợ. Hỗ trợ: {', '.join(VALID_EXTENSIONS)}"
            )
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File quá lớn ({format_file_size(file_size)}). Tối đa: {format_file_size(MAX_FILE_SIZE)}"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File rỗng")
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        audio_path = temp_dir / f"{job_id}_{file.filename}"
        
        with open(audio_path, "wb") as f:
            f.write(content)
        
        # Validate saved file
        is_valid, error_msg = is_valid_audio_file(audio_path)
        if not is_valid:
            audio_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=error_msg or "File không hợp lệ")
        
        # Create job
        jobs[job_id] = {
            "id": job_id,
            "filename": file.filename,
            "file_size": file_size,
            "status": "queued",
            "progress": 0,
            "message": "Đang chờ xử lý...",
            "created_at": time.time()
        }
        
        # Start background processing using asyncio
        asyncio.create_task(asyncio.to_thread(process_job, job_id, audio_path))
        
        logger.info(f"Job {job_id} created for file: {file.filename} ({format_file_size(file_size)})")
        
        return JSONResponse({
            "success": True,
            "job_id": job_id,
            "message": "Đã bắt đầu xử lý",
            "filename": file.filename,
            "file_size": file_size
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lỗi khi upload: {str(e)}")

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Lấy trạng thái job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Không tìm thấy job")
    
    job = jobs[job_id]
    return JSONResponse({
        "success": True,
        "job": job
    })

@app.get("/api/download/{job_id}/{file_type}")
async def download_file(job_id: str, file_type: str):
    """Download transcript, summary, hoặc docx"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Không tìm thấy job")

    job = jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job chưa hoàn thành")

    if file_type == "transcript":
        file_path = job.get("transcript")
    elif file_type == "summary":
        file_path = job.get("summary")
    elif file_type == "docx":
        file_path = job.get("docx")
    else:
        raise HTTPException(
            status_code=400,
            detail="Loại file không hợp lệ. Chỉ hỗ trợ: transcript, summary, docx"
        )

    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="Không tìm thấy file")

    # Set appropriate media type for DOCX
    media_type = None
    if file_type == "docx":
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return FileResponse(
        file_path,
        filename=Path(file_path).name,
        media_type=media_type
    )

@app.get("/api/jobs")
async def list_jobs():
    """List tất cả jobs"""
    return JSONResponse({
        "success": True,
        "jobs": list(jobs.values()),
        "total": len(jobs)
    })

@app.get("/api/health")
async def health_check():
    """Kiểm tra trạng thái hệ thống"""
    checks = {}
    overall_status = "healthy"
    
    # 1. Python version
    try:
        py_ok, py_msg = check_python_version()
        version = sys.version_info
        checks["python"] = {
            "status": "ok" if py_ok else "error",
            "version": f"{version.major}.{version.minor}.{version.micro}",
            "message": py_msg
        }
        if not py_ok:
            overall_status = "degraded"
    except Exception as e:
        checks["python"] = {"status": "error", "message": str(e)}
        overall_status = "degraded"
    
    # 2. FFmpeg
    try:
        ffmpeg_ok, ffmpeg_msg = check_ffmpeg()
        version = "unknown"
        if ffmpeg_ok:
            try:
                result = subprocess.run(
                    ['ffmpeg', '-version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    version = version_line.split()[2] if len(version_line.split()) > 2 else "unknown"
            except:
                pass
        
        checks["ffmpeg"] = {
            "status": "ok" if ffmpeg_ok else "error",
            "version": version,
            "message": ffmpeg_msg,
            "recommendation": "Cài đặt FFmpeg từ https://ffmpeg.org/download.html" if not ffmpeg_ok else None
        }
        if not ffmpeg_ok:
            overall_status = "unhealthy"
    except Exception as e:
        checks["ffmpeg"] = {"status": "error", "message": str(e)}
        overall_status = "degraded"
    
    # 3. Ollama
    try:
        ollama_ok, ollama_msg = check_ollama()
        checks["ollama"] = {
            "status": "ok" if ollama_ok else "error",
            "url": SUMMARIZATION.base_url,
            "message": ollama_msg,
            "recommendation": "Chạy lệnh: ollama serve" if not ollama_ok else None
        }
        if not ollama_ok:
            overall_status = "degraded"
    except Exception as e:
        checks["ollama"] = {"status": "error", "message": str(e)}
        overall_status = "degraded"
    
    # 4. CUDA/GPU
    try:
        import torch
        torch_version = torch.__version__
        cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else None
        gpu_name = None
        gpu_available = False
        
        try:
            gpu_available = torch.cuda.is_available()
            if gpu_available:
                gpu_name = torch.cuda.get_device_name(0)
        except:
            pass
        
        if gpu_name:
            # Determine recommended CUDA version
            if "RTX 40" in gpu_name or "RTX 4090" in gpu_name or "RTX 4080" in gpu_name or "RTX 4070" in gpu_name:
                recommended_cuda = "cu121"
            else:
                recommended_cuda = "cu118"
            
            recommended_cmd = f"pip install torch=={torch_version}+{recommended_cuda} --index-url https://download.pytorch.org/whl/{recommended_cuda}"
            
            if cuda_version and recommended_cuda in cuda_version:
                status = "ok"
            else:
                status = "mismatch"
                overall_status = "degraded"
        else:
            status = "cpu_only"
            recommended_cmd = "pip install torch==2.1.0+cpu"
        
        checks["torch_cuda"] = {
            "status": status,
            "torch_version": torch_version,
            "cuda_version": cuda_version,
            "gpu_name": gpu_name,
            "gpu_available": gpu_available,
            "recommendation": recommended_cmd if status != "ok" else None,
            "message": f"GPU: {gpu_name}" if gpu_name else "Chỉ sử dụng CPU"
        }
    except ImportError:
        checks["torch_cuda"] = {
            "status": "missing",
            "message": "Chưa cài torch. Vui lòng cài torch phù hợp GPU.",
            "recommendation": "pip install torch==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118"
        }
        overall_status = "degraded"
    except Exception as e:
        checks["torch_cuda"] = {"status": "error", "message": str(e)}
        overall_status = "degraded"
    
    # 5. Disk space
    try:
        import shutil
        stat = shutil.disk_usage(APP.output_dir)
        free_gb = stat.free / (1024**3)
        checks["disk_space"] = {
            "status": "ok" if free_gb >= 10 else "warning",
            "free_gb": round(free_gb, 2),
            "message": f"Còn {free_gb:.1f} GB trống" if free_gb >= 10 else f"Cảnh báo: Chỉ còn {free_gb:.1f} GB"
        }
        if free_gb < 10:
            overall_status = "degraded" if overall_status == "healthy" else overall_status
    except Exception as e:
        checks["disk_space"] = {"status": "error", "message": str(e)}
        overall_status = "degraded"
    
    # 6. Whisper model
    try:
        model_path = APP.models_cache / f"faster-whisper-{TRANSCRIPTION.model}"
        model_exists = model_path.exists() or (APP.models_cache.exists() and any(
            TRANSCRIPTION.model in str(p) for p in APP.models_cache.rglob("*")
        ))
        checks["whisper_model"] = {
            "status": "ok" if model_exists else "missing",
            "model": TRANSCRIPTION.model,
            "message": "Model đã tải" if model_exists else "Model chưa tải (sẽ tự động tải khi sử dụng)",
            "path": str(model_path)
        }
        if not model_exists:
            overall_status = "degraded" if overall_status == "healthy" else overall_status
    except Exception as e:
        checks["whisper_model"] = {"status": "error", "message": str(e)}
    
    # 7. Qwen model in Ollama
    try:
        import requests
        response = requests.get(
            f"{SUMMARIZATION.base_url}/api/tags",
            timeout=2
        )
        if response.status_code == 200:
            models = response.json().get("models", [])
            qwen_models = [m for m in models if SUMMARIZATION.model in m.get("name", "")]
            checks["qwen_model"] = {
                "status": "ok" if qwen_models else "missing",
                "model": SUMMARIZATION.model,
                "message": "Model đã cài đặt" if qwen_models else f"Model chưa cài. Chạy: ollama pull {SUMMARIZATION.model}",
                "recommendation": f"ollama pull {SUMMARIZATION.model}" if not qwen_models else None
            }
            if not qwen_models:
                overall_status = "degraded" if overall_status == "healthy" else overall_status
        else:
            checks["qwen_model"] = {
                "status": "error",
                "message": "Không thể kiểm tra model trong Ollama"
            }
    except Exception as e:
        checks["qwen_model"] = {
            "status": "error",
            "message": f"Không thể kiểm tra: {str(e)}"
        }
    
    # Determine HTTP status code
    status_code = 200 if overall_status == "healthy" else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": overall_status,
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/")
async def root():
    """Root endpoint - redirect to static frontend"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

def main():
    """Run server"""
    logger.info("Starting Voicemeet API server")
    logger.info("Open http://127.0.0.1:8000/static/index.html in browser")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
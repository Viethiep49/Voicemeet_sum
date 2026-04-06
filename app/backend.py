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
import asyncio
import sys
import os

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import setup_logger, logger
from src.utils.file_handler import is_valid_audio_file, format_file_size
from config.settings import APP
from src.services.health_service import HealthService
from src.services.job_service import job_service

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

# Valid file extensions
VALID_EXTENSIONS = {'.m4a', '.mp4', '.mp3', '.wav', '.flac'}

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
        if file_size > APP.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File quá lớn ({format_file_size(file_size)}). Tối đa: {format_file_size(APP.max_file_size)}"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File rỗng")
        
        # Create job entry
        job_id = job_service.create_job(file.filename, file_size)
        
        # Save uploaded file
        APP.temp_dir.mkdir(exist_ok=True)
        audio_path = APP.temp_dir / f"{job_id}_{file.filename}"
        
        with open(audio_path, "wb") as f:
            f.write(content)
        
        # Validate saved file
        is_valid, error_msg = is_valid_audio_file(audio_path)
        if not is_valid:
            audio_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=error_msg or "File không hợp lệ")
        
        # Start background processing with exception handling
        async def safe_process():
            try:
                await asyncio.to_thread(job_service.process_job, job_id, audio_path)
                logger.info(f"Background task for {job_id} finished successfully")
            except Exception as e:
                logger.error(f"Background task {job_id} exception: {e}", exc_info=True)

        asyncio.create_task(safe_process())
        
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
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy job")
    
    return JSONResponse({
        "success": True,
        "job": job
    })

@app.get("/api/download/{job_id}/{file_type}")
async def download_file(job_id: str, file_type: str):
    """Download transcript, summary, hoặc docx"""
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy job")

    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job chưa hoàn thành")

    file_path = None
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
    jobs = job_service.list_jobs()
    return JSONResponse({
        "success": True,
        "jobs": jobs,
        "total": len(jobs)
    })

@app.get("/api/health")
async def health_check():
    """Kiểm tra trạng thái hệ thống"""
    result = HealthService.check_system()
    status_code = 200 if result["status"] == "healthy" else 503
    return JSONResponse(status_code=status_code, content=result)

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
import time
import uuid
import asyncio
from typing import Dict, Optional, Any
from pathlib import Path

from src.pipeline.meeting_pipeline import MeetingPipeline
from src.utils.logger import logger

class JobService:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.pipeline = MeetingPipeline()

    def create_job(self, filename: str, file_size: int) -> str:
        """Create a new job and return its ID"""
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "id": job_id,
            "filename": filename,
            "file_size": file_size,
            "status": "queued",
            "progress": 0,
            "message": "Đang chờ xử lý...",
            "created_at": time.time()
        }
        return job_id

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)

    def list_jobs(self):
        return list(self.jobs.values())

    def process_job(self, job_id: str, audio_path: Path):
        """Background task logic"""
        if job_id not in self.jobs:
            logger.error(f"Job {job_id} not found immediately at start of processing")
            return

        try:
            self.jobs[job_id]["status"] = "processing"
            self.jobs[job_id]["progress"] = 0
            self.jobs[job_id]["message"] = "Đang bắt đầu..."
            
            def progress_callback(progress: float, status: str):
                """Update job progress"""
                if job_id in self.jobs:
                    self.jobs[job_id]["progress"] = progress
                    self.jobs[job_id]["message"] = status
                    self.jobs[job_id]["updated_at"] = time.time()
                    logger.info(f"Job {job_id}: {progress:.1f}% - {status}")
            
            # Process
            transcript_path, summary_path, docx_path = self.pipeline.process(
                audio_file=audio_path,
                progress_callback=progress_callback
            )

            # Update job
            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["progress"] = 100
            self.jobs[job_id]["message"] = "Hoàn thành!"
            self.jobs[job_id]["transcript"] = str(transcript_path)
            self.jobs[job_id]["summary"] = str(summary_path)
            self.jobs[job_id]["docx"] = str(docx_path)
            self.jobs[job_id]["completed_at"] = time.time()
            
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
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "failed"
                self.jobs[job_id]["message"] = f"Lỗi: {str(e)}"
                self.jobs[job_id]["error"] = str(e)
                self.jobs[job_id]["failed_at"] = time.time()
            
            # Cleanup temp file on failure
            try:
                if audio_path.exists():
                    audio_path.unlink()
            except Exception:
                pass

job_service = JobService()

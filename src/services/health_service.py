import sys
import subprocess
import shutil
import datetime
import os
from pathlib import Path
from typing import Dict, Any

from src.utils.system_checker import check_python_version, check_ffmpeg, check_ollama
from config.settings import APP, TRANSCRIPTION, SUMMARIZATION

class HealthService:
    @staticmethod
    def check_system() -> Dict[str, Any]:
        """Kiểm tra trạng thái toàn bộ hệ thống"""
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
        
        return {
            "status": overall_status,
            "checks": checks,
            "timestamp": datetime.datetime.now().isoformat()
        }

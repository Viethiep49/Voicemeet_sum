"""
═══════════════════════════════════════════════════════════════════════
    VOICEMEET_SUM - SYSTEM TEST & CHECKLIST
═══════════════════════════════════════════════════════════════════════
Kiểm tra toàn diện hệ thống trước khi demo IT GOTTALENT 2025

File: TEST_SYSTEM.py
Author: Voicemeet_sum Team
Date: 2025-12-19
"""

import sys
import io
import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_subheader(text: str):
    """Print subsection header"""
    print("\n" + "-" * 70)
    print(f"  {text}")
    print("-" * 70)

def check_item(name: str, status: bool, message: str, recommendation: str = None):
    """Print check item with status"""
    status_symbol = "✅" if status else "❌"
    status_text = "OK" if status else "FAILED"

    print(f"{status_symbol} [{status_text:6s}] {name:25s} : {message}")

    if not status and recommendation:
        print(f"           💡 Khuyến nghị: {recommendation}")

    return status

def get_system_info() -> Dict:
    """Get system information"""
    import platform

    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }

    return info

def test_python_environment() -> Tuple[bool, Dict]:
    """Test Python version and environment"""
    print_subheader("1. PYTHON ENVIRONMENT")

    results = {}
    all_ok = True

    # Python version
    version = sys.version_info
    py_ok = version.major >= 3 and version.minor >= 9
    results["python_version"] = check_item(
        "Python Version",
        py_ok,
        f"{version.major}.{version.minor}.{version.micro}",
        "Cần Python 3.9+ để chạy dự án" if not py_ok else None
    )
    all_ok = all_ok and py_ok

    # Virtual environment
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    results["venv"] = check_item(
        "Virtual Environment",
        venv_active,
        "Đã kích hoạt" if venv_active else "Chưa kích hoạt",
        "Chạy: venv\\Scripts\\activate.bat" if not venv_active else None
    )

    # Check required packages
    required_packages = {
        "faster-whisper": "faster_whisper",
        "ollama": "ollama",
        "torch": "torch",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "python-docx": "docx",
        "numpy": "numpy",
        "requests": "requests",
        "psutil": "psutil",
    }

    print("\n  📦 Python Packages:")
    packages_ok = True
    for display_name, import_name in required_packages.items():
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            check_item(f"  {display_name}", True, f"v{version}", None)
            results[f"package_{import_name}"] = True
        except ImportError:
            check_item(f"  {display_name}", False, "Chưa cài đặt", f"pip install {display_name}")
            results[f"package_{import_name}"] = False
            packages_ok = False
            all_ok = False

    results["all_packages"] = packages_ok

    return all_ok, results

def test_gpu_cuda() -> Tuple[bool, Dict]:
    """Test GPU and CUDA availability"""
    print_subheader("2. GPU & CUDA")

    results = {}
    all_ok = True

    try:
        import torch

        # PyTorch version
        results["torch_version"] = check_item(
            "PyTorch Version",
            True,
            torch.__version__,
            None
        )

        # CUDA availability
        cuda_available = torch.cuda.is_available()
        results["cuda_available"] = check_item(
            "CUDA Available",
            cuda_available,
            "Có" if cuda_available else "Không",
            "Cài đặt PyTorch với CUDA: pip install torch --index-url https://download.pytorch.org/whl/cu121" if not cuda_available else None
        )

        if cuda_available:
            # GPU info
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)

            results["gpu_name"] = check_item(
                "GPU Device",
                True,
                gpu_name,
                None
            )

            vram_ok = vram_gb >= 6
            results["vram"] = check_item(
                "VRAM",
                vram_ok,
                f"{vram_gb:.1f} GB",
                "Khuyến nghị >= 8GB VRAM cho model medium/large" if not vram_ok else None
            )

            # CUDA version
            cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else "unknown"
            results["cuda_version"] = check_item(
                "CUDA Version",
                True,
                cuda_version,
                None
            )

            # cuDNN
            cudnn_available = torch.backends.cudnn.is_available()
            results["cudnn"] = check_item(
                "cuDNN",
                cudnn_available,
                "Có" if cudnn_available else "Không",
                None
            )
        else:
            all_ok = False
            print("  ⚠️  Chạy trên CPU - tốc độ sẽ chậm hơn 10-20x")

    except ImportError:
        results["torch_installed"] = check_item(
            "PyTorch",
            False,
            "Chưa cài đặt",
            "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
        )
        all_ok = False

    return all_ok, results

def test_external_tools() -> Tuple[bool, Dict]:
    """Test external tools (FFmpeg, Ollama)"""
    print_subheader("3. EXTERNAL TOOLS")

    results = {}
    all_ok = True

    # FFmpeg
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
            results["ffmpeg"] = check_item(
                "FFmpeg",
                True,
                f"v{version}",
                None
            )
        else:
            results["ffmpeg"] = check_item(
                "FFmpeg",
                False,
                "Lỗi khi chạy",
                "Cài đặt FFmpeg từ https://ffmpeg.org/download.html"
            )
            all_ok = False

    except (subprocess.TimeoutExpired, FileNotFoundError):
        results["ffmpeg"] = check_item(
            "FFmpeg",
            False,
            "Chưa cài đặt",
            "Download từ https://ffmpeg.org/ và thêm vào PATH"
        )
        all_ok = False

    # Ollama
    try:
        response = requests.get("http://localhost:11434", timeout=2)

        if response.status_code == 200:
            results["ollama_running"] = check_item(
                "Ollama Service",
                True,
                "Đang chạy",
                None
            )

            # Check Qwen model
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    qwen_models = [m for m in models if "qwen2.5:7b" in m.get("name", "").lower()]

                    results["qwen_model"] = check_item(
                        "Qwen 2.5 Model",
                        len(qwen_models) > 0,
                        "Đã cài đặt" if qwen_models else "Chưa cài đặt",
                        "Chạy: ollama pull qwen2.5:7b" if not qwen_models else None
                    )

                    if not qwen_models:
                        all_ok = False
            except:
                results["qwen_model"] = check_item(
                    "Qwen 2.5 Model",
                    False,
                    "Không kiểm tra được",
                    None
                )
        else:
            results["ollama_running"] = check_item(
                "Ollama Service",
                False,
                "Không phản hồi",
                "Chạy: ollama serve"
            )
            all_ok = False

    except requests.exceptions.ConnectionError:
        results["ollama_running"] = check_item(
            "Ollama Service",
            False,
            "Không chạy",
            "Cài đặt từ https://ollama.ai/ hoặc chạy: ollama serve"
        )
        all_ok = False
    except Exception as e:
        results["ollama_running"] = check_item(
            "Ollama Service",
            False,
            f"Lỗi: {str(e)}",
            None
        )
        all_ok = False

    return all_ok, results

def test_project_structure() -> Tuple[bool, Dict]:
    """Test project directory structure"""
    print_subheader("4. PROJECT STRUCTURE")

    results = {}
    all_ok = True

    required_dirs = {
        "app": "FastAPI backend",
        "src": "Source code",
        "config": "Configuration",
        "temp": "Temporary files",
        "output": "Output files",
        "logs": "Log files",
        "models_cache": "Model cache",
    }

    for dir_name, description in required_dirs.items():
        dir_path = Path(dir_name)
        exists = dir_path.exists()

        results[f"dir_{dir_name}"] = check_item(
            f"{dir_name}/",
            exists,
            description,
            f"Tạo thư mục: mkdir {dir_name}" if not exists else None
        )

        if dir_name in ["temp", "output", "logs", "models_cache"] and not exists:
            # Create missing directories
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"           ✓ Đã tạo thư mục {dir_name}/")
            except:
                all_ok = False

    # Check key files
    required_files = {
        "app/backend.py": "FastAPI backend",
        "config/settings.py": "Configuration",
        "SETUP.bat": "Setup script",
        "CHAY_APP.bat": "Run script",
    }

    print("\n  📄 Key Files:")
    for file_path, description in required_files.items():
        exists = Path(file_path).exists()
        results[f"file_{file_path}"] = check_item(
            f"  {file_path}",
            exists,
            description,
            f"File thiếu! Kiểm tra lại repo" if not exists else None
        )

        if not exists:
            all_ok = False

    return all_ok, results

def test_disk_space() -> Tuple[bool, Dict]:
    """Test disk space"""
    print_subheader("5. DISK SPACE")

    results = {}

    try:
        import shutil

        # Check output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        stat = shutil.disk_usage(output_dir)
        free_gb = stat.free / (1024**3)
        total_gb = stat.total / (1024**3)

        space_ok = free_gb >= 10
        results["disk_space"] = check_item(
            "Free Disk Space",
            space_ok,
            f"{free_gb:.1f} GB / {total_gb:.1f} GB",
            "Cảnh báo: Cần ít nhất 10GB cho models và output" if not space_ok else None
        )

        return space_ok, results

    except Exception as e:
        results["disk_space"] = check_item(
            "Disk Space",
            False,
            f"Lỗi: {str(e)}",
            None
        )
        return False, results

def test_api_health() -> Tuple[bool, Dict]:
    """Test API health endpoint (if running)"""
    print_subheader("6. API HEALTH CHECK")

    results = {}

    try:
        response = requests.get("http://127.0.0.1:8000/api/health", timeout=3)

        if response.status_code in [200, 503]:
            health_data = response.json()

            results["api_running"] = check_item(
                "API Server",
                response.status_code == 200,
                health_data.get("status", "unknown"),
                "Một số component chưa ready" if response.status_code == 503 else None
            )

            # Show individual checks
            checks = health_data.get("checks", {})
            print("\n  🔍 Detailed Checks:")
            for component, check_data in checks.items():
                status = check_data.get("status") == "ok"
                message = check_data.get("message", "")
                recommendation = check_data.get("recommendation")

                check_item(f"  {component}", status, message, recommendation)

            return response.status_code == 200, results
        else:
            results["api_running"] = check_item(
                "API Server",
                False,
                f"HTTP {response.status_code}",
                None
            )
            return False, results

    except requests.exceptions.ConnectionError:
        results["api_running"] = check_item(
            "API Server",
            False,
            "Không chạy",
            "Khởi động server: CHAY_APP.bat"
        )
        return False, results
    except Exception as e:
        results["api_running"] = check_item(
            "API Server",
            False,
            f"Lỗi: {str(e)}",
            None
        )
        return False, results

def generate_report(all_results: Dict, system_info: Dict):
    """Generate test report"""
    print_header("📊 BÁO CÁO TỔNG HỢP")

    # Count results
    total_checks = 0
    passed_checks = 0

    for category, (category_ok, results) in all_results.items():
        for check_name, check_result in results.items():
            if isinstance(check_result, bool):
                total_checks += 1
                if check_result:
                    passed_checks += 1

    success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0

    print(f"\n  Tổng số kiểm tra: {total_checks}")
    print(f"  Thành công:      {passed_checks} ✅")
    print(f"  Thất bại:        {total_checks - passed_checks} ❌")
    print(f"  Tỷ lệ thành công: {success_rate:.1f}%")

    # Overall status
    print("\n" + "=" * 70)
    if success_rate >= 90:
        print("  🎉 HỆ THỐNG SẴN SÀNG CHO IT GOTTALENT 2025!")
        print("     Có thể demo ngay!")
    elif success_rate >= 70:
        print("  ⚠️  HỆ THỐNG CẦN ĐIỀU CHỈNH")
        print("     Kiểm tra các khuyến nghị phía trên")
    else:
        print("  ❌ HỆ THỐNG CHƯA SẴN SÀNG")
        print("     Cần khắc phục các vấn đề quan trọng")
    print("=" * 70)

    # Save report to file
    report_file = Path("output/system_test_report.json")
    report_file.parent.mkdir(exist_ok=True)

    report_data = {
        "timestamp": datetime.now().isoformat(),
        "system_info": system_info,
        "results": all_results,
        "summary": {
            "total_checks": total_checks,
            "passed": passed_checks,
            "failed": total_checks - passed_checks,
            "success_rate": success_rate
        }
    }

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n  📝 Chi tiết báo cáo được lưu tại: {report_file}")

    return success_rate >= 70

def main():
    """Main test function"""
    print_header("🎤 VOICEMEET_SUM - SYSTEM TEST")
    print(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Mục tiêu: IT GOTTALENT 2025")

    # System info
    system_info = get_system_info()
    print(f"\n  OS: {system_info['os']} {system_info['architecture']}")
    print(f"  Python: {system_info['python_version']}")

    # Run all tests
    all_results = {}

    all_results["python"] = test_python_environment()
    all_results["gpu"] = test_gpu_cuda()
    all_results["tools"] = test_external_tools()
    all_results["structure"] = test_project_structure()
    all_results["disk"] = test_disk_space()
    all_results["api"] = test_api_health()

    # Generate report
    overall_ok = generate_report(all_results, system_info)

    return 0 if overall_ok else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

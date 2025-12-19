"""
Script tự động kiểm tra GPU/CUDA và cài đặt PyTorch phù hợp
File: DEPLOYMENT/install_pytorch_cuda.py
"""
import sys
import subprocess
import platform
import io
from pathlib import Path

# Try to import psutil for process management
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_header(text):
    """In header với format đẹp"""
    try:
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    except UnicodeEncodeError:
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print("\n" + "=" * 70)
        print(f"  {safe_text}")
        print("=" * 70)

def print_info(text):
    """In thông tin"""
    print(f"[INFO] {text}")

def print_success(text):
    """In thành công"""
    try:
        print(f"[OK] {text}")
    except UnicodeEncodeError:
        print(f"[OK] {text.encode('ascii', 'replace').decode('ascii')}")

def print_warning(text):
    """In cảnh báo"""
    try:
        print(f"[WARNING] {text}")
    except UnicodeEncodeError:
        print(f"[WARNING] {text.encode('ascii', 'replace').decode('ascii')}")

def print_error(text):
    """In lỗi"""
    try:
        print(f"[ERROR] {text}")
    except UnicodeEncodeError:
        print(f"[ERROR] {text.encode('ascii', 'replace').decode('ascii')}")

def check_nvidia_gpu():
    """
    Kiểm tra GPU NVIDIA bằng nvidia-smi
    Returns: (has_gpu, gpu_name, cuda_version)
    """
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,driver_version', '--format=csv,noheader'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            if lines:
                # Lấy GPU đầu tiên
                gpu_info = lines[0].split(',')
                gpu_name = gpu_info[0].strip()
                
                # Lấy CUDA version từ nvidia-smi
                cuda_result = subprocess.run(
                    ['nvidia-smi'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                cuda_version = None
                if cuda_result.returncode == 0:
                    for line in cuda_result.stdout.split('\n'):
                        if 'CUDA Version:' in line:
                            parts = line.split('CUDA Version:')
                            if len(parts) > 1:
                                cuda_version = parts[1].strip().split()[0]
                                break
                
                return True, gpu_name, cuda_version
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    except Exception as e:
        print_warning(f"Không thể kiểm tra GPU qua nvidia-smi: {e}")
    
    return False, None, None

def check_torch_installation():
    """
    Kiểm tra PyTorch đã cài đặt chưa
    Returns: (is_installed, torch_version, cuda_version, gpu_available, gpu_name)
    """
    try:
        import torch
        torch_version = torch.__version__
        cuda_version = None
        gpu_available = False
        gpu_name = None
        
        try:
            cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else None
            gpu_available = torch.cuda.is_available()
            if gpu_available:
                gpu_name = torch.cuda.get_device_name(0)
        except:
            pass
        
        return True, torch_version, cuda_version, gpu_available, gpu_name
    except ImportError:
        return False, None, None, False, None

def determine_cuda_version(gpu_name):
    """
    Xác định CUDA version phù hợp dựa trên GPU model
    Returns: (cuda_version, torch_version)
    """
    if not gpu_name:
        return None, None
    
    gpu_name_upper = gpu_name.upper()
    
    # RTX 40 series (Ada Lovelace) - dùng CUDA 12.1
    if any(x in gpu_name_upper for x in ['RTX 40', 'RTX 4090', 'RTX 4080', 'RTX 4070', 'RTX 4060']):
        return "cu121", "2.5.1"
    
    # RTX 30 series (Ampere) - dùng CUDA 11.8
    if any(x in gpu_name_upper for x in ['RTX 30', 'RTX 3090', 'RTX 3080', 'RTX 3070', 'RTX 3060']):
        return "cu118", "2.5.1"
    
    # RTX 20 series (Turing) - dùng CUDA 11.8
    if any(x in gpu_name_upper for x in ['RTX 20', 'RTX 2080', 'RTX 2070', 'RTX 2060']):
        return "cu118", "2.5.1"
    
    # GTX series - dùng CUDA 11.8
    if 'GTX' in gpu_name_upper:
        return "cu118", "2.5.1"
    
    # Mặc định cho GPU NVIDIA khác - dùng CUDA 11.8
    if 'NVIDIA' in gpu_name_upper or 'GEFORCE' in gpu_name_upper:
        return "cu118", "2.5.1"
    
    return None, None

def stop_python_processes():
    """
    Dừng tất cả process Python đang chạy (trừ process hiện tại)
    """
    import os
    import time
    
    if HAS_PSUTIL:
        try:
            current_pid = os.getpid()
            stopped_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        if proc.info['pid'] != current_pid:
                            # Kiểm tra xem có phải là process của project này không
                            cmdline = proc.info.get('cmdline', [])
                            if cmdline and any('Voicemeet_sum' in str(arg) for arg in cmdline):
                                print_info(f"Dừng process Python (PID: {proc.info['pid']})")
                                proc.terminate()
                                stopped_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if stopped_count > 0:
                print_info(f"Đã dừng {stopped_count} process Python")
                time.sleep(2)  # Đợi process dừng
            
            return stopped_count
        except Exception as e:
            print_warning(f"Không thể dừng process Python (psutil): {e}")
    
    # Fallback: dùng subprocess trên Windows
    if platform.system() == 'Windows':
        try:
            # Tìm các process Python liên quan đến project
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and 'python.exe' in result.stdout:
                print_info("Phát hiện process Python đang chạy")
                print_warning("Vui lòng đóng thủ công các process Python trước khi cài đặt")
                print_info("Hoặc chạy: taskkill /F /IM python.exe")
                return 0
        except Exception as e:
            print_warning(f"Không thể kiểm tra process: {e}")
    
    return 0

def cleanup_corrupted_torch():
    """
    Dọn dẹp thư mục torch bị lỗi
    """
    import shutil
    from pathlib import Path
    
    try:
        # Tìm thư mục site-packages của venv hiện tại
        venv_python = Path(sys.executable)
        if 'venv' in str(venv_python) or 'Scripts' in str(venv_python):
            # Đang trong venv
            site_packages = venv_python.parent.parent / 'Lib' / 'site-packages'
        else:
            # Không trong venv, dùng site-packages mặc định
            import site
            if site.getsitepackages():
                site_packages = Path(site.getsitepackages()[0])
            else:
                site_packages = Path(sys.prefix) / 'Lib' / 'site-packages'
        
        if not site_packages.exists():
            return False
        
        # Tìm các thư mục/file bị lỗi
        cleaned = False
        
        # Tìm thư mục/file bắt đầu bằng ~orch
        for item in site_packages.iterdir():
            try:
                if item.name.startswith('~orch') or '~orch' in item.name:
                    if item.is_dir():
                        print_info(f"Xóa thư mục bị lỗi: {item.name}")
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        print_info(f"Xóa file bị lỗi: {item.name}")
                        item.unlink(missing_ok=True)
                    cleaned = True
            except Exception as e:
                print_warning(f"Không thể xóa {item.name}: {e}")
        
        if cleaned:
            print_success("Đã dọn dẹp các file torch bị lỗi")
        
        return cleaned
    except Exception as e:
        print_warning(f"Không thể dọn dẹp: {e}")
        return False

def check_torch_in_use():
    """
    Kiểm tra xem PyTorch có đang được sử dụng không
    """
    try:
        import torch
        # Thử import một số module để xem có process nào đang dùng không
        try:
            # Thử tạo một tensor nhỏ để test
            x = torch.randn(1, 1)
            del x
            return False
        except:
            return True
    except ImportError:
        return False

def install_pytorch_cuda(cuda_version, torch_version):
    """
    Cài đặt PyTorch với CUDA
    """
    if not cuda_version or not torch_version:
        print_error("Không thể xác định CUDA version phù hợp")
        return False
    
    # Kiểm tra và dừng process Python đang chạy
    print_info("Kiểm tra process Python đang chạy...")
    stopped = stop_python_processes()
    
    # Dọn dẹp torch bị lỗi
    print_info("Dọn dẹp file torch bị lỗi...")
    cleanup_corrupted_torch()
    
    # Kiểm tra xem có process nào đang dùng PyTorch không
    print_info("Kiểm tra PyTorch có đang được sử dụng...")
    if check_torch_in_use():
        print_warning("PyTorch có thể đang được sử dụng bởi process khác")
        print_info("Đã thử dừng các process Python, nhưng vẫn có thể có process khác đang dùng")
        response = input("\nBạn có muốn tiếp tục cài đặt? (y/n): ").strip().lower()
        if response != 'y':
            print_info("Đã hủy cài đặt")
            return False
    
    print_info(f"Đang cài đặt PyTorch {torch_version} với CUDA {cuda_version}...")
    
    # Build pip install command
    index_url = f"https://download.pytorch.org/whl/{cuda_version}"
    cmd = [
        sys.executable, "-m", "pip", "install",
        f"torch=={torch_version}+{cuda_version}",
        "--index-url", index_url,
        "--upgrade"
    ]
    
    print_info(f"Lệnh: {' '.join(cmd)}")
    print_info("Quá trình này có thể mất vài phút...")
    print_warning("LƯU Ý: Nếu gặp lỗi 'Access is denied', hãy:")
    print_warning("  1. Đóng tất cả ứng dụng đang chạy (server, Python scripts)")
    print_warning("  2. Chạy lại script này")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Đã cài đặt PyTorch thành công!")
            return True
        else:
            print_error("Cài đặt PyTorch thất bại")
            return False
    except subprocess.CalledProcessError as e:
        print_error(f"Lỗi khi cài đặt: {e}")
        if "Access is denied" in str(e) or "WinError 5" in str(e):
            print_error("\n⚠️  LỖI: Không thể ghi file PyTorch")
            print_error("Nguyên nhân: File đang được sử dụng bởi process khác")
            print_info("\nGiải pháp:")
            print_info("1. Đóng tất cả cửa sổ Python/terminal đang chạy")
            print_info("2. Đóng server FastAPI nếu đang chạy")
            print_info("3. Chạy lại script này")
        return False
    except Exception as e:
        print_error(f"Lỗi không mong đợi: {e}")
        return False

def install_pytorch_cpu():
    """
    Cài đặt PyTorch CPU-only
    """
    print_info("Đang cài đặt PyTorch CPU-only...")
    
    cmd = [
        sys.executable, "-m", "pip", "install",
        "torch",
        "--upgrade"
    ]
    
    print_info(f"Lệnh: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Đã cài đặt PyTorch CPU thành công!")
            return True
        else:
            print_error("Cài đặt PyTorch CPU thất bại")
            return False
    except Exception as e:
        print_error(f"Lỗi khi cài đặt: {e}")
        return False

def verify_installation():
    """
    Xác minh cài đặt PyTorch
    """
    print_header("XÁC MINH CÀI ĐẶT")
    
    try:
        import torch
        print_success(f"PyTorch version: {torch.__version__}")
        
        cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else None
        if cuda_version:
            print_success(f"CUDA version: {cuda_version}")
        else:
            print_warning("PyTorch không có CUDA support (CPU-only)")
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print_success(f"GPU: {gpu_name}")
            print_success(f"VRAM: {memory_gb:.1f} GB")
            
            # Test CUDA
            try:
                x = torch.randn(3, 3).cuda()
                print_success("CUDA hoat dong binh thuong!")
                return True
            except Exception as e:
                print_error(f"CUDA khong hoat dong: {e}")
                return False
        else:
            print_warning("GPU không khả dụng - đang dùng CPU")
            return True
    except ImportError:
        print_error("PyTorch chưa được cài đặt")
        return False
    except Exception as e:
        print_error(f"Lỗi khi xác minh: {e}")
        return False

def main():
    """Hàm chính"""
    print_header("KIỂM TRA VÀ CÀI ĐẶT PYTORCH CUDA")
    
    # 1. Kiểm tra GPU NVIDIA
    print_header("BƯỚC 1: KIỂM TRA GPU")
    has_nvidia_gpu, gpu_name, nvidia_cuda = check_nvidia_gpu()
    
    if has_nvidia_gpu:
        print_success(f"Tìm thấy GPU: {gpu_name}")
        if nvidia_cuda:
            print_info(f"CUDA version (driver): {nvidia_cuda}")
    else:
        print_warning("Không tìm thấy GPU NVIDIA")
        print_info("Sẽ cài đặt PyTorch CPU-only")
    
    # 2. Kiểm tra PyTorch hiện tại
    print_header("BƯỚC 2: KIỂM TRA PYTORCH HIỆN TẠI")
    torch_installed, torch_version, cuda_version, gpu_available, torch_gpu_name = check_torch_installation()
    
    if torch_installed:
        print_info(f"PyTorch đã cài: {torch_version}")
        if cuda_version:
            print_info(f"CUDA version (PyTorch): {cuda_version}")
        if gpu_available:
            print_success(f"GPU khả dụng: {torch_gpu_name}")
        else:
            print_warning("GPU không khả dụng trong PyTorch")
    else:
        print_info("PyTorch chưa được cài đặt")
    
    # 3. Xác định CUDA version cần cài
    print_header("BƯỚC 3: XÁC ĐỊNH CÀI ĐẶT")
    
    if has_nvidia_gpu:
        # Có GPU NVIDIA
        target_cuda, target_torch = determine_cuda_version(gpu_name)
        
        if target_cuda:
            print_info(f"GPU: {gpu_name}")
            print_info(f"Khuyến nghị: PyTorch {target_torch} + CUDA {target_cuda}")
            
            # Kiểm tra xem có cần cài đặt lại không
            if torch_installed:
                if gpu_available and cuda_version:
                    # Kiểm tra xem CUDA version có phù hợp không
                    if target_cuda in cuda_version or cuda_version in target_cuda:
                        print_success("PyTorch đã được cài đặt đúng với GPU!")
                        print_info("Không cần cài đặt lại")
                        
                        # Vẫn xác minh
                        verify_installation()
                        return True
                    else:
                        print_warning(f"CUDA version không khớp: {cuda_version} vs {target_cuda}")
                        print_info("Sẽ cài đặt lại với CUDA version phù hợp")
                else:
                    print_warning("PyTorch không có CUDA support")
                    print_info("Sẽ cài đặt lại với CUDA support")
            
            # Cài đặt PyTorch với CUDA
            print_header("BƯỚC 4: CÀI ĐẶT PYTORCH")
            success = install_pytorch_cuda(target_cuda, target_torch)
            
            if success:
                # Kiểm tra CUDA DLL sau khi cài đặt
                print_header("BƯỚC 5: KIỂM TRA CUDA LIBRARIES")
                try:
                    # Import và chạy check_cuda_libs
                    check_script = Path(__file__).parent / 'check_cuda_libs.py'
                    if check_script.exists():
                        result = subprocess.run(
                            [sys.executable, str(check_script)],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if result.returncode == 0:
                            print_success("CUDA libraries đã sẵn sàng")
                        else:
                            print_warning("Một số CUDA libraries có thể thiếu")
                            print_info("Nếu gặp lỗi 'cublas64_12.dll not found', vui lòng:")
                            print_info("1. Cài đặt CUDA Toolkit từ: https://developer.nvidia.com/cuda-downloads")
                            print_info("2. Hoặc hệ thống sẽ tự động fallback về CPU")
                    else:
                        print_warning("Không tìm thấy script kiểm tra CUDA libraries")
                except Exception as e:
                    print_warning(f"Không thể kiểm tra CUDA libraries: {e}")
                
                verify_installation()
                return True
            else:
                print_error("Cài đặt thất bại")
                return False
        else:
            print_warning(f"Không thể xác định CUDA version cho GPU: {gpu_name}")
            print_info("Sẽ cài đặt PyTorch với CUDA 11.8 (mặc định)")
            success = install_pytorch_cuda("cu118", "2.5.1")
            if success:
                verify_installation()
                return True
    else:
        # Không có GPU - cài CPU-only
        if torch_installed and not gpu_available:
            print_success("PyTorch CPU đã được cài đặt")
            verify_installation()
            return True
        
        print_info("Không có GPU NVIDIA - cài đặt PyTorch CPU-only")
        print_header("BƯỚC 4: CÀI ĐẶT PYTORCH CPU")
        success = install_pytorch_cpu()
        
        if success:
            verify_installation()
            return True
        else:
            print_error("Cài đặt thất bại")
            return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print_error(f"Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


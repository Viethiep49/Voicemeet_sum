"""
Script kiểm tra CUDA libraries (DLL) có sẵn
"""
import os
import sys
from pathlib import Path

def find_cuda_dlls():
    """Tìm các CUDA DLL cần thiết"""
    required_dlls = [
        'cublas64_12.dll',
        'cublas64_11.dll',
        'cudart64_12.dll',
        'cudart64_11.dll',
        'cudnn64_8.dll',
        'curand64_10.dll',
        'cusolver64_11.dll',
        'cusparse64_11.dll',
    ]
    
    found_dlls = {}
    search_paths = []
    
    # 1. PyTorch lib folder
    try:
        import torch
        torch_lib = Path(torch.__file__).parent / 'lib'
        if torch_lib.exists():
            search_paths.append(torch_lib)
    except:
        pass
    
    # 2. CUDA Toolkit paths
    cuda_paths = [
        os.environ.get('CUDA_PATH', ''),
        os.environ.get('CUDA_HOME', ''),
        r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin',
        r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin',
        r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin',
        r'C:\Program Files (x86)\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin',
        r'C:\Program Files (x86)\NVIDIA GPU Computing Toolkit\CUDA\v12.0\bin',
        r'C:\Program Files (x86)\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin',
    ]
    
    for cuda_path in cuda_paths:
        if cuda_path and Path(cuda_path).exists():
            search_paths.append(Path(cuda_path))
    
    # 3. System PATH
    path_env = os.environ.get('PATH', '')
    for path_dir in path_env.split(os.pathsep):
        if path_dir and Path(path_dir).exists():
            search_paths.append(Path(path_dir))
    
    # Tìm DLLs
    for dll_name in required_dlls:
        for search_path in search_paths:
            dll_path = search_path / dll_name
            if dll_path.exists():
                found_dlls[dll_name] = str(dll_path)
                break
    
    return found_dlls, search_paths

def check_cuda_libs():
    """Kiểm tra CUDA libraries"""
    print("=" * 70)
    print("KIỂM TRA CUDA LIBRARIES")
    print("=" * 70)
    
    found_dlls, search_paths = find_cuda_dlls()
    
    print(f"\nĐã tìm thấy {len(found_dlls)} DLL trong {len(search_paths)} thư mục")
    
    # Hiển thị các DLL đã tìm thấy
    if found_dlls:
        print("\n✅ Các DLL đã tìm thấy:")
        for dll_name, dll_path in found_dlls.items():
            print(f"  - {dll_name}: {dll_path}")
    else:
        print("\n❌ Không tìm thấy DLL nào!")
    
    # Kiểm tra DLL quan trọng nhất
    critical_dlls = ['cublas64_12.dll', 'cublas64_11.dll', 'cudart64_12.dll', 'cudart64_11.dll']
    has_critical = any(dll in found_dlls for dll in critical_dlls)
    
    if has_critical:
        print("\n✅ Có đủ DLL cơ bản để chạy CUDA")
    else:
        print("\n⚠️  THIẾU DLL QUAN TRỌNG!")
        print("   Cần cài đặt CUDA Toolkit từ:")
        print("   https://developer.nvidia.com/cuda-downloads")
    
    # Đề xuất thêm vào PATH
    if found_dlls:
        print("\n📋 Đề xuất thêm vào PATH:")
        unique_paths = set()
        for dll_path in found_dlls.values():
            unique_paths.add(str(Path(dll_path).parent))
        
        for path in sorted(unique_paths):
            if path not in os.environ.get('PATH', ''):
                print(f"  {path}")
    
    return has_critical, found_dlls

if __name__ == '__main__':
    try:
        has_critical, found_dlls = check_cuda_libs()
        sys.exit(0 if has_critical else 1)
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)


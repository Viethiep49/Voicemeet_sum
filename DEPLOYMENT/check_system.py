"""
System requirements checker
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.system_checker import print_system_check

if __name__ == "__main__":
    success = print_system_check()
    sys.exit(0 if success else 1)


"""
Лаунчер для запуска Votobu без консоли.
Использует subprocess для запуска с скрытой консолью.
"""

import subprocess
import sys
from pathlib import Path

# Получить путь к main.py
script_dir = Path(__file__).parent
main_script = script_dir / "src" / "main.py"

# Запустить python.exe с флагом CREATE_NO_WINDOW
if sys.platform == 'win32':
    # Windows: скрыть консольное окно
    import ctypes
    CREATE_NO_WINDOW = 0x08000000
    
    subprocess.Popen(
        [sys.executable, str(main_script)],
        creationflags=CREATE_NO_WINDOW,
        close_fds=True
    )
else:
    # Linux/Mac
    subprocess.Popen(
        [sys.executable, str(main_script)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True
    )


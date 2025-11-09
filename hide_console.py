"""
Скрипт для скрытия консольного окна после запуска.
Запускает main.py но прячет консоль.
"""

import sys
import os

# Windows: Скрыть консольное окно
if sys.platform == 'win32':
    import ctypes
    
    # Получить handle консольного окна
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    
    if hwnd != 0:
        # SW_HIDE = 0
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        
# Импортировать и запустить main
sys.path.insert(0, 'src')
from main import main

if __name__ == "__main__":
    main()


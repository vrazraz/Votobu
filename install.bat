@echo off
echo ========================================
echo   Votobu Installation Script v1.0.2
echo ========================================
echo.
echo This will install all dependencies automatically.
echo Installation may take 5-10 minutes depending on your internet speed.
echo.
pause

echo.
echo [1/7] Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo.
echo [2/7] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [3/7] Cleaning old installations...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y >nul 2>&1

echo.
echo [4/7] Installing ALL dependencies from requirements.txt...
echo This includes: PyQt5, Whisper, sounddevice, pynput, ffmpeg, etc.
pip install -r requirements.txt

echo.
echo [5/7] Verifying critical packages...
pip install --upgrade PyQt5==5.15.9 PyQt5-sip PyQt5-Qt5
pip install --upgrade imageio-ffmpeg ffmpeg-python

echo.
echo [6/7] Testing imports...
python -c "import PyQt5; import whisper; import sounddevice; import pynput; print('All imports OK!')"
if %errorlevel% neq 0 (
    echo WARNING: Some imports failed. Check output above.
)

echo.
echo [7/7] Creating application icons...
python create_icons.py

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Installed packages:
pip list | findstr "PyQt5 whisper sounddevice pynput imageio-ffmpeg"
echo.
echo ========================================
echo.
echo Next steps:
echo   1. Double-click: run.bat
echo   2. Wait 1-2 min for Whisper model download (first time only)
echo   3. Look for blue microphone icon in system tray
echo   4. Press F9 and speak, release F9 to process
echo   5. Press Ctrl+V to paste recognized text
echo.
echo Troubleshooting:
echo   - If errors occur, see TROUBLESHOOTING.md
echo   - Run: python test_components.py (to diagnose issues)
echo.
echo ========================================
pause


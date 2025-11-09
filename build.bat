@echo off
echo ========================================
echo   Votobu - Build Standalone .exe
echo ========================================
echo.
echo This will create a standalone .exe file with all dependencies included.
echo The process may take 10-20 minutes.
echo.
echo Requirements:
echo   - PyInstaller (will be installed if missing)
echo   - All Votobu dependencies already installed
echo.
pause

echo.
echo [1/5] Installing PyInstaller...
pip install pyinstaller

echo.
echo [2/5] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Votobu.spec del Votobu.spec

echo.
echo [3/5] Building executable with PyInstaller...
echo This may take 10-20 minutes...
pyinstaller ^
    --name=Votobu ^
    --onefile ^
    --windowed ^
    --icon=assets/icon.png ^
    --add-data="assets;assets" ^
    --add-data="config;config" ^
    --hidden-import=whisper ^
    --hidden-import=sounddevice ^
    --hidden-import=pynput ^
    --hidden-import=imageio_ffmpeg ^
    --collect-all=whisper ^
    --collect-all=imageio_ffmpeg ^
    src/main.py

echo.
echo [4/5] Copying additional files...
if not exist dist\Votobu mkdir dist\Votobu
copy README.md dist\Votobu\ >nul 2>&1
copy QUICKSTART.md dist\Votobu\ >nul 2>&1
copy TROUBLESHOOTING.md dist\Votobu\ >nul 2>&1
copy LICENSE dist\Votobu\ >nul 2>&1

echo.
echo [5/5] Creating portable package...
cd dist
if exist Votobu.zip del Votobu.zip
powershell Compress-Archive -Path Votobu\* -DestinationPath Votobu-v1.0.2-Windows.zip
cd ..

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Standalone executable created:
echo   dist\Votobu.exe
echo.
echo Portable package created:
echo   dist\Votobu-v1.0.2-Windows.zip
echo.
echo You can distribute this .exe file to other computers
echo without requiring Python installation!
echo.
echo Note: First run will still need to download Whisper model (~150MB)
echo.
pause


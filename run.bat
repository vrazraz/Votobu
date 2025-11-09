@echo off
echo ========================================
echo   Votobu - Voice to Text
echo ========================================
echo.
echo Starting application...
echo.
echo Look for the microphone icon in your system tray!
echo Press F9 to start recording, release to stop.
echo.
echo Note: First startup may take 1-2 minutes to load Whisper model.
echo.
echo ========================================
echo.

python src\main.py

echo.
echo ========================================
echo   Votobu stopped
echo ========================================
echo.
echo If you encountered errors, check TROUBLESHOOTING.md
echo.
pause


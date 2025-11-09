@echo off
echo ========================================
echo   Votobu - Offline Installer Creator
echo ========================================
echo.
echo This will create an offline installer package that includes
echo all Python dependencies as wheel files.
echo.
echo The package can be installed on computers without internet access.
echo.
pause

echo.
echo [1/4] Creating offline package directory...
if not exist offline_installer mkdir offline_installer
if not exist offline_installer\wheels mkdir offline_installer\wheels

echo.
echo [2/4] Downloading all dependencies as wheels...
pip download -r requirements.txt -d offline_installer\wheels

echo.
echo [3/4] Copying installation files...
copy install.bat offline_installer\install_offline.bat
copy requirements.txt offline_installer\
copy README.md offline_installer\
copy QUICKSTART.md offline_installer\
copy TROUBLESHOOTING.md offline_installer\
xcopy /E /I /Y src offline_installer\src
xcopy /E /I /Y assets offline_installer\assets
xcopy /E /I /Y config offline_installer\config
copy create_icons.py offline_installer\
copy run.bat offline_installer\
copy test_components.py offline_installer\

echo.
echo [4/4] Creating install_offline.bat script...
echo @echo off > offline_installer\install_offline.bat
echo echo Installing Votobu from offline package... >> offline_installer\install_offline.bat
echo echo. >> offline_installer\install_offline.bat
echo pip install --no-index --find-links=wheels -r requirements.txt >> offline_installer\install_offline.bat
echo python create_icons.py >> offline_installer\install_offline.bat
echo echo. >> offline_installer\install_offline.bat
echo echo Installation complete! Run run.bat to start. >> offline_installer\install_offline.bat
echo pause >> offline_installer\install_offline.bat

echo.
echo Creating ZIP archive...
cd offline_installer
powershell Compress-Archive -Path * -DestinationPath ../Votobu-Offline-Installer-v1.0.2.zip -Force
cd ..

echo.
echo ========================================
echo   Offline Installer Created!
echo ========================================
echo.
echo Package created: Votobu-Offline-Installer-v1.0.2.zip
echo.
echo To use on another computer:
echo   1. Extract the ZIP file
echo   2. Run install_offline.bat
echo   3. Run run.bat
echo.
echo This package includes all dependencies and works without internet!
echo (Except for first Whisper model download ~150MB)
echo.
pause


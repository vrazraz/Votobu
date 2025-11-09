@echo off
echo ========================================
echo   Git Initialization for Votobu
echo ========================================
echo.
echo This will initialize Git and prepare for first push
echo.
pause

echo.
echo [1/5] Initializing Git repository...
git init

echo.
echo [2/5] Configuring Git...
echo.
set /p username="Enter your GitHub username: "
set /p email="Enter your email: "

git config user.name "%username%"
git config user.email "%email%"

echo.
echo [3/5] Adding files to Git...
git add .

echo.
echo [4/5] Creating initial commit...
git commit -m "🎉 Initial commit: Votobu v1.0.2 - Voice-to-Text Hotkey Application"

echo.
echo [5/5] Setup complete!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Create repository on GitHub.com:
echo    - Go to: https://github.com/new
echo    - Name: Votobu
echo    - Description: Voice-to-Text Hotkey Application
echo    - Public repository
echo    - Do NOT add README, .gitignore, or LICENSE
echo.
echo 2. Connect to GitHub:
echo    git remote add origin https://github.com/%username%/Votobu.git
echo.
echo 3. Push to GitHub:
echo    git branch -M main
echo    git push -u origin main
echo.
echo See GITHUB_GUIDE.md for detailed instructions
echo.
pause


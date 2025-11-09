@echo off
echo ========================================
echo   Creating Desktop Shortcut
echo ========================================
echo.

REM Get current directory
set "CURRENT_DIR=%CD%"

REM Create VBScript to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Votobu.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CURRENT_DIR%\Votobu.vbs" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%CURRENT_DIR%\assets\icon.png" >> CreateShortcut.vbs
echo oLink.Description = "Votobu - Voice to Text" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Run VBScript
cscript CreateShortcut.vbs

REM Cleanup
del CreateShortcut.vbs

echo.
echo Desktop shortcut created!
echo Double-click "Votobu" on your desktop to run without console.
echo.
pause


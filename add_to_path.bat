@echo off
SET "TARGET_DIR=C:\zipper"

echo Checking if %TARGET_DIR% is in your PATH...
echo %PATH% | find /I "%TARGET_DIR%" >nul
IF %ERRORLEVEL% EQU 0 (
    echo %TARGET_DIR% is already in your PATH.
) ELSE (
    echo Adding %TARGET_DIR% to your PATH...
    REM %PATH% represents the current session PATH; setx updates the registry.
    setx PATH "%PATH%;%TARGET_DIR%"
    echo Done. You must open a new CMD window for the changes to take effect.
)
pause
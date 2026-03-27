@echo off
setlocal
cd /d "%~dp0"

echo === pdf-layout-diff Windows build ===
echo.

echo Installing Python dependencies ...
python -m pip install -r requirements.txt pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Dependency installation FAILED
    exit /b 1
)

echo Building with PyInstaller ...
pyinstaller compare_pdfs.spec --noconfirm --clean

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo BUILD FAILED
    exit /b 1
)

echo.
echo Build complete!
echo Output: dist\compare_pdfs\
echo.
echo Usage:
echo   dist\compare_pdfs\compare_pdfs.exe --old-dir OLD --new-dir NEW --output-dir OUT
echo.
pause

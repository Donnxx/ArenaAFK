@echo off
echo Installing Arena Queue Detector...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Checking for Tesseract OCR...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo Tesseract OCR not found!
    echo Please install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo After installing Tesseract, run this script again.
    pause
    exit /b 1
)

echo.
echo ✓ Installation complete!
echo ✓ You can now run: python ARENAGUI.py
echo.
pause

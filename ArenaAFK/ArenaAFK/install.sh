#!/bin/bash
echo "Installing Arena Queue Detector..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "Python found! Installing dependencies..."
python3 -m pip install -r requirements.txt

echo
echo "Checking for Tesseract OCR..."
if ! command -v tesseract &> /dev/null; then
    echo "Tesseract OCR not found!"
    echo "Please install Tesseract:"
    echo "  macOS: brew install tesseract"
    echo "  Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "  CentOS/RHEL: sudo yum install tesseract"
    exit 1
fi

echo
echo "✓ Installation complete!"
echo "✓ You can now run: python3 ARENAGUI.py"
echo

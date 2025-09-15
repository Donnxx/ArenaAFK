#!/usr/bin/env python3
"""
Setup script for Arena Queue Detector
"""

import os
import sys
import subprocess
import platform

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Python requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python requirements: {e}")
        return False

def check_tesseract():
    """Check if Tesseract is installed"""
    print("Checking for Tesseract OCR...")
    system = platform.system()
    
    try:
        result = subprocess.run(["tesseract", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Tesseract OCR is installed and accessible")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ Tesseract OCR not found")
    print("\nPlease install Tesseract OCR:")
    
    if system == "Windows":
        print("• Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("• Or use chocolatey: choco install tesseract")
    elif system == "Darwin":  # macOS
        print("• Run: brew install tesseract")
    else:  # Linux
        print("• Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("• CentOS/RHEL: sudo yum install tesseract")
        print("• Arch: sudo pacman -S tesseract")
    
    return False

def main():
    """Main setup function"""
    print("Arena Queue Detector Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("✗ Python 3.6 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        print("Setup failed during requirements installation")
        sys.exit(1)
    
    # Check Tesseract
    tesseract_ok = check_tesseract()
    
    print("\n" + "=" * 30)
    if tesseract_ok:
        print("✓ Setup completed successfully!")
        print("You can now run: python ARENAGUI.py")
    else:
        print("⚠ Setup completed with warnings")
        print("Please install Tesseract OCR before running the application")
    
    print("\nFor help, see the README.md file")

if __name__ == "__main__":
    main()

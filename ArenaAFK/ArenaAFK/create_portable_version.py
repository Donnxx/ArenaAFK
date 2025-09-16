#!/usr/bin/env python3
"""
Create a portable version that includes everything needed
This creates a folder with the app + all dependencies bundled
"""

import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path

def create_portable_version():
    """Create a portable version with all dependencies"""
    print("Creating portable version...")
    
    # Create portable directory
    portable_dir = "ArenaQueueDetector_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # Copy main application
    shutil.copy2("ARENAGUI.py", portable_dir)
    print("✓ Added main application")
    
    # Copy essential files
    files_to_include = [
        "requirements.txt",
        "README.md",
        "LICENSE",
        "icon.ico",
        "setup.py"
    ]
    
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, file, portable_dir)
            print(f"✓ Added {file}")
    
    # Create a portable launcher script
    launcher_content = f'''@echo off
echo Arena Queue Detector - Portable Version
echo ======================================
echo.
echo Setting up portable environment...

REM Create virtual environment
python -m venv venv
call venv\\Scripts\\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Run the application
python ARENAGUI.py

pause
'''
    
    with open(os.path.join(portable_dir, "RUN_PORTABLE.bat"), "w") as f:
        f.write(launcher_content)
    print("✓ Added portable launcher")
    
    # Create Unix launcher
    unix_launcher = '''#!/bin/bash
echo "Arena Queue Detector - Portable Version"
echo "======================================"
echo ""
echo "Setting up portable environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 ARENAGUI.py
'''
    
    with open(os.path.join(portable_dir, "run_portable.sh"), "w") as f:
        f.write(unix_launcher)
    
    # Make it executable on Unix systems
    if platform.system() != "Windows":
        os.chmod(os.path.join(portable_dir, "run_portable.sh"), 0o755)
    print("✓ Added Unix launcher")
    
    # Create portable README
    portable_readme = """# Arena Queue Detector - Portable Version

## 🚀 Super Easy Setup

### Windows:
1. Double-click `RUN_PORTABLE.bat`
2. Wait for setup to complete
3. Enter your Discord settings when prompted

### macOS/Linux:
1. Open terminal in this folder
2. Run: `chmod +x run_portable.sh && ./run_portable.sh`
3. Enter your Discord settings when prompted

## ✨ What This Includes:
- ✅ Complete Python application
- ✅ All dependencies (auto-installed)
- ✅ Virtual environment (isolated)
- ✅ No system-wide installation needed

## 📋 Prerequisites:
- Python 3.6+ installed on your system
- Tesseract OCR installed
- Discord webhook URL and User ID

## 🎯 Perfect For:
- Users who want everything in one folder
- No admin rights needed
- Easy to share and backup
- Works on any computer with Python

---
This portable version creates its own isolated environment!
"""
    
    with open(os.path.join(portable_dir, "PORTABLE_README.txt"), "w") as f:
        f.write(portable_readme)
    print("✓ Added portable documentation")
    
    print(f"\n🎉 Portable version created in: {portable_dir}")
    print("📁 Users can download this entire folder and run it anywhere!")
    return portable_dir

def main():
    """Main function"""
    print("Arena Queue Detector - Portable Version Creator")
    print("=" * 50)
    
    portable_dir = create_portable_version()
    if portable_dir:
        print(f"\n✅ Success! Portable version ready in: {portable_dir}")
        print("📤 Zip this folder and upload to GitHub")
        print("👥 Users get everything they need in one download!")

if __name__ == "__main__":
    main()


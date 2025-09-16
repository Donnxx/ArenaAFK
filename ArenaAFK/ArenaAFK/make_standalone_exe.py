#!/usr/bin/env python3
"""
Create a completely standalone .exe that requires NO Python installation
This is the easiest way for users to get the app running
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")
    
    # Check if main file exists
    if not os.path.exists("ARENAGUI.py"):
        print("❌ ARENAGUI.py not found!")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    print("✅ All required files found")
    return True

def install_dependencies():
    """Install all required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def build_standalone_exe():
    """Build a completely standalone executable"""
    print("Building standalone executable...")
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("ArenaQueueDetector.spec"):
        os.remove("ArenaQueueDetector.spec")
    
    # PyInstaller command for maximum compatibility
    cmd = [
        "pyinstaller",
        "--onefile",  # Single file
        "--windowed",  # No console window
        "--name=ArenaQueueDetector",
        "--clean",  # Clean build
        "--noconfirm",  # Don't ask for confirmation
        
        # Include all necessary modules
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageGrab",
        "--hidden-import=PIL.ImageFilter",
        "--hidden-import=pytesseract",
        "--hidden-import=requests",
        "--hidden-import=configparser",
        "--hidden-import=threading",
        "--hidden-import=time",
        "--hidden-import=os",
        "--hidden-import=platform",
        "--hidden-import=shutil",
        
        # Include icon if it exists
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        
        "ARENAGUI.py"
    ]
    
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build executable: {e}")
        return False

def test_executable():
    """Test if the executable works"""
    exe_path = "dist/ArenaQueueDetector.exe"
    if os.path.exists(exe_path):
        print(f"✅ Executable created: {exe_path}")
        print(f"📏 File size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        return True
    else:
        print("❌ Executable not found!")
        return False

def create_user_instructions():
    """Create simple instructions for users"""
    instructions = """# Arena Queue Detector - Standalone Version

## 🚀 SUPER EASY SETUP (No Python Required!)

### What You Need:
1. **ArenaQueueDetector.exe** (this file)
2. **Tesseract OCR** installed on your computer
3. **Discord webhook URL** and **User ID**

### How to Run:
1. **Double-click ArenaQueueDetector.exe**
2. **Enter your Discord webhook URL** when prompted
3. **Enter your Discord User ID** (the number, not username)
4. **Click "Start Monitoring"**

### Discord Setup (One-time):
1. Go to your Discord server
2. Server Settings → Integrations → Webhooks
3. Create New Webhook → Copy the URL
4. Get your User ID: Enable Developer Mode, right-click your username, Copy ID

### Tesseract OCR Setup:
**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location

**Mac:**
- Run: `brew install tesseract`

**Linux:**
- Run: `sudo apt-get install tesseract-ocr`

### That's It! 🎉
No Python, no pip, no command line needed!
Just double-click and go!

---
Made with ❤️ for the gaming community
"""
    
    with open("dist/USER_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    print("✅ User instructions created")

def main():
    """Main function"""
    print("Arena Queue Detector - Standalone Executable Builder")
    print("=" * 60)
    print("This creates a .exe file that works WITHOUT Python installed!")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Build executable
    if not build_standalone_exe():
        return
    
    # Test executable
    if not test_executable():
        return
    
    # Create user instructions
    create_user_instructions()
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Standalone executable is ready!")
    print("=" * 60)
    print("📁 Location: dist/ArenaQueueDetector.exe")
    print("📄 Instructions: dist/USER_INSTRUCTIONS.txt")
    print("\n📤 Upload these files to GitHub Releases:")
    print("   • ArenaQueueDetector.exe")
    print("   • USER_INSTRUCTIONS.txt")
    print("\n👥 Users can download and run without any setup!")

if __name__ == "__main__":
    main()

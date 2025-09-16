#!/usr/bin/env python3
"""
Script to build an executable version of Arena Queue Detector
This creates a single .exe file that users can run without installing Python
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install PyInstaller: {e}")
            return False

def build_executable():
    """Build the executable file"""
    print("Building executable...")
    
    # PyInstaller command with options for standalone executable
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Hide console window (GUI app)
        "--name=ArenaQueueDetector",  # Name of the executable
        "--icon=icon.ico",  # Icon file (optional)
        "--add-data", "icon.ico;.",  # Include icon in the executable
        "--hidden-import", "tkinter",  # Ensure tkinter is included
        "--hidden-import", "PIL",  # Ensure PIL is included
        "--hidden-import", "pytesseract",  # Ensure pytesseract is included
        "--hidden-import", "requests",  # Ensure requests is included
        "--hidden-import", "configparser",  # Ensure configparser is included
        "--clean",  # Clean cache before building
        "ARENAGUI.py"
    ]
    
    # Remove icon option if icon file doesn't exist
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
        print("Note: No icon.ico found, building without custom icon")
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        print("✓ Find your executable in the 'dist' folder")
        print("✓ You can now share the .exe file with others")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build executable: {e}")
        return False

def main():
    """Main function"""
    print("Arena Queue Detector - Executable Builder")
    print("=" * 40)
    
    # Install PyInstaller
    if not install_pyinstaller():
        print("Cannot build executable without PyInstaller")
        return
    
    # Build the executable
    if build_executable():
        print("\n🎉 Success! Your executable is ready to share!")
        print("📁 Look in the 'dist' folder for 'ArenaQueueDetector.exe'")
        print("📤 You can upload this .exe file to GitHub as a release")
    else:
        print("\n❌ Failed to build executable")

if __name__ == "__main__":
    main()

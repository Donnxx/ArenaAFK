#!/usr/bin/env python3
"""
Create a complete release package with everything users need
This creates a zip file with the executable + all necessary files
"""

import os
import zipfile
import shutil
import subprocess
import sys
from datetime import datetime

def build_executable():
    """Build the executable using the existing build script"""
    print("Building executable...")
    try:
        subprocess.check_call([sys.executable, "build_executable.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build executable: {e}")
        return False

def create_release_package():
    """Create a complete release package"""
    print("Creating release package...")
    
    # Create release directory
    release_dir = "ArenaQueueDetector_Release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy executable
    if os.path.exists("dist/ArenaQueueDetector.exe"):
        shutil.copy2("dist/ArenaQueueDetector.exe", release_dir)
        print("✓ Added executable")
    else:
        print("❌ Executable not found. Run build first.")
        return False
    
    # Copy essential files
    files_to_include = [
        "README.md",
        "LICENSE",
        "icon.ico"
    ]
    
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"✓ Added {file}")
    
    # Create a simple setup guide
    setup_guide = """# Arena Queue Detector - Quick Start

## 🚀 Super Easy Setup (2 minutes!)

1. **Double-click ArenaQueueDetector.exe** - that's it!
2. **Enter your Discord webhook URL** when prompted
3. **Enter your Discord User ID** (the number, not username)
4. **Click "Start Monitoring"**

## 📋 What You Need First:
- Discord webhook URL (from your server settings)
- Your Discord User ID (right-click your username → Copy ID)

## 🎮 How to Get Discord Setup:
1. Go to your Discord server
2. Server Settings → Integrations → Webhooks
3. Create New Webhook
4. Copy the webhook URL
5. Get your User ID (enable Developer Mode, right-click your username)

## ⚠️ Important Notes:
- Make sure Tesseract OCR is installed on your system
- The app monitors a specific screen area for "Enter Arena" text
- You'll get Discord notifications when queues are ready!

## 🆘 Need Help?
Check the full README.md for detailed instructions and troubleshooting.

---
Made with ❤️ for the gaming community
"""
    
    with open(os.path.join(release_dir, "QUICK_START.txt"), "w") as f:
        f.write(setup_guide)
    print("✓ Added quick start guide")
    
    # Create zip file
    zip_name = f"ArenaQueueDetector_v{datetime.now().strftime('%Y%m%d')}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    print(f"✓ Created release package: {zip_name}")
    return zip_name

def main():
    """Main function"""
    print("Arena Queue Detector - Release Package Creator")
    print("=" * 50)
    
    # Build executable first
    if not build_executable():
        print("❌ Cannot create package without executable")
        return
    
    # Create release package
    zip_file = create_release_package()
    if zip_file:
        print(f"\n🎉 Success! Release package created: {zip_file}")
        print("📤 Upload this zip file to GitHub as a release")
        print("👥 Users can download and extract to get started instantly!")
    else:
        print("\n❌ Failed to create release package")

if __name__ == "__main__":
    main()

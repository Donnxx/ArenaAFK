#!/usr/bin/env python3
"""
Build all versions of Arena Queue Detector for easy distribution
This creates multiple download options for different user needs
"""

import os
import subprocess
import sys
from datetime import datetime

def run_script(script_name, description):
    """Run a build script and report results"""
    print(f"\n{'='*50}")
    print(f"Building: {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print("✅ SUCCESS!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Build all versions"""
    print("Arena Queue Detector - All Versions Builder")
    print("=" * 60)
    print("This will create multiple download options for users:")
    print("1. Single executable (.exe)")
    print("2. Complete release package (.zip)")
    print("3. Portable version (folder)")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("ARENAGUI.py"):
        print("❌ Error: ARENAGUI.py not found. Run this from the project root.")
        return
    
    # Build all versions
    builds = [
        ("build_executable.py", "Single Executable (.exe)"),
        ("create_release_package.py", "Release Package (.zip)"),
        ("create_portable_version.py", "Portable Version (folder)")
    ]
    
    results = []
    for script, description in builds:
        success = run_script(script, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("BUILD SUMMARY")
    print(f"{'='*60}")
    
    for description, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{description:<30} {status}")
    
    # Instructions for GitHub
    print(f"\n{'='*60}")
    print("NEXT STEPS FOR GITHUB RELEASE:")
    print(f"{'='*60}")
    print("1. Go to your GitHub repository")
    print("2. Click 'Releases' → 'Create a new release'")
    print("3. Upload these files:")
    
    if os.path.exists("dist/ArenaQueueDetector.exe"):
        print("   • dist/ArenaQueueDetector.exe (single executable)")
    
    if os.path.exists("ArenaQueueDetector_Release"):
        print("   • ArenaQueueDetector_Release/ (zip this folder)")
    
    if os.path.exists("ArenaQueueDetector_Portable"):
        print("   • ArenaQueueDetector_Portable/ (zip this folder)")
    
    print("\n4. Users can choose their preferred download method!")
    print("5. Update README.md to point to the release files")

if __name__ == "__main__":
    main()

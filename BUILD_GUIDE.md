# Build Guide - Arena Queue Detector

This guide shows you how to create executable files for distribution.

## Quick Start (Easiest)

```bash
python make_standalone_exe.py
```

**That's it!** This script handles everything automatically.

## What You Need

- Python 3.6+ installed
- Internet connection (for downloading dependencies)
- Windows (for .exe files)

## Build Options

### Option 1: Super Easy Build
```bash
python make_standalone_exe.py
```
**Creates:**
- `dist/ArenaQueueDetector.exe` - Standalone executable
- `dist/USER_INSTRUCTIONS.txt` - User guide

### Option 2: Original Build
```bash
python build_executable.py
```
**Creates:**
- `dist/ArenaQueueDetector.exe` - Standalone executable

### Option 3: All Versions
```bash
python build_all_versions.py
```
**Creates:**
- Single .exe file
- Complete release package (.zip)
- Portable version (folder)

## Output Files

After building, you'll find:

```
dist/
├── ArenaQueueDetector.exe          # Main executable
└── USER_INSTRUCTIONS.txt           # User guide

ArenaQueueDetector_Release/         # Complete package
├── ArenaQueueDetector.exe
├── README.md
├── LICENSE
├── icon.ico
└── QUICK_START.txt

ArenaQueueDetector_Portable/        # Portable version
├── ARENAGUI.py
├── requirements.txt
├── RUN_PORTABLE.bat
├── run_portable.sh
└── PORTABLE_README.txt
```

## Uploading to GitHub

1. **Run build script:**
   ```bash
   python make_standalone_exe.py
   ```

2. **Go to GitHub:**
   - Repository → Releases → Create new release

3. **Upload files:**
   - `ArenaQueueDetector.exe`
   - `USER_INSTRUCTIONS.txt`

4. **Users download and run!**

## Troubleshooting

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Icon not found"
- The app works without an icon
- Add `icon.ico` to the project root for custom icon

### Large file size
- This is normal for standalone executables
- All Python libraries are bundled inside
- Users don't need Python installed

## Testing Your Build

1. **Copy the .exe to a clean folder**
2. **Double-click to run**
3. **Test the GUI and Discord integration**
4. **Verify it works without Python installed**

## Distribution Tips

- **Test on different Windows versions**
- **Include clear instructions**
- **Provide multiple download options**
- **Update version numbers in releases**

---

**Need help?** Check the main README.md or create an issue on GitHub!


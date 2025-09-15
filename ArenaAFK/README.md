# Arena Queue Detector

A Python application that monitors for arena queue availability in games and sends Discord notifications when queues are ready.

## Features

- 🔍 **OCR Detection**: Uses Tesseract OCR to detect "Enter Arena" text on screen
- 🔔 **Discord Integration**: Sends notifications via Discord webhooks
- ⚙️ **Configurable**: Saves settings to config file for convenience
- 🖼️ **Debug Tools**: Includes OCR testing functionality
- 🎯 **Precise Monitoring**: Monitors specific screen regions for optimal detection

## Prerequisites

### 1. Install Tesseract OCR

**Windows:**
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`)
3. The app will automatically detect this path

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### 2. Python Dependencies

**Option 1: Automated Setup (Recommended)**
```bash
python setup.py
```

**Option 2: Manual Installation**
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Clone or download this repository**
2. **Run the setup script**: `python setup.py`
3. **Configure Discord webhook** (see setup section below)
4. **Run the application**: `python ARENAGUI.py`

## Setup

### 1. Discord Webhook Setup

1. Go to your Discord server settings
2. Navigate to "Integrations" → "Webhooks"
3. Click "New Webhook"
4. Copy the webhook URL
5. Get your Discord User ID (enable Developer Mode in Discord, right-click your username, copy ID)

### 2. Configuration

1. Run the application: `python ARENAGUI.py`
2. Enter your Discord webhook URL
3. Enter your Discord User ID (the number, not your username)
4. Click "Start Monitoring"

Your settings will be automatically saved to `config.ini`.

## Usage

### Basic Operation

1. **Start Monitoring**: Click "Start Monitoring" to begin watching for arena queues
2. **Stop Monitoring**: Click "Stop Monitoring" to stop the detection
3. **Test OCR**: Use "Test OCR Area" to see what text is being detected in the monitoring area

### Monitoring Area

The app monitors a specific screen region:
- **Coordinates**: (751, 186) to (1175, 403)
- **Size**: 424x217 pixels

This area should contain the "Enter Arena" button when a queue is ready.

### Discord Notifications

When a queue is detected, the app will:
- Send a message to your Discord channel via webhook
- Mention your user ID with: `⚔️ Arena queue popped! Click 'Enter Arena' now! @username`
- Include a 15-second cooldown to prevent spam

## Troubleshooting

### OCR Not Working

1. Use the "Test OCR Area" button to see what text is being detected
2. Check that the monitoring area contains the "Enter Arena" button
3. Ensure good contrast in the game's UI
4. Try adjusting the game's resolution or UI scaling

### Discord Messages Not Sending

1. Verify your webhook URL is correct
2. Check that your Discord User ID is a number (not username)
3. Ensure the webhook has permission to send messages in the channel

### Common Issues

- **"Could not load icon.ico"**: This is normal if you don't have an icon file
- **OCR errors**: Make sure Tesseract is installed correctly
- **Screen detection issues**: The coordinates are optimized for specific game resolutions

## Configuration File

Settings are saved in `config.ini`:
```ini
[Settings]
webhook_url = your_webhook_url_here
mention_id = your_discord_user_id_here
```

## System Requirements

- Python 3.6+
- Windows/macOS/Linux
- Tesseract OCR
- Discord webhook access

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application!

## GitHub Repository

This project is ready to be shared on GitHub! The repository includes:

- ✅ Complete source code with cross-platform compatibility
- ✅ Comprehensive documentation and setup instructions  
- ✅ Automated setup script for easy installation
- ✅ Proper error handling and user feedback
- ✅ MIT license for open source sharing
- ✅ `.gitignore` file to exclude unnecessary files

### Repository Structure

```
ArenaAFK/
├── ARENAGUI.py          # Main application
├── setup.py             # Automated setup script
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── LICENSE             # MIT license
├── .gitignore          # Git ignore rules
└── config.ini          # User settings (created on first run)
```

## License

MIT License - feel free to use and modify as needed.

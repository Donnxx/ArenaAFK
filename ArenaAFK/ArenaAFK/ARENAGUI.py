import tkinter as tk
from tkinter import messagebox
import threading
import time
import requests
import pytesseract
from PIL import ImageGrab, ImageFilter, Image
import os
import configparser
import platform
import shutil


# Configure Tesseract path based on operating system
def setup_tesseract():
    """Setup Tesseract OCR path based on the operating system"""
    system = platform.system()
    
    if system == "Windows":
        # Common Windows installation paths
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', ''))
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",
            "/usr/bin/tesseract"
        ]
    else:  # Linux
        possible_paths = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract"
        ]
    
    # Try to find tesseract in common locations
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return True
    
    # Fallback to checking possible paths
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    
    return False

# Setup Tesseract
tesseract_found = setup_tesseract()
CHECK_INTERVAL = 1
CONFIG_FILE = "config.ini"

class ArenaQueueDetectorApp:
    def __init__(self, root):
        self.root = root
        root.title("Arena Queue Detector")

        # Check if Tesseract is available
        if not tesseract_found:
            messagebox.showerror("Tesseract Not Found", 
                               "Tesseract OCR is not installed or not found in PATH.\n\n"
                               "Please install Tesseract OCR:\n"
                               "Windows: https://github.com/UB-Mannheim/tesseract/wiki\n"
                               "macOS: brew install tesseract\n"
                               "Linux: sudo apt-get install tesseract-ocr")

        # Config parser
        self.config = configparser.ConfigParser()
        self.load_config()

        tk.Label(root, text="Discord Webhook URL:").pack()
        self.webhook_entry = tk.Entry(root, width=60)
        self.webhook_entry.pack()
        self.webhook_entry.insert(0, self.webhook_url or "")

        tk.Label(root, text="Discord User ID to Mention:").pack()
        self.userid_entry = tk.Entry(root, width=30)
        self.userid_entry.pack()
        self.userid_entry.insert(0, self.mention_id or "")

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitor)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitor, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.test_button = tk.Button(root, text="Test OCR Area", command=self.test_ocr_area)
        self.test_button.pack(pady=5)

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.pack()

        self.monitoring = False

    def load_config(self):
        self.webhook_url = None
        self.mention_id = None
        if os.path.exists(CONFIG_FILE):
            try:
                self.config.read(CONFIG_FILE)
                self.webhook_url = self.config.get("Settings", "webhook_url", fallback=None)
                self.mention_id = self.config.get("Settings", "mention_id", fallback=None)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        if "Settings" not in self.config.sections():
            self.config.add_section("Settings")
        self.config.set("Settings", "webhook_url", self.webhook_entry.get().strip())
        self.config.set("Settings", "mention_id", self.userid_entry.get().strip())
        try:
            with open(CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"Error saving config: {e}")

    def send_discord_message(self, webhook_url, mention_id):
        content = f"⚔️ Arena queue popped! Click 'Enter Arena' now! <@{mention_id}>"
        try:
            requests.post(webhook_url, json={"content": content})
        except Exception as e:
            print(f"Failed to send Discord message: {e}")

    def monitor_loop(self, webhook_url, mention_id):
        if not tesseract_found:
            self.status_label.config(text="Status: Error - Tesseract not found")
            return
            
        self.status_label.config(text="Status: Monitoring...")
        bbox = (751, 186, 751 + 424, 186 + 217)

        while self.monitoring:
            screenshot = ImageGrab.grab(bbox=bbox)
            gray_img = screenshot.convert('L')
            gray_img = gray_img.resize((screenshot.width * 3, screenshot.height * 3), Image.LANCZOS)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)

            found_enter = False
            for thresh in [100, 130, 150, 180]:
                img = gray_img.point(lambda x: 0 if x < thresh else 255, '1')
                for psm in [6, 7, 8]:
                    try:
                        text = pytesseract.image_to_string(img, config=f'--psm {psm}').lower().strip()
                        print(f"OCR detected text: '{text}'")  # Debug output
                        
                        # Check for various forms of "enter" text
                        enter_variations = ["enter", "enter arena", "enter arena!", "enter!", "enter arena.", "enter."]
                        if any(variation in text for variation in enter_variations):
                            print(f"Detected 'Enter' variation: '{text}'. Sending Discord alert...")
                            self.send_discord_message(webhook_url, mention_id)
                            found_enter = True
                            break
                    except Exception as e:
                        print(f"OCR error: {e}")
                if found_enter:
                    break

            if found_enter:
                time.sleep(15)  # cooldown to avoid spam

            time.sleep(CHECK_INTERVAL)

        self.status_label.config(text="Status: Stopped")

    def start_monitor(self):
        if not tesseract_found:
            messagebox.showerror("Tesseract Not Available", "Cannot start monitoring without Tesseract OCR installed.")
            return
            
        webhook_url = self.webhook_entry.get().strip()
        mention_id = self.userid_entry.get().strip()

        if not webhook_url or not mention_id:
            messagebox.showerror("Error", "Please enter both the webhook URL and user ID.")
            return

        if self.monitoring:
            messagebox.showinfo("Info", "Already monitoring!")
            return

        self.save_config()

        self.monitoring = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.monitor_loop, args=(webhook_url, mention_id), daemon=True).start()

    def test_ocr_area(self):
        """Test the OCR area to see what text is being detected"""
        if not tesseract_found:
            messagebox.showerror("Tesseract Not Available", "Tesseract OCR is not installed or not found in PATH.")
            return
            
        bbox = (751, 186, 751 + 424, 186 + 217)
        try:
            screenshot = ImageGrab.grab(bbox=bbox)
            gray_img = screenshot.convert('L')
            gray_img = gray_img.resize((screenshot.width * 3, screenshot.height * 3), Image.LANCZOS)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)
            
            # Save the processed image for debugging
            screenshot.save("debug_screenshot.png")
            gray_img.save("debug_processed.png")
            
            print("Screenshots saved as debug_screenshot.png and debug_processed.png")
            
            # Test OCR with different settings
            ocr_results = []
            for thresh in [100, 130, 150, 180]:
                img = gray_img.point(lambda x: 0 if x < thresh else 255, '1')
                for psm in [6, 7, 8]:
                    try:
                        text = pytesseract.image_to_string(img, config=f'--psm {psm}').strip()
                        result = f"Threshold: {thresh}, PSM: {psm} -> Text: '{text}'"
                        print(result)
                        ocr_results.append(result)
                    except Exception as e:
                        error_msg = f"OCR error with thresh {thresh}, psm {psm}: {e}"
                        print(error_msg)
                        ocr_results.append(error_msg)
            
            # Show results in a dialog
            results_text = "\n".join(ocr_results[:10])  # Show first 10 results
            if len(ocr_results) > 10:
                results_text += f"\n... and {len(ocr_results) - 10} more results"
            
            messagebox.showinfo("OCR Test Complete", 
                              f"OCR test completed. Check console output and saved images.\n\n"
                              f"First few results:\n{results_text}")
            
        except Exception as e:
            messagebox.showerror("Test Error", f"Error testing OCR area: {e}")

    def stop_monitor(self):
        if not self.monitoring:
            return
        self.monitoring = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopping...")

def on_closing():
    app.stop_monitor()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("icon.ico")
    except:
        print("Warning: Could not load icon.ico")
    app = ArenaQueueDetectorApp(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

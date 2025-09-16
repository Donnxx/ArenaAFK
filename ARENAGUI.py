import tkinter as tk
from tkinter import messagebox
import threading
import time
import requests
import pytesseract
from pytesseract import Output
from PIL import ImageGrab, ImageFilter, Image, ImageOps
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

        # Reminder controls
        self.enable_reminders_var = tk.BooleanVar(value=False)
        self.reminder_check = tk.Checkbutton(root, text="Enable periodic Discord reminder to move your character", variable=self.enable_reminders_var)
        self.reminder_check.pack(pady=2)

        tk.Label(root, text="Reminder interval (minutes):").pack()
        self.reminder_interval_entry = tk.Entry(root, width=10)
        self.reminder_interval_entry.pack()
        self.reminder_interval_entry.insert(0, str(self.reminder_interval_minutes if hasattr(self, 'reminder_interval_minutes') and self.reminder_interval_minutes else 5))

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.pack()

        self.monitoring = False

    def _normalize_ocr_text(self, text):
        try:
            cleaned = ''.join(ch for ch in text.lower() if ch.isalnum() or ch.isspace())
            return ' '.join(cleaned.split())
        except Exception:
            return text.lower().strip()

    def load_config(self):
        self.webhook_url = None
        self.mention_id = None
        self.reminders_enabled = False
        self.reminder_interval_minutes = 5
        if os.path.exists(CONFIG_FILE):
            try:
                self.config.read(CONFIG_FILE)
                self.webhook_url = self.config.get("Settings", "webhook_url", fallback=None)
                self.mention_id = self.config.get("Settings", "mention_id", fallback=None)
                self.reminders_enabled = self.config.getboolean("Settings", "reminders_enabled", fallback=False)
                self.reminder_interval_minutes = self.config.getint("Settings", "reminder_interval_minutes", fallback=5)
            except Exception as e:
                print(f"Error loading config: {e}")
        # Reflect loaded config into UI-related vars if UI already created
        try:
            self.enable_reminders_var.set(self.reminders_enabled)
        except Exception:
            pass

    def save_config(self):
        if "Settings" not in self.config.sections():
            self.config.add_section("Settings")
        self.config.set("Settings", "webhook_url", self.webhook_entry.get().strip())
        self.config.set("Settings", "mention_id", self.userid_entry.get().strip())
        self.config.set("Settings", "reminders_enabled", str(self.enable_reminders_var.get()))
        try:
            interval_val = int(self.reminder_interval_entry.get().strip())
            if interval_val <= 0:
                interval_val = 5
        except Exception:
            interval_val = 5
        self.config.set("Settings", "reminder_interval_minutes", str(interval_val))
        try:
            with open(CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"Error saving config: {e}")

    def send_discord_message(self, webhook_url, mention_id, content=None):
        if content is None:
            content = f"Arena queue popped! Click 'Enter Arena' now! <@{mention_id}>"
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
        # Reminder configuration
        try:
            reminders_enabled = self.enable_reminders_var.get()
        except Exception:
            reminders_enabled = False
        try:
            reminder_interval_minutes = int(self.reminder_interval_entry.get().strip())
            if reminder_interval_minutes <= 0:
                reminder_interval_minutes = 5
        except Exception:
            reminder_interval_minutes = 5
        reminder_interval_seconds = reminder_interval_minutes * 60
        last_reminder_time = 0

        while self.monitoring:
            screenshot = ImageGrab.grab(bbox=bbox)
            gray_img = screenshot.convert('L')
            # Scale up for better OCR
            gray_img = gray_img.resize((screenshot.width * 4, screenshot.height * 4), Image.LANCZOS)
            # Enhance contrast
            gray_img = ImageOps.autocontrast(gray_img, cutoff=2)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)

            found_enter = False
            best_hit = None
            for thresh in [90, 110, 130, 150, 170, 190, 210]:
                for invert in [False, True]:
                    if not invert:
                        img = gray_img.point(lambda x: 0 if x < thresh else 255, '1')
                    else:
                        inv = ImageOps.invert(gray_img)
                        img = inv.point(lambda x: 0 if x < thresh else 255, '1')

                    for psm in [6, 7, 8, 11, 12, 13]:
                        try:
                            tesseract_config = f"--oem 1 --psm {psm} -l eng -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !."
                            data = pytesseract.image_to_data(img, config=tesseract_config, output_type=Output.DICT)
                            words = data.get('text', [])
                            confs = data.get('conf', [])
                            # Filter words by confidence
                            candidates = []
                            for w, c in zip(words, confs):
                                try:
                                    cval = float(c)
                                except Exception:
                                    cval = -1
                                w_norm = self._normalize_ocr_text(w)
                                if w_norm and cval >= 70:  # confidence threshold
                                    candidates.append((w_norm, cval))
                            if candidates:
                                # Reduce logging noise: show top few candidates
                                print(f"OCR candidates (psm {psm}, thresh {thresh}, invert {invert}): {candidates[:5]}")
                            # Compose a normalized line to match multi-word phrases
                            full_norm = self._normalize_ocr_text(' '.join(words))
                            keywords = [
                                "enter", "enter arena", "enter arena now", "enter arena!", "enter!",
                                "accept", "accept match", "accept queue", "accept now", "accept!"
                            ]
                            if any(k in full_norm for k in keywords) or any(any(k in w for k in keywords) for w, _ in candidates):
                                best_hit = (full_norm, psm, thresh, invert)
                                found_enter = True
                                break
                        except Exception as e:
                            # Only log occasional errors
                            print(f"OCR error (psm {psm}, thresh {thresh}, invert {invert}): {e}")
                    if found_enter:
                        break
                if found_enter:
                    break

            if found_enter:
                if best_hit:
                    print(f"Detected actionable keyword in OCR (hit): '{best_hit[0]}' [psm={best_hit[1]} thresh={best_hit[2]} invert={best_hit[3]}]")
                self.send_discord_message(webhook_url, mention_id)
                time.sleep(15)  # cooldown to avoid spam

            # Periodic reminder to move character while waiting
            if not found_enter and reminders_enabled:
                now = time.time()
                if now - last_reminder_time >= reminder_interval_seconds:
                    reminder_msg = f"Reminder: Move your character to avoid logout while in queue. <@{mention_id}>"
                    print("Sending periodic reminder to Discord")
                    self.send_discord_message(webhook_url, mention_id, content=reminder_msg)
                    last_reminder_time = now

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
            gray_img = gray_img.resize((screenshot.width * 4, screenshot.height * 4), Image.LANCZOS)
            gray_img = ImageOps.autocontrast(gray_img, cutoff=2)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)
            gray_img = gray_img.filter(ImageFilter.SHARPEN)
            
            # Save the processed image for debugging
            screenshot.save("debug_screenshot.png")
            gray_img.save("debug_processed.png")
            
            print("Screenshots saved as debug_screenshot.png and debug_processed.png")
            
            # Test OCR with different settings
            ocr_results = []
            for thresh in [90, 110, 130, 150, 170, 190, 210]:
                for invert in [False, True]:
                    if not invert:
                        img = gray_img.point(lambda x: 0 if x < thresh else 255, '1')
                    else:
                        inv = ImageOps.invert(gray_img)
                        img = inv.point(lambda x: 0 if x < thresh else 255, '1')
                    for psm in [6, 7, 8, 11, 12, 13]:
                        try:
                            tesseract_config = f"--oem 1 --psm {psm} -l eng -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !."
                            data = pytesseract.image_to_data(img, config=tesseract_config, output_type=Output.DICT)
                            words = data.get('text', [])
                            confs = data.get('conf', [])
                            candidates = []
                            for w, c in zip(words, confs):
                                try:
                                    cval = float(c)
                                except Exception:
                                    cval = -1
                                w_norm = self._normalize_ocr_text(w)
                                if w_norm and cval >= 70:
                                    candidates.append((w_norm, cval))
                            full_norm = self._normalize_ocr_text(' '.join(words))
                            result = f"Thresh {thresh}, Invert {invert}, PSM {psm} -> words={candidates[:6]} | full='{full_norm}'"
                            print(result)
                            ocr_results.append(result)
                        except Exception as e:
                            error_msg = f"OCR error with thresh {thresh}, invert {invert}, psm {psm}: {e}"
                            print(error_msg)
                            ocr_results.append(error_msg)
            
            # Show results in a dialog
            results_text = "\n".join(ocr_results[:12])  # Show first results
            if len(ocr_results) > 12:
                results_text += f"\n... and {len(ocr_results) - 12} more results"
            
            messagebox.showinfo("OCR Test Complete", 
                              f"OCR test completed. Check console output and saved images.\n\n"
                              f"Sample results:\n{results_text}")
            
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

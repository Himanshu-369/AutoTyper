import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import pyautogui
import time
import threading
import random
import math

# --- CONFIGURATION ---
pyautogui.PAUSE = 0 

# --- MODERN DARK THEME PALETTE ---
COLOR_BG = "#121212"         
COLOR_SURFACE = "#1e1e1e"    
COLOR_TEXT = "#e0e0e0"       
COLOR_SUBTEXT = "#a0a0a0"    
COLOR_INPUT_BG = "#2d2d30"   
COLOR_ACCENT = "#3b8ed0"     

# Status & Button Colors
COLOR_SUCCESS = "#28a745"    
COLOR_DANGER = "#dc3545"     
COLOR_DISABLED = "#3e3e42"   
COLOR_WARNING = "#ffc107"    

# --- DATA ---
KEY_NEIGHBORS = {
    'q': 'wa', 'w': 'qeas', 'e': 'wrsd', 'r': 'etdf', 't': 'ryfg', 'y': 'tugh', 'u': 'yijh', 'i': 'uokj', 'o': 'iplk', 'p': 'ol',
    'a': 'qwsz', 's': 'qweadz', 'd': 'ersfcx', 'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg', 'j': 'uikmnh', 'k': 'iolmj', 'l': 'opk',
    'z': 'asx', 'x': 'sdzc', 'c': 'dfxv', 'v': 'fgcb', 'b': 'ghvn', 'n': 'hjbm', 'm': 'jkln'
}

# Common letter pairs that get swapped by humans (e.g., "the" -> "teh")
COMMON_SWAPS = ['th', 'he', 'an', 'in', 'er', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of', 'ed']

class UltimateTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Humanized AutoTyper")
        self.root.geometry("650x950") 
        self.root.configure(bg=COLOR_BG)
        
        self.is_typing = False
        
        self.setup_styles()
        self.build_ui()
        
        # Apply default profile
        self.apply_profile("Lazy Student")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=COLOR_BG)
        style.configure("Surface.TFrame", background=COLOR_SURFACE)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=COLOR_BG, foreground=COLOR_ACCENT, font=("Segoe UI", 18, "bold"))
        style.configure("CardTitle.TLabel", background=COLOR_SURFACE, foreground=COLOR_ACCENT, font=("Segoe UI", 9, "bold"))
        style.configure("TButton", background=COLOR_SURFACE, foreground=COLOR_TEXT, borderwidth=0)
        style.configure("Horizontal.TProgressbar", troughcolor=COLOR_INPUT_BG, background=COLOR_ACCENT, bordercolor=COLOR_BG, lightcolor=COLOR_ACCENT, darkcolor=COLOR_ACCENT)

    def build_ui(self):
        # --- HEADER & TOOLBAR ---
        header_frame = ttk.Frame(self.root, padding=(20, 20, 20, 5))
        header_frame.pack(fill="x")
        
        # Title and Topmost Toggle
        top_row = tk.Frame(header_frame, bg=COLOR_BG)
        top_row.pack(fill="x")
        tk.Label(top_row, text="Humanized AutoTyper", bg=COLOR_BG, fg=COLOR_ACCENT, font=("Segoe UI", 16, "bold")).pack(side="left")
        
        self.topmost_var = tk.BooleanVar(value=False)
        tk.Checkbutton(top_row, text="Always on Top", variable=self.topmost_var, command=self.toggle_topmost,
                       bg=COLOR_BG, fg=COLOR_SUBTEXT, selectcolor=COLOR_INPUT_BG, activebackground=COLOR_BG,
                       highlightthickness=0).pack(side="right")

        # Utility Toolbar
        toolbar = tk.Frame(header_frame, bg=COLOR_BG, pady=10)
        toolbar.pack(fill="x")
        
        self.make_tool_btn(toolbar, "📂 Load File", self.load_file)
        self.make_tool_btn(toolbar, "📋 Paste Clipboard", self.paste_clipboard)
        
        # Profile Dropdown
        tk.Label(toolbar, text="Profile:", bg=COLOR_BG, fg=COLOR_SUBTEXT).pack(side="left", padx=(20, 5))
        self.profile_var = tk.StringVar(value="Lazy Student")
        profile_cb = ttk.Combobox(toolbar, textvariable=self.profile_var, values=["Pro Typist", "Lazy Student", "Tired Human", "Just Type"], 
                                  state="readonly", width=15)
        profile_cb.pack(side="left")
        profile_cb.bind("<<ComboboxSelected>>", self.on_profile_change)

        # --- INPUT AREA ---
        input_container = ttk.Frame(self.root, padding=(20, 0))
        input_container.pack(fill="x")
        
        self.text_area = scrolledtext.ScrolledText(
            input_container, height=8, font=("Consolas", 11), 
            bg=COLOR_INPUT_BG, fg=COLOR_TEXT, 
            insertbackground=COLOR_TEXT, relief="flat", 
            borderwidth=5, highlightthickness=0
        )
        self.text_area.pack(fill="x")
        self.text_area.bind("<KeyRelease>", self.update_stats)

        # --- STATS & PROGRESS ---
        stats_frame = ttk.Frame(self.root, padding=(20, 5))
        stats_frame.pack(fill="x")
        
        self.word_count_label = tk.Label(stats_frame, text="0 Words", bg=COLOR_BG, fg=COLOR_SUBTEXT, font=("Segoe UI", 9))
        self.word_count_label.pack(side="left")
        self.est_label = tk.Label(stats_frame, text="~ 0m 0s", bg=COLOR_BG, fg=COLOR_SUBTEXT, font=("Segoe UI", 9))
        self.est_label.pack(side="right")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))

        # --- SETTINGS CARDS ---
        settings_wrapper = ttk.Frame(self.root, padding=20)
        settings_wrapper.pack(fill="both", expand=True)

        # 1. Speed & Fatigue
        self.create_settings_card(settings_wrapper, "SPEED & FATIGUE", [
            ("Base Speed (WPM)", "wpm_var", 70),
            ("Start Delay (sec)", "start_delay_var", 6),
            ("Fatigue Impact (%)", "fatigue_rate", 10.0) # Speed drops by 10% over time
        ])

        tk.Frame(settings_wrapper, bg=COLOR_BG, height=10).pack()

        # 2. Errors & Imperfections
        self.create_settings_card(settings_wrapper, "HUMAN IMPERFECTIONS", [
            ("Typos (Corrected) %", "corrected_error_rate", 4.0),
            ("Typos (Ignored) %", "persistent_error_rate", 1.0),
            ("Swap Errors (teh/the) %", "swap_error_rate", 1.5),
            ("Double Space Error %", "double_space_rate", 1.0)
        ])

        tk.Frame(settings_wrapper, bg=COLOR_BG, height=10).pack()

        # 3. Behavioral
        self.create_settings_card(settings_wrapper, "BEHAVIORAL LOGIC", [
            ("Word Rethink Rate %", "word_rethink_rate", 2.0),
            ("Paragraph Pause (sec)", "para_pause_var", 1.5)
        ])

        # --- STATUS & BUTTONS ---
        self.status_label = tk.Label(self.root, text="Ready", bg=COLOR_BG, fg=COLOR_ACCENT, font=("Segoe UI", 11, "bold"))
        self.status_label.pack(pady=(0, 5))

        btn_frame = ttk.Frame(self.root, padding=(20, 0, 20, 20))
        btn_frame.pack(fill="x", side="bottom")

        self.start_btn = tk.Button(
            btn_frame, text="Start Typing", bg=COLOR_SUCCESS, fg="white", 
            activebackground="#218838", activeforeground="white",
            font=("Segoe UI", 10, "bold"), relief="flat", pady=12, cursor="hand2", command=self.initiate_start
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.stop_btn = tk.Button(
            btn_frame, text="Stop", bg=COLOR_DISABLED, fg="white", 
            disabledforeground="#888", font=("Segoe UI", 10, "bold"), relief="flat",
            pady=12, cursor="arrow", state="disabled", command=self.stop_typing
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))

    # --- UI HELPERS ---
    def make_tool_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, command=cmd, bg=COLOR_SURFACE, fg=COLOR_TEXT, 
                        relief="flat", font=("Segoe UI", 9), padx=10, cursor="hand2", activebackground=COLOR_INPUT_BG)
        btn.pack(side="left", padx=(0, 10))

    def create_settings_card(self, parent, title, rows):
        card = tk.Frame(parent, bg=COLOR_SURFACE, padx=15, pady=10)
        card.pack(fill="x")
        tk.Label(card, text=title, bg=COLOR_SURFACE, fg=COLOR_ACCENT, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
        
        for label_text, var_name, default_val in rows:
            row = tk.Frame(card, bg=COLOR_SURFACE)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label_text, bg=COLOR_SURFACE, fg=COLOR_TEXT).pack(side="left")
            var = tk.DoubleVar(value=default_val)
            setattr(self, var_name, var)
            entry = tk.Entry(row, textvariable=var, bg=COLOR_INPUT_BG, fg=COLOR_TEXT, 
                             insertbackground=COLOR_TEXT, relief="flat", width=6, justify="center")
            entry.pack(side="right")
            entry.bind("<KeyRelease>", self.update_stats)

    def toggle_topmost(self):
        self.root.attributes('-topmost', self.topmost_var.get())

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", f.read())
                self.update_stats()
            except Exception as e:
                self.update_status(f"Error: {str(e)}", COLOR_DANGER)

    def paste_clipboard(self):
        try:
            content = self.root.clipboard_get()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.update_stats()
        except:
            self.update_status("Clipboard empty or invalid", COLOR_WARNING)

    # --- PROFILES ---
    def on_profile_change(self, event):
        self.apply_profile(self.profile_var.get())

    def apply_profile(self, name):
        # Default fallback
        data = {
            "wpm": 70, "correct": 4.0, "persist": 1.0, "rethink": 2.0, "swap": 1.5, "double": 1.0, "fatigue": 10.0
        }
        
        if name == "Pro Typist":
            data = {"wpm": 110, "correct": 1.5, "persist": 0.1, "rethink": 0.5, "swap": 0.5, "double": 0.1, "fatigue": 5.0}
        elif name == "Lazy Student":
            data = {"wpm": 65, "correct": 6.0, "persist": 2.0, "rethink": 3.0, "swap": 2.5, "double": 2.0, "fatigue": 15.0}
        elif name == "Tired Human":
            data = {"wpm": 45, "correct": 8.0, "persist": 3.0, "rethink": 5.0, "swap": 4.0, "double": 3.0, "fatigue": 30.0}
        elif name == "Just Type":
            data = {"wpm": 90, "correct": 0.0, "persist": 0.0, "rethink": 0.0, "swap": 0.0, "double": 0.0, "fatigue": 0.0}


        # Apply to variables
        self.wpm_var.set(data["wpm"])
        self.corrected_error_rate.set(data["correct"])
        self.persistent_error_rate.set(data["persist"])
        self.word_rethink_rate.set(data["rethink"])
        self.swap_error_rate.set(data["swap"])
        self.double_space_rate.set(data["double"])
        self.fatigue_rate.set(data["fatigue"])
        self.update_stats()

    # --- LOGIC ---

    def calculate_base_delay(self):
        try:
            wpm = self.wpm_var.get()
            return 60.0 / (max(wpm, 1) * 5.0)
        except: return 0.1

    def update_stats(self, event=None):
        text = self.text_area.get("1.0", tk.END).strip()
        words = len(text.split())
        chars = len(text)
        self.word_count_label.config(text=f"{words} Words")
        
        if chars == 0:
            self.est_label.config(text="~ 0m 0s")
            return

        base_delay = self.calculate_base_delay()
        # Complex Overhead Calculation
        overhead = 0
        overhead += (chars * (self.corrected_error_rate.get()/100)) * 0.6 
        overhead += (chars * (self.word_rethink_rate.get()/100)) * 2.0
        
        # Paragraph pauses
        paragraphs = text.count('\n')
        overhead += paragraphs * self.para_pause_var.get()

        total_seconds = (chars * base_delay) + overhead
        m, s = divmod(int(total_seconds), 60)
        self.est_label.config(text=f"Est: {m}m {s}s")

    def update_status(self, text, color_code=None):
        if color_code:
            self.status_label.config(text=text, fg=color_code)
        else:
            self.status_label.config(text=text, fg=COLOR_ACCENT)

    def initiate_start(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.update_status("Please enter text", COLOR_DANGER)
            return

        self.start_btn.config(state="disabled", bg=COLOR_DISABLED)
        self.stop_btn.config(state="normal", bg=COLOR_DANGER)
        
        threading.Thread(target=self.countdown_logic, args=(text,)).start()

    def countdown_logic(self, text):
        delay = int(self.start_delay_var.get())
        for i in range(delay, 0, -1):
            if not self.stop_btn['state'] == 'normal': return 
            self.update_status(f"Starting in {i}...", COLOR_WARNING)
            time.sleep(1)
        
        if self.stop_btn['state'] == 'normal':
            self.is_typing = True
            self.type_text(text)

    def stop_typing(self):
        self.is_typing = False
        self.update_status("Stopping...", COLOR_DANGER)

    # --- ADVANCED TYPING ENGINE ---

    def get_neighbor(self, char):
        char_lower = char.lower()
        if char_lower in KEY_NEIGHBORS:
            neighbor = random.choice(KEY_NEIGHBORS[char_lower])
            return neighbor.upper() if char.isupper() else neighbor
        return char

    def press_key_human(self, char):
        """Simulates human key press with Shift latency"""
        if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
            # Hold shift
            pyautogui.keyDown('shift')
            time.sleep(random.uniform(0.05, 0.12)) # Hold time
            
            # Press key
            pyautogui.press(char.lower())
            
            # Release shift (sometimes early, sometimes late, usually late)
            time.sleep(random.uniform(0.05, 0.1))
            pyautogui.keyUp('shift')
        else:
            pyautogui.press(char)

    def type_text(self, text):
        try:
            # Rates
            base_delay_target = self.calculate_base_delay()
            prob_correct = self.corrected_error_rate.get() / 100.0
            prob_persist = self.persistent_error_rate.get() / 100.0
            prob_rethink = self.word_rethink_rate.get() / 100.0
            prob_swap = self.swap_error_rate.get() / 100.0
            prob_dbl_space = self.double_space_rate.get() / 100.0
            fatigue_factor = self.fatigue_rate.get() / 100.0
            
            total_chars = len(text)
            chars_done = 0
            word_buffer = ""
            
            # Cognitive Flow
            flow = 1.0 
            
            i = 0
            while i < len(text):
                if not self.is_typing: break
                
                char = text[i]
                chars_done += 1
                
                # --- FATIGUE CALCULATION ---
                # Speed decreases slightly as we progress
                progress = chars_done / max(total_chars, 1)
                fatigue_mult = 1.0 + (progress * fatigue_factor)
                
                # --- FLOW CALCULATION ---
                flow += random.uniform(-0.15, 0.15)
                flow = max(0.6, min(1.6, flow)) # Clamp speed variance

                # --- GUI UPDATE ---
                if i % 10 == 0:
                    percent = int((chars_done / total_chars) * 100)
                    self.progress_var.set(percent)
                    self.root.after(0, lambda p=percent: self.update_status(f"Typing... {p}%", COLOR_SUCCESS))

                # --- 1. PARAGRAPH PAUSE ---
                if char == '\n':
                    pyautogui.press('enter')
                    # Long pause for new paragraph thinking
                    pause = self.para_pause_var.get() * random.uniform(0.8, 1.2)
                    time.sleep(pause)
                    i += 1
                    word_buffer = ""
                    continue

                # --- 2. WORD RETHINK (Change Mind) ---
                if char in " .,?!":
                    if len(word_buffer) > 3 and random.random() < prob_rethink:
                        self.press_key_human(char)
                        time.sleep(base_delay_target * 4) # Realize mistake
                        
                        # Use CTRL+BACKSPACE logic
                        if random.random() < 0.7:
                            pyautogui.hotkey('ctrl', 'backspace') # Pro move
                            pyautogui.press('backspace') # Delete the punctuation
                        else:
                            # Panic backspace
                            for _ in range(len(word_buffer) + 1):
                                pyautogui.press('backspace')
                                time.sleep(0.04)
                        
                        time.sleep(random.uniform(0.5, 1.2)) # Think
                        word_buffer = ""
                    else:
                        word_buffer = ""
                else:
                    word_buffer += char

                # --- 3. SWAP ERROR (teh/the) ---
                # Check if current and next char make a common pair
                if i + 1 < len(text) and char.isalnum() and random.random() < prob_swap:
                    next_char = text[i+1]
                    pair = (char + next_char).lower()
                    if pair in COMMON_SWAPS:
                        # Type swapped
                        pyautogui.write(next_char)
                        time.sleep(base_delay_target * flow)
                        pyautogui.write(char)
                        time.sleep(0.2) # Realize
                        
                        # Fix it
                        pyautogui.press('backspace')
                        pyautogui.press('backspace')
                        time.sleep(0.15)
                        # We don't increment i, we just fall through to type correctly now
                
                # --- 4. PERSISTENT ERROR (Ignored) ---
                if char.isalnum() and random.random() < prob_persist:
                    typo = self.get_neighbor(char)
                    pyautogui.write(typo)
                    i += 1
                    time.sleep(base_delay_target * flow * fatigue_mult)
                    continue

                # --- 5. CORRECTED ERROR (Typo -> Fix) ---
                if char.isalnum() and random.random() < prob_correct:
                    typo = self.get_neighbor(char)
                    pyautogui.write(typo)
                    time.sleep(random.uniform(0.15, 0.4)) # Reaction time
                    pyautogui.press('backspace')
                    time.sleep(random.uniform(0.05, 0.1))

                # --- 6. DOUBLE SPACE ERROR ---
                if char == ' ' and random.random() < prob_dbl_space:
                    pyautogui.write("  ")
                    # 50% chance to fix it, 50% leave it
                    if random.random() < 0.5:
                        time.sleep(0.2)
                        pyautogui.press('backspace')
                    else:
                        i += 1
                        continue # Skip typing the actual space since we did 2

                # --- EXECUTE TYPING ---
                self.press_key_human(char)

                # --- DELAY ---
                # Base * Flow * Fatigue * Random Jitter
                delay = (base_delay_target * flow * fatigue_mult) * random.uniform(0.8, 1.2)
                time.sleep(delay)
                i += 1

            if self.is_typing:
                self.root.after(0, lambda: self.update_status("Task Complete", COLOR_SUCCESS))
                self.progress_var.set(100)
        
        except pyautogui.FailSafeException:
            self.root.after(0, lambda: self.update_status("Emergency Stop (Mouse Corner)", COLOR_DANGER))
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"Error: {e}", COLOR_DANGER))
        finally:
            self.is_typing = False
            self.root.after(0, self.reset_ui)

    def reset_ui(self):
        self.start_btn.config(state="normal", bg=COLOR_SUCCESS)
        self.stop_btn.config(state="disabled", bg=COLOR_DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTyperApp(root)
    root.mainloop()

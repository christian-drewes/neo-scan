import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# --- Theme Configuration ---
BG_COLOR = "#0a0f0d"        # Deep dark background
FG_COLOR = "#00ff41"        # Classic terminal neon green
ACCENT_COLOR = "#ff007f"    # Cyberpunk magenta 
FONT_MAIN = ("Consolas", 11)
FONT_TITLE = ("Consolas", 16, "bold")

class HackerScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEON_SCAN // Project: Mirage")
        self.root.geometry("500x450")
        self.root.configure(bg=BG_COLOR)
        self.targets = []

        self.setup_ui()

    def setup_ui(self):
        # Title Label
        title_lbl = tk.Label(self.root, text="[ SYSTEM_SCAN_INTERFACE ]", 
                             bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_TITLE)
        title_lbl.pack(pady=20)

        # Target Entry Frame
        entry_frame = tk.Frame(self.root, bg=BG_COLOR)
        entry_frame.pack(fill=tk.X, padx=40, pady=5)

        self.target_entry = tk.Entry(entry_frame, bg="#1a2621", fg=FG_COLOR, 
                                     font=FONT_MAIN, insertbackground=FG_COLOR, relief=tk.FLAT)
        self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        add_btn = tk.Button(entry_frame, text="ADD_TARGET", bg=ACCENT_COLOR, fg="#ffffff", 
                            font=FONT_MAIN, relief=tk.FLAT, activebackground="#cc0066", 
                            activeforeground="#ffffff", command=self.add_target)
        add_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Target Listbox
        list_frame = tk.Frame(self.root, bg=BG_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)

        self.target_listbox = tk.Listbox(list_frame, bg="#0d1411", fg=FG_COLOR, 
                                         font=FONT_MAIN, relief=tk.FLAT, selectbackground=ACCENT_COLOR)
        self.target_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, bg=BG_COLOR)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.target_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.target_listbox.yview)

        # Scan Button
        scan_btn = tk.Button(self.root, text="> INITIATE_SCAN_SEQUENCE <", bg=FG_COLOR, fg=BG_COLOR, 
                             font=("Consolas", 12, "bold"), relief=tk.FLAT, 
                             activebackground="#00cc33", activeforeground=BG_COLOR, 
                             command=self.start_scan)
        scan_btn.pack(fill=tk.X, padx=40, pady=25, ipady=8)

    def add_target(self):
        target = self.target_entry.get().strip()
        if target:
            if target not in self.targets:
                self.targets.append(target)
                self.target_listbox.insert(tk.END, f" [+] {target}")
            self.target_entry.delete(0, tk.END)

    def start_scan(self):
        if not self.targets:
            messagebox.showwarning("ERR_NO_TARGETS", "Target list empty. Provide an IP/URL.")
            return

        self.open_scan_modal()

    def open_scan_modal(self):
        # Create Modal Window
        self.modal = tk.Toplevel(self.root)
        self.modal.title("SCAN_EXECUTION_LOG")
        self.modal.geometry("600x400")
        self.modal.configure(bg=BG_COLOR)
        self.modal.transient(self.root) 
        self.modal.grab_set() 

        # Console Text Area
        self.console_text = tk.Text(self.modal, bg="#050806", fg=FG_COLOR, 
                                    font=FONT_MAIN, relief=tk.FLAT, state=tk.DISABLED)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Run scan in a background thread to prevent GUI freezing
        scan_thread = threading.Thread(target=self.execute_scan, daemon=True)
        scan_thread.start()

    def log_to_console(self, message, is_accent=False):
        """Helper to append text to the modal console."""
        self.console_text.config(state=tk.NORMAL)
        
        # Add tags for colors if accent is true
        if is_accent:
            self.console_text.insert(tk.END, message + "\n", "accent")
            self.console_text.tag_config("accent", foreground=ACCENT_COLOR)
        else:
            self.console_text.insert(tk.END, message + "\n")
            
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)

    def execute_scan(self):
        """
        MOCK SCAN FUNCTION: 
        Replaces actual subprocess calls with time.sleep() for safety and demonstration.
        """
        self.log_to_console("[SYSTEM] Booting scan protocols...", is_accent=True)
        time.sleep(1)

        for target in self.targets:
            self.log_to_console(f"\n{'='*40}")
            self.log_to_console(f"[*] TARGET LOCK: {target}", is_accent=True)
            self.log_to_console(f"{'='*40}")
            time.sleep(1)

            # --- SUBFINDER MOCK ---
            self.log_to_console(f"[>] Executing subfinder on {target}...")
            # Example of how you would implement this:
            # subprocess.run(["subfinder", "-d", target, "-o", f"{target}_subs.txt"])
            time.sleep(1.5)
            self.log_to_console(f"[+] Subfinder complete. 3 subdomains archived to local databank.")

            # --- NMAP MOCK ---
            self.log_to_console(f"[>] Initiating NMAP sequence (Ports, TLS, Ciphers, Vuln-Scripts)...")
            # Example of how you would implement this:
            # subprocess.run(["nmap", "-sV", "-sU", "--script", "vuln,ssl-enum-ciphers", target])
            time.sleep(2)
            self.log_to_console(f"    - SYN Stealth scan complete.")
            time.sleep(1)
            self.log_to_console(f"    - UDP heuristic checks complete.")
            time.sleep(1.5)
            self.log_to_console(f"    - Script engine evaluation (vuln, tls) finished.")
            
            self.log_to_console(f"[+] NMAP scan parameters saved to matrix.", is_accent=True)
            time.sleep(0.5)

        self.log_to_console("\n[!] ALL_TASKS_COMPLETE. Disconnecting...", is_accent=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerScannerApp(root)
    root.mainloop()

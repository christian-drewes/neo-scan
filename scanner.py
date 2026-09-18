import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLineEdit, QPushButton, 
                             QListWidget, QLabel, QTextEdit, QDialog, QCheckBox,
                             QFileDialog)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
import subprocess

# --- Theme Configuration (CSS) ---
STYLESHEET = """
/* Explicitly target main windows and dialogs to override Apple's Aqua theme */
QMainWindow, QDialog, QWidget {
    background-color: #0a0f0d;
    color: #00ff41;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
}
QLabel#Title {
    color: #ff007f;
    font-size: 20px;
    font-weight: bold;
}
QLineEdit {
    background-color: #1a2621;
    color: #00ff41;
    border: 1px solid #ff007f;
    padding: 8px;
}
QPushButton {
    background-color: #0a0f0d;
    color: #00ff41;
    border: 1px solid #00ff41;
    padding: 8px 15px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00ff41;
    color: #0a0f0d;
}
QPushButton:disabled {
    color: #444444;
    border: 1px solid #444444;
    background-color: transparent;
}
QPushButton#AddBtn {
    color: #ff007f;
    border: 1px solid #ff007f;
}
QPushButton#AddBtn:hover {
    background-color: #ff007f;
    color: #0a0f0d;
}
QPushButton#RemoveBtn {
    color: #ff007f;
    border: 1px dashed #ff007f;
}
QPushButton#RemoveBtn:hover {
    background-color: #ff007f;
    color: #0a0f0d;
}
QPushButton#MenuBtn {
    border: 1px dashed #333333;
    color: #aaaaaa;
    text-align: left;
}
QPushButton#MenuBtn:hover {
    color: #00ff41;
    border: 1px dashed #00ff41;
    background-color: transparent;
}
QListWidget, QTextEdit {
    background-color: #050806;
    border: 1px solid #333333;
    padding: 5px;
}
/* Custom Checkbox Styling */
QCheckBox {
    color: #00ff41;
    spacing: 8px;
    font-weight: bold;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    background-color: #0a0f0d;
    border: 1px solid #00ff41;
}
QCheckBox::indicator:checked {
    background-color: #00ff41;
    border: 1px solid #00ff41;
}
QCheckBox::indicator:hover {
    border: 1px solid #ff007f;
}
"""

class ScanWorker(QThread):
    log_signal = pyqtSignal(str, bool)
    finished_signal = pyqtSignal()

    def __init__(self, targets, scan_config):
        super().__init__()
        self.targets = targets
        self.scan_config = scan_config

    def run(self):
        self.log_signal.emit("[SYSTEM] Booting scan protocols...", True)
        time.sleep(1)

        for target in self.targets:
            self.log_signal.emit(f"\n{'='*40}", False)
            self.log_signal.emit(f"[*] TARGET LOCK: {target}", True)
            self.log_signal.emit(f"{'='*40}", False)
            time.sleep(1)

            # Check Config before running Subfinder
            if self.scan_config["subfinder"]:
                self.subfinder(target)
            else:
                self.log_signal.emit("[!] Skipping Subfinder...", False)

            # Check Config before running NMAP TLS
            if self.scan_config["nmap_tls"]:
                self.nmapTLS(target)
            else:
                self.log_signal.emit("[!] Skipping NMAP TLS...", False)

            if self.scan_config["nmap_agg"]:
                self.nmapAgg(target)
            else:
                self.log_signal.emit("[!] Skipping NMAP Aggressive Scan...", False)

            if self.scan_config["nmap_fast"]:
                self.nmapFast(target)

            # Check Config before running NMAP UDP
            if self.scan_config["nmap_udp"]:
                self.nmapUDP(target)
            else:
                self.log_signal.emit("[!] Skipping NMAP UDP...", False)

            if self.scan_config["dir_scan"]:
                self.directoryScan(target)
            else:
                self.log_signal.emit("[!] Skipping Directory Scan...", False)

            self.log_signal.emit("[+] Target sequence completed.", True)
            time.sleep(0.5)

        self.log_signal.emit("\n[!] ALL_TASKS_COMPLETE. Disconnecting...", True)
        self.finished_signal.emit()
    
    def nmapAgg(self, target):
        self.log_signal.emit("\n[!] Checking target ports", False)
        result = subprocess.run(["nmap", "-A", "", target], capture_output=True, text=True)
        self.log_signal.emit(result.stdout, True)

    def nmapFast(self, target):
        self.log_signal.emit("\n[!] Checking target ports", False)
        result = subprocess.run(["nmap", "-A", "", target], capture_output=True, text=True)
        self.log_signal.emit(result.stdout, True)

    def nmapTLS(self, target):
        self.log_signal.emit("\n[!] Checking target for weak ciphers and TLS", False)
        result = subprocess.run(["nmap", "-p443", "--script", "ssl-enum-ciphers", target], capture_output=True, text=True)
        self.log_signal.emit(result.stdout, True)

    def nmapUDP(self, target):
        self.log_signal.emit("\n[!] Checking target for UDP", False)
        result = subprocess.run(["nmap", "-sU", target], capture_output=True, text=True)
        self.log_signal.emit(result.stdout, True)
        self.log_signal.emit("    - UDP heuristic checks complete.", False)

    def subfinder(self, target):
        self.log_signal.emit("\n[!] Checking target for subdomains", False)
        result = subprocess.run(["subfinder", "-d", target], capture_output=True, text=True)
        self.log_signal.emit(result.stdout, True)
        if result.stderr:
            self.log_signal.emit(result.stderr, True)

    def directoryScan(self, target):
        self.log_signal.emit("\n[!] Checking target directory", False)
        url = "http://"+target
        result = subprocess.run(["dirb", url], capture_output=True, text=True)
        self.log_signal.emit(result.stdout, True)

class ScanModal(QDialog):
    def __init__(self, targets, scan_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SCAN_EXECUTION_LOG")
        self.resize(650, 450)
        self.targets = targets
        self.scan_config = scan_config

        layout = QVBoxLayout(self)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        # Action Button Row (Bottom of the Modal)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch() # Push button to the right
        
        self.save_btn = QPushButton("[↓] SAVE_LOG")
        self.save_btn.setEnabled(False) # Keep disabled until scan finishes
        self.save_btn.clicked.connect(self.save_log)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)

        # Background Thread Setup
        self.worker = ScanWorker(self.targets, self.scan_config)
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self.scan_finished) # Listen for completion
        self.worker.start()

    def append_log(self, text, is_accent):
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        if is_accent:
            self.console.insertHtml(f'<span style="color:#ff007f;">{text}</span><br>')
        else:
            self.console.insertHtml(f'<span style="color:#00ff41;">{text}</span><br>')
        self.console.moveCursor(QTextCursor.MoveOperation.End)

    def scan_finished(self):
        """Called when the ScanWorker emits the finished_signal."""
        self.save_btn.setEnabled(True) # Unlock the save button

    def save_log(self):
        """Opens a save dialog and writes the console text to a file."""
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Scan Log", 
            "scan_results.txt", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # Get the raw text (without the HTML/CSS tags)
                log_data = self.console.toPlainText()
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(log_data)
                self.append_log(f"\n[SYSTEM] Log successfully archived to: {file_path}", True)
            except Exception as e:
                self.append_log(f"\n[ERR] Failed to write log file: {str(e)}", True)


class HackerScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEON_SCAN // Project: Mirage")
        self.resize(550, 550)
        
        self.targets = []
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_lbl = QLabel("[ SYSTEM_SCAN_INTERFACE ]")
        title_lbl.setObjectName("Title")
        main_layout.addWidget(title_lbl)

        # Input Row
        input_layout = QHBoxLayout()
        self.target_entry = QLineEdit()
        self.target_entry.setPlaceholderText("Enter Target IP/URL...")
        self.target_entry.returnPressed.connect(self.add_target)
        input_layout.addWidget(self.target_entry)

        add_btn = QPushButton("ADD_TARGET")
        add_btn.setObjectName("AddBtn")
        add_btn.clicked.connect(self.add_target)
        input_layout.addWidget(add_btn)
        
        main_layout.addLayout(input_layout)

        # Toggle Options Button
        self.menu_btn = QPushButton("[+] TOGGLE_SCAN_MODULES")
        self.menu_btn.setObjectName("MenuBtn")
        self.menu_btn.clicked.connect(self.toggle_options)
        main_layout.addWidget(self.menu_btn)

        # Hidden Options Panel
        self.options_panel = QWidget()
        options_layout = QGridLayout(self.options_panel)
        options_layout.setContentsMargins(10, 5, 10, 15)

        self.chk_subfinder = QCheckBox("Subfinder Enumeration")
        self.chk_subfinder.setChecked(True) # Enabled by default
        
        self.chk_nmap_tls = QCheckBox("NMAP TLS / Ciphers")
        self.chk_nmap_tls.setChecked(True)
        
        self.chk_nmap_udp = QCheckBox("NMAP UDP Scan")
        self.chk_nmap_udp.setChecked(False) # Off by default (takes too long)

        self.chk_nmap_fast = QCheckBox("NMAP Fast")
        self.chk_nmap_fast.setChecked(True)

        self.chk_nmap_agg = QCheckBox("NMAP Aggressive")
        self.chk_nmap_agg.setChecked(False)
        
        self.chk_dir_scan = QCheckBox("Directory Brute Force")
        self.chk_dir_scan.setChecked(False)

        options_layout.addWidget(self.chk_subfinder, 0, 0)
        options_layout.addWidget(self.chk_nmap_tls, 0, 1)
        options_layout.addWidget(self.chk_nmap_udp, 1, 0)
        options_layout.addWidget(self.chk_dir_scan, 1, 1)
        options_layout.addWidget(self.chk_nmap_fast, 0, 2)
        options_layout.addWidget(self.chk_nmap_agg, 1, 2)

        self.options_panel.setVisible(False) # Hide the panel initially
        main_layout.addWidget(self.options_panel)

        # Target List
        self.target_listbox = QListWidget()
        main_layout.addWidget(self.target_listbox)

        # Remove Target Button Row
        remove_layout = QHBoxLayout()
        remove_layout.addStretch() # Pushes the button to the right side
        remove_btn = QPushButton("[-] REMOVE_SELECTED")
        remove_btn.setObjectName("RemoveBtn")
        remove_btn.clicked.connect(self.remove_target)
        remove_layout.addWidget(remove_btn)
        
        main_layout.addLayout(remove_layout)

        # Scan Button
        scan_btn = QPushButton("> INITIATE_SCAN_SEQUENCE <")
        scan_btn.clicked.connect(self.start_scan)
        main_layout.addWidget(scan_btn)

    def toggle_options(self):
        """Hides or reveals the scan config checkboxes."""
        is_visible = self.options_panel.isVisible()
        self.options_panel.setVisible(not is_visible)
        
        if is_visible:
            self.menu_btn.setText("[+] TOGGLE_SCAN_MODULES")
        else:
            self.menu_btn.setText("[-] HIDE_SCAN_MODULES")

    def add_target(self):
        target = self.target_entry.text().strip()
        if target and target not in self.targets:
            self.targets.append(target)
            self.target_listbox.addItem(f" [+] {target}")
            self.target_entry.clear()

    def remove_target(self):
        """Removes the currently selected target from the listbox and underlying array."""
        current_row = self.target_listbox.currentRow()
        
        # Ensure a valid item is actually selected
        if current_row >= 0:
            del self.targets[current_row]
            self.target_listbox.takeItem(current_row)

    def start_scan(self):
        if not self.targets:
            return
            
        # Build configuration dictionary based on what is checked
        scan_config = {
            "subfinder": self.chk_subfinder.isChecked(),
            "nmap_tls": self.chk_nmap_tls.isChecked(),
            "nmap_udp": self.chk_nmap_udp.isChecked(),
            "dir_scan": self.chk_dir_scan.isChecked(),
            "nmap_agg": self.chk_nmap_agg.isChecked(),
            "nmap_fast": self.chk_nmap_fast.isChecked(),
        }
            
        self.modal = ScanModal(self.targets, scan_config, self)
        self.modal.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Force the cross-platform standard theme
    app.setStyle("Fusion") 
    
    # Apply the stylesheet
    app.setStyleSheet(STYLESHEET)
    
    window = HackerScannerApp()
    window.show()
    sys.exit(app.exec())
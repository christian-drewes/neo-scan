import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget, 
                             QLabel, QTextEdit, QDialog)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor

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
QPushButton#AddBtn {
    color: #ff007f;
    border: 1px solid #ff007f;
}
QPushButton#AddBtn:hover {
    background-color: #ff007f;
    color: #0a0f0d;
}
QListWidget, QTextEdit {
    background-color: #050806;
    border: 1px solid #333333;
    padding: 5px;
}
"""

class ScanWorker(QThread):
    log_signal = pyqtSignal(str, bool)
    finished_signal = pyqtSignal()

    def __init__(self, targets):
        super().__init__()
        self.targets = targets

    def run(self):
        self.log_signal.emit("[SYSTEM] Booting scan protocols...", True)
        time.sleep(1)

        for target in self.targets:
            self.log_signal.emit(f"\n{'='*40}", False)
            self.log_signal.emit(f"[*] TARGET LOCK: {target}", True)
            self.log_signal.emit(f"{'='*40}", False)
            time.sleep(1)

            self.log_signal.emit(f"[>] Executing subfinder on {target}...", False)
            time.sleep(1.5)
            self.log_signal.emit("[+] Subfinder complete. 3 subdomains archived.", False)

            self.log_signal.emit("[>] Initiating NMAP sequence (Ports, TLS, Vuln)...", False)
            time.sleep(2)
            self.log_signal.emit("    - SYN Stealth scan complete.", False)
            time.sleep(1)
            self.log_signal.emit("    - UDP heuristic checks complete.", False)
            time.sleep(1.5)
            self.log_signal.emit("    - Script engine evaluation finished.", False)
            
            self.log_signal.emit("[+] NMAP scan parameters saved to matrix.", True)
            time.sleep(0.5)

        self.log_signal.emit("\n[!] ALL_TASKS_COMPLETE. Disconnecting...", True)
        self.finished_signal.emit()


class ScanModal(QDialog):
    def __init__(self, targets, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SCAN_EXECUTION_LOG")
        self.resize(650, 450)
        self.targets = targets

        layout = QVBoxLayout(self)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        self.worker = ScanWorker(self.targets)
        self.worker.log_signal.connect(self.append_log)
        self.worker.start()

    def append_log(self, text, is_accent):
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        if is_accent:
            self.console.insertHtml(f'<span style="color:#ff007f;">{text}</span><br>')
        else:
            self.console.insertHtml(f'<span style="color:#00ff41;">{text}</span><br>')
        self.console.moveCursor(QTextCursor.MoveOperation.End)


class HackerScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEON_SCAN // Project: Mirage")
        self.resize(550, 500)
        
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

        self.target_listbox = QListWidget()
        main_layout.addWidget(self.target_listbox)

        scan_btn = QPushButton("> INITIATE_SCAN_SEQUENCE <")
        scan_btn.clicked.connect(self.start_scan)
        main_layout.addWidget(scan_btn)

    def add_target(self):
        target = self.target_entry.text().strip()
        if target and target not in self.targets:
            self.targets.append(target)
            self.target_listbox.addItem(f" [+] {target}")
            self.target_entry.clear()

    def start_scan(self):
        if not self.targets:
            return
            
        self.modal = ScanModal(self.targets, self)
        self.modal.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # [CRITICAL MAC FIX]: Force the cross-platform standard theme
    app.setStyle("Fusion") 
    
    # Apply the stylesheet
    app.setStyleSheet(STYLESHEET)
    
    window = HackerScannerApp()
    window.show()
    sys.exit(app.exec())
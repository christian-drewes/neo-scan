# NEO_SCAN // Project: Mirage 🌐

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-Cross%20Platform-green.svg)
![License](https://img.shields.io/badge/License-MIT-magenta.svg)

**NEO_SCAN** is a cross-platform, cyberpunk-themed GUI wrapper for offensive security and reconnaissance tools. Built with Python and PyQt6, it provides a sleek, non-blocking interface to run CLI tools like `subfinder` and `nmap` against multiple targets while streaming the results live to a built-in tactical console.

---

## ⚡ Features

* **Cross-Platform:** Looks and behaves exactly the same on Windows, macOS, and Linux.
* **Multi-Target Queuing:** Add multiple domains or IP addresses to a target matrix before initiating the scan.
* **Live Console Streaming:** Uses asynchronous background threading (`QThread` & `subprocess`) to stream real-time CLI tool output to the UI without freezing the application.
* **Tool Integration:** 
  * Integrates seamlessly with ProjectDiscovery's `subfinder`.
  * Pre-built architecture to plug in `nmap` for port, TLS, and vulnerability scanning.

---

## ⚠️ Disclaimer
**For educational and authorized testing purposes only.** 
This tool automates active network reconnaissance. Ensure you have explicit, written permission to scan the targets you input into this software. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

## ⚙️ Prerequisites

Before running the application, you must have the underlying CLI tools installed and accessible in your system's PATH.

1. **Python 3.8+**
2. **[Subfinder](https://github.com/projectdiscovery/subfinder):** Required for subdomain enumeration.
   * *Mac/Linux (via Go):* `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`
   * *Mac (via Homebrew):* `brew install subfinder`
3. **[Nmap](https://nmap.org/download.html):** Required for network scanning (Note: Nmap integration is currently mocked in the source code and requires user implementation).

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/neo-scan.git](https://github.com/yourusername/neo-scan.git)
   cd neo-scan

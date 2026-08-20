# GHOST-WebScanner 🛡️

**GHOST-WebScanner** is an advanced, asynchronous web security and reconnaissance suite designed for professional penetration testers and security researchers. Built with performance and usability in mind, it automates the initial stages of a web application security assessment.

## 🚀 Features

- **Asynchronous Reconnaissance**: Fast IP discovery, port scanning, and HTTP header analysis using `aiohttp` and `asyncio`.
- **Automated Vulnerability Scanning**:
    - **SQL Injection**: Error-based detection using sophisticated payloads.
    - **Cross-Site Scripting (XSS)**: Reflected XSS detection in URL parameters.
- **Professional Reporting**: Generates detailed scan reports with severity classification.
- **Elite CLI Interface**: High-quality terminal UI with real-time progress tracking and formatted results tables.

## 🛠️ Installation

```bash
git clone https://github.com/GhostSy1/GHOST-WebScanner.git
cd GHOST-WebScanner
pip install -r requirements.txt
```

## 📖 Usage

Run a full scan against a target URL:

```bash
python main.py -u https://example.com
```

## 📊 Severity Levels

- 🔴 **Critical**: Immediate action required (e.g., SQL Injection).
- 🟠 **High**: Serious vulnerability (e.g., XSS).
- 🟡 **Medium**: Security misconfigurations.
- 🔵 **Low/Info**: Information disclosure and recon data.

## ⚖️ Disclaimer

This tool is developed for educational and ethical security testing purposes only. The developer (**Abdulaziz**) is not responsible for any misuse or damage caused by this tool. Always obtain proper authorization before scanning any target.

---
Developed with ❤️ by **GHOST (Abdulaziz)**

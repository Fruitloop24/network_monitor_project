
---

# 🔍 **Linux Looker** 🔍  
[Visit my e-portfolio](https://eportkc.com)

## Automated Linux Diagnostic Tool for Quick System Insights

### Extended Overview

**Linux Looker** is a modular, security-focused diagnostic tool for Linux systems that provides quick, detailed insights into system health. It includes eight diagnostic tools, covering DNS, memory, disk usage, firewall, network interfaces, routing, speed tests, logs, and system information. Users can run individual or multiple tools as needed, with results color-coded for readability and saved as text files on the desktop. **Linux Looker** prioritizes security by discarding the sudo password after each run.

### Key Features
- 🌐 **DNS Information**: Provides detailed information on DNS records, including A, AAAA, MX, TXT, PTR, and SOA records, along with DNSSEC status and TTL values.
- 💾 **Memory and Disk Usage**: Displays RAM and swap usage, disk space stats, and lists the top three memory-consuming processes.
- 🔥 **Firewall Information**: Shows firewall status, open ports, and configured firewall rules.
- 🖧 **Interface Information**: Displays network interface status, including IP addresses, subnet masks, and error statistics.
- 🗺 **Routing Table and Traceroute**: Shows the system's routing table and performs a traceroute to identify network paths.
- ⚡ **Net Speed Test, IP, Ping**: Checks download/upload speeds, public/private IP addresses, and measures network latency using ping.
- 📜 **System Logs (Last 10)**: Pulls the last 10 logs from key services like authentication, firewall, and kernel logs.
- 🖥️ **System Info & ARP**: Provides system information (CPU, RAM, uptime) and shows the ARP table with MAC-to-IP mappings.

---

## Installation

To install **Linux Looker**, follow these steps. The primary installation method is through the provided Makefile, which sets up a virtual environment and installs all necessary dependencies. Alternative installation options are also available below for advanced users.

### Primary Installation Method (via Makefile)
1. **Download the Repository**  
   Run the following command in your terminal to download the repository from GitHub:
   ```bash
   git clone https://github.com/Fruitloop24/network_monitor_project.git
   ```

2. **Navigate to the Project Directory**  
   Change into the project directory:
   ```bash
   cd network_monitor_project
   ```

3. **Run the Makefile**  
   Execute the Makefile to set up the virtual environment (`myenv`), install `pyinstaller`, and package the tool:
   ```bash
   make
   ```

4. **Run Linux Looker**  
   After installation, start Linux Looker from the containerized setup using:
   ```bash
   ./dist/linux_looker
   ```

### Alternative Installation Methods
For those who prefer a manual setup, here are additional installation options:

#### Option 1: Install via GitHub
1. Clone the Repository:
   ```bash
   git clone https://github.com/Fruitloop24/network_monitor_project.git
   ```
2. Navigate to the Project Directory:
   ```bash
   cd network_monitor_project
   ```
3. Set Up a Virtual Environment and Install Dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Checksums

To verify the integrity of the downloaded files, you can check their checksums.

### MD5 Checksum:
Run this command to verify the MD5 checksum:
```bash
md5sum linux_looker.zip
```
Ensure the output matches:
```
0e1ddf2ac854e0147e5f752462a0cd23  linux_looker.zip
```

### SHA-256 Checksum:
Run this command to verify the SHA-256 checksum:
```bash
sha256sum linux_looker.zip
```
Ensure the output matches:
```
8d159f1f0d7c2bbde5544cdc446908059caaf752e20853ce37d2c39a4670d77a  linux_looker.zip
```

---

## How to Use

Once you've installed **Linux Looker**, navigate to the `network_monitor_project` directory and use `./dist/linux_looker` to start the application. Follow these steps to get started:

1. **Choose Tools**  
   Upon running, you will be prompted with a menu to select one or more diagnostic tools. Select the tools by entering the corresponding numbers or opt to run all tools.

2. **View Output**  
   The results will be displayed in the terminal and saved as text files on your desktop for easy access.

---

[Visit my e-portfolio](https://eportkc.com)

---


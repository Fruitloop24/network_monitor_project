# 🔍 **Linux Looker** 🔍
## Automated Linux Diagnostic Tool for Quick System Insights

### **Extended Overview**

**Linux Looker** is a modular Python-based diagnostic tool that provides users with a fast, efficient, and color-coded way to inspect the health of their Linux systems. Designed with intermediate Linux users in mind, it eliminates the need to memorize complex CLI commands by bundling multiple system health checks into one tool.

## **Key Selling Points**

- **Simplicity**: No need to run separate commands or remember complex syntax. With an intuitive menu system, users can easily navigate and execute the tools.

- **Quick Insights**: The tool is modular, allowing you to run individual scans or all tools at once for a comprehensive system report. This flexibility makes it ideal for both targeted diagnostics and full system checks.

- **Credentialed and Non-Credentialed Scans**: Our tool supports both credentialed (sudo-required) and non-credentialed scans. The credentialed scans request a sudo password for that specific run and never store or save any sensitive information. For each new scan that requires elevated privileges, the password must be entered again, ensuring maximum privacy and security.

- **Security & Privacy**: We are privacy-conscious and take security seriously. The sudo password is only used during the run of the tool for necessary scans and is discarded immediately after. No data or passwords are stored in the system or saved between sessions.

- **Color-Coded Output**: To enhance readability, the results are presented in a clear, color-coded format. Important sections, system information, and warnings are easy to identify at a glance.

- **Immediate Reports**: All output is automatically saved as neatly formatted text files on your desktop. This allows you to review past results without needing to re-run any commands, providing both convenience and efficiency.

- **Small Footprint**: The tool is lightweight, with a total size of only **29.8 MB**, ensuring it won't take up unnecessary space on your system.

Imagine having all the most critical system health data—network information, firewall status, system memory, logs—available in one place and color-coded for easy readability. Whether you’re troubleshooting an isolated issue like a slow internet connection or scanning your whole system for performance bottlenecks, **Linux Looker** saves time by providing the information in one go.

---

### **Key Features**

1. **DNS Information 🌐**  
   Provides detailed information on DNS records, including A, AAAA, MX, TXT, PTR, and SOA records, along with DNSSEC status and TTL values.

2. **Memory and Disk Usage 💾**  
   Displays RAM and swap usage, disk space stats, and lists the top three memory-consuming processes.

3. **Firewall Information 🔥**  
   Shows firewall status, open ports, and configured firewall rules.

4. **Interface Information 🖧**  
   Displays network interface status, including IP addresses, subnet masks, and error statistics.

5. **Routing Table and Traceroute 🗺**  
   Shows the system's routing table and performs a traceroute to identify network paths.

6. **Net Speed Test, IP, Ping ⚡**  
   Checks download/upload speeds, public/private IP addresses, and measures network latency using ping.

7. **System Logs (Last 10) 📜**  
   Pulls the last 10 logs from key services like authentication, firewall, and kernel logs.

8. **System Info & ARP 🖥️**  
   Provides system information (CPU, RAM, uptime) and shows the ARP table with MAC-to-IP mappings.

---

### **Running the Tools Together or Separately**

- You can run individual tools by selecting them from the menu, or you can run all tools at once for a full system diagnostic.
- The output is neatly organized into text files saved to your desktop for easy reference.

Sure, I'll add the steps for installing the Linux Looker via the Python package option and update the formatting. Here's the full installation and usage guide in markdown format:

```markdown
## Installation

To install **Linux Looker**, follow these steps. You can either clone from GitHub, download the zip file, or install via the Python package.

### Option 1: Install via GitHub

1. **Clone the Repository**  
   Run the following command in your terminal to clone the repository from GitHub:  
   ```bash
   git clone https://github.com/Fruitloop24/network_monitor_project.git
   ```

2. **Navigate to the Project Directory**  
   Change into the project directory:  
   ```bash
   cd network_monitor_project
   ```

3. **Set Up a Virtual Environment**  
   Create and activate a Python virtual environment:  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install Required Dependencies**  
   Install the required Python packages using the following command:  
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Install via Zip File

1. **Download the Zip File**  
   Download the latest release zip file from the GitHub Releases page.

2. **Unzip the File**  
   Unzip the downloaded file and navigate to the project directory:  
   ```bash
   unzip linux_looker.zip
   cd network_monitor_project
   ```

3. **Set Up a Virtual Environment**  
   If needed, set up a virtual environment as in Option 1 and activate it.  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install Required Dependencies**  
   Install the required dependencies using:  
   ```bash
   pip install -r requirements.txt
   ```

### Option 3: Install via Python Package

1. **Install the Package**  
   Install **Linux Looker** via `pip` by running:  
   ```bash
   pip install linux_looker
   ```

2. **Verify the Installation**  
   After installation, verify that **Linux Looker** is installed correctly by running:  
   ```bash
   linux_looker --help
   ```

3. **Run the Tool**  
   Once verified, run the tool using:  
   ```bash
   linux_looker
   ```

---

## Checksums

To verify the integrity of the downloaded files, you can check their checksums.

### MD5 Checksum:
Run this command to verify the MD5 checksum:
```bash
md5sum linux_looker.zip
```
Ensure the output matches:
```
e4374699c05802d60687fd1dad7e6f28  linux_looker.zip
```

### SHA-256 Checksum:
Run this command to verify the SHA-256 checksum:
```bash
sha256sum linux_looker.zip
```
Ensure the output matches:
```
482510fb2b1875aa6688ef3606f165b97063af3f561376f54e269879144543c8  linux_looker.zip
```

---

## How to Use

Once you've installed **Linux Looker**, make sure you navigate to the `network_monitor_project` directory (or run it directly if installed via the Python package). Follow these steps to get started:

### Option 1: Running via GitHub or Zip File

1. **Activate the Virtual Environment**  
   Before running the tool, activate the virtual environment:  
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Tool**  
   To start the tool, run the following command:  
   ```bash
   python3 linux_monitor.py
   ```

3. **Choose Tools**  
   You’ll be prompted with a menu to choose one or more diagnostic tools.  
   Select the tools by entering the corresponding numbers or choose the option to run all tools.

4. **View Output**  
   The output will be displayed in the terminal and saved as text files on your desktop for later review.

### Option 2: Running via Python Package

1. **Activate the Environment** (if installed in a virtual environment):  
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Tool**  
   Simply run the following command:  
   ```bash
   linux_looker
   ```

3. **Choose Tools**  
   After launching, you will be prompted to select one or more diagnostic tools. Select the desired tools or opt to run them all.

4. **View Output**  
   The results will be displayed in the terminal and saved to your desktop for easy access.

---

With these instructions, you can install and use **Linux Looker** with ease!
```

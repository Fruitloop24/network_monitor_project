# 🔍 **Linux Looker** 🔍
## Automated Linux Diagnostic Tool for Quick System Insights

### **Extended Overview**

**Linux Looker** is a modular Python-based diagnostic tool that provides users with a fast, efficient, and color-coded way to inspect the health of their Linux systems. Designed with intermediate Linux users in mind, it eliminates the need to memorize complex CLI commands by bundling multiple system health checks into one tool.

### **Key Selling Points**

- **Simplicity**: No need to run separate commands or remember complex syntax.
- **Quick Insights**: Tools are modular and can be run individually or all at once for a comprehensive report.
- **Color-Coded Output**: Results are presented in a visually appealing, easy-to-read format.
- **Immediate Reports**: All output is saved as neatly formatted text files on your desktop, allowing you to refer back to it without re-running commands.

Imagine having all the most critical system health data—network information, firewall status, system memory, logs—available in one place and color-coded for easy readability. Whether you’re troubleshooting an isolated issue like a slow internet connection or scanning your whole system for performance bottlenecks, **Linux Looker** saves time by providing the information in one go.

---

### **Key Features**

#### 1. DNS Information 🌐
- **What It Does**: Performs a detailed DNS lookup, providing information about A, AAAA, MX, TXT, PTR, and SOA records. It also checks DNSSEC status and provides query times and TTL values.
- **Use Cases**:
  - **Spot DNS Misconfigurations**: Verify if a website's DNS records are correctly set up (A, MX, TXT, and SPF records). Avoid email delivery issues or domain validation problems by quickly identifying misconfigurations.
  - **Troubleshoot Slow Domain Resolution**: Use query time metrics and DNS server info to spot slow DNS resolution, helping troubleshoot websites that take too long to load.
  - **Confirm Security Settings**: Ensure DNSSEC is enabled for domain protection, and check SPF records to avoid email spoofing.
  - **Advanced Use**: Reverse DNS lookups (PTR) can be used for network troubleshooting to confirm correct IP-to-hostname mappings in enterprise environments.

#### 2. Memory and Disk Usage 💾
- **What It Does**: Displays system RAM, swap usage, and disk space statistics. It also identifies the top three memory-hungry processes and checks for potential memory leaks or high swap usage.
- **Use Cases**:
  - **Optimize System Performance**: Easily pinpoint memory bottlenecks or excessive swap usage that might be slowing down the system. Memory-intensive processes can be identified and managed.
  - **Spot Memory Leaks**: For users suspecting memory leaks, this tool helps reveal processes that continually eat away at system memory.
  - **Ensure Storage Health**: Get a quick view of available disk space and usage. Prevent system slowdowns by acting before critical partitions run out of space.
  - **Advanced Use**: Integrate with alert systems to notify users if memory or disk usage crosses predefined thresholds (e.g., RAM above 85%, swap above 50%).

#### 3. Firewall Information 🔥
- **What It Does**: Shows the current firewall status, open ports, allowed/denied rules, and services listening on those ports. It also provides detailed logging of blocked attempts.
- **Use Cases**:
  - **Ensure Proper Firewall Configuration**: Check that critical ports (SSH, HTTP, etc.) are open, while others are properly locked down. Useful for auditing security configurations.
  - **Troubleshoot Connectivity Issues**: Easily identify if a service is failing because the firewall is blocking it. For example, if an application can't connect to the internet, this tool will reveal whether a port block is the cause.
  - **Block Unauthorized Access**: View all denied traffic and determine if there are any suspicious attempts to access the system.
  - **Advanced Use**: Regular firewall audits to ensure all ports are secured, especially after installing new applications.

#### 4. Interface Information 🖧
- **What It Does**: Shows the status of all network interfaces, including IP addresses, subnet masks, VLAN configurations, duplex settings, and error statistics (e.g., dropped packets).
- **Use Cases**:
  - **Diagnose Interface Errors**: Interface status, error stats, and dropped packets help quickly identify issues with network hardware or misconfigured interfaces.
  - **Track IP Changes**: Ensure your network interfaces are receiving the correct IP address, which is essential when troubleshooting connectivity issues.
  - **Verify VLANs**: For advanced network setups, this tool checks VLAN configurations to ensure proper network segmentation and isolation.
  - **Advanced Use**: Useful in virtualized environments or networks with multiple interfaces to track the health of each interface, including virtual ones.

#### 5. Routing Table and Traceroute 🗺
- **What It Does**: Provides a detailed routing table and performs a traceroute to a public DNS server (e.g., 8.8.8.8). This shows the path packets take to reach their destination and the routers they pass through.
- **Use Cases**:
  - **Troubleshoot Connectivity**: Easily identify misconfigured routes that could be preventing access to certain networks or services. Useful for diagnosing unreachable servers or websites.
  - **Check Network Latency**: Traceroute reveals which hop is causing delays in network performance. This is critical for diagnosing high-latency issues in enterprise networks or cloud environments.
  - **Route Verification**: Verify the network paths that packets take and ensure they are optimized or secured as per the desired network configuration.
  - **Advanced Use**: Use routing table details to optimize network routing for complex enterprise setups or multi-homed servers.

#### 6. Net Speed Test, IP, Ping ⚡
- **What It Does**: Performs an internet speed test (upload/download speeds), displays public/private IP addresses, and measures network latency using the ping command.
- **Use Cases**:
  - **Identify Slow Internet Issues**: Quickly determine if slow internet is caused by poor download or upload speeds. Useful for diagnosing VPN or ISP throttling issues.
  - **Confirm IP Address Configuration**: Verify if your device is using the correct public/private IP address, especially when troubleshooting VPNs or cloud environments.
  - **Check Network Latency**: Use ping latency results to assess network performance and pinpoint delays.
  - **Advanced Use**: Useful in diagnosing issues with VPNs and IP misconfigurations, especially when testing from multiple network locations.

#### 7. System Logs (Last 10) 📜
- **What It Does**: Pulls the last 10 logs from system services such as kernel, authentication, and firewall logs. This tool helps quickly spot recent errors or login attempts.
- **Use Cases**:
  - **Spot Unauthorized Access**: Review authentication logs to detect any suspicious login attempts (e.g., failed SSH logins).
  - **Monitor System Stability**: Quickly identify if any kernel-level errors (e.g., hardware failures, driver issues) are affecting the system's stability.
  - **Track Recent Changes**: Verify firewall logs to ensure no suspicious connections have been blocked or allowed.
  - **Advanced Use**: Add support for specifying log ranges or alert systems for repeated failed login attempts.

#### 8. System Info & ARP 🖥️
- **What It Does**: Displays detailed system information (CPU, RAM, uptime, architecture) and provides a full ARP table showing MAC-to-IP mappings for devices on the local network.
- **Use Cases**:
  - **Verify System Health**: Get an instant overview of CPU, memory, disk space, and uptime to ensure the system is running smoothly.
  - **Track Connected Devices**: ARP table helps track all devices on the network, which is useful for identifying unauthorized or unexpected devices.
  - **Ensure Proper Networking**: Quickly verify if the system's networking is functioning correctly by checking its IP configuration and ARP table for issues like duplicate IPs or misconfigurations.
  - **Advanced Use**: Regularly review ARP tables in environments prone to ARP spoofing or man-in-the-middle attacks to spot malicious behavior.

---

### **Running the Tools Together or Separately**

- You can run individual tools by selecting them from the menu, or you can run all tools at once for a full system diagnostic.
- The output is neatly organized into text files saved to your desktop for easy reference.

### **Advanced Use Cases:**

- **DNS and Network Troubleshooting:**
  - **Tools**: DNS Information, Routing Table, Net Speed Test.
  - **Scenario**: You're having trouble accessing certain websites or services. Start with DNS Information to verify the DNS records, use Routing Table to check if the network paths are correct, and finally run the Net Speed Test to rule out speed or latency issues.

- **Security Audit:**
  - **Tools**: Firewall Information, System Logs, ARP Table.
  - **Scenario**: You're auditing your system for unauthorized access or suspicious activity. Begin with Firewall Information to ensure the firewall is correctly configured, then check System Logs for recent login attempts, and finally inspect the ARP Table for unauthorized devices on the network.

- **Performance Bottleneck:**
  - **Tools**: Memory and Disk Usage, Interface Information, Net Speed Test.
  - **Scenario**: Your system feels slow, and you're unsure if it's memory-related, disk, or network. Check Memory and Disk Usage to spot any memory hogs, use Interface Information to verify there are no interface errors, and then run Net Speed Test to see if network bandwidth is the issue.
## Installation

To install **Linux Looker**, follow these steps. You can either clone from GitHub or download the zip file.

### Option 1: Install via GitHub

1. **Clone the Repository**  
   Run the following command in your terminal to clone the repository from GitHub:  
   `git clone https://github.com/Fruitloop24/network_monitor_project.git`

2. **Navigate to the Project Directory**  
   Change into the project directory:  
   `cd network_monitor_project`

3. **Set Up a Virtual Environment**  
   Create and activate a Python virtual environment:  
   `python3 -m venv .venv`  
   `source .venv/bin/activate`

4. **Install Required Dependencies**  
   Install the required Python packages using the following command:  
   `pip install -r requirements.txt`

### Option 2: Install via Zip File

1. **Download the Zip File**  
   Download the latest release zip file from the GitHub Releases page.

2. **Unzip the File**  
   Unzip the downloaded file and navigate to the project directory:  
   `unzip network_monitor_project.zip`  
   `cd network_monitor_project`


To verify the MD5 checksum, use this command:
`md5sum linux_looker.zip`

Ensure the output matches:
`e4374699c05802d60687fd1dad7e6f28 linux_looker.zip`

To verify the SHA-256 checksum, use this command:
`sha256sum linux_looker.zip`

Ensure the output matches:
`482510fb2b1875aa6688ef3606f165b97063af3f561376f54e269879144543c8 linux_looker.zip`

---

## How to Use

Once you’ve installed **Linux Looker**, follow these steps to run it:

1. **Activate the Virtual Environment**  
   Before running the tool, activate the virtual environment:  
   `source .venv/bin/activate`

2. **Run the Tool**  
   To start the tool, run the following command:  
   `python3 linux_monitor.py`

3. **Choose Tools**  
   You’ll be prompted with a menu to choose one or more diagnostic tools.  
   Select the tools by entering the corresponding numbers or choose the option to run all tools.
   
4. **View Output**  
   The output will be displayed in the terminal and saved as text files on your desktop for later review.

---

With these instructions, you can install and use **Linux Looker** with ease!

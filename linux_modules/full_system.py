import os
import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add linux_modules directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Path to the report file
report_file = os.path.join(os.path.dirname(__file__), 'full_system_report.txt')

def run_and_capture_output(command, description):
    """Runs a shell command and captures its output."""
    print(f"{Fore.GREEN}{description}{Style.RESET_ALL}")
    result = os.popen(command).read().strip()
    print(result)
    with open(report_file, 'a') as f:
        f.write(f"{description}\n{result}\n\n")
    return result

def run_python_module(module_name, description):
    """Runs a Python module and captures its output."""
    print(f"{Fore.GREEN}{description}{Style.RESET_ALL}")
    module = __import__(module_name)
    result = module.main() if hasattr(module, 'main') else "No output"
    print(result)
    with open(report_file, 'a') as f:
        f.write(f"{description}\n{result}\n\n")
    return result

def run_full_system_scan():
    """Runs a full system scan by calling all available tools."""
    # Start fresh report
    with open(report_file, 'w') as f:
        f.write(f"Full System Scan Report - {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # Run each tool sequentially
    run_python_module('linux_modules.system_info', "=======================================\n💻 System Information\n=======================================")
    run_python_module('linux_modules.interface_details', "=======================================\n🖧 Interface Details\n=======================================")
    run_python_module('linux_modules.dns_info', "=======================================\n🔍 DNS Information\n=======================================")
    run_python_module('linux_modules.last_ten_logs', "=======================================\n📝 Last Ten Logs\n=======================================")
    run_python_module('linux_modules.memory_status', "=======================================\n💾 Memory and Disk Usage\n=======================================")
    run_python_module('linux_modules.routing_table', "=======================================\n🚦 Routing Information\n=======================================")
    run_python_module('linux_modules.firewall_status', "=======================================\n🛡️  Firewall and Open Ports\n=======================================")
    run_python_module('linux_modules.network_speed_test', "=======================================\n📊 Network Speed Test\n=======================================")

    print(f"{Fore.GREEN}Full System Scan Completed!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Report saved to {report_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    run_full_system_scan()









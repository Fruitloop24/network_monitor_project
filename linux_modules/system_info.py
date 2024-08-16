import socket
import os
import platform
import subprocess
import psutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_system_info():
    """
    Retrieves and formats system information.
    """
    try:
        system_info = f"{Fore.CYAN}System Information:{Style.RESET_ALL}\n"

        # Get operating system information
        system_info += get_os_info()

        # Get network information
        system_info += get_network_info()

        # Get user and uptime information
        system_info += get_user_uptime_info()

        # Get CPU information
        system_info += get_cpu_info()

        # Get memory information
        system_info += get_memory_info()

        # Get disk information
        system_info += get_disk_info()

        # Get manufacture information
        system_info += get_manufacture_info()

    except Exception as e:
        system_info = f"{Fore.RED}Error retrieving system information: {e}{Style.RESET_ALL}\n"

    return system_info

def get_os_info():
    """
    Retrieves operating system information.
    """
    return (
        f"{Fore.GREEN}Operating System:{Style.RESET_ALL} {platform.system()} {platform.release()}\n"
        f"{Fore.GREEN}Architecture:{Style.RESET_ALL} {platform.machine()}\n"
    )

def get_network_info():
    """
    Retrieves network information.
    """
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        ip_address = "Unable to retrieve IP address"
    return (
        f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {socket.gethostname()}\n"
        f"{Fore.GREEN}IP Address:{Style.RESET_ALL} {ip_address}\n"
    )

def get_user_uptime_info():
    """
    Retrieves user and uptime information.
    """
    try:
        user = os.getlogin()
    except Exception as e:
        user = f"Unable to retrieve user: {e}"
    try:
        uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
    except Exception as e:
        uptime = f"Unable to retrieve uptime: {e}"
    return (
        f"{Fore.GREEN}User:{Style.RESET_ALL} {user}\n"
        f"{Fore.GREEN}System Uptime:{Style.RESET_ALL} {uptime}\n"
    )

def get_cpu_info():
    """
    Retrieves CPU information.
    """
    try:
        core_count = psutil.cpu_count(logical=False)
        thread_count = psutil.cpu_count(logical=True)
        cpu_model = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | uniq", shell=True).decode().strip().split(':')[1].strip()
    except Exception as e:
        core_count = "Unknown"
        thread_count = "Unknown"
        cpu_model = f"Unable to retrieve CPU info: {e}"
    return (
        f"{Fore.GREEN}CPU:{Style.RESET_ALL} {cpu_model}\n"
        f"{Fore.GREEN}Cores:{Style.RESET_ALL} {core_count} physical cores\n"
        f"{Fore.GREEN}Threads:{Style.RESET_ALL} {thread_count} logical processors\n"
    )

def get_memory_info():
    """
    Retrieves memory information.
    """
    try:
        total_memory = subprocess.check_output("grep MemTotal /proc/meminfo", shell=True).decode().strip().split(":")[1].strip()
    except Exception as e:
        total_memory = f"Unable to retrieve memory info: {e}"
    return f"{Fore.GREEN}Memory:{Style.RESET_ALL} {total_memory}\n"

def get_disk_info():
    """
    Retrieves disk information.
    """
    try:
        disk_info = subprocess.check_output("df -h --total | grep total", shell=True).decode().strip().split()
        disk_total = disk_info[1]
        disk_used = disk_info[2]
        disk_free = disk_info[3]
        disk_usage = disk_info[4]
        return (
            f"{Fore.GREEN}Disk Info:{Style.RESET_ALL} Total: {disk_total}, Used: {disk_used}, Free: {disk_free}, Usage: {disk_usage}\n"
        )
    except Exception as e:
        return f"{Fore.RED}Unable to retrieve disk info: {e}\n"

def get_manufacture_info():
    """
    Retrieves manufacture information.
    """
    try:
        manufacture_info = subprocess.check_output("sudo dmidecode -t system | grep -E 'Manufacturer|Product Name|Serial Number'", shell=True).decode().strip()
        if "Default string" in manufacture_info:
            manufacture_info = "Manufacture info not available or system is virtual."
    except Exception as e:
        manufacture_info = f"Unable to retrieve manufacturing information: {e}"
    return f"{Fore.GREEN}Manufacture Info:{Style.RESET_ALL} {manufacture_info}\n"

if __name__ == "__main__":
    print(get_system_info())

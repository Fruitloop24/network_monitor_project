import socket
import os
import platform
import subprocess
import psutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_system_info(sudo_password=None):
    """
    Retrieves and formats full system information.
    """
    try:
        system_info = f"{Fore.CYAN}===== SYSTEM STATS ====={Style.RESET_ALL}\n"
        system_info += get_os_info()
        system_info += get_cpu_info()
        system_info += get_memory_info()
        system_info += get_disk_info()

        user_info = f"{Fore.MAGENTA}===== USER STATS ====={Style.RESET_ALL}\n"
        user_info += get_user_info()

        network_info = f"{Fore.GREEN}===== NETWORK & DEVICES ====={Style.RESET_ALL}\n"
        network_info += get_network_info()
        network_info += get_arp_table_info(sudo_password)  # ARP table using old method
        network_info += get_external_devices(sudo_password)

        return system_info + user_info + network_info

    except Exception as e:
        return f"{Fore.RED}Error retrieving system information: {e}{Style.RESET_ALL}\n"


def get_os_info():
    """
    Retrieves operating system information.
    """
    return (
        f"{Fore.GREEN}Operating System:{Style.RESET_ALL} {platform.system()} {platform.release()}\n"
        f"{Fore.GREEN}Architecture:{Style.RESET_ALL} {platform.machine()}\n"
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
    Retrieves memory information in GB.
    """
    try:
        total_memory = psutil.virtual_memory().total / (1024 ** 3)
        return f"{Fore.GREEN}RAM:{Style.RESET_ALL} {total_memory:.2f} GB\n"
    except Exception as e:
        return f"{Fore.RED}Unable to retrieve memory info: {e}{Style.RESET_ALL}\n"

def get_disk_info():
    """
    Retrieves disk usage information and ensures values add up correctly.
    """
    try:
        disk_usage = psutil.disk_usage('/')
        return (
            f"{Fore.GREEN}Disk Info:{Style.RESET_ALL} "
            f"Total: {disk_usage.total / (1024**3):.0f}G, "
            f"Used: {disk_usage.used / (1024**3):.0f}G, "
            f"Free: {disk_usage.free / (1024**3):.0f}G, "
            f"Usage: {disk_usage.percent}%\n"
        )
    except Exception as e:
        return f"{Fore.RED}Unable to retrieve disk info: {e}{Style.RESET_ALL}\n"

def get_user_info():
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
        f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {socket.gethostname()}\n"
        f"{Fore.GREEN}User:{Style.RESET_ALL} {user}\n"
        f"{Fore.GREEN}System Uptime:{Style.RESET_ALL} {uptime}\n"
    )

def get_network_info():
    """
    Retrieves network information.
    """
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        ip_address = "Unable to retrieve IP address"

    return f"{Fore.GREEN}IP Address:{Style.RESET_ALL} {ip_address}\n"

def get_arp_table_info(sudo_password=None):
    """
    Retrieves the ARP table using the 'arp -a' command (old method).
    """
    try:
        if sudo_password:
            arp_output = subprocess.check_output(f"echo {sudo_password} | sudo -S arp -a", shell=True).decode().strip()
        else:
            arp_output = subprocess.check_output("arp -a", shell=True).decode().strip()

        if arp_output:
            return f"{Fore.GREEN}ARP Table:{Style.RESET_ALL}\n{arp_output}\n"
        else:
            return f"{Fore.YELLOW}No ARP entries found.{Style.RESET_ALL}\n"
    except Exception as e:
        return f"{Fore.RED}Unable to retrieve ARP table: {e}{Style.RESET_ALL}\n"

def get_external_devices(sudo_password=None):
    """
    Retrieves information about externally mounted devices.
    """
    try:
        if sudo_password:
            output = subprocess.check_output(f"echo {sudo_password} | sudo -S lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT", shell=True).decode().strip()
        else:
            output = subprocess.check_output("lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT", shell=True).decode().strip()

        # Filter out the internal mounts and show only external devices (if mounted)
        mount_lines = [line for line in output.splitlines() if "/media" in line or "/mnt" in line]
        if mount_lines:
            return f"{Fore.GREEN}External Mount Points:{Style.RESET_ALL}\n" + "\n".join(mount_lines) + "\n"
        else:
            return f"{Fore.YELLOW}No external devices detected.{Style.RESET_ALL}\n"

    except Exception as e:
        return f"{Fore.RED}Unable to retrieve external devices: {e}{Style.RESET_ALL}\n"


if __name__ == "__main__":
    try:
        sudo_password = input("Enter your sudo password (or leave blank for non-sudo mode): ").strip()
        print(get_system_info(sudo_password))
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")








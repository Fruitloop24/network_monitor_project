import psutil
import shutil
from colorama import Fore, Style
import re
import os

def format_memory_status(mem, swap):
    """Formats the RAM and swap memory status with warnings for high usage."""
    ram_warning = f"{Fore.GREEN}Status: Healthy ✅{Style.RESET_ALL}\n"
    swap_warning = f"{Fore.GREEN}Status: Healthy ✅{Style.RESET_ALL}\n"

    # Warning for RAM usage over 85%
    if mem.percent > 85:
        ram_warning = f"{Fore.RED}{Style.BRIGHT}WARNING: High RAM usage! ({mem.percent}% used){Style.RESET_ALL}\n"
    elif mem.percent > 75:
        ram_warning = f"{Fore.YELLOW}{Style.BRIGHT}WARNING: RAM usage above normal! ({mem.percent}% used){Style.RESET_ALL}\n"

    # Warning for Swap usage over 50%
    if swap.percent > 50:
        swap_warning = f"{Fore.RED}{Style.BRIGHT}WARNING: High Swap usage! ({swap.percent}% used){Style.RESET_ALL}\n"
    elif swap.percent > 30:
        swap_warning = f"{Fore.YELLOW}{Style.BRIGHT}WARNING: Swap usage above normal! ({swap.percent}% used){Style.RESET_ALL}\n"

    return (
        f"{Fore.CYAN}{Style.BRIGHT}RAM Status:{Style.RESET_ALL}\n"
        f"  Total: {Fore.GREEN}{mem.total // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Used: {Fore.RED}{mem.used // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Free: {Fore.GREEN}{mem.free // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Cached: {Fore.YELLOW}{mem.cached // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"{ram_warning}"
        f"{Fore.CYAN}{Style.BRIGHT}Swap Memory:{Style.RESET_ALL}\n"
        f"  Total: {Fore.GREEN}{swap.total // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Used: {Fore.RED}{swap.used // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Free: {Fore.GREEN}{swap.free // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"{swap_warning}"
    )

def format_partition(partition, status):
    """Formats the partition information."""
    if status == "Unused":
        return (
            f"\n{Fore.GREEN}Mount Point:{Style.RESET_ALL} {partition}\n"
            f"{Fore.CYAN}  Status: {status}{Style.RESET_ALL}\n"
        )
    else:
        return (
            f"\n{Fore.GREEN}Mount Point:{Style.RESET_ALL} {partition.mountpoint}\n"
            f"  Total Size: {Fore.GREEN}{status['total']} GB{Style.RESET_ALL}\n"
            f"  Available: {Fore.GREEN}{status['available']} GB{Style.RESET_ALL}\n"
            f"  Status: {Fore.GREEN}Healthy ✅{Style.RESET_ALL}\n"
        )

def get_memory_status(sudo_password=None):
    """Retrieves and formats memory and swap status with optional sudo."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return format_memory_status(mem, swap)

def get_filesystem_info(sudo_password=None):
    """Retrieves and formats filesystem info, excluding snap mounts."""
    partitions = psutil.disk_partitions()
    used_partitions = []
    unused_partitions = []

    for partition in partitions:
        # Exclude snap mounts
        if 'snap' in partition.mountpoint:
            continue
        try:
            usage = shutil.disk_usage(partition.mountpoint)
            status = {
                "total": usage.total // (1024 ** 3),
                "available": usage.free // (1024 ** 3)
            }
            used_partitions.append(format_partition(partition, status))
        except PermissionError:
            used_partitions.append(f"{Fore.RED}Permission Denied: {partition.mountpoint}{Style.RESET_ALL}\n")

    return "".join(used_partitions) + "\n" + "".join(unused_partitions)

def get_top_memory_processes():
    """Retrieves the top 3 processes by memory usage."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            if proc.info['memory_percent'] > 0:
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort processes by memory usage
    top_processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]
    formatted_processes = ""

    for process in top_processes:
        status = "Healthy" if process['memory_percent'] < 20 else "Warning"
        formatted_processes += (
            f"  PID: {process['pid']}, Name: {process['name']}, Memory: {Fore.RED if status == 'Warning' else Fore.GREEN}{process['memory_percent']:.2f}% {status}{Style.RESET_ALL}\n"
        )

    return f"{Fore.CYAN}{Style.BRIGHT}Top 3 Memory-Hungry Processes:{Style.RESET_ALL}\n" + formatted_processes

def output_to_file(content, filename="memory_file_status.txt"):
    """Writes the content to a file on the Desktop."""
    with open(os.path.join(os.path.expanduser("~/Desktop"), filename), "w") as file:
        file.write(content)

def run_memory_tool_from_menu(sudo_password=None):
    """This function is used to call the memory tool from another script."""
    output = get_memory_status(sudo_password)
    output += get_filesystem_info(sudo_password)
    output += get_top_memory_processes()

    print(output)

    # Remove color codes for output to file
    plain_output = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', output)
    output_file_path = os.path.join(os.path.expanduser("~/Desktop"), "memory_file_status.txt")
    output_to_file(plain_output, output_file_path)
    
    print(f"Output written to {output_file_path}")

if __name__ == "__main__":
    run_memory_tool_from_menu()





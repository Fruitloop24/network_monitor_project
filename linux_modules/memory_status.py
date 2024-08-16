import psutil
import shutil
from colorama import Fore, Style
import os

def format_memory_status(mem, swap):
    """Formats the RAM and swap memory status."""
    return (
        f"{Fore.CYAN}{Style.BRIGHT}RAM Status:{Style.RESET_ALL}\n"
        f"  Total: {Fore.GREEN}{Style.BRIGHT}{mem.total // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Used: {Fore.RED}{Style.BRIGHT}{mem.used // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Free: {Fore.GREEN}{Style.BRIGHT}{mem.free // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Cached: {Fore.YELLOW}{Style.BRIGHT}{mem.cached // (1024 ** 2)} MB{Style.RESET_ALL}\n\n"
        f"{Fore.CYAN}{Style.BRIGHT}Swap Memory:{Style.RESET_ALL}\n"
        f"  Total: {Fore.GREEN}{Style.BRIGHT}{swap.total // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Used: {Fore.RED}{Style.BRIGHT}{swap.used // (1024 ** 2)} MB{Style.RESET_ALL}\n"
        f"  Free: {Fore.GREEN}{Style.BRIGHT}{swap.free // (1024 ** 2)} MB{Style.RESET_ALL}\n"
    )

def format_partition(partition, status):
    """Formats the partition information based on its status."""
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
        )

def get_memory_status():
    """Retrieves and formats memory and swap status."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return format_memory_status(mem, swap)

def get_filesystem_info():
    """Retrieves and formats the filesystem information."""
    partitions = psutil.disk_partitions()
    
    used_partitions = []
    unused_partitions = []

    for partition in partitions:
        try:
            usage = shutil.disk_usage(partition.mountpoint)
            if usage.total == 0 or (usage.total // (1024 ** 3)) == 0:
                unused_partitions.append(format_partition(partition.mountpoint, "Unused"))
            else:
                status = {
                    "total": usage.total // (1024 ** 3),
                    "available": usage.free // (1024 ** 3)
                }
                used_partitions.append(format_partition(partition, status))
        except PermissionError:
            used_partitions.append(f"{Fore.RED}Permission Denied: {partition.mountpoint}{Style.RESET_ALL}\n")

    return "".join(used_partitions) + "\n" + "".join(unused_partitions)

def output_to_file(content, filename="memory_file_status.txt"):
    """Writes the content to a file."""
    with open(filename, "w") as file:
        file.write(content)

def main():
    """Main function to retrieve and display system information."""
    output = get_memory_status()
    output += get_filesystem_info()

    print(output)

    plain_output = output.replace(Fore.CYAN, "").replace(Fore.GREEN, "").replace(Fore.RED, "").replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "").replace(Style.BRIGHT, "")
    output_file_path = os.path.join(os.getcwd(), "memory_file_status.txt")
    output_to_file(plain_output, output_file_path)
    
    print(f"Output written to {output_file_path}")

if __name__ == "__main__":
    main()



import subprocess
from colorama import Fore, Style, init
from pathlib import Path

# Initialize colorama for color output
init(autoreset=True)

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            raise Exception(f"Command failed: {command}")
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"{Fore.RED}Error running command '{command}': {e}{Style.RESET_ALL}"]

def get_routing_table():
    lines = run_command("route -n")
    formatted_routes = []
    header = True
    for line in lines:
        if header:
            header = False
            continue
        parts = line.split()
        if len(parts) >= 8:
            destination = parts[0]
            gateway = parts[1]
            interface = parts[-1]
            formatted_routes.append(f"{Fore.GREEN}Destination: {Style.RESET_ALL}{destination}, {Fore.GREEN}Gateway: {Style.RESET_ALL}{gateway}, {Fore.GREEN}Interface: {Style.RESET_ALL}{interface}")
    return "\n".join(formatted_routes)

def traceroute(destination="8.8.8.8"):
    lines = run_command(f"traceroute {destination}")
    if lines and not lines[0].startswith(Fore.RED):
        formatted_traceroute = [f"{Fore.YELLOW}{line}{Style.RESET_ALL}" for line in lines]
        return f"{Fore.GREEN}Traceroute Successful to {destination}:{Style.RESET_ALL}\n" + "\n".join(formatted_traceroute)
    else:
        return f"{Fore.RED}Traceroute failed or was blocked. Please check your connection or permissions.{Style.RESET_ALL}"

def run_routing_tool_from_menu(sudo_password=None):
    output = []
    output.append(f"{Fore.CYAN}Routing Table:{Style.RESET_ALL}\n")
    output.append(get_routing_table())
    output.append("\n")
    output.append(traceroute("8.8.8.8"))

    # Print colored output for CLI
    print("\n".join(output))

    # Save plain output to a text file (without color codes)
    plain_output = "\n".join(output).replace(Fore.GREEN, "").replace(Fore.CYAN, "").replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "")
    Path("~/Desktop/routing_table.txt").expanduser().write_text(plain_output)
    print(f"Summary saved to ~/Desktop/routing_table.txt")

if __name__ == "__main__":
    run_routing_tool_from_menu()




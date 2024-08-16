import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            raise Exception(f"Command failed: {command}")
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"{Fore.RED}Error running command '{command}': {e}{Style.RESET_ALL}"]

def format_section(title, content):
    return f"{Fore.CYAN}{title}:{Style.RESET_ALL}\n{content}\n"

def get_routing_table():
    lines = run_command("ip route show")
    formatted_routes = []

    for route in lines:
        parts = route.split()
        if 'default' in parts:
            gateway = parts[2]
            interface = parts[-1]
            formatted_routes.append(
                f"  {Fore.GREEN}Gateway:{Style.RESET_ALL} {gateway}\n"
                f"  {Fore.GREEN}Interface:{Style.RESET_ALL} {interface}\n"
            )
        else:
            dest = parts[0]
            gateway = parts[2] if len(parts) > 2 else "None"
            interface = parts[-1]
            formatted_routes.append(
                f"  {Fore.GREEN}Destination:{Style.RESET_ALL} {dest}\n"
                f"  {Fore.GREEN}Gateway:{Style.RESET_ALL} {gateway}\n"
                f"  {Fore.GREEN}Interface:{Style.RESET_ALL} {interface}\n"
            )
    
    return "\n".join(formatted_routes)

def get_interfaces_info():
    lines = run_command("ip addr show")
    formatted_interfaces = []
    current_interface = ""

    for line in lines:
        if line.startswith(" "):
            if "inet" in line:
                ip = line.split()[1]
                formatted_interfaces.append(f"  {Fore.GREEN}IP Address:{Style.RESET_ALL} {ip}")
            elif "link/ether" in line:
                mac = line.split()[1]
                formatted_interfaces.append(f"  {Fore.YELLOW}MAC Address:{Style.RESET_ALL} {mac}")
        else:
            if current_interface:
                formatted_interfaces.append("\n")
            current_interface = line.split(":")[1].strip()
            formatted_interfaces.append(f"{Fore.CYAN}Interface:{Style.RESET_ALL} {Fore.GREEN}{current_interface}{Style.RESET_ALL}")
    
    return "\n".join(formatted_interfaces)

def get_arp_table():
    lines = run_command("arp -n")
    formatted_arp = []

    for entry in lines[1:]:  # Skip the header line
        parts = entry.split()
        ip_address = parts[0]
        mac_address = parts[2]
        interface = parts[-1]

        formatted_arp.append(
            f"  {Fore.GREEN}IP Address:{Style.RESET_ALL} {ip_address}\n"
            f"  {Fore.YELLOW}MAC Address:{Style.RESET_ALL} {mac_address}\n"
            f"  {Fore.GREEN}Interface:{Style.RESET_ALL} {interface}\n"
        )
    
    return "\n".join(formatted_arp)

def traceroute(destination="8.8.8.8"):
    lines = run_command(f"traceroute {destination}")
    if lines and not lines[0].startswith(Fore.RED):
        formatted_traceroute = [
            f"  {Fore.YELLOW}{line}{Style.RESET_ALL}" for line in lines
        ]
        return "\n".join(formatted_traceroute)
    else:
        return f"{Fore.RED}Traceroute failed or was blocked. Please check your connection or permissions.{Style.RESET_ALL}"

def main():
    output = []
    output.append(format_section("Routing Table Information", get_routing_table()))
    output.append(format_section("Interface Information", get_interfaces_info()))
    output.append(format_section("ARP Table", get_arp_table()))
    output.append(format_section(f"Traceroute to 8.8.8.8", traceroute()))

    print("\n".join(output))

if __name__ == "__main__":
    main()







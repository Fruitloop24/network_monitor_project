import subprocess
from colorama import Fore, Style, init
import re
from datetime import datetime
import os

# Initialize colorama
init(autoreset=True)

def run_command(command, timeout=20):
    """
    Executes a shell command and returns the output or error message.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            return f"{Fore.RED}Error running command '{command}': {result.stderr.strip()}{Style.RESET_ALL}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"{Fore.RED}Command '{command}' timed out{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}Unexpected error running command '{command}': {str(e)}{Style.RESET_ALL}"

def strip_color_codes(text):
    """
    Removes color codes from the text.
    """
    color_code_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return color_code_pattern.sub('', text)

def get_firewall_status(sudo_password=None):
    """
    Retrieves the firewall status using 'ufw status verbose'.
    Requires sudo privileges to get accurate status.
    """
    if sudo_password:
        return run_command(f"echo {sudo_password} | sudo -S ufw status verbose")
    else:
        return f"{Fore.RED}Firewall status requires sudo privileges to check if active. Please run with sudo.{Style.RESET_ALL}"

def get_open_ports(sudo_password=None):
    """
    Retrieves the list of open ports using 'lsof'.
    """
    if sudo_password:
        return run_command(f"echo {sudo_password} | sudo -S lsof -i -P -n | grep LISTEN")
    else:
        return run_command("lsof -i -P -n | grep LISTEN")

def get_firewall_rules(sudo_password=None):
    """
    Retrieves the numbered list of firewall rules using 'ufw status numbered'.
    """
    if sudo_password:
        return run_command(f"echo {sudo_password} | sudo -S ufw status numbered")
    else:
        return f"{Fore.RED}Error: sudo required to view firewall rules.{Style.RESET_ALL}"

def count_firewall_rules(status):
    """
    Counts the number of ALLOW and DENY rules in the firewall status.
    """
    allow_count = len(re.findall(r'ALLOW', status))
    deny_count = len(re.findall(r'DENY', status))
    return allow_count, deny_count

def format_open_ports(open_ports):
    """
    Formats the open ports output to separate port numbers and services.
    """
    if not open_ports:
        return f"{Fore.RED}No open ports found.{Style.RESET_ALL}"

    formatted_ports = ""
    for line in open_ports.splitlines():
        parts = re.split(r'\s+', line)
        if len(parts) >= 9:
            service = parts[0]
            port = parts[8]
            protocol = parts[4]
            formatted_ports += f"  Service: {Fore.GREEN}{service}{Style.RESET_ALL}, Port: {Fore.CYAN}{port}{Style.RESET_ALL}, Protocol: {protocol}\n"
    
    return formatted_ports

def format_firewall_status(status):
    """
    Formats the firewall status output, keeping only the essentials.
    """
    # Extract relevant details from the firewall status
    relevant_lines = []
    for line in status.splitlines():
        if "Status:" in line or "Default:" in line or "Logging:" in line or "New profiles:" in line:
            relevant_lines.append(line)
    
    return "\n".join(relevant_lines)

def format_summary(status, open_ports, rules):
    """
    Formats the firewall summary including status, open ports, and rules.
    """
    allow_count, deny_count = count_firewall_rules(rules)
    total_rules = allow_count + deny_count
    
    # Format the firewall status to only show relevant information
    formatted_status = format_firewall_status(status)
    
    # Header and section split with primary colors
    summary = (
        f"{Fore.CYAN}===== FIREWALL SUMMARY ====={Style.RESET_ALL}\n\n"
        f"{Fore.CYAN}{Style.BRIGHT}1. Firewall Status:{Style.RESET_ALL}\n"
        f"{formatted_status}\n\n"
        
        f"{Fore.CYAN}{Style.BRIGHT}2. Open Ports and Services:{Style.RESET_ALL}\n"
        f"{format_open_ports(open_ports)}\n\n"
        
        f"{Fore.CYAN}{Style.BRIGHT}3. Firewall Rules (Numbered):{Style.RESET_ALL}\n"
        f"  {Fore.GREEN}{allow_count} Allow, {Fore.RED}{deny_count} Deny (Total: {total_rules}){Style.RESET_ALL}\n"
        f"{Fore.GREEN}Rules:\n{rules}{Style.RESET_ALL}\n"
    )
    return summary

def save_to_file(content, filename="firewall_summary.txt", append_timestamp=False):
    """
    Saves the given content to a text file on the Desktop, stripping out color codes.
    If append_timestamp is True, appends a timestamp to the filename.
    """
    # Strip color codes for plain content
    plain_content = strip_color_codes(content)
    
    # Append a timestamp to the filename if requested
    if append_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"firewall_summary_{timestamp}.txt"
    
    # Save the file to the user's Desktop
    desktop_path = os.path.join(os.path.expanduser("~/Desktop"), filename)
    try:
        with open(desktop_path, "w") as file:
            file.write(plain_content)
        print(f"{Fore.BLUE}Summary saved to {desktop_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving to file '{desktop_path}': {str(e)}{Style.RESET_ALL}")

def run_firewall_tool_from_menu(sudo_password=None):
    """
    Runs the firewall tool from the menu, handling both privileged and non-privileged modes.
    """
    try:
        status = get_firewall_status(sudo_password)
        open_ports = get_open_ports(sudo_password)
        rules = get_firewall_rules(sudo_password)
        
        # Format and display the firewall summary
        firewall_summary = format_summary(status, open_ports, rules)
        print(firewall_summary)
        
        # Save the summary to a file on the desktop
        save_to_file(firewall_summary, append_timestamp=False)  # Set to True to save multiple reports with timestamps
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    run_firewall_tool_from_menu(sudo_password=None)







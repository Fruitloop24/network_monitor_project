import subprocess
from colorama import Fore, Style, init
import re
from datetime import datetime

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

def get_firewall_status():
    """
    Retrieves the firewall status using 'ufw status verbose'.
    """
    return run_command("sudo ufw status verbose")

def get_open_ports():
    """
    Retrieves the list of open ports using 'lsof'.
    """
    return run_command("sudo lsof -i -P -n | grep LISTEN")

def get_firewall_rules():
    """
    Retrieves the numbered list of firewall rules using 'ufw status numbered'.
    """
    return run_command("sudo ufw status numbered")

def count_firewall_rules(status):
    """
    Counts the number of ALLOW and DENY rules in the firewall status.
    """
    allow_count = len(re.findall(r'ALLOW', status))
    deny_count = len(re.findall(r'DENY', status))
    return allow_count, deny_count

def format_summary(status, open_ports, rules):
    """
    Formats the firewall summary including status, open ports, and rules.
    """
    allow_count, deny_count = count_firewall_rules(status)
    total_rules = allow_count + deny_count
    summary = (
        f"{Fore.GREEN}Firewall Status: {Fore.YELLOW}{'Active' if 'active' in status.lower() else 'Inactive'}{Style.RESET_ALL}, "
        f"{total_rules} Rules ({Fore.GREEN}{allow_count} Allow{Style.RESET_ALL}, {Fore.RED}{deny_count} Deny{Style.RESET_ALL})\n\n"
        f"{Fore.GREEN}Firewall Status:{Style.RESET_ALL}\n{Fore.CYAN}{status}{Style.RESET_ALL}\n\n"
        f"{Fore.GREEN}Open Ports:{Style.RESET_ALL}\n{Fore.CYAN}{open_ports}{Style.RESET_ALL}\n\n"
        f"{Fore.GREEN}Firewall Rules (Numbered):{Style.RESET_ALL}\n{Fore.CYAN}{rules}{Style.RESET_ALL}\n\n"
    )
    return summary

def save_to_file(content, filename="firewall_summary.txt", append_timestamp=False):
    """
    Saves the given content to a text file, stripping out color codes.
    If append_timestamp is True, appends a timestamp to the filename.
    """
    plain_content = strip_color_codes(content)
    if append_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"firewall_summary_{timestamp}.txt"
    try:
        with open(filename, "w") as file:
            file.write(plain_content)
        print(f"{Fore.BLUE}Summary saved to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving to file '{filename}': {str(e)}{Style.RESET_ALL}")

def main():
    try:
        status = get_firewall_status()
        open_ports = get_open_ports()
        rules = get_firewall_rules()
        firewall_summary = format_summary(status, open_ports, rules)
        save_to_file(firewall_summary, append_timestamp=False)  # Set to True to save multiple reports with timestamps
        print(firewall_summary)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()





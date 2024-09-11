from subprocess import run
from colorama import Fore, Style, init
from pathlib import Path
import re

# Initialize colorama
init(autoreset=True)

def get_last_logs(sudo_password=None):
    """Fetches the last system, auth (SSH), kernel, and firewall logs, with better readability."""
    
    # Helper function to run sudo commands with password if needed
    def run_sudo_command(command):
        if sudo_password:
            return run(f"echo {sudo_password} | sudo -S {command}", shell=True, capture_output=True, text=True)
        else:
            return run(command, shell=True, capture_output=True, text=True)

    # Fetch last 10 logs for each category
    sys_logs = run_sudo_command("journalctl -n 10 --no-pager --no-hostname")
    auth_logs = run_sudo_command("journalctl -n 10 -u ssh --no-pager --no-hostname")
    kern_logs = run_sudo_command("journalctl -n 10 -k --no-pager --no-hostname")
    firewall_logs = run_sudo_command("journalctl -n 10 -u ufw --no-pager --no-hostname")

    # Function to format logs with separator and more readable spacing
    def format_logs(logs, log_type, color):
        entries = logs.stdout.strip().splitlines()
        formatted_entries = [f"{color}{entry}{Style.RESET_ALL}" for entry in entries]
        if entries:
            return f"\n{Fore.YELLOW}{'='*22}\n   {log_type.upper()} LOGS\n{'='*22}{Style.RESET_ALL}\n" + \
                   "\n------------------------------------------------------------\n".join(formatted_entries) + "\n\n"
        else:
            return f"{Fore.GREEN}{log_type} Logs: No logs found.\n{Style.RESET_ALL}\n\n"

    # Format logs with better readability
    sys_output = format_logs(sys_logs, "System", Fore.RED)
    auth_output = format_logs(auth_logs, "Authentication", Fore.BLUE)
    kern_output = format_logs(kern_logs, "Kernel", Fore.CYAN)
    firewall_output = format_logs(firewall_logs, "Firewall", Fore.YELLOW)

    # Combine all formatted outputs for CLI
    output = sys_output + auth_output + kern_output + firewall_output

    # Display the output in the CLI
    print(output)

    # Function to remove ANSI color codes for the plain text file
    def remove_ansi_codes(text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)

    # Save plain text output to a file on the desktop
    try:
        desktop_path = Path.home() / "Desktop" / "log_summary.txt"
        with open(desktop_path, "w") as f:
            # Strip ANSI color codes and write clean plain text
            f.write(remove_ansi_codes(output))
        print(f"Summary saved to {desktop_path}")
    except Exception as e:
        print(f"{Fore.RED}Failed to save log summary to desktop: {e}{Style.RESET_ALL}")

# Function to call from the menu
def run_logs_tool_from_menu(sudo_password=None):
    """Wrapper to call the logs tool from the menu."""
    get_last_logs(sudo_password)

if __name__ == "__main__":
    try:
        sudo_password = input("Enter your sudo password: ").strip()  # Ask for sudo password upfront
        get_last_logs(sudo_password)
    except Exception as e:
        print(f"Error: {str(e)}")







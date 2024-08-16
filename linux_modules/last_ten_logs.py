from subprocess import run
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_last_ten_logs():
    # Fetch system logs
    sys_logs = run("sudo journalctl -n 10 -p 3 --no-pager --no-hostname", shell=True, capture_output=True, text=True)
    # Fetch authentication logs
    auth_logs = run("sudo journalctl -n 10 -u ssh --no-pager --no-hostname", shell=True, capture_output=True, text=True)
    # Fetch kernel logs
    kern_logs = run("sudo journalctl -n 10 -k --no-pager --no-hostname", shell=True, capture_output=True, text=True)

    # Color key
    color_key = f"{Fore.RED}Error Logs{Style.RESET_ALL}, " \
                f"{Fore.YELLOW}Warning Logs{Style.RESET_ALL}, " \
                f"{Fore.GREEN}Informational Logs{Style.RESET_ALL}, " \
                f"{Fore.BLUE}Authentication Logs{Style.RESET_ALL}, " \
                f"{Fore.CYAN}Kernel Logs{Style.RESET_ALL}\n"

    # Function to add more explicit spacing between log entries
    def format_logs(logs, color):
        entries = logs.splitlines()
        return f"{color}\n{'-'*60}\n".join(entries) + f"{Style.RESET_ALL}"

    # Colorized output for CLI with clear separations
    sys_output = f"{Fore.RED}System Logs:\n{'-'*60}\n{format_logs(sys_logs.stdout.strip(), Fore.RED)}\n\n"
    auth_output = f"{Fore.BLUE}Authentication Logs:\n{'-'*60}\n{format_logs(auth_logs.stdout.strip(), Fore.BLUE)}\n\n"
    kern_output = f"{Fore.CYAN}Kernel Logs:\n{'-'*60}\n{format_logs(kern_logs.stdout.strip(), Fore.CYAN)}\n\n"

    # Plain text output with explicit separators between log entries
    plain_text_output = "Color Key: Error Logs, Warning Logs, Informational Logs, Authentication Logs, Kernel Logs\n\n" \
                        "System Logs:\n" + "\n\n".join(sys_logs.stdout.strip().splitlines()) + "\n\n" \
                        "Authentication Logs:\n" + "\n\n".join(auth_logs.stdout.strip().splitlines()) + "\n\n" \
                        "Kernel Logs:\n" + "\n\n".join(kern_logs.stdout.strip().splitlines()) + "\n\n"

    # Complete CLI output with color key and improved separations
    colorful_output = color_key + "\n" + sys_output + auth_output + kern_output

    return colorful_output, plain_text_output

if __name__ == "__main__":
    try:
        colorful_output, text_output = get_last_ten_logs()
        # Print colorful output to CLI
        print(colorful_output)
        # Save plain text output to file
        with open("log_summary.txt", "w") as file:
            file.write(text_output)
            print("Summary saved to log_summary.txt")
    except Exception as e:
        print(f"Error: {str(e)}")



import os
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the base directory where the modules are located
base_dir = os.path.expanduser("~/Documents/network_monitor_project")

# Define the function to run the selected tools
def run_tool(choice, ip_address, credentials=None):
    if choice == '1':
        print(f"{Fore.GREEN}=======================================")
        print(f"💻 System Information")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/system_info.py {ip_address}')
    elif choice == '2':
        print(f"{Fore.GREEN}=======================================")
        print(f"💾 Memory and Disk Usage")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/memory_status.py {ip_address}')
    elif choice == '3':
        print(f"{Fore.GREEN}=======================================")
        print(f"🖧 Interface Details")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/interface_details.py {ip_address}')
    elif choice == '4':
        print(f"{Fore.GREEN}=======================================")
        print(f"📝 Last Ten Logs")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/last_ten_logs.py {ip_address}')
    elif choice == '5':
        print(f"{Fore.GREEN}=======================================")
        print(f"🛡️  Firewall and Open Ports")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/firewall_status.py {ip_address} {credentials}')
    elif choice == '6':
        print(f"{Fore.GREEN}=======================================")
        print(f"🌐 Routing Information")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/routing_table.py {ip_address}')
    elif choice == '7':
        print(f"{Fore.GREEN}=======================================")
        print(f"🔍 DNS Information")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/dns_info.py {ip_address}')
    elif choice == '8':
        print(f"{Fore.GREEN}=======================================")
        print(f"📊 Network Speed Test")
        print(f"======================================={Style.RESET_ALL}")
        os.system(f'python3 {base_dir}/linux_modules/network_speed_test.py {ip_address}')
    else:
        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

# Run all tools and output to CLI sequentially
def run_all_tools(ip_address, credentials=None):
    print(f"{Fore.GREEN}=======================================")
    print(f"🛠️ Running All Tools")
    print(f"======================================={Style.RESET_ALL}")
    
    # Create the full_report directory on the desktop
    report_dir = os.path.join(os.path.expanduser("~/Desktop"), "full_report")
    os.makedirs(report_dir, exist_ok=True)
    
    # List of tools in the desired order
    tools = [
        ('1', 'system_info.txt'),
        ('2', 'memory_status.txt'),
        ('3', 'interface_details.txt'),
        ('4', 'last_ten_logs.txt'),
        ('5', 'firewall_status.txt'),
        ('6', 'routing_table.txt'),
        ('7', 'dns_info.txt'),
        ('8', 'network_speed_test.txt')
    ]

    for choice, filename in tools:
        print(f"{Fore.CYAN}Running tool {choice}...{Style.RESET_ALL}")
        run_tool(choice, ip_address, credentials)
        output_file = os.path.join(report_dir, filename)
        with open(output_file, 'w') as f:
            subprocess.run(f'python3 {base_dir}/linux_modules/{filename[:-4]}.py {ip_address}', shell=True, stdout=f)

    print(f"{Fore.GREEN}All tools have been run. Reports saved in {report_dir}{Style.RESET_ALL}")

# Main menu loop
def main():
    while True:
        print(f"{Fore.CYAN}=======================================")
        print(f"🔍 LINUX LOOKER")
        print(f"======================================={Style.RESET_ALL}")
        credentials = None

        # Step 1: Credentialed Test
        cred_choice = input("Would you like to perform a credentialed test? (y/n): ").strip().lower()
        if cred_choice == 'y':
            credentials = input("Enter credentials (format: username:password): ").strip()

        # Step 2: IP Selection
        ip_address = input("Enter the IP Address to scan (or press Enter to scan the host): ").strip()
        if not ip_address:
            ip_address = "localhost"

        # Step 3: Tool Selection
        print("\nSelect Tools to Run (separate choices with commas, e.g., 1,2,3):")
        print("[1] System Information")
        print("[2] Memory and Disk Usage")
        print("[3] Interface Details")
        print("[4] Last Ten Logs")
        print("[5] Firewall and Open Ports")
        print("[6] Routing Information")
        print("[7] DNS Information")
        print("[8] Network Speed Test")
        print("[*] Run All Tools (Full Report)")
        print("\nExample: To run System Information and Memory and Disk Usage, enter: 1,2")
        tool_choices = input("Enter your choices: ").replace(" ", "").split(",")

        if '*' in tool_choices:
            run_all_tools(ip_address, credentials)
        else:
            for tool_choice in tool_choices:
                run_tool(tool_choice, ip_address, credentials)

if __name__ == "__main__":
    main()

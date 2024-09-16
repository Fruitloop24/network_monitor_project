from linux_modules.memory_status import run_memory_tool_from_menu
from linux_modules.dns_info import run_dns_tool_from_menu
from linux_modules.firewall_status import run_firewall_tool_from_menu
from linux_modules.interface_details import run_interface_tool_from_menu
from linux_modules.routing_table import run_routing_tool_from_menu
from linux_modules.network_speed_test import run_network_test_from_menu
from linux_modules.last_ten_logs import run_logs_tool_from_menu
from linux_modules.system_info import get_system_info  # Import system info tool
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Main menu loop
def main():
    while True:
        # Display the menu with proper colors and icons after the number
        print(f"{Fore.CYAN}=======================================")
        print(f"🔍 {Fore.YELLOW}WELCOME TO LINUX LOOKER{Fore.CYAN} 🔍")
        print(f"======================================={Style.RESET_ALL}")

        # Tool Selection Menu with icons after numbers
        print("\nSelect Tools to Run:")
        print(f"[1] 🌐 {Fore.BLUE}DNS Information")
        print(f"[2] 💾 {Fore.MAGENTA}Memory and Disk Usage")
        print(f"[3] 🔥 {Fore.RED}Firewall Information")
        print(f"[4] 🖧 {Fore.GREEN}Interface Information")
        print(f"[5] 🗺 {Fore.YELLOW}Routing Table and Traceroute")
        print(f"[6] ⚡ {Fore.CYAN}Net Speed Test, IP, Ping")
        print(f"[7] 📜 {Fore.LIGHTYELLOW_EX}System Logs (Last 10)")
        print(f"[8] 🖥️ {Fore.LIGHTCYAN_EX}System Info & ARP")
        print(f"[*] 🔧 {Fore.MAGENTA}Run All Tools (Full Report){Style.RESET_ALL}")

        # Capture user's tool choices
        tool_choices = input("\nEnter your choice(s) (e.g., 1,2,3 or * for all tools): ").strip().split(',')

        # Ask if the user wants a privileged scan for the selected tools
        privileged_scan = input("Would you like to run a credentialed (privileged) scan? (y/n): ").strip().lower()
        sudo_password = None
        if privileged_scan == 'y':
            sudo_password = input("Enter your sudo password: ").strip()

        # Run the selected tools
        if '*' in tool_choices:
            # Run all tools if * is selected
            print(f"{Fore.CYAN}Running all tools...{Style.RESET_ALL}")
            run_dns_tool_from_menu(sudo_password)
            run_memory_tool_from_menu(sudo_password)
            run_firewall_tool_from_menu(sudo_password)
            run_interface_tool_from_menu(sudo_password)
            run_routing_tool_from_menu(sudo_password)
            run_network_test_from_menu(sudo_password)
            run_logs_tool_from_menu(sudo_password)
            print(get_system_info(sudo_password))  # Run system info tool
        else:
            # Run specific tools based on user's choice
            for choice in tool_choices:
                if choice == '1':
                    print(f"{Fore.GREEN}Running DNS Information 🌐...{Style.RESET_ALL}")
                    run_dns_tool_from_menu(sudo_password)
                elif choice == '2':
                    print(f"{Fore.GREEN}Running Memory and Disk Usage 💾...{Style.RESET_ALL}")
                    run_memory_tool_from_menu(sudo_password)
                elif choice == '3':
                    print(f"{Fore.GREEN}Running Firewall Information 🔥...{Style.RESET_ALL}")
                    run_firewall_tool_from_menu(sudo_password)
                elif choice == '4':
                    print(f"{Fore.GREEN}Running Interface Information 🖧...{Style.RESET_ALL}")
                    run_interface_tool_from_menu(sudo_password)
                elif choice == '5':
                    print(f"{Fore.GREEN}Running Routing Table and Traceroute 🗺...{Style.RESET_ALL}")
                    run_routing_tool_from_menu(sudo_password)
                elif choice == '6':
                    print(f"{Fore.GREEN}Running Net Speed Test, IP, Ping ⚡...{Style.RESET_ALL}")
                    run_network_test_from_menu(sudo_password)
                elif choice == '7':
                    print(f"{Fore.GREEN}Running System Logs (Last 10) 📜...{Style.RESET_ALL}")
                    run_logs_tool_from_menu(sudo_password)
                elif choice == '8':
                    print(f"{Fore.GREEN}Running System Info & ARP 🖥️...{Style.RESET_ALL}")
                    print(get_system_info(sudo_password))  # Call system info and ARP tool

        # Ask if they want to run another tool
        continue_choice = input(f"{Fore.GREEN}\nDo you want to run another tool? (y/n): {Style.RESET_ALL}").strip().lower()
        if continue_choice != 'y':
            print(f"{Fore.YELLOW}Thank you for using Linux Looker!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()

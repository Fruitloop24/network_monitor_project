import psutil
import subprocess
import socket
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_interface_details():
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        ip, subnet_mask = extract_ip_and_subnet(addrs)
        stats = psutil.net_if_stats().get(interface)

        if stats:
            mtu, is_up, duplex, speed = extract_interface_stats(interface, stats)
        else:
            mtu, is_up, duplex, speed = "Unknown", "Unknown", "Unknown", "Unknown"

        interfaces.append({
            "Interface": interface,
            "IP Address": ip,
            "Subnet Mask": subnet_mask,
            "Status": is_up,
            "MTU": mtu,
            "Duplex": duplex,
            "Speed (Mbps)": speed
        })
    
    return interfaces

def extract_ip_and_subnet(addrs):
    try:
        ip_info = [(addr.address, addr.netmask) for addr in addrs if addr.family == socket.AF_INET]
        if ip_info:
            return ip_info[0]
        else:
            return "N/A", "N/A"
    except Exception as e:
        return f"Error retrieving IP: {e}", f"Error retrieving Subnet Mask: {e}"

def extract_interface_stats(interface, stats):
    try:
        mtu = stats.mtu
        is_up = "Up" if stats.isup else "Down"
        duplex = detect_duplex(interface, stats.duplex)
        speed = stats.speed if stats.speed > 0 else "Unknown"
        return mtu, is_up, duplex, speed
    except Exception as e:
        return "Error retrieving MTU", "Error retrieving Status", "Error retrieving Duplex", f"Error retrieving Speed: {e}"

def detect_duplex(interface, initial_duplex):
    """Tries to detect duplex mode more accurately using ethtool."""
    if initial_duplex in [psutil.NIC_DUPLEX_FULL, psutil.NIC_DUPLEX_HALF]:
        return "Full" if initial_duplex == psutil.NIC_DUPLEX_FULL else "Half"

    try:
        ethtool_output = subprocess.run(
            f"ethtool {interface} | grep 'Duplex:'",
            shell=True, capture_output=True, text=True
        )
        if "Full" in ethtool_output.stdout:
            return "Full"
        elif "Half" in ethtool_output.stdout:
            return "Half"
        else:
            return "Unknown"
    except Exception as e:
        return f"Error detecting Duplex: {e}"

def get_vlans_and_errors(interface):
    try:
        errors = subprocess.run(f"ifconfig {interface} | grep 'errors'", shell=True, capture_output=True, text=True)
        vlan_info = subprocess.run(f"grep {interface} /proc/net/vlan/config", shell=True, capture_output=True, text=True)

        vlan_details = vlan_info.stdout.strip() if vlan_info.returncode == 0 else "No VLANs found."
        error_details = errors.stdout.strip() if errors.returncode == 0 else "No errors found."

        return f"{Fore.YELLOW}VLAN Info for {interface}:{Style.RESET_ALL}\n{vlan_details}\n\n{Fore.YELLOW}Error Info for {interface}:{Style.RESET_ALL}\n{error_details}\n\n"
    except Exception as e:
        return f"Error fetching VLAN or error details for {interface}: {str(e)}\n\n"

def format_interface_info(interface):
    return (
        f"{Fore.CYAN}Interface: {interface['Interface']}{Style.RESET_ALL}\n"
        f"  {Fore.GREEN}IP Address:{Style.RESET_ALL} {interface['IP Address']}\n"
        f"  {Fore.GREEN}Subnet Mask:{Style.RESET_ALL} {interface['Subnet Mask']}\n"
        f"  {Fore.GREEN}Status:{Style.RESET_ALL} {interface['Status']}\n"
        f"  {Fore.GREEN}MTU:{Style.RESET_ALL} {interface['MTU']}\n"
        f"  {Fore.GREEN}Duplex:{Style.RESET_ALL} {interface['Duplex']}\n"
        f"  {Fore.GREEN}Speed (Mbps):{Style.RESET_ALL} {interface['Speed (Mbps)']}\n"
    )

def get_all_interface_info():
    interfaces_info = get_interface_details()
    full_info = ""

    for interface in interfaces_info:
        full_info += format_interface_info(interface)
        full_info += get_vlans_and_errors(interface['Interface'])
        full_info += "-"*40 + "\n"

    return full_info

if __name__ == "__main__":
    try:
        interface_info = get_all_interface_info()
        print(interface_info)

        # Save to a text file (without color formatting)
        plain_text_info = interface_info.replace(Fore.CYAN, "").replace(Fore.GREEN, "").replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "")
        with open("interface_details.txt", "w") as file:
            file.write(plain_text_info)
        print("Summary saved to interface_details.txt")

    except Exception as e:
        print(f"Error: {str(e)}")








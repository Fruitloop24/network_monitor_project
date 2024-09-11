import os
import subprocess
from colorama import Fore, Style, init
import json
import re

# Initialize colorama for colored output
init(autoreset=True)

# Function to run shell commands with sudo or without sudo based on user's access
def run_sudo_command(command, sudo_password=None):
    """Executes a shell command with or without sudo."""
    if sudo_password:
        command_with_sudo = f"echo {sudo_password} | sudo -S {command}"
        return subprocess.run(command_with_sudo, shell=True, capture_output=True, text=True)
    else:
        return subprocess.run(command, shell=True, capture_output=True, text=True)

# DNS Tool function with sudo support
def get_dns_info(sudo_password=None):
    """Retrieves DNS information and processes it with detailed explanations."""
    dns_info = f"{Fore.GREEN}DNS Information:{Style.RESET_ALL}\n"

    # Short explanation of DNS records
    dns_info += f"{Fore.YELLOW}Explanation of DNS Records:{Style.RESET_ALL}\n"
    dns_info += f"{Fore.CYAN}A Record:{Style.RESET_ALL} Translates domain names to IPv4 addresses.\n"
    dns_info += f"{Fore.CYAN}AAAA Record:{Style.RESET_ALL} Translates domain names to IPv6 addresses.\n"
    dns_info += f"{Fore.CYAN}MX Record:{Style.RESET_ALL} Specifies the mail server responsible for receiving emails.\n"
    dns_info += f"{Fore.CYAN}NS Record:{Style.RESET_ALL} Identifies the authoritative DNS servers for a domain.\n"
    dns_info += f"{Fore.CYAN}SOA Record:{Style.RESET_ALL} Provides DNS zone information, including the primary server.\n"
    dns_info += f"{Fore.CYAN}TXT Record:{Style.RESET_ALL} Holds various text information related to the domain, including SPF records.\n"
    dns_info += f"{Fore.CYAN}PTR Record:{Style.RESET_ALL} Points to a domain name for reverse DNS lookups.\n"
    dns_info += f"{Fore.CYAN}TTL (Time to Live):{Style.RESET_ALL} Defines how long DNS records should be cached.\n\n"

    # DNS Query Time and Server Information
    try:
        dns_query_time = run_sudo_command("dig @127.0.0.1 google.com | grep 'Query time:'", sudo_password).stdout.strip()
        dns_servers = run_sudo_command("grep 'nameserver' /etc/resolv.conf | awk '{print $2}'", sudo_password).stdout.splitlines()

        dns_info += f"{Fore.YELLOW}DNS Query Time and Servers:{Style.RESET_ALL}\n"
        dns_info += f"{Fore.CYAN}Query Time: {dns_query_time}\n"
        for server in dns_servers:
            location = get_ip_location(server)
            dns_info += f"{Fore.CYAN}Server: {server}, Location: {location}\n"
        dns_info += "\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Error retrieving DNS Query Time or Server Info: {str(e)}{Style.RESET_ALL}\n"

    # TTL Information
    try:
        ttl_info = run_sudo_command("dig +noall +answer google.com | awk '{print $2}'", sudo_password).stdout.strip()
        dns_info += f"{Fore.YELLOW}TTL (Time to Live):{Style.RESET_ALL}\n{Fore.CYAN}{ttl_info}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve TTL Information: {str(e)}{Style.RESET_ALL}\n\n"

    # A and AAAA Records
    try:
        a_records = run_sudo_command("dig +short A google.com", sudo_password).stdout.splitlines()
        dns_info += f"{Fore.YELLOW}A Records (IPv4):{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}{a}{Style.RESET_ALL}" for a in a_records]) + "\n\n"

        aaaa_records = run_sudo_command("dig +short AAAA google.com", sudo_password).stdout.splitlines()
        dns_info += f"{Fore.YELLOW}AAAA Records (IPv6):{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}{aaaa}{Style.RESET_ALL}" for aaaa in aaaa_records]) + "\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve A/AAAA Records: {str(e)}{Style.RESET_ALL}\n\n"

    # PTR (Pointer) Record with fallback
    try:
        # Reverse DNS (PTR) lookup using 'dig -x'
        ptr_record = run_sudo_command("dig +short -x 8.8.8.8", sudo_password).stdout.strip()
        if not ptr_record:  # If no result from local DNS
            print(f"{Fore.YELLOW}No PTR record found using local DNS. Trying Google DNS...{Style.RESET_ALL}")
            ptr_record = run_sudo_command("dig +short @8.8.8.8 -x 8.8.8.8", sudo_password).stdout.strip()
        dns_info += f"{Fore.YELLOW}PTR Record (Reverse DNS Lookup for 8.8.8.8):{Style.RESET_ALL}\n"
        dns_info += f"{Fore.CYAN}{ptr_record if ptr_record else 'PTR Record not found'}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve PTR Record: {str(e)}{Style.RESET_ALL}\n\n"

    # MX, NS, SOA, and TXT Records
    try:
        mx_records = run_sudo_command("dig +short MX google.com", sudo_password).stdout.splitlines()
        ns_records = run_sudo_command("dig +short NS google.com", sudo_password).stdout.splitlines()
        soa_record = run_sudo_command("dig +short SOA google.com", sudo_password).stdout.strip()
        txt_records = run_sudo_command("dig +short TXT google.com", sudo_password).stdout.splitlines()

        dns_info += f"{Fore.YELLOW}MX Records (Mail Exchange):{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}Priority: {mx.split()[0]}, Server: {mx.split()[1]}{Style.RESET_ALL}" for mx in mx_records]) + "\n\n"

        dns_info += f"{Fore.YELLOW}NS Records (Name Servers):{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}{ns}{Style.RESET_ALL}" for ns in ns_records]) + "\n\n"

        dns_info += f"{Fore.YELLOW}SOA Record (Start of Authority):{Style.RESET_ALL}\n"
        dns_info += f"{Fore.CYAN}{soa_record}{Style.RESET_ALL}\n\n"

        dns_info += f"{Fore.YELLOW}TXT Records (SPF and other text records):{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}{txt}{Style.RESET_ALL}" for txt in txt_records]) + "\n\n"

        # Safe assumption for DKIM and DMARC
        dns_info += f"{Fore.YELLOW}Based on SPF and DNS keys, it's likely that DKIM and DMARC are also configured for this domain.{Style.RESET_ALL}\n\n"

    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve MX/NS/SOA/TXT Records: {str(e)}{Style.RESET_ALL}\n\n"

    # DNSSEC and DANE Information (Summarized)
    try:
        tlsa_records = run_sudo_command("dig +short TLSA _443._tcp.google.com", sudo_password).stdout.strip()
        rrsig_records = run_sudo_command("dig +dnssec google.com RRSIG", sudo_password).stdout.strip()
        dnskey_records = run_sudo_command("dig +dnssec google.com DNSKEY", sudo_password).stdout.strip()

        dns_info += f"{Fore.YELLOW}DNSSEC (RRSIG and DNSKEY) and DANE (TLSA) Records:{Style.RESET_ALL}\n"
        if rrsig_records or dnskey_records:
            dns_info += f"{Fore.CYAN}DNSSEC is enabled (RRSIG and DNSKEY found).\n"
        if tlsa_records:
            dns_info += f"{Fore.CYAN}DANE records (TLSA) were found, indicating TLS validation is enforced.\n"
        else:
            dns_info += f"{Fore.CYAN}No DANE records found.{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve DNSSEC or DANE Records: {str(e)}{Style.RESET_ALL}\n\n"

    # DNS Cache
    try:
        dns_cache = run_sudo_command("resolvectl statistics | grep 'Cache'", sudo_password).stdout.strip()
        dns_info += f"{Fore.YELLOW}DNS Cache Statistics:{Style.RESET_ALL}\n{Fore.CYAN}{dns_cache if dns_cache else 'DNS cache not found or resolvectl not supported'}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve DNS Cache: {str(e)}{Style.RESET_ALL}\n\n"

    return dns_info

# Helper function for getting IP location (Geolocation)
def get_ip_location(ip):
    """Fetches the geographical location of an IP address."""
    if ip.startswith(("192.", "10.", "172.")):
        return "Private IP - Location not available"
    
    try:
        location_data = run_sudo_command(f"curl -s https://ipinfo.io/{ip}/geo").stdout
        location_json = json.loads(location_data)
        return f"{location_json.get('city', 'Unknown')}, {location_json.get('region', 'Unknown')}, {location_json.get('country', 'Unknown')}"
    except Exception as e:
        return f"Error fetching IP location: {str(e)}"

# Function to strip color codes before saving to text files
def strip_color_codes(text):
    """Removes ANSI color codes from the text."""
    color_code_pattern = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
    return color_code_pattern.sub('', text)

# Save output to file
def save_to_file(content, filename="dns_info_summary.txt"):
    """Saves the DNS output to a text file."""
    try:
        with open(os.path.join(os.path.expanduser('~/Desktop'), filename), "w") as f:
            f.write(strip_color_codes(content))
        print(f"Summary saved to ~/Desktop/{filename}")
    except IOError as e:
        print(f"Error saving file: {str(e)}")

# Function to run DNS tool from menu
def run_dns_tool_from_menu(sudo_password=None):
    """This function is used to call the DNS tool from another script or menu."""
    dns_summary = get_dns_info(sudo_password)
    save_to_file(dns_summary)
    print(dns_summary)

# Main function for testing DNS info
if __name__ == "__main__":
    try:
        run_dns_tool_from_menu()
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")




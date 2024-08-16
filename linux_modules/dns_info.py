import subprocess
from colorama import Fore, Style, init
import json
import re

init(autoreset=True)

def run_command(command, timeout=10):
    """Executes a shell command and returns the output or error message."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            return f"Error running command '{command}': {result.stderr.strip()}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"Command '{command}' timed out"
    except Exception as e:
        return f"Unexpected error running command '{command}': {str(e)}"

def strip_color_codes(text):
    """Removes color codes from the text."""
    color_code_pattern = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
    return color_code_pattern.sub('', text)

def get_ip_location(ip):
    """Fetches the geographical location of an IP address."""
    if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172."):
        return "Private IP - Location not available"
    
    try:
        location = run_command(f"curl -s https://ipinfo.io/{ip}/geo")
        if not location:
            return "Location not found"
        
        location_json = json.loads(location)
        city = location_json.get('city', 'Unknown')
        region = location_json.get('region', 'Unknown')
        country = location_json.get('country', 'Unknown')
        organization = location_json.get('org', 'Unknown')

        return f"City: {city}, Region: {region}, Country: {country}, Organization: {organization}"
    except Exception as e:
        return f"Error fetching location for IP {ip}: {str(e)}"

def get_ssl_info(domain):
    """Retrieves SSL certificate information for a domain."""
    ssl_info = f"{Fore.GREEN}SSL Certificate Information for {domain}:{Style.RESET_ALL}\n"
    ssl_command = f"echo | openssl s_client -showcerts -servername {domain} -connect {domain}:443 2>/dev/null | openssl x509 -noout -dates -issuer -subject"
    ssl_output = run_command(ssl_command)
    
    if "Error" in ssl_output or not ssl_output:
        ssl_info += f"{Fore.RED}Failed to retrieve SSL certificate for {domain}{Style.RESET_ALL}\n"
    else:
        issuer = re.search(r'issuer=([^,\n]+)', ssl_output)
        subject = re.search(r'subject=([^,\n]+)', ssl_output)
        not_before = re.search(r'notBefore=([^,\n]+)', ssl_output)
        not_after = re.search(r'notAfter=([^,\n]+)', ssl_output)

        ssl_info += f"{Fore.YELLOW}Issuer:{Style.RESET_ALL} {issuer.group(1) if issuer else 'Unknown'}\n"
        ssl_info += f"{Fore.YELLOW}Subject:{Style.RESET_ALL} {subject.group(1) if subject else 'Unknown'}\n"
        ssl_info += f"{Fore.YELLOW}Valid From:{Style.RESET_ALL} {not_before.group(1) if not_before else 'Unknown'}\n"
        ssl_info += f"{Fore.YELLOW}Valid Until:{Style.RESET_ALL} {not_after.group(1) if not_after else 'Unknown'}\n\n"
    
    return ssl_info

def get_dns_info():
    dns_info = f"{Fore.GREEN}DNS Information:{Style.RESET_ALL}\n"

    dns_info += f"{Fore.YELLOW}Explanation of DNS Records:{Style.RESET_ALL}\n"
    dns_info += f"{Fore.CYAN}A Record:{Style.RESET_ALL} Translates domain names to IP addresses (IPv4).\n"
    dns_info += f"{Fore.CYAN}AAAA Record:{Style.RESET_ALL} Translates domain names to IP addresses (IPv6).\n"
    dns_info += f"{Fore.CYAN}MX Record:{Style.RESET_ALL} Specifies the mail server responsible for receiving emails.\n"
    dns_info += f"{Fore.CYAN}NS Record:{Style.RESET_ALL} Identifies the authoritative DNS servers for a domain.\n"
    dns_info += f"{Fore.CYAN}SOA Record:{Style.RESET_ALL} Provides information about the DNS zone, including the primary DNS server and email of the domain administrator.\n"
    dns_info += f"{Fore.CYAN}TXT Record:{Style.RESET_ALL} Holds various text information related to the domain, including SPF records.\n"
    dns_info += f"{Fore.CYAN}DANE (TLSA) Record:{Style.RESET_ALL} Associates a TLS server certificate with a domain name using DNSSEC.\n"
    dns_info += f"{Fore.CYAN}RRSIG Record:{Style.RESET_ALL} Contains a cryptographic signature for DNSSEC.\n"
    dns_info += f"{Fore.CYAN}DNSKEY Record:{Style.RESET_ALL} Holds the public key used in DNSSEC.\n"
    dns_info += f"{Fore.CYAN}PTR Record:{Style.RESET_ALL} Maps an IP address to a domain name (reverse DNS).\n"
    dns_info += f"{Fore.CYAN}TTL (Time to Live):{Style.RESET_ALL} Defines how long DNS records should be cached.\n\n"

    try:
        # Query Time
        dns_query_time = run_command("dig @127.0.0.1 google.com | grep 'Query time:'")
        dns_info += f"{Fore.YELLOW}Query Time:{Style.RESET_ALL}\n{dns_query_time}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve Query Time: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # DNS Servers and Locations
        dns_servers = run_command("grep 'nameserver' /etc/resolv.conf | awk '{print $2}'").splitlines()
        dns_info += f"{Fore.YELLOW}DNS Servers:{Style.RESET_ALL}\n"
        for server in dns_servers:
            location = get_ip_location(server)
            dns_info += f"{Fore.CYAN}Server: {server}\nLocation: {location}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve DNS Servers: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # TXT Records (including SPF)
        txt_records = run_command("dig +short TXT google.com")
        spf_records = []
        other_txt_records = []

        for record in txt_records.splitlines():
            if "v=spf1" in record:
                spf_records.append(record.strip())
            else:
                other_txt_records.append(record.strip())

        dns_info += f"{Fore.YELLOW}SPF Record:{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.MAGENTA}{spf}{Style.RESET_ALL}" for spf in spf_records]) + "\n\n"

        dns_info += f"{Fore.YELLOW}Other TXT Records:{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.MAGENTA}{txt}{Style.RESET_ALL}" for txt in other_txt_records]) + "\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve TXT Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # MX Records
        mx_records = run_command("dig +short MX google.com").splitlines()
        dns_info += f"{Fore.YELLOW}MX Records:{Style.RESET_ALL}\n"
        for mx in mx_records:
            dns_info += f"{Fore.CYAN}Priority: {mx.split()[0]}, Server: {mx.split()[1]}{Style.RESET_ALL}\n"
        dns_info += "\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve MX Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # NS Records
        ns_records = run_command("dig +short NS google.com").splitlines()
        dns_info += f"{Fore.YELLOW}NS Records:{Style.RESET_ALL}\n"
        for ns in ns_records:
            dns_info += f"{Fore.CYAN}{ns}{Style.RESET_ALL}\n"
        dns_info += "\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve NS Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # SOA Record
        soa_record = run_command("dig +short SOA google.com")
        dns_info += f"{Fore.YELLOW}SOA Record:{Style.RESET_ALL}\n{Fore.CYAN}{soa_record}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve SOA Record: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # A Records
        a_records = run_command("dig +short A google.com").splitlines()
        dns_info += f"{Fore.YELLOW}A Records:{Style.RESET_ALL}\n"
        for a in a_records:
            dns_info += f"{Fore.CYAN}{a}{Style.RESET_ALL}\n"
        dns_info += "\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve A Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # AAAA Records
        aaaa_records = run_command("dig +short AAAA google.com").splitlines()
        dns_info += f"{Fore.YELLOW}AAAA Records:{Style.RESET_ALL}\n"
        for aaaa in aaaa_records:
            dns_info += f"{Fore.CYAN}{aaaa}{Style.RESET_ALL}\n"
        dns_info += "\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve AAAA Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # TTL Information
        ttl_info = run_command("dig +noall +answer google.com | awk '{print $2}'")
        dns_info += f"{Fore.YELLOW}TTL (Time to Live):{Style.RESET_ALL}\n{Fore.CYAN}{ttl_info}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve TTL Information: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # DANE (TLSA) Records
        tlsa_records = run_command("dig +short TLSA _443._tcp.google.com").splitlines()
        dns_info += f"{Fore.YELLOW}DANE (TLSA) Records:{Style.RESET_ALL}\n"
        if tlsa_records:
            for tlsa in tlsa_records:
                dns_info += f"{Fore.CYAN}{tlsa}{Style.RESET_ALL}\n"
        else:
            dns_info += f"{Fore.RED}No DANE (TLSA) records found{Style.RESET_ALL}\n"
        dns_info += "\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve DANE (TLSA) Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # DNSSEC Records (RRSIG and DNSKEY)
        rrsig_records = run_command("dig +dnssec google.com RRSIG").splitlines()
        dnskey_records = run_command("dig +dnssec google.com DNSKEY").splitlines()
        dns_info += f"{Fore.YELLOW}RRSIG Records:{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}{rrsig}{Style.RESET_ALL}" for rrsig in rrsig_records])
        dns_info += "\n\n"
        dns_info += f"{Fore.YELLOW}DNSKEY Records:{Style.RESET_ALL}\n"
        dns_info += "\n".join([f"{Fore.CYAN}{dnskey}{Style.RESET_ALL}" for dnskey in dnskey_records])
        dns_info += "\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve DNSSEC Records: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # DNS Cache (Using resolvectl)
        dns_cache = run_command("resolvectl statistics | grep 'Cache'")
        dns_info += f"{Fore.YELLOW}DNS Cache:{Style.RESET_ALL}\n{Fore.CYAN}{dns_cache if dns_cache else 'DNS cache not found or resolvectl not supported'}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve DNS Cache: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # PTR Record (Reverse DNS)
        ptr_record = run_command("dig -x 127.0.0.1 +short")
        dns_info += f"{Fore.YELLOW}PTR Record (Reverse DNS):{Style.RESET_ALL}\n{Fore.CYAN}{ptr_record if ptr_record else 'No PTR record found'}{Style.RESET_ALL}\n\n"
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve PTR Record: {str(e)}{Style.RESET_ALL}\n\n"

    try:
        # SSL Information
        ssl_info = get_ssl_info("google.com")
        dns_info += ssl_info
    except Exception as e:
        dns_info += f"{Fore.RED}Failed to retrieve SSL Information: {str(e)}{Style.RESET_ALL}\n\n"

    return dns_info

def save_to_file(content, filename="dns_info_summary.txt"):
    """Saves the given content to a text file, stripping out color codes."""
    try:
        with open(filename, "w") as f:
            plain_content = strip_color_codes(content)
            f.write(plain_content)
        print(f"Summary saved to {filename}")
    except IOError as e:
        print(f"Error saving file: {str(e)}")

if __name__ == "__main__":
    try:
        dns_summary = get_dns_info()
        save_to_file(dns_summary)
        print(dns_summary)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

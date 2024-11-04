import subprocess
import speedtest
import socket
import requests
from colorama import Fore, Style, init
from pathlib import Path

# Initialize colorama
init(autoreset=True)

def run_speed_test(sudo_password=None):
    """Runs a network speed test and returns the results."""
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    server_info = st.get_best_server()

    # CLI Output
    print(f"{Fore.GREEN}Network Speed Test:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Server: {server_info['host']} ({server_info['name']}, {server_info['country']})")
    print(f"Download Speed: [{Fore.GREEN}{'█' * int(download_speed / 10)}{'░' * (20 - int(download_speed / 10))}{Style.RESET_ALL}] {download_speed:.2f} Mbps")
    print(f"Upload Speed: [{Fore.GREEN}{'█' * int(upload_speed / 10)}{'░' * (20 - int(upload_speed / 10))}{Style.RESET_ALL}] {upload_speed:.2f} Mbps")

    # Fetch Public IP and Location
    public_ip, location = get_public_ip_and_location()
    print(f"\nPublic IP: {public_ip}")
    print(f"Location: {location}")

    # Private IP
    private_ip = get_private_ip()
    print(f"Private IP: {private_ip}")

    # Ping Test (if sudo_password is provided, use sudo, else run normally)
    ping_result = run_ping_test(sudo_password)

    # Save the plain text output to a file on the desktop
    save_plain_text_output(server_info, download_speed, upload_speed, public_ip, location, private_ip, ping_result)

def get_public_ip_and_location():
    """Fetches the user's public IP and location information."""
    try:
        ip_info = requests.get("https://api.ipify.org?format=json").json()
        public_ip = ip_info.get("ip")
        
        # Fetch location based on public IP (optional, can be turned off for privacy)
        location_info = requests.get(f"https://ipinfo.io/{public_ip}/json").json()
        location = f"{location_info.get('city', '')}, {location_info.get('region', '')}, {location_info.get('country', '')}"
    except Exception as e:
        public_ip, location = "Unknown", "Unknown"
        print(f"{Fore.RED}Failed to fetch public IP and location: {e}{Style.RESET_ALL}")
    
    return public_ip, location

def get_private_ip():
    """Retrieves the private IP from the main interface."""
    try:
        private_ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
        if private_ip:
            return private_ip
        else:
            raise ValueError("No private IP found.")
    except Exception as e:
        return f"{Fore.RED}Failed to retrieve private IP: {e}{Style.RESET_ALL}"

def run_ping_test(sudo_password):
    """Performs a ping test, checks for sudo requirements."""
    try:
        if sudo_password:
            ping_result = subprocess.run(f"echo {sudo_password} | sudo -S ping -c 4 google.com", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            ping_result = subprocess.run(["ping", "-c", "4", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        latency = extract_latency(ping_result.stdout.decode())
        print(f"\nPing Test:")
        print(f"Latency: {latency} ms")
        return latency
    except Exception as e:
        return f"{Fore.RED}Error: Sudo privileges required for ping test or permission denied{Style.RESET_ALL}"

def extract_latency(ping_output):
    """Extracts the latency from the ping command output."""
    lines = ping_output.splitlines()
    for line in lines:
        if "avg" in line:
            latency = line.split('/')[4]  # Get the average latency value
            return latency
    return "Unknown"

def save_plain_text_output(server_info, download_speed, upload_speed, public_ip, location, private_ip, latency):
    """Saves the plain text output to a file on the desktop."""
    desktop_path = Path.home() / "Desktop" / "network_speed_test_results.txt"
    with desktop_path.open("w") as f:
        f.write("Network Speed Test:\n")
        f.write(f"Server: {server_info['host']} ({server_info['name']}, {server_info['country']})\n")
        f.write(f"Download Speed: {download_speed:.2f} Mbps\n")
        f.write(f"Upload Speed: {upload_speed:.2f} Mbps\n\n")
        f.write(f"Public IP: {public_ip}\n")
        f.write(f"Location: {location}\n")
        f.write(f"Private IP: {private_ip}\n\n")
        f.write("Ping Test:\n")
        f.write(f"Latency: {latency} ms\n")
    print(f"Summary saved to {desktop_path}")

# Function to call from the menu
def run_network_test_from_menu(sudo_password=None):
    """Wrapper to call the speed test from the menu."""
    run_speed_test(sudo_password)

if __name__ == "__main__":
    run_speed_test()



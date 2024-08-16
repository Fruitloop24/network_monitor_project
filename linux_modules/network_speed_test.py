import subprocess
import speedtest
import socket
import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def run_speed_test():
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

    # Public IP and Location
    ip_info = requests.get("https://ipinfo.io").json()
    public_ip = ip_info.get("ip")
    location = f"{ip_info.get('city', '')}, {ip_info.get('region', '')}, {ip_info.get('country', '')}"

    print(f"\nPublic IP: {public_ip}")
    print(f"Location: {location}")

    # Private IP
    try:
        private_ip = socket.gethostbyname(socket.gethostname())
        if private_ip.startswith("127."):
            raise ValueError("No valid private IP found.")
        print(f"Private IP: {private_ip}")
    except Exception as e:
        print(f"{Fore.RED}Private IP: Failed to retrieve private IP. Error: {e}{Style.RESET_ALL}")

    # Ping Test
    ping_result = subprocess.run(["ping", "-c", "4", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    latency = extract_latency(ping_result.stdout.decode())
    print(f"\nPing Test:")
    print(f"Latency: {latency} ms")

    # Save the plain text output to a file
    save_plain_text_output(server_info, download_speed, upload_speed, public_ip, location, private_ip, latency)

def extract_latency(ping_output):
    """Extracts the latency from the ping command output."""
    lines = ping_output.splitlines()
    for line in lines:
        if "avg" in line:
            latency = line.split('/')[4]  # Get the average latency value
            return latency
    return "Unknown"

def save_plain_text_output(server_info, download_speed, upload_speed, public_ip, location, private_ip, latency):
    """Saves the plain text output to a file."""
    with open("network_speed_test_results.txt", "w") as f:
        f.write("Network Speed Test:\n")
        f.write(f"Server: {server_info['host']} ({server_info['name']}, {server_info['country']})\n")
        f.write(f"Download Speed: {download_speed:.2f} Mbps\n")
        f.write(f"Upload Speed: {upload_speed:.2f} Mbps\n\n")
        f.write(f"Public IP: {public_ip}\n")
        f.write(f"Location: {location}\n")
        f.write(f"Private IP: {private_ip if private_ip else 'Failed to retrieve private IP.'}\n\n")
        f.write("Ping Test:\n")
        f.write(f"Latency: {latency} ms\n")

if __name__ == "__main__":
    run_speed_test()

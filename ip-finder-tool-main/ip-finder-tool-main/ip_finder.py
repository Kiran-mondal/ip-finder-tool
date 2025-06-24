import socket
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
from pyfiglet import Figlet
from rich import print
from rich.table import Table

API_URL = "https://ipinfo.io/{}?token=a6420792a3520a"  # Replace with your token
LOG_FILE = "log.json"

figlet = Figlet(font='slant')
print(f"[bold blue]{figlet.renderText('IP Finder Tool')}[/bold blue]")

def extract_domain(input_str):
    if input_str.startswith("http://") or input_str.startswith("https://"):
        parsed_url = urlparse(input_str)
        return parsed_url.hostname
    return input_str

def get_ip_info(ip_or_domain):
    try:
        # Extract domain if URL is given
        domain = extract_domain(ip_or_domain)
        ip_address = socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"[red]Invalid domain, URL or IP: {ip_or_domain}[/red]")
        return None

    response = requests.get(API_URL.format(ip_address))
    if response.status_code != 200:
        print("[red]Failed to fetch IP info.[/red]")
        return None

    data = response.json()
    data["ip"] = ip_address  # Add resolved IP
    data["hostname"] = data.get("hostname", socket.getfqdn(ip_address))
    return data

def print_ip_info(data):
    table = Table(title="📍 IP Information")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    fields = [
        ("IP", data.get("ip", "N/A")),
        ("Hostname", data.get("hostname", "N/A")),
        ("City", data.get("city", "N/A")),
        ("Region", data.get("region", "N/A")),
        ("Country", data.get("country", "N/A")),
        ("Location", data.get("loc", "N/A")),
        ("Org", data.get("org", "N/A")),
        ("Timezone", data.get("timezone", "N/A"))
    ]

    for name, value in fields:
        table.add_row(name, value)

    print(table)

def save_log(entry):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    entry["timestamp"] = datetime.now().isoformat()
    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

while True:
    user_input = input("\nEnter domain, link, or IP (leave blank for your own): ").strip()
    if not user_input:
        user_input = requests.get("https://api.ipify.org").text
        print(f"[yellow]Detected your IP: {user_input}[/yellow]")

    ip_info = get_ip_info(user_input)
    if ip_info:
        print_ip_info(ip_info)
        save_log(ip_info)

    try:
        again = input("\n[?] Lookup another? (y/n): ").strip().lower()
        if again != 'y':
            break
    except KeyboardInterrupt:
        break


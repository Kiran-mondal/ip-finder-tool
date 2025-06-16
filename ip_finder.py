import socket
import requests
import pyfiglet
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
LOG_FILE = "log.json"

def show_banner():
    banner = pyfiglet.figlet_format("IP Finder v2.0", font="slant")
    console.clear()
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print(Panel.fit("[bold green]IP Lookup Tool by Kiran Mondal[/]\n[bold blue]GitHub:[/] https://github.com/Kiran-mondal/ip-finder-tool"))

def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_ip_info(ip):
    try:
        return requests.get(f"https://ipinfo.io/{ip}/json").json()
    except Exception as e:
        return {"error": str(e)}

def print_info(info):
    if "error" in info:
        console.print(f"[bold red]❌ Error:[/] {info['error']}")
        return
    table = Table(title="📍 IP Info", style="cyan")
    table.add_column("Field", style="bold yellow")
    table.add_column("Value", style="white")
    for key, value in info.items():
        table.add_row(str(key), str(value))
    console.print(table)

def save_log(ip, info):
    log = {"ip": ip, "timestamp": datetime.now().isoformat(), "data": info}
    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    data.append(log)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    show_banner()
    while True:
        user_input = Prompt.ask("\n[bold green]Enter IP or domain (or leave blank to auto-detect)[/]").strip()

        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold red]👋 Goodbye![/bold red]")
            break

        if not user_input:
            user_input = requests.get("https://api.ipify.org").text
            console.print(f"[bold blue]Your public IP:[/] {user_input}")
        elif not user_input.replace('.', '').isdigit():
            resolved = resolve_domain(user_input)
            if resolved:
                console.print(f"[bold blue]Resolved IP:[/] {resolved}")
                user_input = resolved
            else:
                console.print("[bold red]❌ Invalid domain.[/]")
                continue

        info = get_ip_info(user_input)
        print_info(info)
        save_log(user_input, info)

        again = Prompt.ask("[bold magenta]🔁 Lookup again? (y/n)[/]", default="y")
        if again.lower() != "y":
            break

if __name__ == "__main__":
    main()

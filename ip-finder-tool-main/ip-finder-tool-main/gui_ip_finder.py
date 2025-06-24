import socket
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import tkinter as tk
from tkinter import messagebox, scrolledtext

API_URL = "https://ipinfo.io/{}?token=a6420792a3520a"  # Replace with your token
LOG_FILE = "log.json"


def extract_domain(input_str):
    if input_str.startswith("http://") or input_str.startswith("https://"):
        parsed_url = urlparse(input_str)
        return parsed_url.hostname
    return input_str


def get_ip_info(ip_or_domain):
    try:
        domain = extract_domain(ip_or_domain)
        ip_address = socket.gethostbyname(domain)
    except socket.gaierror:
        return f"Invalid domain, URL or IP: {ip_or_domain}"

    response = requests.get(API_URL.format(ip_address))
    if response.status_code != 200:
        return "Failed to fetch IP info."

    data = response.json()
    data["ip"] = ip_address
    data["hostname"] = data.get("hostname", socket.getfqdn(ip_address))
    return data


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


def show_info():
    user_input = entry.get().strip()
    if not user_input:
        user_input = requests.get("https://api.ipify.org").text

    result = get_ip_info(user_input)
    if isinstance(result, str):
        messagebox.showerror("Error", result)
    else:
        output = f"IP: {result.get('ip', 'N/A')}\n"
        output += f"Hostname: {result.get('hostname', 'N/A')}\n"
        output += f"City: {result.get('city', 'N/A')}\n"
        output += f"Region: {result.get('region', 'N/A')}\n"
        output += f"Country: {result.get('country', 'N/A')}\n"
        output += f"Location: {result.get('loc', 'N/A')}\n"
        output += f"Org: {result.get('org', 'N/A')}\n"
        output += f"Timezone: {result.get('timezone', 'N/A')}\n"

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, output)

        save_log(result)


# GUI setup
root = tk.Tk()
root.title("IP Finder Tool GUI")
root.geometry("500x400")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill="both")

title = tk.Label(frame, text="IP Finder Tool", font=("Helvetica", 18, "bold"))
title.pack(pady=10)

entry = tk.Entry(frame, width=40)
entry.pack(pady=5)
entry.insert(0, "Enter domain, link, or IP")

btn = tk.Button(frame, text="Find IP Info", command=show_info, bg="#007acc", fg="white")
btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(frame, height=10, width=60)
output_box.pack(pady=10)

root.mainloop()


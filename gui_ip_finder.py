import tkinter as tk
from tkinter import messagebox
import socket
import requests
import json
from datetime import datetime

def resolve_hostname(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def get_ip_info(ip):
    try:
        return requests.get(f"https://ipinfo.io/{ip}/json").json()
    except:
        return {"error": "Unable to fetch IP info."}

def log_to_file(ip, data):
    entry = {
        "ip": ip,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    try:
        with open("log.json", "r") as f:
            existing = json.load(f)
    except:
        existing = []
    existing.append(entry)
    with open("log.json", "w") as f:
        json.dump(existing, f, indent=4)

def search_ip():
    domain = entry.get().strip()
    if not domain:
        domain = requests.get("https://api.ipify.org").text
    elif not domain.replace(".", "").isdigit():
        domain = resolve_hostname(domain)
        if not domain:
            messagebox.showerror("Error", "Invalid domain.")
            return

    data = get_ip_info(domain)
    log_to_file(domain, data)
    result.delete("1.0", tk.END)
    for k, v in data.items():
        result.insert(tk.END, f"{k}: {v}\n")

root = tk.Tk()
root.title("IP Finder Tool")
root.geometry("400x400")

tk.Label(root, text="Enter IP or Domain:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack()

tk.Button(root, text="Lookup", command=search_ip).pack(pady=10)
result = tk.Text(root, height=15, width=50)
result.pack(pady=10)

root.mainloop()

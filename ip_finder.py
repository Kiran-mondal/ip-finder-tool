import requests
import socket

def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

if __name__ == "__main__":
    print("🔎 IP Finder Tool")
    print("--------------------------")
    user_input = input("Enter IP address or website (e.g., google.com): ").strip()

    if user_input == "":
        user_input = requests.get("https://api.ipify.org").text
        print(f"\n🌐 Using your public IP: {user_input}")
    elif not user_input.replace('.', '').isdigit():
        resolved_ip = resolve_hostname(user_input)
        if resolved_ip:
            print(f"\n🌐 Resolved IP for {user_input}: {resolved_ip}")
            user_input = resolved_ip
        else:
            print("❌ Error: Could not resolve hostname.")
            exit()

    info = get_ip_info(user_input)

    print("\n📌 IP Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

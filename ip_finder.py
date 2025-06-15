import requests

def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    ip = input("Enter IP address (leave blank for your IP): ").strip()
    if ip == "":
        ip = requests.get("https://api.ipify.org").text

    info = get_ip_info(ip)

    print("\nIP Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

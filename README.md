🌐 IP Finder Tool



A powerful terminal-based IP & domain lookup tool with auto-detection and live IP information fetching using the IPinfo API. Stylish, informative, and logs everything you check!


---

✨ Features

🔗 Accepts domain, IP, or URL as input

🔍 Auto-detects your own public IP if no input is provided

🌎 Displays detailed location and network info:

IP Address

Hostname

City, Region, Country

Location (lat, long)

Organization

Timezone


📊 Clean output in styled tables using rich

🎨 Banner header using pyfiglet

📁 Auto-logs results in log.json with timestamps

🔁 Loops until you exit (Ctrl+C or type 'n')



---

🚀 Installation

# Clone the repository
git clone https://github.com/Kiran-mondal/ip-finder-tool.git
cd ip-finder-tool

# Install dependencies
pip install -r requirements.txt

Dependencies:

requests

pyfiglet

rich



---

🛠 Usage

python ip_finder.py

Example

Enter domain, link, or IP (leave blank for your own): google.com

📍 IP Information:
+-------------+---------------------------+
| Field       | Value                     |
+-------------+---------------------------+
| IP          | 142.250.195.142           |
| Hostname    | lhr25s12-in-f14.1e100.net |
| City        | London                    |
| Region      | England                   |
| Country     | GB                        |
| Location    | 51.5074,-0.1278           |
| Org         | Google LLC                |
| Timezone    | Europe/London             |
+-------------+---------------------------+


---

💡 Developer

👨‍💻 Developed by: Kiran Mondal

📍 Runs on: Termux / Linux / Windows Terminal / macOS Terminal



---

📌 Note

> 🔐 You need to set your own IPinfo API Token in the script. Get it free at: https://ipinfo.io/signup



Replace this line in the code:

API_URL = "https://ipinfo.io/{}?token=your_token_here"


---

📦 License

This project is licensed under the MIT License. See LICENSE for more info.


---

🖼 Preview (Coming soon!)

Animated example GIF or screenshot will be added soon to help visualize usage.


---

Happy hacking! 🚀


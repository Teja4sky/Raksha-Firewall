# **🛡️ Rasksaa — Personal Privacy Firewall**


“Your Network’s Silent Guardian.”
Built for users who value privacy and control above everything else.


Rasksaa is a Python-based, headless network firewall designed to monitor and protect local networks in real time. It detects suspicious activity — such as port scans, SYN floods, and unusual packet bursts — and automatically blocks attacker IPs using system-level firewall rules.


 ### **Overview**

Rasksaa (from the Sanskrit word Raksha, meaning Protection) is a Python-based, headless network firewall designed for personal systems where privacy is the top priority.


It provides real-time protection against common cyber threats like:

**Port Scanning**

**SYN / UDP Floods**

**Abnormal Packet Bursts**


Rasksaa automatically monitors network packets, detects unusual activity, and blocks suspicious IPs — all while keeping the user in full control.
It’s designed for individuals, developers, and privacy-conscious users, not for enterprise or commercial use.



## ⚙️ Core Features
Feature	Description
🔍 Real-Time Detection	Monitors live network packets and identifies suspicious patterns
🚫 Auto Blocking	Instantly blocks offending IPs using Linux firewall (iptables)
🧾 Whitelist	Prevents blocking of trusted devices
📋 Logging	Logs all events in text and CSV formats for transparency
💡 Headless Operation	Runs without a GUI — perfect for servers and Raspberry Pi
🔒 Offline Privacy	No internet dependency, no tracking, no telemetry
⚙️ Lightweight	Uses very low CPU and RAM resources
🧩 Portable	Runs on Linux, Raspberry Pi OS, or Ubuntu



## Technical Stack 
Component	Technology
Language	Python 3.10+
Firewall Engine	iptables
Packet Capture	Scapy
Configuration	JSON
Logging	TXT + CSV
Platforms	Linux / Raspberry Pi / Ubuntu



## **🧾 Installation**
1️⃣ Clone Repository
git clone https://github.com/Teja4sky/Raksha-Firewall.git

  cd Rasksaa

2️⃣ Install Dependencies

  pip install -r requirements.txt

3️⃣ Run the Firewall (root required)

  sudo python3 rasksaa_firewall.py



## 🔧 Configuration
✅ Whitelist File (whitelist.json)
{
  "whitelist": [
    "127.0.0.1",
    "192.168.1.10"
  ]
}


Add your trusted devices here (to prevent accidental blocking).

Keep this list short and specific to maintain strict protection.






## 📊 Output Example
[12:10:52] 🚀 Rasksaa Started — Monitoring traffic 

[12:11:23] [ALERT] Port Scan Detected from 192.168.1.8 (12 ports)

[12:11:23] [BLOCKED] IP 192.168.1.8 added to firewall rules

[12:11:23] [LOG] Event written to firewall_log.txt






## 🧪 Testing

Run only in a controlled lab or your personal system.

Test Type	Command	Expected Result
Port Scan	nmap -sS <target-ip>	Detected & blocked
SYN Flood	sudo hping3 -S -p 80 --flood <target-ip>	Blocked instantly
View Rules	sudo iptables -L	Displays blocked IPs
Flush Rules	sudo iptables -F	Clears all blocks






## 🧩 Future Roadmap
Version	Planned Feature
v2.0	Web dashboard (Flask-based UI)

v3.0	AI-based anomaly detection

v4.0	Dual network mode (wired + wireless)

v5.0	Cloud-sync and multi-device support

💡 Who Should Use Rasksaa




✅ Privacy-focused individuals

✅ Developers testing their network security

✅ Home users protecting personal devices

✅ Raspberry Pi or IoT hobbyists

✅ Students learning about real-world firewalls


If you care about privacy, control, and transparency more than automation or fancy dashboards —
Rasksaa is built for you.

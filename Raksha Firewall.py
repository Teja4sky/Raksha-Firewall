from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict, deque
from datetime import datetime
import os, csv, json, tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading

# ===== Configuration =====
SCAN_LIMIT = 10
SYN_LIMIT = 50
UDP_LIMIT = 200
TIME_WINDOW = 10
LOG_FILE = "firewall_log.txt"
CSV_FILE = "blocked_ips.csv"
WHITELIST_FILE = "whitelist.json"
# ==========================

scan_map = defaultdict(set)
syn_times = defaultdict(lambda: deque())
udp_times = defaultdict(lambda: deque())
pkt_times = defaultdict(lambda: deque())
blocked_ips = set()
whitelist = set()
running = True

# ===== GUI Setup =====
win = tk.Tk()
win.title("Smart Firewall - GUI")
win.geometry("850x550")
win.configure(bg="#0b0f16")

title = tk.Label(win, text="🚀 Smart Firewall (Port Scan + DDoS Protection)",
                 bg="#0b0f16", fg="#FEE715", font=("Arial", 15, "bold"))
title.pack(pady=10)

log_box = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg="#111",
                                    fg="#00FF00", font=("Consolas", 10))
log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def log(msg):
    """Write logs to GUI and file"""
    time_now = datetime.now().strftime("%H:%M:%S")
    line = f"[{time_now}] {msg}"
    log_box.insert(tk.END, line + "\n")
    log_box.yview(tk.END)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line)

def save_csv(ip, reason):
    """Save blocked IPs"""
    new_file = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["Time", "IP", "Reason"])
        w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip, reason])

def load_whitelist():
    """Load whitelist.json"""
    global whitelist
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE) as f:
            data = json.load(f)
            whitelist = set(data.get("whitelist", []))
    else:
        whitelist = {"127.0.0.1"}
        with open(WHITELIST_FILE, "w") as f:
            json.dump({"whitelist": list(whitelist)}, f, indent=2)
    log(f"[INFO] Whitelist loaded: {whitelist}")

def save_whitelist():
    with open(WHITELIST_FILE, "w") as f:
        json.dump({"whitelist": sorted(list(whitelist))}, f, indent=2)

def add_wl():
    ip = simpledialog.askstring("Add Whitelist", "Enter IP to whitelist:")
    if ip:
        whitelist.add(ip.strip())
        save_whitelist()
        log(f"[WL] Added {ip}")

def remove_wl():
    ip = simpledialog.askstring("Remove Whitelist", "Enter IP to remove:")
    if ip:
        whitelist.discard(ip.strip())
        save_whitelist()
        log(f"[WL] Removed {ip}")

def block(ip, reason):
    """Block attacker IP"""
    if ip in whitelist or ip in blocked_ips:
        return
    os.system(f"iptables -I INPUT -s {ip} -j DROP")
    blocked_ips.add(ip)
    save_csv(ip, reason)
    log(f"[BLOCKED] {ip} ({reason})")

def clear_logs():
    log_box.delete(1.0, tk.END)
    open(LOG_FILE, "w").close()
    log("[INFO] Logs cleared.")

def stop_fw():
    global running
    running = False
    log("[STOPPED] Firewall stopped.")
    messagebox.showinfo("Firewall", "Monitoring stopped.")

def unblock_all():
    os.system("iptables -F INPUT")
    blocked_ips.clear()
    log("[INFO] All IPs unblocked.")

def check_pkt(pkt):
    """Main detection logic"""
    if not running or not pkt.haslayer(IP):
        return
    ip = pkt[IP].src
    if ip in whitelist:
        return
    now = datetime.now()

    pkt_times[ip].append(now)
    while pkt_times[ip] and (now - pkt_times[ip][0]).total_seconds() > TIME_WINDOW:
        pkt_times[ip].popleft()
    if len(pkt_times[ip]) > 300:
        block(ip, "High Packet Rate"); return

    if pkt.haslayer(TCP):
        tcp = pkt[TCP]
        if tcp.flags == "S":
            scan_map[ip].add(tcp.dport)
            syn_times[ip].append(now)
            while syn_times[ip] and (now - syn_times[ip][0]).total_seconds() > TIME_WINDOW:
                syn_times[ip].popleft()
            if len(syn_times[ip]) > SYN_LIMIT:
                block(ip, "SYN Flood"); return
            if len(scan_map[ip]) > SCAN_LIMIT:
                block(ip, "Port Scan"); return

    if pkt.haslayer(UDP):
        udp_times[ip].append(now)
        while udp_times[ip] and (now - udp_times[ip][0]).total_seconds() > TIME_WINDOW:
            udp_times[ip].popleft()
        if len(udp_times[ip]) > UDP_LIMIT:
            block(ip, "UDP Flood"); return

def start_fw():
    log("🔥 Firewall started (Monitoring for scans & DDoS)...")
    sniff(filter="ip", prn=check_pkt, store=0)

# ===== Buttons =====
frame = tk.Frame(win, bg="#0b0f16")
frame.pack(pady=10)

buttons = [
    ("🧹 Clear Logs", clear_logs, "#FEE715", "#000"),
    ("⛔ Stop Firewall", stop_fw, "#FF4B4B", "#fff"),
    ("🔓 Unblock All", unblock_all, "#4BCFFA", "#000"),
    ("➕ Add WL", add_wl, "#8EE4AF", "#000"),
    ("➖ Remove WL", remove_wl, "#FFB4A2", "#000")
]

for i, (text, cmd, bg, fg) in enumerate(buttons):
    tk.Button(frame, text=text, command=cmd, bg=bg, fg=fg,
              font=("Arial", 11, "bold"), width=14).grid(row=0, column=i, padx=5)

# ===== Start Firewall =====
def start_gui():
    load_whitelist()
    t = threading.Thread(target=start_fw, daemon=True)
    t.start()
    win.mainloop()

if __name__ == "__main__":
    start_gui()

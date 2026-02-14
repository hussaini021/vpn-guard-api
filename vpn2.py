import requests
import json
import time
import os
import logging
from typing import Dict, List, Tuple, Optional

# ==========================================
# COLOR SYSTEM (ANSI)
# ==========================================

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ==========================================
# AUTHOR INFO
# ==========================================

AUTHOR = "Murtaza Hussaini"
UNIVERSITY = "University of Kabul"
FACULTY = "ISE Faculty"
YEAR = "3rd Year"
GITHUB = "https://github.com/hussaini021"

# ==========================================
# CONFIG
# ==========================================

IP_API = "https://api.ipify.org"
IP_INFO_API = "http://ip-api.com/json/"
IPV6_API = "https://api64.ipify.org"
HTTPS_TEST_URL = "https://example.com"
HEADER_TEST_URL = "https://httpbin.org/headers"

DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

logging.basicConfig(level=logging.ERROR)

session = requests.Session()

# ==========================================
# UI
# ==========================================

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def show_logo():
    clear()
    print(GREEN + BOLD + """
██╗   ██╗██████╗ ███╗   ██╗
██║   ██║██╔══██╗████╗  ██║
██║   ██║██████╔╝██╔██╗ ██║
╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║
 ╚████╔╝ ██║     ██║ ╚████║
  ╚═══╝  ╚═╝     ╚═╝  ╚═══╝
""" + RESET)

    print(CYAN + BOLD + "          VPN GUARD PRO v2.0\n" + RESET)
    print(GREEN + "===============================================" + RESET)
    print(WHITE + f" Developer : {AUTHOR}")
    print(f" University: {UNIVERSITY}")
    print(f" Faculty   : {FACULTY}")
    print(f" Academic  : {YEAR}")
    print(f" GitHub    : {GITHUB}")
    print(GREEN + "===============================================\n" + RESET)

def show_menu():
    print(GREEN + "1) Run Full VPN Security Test" + RESET)
    print(GREEN + "2) Quick IP Information" + RESET)
    print(GREEN + "3) View Test History" + RESET)
    print(GREEN + "4) Exit\n" + RESET)
    return input(YELLOW + "Select an option: " + RESET)

# ==========================================
# CORE FUNCTIONS
# ==========================================

def get_public_ip() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    try:
        ip = session.get(IP_API, timeout=5).text.strip()
        info = session.get(f"{IP_INFO_API}{ip}", timeout=5).json()
        return ip, info.get("country"), info.get("isp")
    except:
        return None, None, None

def ipv6_check() -> Tuple[bool, Optional[str]]:
    try:
        r = session.get(IPV6_API, timeout=5)
        if ":" in r.text:
            return True, r.text
        return False, None
    except:
        return False, None

def https_check() -> bool:
    try:
        r = session.get(HTTPS_TEST_URL, timeout=5)
        return r.status_code == 200
    except:
        return False

def header_check() -> Dict:
    try:
        r = session.get(HEADER_TEST_URL, timeout=5)
        return r.json().get("headers", {})
    except:
        return {}

def ip_stability_test(duration: int = 10, interval: int = 5) -> Tuple[bool, List[str]]:
    ips = []
    for _ in range(duration // interval):
        ip, _, _ = get_public_ip()
        ips.append(ip)
        time.sleep(interval)
    return len(set(ips)) == 1, ips

def calculate_risk_score(ip_changed: bool,
                         ipv6_leak: bool,
                         proxy_leak: bool) -> int:

    score = 100

    if not ip_changed:
        score -= 50
    if ipv6_leak:
        score -= 25
    if proxy_leak:
        score -= 25

    return max(score, 0)

# ==========================================
# MAIN TEST ENGINE
# ==========================================

def run_full_test():

    print(CYAN + "\nChecking initial IP..." + RESET)
    ip1, country1, isp1 = get_public_ip()

    input(YELLOW + "\nConnect your VPN now and press Enter to continue..." + RESET)

    print(CYAN + "\nChecking VPN IP..." + RESET)
    ip2, country2, isp2 = get_public_ip()

    ipv6_leak, _ = ipv6_check()
    headers = header_check()
    https_status = https_check()
    stable, ips_seen = ip_stability_test()

    proxy_headers = ["Via", "X-Forwarded-For", "X-Real-IP"]
    proxy_leak = any(h in headers for h in proxy_headers)

    ip_changed = ip1 != ip2
    score = calculate_risk_score(ip_changed, ipv6_leak, proxy_leak)

    result = {
        "ip_before": ip1,
        "ip_after": ip2,
        "country_before": country1,
        "country_after": country2,
        "ipv6_leak": ipv6_leak,
        "proxy_leak": proxy_leak,
        "https_status": https_status,
        "ip_stability": stable,
        "risk_score": score,
        "timestamp": time.ctime()
    }

    save_history(result)
    print_report(result)

def quick_ip_check():
    ip, country, isp = get_public_ip()
    print(CYAN + "\nQuick IP Information" + RESET)
    print("---------------------------------------")
    print(GREEN + f"IP      : {ip}")
    print(f"Country : {country}")
    print(f"ISP     : {isp}" + RESET)
    input("\nPress Enter to continue...")

def save_history(data: Dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

def view_history():
    clear()
    print(CYAN + BOLD + "VPN Test History\n" + RESET)
    if not os.path.exists(HISTORY_FILE):
        print(RED + "No history found." + RESET)
    else:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                print(GREEN + line.strip() + RESET)
    input("\nPress Enter to continue...")

def print_report(data: Dict):

    print(GREEN + "\n========================================" + RESET)
    print(CYAN + BOLD + "Advanced VPN Diagnostic Report" + RESET)
    print(GREEN + "========================================\n" + RESET)

    print(f"IP Before VPN : {data['ip_before']}")
    print(f"IP After VPN  : {data['ip_after']}")
    print(f"IP Stability  : {'Stable' if data['ip_stability'] else 'Unstable'}")
    print(f"IPv6 Leak     : {'Yes' if data['ipv6_leak'] else 'No'}")
    print(f"Proxy Headers : {'Detected' if data['proxy_leak'] else 'Not Detected'}")
    print(f"HTTPS Test    : {'Successful' if data['https_status'] else 'Failed'}")
    print(f"Risk Score    : {data['risk_score']}/100")

    print(GREEN + "\n========================================" + RESET)

    if data["risk_score"] > 70:
        print(GREEN + BOLD + "Overall Status: LOW RISK 🟢" + RESET)
    elif data["risk_score"] > 40:
        print(YELLOW + BOLD + "Overall Status: MEDIUM RISK ⚠" + RESET)
    else:
        print(RED + BOLD + "Overall Status: HIGH RISK 🔴" + RESET)

    input("\nPress Enter to continue...")
def run_analysis():
    return {
        "vpn": "NOT DETECTED",
        "risk": "LOW"
    }
# ==========================================
# ENTRY POINT
# ==========================================

def main():
    while True:
        show_logo()
        choice = show_menu()

        if choice == "1":
            run_full_test()
        elif choice == "2":
            quick_ip_check()
        elif choice == "3":
            view_history()
        elif choice == "4":
            print(GREEN + "\nExiting VPN Guard Pro...\n" + RESET)
            break
        else:
            print(RED + "Invalid option!" + RESET)
            time.sleep(1)

if __name__ == "__main__":

    main()

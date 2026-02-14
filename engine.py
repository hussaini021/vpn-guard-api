# engine.py
import requests

PROJECT_INFO = {
    "name": "VPN Guard Pro",
    "version": "1.0.0",
    "author": "Hussaini Murtaza",
    "role": "Cybersecurity & Python Developer",
    "github": "https://github.com/hussaini021",
    "engine": "Protected"
}

LOGO = r"""
██╗   ██╗██████╗ ███╗   ██╗
██║   ██║██╔══██╗████╗  ██║
██║   ██║██████╔╝██╔██╗ ██║
╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║
 ╚████╔╝ ██║     ██║ ╚████║
  ╚═══╝  ╚═╝     ╚═╝  ╚═══╝
VPN Guard Pro
"""

IP_API = "https://api.ipify.org"
IP_INFO_API = "http://ip-api.com/json/"
IPV6_API = "https://api64.ipify.org"
HEADER_TEST_URL = "https://httpbin.org/headers"
HTTPS_TEST_URL = "https://example.com"

session = requests.Session()

def get_public_ip():
    ip = session.get(IP_API, timeout=5).text.strip()
    info = session.get(f"{IP_INFO_API}{ip}", timeout=5).json()
    return ip, info.get("country"), info.get("isp")

def ipv6_check():
    try:
        r = session.get(IPV6_API, timeout=5)
        return ":" in r.text
    except:
        return False

def header_check():
    try:
        return session.get(HEADER_TEST_URL, timeout=5).json().get("headers", {})
    except:
        return {}

def https_check():
    try:
        return session.get(HTTPS_TEST_URL, timeout=5).status_code == 200
    except:
        return False

def run_analysis():
    ip, country, isp = get_public_ip()
    ipv6 = ipv6_check()
    headers = header_check()
    https_ok = https_check()

    proxy_headers = ["Via", "X-Forwarded-For", "X-Real-IP"]
    proxy_leak = any(h in headers for h in proxy_headers)

    risk = 100
    if ipv6:
        risk -= 30
    if proxy_leak:
        risk -= 30
    if not https_ok:
        risk -= 20

    return {
        "project": PROJECT_INFO,
        "logo": LOGO,
        "analysis": {
            "ip": ip,
            "country": country,
            "isp": isp,
            "ipv6_leak": ipv6,
            "proxy_leak": proxy_leak,
            "https_ok": https_ok,
            "risk_score": max(risk, 0)
        }
    }

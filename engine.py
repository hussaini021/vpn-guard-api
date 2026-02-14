# engine.py
import requests

PROJECT_INFO = {
    "name": "VPN Guard Pro",
    "version": "1.0.0",
    "author": "Hussaini Murtaza",
    "engine": "Protected"
}

LOGO = "VPN Guard Pro"

session = requests.Session()
session.headers.update({"User-Agent": "VPN-Guard/1.0"})

def safe_get(url, timeout=3):
    try:
        return session.get(url, timeout=timeout)
    except:
        return None

def run_analysis():
    result = {
        "project": PROJECT_INFO,
        "logo": LOGO,
        "analysis": {}
    }

    # IP
    r = safe_get("https://api.ipify.org")
    if not r:
        result["analysis"]["error"] = "IP service unavailable"
        return result

    ip = r.text.strip()
    result["analysis"]["ip"] = ip

    # HTTPS test
    https_test = safe_get("https://example.com")
    result["analysis"]["https_ok"] = bool(https_test)

    # VPN risk (simple + safe)
    risk = 100
    if not https_test:
        risk -= 20

    result["analysis"]["risk_score"] = risk
    return result        r = session.get(IPV6_API, timeout=5)
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

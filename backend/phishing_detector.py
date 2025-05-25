import requests
from bs4 import BeautifulSoup

def is_phishing(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        if "login" in url or "verify" in url or "secure" in url:
            return {"phishing": True, "reason": "Suspicious keywords in URL"}
        return {"phishing": False, "reason": "URL seems safe"}
    except Exception as e:
        return {"phishing": True, "reason": f"Error accessing URL: {e}"}

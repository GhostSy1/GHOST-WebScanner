import aiohttp
import asyncio
from bs4 import BeautifulSoup

class VulnScanner:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []

    async def check_sql_injection(self):
        # Basic error-based SQLi check
        payloads = ["'", "''", "\"", "';--", " OR 1=1"]
        async with aiohttp.ClientSession() as session:
            for payload in payloads:
                try:
                    async with session.get(f"{self.target}{payload}", timeout=10) as response:
                        text = await response.text()
                        errors = [
                            "you have an error in your sql syntax",
                            "warning: mysql_fetch_array()",
                            "unclosed quotation mark after the character string",
                            "postgresql query failed"
                        ]
                        if any(error in text.lower() for error in errors):
                            self.vulnerabilities.append({
                                "type": "SQL Injection",
                                "finding": f"Potential SQLi with payload: {payload}",
                                "severity": "Critical"
                            })
                            break
                except Exception:
                    pass

    async def check_xss(self):
        # Basic XSS check in URL parameters
        payload = "<script>alert('GHOST')</script>"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.target}?test={payload}", timeout=10) as response:
                    text = await response.text()
                    if payload in text:
                        self.vulnerabilities.append({
                            "type": "Cross-Site Scripting (XSS)",
                            "finding": "Reflected XSS in URL parameter",
                            "severity": "High"
                        })
            except Exception:
                pass

    async def run(self):
        await asyncio.gather(
            self.check_sql_injection(),
            self.check_xss()
        )
        return self.vulnerabilities

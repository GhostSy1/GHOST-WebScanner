import aiohttp
import asyncio
from core.payload_db import PAYLOADS
from core.evasion import EvasionEngine
class VulnScanner:
    def __init__(self, target, intensity="medium"):
        self.target = target
        self.intensity = intensity
        self.evasion = EvasionEngine()
        self.vulnerabilities = []
    async def scan_endpoint(self, session, vuln_type, payload):
        obfuscated = self.evasion.obfuscate_payload(payload, self.intensity)
        url = f"{self.target}/{obfuscated}"
        headers = self.evasion.get_custom_headers()
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                text = await response.text()
                if self.check_signature(vuln_type, text, response):
                    self.vulnerabilities.append({
                        "type": vuln_type,
                        "finding": f"Detected via payload: {payload}",
                        "severity": self.get_severity(vuln_type)
                    })
                    return True
        except Exception:
            pass
        return False
    def check_signature(self, vuln_type, body, response):
        body = body.lower()
        if vuln_type == "SQLI":
            return any(e in body for e in ["sql syntax", "mysql_fetch", "unclosed quotation", "postgresql query"])
        if vuln_type == "XSS":
            return "<script>alert(1)</script>" in body or "onerror=alert(1)" in body
        if vuln_type == "LFI":
            return "root:x:0:0:" in body or "[extensions]" in body
        if vuln_type == "RCE":
            return "uid=" in body and "gid=" in body
        if vuln_type == "SSTI":
            return "49" in body and "{{" in body
        return False
    def get_severity(self, vuln_type):
        mapping = {"SQLI": "Critical", "RCE": "Critical", "XSS": "High", "LFI": "High", "SSRF": "High"}
        return mapping.get(vuln_type, "Medium")
    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for v_type, payloads in PAYLOADS.items():
                for p in payloads:
                    tasks.append(self.scan_endpoint(session, v_type, p))
            await asyncio.gather(*tasks)
        return self.vulnerabilities

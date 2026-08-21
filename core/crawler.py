import aiohttp
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

class DeepWebCrawler:
    def __init__(self, target_url):
        self.target_url = target_url
        self.parsed_target = urlparse(target_url)
        self.domain = self.parsed_target.netloc
        self.visited_urls = set()
        self.discovered_endpoints = set()
        self.discovered_js = set()

    async def crawl(self, session, url):
        if url in self.visited_urls or len(self.visited_urls) > 50:
            return
        self.visited_urls.add(url)
        
        try:
            async with session.get(url, timeout=5, ssl=False, headers={"User-Agent": "Ghost-WebScanner-Crawler/2.6"}) as resp:
                if resp.status != 200:
                    return
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == self.domain:
                        self.discovered_endpoints.add(full_url)
                        
                for script in soup.find_all('script', src=True):
                    src = script['src']
                    full_js_url = urljoin(url, src)
                    if urlparse(full_js_url).netloc == self.domain or not urlparse(full_js_url).netloc:
                        self.discovered_js.add(full_js_url)
        except:
            pass

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await self.crawl(session, self.target_url)
            sub_tasks = [self.crawl(session, ep) for banner, ep in zip(range(10), list(self.discovered_endpoints)[:10])]
            if sub_tasks:
                import asyncio
                await asyncio.gather(*sub_tasks)
                
        return {
            "endpoints": list(self.discovered_endpoints),
            "js_files": list(self.discovered_js)
        }

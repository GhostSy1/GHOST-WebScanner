import socket
import aiohttp
import asyncio
from urllib.parse import urlparse

class ReconModule:
    def __init__(self, target):
        self.target = target
        self.domain = urlparse(target).netloc
        self.results = {
            "ip": None,
            "headers": {},
            "ports": []
        }

    async def get_ip(self):
        try:
            self.results["ip"] = socket.gethostbyname(self.domain)
        except Exception:
            self.results["ip"] = "Unknown"

    async def check_headers(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.target, timeout=10) as response:
                    self.results["headers"] = dict(response.headers)
            except Exception:
                pass

    async def scan_ports(self, ports=[80, 443, 8080, 8443]):
        # Simple async port scanner
        for port in ports:
            conn = asyncio.open_connection(self.domain, port)
            try:
                reader, writer = await asyncio.wait_for(conn, timeout=2)
                self.results["ports"].append(port)
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def run(self):
        await asyncio.gather(
            self.get_ip(),
            self.check_headers(),
            self.scan_ports()
        )
        return self.results

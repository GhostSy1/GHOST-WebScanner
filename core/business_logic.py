import aiohttp

class BusinessLogicAnalyzer:
    def __init__(self, target_url):
        self.target_url = target_url
        self.findings = []

    async def test_price_manipulation(self, session):
        test_endpoints = [
            f"{self.target_url}/api/cart/add",
            f"{self.target_url}/checkout",
            f"{self.target_url}/api/v1/order"
        ]
        for ep in test_endpoints:
            try:
                async with session.post(ep, json={"item_id": 1, "price": -10.00}, timeout=4, ssl=False) as resp:
                    if resp.status in [200, 201]:
                        self.findings.append({"flaw": "Price Manipulation / Negative Cart Value", "endpoint": ep})
            except:
                pass

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await self.test_price_manipulation(session)
        return self.findings

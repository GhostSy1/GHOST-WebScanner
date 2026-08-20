import random
import base64
import urllib.parse
class EvasionEngine:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
        ]
    def get_random_ua(self):
        return random.choice(self.user_agents)
    def obfuscate_payload(self, payload, level="medium"):
        if level == "low":
            return payload
        elif level == "medium":
            return urllib.parse.quote(payload)
        elif level == "high":
            encoded = urllib.parse.quote(payload)
            return urllib.parse.quote(encoded)
        return payload
    def get_custom_headers(self):
        return {
            "User-Agent": self.get_random_ua(),
            "Accept": "*/*",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Originating-IP": "127.0.0.1",
            "X-Remote-IP": "127.0.0.1",
            "X-Remote-Addr": "127.0.0.1"
        }

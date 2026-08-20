import unittest
from core.evasion import EvasionEngine
class TestEvasionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EvasionEngine()
    def test_user_agent_rotation(self):
        ua = self.engine.get_random_ua()
        self.assertIsInstance(ua, str)
        self.assertGreater(len(ua), 10)
    def test_obfuscation(self):
        payload = "<script>alert(1)</script>"
        obf = self.engine.obfuscate_payload(payload, level="medium")
        self.assertIn("%3C", obf)
if __name__ == "__main__":
    unittest.main()

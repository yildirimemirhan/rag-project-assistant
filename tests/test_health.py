import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from health import health_status  # noqa: E402


class FakeCollection:
    def count(self):
        return 109


class TestHealth(unittest.TestCase):
    def test_warming_when_state_empty(self):
        self.assertEqual(health_status({}, "m"), (503, {"status": "warming"}))

    def test_ok_when_initialised(self):
        code, body = health_status({"collection": FakeCollection()}, "openai/gpt-oss-120b")
        self.assertEqual(code, 200)
        self.assertEqual(body, {"status": "ok", "chunks": 109, "model": "openai/gpt-oss-120b"})


if __name__ == "__main__":
    unittest.main()

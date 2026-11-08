import unittest
import tempfile
from pathlib import Path
from sdcu_core.ui.auditor import UIAuditor

class TestUIAuditor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detects_ai_purple_gradient(self):
        component = self.root / "Hero.tsx"
        component.write_text('<div className="bg-gradient-to-r from-purple-600 to-pink-500">Slop</div>', encoding="utf-8")

        auditor = UIAuditor(str(self.root))
        findings = auditor.scan()

        found = [f for f in findings if f.sign == "AI Purple Gradient"]
        self.assertTrue(len(found) > 0)
        self.assertEqual(found[0].pass_name, "Color / Palette")

    def test_detects_emoji_badges(self):
        component = self.root / "Button.tsx"
        component.write_text('<button className="btn">✨ New Feature</button>', encoding="utf-8")

        auditor = UIAuditor(str(self.root))
        findings = auditor.scan()

        found = [f for f in findings if f.sign == "Emoji Badge Spam"]
        self.assertTrue(len(found) > 0)

if __name__ == "__main__":
    unittest.main()

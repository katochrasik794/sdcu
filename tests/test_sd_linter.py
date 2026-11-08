import unittest
import tempfile
import os
from pathlib import Path
from sdcu_core.sd.linter import SystemDesignLinter

class TestSystemDesignLinter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detects_frontend_api_key_leak(self):
        vuln_file = self.root / "app.ts"
        vuln_file.write_text("export const apiKey = process.env.NEXT_PUBLIC_STRIPE_SECRET_KEY;", encoding="utf-8")
        
        linter = SystemDesignLinter(str(self.root))
        findings = linter.scan()

        found = [f for f in findings if f.checkpoint_id == "01"]
        self.assertTrue(len(found) > 0)
        self.assertEqual(found[0].severity, "CRITICAL")

    def test_detects_sql_injection(self):
        vuln_file = self.root / "db.ts"
        vuln_file.write_text("const q = `SELECT * FROM users WHERE email = '${email}'`;", encoding="utf-8")
        
        linter = SystemDesignLinter(str(self.root))
        findings = linter.scan()

        found = [f for f in findings if f.checkpoint_id == "03"]
        self.assertTrue(len(found) > 0)
        self.assertEqual(found[0].severity, "HIGH")

    def test_detects_potential_n_plus_one(self):
        vuln_file = self.root / "service.ts"
        vuln_file.write_text("users.forEach(async (u) => { await db.posts.findMany({ userId: u.id }); });", encoding="utf-8")
        
        linter = SystemDesignLinter(str(self.root))
        findings = linter.scan()

        found = [f for f in findings if f.checkpoint_id == "12"]
        self.assertTrue(len(found) > 0)

if __name__ == "__main__":
    unittest.main()


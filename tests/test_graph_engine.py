import unittest
import tempfile
from pathlib import Path
from sdcu_core.graph.engine import ContextGraphEngine

class TestContextGraphEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_build_and_query_graph(self):
        # Create sample files
        auth_file = self.root / "auth.py"
        auth_file.write_text("def login(): pass\ndef verify(): pass", encoding="utf-8")

        api_file = self.root / "api.py"
        api_file.write_text("from auth import login\ndef handle_request(): pass", encoding="utf-8")

        engine = ContextGraphEngine(str(self.root))
        result = engine.build()

        self.assertTrue(result["node_count"] > 0)
        self.assertTrue(result["edge_count"] > 0)

        # Test query
        q_res = engine.query("login authentication")
        self.assertTrue(len(q_res["matched_keywords"]) > 0)

        # Test path
        path = engine.shortest_path("api.py", "auth")
        self.assertIsNotNone(path)

if __name__ == "__main__":
    unittest.main()


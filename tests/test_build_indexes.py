import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from guides.tools.build_indexes import main

class BuildIndexesTests(unittest.TestCase):
    def test_build_indexes_creates_files(self):
        with TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            summaries_dir = tmp_root / "public" / "summaries"
            summaries_dir.mkdir(parents=True)
            
            index_dir = tmp_root / "public" / "index"
            
            (summaries_dir / "test1.md").write_text("""---
title: Test 1
tools: [ToolA]
patterns: [PatternX]
concepts: [Concept1]
entities: [Entity1]
topics: [Topic1]
---
# Test 1""", encoding="utf-8")
            
            (summaries_dir / "test2.md").write_text("""---
title: Test 2
tools: [ToolA, ToolB]
patterns: [PatternY]
---
# Test 2""", encoding="utf-8")

            argv = [
                "--summaries", str(summaries_dir),
                "--index-dir", str(index_dir)
            ]
            
            rc = main(argv)
            self.assertEqual(rc, 0)
            
            # Verify files exist
            self.assertTrue((index_dir / "tools.md").exists())
            self.assertTrue((index_dir / "patterns.md").exists())
            self.assertTrue((index_dir / "concepts.md").exists())
            self.assertTrue((index_dir / "entities.md").exists())
            self.assertTrue((index_dir / "topics.md").exists())
            
            # Verify content
            tools_content = (index_dir / "tools.md").read_text(encoding="utf-8")
            self.assertIn("ToolA", tools_content)
            self.assertIn("ToolB", tools_content)
            self.assertIn("(2 mentions)", tools_content) # ToolA has 2 mentions
            self.assertIn("(1 mentions)", tools_content) # ToolB has 1 mention

if __name__ == "__main__":
    unittest.main()

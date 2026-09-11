"""Exercise draft visibility, dated publication, and snapshot preservation in isolation."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class JournalPublishing(unittest.TestCase):
    def test_drafts_and_snapshots(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "site"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            def run(*args, success=True):
                result = subprocess.run([sys.executable, str(root / "scripts/build_journal.py"), *args],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode == 0, success, result.stderr + result.stdout)
                return result
            snapshot = root / "journal/snapshots/2026-09-10/music-kitchen-product.md"
            original = snapshot.read_bytes()
            run("build")
            generated = [root / "index.html", root / "journal/feed.xml"] + list((root / "artifacts").glob("*.html"))
            hashes = {p: hashlib.sha256(p.read_bytes()).digest() for p in generated}
            run("build")
            self.assertEqual(hashes, {p: hashlib.sha256(p.read_bytes()).digest() for p in generated})
            run("new", "2026-09-09", "--title", "Draft must remain private")
            run("build")
            self.assertNotIn("Draft must remain private", (root / "journal/index.html").read_text())
            self.assertFalse((root / "journal/2026-09-09.html").exists())
            run("publish", "2026-09-09", success=False)
            self.assertFalse((root / "journal/snapshots/2026-09-09").exists())
            catalog = root / "journal/content.json"
            data = json.loads(catalog.read_text())
            entry = data["entries"][-1]
            for key in ["summary", "stage", "focus", "next_step"]:
                entry[key] = "A completed, evidence-based update."
            catalog.write_text(json.dumps(data))
            (root / "journal/entries/2026-09-09.md").write_text("# Draft must remain private\n\nActual completed work.\n")
            source = root / "research/MUSIC-KITCHEN-PRODUCT.md"
            source.write_text(source.read_text() + "\nNew direction only in the working artifact.\n")
            run("publish", "2026-09-09")
            self.assertEqual(snapshot.read_bytes(), original)
            self.assertIn("New direction only", (root / "artifacts/music-kitchen-product.html").read_text())
            self.assertNotIn("New direction only", (snapshot.with_suffix(".html")).read_text())
            self.assertIn("New direction only", (root / "journal/snapshots/2026-09-09/music-kitchen-product.md").read_text())
            self.assertIn('href="2026-09-09.html"', (root / "journal/2026-09-10.html").read_text())
            self.assertIn('href="2026-09-10.html"', (root / "journal/2026-09-09.html").read_text())
            run("publish", "2026-09-09", success=False)


if __name__ == "__main__":
    unittest.main()

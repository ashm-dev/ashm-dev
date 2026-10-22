import subprocess
import tempfile
import unittest
from pathlib import Path

from update_readme import update


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.author = self.root / "author"
        self.checkout = self.root / "checkout"
        self.attempts = self.root / "attempts"
        self.git(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.git(self.root, "clone", str(self.remote), str(self.author))
        self.git(self.author, "config", "user.name", "Test Author")
        self.git(self.author, "config", "user.email", "author@example.com")
        (self.author / "scripts").mkdir()
        (self.author / "source.txt").write_text("old\n")
        self.generator()
        for name in ("README.md", "README.ru.md", "contributions.json"):
            (self.author / name).write_text("old\n")
        self.commit("Initial profile")
        self.git(self.root, "clone", str(self.remote), str(self.checkout))
        self.original = self.git(self.checkout, "rev-parse", "HEAD")
        (self.checkout / "notes.txt").write_text("Keep this file\n")
        (self.checkout / "README.md").write_text("Local draft\n")

    def git(self, cwd, *args):
        return subprocess.check_output(
            ["git", "-C", str(cwd), *args], text=True, stderr=subprocess.PIPE,
        ).strip()

    def commit(self, message):
        self.git(self.author, "add", ".")
        self.git(self.author, "commit", "-m", message)
        self.git(self.author, "push", "origin", "main")

    def generator(self, before="", after=""):
        (self.author / "scripts/build_readme.py").write_text(
            "from pathlib import Path\nimport subprocess\n"
            "root = Path(__file__).resolve().parents[1]\n"
            f"with Path({str(self.attempts)!r}).open('a') as log: log.write('attempt\\n')\n"
            + before
            + "value = (root / 'source.txt').read_text()\n"
            + after
            + "for name in ('README.md', 'README.ru.md', 'contributions.json'):\n"
            "    (root / name).write_text(value)\n"
        )

    def assert_checkout_preserved(self):
        self.assertEqual(self.git(self.checkout, "rev-parse", "HEAD"), self.original)
        self.assertEqual((self.checkout / "notes.txt").read_text(), "Keep this file\n")
        self.assertEqual((self.checkout / "README.md").read_text(), "Local draft\n")
        self.assertEqual(self.git(self.checkout, "worktree", "list", "--porcelain").count("worktree "), 1)

    def assert_published(self, value):
        for name in ("README.md", "README.ru.md", "contributions.json"):
            self.assertEqual(self.git(self.remote, "show", f"main:{name}"), value)
        self.assert_checkout_preserved()

    def test_stale_checkout_publishes_from_current_main(self):
        (self.author / "source.txt").write_text("fresh\n")
        (self.author / "unrelated.txt").write_text("Keep upstream changes\n")
        self.commit("Update source")
        parent = self.git(self.remote, "rev-parse", "main")
        update(self.checkout, delay=0)
        self.assert_published("fresh")
        self.assertEqual(self.git(self.remote, "rev-parse", "main^"), parent)
        self.assertEqual(self.git(self.remote, "show", "main:unrelated.txt"), "Keep upstream changes")

    def test_concurrent_push_regenerates_from_new_main(self):
        self.concurrent_push("pending\n")

    def test_concurrent_push_is_detected_even_without_local_changes(self):
        self.concurrent_push("old\n")

    def concurrent_push(self, source):
        (self.author / "source.txt").write_text(source)
        marker = self.root / "concurrent"
        self.generator(after=(
            f"marker = Path({str(marker)!r})\n"
            "if not marker.exists():\n"
            "    marker.touch()\n"
            f"    peer = Path({str(self.author)!r})\n"
            "    (peer / 'source.txt').write_text('concurrent\\n')\n"
            "    for args in [('add', 'source.txt'), ('commit', '-m', 'Concurrent update'), ('push', 'origin', 'main')]:\n"
            "        subprocess.run(['git', '-C', str(peer), *args], check=True)\n"
        ))
        self.commit("Add concurrent publisher")
        update(self.checkout, delay=0)
        self.assert_published("concurrent")
        self.assertEqual(self.attempts.read_text().splitlines(), ["attempt", "attempt"])

    def test_transient_generation_failure_is_retried(self):
        marker = self.root / "failed-once"
        self.generator(before=(
            f"marker = Path({str(marker)!r})\n"
            "if not marker.exists():\n"
            "    marker.touch()\n"
            "    (root / 'README.md').write_text('partial')\n"
            "    raise RuntimeError('Temporary source failure')\n"
        ))
        (self.author / "source.txt").write_text("recovered\n")
        self.commit("Add transient failure")
        update(self.checkout, delay=0)
        self.assert_published("recovered")
        self.assertEqual(self.attempts.read_text().splitlines(), ["attempt", "attempt"])

    def test_permanent_failure_preserves_published_data(self):
        self.generator(before="(root / 'README.md').write_text('partial')\nraise RuntimeError('Source unavailable')\n")
        self.commit("Add unavailable source")
        parent = self.git(self.remote, "rev-parse", "main")
        with self.assertRaises(subprocess.CalledProcessError):
            update(self.checkout, delay=0)
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), parent)
        self.assertEqual(self.attempts.read_text().splitlines(), ["attempt"] * 3)
        self.assert_published("old")

    def test_unchanged_data_does_not_create_a_commit(self):
        update(self.checkout, delay=0)
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), self.original)
        self.assert_published("old")

    def test_transient_push_failure_is_retried(self):
        marker = self.root / "rejected-once"
        hook = self.remote / "hooks/pre-receive"
        (self.author / "source.txt").write_text("fresh\n")
        self.commit("Update source")
        hook.write_text(f'#!/bin/sh\nif [ ! -f "{marker}" ]; then touch "{marker}"; exit 1; fi\n')
        hook.chmod(0o755)
        update(self.checkout, delay=0)
        self.assert_published("fresh")
        self.assertEqual(self.attempts.read_text().splitlines(), ["attempt", "attempt"])

    def test_permanent_push_failure_is_reported(self):
        (self.author / "source.txt").write_text("fresh\n")
        self.commit("Update source")
        parent = self.git(self.remote, "rev-parse", "main")
        hook = self.remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        with self.assertRaises(subprocess.CalledProcessError):
            update(self.checkout, delay=0)
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), parent)
        self.assertEqual(self.attempts.read_text().splitlines(), ["attempt"] * 3)
        self.assert_published("old")


if __name__ == "__main__":
    unittest.main()

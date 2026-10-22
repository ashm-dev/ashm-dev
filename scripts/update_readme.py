"""Regenerate and publish the profile from current main with bounded retries."""
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def git(repository, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repository), *args], check=check,
        text=True, stdout=subprocess.PIPE, timeout=60,
    )


def update(repository, delay=10):
    for attempt in range(1, 4):
        try:
            git(repository, "fetch", "origin", "main")
            with tempfile.TemporaryDirectory(prefix="profile-update-") as directory:
                git(repository, "worktree", "add", "--detach", directory, "FETCH_HEAD")
                try:
                    subprocess.run(
                        [sys.executable, "-B", "scripts/build_readme.py"],
                        cwd=directory, check=True, timeout=300,
                    )
                    git(directory, "add", "README.md", "README.ru.md", "contributions.json")
                    diff = git(directory, "diff", "--cached", "--quiet", check=False)
                    if diff.returncode == 1:
                        git(directory, "-c", "user.name=github-actions[bot]", "-c",
                            "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                            "commit", "-m", "chore(readme): refresh contributions")
                    else:
                        diff.check_returncode()
                    commit = git(directory, "rev-parse", "HEAD").stdout.strip()
                    git(repository, "push", "origin", f"{commit}:refs/heads/main")
                    print(f"Profile published at {commit}; changed: {diff.returncode == 1}")
                    return
                finally:
                    git(repository, "worktree", "remove", "--force", directory)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            if attempt == 3:
                raise
            print(f"Profile update attempt {attempt} failed: {error}; retrying.", file=sys.stderr)
            time.sleep(delay * attempt)


if __name__ == "__main__":
    update(Path(__file__).resolve().parents[1])

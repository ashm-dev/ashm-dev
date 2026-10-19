"""Collect public authored GitHub contributions and SQLAlchemy main commits."""
import json
import os
import subprocess
from collections import defaultdict

from backports import is_backport

GITHUB_USER = "ashm-dev"
SKIP_OWNERS = ("ashm-dev/", "kartochka/")


def gh_api(*args, repo="ashm-dev/ashm-dev"):
    return json.loads(subprocess.check_output(
        ["gh", "api", *args], text=True, timeout=120,
        env={**os.environ, "GH_REPO": repo},
    ))


def authored(api, kind, extra):
    query = '''query($endCursor: String) {
      user(login: "ashm-dev") {
        KIND(first: 100, after: $endCursor) {
          nodes { number title url state repository { nameWithOwner isPrivate } EXTRA }
          pageInfo { hasNextPage endCursor }
        }
      }
    }'''.replace("KIND", kind).replace("EXTRA", extra)
    pages = api("graphql", "--paginate", "--slurp", "-f", "query=" + query)
    rows = [row for page in pages for row in page["data"]["user"][kind]["nodes"]
            if not row["repository"]["isPrivate"]
            and not row["repository"]["nameWithOwner"].startswith(SKIP_OWNERS)]
    return sorted(rows, key=lambda row: row["number"], reverse=True)


def github_projects(api=gh_api):
    projects = defaultdict(lambda: defaultdict(list))
    prs = authored(api, "pullRequests", "baseRefName headRefName body")
    for pr in prs:
        repo = pr["repository"]["nameWithOwner"]
        if pr["state"] not in ("OPEN", "MERGED") or is_backport(pr, prs):
            continue
        if repo == "sqlalchemy/sqlalchemy" and pr["state"] == "MERGED":
            continue
        projects[repo]["Pull requests"].append((
            "open" if pr["state"] == "OPEN" else "done", f"#{pr['number']}", pr["url"], pr["title"],
        ))
    for issue in authored(api, "issues", "stateReason"):
        if issue["state"] != "OPEN" and issue["stateReason"] != "COMPLETED":
            continue
        projects[issue["repository"]["nameWithOwner"]]["Issues"].append((
            "open" if issue["state"] == "OPEN" else "done", f"#{issue['number']}", issue["url"], issue["title"],
        ))
    repo = "sqlalchemy/sqlalchemy"
    pages = api("--paginate", "--slurp",
                f"repos/{repo}/commits?sha=main&author={GITHUB_USER}&per_page=100", repo=repo)
    for page in pages:
        for commit in page:
            if (commit.get("author") or {}).get("login") == GITHUB_USER:
                projects[repo]["Commits"].append((
                    "done", commit["sha"][:10], commit["html_url"], commit["commit"]["message"].splitlines()[0],
                ))
    return projects

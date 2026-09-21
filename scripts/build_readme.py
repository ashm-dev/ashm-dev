#!/usr/bin/env python3
"""Rewrite the contributions in README.md and docs/_data from GitHub, patchwork and Bugzilla."""
import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

GITHUB_USER = "ashm-dev"
SOURCEWARE_EMAIL = "ashamil435@gmail.com"
SKIP_OWNERS = ("ashm-dev/", "kartochka/")
ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DATA = ROOT / "docs" / "_data" / "contributions.json"
START = "<!-- contributions:start -->"
END = "<!-- contributions:end -->"

NOUN = {"Pull requests": "PRs", "Issues": "issues", "Patches": "patches", "Bugs": "bugs"}
ICON = {"done": "✅", "open": "🟡"}
ISSUE_STATE = {"open": "open", "closed": "done"}


def gh_search(kind):
    cmd = ["gh", "search", kind, "--author", GITHUB_USER, "--limit", "1000",
           "--json", "repository,number,title,state,url"]
    rows = json.loads(subprocess.check_output(cmd, text=True))
    return [r for r in rows if not r["repository"]["nameWithOwner"].startswith(SKIP_OWNERS)]


def landed_titles(repo):
    cmd = ["gh", "api", "--paginate", f"repos/{repo}/commits?author={GITHUB_USER}&per_page=100",
           "--jq", '.[].commit.message | split("\\n")[0]']
    return {normalize(line) for line in subprocess.check_output(cmd, text=True).splitlines()}


def normalize(title):
    return re.sub(r"\s*\(#\d+\)\s*$", "", title).strip().casefold()


def get_json(url, **params):
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=60) as resp:
        return json.load(resp)


def github_projects():
    projects = defaultdict(lambda: {"Pull requests": [], "Issues": []})
    prs = gh_search("prs")
    # Gerrit-based projects (SQLAlchemy) close the GitHub PR and land the same commit by hand.
    landed = {repo: landed_titles(repo)
              for repo in {pr["repository"]["nameWithOwner"] for pr in prs if pr["state"] == "closed"}}
    for pr in prs:
        repo = pr["repository"]["nameWithOwner"]
        if pr["state"] == "closed" and normalize(pr["title"]) not in landed[repo]:
            continue
        projects[repo]["Pull requests"].append(
            ("open" if pr["state"] == "open" else "done", f"#{pr['number']}", pr["url"], pr["title"]))
    for issue in gh_search("issues"):
        projects[issue["repository"]["nameWithOwner"]]["Issues"].append(
            (ISSUE_STATE[issue["state"]], f"#{issue['number']}", issue["url"], issue["title"]))
    return projects


def glibc_project():
    # ponytail: single page of 250 patches, add pagination when the series count passes that
    patches = get_json("https://patchwork.sourceware.org/api/1.2/patches/",
                       project="glibc", submitter=SOURCEWARE_EMAIL, per_page=250)
    bugs = get_json("https://sourceware.org/bugzilla/rest/bug", product="glibc",
                    reporter=SOURCEWARE_EMAIL, limit=0,
                    include_fields="id,summary,status")["bugs"]
    return {
        "Patches": [("done" if p["state"] == "committed" else "open", f"patch {p['id']}",
                     f"https://patchwork.sourceware.org/patch/{p['id']}/", p["name"])
                    for p in patches if p["state"] not in ("superseded", "dropped", "rejected")],
        "Bugs": [("done" if b["status"] == "RESOLVED" else "open", f"BZ #{b['id']}",
                  f"https://sourceware.org/bugzilla/show_bug.cgi?id={b['id']}", b["summary"])
                 for b in bugs],
    }


def landed(sections):
    first = next(iter(sections.values()))
    return sum(1 for state, *_ in first if state == "done")


def summary(sections):
    (first_name, _), (second_name, second) = sections.items()
    verb = "committed" if first_name == "Patches" else "merged"
    return f"{landed(sections)} {verb} {NOUN[first_name]} · {len(second)} {NOUN[second_name]}"


def number(item):
    return int("".join(ch for ch in item[1] if ch.isdigit()))


def ordered(projects):
    nonempty = {name: sections for name, sections in projects.items() if any(sections.values())}
    return sorted(nonempty.items(), key=lambda kv: landed(kv[1]), reverse=True)


def escape(text):
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        parts[i] = html.escape(parts[i], quote=False).replace("_", "\\_").replace("*", "\\*")
    return "`".join(parts)


def render_project(name, sections):
    lines = ["<details>", f"<summary><b>{name}</b> — {summary(sections)}</summary>", ""]
    for title, items in sections.items():
        if not items:
            continue
        lines += [f"#### {title}", ""]
        lines += [f"- {ICON[state]} [{label}]({url}) {escape(text)}"
                  for state, label, url, text in sorted(items, key=number, reverse=True)]
        lines.append("")
    lines.append("</details>")
    return "\n".join(lines)


def render_all(projects):
    return "\n\n".join(render_project(name, sections) for name, sections in ordered(projects))


def to_data(projects):
    return [{
        "name": name,
        "summary": summary(sections),
        "sections": [{
            "title": title,
            "items": [{"state": state, "label": label, "url": url, "title": text}
                      for state, label, url, text in sorted(items, key=number, reverse=True)],
        } for title, items in sections.items()],
    } for name, sections in ordered(projects)]


def splice(text, body):
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{START}\n{body}\n{END}{tail}"


def main():
    projects = github_projects()
    projects["glibc (sourceware)"] = glibc_project()
    README.write_text(splice(README.read_text(), render_all(projects)))
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(to_data(projects), ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()

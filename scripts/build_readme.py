#!/usr/bin/env python3
"""Rewrite the contributions section of README.md from GitHub, patchwork and Bugzilla."""
import html
import json
import subprocess
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

GITHUB_USER = "ashm-dev"
SOURCEWARE_EMAIL = "ashamil435@gmail.com"
SKIP_OWNERS = ("ashm-dev/", "kartochka/")
README = Path(__file__).resolve().parent.parent / "README.md"
START = "<!-- contributions:start -->"
END = "<!-- contributions:end -->"

NOUN = {"Pull requests": "PRs", "Issues": "issues", "Patches": "patches", "Bugs": "bugs"}
PR_ICON = {"merged": "✅", "open": "🟡"}
ISSUE_ICON = {"open": "🟡", "closed": "✅"}


def gh_search(kind):
    cmd = ["gh", "search", kind, "--author", GITHUB_USER, "--limit", "1000",
           "--json", "repository,number,title,state,url"]
    rows = json.loads(subprocess.check_output(cmd, text=True))
    return [r for r in rows if not r["repository"]["nameWithOwner"].startswith(SKIP_OWNERS)]


def get_json(url, **params):
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=60) as resp:
        return json.load(resp)


def github_projects():
    projects = defaultdict(lambda: {"Pull requests": [], "Issues": []})
    for pr in gh_search("prs"):
        if pr["state"] == "closed":
            continue
        projects[pr["repository"]["nameWithOwner"]]["Pull requests"].append(
            (PR_ICON[pr["state"]], f"#{pr['number']}", pr["url"], pr["title"]))
    for issue in gh_search("issues"):
        projects[issue["repository"]["nameWithOwner"]]["Issues"].append(
            (ISSUE_ICON[issue["state"]], f"#{issue['number']}", issue["url"], issue["title"]))
    return projects


def glibc_project():
    # ponytail: single page of 250 patches, add pagination when the series count passes that
    patches = get_json("https://patchwork.sourceware.org/api/1.2/patches/",
                       project="glibc", submitter=SOURCEWARE_EMAIL, per_page=250)
    bugs = get_json("https://sourceware.org/bugzilla/rest/bug", product="glibc",
                    reporter=SOURCEWARE_EMAIL, limit=0,
                    include_fields="id,summary,status")["bugs"]
    return {
        "Patches": [("✅" if p["state"] == "committed" else "🟡", f"patch {p['id']}",
                     f"https://patchwork.sourceware.org/patch/{p['id']}/", p["name"])
                    for p in patches if p["state"] not in ("superseded", "dropped", "rejected")],
        "Bugs": [("✅" if b["status"] == "RESOLVED" else "🟡", f"BZ #{b['id']}",
                      f"https://sourceware.org/bugzilla/show_bug.cgi?id={b['id']}", b["summary"])
                     for b in bugs],
    }


def landed(sections):
    first = next(iter(sections.values()))
    return sum(1 for icon, *_ in first if icon == "✅")


def escape(text):
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        parts[i] = html.escape(parts[i], quote=False).replace("_", "\\_").replace("*", "\\*")
    return "`".join(parts)


def number(item):
    return int("".join(ch for ch in item[1] if ch.isdigit()))


def render_project(name, sections):
    (first_name, first), (second_name, second) = sections.items()
    verb = "committed" if first_name == "Patches" else "merged"
    summary = f"{landed(sections)} {verb} {NOUN[first_name]} · {len(second)} {NOUN[second_name]}"
    lines = ["<details>", f"<summary><b>{name}</b> — {summary}</summary>", ""]
    for title, items in sections.items():
        if not items:
            continue
        lines += [f"#### {title}", ""]
        lines += [f"- {icon} [{label}]({url}) {escape(text)}"
                  for icon, label, url, text in sorted(items, key=number, reverse=True)]
        lines.append("")
    lines.append("</details>")
    return "\n".join(lines)


def render_all(projects):
    nonempty = {name: sections for name, sections in projects.items() if any(sections.values())}
    ordered = sorted(nonempty.items(), key=lambda kv: landed(kv[1]), reverse=True)
    return "\n\n".join(render_project(name, sections) for name, sections in ordered)


def splice(text, body):
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{START}\n{body}\n{END}{tail}"


def main():
    projects = github_projects()
    projects["glibc (sourceware)"] = glibc_project()
    README.write_text(splice(README.read_text(), render_all(projects)))


if __name__ == "__main__":
    main()

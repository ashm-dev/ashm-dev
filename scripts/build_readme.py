#!/usr/bin/env python3
"""Render profile READMEs and site data from accepted upstream contributions."""
import html
import json
from pathlib import Path

from github_contributions import github_projects
from sourceware_contributions import glibc_project

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- contributions:start -->"
END = "<!-- contributions:end -->"
ORDER = ("Commits", "Pull requests", "Patches", "Issues", "Bugs")
ICON = {"done": "🟢", "open": "🟡"}
LABELS = {
    "en": {"Pull requests": "PR", "Issues": "Issues", "Patches": "Patches", "Bugs": "Bug reports", "Commits": "Commits"},
    "ru": {"Pull requests": "PR", "Issues": "Issues", "Patches": "Патчи", "Bugs": "Баги", "Commits": "Коммиты"},
}
DONE = {
    "en": {"Pull requests": "merged", "Issues": "completed", "Patches": "committed", "Bugs": "fixed", "Commits": "committed"},
    "ru": {"Pull requests": "принято", "Issues": "выполнено", "Patches": "принято", "Bugs": "исправлено", "Commits": "принято"},
}


def sections_in_order(sections):
    return [(title, sections[title]) for title in ORDER if sections.get(title)]


def summary(sections, lang="en"):
    parts = []
    for title, items in sections_in_order(sections):
        counts = []
        for state, label in (("done", DONE[lang][title]), ("open", "открыто" if lang == "ru" else "open")):
            count = sum(item[0] == state for item in items)
            if count:
                counts.append(f"{count} {label}")
        parts.append(f"{LABELS[lang][title]}: {', '.join(counts)}")
    return " · ".join(parts)


def ordered(projects):
    def rank(project):
        name, sections = project
        done = sum(item[0] == "done" for title, items in sections.items()
                   if title in ("Pull requests", "Patches", "Commits") for item in items)
        return -done, name
    return sorted(((name, sections) for name, sections in projects.items() if any(sections.values())), key=rank)


def ordered_items(title, items):
    if title == "Commits":
        return items
    return sorted(items, key=lambda item: int("".join(ch for ch in item[1] if ch.isdigit())), reverse=True)


def escape(text):
    parts = text.split("`")
    for index in range(0, len(parts), 2):
        parts[index] = html.escape(parts[index], quote=False).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]")
    return "`".join(parts).rstrip()


def render_project(name, sections, lang):
    lines = ["<details>", f"<summary><b>{html.escape(name)}</b><br>{html.escape(summary(sections, lang))}</summary>", ""]
    for title, items in sections_in_order(sections):
        lines += [f"#### {LABELS[lang][title]}", ""]
        lines += [f"- {ICON[state]} [{label}]({url}) {escape(text)}"
                  for state, label, url, text in ordered_items(title, items)]
        lines.append("")
    return "\n".join([*lines, "</details>"])


def render_all(projects, lang="en"):
    return "\n\n".join(render_project(name, sections, lang) for name, sections in ordered(projects))


def to_data(projects):
    return [{
        "name": name, "summary": summary(sections),
        "sections": [{
            "title": title,
            "items": [{"state": state, "label": label, "url": url, "title": text}
                      for state, label, url, text in ordered_items(title, items)],
        } for title, items in sections_in_order(sections)],
    } for name, sections in ordered(projects)]


def splice(text, body):
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{START}\n{body}\n{END}{tail}"


def main():
    projects = github_projects()
    projects["glibc"] = glibc_project()
    files = {ROOT / "contributions.json": json.dumps(to_data(projects), ensure_ascii=False, indent=1) + "\n"}
    for lang, filename in (("en", "README.md"), ("ru", "README.ru.md")):
        path = ROOT / filename
        files[path] = splice(path.read_text(), render_all(projects, lang))
    for path, text in files.items():
        path.write_text(text)


if __name__ == "__main__":
    main()

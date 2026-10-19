"""Select the latest revision before applying Patchwork state exclusions."""
import re

EXCLUDED_STATES = {"superseded", "dropped", "rejected", "not-applicable"}


def identity(patch):
    name = patch["name"].strip()
    prefix = re.match(r"^\[([^]]+)\]\s*", name)
    part = ""
    if prefix and re.fullmatch(r"(?:PATCH|RFC|v\d+|\d+/\d+|[\s,])+", prefix[1], re.I):
        number = re.search(r"(\d+)/\d+", prefix[1])
        part = number[1] if number else ""
        name = name[prefix.end():]
    return part, " ".join(name.casefold().split())


def revision(patch):
    versions = [series["version"] for series in patch["series"]]
    match = re.match(r"^\[[^]]*\bv(\d+)\b", patch["name"], re.I)
    if match:
        versions.append(int(match[1]))
    return max(versions, default=1), patch["date"], patch["id"]


def latest_patches(patches):
    latest = {}
    for patch in patches:
        key = identity(patch)
        if key not in latest or revision(patch) > revision(latest[key]):
            latest[key] = patch
    return sorted((patch for patch in latest.values() if patch["state"] not in EXCLUDED_STATES),
                  key=lambda patch: patch["id"], reverse=True)

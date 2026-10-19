"""Recognize repeated changes without excluding original release-branch fixes."""
import re

VERSION_PREFIX = re.compile(r"^\[v?\d+(?:\.\d+)+\]\s*", re.I)


def subject(title):
    title = VERSION_PREFIX.sub("", title)
    return re.sub(r"\s*\((?:gh[- ]?)?#?\d+\)\s*$", "", title, flags=re.I).strip().casefold()


def is_backport(pr, peers):
    body = re.sub(r"<!--.*?-->", "", pr["body"], flags=re.S)
    if re.search(r"cherry[ -]picked from commit\s+[0-9a-f]+", body, re.I):
        return True
    if re.search(r"^\s*(?:manual\s+)?backport of\s+(?:#|https://github\.com/)", body, re.I | re.M):
        return True
    if not VERSION_PREFIX.match(pr["title"]):
        return False
    if re.search(r"\((?:gh[- ]?)?#?\d+\)\s*$", pr["title"], re.I):
        return True
    return any(
        other["number"] != pr["number"]
        and other["state"] in ("OPEN", "MERGED")
        and other["repository"]["nameWithOwner"] == pr["repository"]["nameWithOwner"]
        and other["baseRefName"] != pr["baseRefName"]
        and not VERSION_PREFIX.match(other["title"])
        and subject(other["title"]) == subject(pr["title"])
        for other in peers
    )

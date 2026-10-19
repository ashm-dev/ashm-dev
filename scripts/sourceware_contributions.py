"""Read glibc patch revisions and reported bugs from Sourceware."""
import json
import urllib.parse
import urllib.request
from datetime import UTC, datetime

from patch_activity import has_recent_activity
from patch_versions import latest_patches

SOURCEWARE_EMAIL = "ashamil435@gmail.com"


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response), response.headers.get("Link", "")


def paginated(url, fetch):
    while url:
        page, links = fetch(url)
        yield from page
        url = next((part.split(";")[0].strip()[1:-1]
                    for part in links.split(",") if 'rel="next"' in part), None)


def glibc_project(fetch=fetch_json):
    now = datetime.now(UTC)
    url = "https://patchwork.sourceware.org/api/1.2/patches/?" + urllib.parse.urlencode({
        "project": "glibc", "submitter": SOURCEWARE_EMAIL, "per_page": 250,
    })
    patches = [patch for patch in latest_patches(paginated(url, fetch))
               if patch["state"] == "committed"
               or has_recent_activity(patch, paginated(patch["comments"], fetch), now)]
    url = "https://sourceware.org/bugzilla/rest/bug?" + urllib.parse.urlencode({
        "product": "glibc", "reporter": SOURCEWARE_EMAIL, "limit": 0,
        "include_fields": "id,summary,status,resolution,is_open",
    })
    response, _ = fetch(url)
    return {
        "Patches": [("done" if patch["state"] == "committed" else "open", f"#{patch['id']}",
                     f"https://patchwork.sourceware.org/patch/{patch['id']}/", patch["name"])
                    for patch in patches],
        "Bugs": [("open" if bug["is_open"] else "done", f"BZ #{bug['id']}",
                  f"https://sourceware.org/bugzilla/show_bug.cgi?id={bug['id']}", bug["summary"])
                 for bug in sorted(response["bugs"], key=lambda bug: bug["id"], reverse=True)
                 if bug["is_open"] or bug["resolution"] == "FIXED"],
    }

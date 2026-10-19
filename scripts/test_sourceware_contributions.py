import unittest
from urllib.parse import parse_qs, urlsplit

from sourceware_contributions import glibc_project


class SourcewareTest(unittest.TestCase):
    def test_pagination_revisions_and_bug_resolutions(self):
        def fetch(url):
            query = parse_qs(urlsplit(url).query)
            if "patchwork" in url:
                patch = {"id": 1, "name": "[v2] Fix parser", "state": "new",
                         "date": "2026-10-01", "series": [{"version": 2}]}
                if query.get("page") == ["2"]:
                    patch.update(id=2, name="[v3] Fix parser", state="committed", series=[{"version": 3}])
                    return [patch], ""
                return [patch], '<https://patchwork.sourceware.org/api/1.2/patches/?page=2>; rel="next"'
            self.assertIn("resolution", query["include_fields"][0])
            return {"bugs": [
                {"id": 1, "summary": "Open", "status": "NEW", "is_open": True, "resolution": ""},
                {"id": 2, "summary": "Fixed", "status": "VERIFIED", "is_open": False, "resolution": "FIXED"},
                {"id": 3, "summary": "Duplicate", "status": "RESOLVED", "is_open": False, "resolution": "DUPLICATE"},
            ]}, ""
        sections = glibc_project(fetch)
        self.assertEqual([x[:2] for x in sections["Patches"]], [("done", "#2")])
        self.assertEqual([x[:2] for x in sections["Bugs"]], [("done", "BZ #2"), ("open", "BZ #1")])


if __name__ == "__main__":
    unittest.main()

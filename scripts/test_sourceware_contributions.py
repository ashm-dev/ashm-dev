import unittest
from datetime import UTC, datetime
from unittest.mock import patch
from urllib.error import URLError
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


class PatchInactivityTest(unittest.TestCase):
    now = datetime(2026, 10, 19, 12, tzinfo=UTC)

    def make_patch(self, date="2026-09-01T12:00:00", state="new", version=1):
        return {"id": version, "name": f"[v{version}] Fix parser", "state": state,
                "date": date, "series": [{"version": version}],
                "comments": f"https://patchwork.sourceware.org/api/patches/{version}/comments/"}

    def collect(self, patches, comments=None):
        responses = {item["comments"]: ([], "") for item in patches}
        responses.update(comments or {})

        def fetch(url):
            if "/comments/" in url:
                response = responses[url]
                if isinstance(response, Exception):
                    raise response
                return response
            if "patchwork" in url:
                return patches, ""
            return {"bugs": []}, ""

        with patch("sourceware_contributions.datetime") as clock:
            clock.now.return_value = self.now
            return glibc_project(fetch)["Patches"]

    def test_unanswered_patch_expires_after_thirty_days(self):
        for date, expected in [("2026-09-19T12:00:01", ["#1"]),
                               ("2026-09-19T12:00:00", []),
                               ("2026-09-19T11:59:59", [])]:
            with self.subTest(date=date):
                self.assertEqual([item[1] for item in self.collect([self.make_patch(date)])], expected)

    def test_old_committed_patch_stays_without_reading_its_discussion(self):
        item = self.make_patch("2020-01-01T00:00:00", "committed")
        result = self.collect([item], {item["comments"]: URLError("Unavailable")})
        self.assertEqual([row[:2] for row in result], [("done", "#1")])

    def test_last_reply_resets_the_deadline_regardless_of_author_or_order(self):
        item = self.make_patch()
        for email in ["reviewer@example.org", "ashamil435@gmail.com"]:
            with self.subTest(email=email):
                comments = [{"date": "2026-09-20T12:00:00", "submitter": {"email": email}},
                            {"date": "2026-09-02T12:00:00", "submitter": {"email": email}}]
                result = self.collect([item], {item["comments"]: (comments, "")})
                self.assertEqual([row[:2] for row in result], [("open", "#1")])

    def test_reply_deadline_uses_elapsed_time_not_calendar_dates(self):
        item = self.make_patch()
        for date, expected in [("2026-09-19T15:00:00+03:00", []),
                               ("2026-09-19T15:00:01+03:00", ["#1"]),
                               ("2026-09-19T12:00:00Z", [])]:
            with self.subTest(date=date):
                result = self.collect([item], {item["comments"]: ([{"date": date}], "")})
                self.assertEqual([row[1] for row in result], expected)

    def test_recent_reply_on_later_page_reopens_an_inactive_patch(self):
        item = self.make_patch()
        self.assertEqual(self.collect([item]), [])
        url = item["comments"]
        result = self.collect([item], {
            url: ([{"date": "2026-09-02T12:00:00"}], f'<{url}?page=2>; rel="next"'),
            url + "?page=2": ([{"date": "2026-10-18T12:00:00"}], ""),
        })
        self.assertEqual([row[:2] for row in result], [("open", "#1")])

    def test_expired_latest_revision_does_not_restore_an_older_revision(self):
        old = self.make_patch()
        latest = self.make_patch(version=2)
        result = self.collect([old, latest], {
            old["comments"]: ([{"date": "2026-10-18T12:00:00"}], ""),
        })
        self.assertEqual(result, [])

    def test_unavailable_discussion_does_not_silently_hide_a_patch(self):
        item = self.make_patch()
        with self.assertRaises(URLError):
            self.collect([item], {item["comments"]: URLError("Unavailable")})


if __name__ == "__main__":
    unittest.main()

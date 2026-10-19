import unittest

from patch_versions import latest_patches


def patch(number, name, version=1, state="new", date="2026-10-01T00:00:00"):
    return {"id": number, "name": name, "state": state, "date": date,
            "series": [{"version": version}]}


class PatchVersionsTest(unittest.TestCase):
    def test_latest_revision_replaces_old_still_open_revision(self):
        old = patch(144254, "[v2] libio: Use __wunderflow", 2)
        latest = patch(145006, "[v3] libio: Use __wunderflow", 3, "committed")
        self.assertEqual(latest_patches([old, latest]), [latest])

    def test_rejected_latest_does_not_restore_old_revision(self):
        old = patch(1, "Fix example")
        latest = patch(2, "[v2] Fix example", 2, "rejected")
        self.assertEqual(latest_patches([latest, old]), [])

    def test_separate_patches_for_same_bug_are_not_combined(self):
        first = patch(1, "Fix parser [BZ #123]")
        second = patch(2, "Test parser [BZ #123]")
        self.assertEqual({p["id"] for p in latest_patches([first, second])}, {1, 2})

    def test_series_versions_keep_both_parts(self):
        rows = [patch(1, "[v2,1/2] Fix parser", 2), patch(2, "[v2,2/2] Add test", 2),
                patch(3, "[v3,1/2] Fix parser", 3, "committed"),
                patch(4, "[v3,2/2] Add test", 3, "committed")]
        self.assertEqual({p["id"] for p in latest_patches(rows)}, {3, 4})

    def test_renamed_superseded_patch_is_not_listed(self):
        old = patch(1, "Old title", state="superseded")
        latest = patch(2, "New title", state="committed")
        self.assertEqual(latest_patches([old, latest]), [latest])


if __name__ == "__main__":
    unittest.main()

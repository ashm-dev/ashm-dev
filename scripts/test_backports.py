import unittest

from backports import is_backport


def pr(number, title, base="main", body="", head="fix"):
    return {"number": number, "title": title, "baseRefName": base, "state": "MERGED",
            "headRefName": head, "body": body,
            "repository": {"nameWithOwner": "python/cpython"}}


class BackportTest(unittest.TestCase):
    def test_versioned_copy_of_original_is_excluded(self):
        original = pr(140307, "gh-140306: Fix memory leaks")
        copy = pr(140397, "[3.13] gh-140306: Fix memory leaks", "3.13")
        self.assertTrue(is_backport(copy, [original, copy]))
        self.assertFalse(is_backport(original, [original, copy]))

    def test_manual_backport_with_changed_title_is_excluded(self):
        copy = pr(150078, "[3.14] Fix JSON use-after-free", "3.14",
                  "Manual backport of #142851 to 3.14.")
        self.assertTrue(is_backport(copy, [copy]))

    def test_cherry_pick_is_excluded(self):
        copy = pr(140684, "Fix cleanup", "3.13",
                  "(cherry picked from commit a615fb49c948902a982c3256899507abcc9f9bc8)")
        self.assertTrue(is_backport(copy, [copy]))

    def test_original_release_fix_is_kept_despite_template(self):
        original = pr(159119, "gh-158961: Fix JIT crashes with UBSan", "3.14",
                      "<!-- Manual backport of #123; cherry picked from commit abc -->\nIssue: gh-158961")
        self.assertFalse(is_backport(original, [original]))

    def test_other_project_or_nonversion_title_does_not_create_a_copy(self):
        original = pr(1, "Update types")
        other = pr(2, "[3.13] Update types", "3.13")
        other["repository"] = {"nameWithOwner": "other/project"}
        self.assertFalse(is_backport(other, [original, other]))
        self.assertFalse(is_backport(pr(3, "[PyMySQL] Update types"), [original]))

    def test_unmerged_closed_attempt_does_not_hide_the_release_fix(self):
        original = pr(1, "Fix parser")
        original["state"] = "CLOSED"
        release_fix = pr(2, "[3.14] Fix parser", "3.14")
        self.assertFalse(is_backport(release_fix, [original, release_fix]))

    def test_versioned_pr_with_original_reference_is_excluded(self):
        self.assertTrue(is_backport(pr(4, "[8.18] Fix parser (#3)", "8.18"), []))


if __name__ == "__main__":
    unittest.main()

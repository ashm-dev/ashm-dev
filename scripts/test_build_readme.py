import unittest

from build_readme import render_all, splice, summary, to_data

PROJECTS = {
    "a/small": {"Pull requests": [("open", "#1", "u", "t")], "Issues": []},
    "c/empty": {"Pull requests": [], "Issues": []},
    "b/big": {"Pull requests": [("done", "#9", "u", "x"), ("done", "#10", "u", "<termios.h> __wrapped__ `_json`")],
              "Issues": [("done", "#2", "u", "i")]},
}


class RenderTest(unittest.TestCase):
    def test_orders_by_landed_and_escapes_markdown(self):
        out = render_all(PROJECTS)
        self.assertLess(out.index("b/big"), out.index("a/small"))
        self.assertIn("PR: 2 merged · Issues: 1 completed", out)
        self.assertIn("&lt;termios.h&gt; \\_\\_wrapped\\_\\_ `_json`", out)
        self.assertLess(out.index("[#10]"), out.index("[#9]"))
        self.assertNotIn("c/empty", out)
        self.assertNotIn("#### Issues", out.split("a/small")[1])

    def test_data_keeps_order_and_raw_titles(self):
        data = to_data(PROJECTS)
        self.assertEqual([p["name"] for p in data], ["b/big", "a/small"])
        self.assertEqual(data[0]["summary"], "PR: 2 merged · Issues: 1 completed")
        self.assertEqual(data[0]["sections"][0]["items"][0]["title"], "<termios.h> __wrapped__ `_json`")

    def test_summary_includes_open_counts_and_omits_empty_sections(self):
        self.assertEqual(summary(PROJECTS["a/small"]), "PR: 1 open")
        self.assertEqual(summary(PROJECTS["b/big"], "ru"), "PR: 2 принято · Issues: 1 выполнено")

    def test_commit_order_is_not_derived_from_hex_digits(self):
        commits = [("done", "abc123", "u", "Recent"), ("done", "fff999", "v", "Older")]
        data = to_data({"sqlalchemy/sqlalchemy": {"Commits": commits}})
        self.assertEqual([x["title"] for x in data[0]["sections"][0]["items"]], ["Recent", "Older"])
        self.assertEqual(data[0]["summary"], "Commits: 2 committed")

    def test_readme_has_circles_without_per_item_status_text(self):
        out = render_all(PROJECTS, "ru")
        self.assertIn("- 🟢 [#10]", out)
        self.assertIn("- 🟡 [#1]", out)
        self.assertIn("#### PR", out)
        self.assertNotIn("— принято", out)

    def test_trailing_title_whitespace_does_not_leak_into_markdown(self):
        out = render_all({"a/project": {"Pull requests": [("done", "#1", "u", "Title  ")]}})
        self.assertIn("[#1](u) Title\n", out)

    def test_splice_keeps_text_outside_markers(self):
        text = "intro\n<!-- contributions:start -->\nold\n<!-- contributions:end -->\ntail"
        self.assertEqual(splice(text, "new"),
                         "intro\n<!-- contributions:start -->\nnew\n<!-- contributions:end -->\ntail")


if __name__ == "__main__":
    unittest.main()

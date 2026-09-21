import unittest

from build_readme import normalize, render_all, splice, to_data

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
        self.assertIn("2 merged PRs · 1 issues", out)
        self.assertIn("&lt;termios.h&gt; \\_\\_wrapped\\_\\_ `_json`", out)
        self.assertLess(out.index("[#10]"), out.index("[#9]"))
        self.assertNotIn("c/empty", out)
        self.assertNotIn("#### Issues", out.split("a/small")[1])

    def test_data_keeps_order_and_raw_titles(self):
        data = to_data(PROJECTS)
        self.assertEqual([p["name"] for p in data], ["b/big", "a/small"])
        self.assertEqual(data[0]["summary"], "2 merged PRs · 1 issues")
        self.assertEqual(data[0]["sections"][0]["items"][0]["title"], "<termios.h> __wrapped__ `_json`")

    def test_normalize_drops_pr_suffix(self):
        self.assertEqual(normalize("Remove unused typing imports (#12568) "), "remove unused typing imports")

    def test_splice_keeps_text_outside_markers(self):
        text = "intro\n<!-- contributions:start -->\nold\n<!-- contributions:end -->\ntail"
        self.assertEqual(splice(text, "new"),
                         "intro\n<!-- contributions:start -->\nnew\n<!-- contributions:end -->\ntail")


if __name__ == "__main__":
    unittest.main()

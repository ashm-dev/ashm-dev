import unittest

from build_readme import render_all, splice


class RenderTest(unittest.TestCase):
    def test_orders_by_landed_and_escapes_html(self):
        projects = {
            "a/small": {"Pull requests": [("🟡", "#1", "u", "t")], "Issues": []},
            "b/big": {"Pull requests": [("✅", "#9", "u", "x"), ("✅", "#10", "u", "<termios.h>")],
                      "Issues": [("✅", "#2", "u", "i")]},
        }
        out = render_all(projects)
        self.assertLess(out.index("b/big"), out.index("a/small"))
        self.assertIn("2 merged PRs · 1 issues", out)
        self.assertIn("&lt;termios.h&gt;", out)
        self.assertLess(out.index("[#10]"), out.index("[#9]"))
        self.assertNotIn("**Issues**", out.split("a/small")[1])

    def test_splice_keeps_text_outside_markers(self):
        text = "intro\n<!-- contributions:start -->\nold\n<!-- contributions:end -->\ntail"
        self.assertEqual(splice(text, "new"),
                         "intro\n<!-- contributions:start -->\nnew\n<!-- contributions:end -->\ntail")


if __name__ == "__main__":
    unittest.main()

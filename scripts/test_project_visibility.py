import unittest

from build_readme import render_all, to_data


def items(count, state="done"):
    return [(state, f"#{number}", f"https://example.test/{number}", f"Change {number}")
            for number in range(1, count + 1)]


class ProjectVisibilityTest(unittest.TestCase):
    def test_hides_projects_with_at_most_five_prs_or_patches(self):
        cases = [
            {},
            {"Pull requests": []},
            {"Pull requests": items(1)},
            {"Pull requests": items(5)},
            {"Patches": items(5)},
            {"Pull requests": items(3), "Patches": items(2)},
            {"Issues": items(10)},
            {"Commits": items(10)},
            {"Bugs": items(10)},
            {"Pull requests": items(5), "Issues": items(10),
             "Commits": items(10), "Bugs": items(10)},
        ]
        for sections in cases:
            with self.subTest(sections=sections):
                projects = {"owner/project": sections}
                self.assertEqual(to_data(projects), [])
                for lang in ("en", "ru"):
                    self.assertEqual(render_all(projects, lang), "")

    def test_keeps_projects_with_more_than_five_prs_or_patches(self):
        cases = [
            {"Pull requests": items(6)},
            {"Patches": items(6)},
            {"Pull requests": items(3), "Patches": items(3)},
            {"Pull requests": items(5) + [("open", "#6", "https://example.test/6", "Change 6")]},
            {"Patches": items(6, "open")},
        ]
        for sections in cases:
            with self.subTest(sections=sections):
                projects = {"owner/project": sections}
                self.assertEqual([project["name"] for project in to_data(projects)], ["owner/project"])
                for lang in ("en", "ru"):
                    self.assertIn("<summary><b>owner/project</b>", render_all(projects, lang))

    def test_filters_hidden_projects_without_changing_visible_sections(self):
        projects = {
            "owner/hidden": {"Pull requests": items(5), "Issues": items(10)},
            "owner/visible": {"Pull requests": items(6), "Issues": items(2)},
        }
        data = to_data(projects)
        self.assertEqual([project["name"] for project in data], ["owner/visible"])
        self.assertEqual([section["title"] for section in data[0]["sections"]], ["Pull requests", "Issues"])
        self.assertEqual(len(data[0]["sections"][1]["items"]), 2)
        for lang in ("en", "ru"):
            out = render_all(projects, lang)
            self.assertIn("owner/visible", out)
            self.assertNotIn("owner/hidden", out)


if __name__ == "__main__":
    unittest.main()

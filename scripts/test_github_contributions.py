import unittest
from urllib.parse import parse_qs, urlsplit

from github_contributions import github_projects


def row(number, state="MERGED", repo="python/cpython", private=False, **extra):
    return {"number": number, "title": f"Change {number}", "url": f"https://github.com/{repo}/pull/{number}",
            "state": state, "baseRefName": "main", "headRefName": "fix", "body": "",
            "repository": {"nameWithOwner": repo, "isPrivate": private}, **extra}


class GithubTest(unittest.TestCase):
    def collect(self, prs=(), issues=(), commits=()):
        def api(*args, repo="ashm-dev/ashm-dev"):
            if args[0] == "graphql":
                self.assertIn("--paginate", args)
                query = next(arg for arg in args if arg.startswith("query="))
                kind, records = ("pullRequests", prs) if "pullRequests(" in query else ("issues", issues)
                return [{"data": {"user": {kind: {"nodes": list(records[:1])}}}},
                        {"data": {"user": {kind: {"nodes": list(records[1:])}}}}]
            endpoint = next(arg for arg in args if arg.startswith("repos/"))
            self.assertEqual(repo, "sqlalchemy/sqlalchemy")
            self.assertEqual(parse_qs(urlsplit(endpoint).query),
                             {"sha": ["main"], "author": ["ashm-dev"], "per_page": ["100"]})
            return [list(commits)]
        return github_projects(api)

    def test_open_and_merged_are_kept_without_matching_commit_titles(self):
        projects = self.collect([row(1), row(2, "OPEN"), row(3, "CLOSED")])
        self.assertEqual([(x[0], x[1]) for x in projects["python/cpython"]["Pull requests"]],
                         [("open", "#2"), ("done", "#1")])

    def test_private_and_excluded_projects_are_not_published(self):
        projects = self.collect([row(1, private=True), row(2, repo="kartochka/project"),
                                 row(3, repo="ashm-dev/fork"), row(4, repo="other/project")])
        self.assertEqual(set(projects), {"other/project"})

    def test_issues_require_completed_reason(self):
        issues = [row(1, "OPEN", stateReason=None), row(2, "CLOSED", stateReason="COMPLETED"),
                  row(3, "CLOSED", stateReason="NOT_PLANNED"), row(4, "CLOSED", stateReason="DUPLICATE")]
        projects = self.collect(issues=issues)
        self.assertEqual([(x[0], x[1]) for x in projects["python/cpython"]["Issues"]],
                         [("done", "#2"), ("open", "#1")])

    def test_sqlalchemy_counts_main_authorship_not_pr_or_committer(self):
        commits = [{"sha": "abc123def456", "html_url": "https://github.com/sqlalchemy/sqlalchemy/commit/abc123def456",
                    "author": {"login": "ashm-dev"}, "committer": {"login": "maintainer"},
                    "commit": {"message": "Different title\n\nDetails"}},
                   {"sha": "000000000000", "author": {"login": "someone-else"},
                    "committer": {"login": "ashm-dev"}}]
        projects = self.collect([row(1, repo="sqlalchemy/sqlalchemy"),
                                 row(2, "OPEN", repo="sqlalchemy/sqlalchemy")], commits=commits)
        sections = projects["sqlalchemy/sqlalchemy"]
        self.assertEqual(sections["Commits"], [("done", "abc123def4", commits[0]["html_url"], "Different title")])
        self.assertEqual([x[1] for x in sections["Pull requests"]], ["#2"])

    def test_backports_are_removed_but_release_specific_fixes_remain(self):
        prs = [row(1, title="Fix parser"),
               row(2, title="[3.13] Fix parser", baseRefName="3.13"),
               row(3, "OPEN", baseRefName="3.14", body="<!-- Backport instructions -->")]
        projects = self.collect(prs)
        self.assertEqual([x[1] for x in projects["python/cpython"]["Pull requests"]], ["#3", "#1"])


if __name__ == "__main__":
    unittest.main()

"""Direct positioning regressions and conservative non-prose exceptions."""

import importlib.util
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    "style_lint", Path(__file__).with_name("style_lint.py"))
lint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lint)


class FactoryPositioningTests(unittest.TestCase):
    def check(self, text, path="factories/index.mdx"):
        return lint.check_factory_positioning(text.splitlines(), path)

    def test_direct_and_wrapped_definitions(self):
        for text in (
            "Warp Factories is a team of cloud agents.",
            "Your factory is a team of agents.",
            "A **software factory** is a workforce of agents.",
            "A factory is a team\nof cloud agents.",
            "---\ndescription: >-\n  Your factory is a team of\n  cloud agents.\n---",
            '---\ndescription: "Warp Factories is a team of agents."\n---',
        ):
            with self.subTest(text=text):
                issues = self.check(text)
                self.assertEqual(len(issues), 1)
                self.assertEqual(issues[0].check, "factory-positioning")
                self.assertFalse(issues[0].fixable)

    def test_roles_quotes_code_and_comments_are_not_definitions(self):
        for text in (
            "The foreman routes the request to the review agent.",
            "Your engineering team configures the factory.",
            'Avoid "A factory is a team of agents".',
            "Avoid 'A factory is a team of agents'.",
            "> A factory is a team of agents.",
            "`A factory is a team of agents`",
            "~~~text\nA factory is a team of agents.\n~~~",
            "````text\n```\nA factory is a team of agents.\n````",
            "<!--\nA factory is a team of agents.\n-->",
            "{/*\nA factory is a team of agents.\n*/}",
            "Warp Factories is infrastructure for development workflows.",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.check(text), [])

    def test_history_and_line_locations(self):
        self.assertEqual(self.check("A factory is a team of agents.",
                                    "src/content/docs/changelog/2026.mdx"), [])
        issues = self.check("Introduction.\n\nYour factory is a team\nof agents.")
        self.assertEqual(issues[0].line, 3)


if __name__ == "__main__":
    unittest.main()

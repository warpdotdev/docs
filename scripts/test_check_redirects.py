#!/usr/bin/env python3
import unittest

from check_redirects import (
    load_redirects,
    redirect_source_matches_path,
    url_to_content_path,
)


class RedirectSourceTests(unittest.TestCase):
    def test_vercel_source_patterns_match_paths(self):
        cases = (
            ("/docs/", "/docs", True),
            ("/docs(/?)", "/docs", True),
            ("/docs(/?)", "/docs/", True),
            ("/docs(/?)", "/docs/child", False),
            ("/docs#section", "/docs", False),
            ("/:path*", "/", True),
            ("/:path*", "/docs/child", True),
            ("/docs/:path*", "/docs", True),
            ("/docs/:path*", "/documentation", False),
            ("/:path+", "/", False),
            ("/:path+", "/docs/child", True),
            ("/docs/:path+", "/docs", False),
            ("/docs/:path+", "/docs/child", True),
            ("/:path(.*)", "/", True),
            ("/:path(.*)", "/docs/child", True),
            ("/docs/:path(.*)", "/documentation/child", False),
            ("/errors/:code", "/errors/404", True),
            ("/errors/:code", "/errors/404/details", False),
            ("/university/(.*)", "/university/guides/terminal", True),
            ("/university/(.*)", "/universities/guides", False),
            (r"/guides/a-\+-b(/?)", "/guides/a-+-b", True),
            (r"/guides/a-\+-b(/?)", "/guides/a--b", False),
        )

        for source, path, expected in cases:
            with self.subTest(source=source, path=path):
                self.assertEqual(
                    redirect_source_matches_path(source, path),
                    expected,
                )

    def test_repository_source_patterns_are_supported(self):
        for redirect in load_redirects():
            with self.subTest(source=redirect["source"]):
                self.assertIsInstance(
                    redirect_source_matches_path(
                        redirect["source"],
                        "/__pattern_probe__",
                    ),
                    bool,
                )

    def test_live_session_sharing_page_has_no_redirect(self):
        route = "/knowledge-and-collaboration/session-sharing"

        self.assertIsNotNone(url_to_content_path(route))
        matching_sources = [
            redirect["source"]
            for redirect in load_redirects()
            if redirect_source_matches_path(redirect["source"], route)
        ]

        self.assertEqual(matching_sources, [])

    def test_restored_transition_page_has_no_redirect(self):
        route = "/platform/transitioning-from-oz"
        self.assertIsNotNone(url_to_content_path(route))
        self.assertEqual(
            [r["source"] for r in load_redirects()
             if redirect_source_matches_path(r["source"], route)],
            [],
        )

    def test_former_map_redirect_ends_at_restored_page(self):
        route = "/platform/documentation-map"
        self.assertIsNone(url_to_content_path(route))
        redirects = load_redirects()
        for source in (route, route + "/"):
            matches = [r for r in redirects
                       if redirect_source_matches_path(r["source"], source)]
            self.assertEqual(len(matches), 1, source)
            self.assertEqual(
                matches[0]["destination"], "/platform/transitioning-from-oz/"
            )
            self.assertEqual(matches[0]["statusCode"], 308)
            self.assertFalse(any(
                redirect_source_matches_path(r["source"], matches[0]["destination"])
                for r in redirects
            ))


if __name__ == "__main__":
    unittest.main()

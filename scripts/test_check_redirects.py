#!/usr/bin/env python3
import unittest

from check_redirects import (
    load_redirects,
    redirect_source_matches_path,
    url_to_content_path,
)


class RedirectSourceTests(unittest.TestCase):
    def test_live_session_sharing_page_has_no_redirect(self):
        route = "/knowledge-and-collaboration/session-sharing"

        self.assertIsNotNone(url_to_content_path(route))
        matching_sources = [
            redirect["source"]
            for redirect in load_redirects()
            if redirect_source_matches_path(redirect["source"], route)
        ]

        self.assertEqual(matching_sources, [])


if __name__ == "__main__":
    unittest.main()

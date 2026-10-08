#!/usr/bin/env python3
"""Regression tests for QUALITY-2052: `validate_ui_path` used to stop at the
Settings navigation hierarchy (section/umbrella/subpage + known sub_sections)
and treat any trailing segment as a free-form toggle/setting name, so a stale
path like "Settings > Features > General > Choose an editor to open file
links" kept validating after the control moved to "Settings > Code > Editor
and Code Review" in the reorg fixed by docs#587 / docs#708 — the old
"Features > General" section still exists, so nothing ever checked whether
the trailing control label actually belonged there.

These tests cover the extractor (`_extract_control_labels_from_text`,
`_extract_settings_sections`'s `controls` population) and the validator
(`_check_relocated_control`, wired into `validate_ui_path`) that close that
gap, plus a fixture modeled directly on the docs#708 diff: the old path must
fail, the corrected path must pass, and an unrelated "Features > General"
path with no known-control trailing segment must stay valid.

Run:
    python3 .agents/skills/validate_ui_refs/test_control_relocation.py
"""
from __future__ import annotations

import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("validate_ui_refs", _HERE / "validate_ui_refs.py")
vur = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vur)


def _valid_paths_fixture() -> dict:
    """A minimal synthetic snapshot modeled on the real Features / Code umbrella
    shape, with the four docs#708 controls attributed to "Editor and Code
    Review" and a handful of untouched Features controls attributed to
    "Features".
    """
    return {
        "umbrellas": {
            "Code": {
                "subpages": ["Indexing and projects", "Editor and Code Review"],
                "source_file": "app/src/settings_view/mod.rs",
            },
        },
        "deprecated_sections": {},
        "settings_sections": {
            "Features": {
                "display_name": "Features",
                "sub_sections": ["General", "Session"],
                "controls": ["Show sticky command header", "Auto save"],
                "source_file": "app/src/settings_view/features_page.rs",
            },
            "Editor and Code Review": {
                "display_name": "Editor and Code Review",
                "sub_sections": ["Code Editor and Review"],
                "controls": [
                    "Choose an editor to open file links",
                    "Choose a layout to open files in Warp",
                    "Group files into single editor pane",
                    "Open Markdown files in Warp's Markdown Viewer by default",
                ],
                "source_file": "app/src/settings_view/code_editor_review_page.rs",
                "umbrella": "Code",
            },
            "Indexing and projects": {
                "display_name": "Indexing and projects",
                "sub_sections": [],
                "controls": [],
                "source_file": "app/src/settings_view/code_indexing_page.rs",
                "umbrella": "Code",
            },
        },
        "macos_menu_bar": {},
        "warp_drive": {},
    }


class TestRelocatedControlDetection(unittest.TestCase):
    """Fixture modeled directly on the docs#708 diff (old path vs. fixed path)."""

    def setUp(self):
        self.data = _valid_paths_fixture()

    def test_stale_pre_708_path_fails(self):
        result = vur.validate_ui_path(
            "Settings > Features > General > Choose an editor to open file links",
            self.data,
        )
        self.assertFalse(result["valid"])
        self.assertEqual(result["fix_type"], "relocated_control")
        self.assertEqual(
            result["suggestion"],
            "Settings > Code > Editor and Code Review > Choose an editor to open file links",
        )

    def test_corrected_708_path_passes(self):
        result = vur.validate_ui_path(
            "Settings > Code > Editor and Code Review > Choose an editor to open file links",
            self.data,
        )
        self.assertTrue(result["valid"])

    def test_second_relocated_control_from_708_also_fails(self):
        result = vur.validate_ui_path(
            "Settings > Features > General > Choose a layout to open files in Warp",
            self.data,
        )
        self.assertFalse(result["valid"])
        self.assertEqual(
            result["suggestion"],
            "Settings > Code > Editor and Code Review > Choose a layout to open files in Warp",
        )

    def test_relocated_control_case_insensitive_match(self):
        # docs#708 also fixed a casing drift ("Markdown viewer" -> "Markdown
        # Viewer") alongside the path move; the label match is case-insensitive
        # so the stale path is still caught regardless of which casing drifted in.
        result = vur.validate_ui_path(
            "Settings > Features > General > "
            "Open Markdown files in Warp's Markdown viewer by default",
            self.data,
        )
        self.assertFalse(result["valid"])
        self.assertIn("Editor and Code Review", result["suggestion"])

    def test_features_general_without_trailing_control_stays_valid(self):
        # Acceptance criterion: the old section itself is still real and must
        # not be flagged just because it once hosted a control that moved.
        result = vur.validate_ui_path("Settings > Features > General", self.data)
        self.assertTrue(result["valid"])

    def test_unrelated_features_control_on_features_stays_valid(self):
        result = vur.validate_ui_path(
            "Settings > Features > General > Show sticky command header", self.data
        )
        self.assertTrue(result["valid"])

    def test_control_documented_on_its_own_umbrella_subpage_stays_valid(self):
        result = vur.validate_ui_path(
            "Settings > Code > Editor and Code Review > Group files into single editor pane",
            self.data,
        )
        self.assertTrue(result["valid"])

    def test_unknown_trailing_segment_stays_a_free_form_toggle_name(self):
        # A trailing segment that matches no known control label at all is
        # still allowed — this check only fires for *known* relocated controls.
        result = vur.validate_ui_path(
            "Settings > Features > General > Some made-up toggle name", self.data
        )
        self.assertTrue(result["valid"])


class TestControlLabelExtraction(unittest.TestCase):
    """Unit tests for `_extract_control_labels_from_text`."""

    def test_extracts_inline_render_body_item_literal(self):
        text = textwrap.dedent(
            """
            render_body_item::<EditorAndCodeReviewPageAction>(
                "Auto save".into(),
                None,
            )
            """
        )
        self.assertEqual(vur._extract_control_labels_from_text(text), ["Auto save"])

    def test_extracts_inline_render_body_item_to_string_literal(self):
        text = textwrap.dedent(
            """
            column.add_child(render_body_item::<ExternalEditorAction>(
                "Open Markdown files in Warp's Markdown Viewer by default".to_string(),
                None,
            ));
            """
        )
        self.assertEqual(
            vur._extract_control_labels_from_text(text),
            ["Open Markdown files in Warp's Markdown Viewer by default"],
        )

    def test_extracts_render_dropdown_item_second_argument(self):
        text = textwrap.dedent(
            """
            render_dropdown_item(
                appearance,
                "Choose an editor to open file links",
                None,
                None,
                LocalOnlyIconState::Hidden,
                None,
                &self.editor_dropdown,
            )
            """
        )
        self.assertEqual(
            vur._extract_control_labels_from_text(text),
            ["Choose an editor to open file links"],
        )

    def test_resolves_const_indirection(self):
        text = textwrap.dedent(
            """
            const TABBED_FILE_VIEWER_TOGGLE_HEADER: &str = "Group files into single editor pane";

            column.add_child(render_body_item::<ExternalEditorAction>(
                TABBED_FILE_VIEWER_TOGGLE_HEADER.into(),
                None,
            ));
            """
        )
        self.assertEqual(
            vur._extract_control_labels_from_text(text),
            ["Group files into single editor pane"],
        )

    def test_deduplicates_repeated_labels(self):
        text = textwrap.dedent(
            """
            render_body_item::<Action>("Auto save".into(), None);
            render_body_item::<Action>("Auto save".into(), None);
            """
        )
        self.assertEqual(vur._extract_control_labels_from_text(text), ["Auto save"])

    def test_no_matches_returns_empty_list(self):
        self.assertEqual(vur._extract_control_labels_from_text("fn noop() {}"), [])


class TestExtractSettingsSectionsControls(unittest.TestCase):
    """`_extract_settings_sections()` should populate `controls` per page,
    including from an extra embedded-sub-view file for "Editor and Code
    Review", while never attributing controls from a source file shared by
    multiple pages (that misattribution is the same failure mode the
    docstring already documents for `sub_sections`).
    """

    _MOD_RS = textwrap.dedent(
        """
        pub enum SettingsSection {
            Features,
            EditorAndCodeReview,
            WarpAgent,
            AgentProfiles,
        }

        impl Display for SettingsSection {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                match self {
                    SettingsSection::EditorAndCodeReview => write!(f, "Editor and Code Review"),
                    SettingsSection::AgentProfiles => write!(f, "Profiles"),
                    _ => write!(f, "{self:?}"),
                }
            }
        }
        """
    )

    def _build_warp_checkout(self, root: Path) -> None:
        settings_dir = root / "app" / "src" / "settings_view"
        settings_dir.mkdir(parents=True)
        (settings_dir / "mod.rs").write_text(self._MOD_RS, encoding="utf-8")
        (settings_dir / "features_page.rs").write_text(
            'render_body_item::<FeaturesPageAction>("Auto save".into(), None);',
            encoding="utf-8",
        )
        (settings_dir / "code_editor_review_page.rs").write_text(
            'render_body_item::<EditorAndCodeReviewPageAction>('
            '"Format on save".into(), None);',
            encoding="utf-8",
        )
        features_subdir = settings_dir / "features"
        features_subdir.mkdir()
        (features_subdir / "external_editor.rs").write_text(
            'render_dropdown_item(appearance, '
            '"Choose an editor to open file links", None, None, x, None, &h);',
            encoding="utf-8",
        )
        # A shared backing file for two umbrella subpages — controls here must
        # NOT be attributed to either page (see the class docstring).
        (settings_dir / "ai_page.rs").write_text(
            'render_body_item::<AiPageAction>("Shared widget label".into(), None);',
            encoding="utf-8",
        )

    def test_editor_and_code_review_collects_controls_from_primary_and_extra_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "warp"
            self._build_warp_checkout(root)
            sections = vur._extract_settings_sections(root)
            controls = sections["Editor and Code Review"]["controls"]
            self.assertIn("Format on save", controls)
            self.assertIn("Choose an editor to open file links", controls)

    def test_features_collects_its_own_controls_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "warp"
            self._build_warp_checkout(root)
            sections = vur._extract_settings_sections(root)
            self.assertEqual(sections["Features"]["controls"], ["Auto save"])

    def test_shared_source_file_controls_are_not_attributed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "warp"
            self._build_warp_checkout(root)
            sections = vur._extract_settings_sections(root)
            # "WarpAgent" and "AgentProfiles" are both hardcoded in
            # `_extract_settings_sections()`'s `page_files` map to the shared
            # ai_page.rs. No section should end up with its label attributed.
            all_controls = [
                c
                for entry in sections.values()
                for c in entry.get("controls", [])
            ]
            self.assertNotIn("Shared widget label", all_controls)


if __name__ == "__main__":
    unittest.main()

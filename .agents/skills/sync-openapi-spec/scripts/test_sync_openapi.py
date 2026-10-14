import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).with_name("sync_openapi.py")
SERVER_ROOT = SCRIPT.resolve().parents[4].parent / "warp-server"


class SyncOpenAPITest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "source.yaml"
        self.target = Path(self.temp.name) / "target.yaml"
        self.spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Public API",
                "version": "1",
                "description": "Factory and cloud-agent API.",
            },
            "tags": [{"name": "factory"}, {"name": "private", "x-internal": True}],
            "paths": {
                "/factory-inbox": {
                    "get": {
                        "operationId": "listInbox",
                        "tags": ["factory"],
                        "parameters": [
                            {"$ref": "#/components/parameters/Team"},
                            {
                                "name": "private",
                                "in": "query",
                                "x-internal": True,
                                "schema": {"type": "string"},
                            },
                        ],
                        "responses": {
                            "200": {"$ref": "#/components/responses/Result"},
                        },
                    },
                    "post": {
                        "operationId": "privateWrite",
                        "x-internal": True,
                        "responses": {
                            "200": {
                                "description": "private",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Private"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "components": {
                "parameters": {
                    "Team": {"name": "team", "in": "header", "schema": {"type": "string"}},
                    "Unused": {"name": "unused", "in": "query", "schema": {"type": "string"}},
                },
                "responses": {
                    "Result": {
                        "description": "ok",
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/Item"}},
                        },
                    },
                },
                "schemas": {
                    "Item": {
                        "type": "object",
                        "properties": {
                            "child": {"$ref": "#/components/schemas/Child"},
                            "secret": {"type": "string", "x-internal": True},
                            "name": {
                                "type": "string",
                                "x-oapi-codegen-extra-tags": {"binding": "required"},
                                "x-stainless-param": "name",
                            },
                        },
                    },
                    "Child": {
                        "type": "object",
                        "properties": {"parent": {"$ref": "#/components/schemas/Item"}},
                    },
                    "Private": {"type": "object", "x-internal": True},
                },
            },
        }

    def run_sync(self, mode):
        self.source.write_text(yaml.safe_dump(self.spec), encoding="utf-8")
        return subprocess.run(
            [
                sys.executable, str(SCRIPT), "--mode", mode,
                "--server-root", str(SERVER_ROOT),
                "--source", str(self.source), "--target", str(self.target),
            ],
            capture_output=True, text=True,
        )

    def test_public_export_matches_release_generator(self):
        result = self.run_sync("apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        canonical = Path(self.temp.name) / "canonical.yaml"
        subprocess.run(
            [str(SERVER_ROOT / "script/generate-public-openapi"), str(canonical), str(self.source)],
            check=True, capture_output=True, text=True,
        )
        self.assertEqual(self.target.read_bytes(), canonical.read_bytes())
        exported = yaml.safe_load(self.target.read_text())
        self.assertEqual(exported["info"], self.spec["info"])
        self.assertEqual(set(exported["paths"]["/factory-inbox"]), {"get"})
        self.assertEqual(exported["tags"], [{"name": "factory"}])
        self.assertEqual(set(exported["components"]["parameters"]), {"Team"})
        self.assertEqual(set(exported["components"]["schemas"]), {"Item", "Child"})
        item = exported["components"]["schemas"]["Item"]
        self.assertEqual(set(item["properties"]), {"child", "name"})
        self.assertEqual(item["properties"]["name"], {"type": "string"})
        self.assertEqual(self.run_sync("diff").returncode, 0)

    def test_unresolved_reference_does_not_overwrite_target(self):
        self.spec["components"]["schemas"]["Item"]["properties"]["child"] = {
            "$ref": "#/components/schemas/Missing",
        }
        self.target.write_text("existing target\n")
        result = self.run_sync("apply")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("#/components/schemas/Missing", result.stderr)
        self.assertEqual(self.target.read_text(), "existing target\n")

    def test_diff_reports_reusable_components_and_metadata(self):
        self.assertEqual(self.run_sync("apply").returncode, 0)
        exported = yaml.safe_load(self.target.read_text())
        actual = copy.deepcopy(exported)
        actual["tags"] = []
        actual["components"]["parameters"]["Team"]["description"] = "changed"
        self.target.write_text(yaml.safe_dump(actual))
        result = self.run_sync("diff")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("parameters", result.stdout)
        self.assertIn("Team", result.stdout)
        self.assertIn("tags", result.stdout)


if __name__ == "__main__":
    unittest.main()

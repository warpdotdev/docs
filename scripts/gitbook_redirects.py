#!/usr/bin/env python3

"""CLI tool to manage GitBook site redirects via the GitBook API.

Supports:
- List redirects
- Create redirect
- Update redirect
- Delete redirect
- Get redirect by source

Auth:
- Provide a GitBook API token via the GITBOOK_TOKEN environment variable
  or the --token flag.

Examples
========
List all redirects (using default org/site IDs):

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    list --limit 1000

List redirects matching a specific path fragment:

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    list --search "/support-and-billing/"

Create a redirect to a site page:

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    create \
    --source "/old-path" \
    --destination-json '{"kind": "site-page", "pageId": "PAGE_ID", "siteSpaceId": "SP_ID"}'

Update an existing redirect (change destination):

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    update SITE_REDIRECT_ID \
    --destination-json '{"kind": "site-page", "pageId": "NEW_PAGE_ID", "siteSpaceId": "SP_ID"}'

Update an existing redirect (change source only):

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    update SITE_REDIRECT_ID \
    --source "/new-old-path"

Delete a redirect by ID:

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    delete SITE_REDIRECT_ID

Get a redirect by its source path:

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    get-by-source --source "/old-path"

Get a redirect by source path for a share-link site:

  GITBOOK_TOKEN=xxx python gitbook_redirects.py \
    get-by-source --source "/old-path" --share-key SHARE_KEY
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import requests


API_BASE_URL = "https://api.gitbook.com/v1"


class GitBookRedirectClient:
    def __init__(self, token: str, organization_id: str, site_id: str) -> None:
        self.token = token
        self.organization_id = organization_id
        self.site_id = site_id
        self.base = f"{API_BASE_URL}/orgs/{organization_id}/sites/{site_id}"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _handle_response(self, resp: requests.Response) -> Any:
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Try to show GitBook error payload if present
            try:
                data = resp.json()
            except Exception:
                data = resp.text
            print(f"Request failed: {e}\nStatus: {resp.status_code}\nResponse: {data}", file=sys.stderr)
            sys.exit(1)

        if resp.status_code == 204:
            return None
        if not resp.content:
            return None
        try:
            return resp.json()
        except ValueError:
            return resp.text

    def list_redirects(self, page: Optional[str] = None, limit: Optional[int] = None, search: Optional[str] = None) -> Any:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if search is not None:
            params["search"] = search

        resp = self.session.get(f"{self.base}/redirects", params=params)
        return self._handle_response(resp)

    def create_redirect(self, source: str, destination: Dict[str, Any]) -> Any:
        payload = {"source": source, "destination": destination}
        resp = self.session.post(f"{self.base}/redirects", data=json.dumps(payload))
        return self._handle_response(resp)

    def delete_redirect(self, site_redirect_id: str) -> Any:
        resp = self.session.delete(f"{self.base}/redirects/{site_redirect_id}")
        return self._handle_response(resp)

    def update_redirect(
        self,
        site_redirect_id: str,
        source: Optional[str] = None,
        destination: Optional[Dict[str, Any]] = None,
    ) -> Any:
        payload: Dict[str, Any] = {}
        if source is not None:
            payload["source"] = source
        if destination is not None:
            payload["destination"] = destination

        if not payload:
            print("Nothing to update: provide --source and/or --destination-json", file=sys.stderr)
            sys.exit(1)

        resp = self.session.patch(f"{self.base}/redirects/{site_redirect_id}", data=json.dumps(payload))
        return self._handle_response(resp)

    def get_by_source(self, source: str, share_key: Optional[str] = None) -> Any:
        params: Dict[str, Any] = {"source": source}
        if share_key is not None:
            params["shareKey"] = share_key

        resp = self.session.get(f"{self.base}/redirect", params=params)
        return self._handle_response(resp)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage GitBook site redirects via API")

    parser.add_argument(
        "--org-id",
        default="-MbqIZLCtzerswjFm7mh",
        help="GitBook organization ID (default: -MbqIZLCtzerswjFm7mh)",
    )
    parser.add_argument(
        "--site-id",
        default="site_FKhQ8",
        help="GitBook site ID (default: site_FKhQ8)",
    )
    parser.add_argument("--token", help="GitBook API token (overrides GITBOOK_TOKEN env var)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser("list", help="List redirects")
    p_list.add_argument("--page", help="Identifier of the page of results to fetch")
    p_list.add_argument("--limit", type=int, help="Number of results per page (max 1000)")
    p_list.add_argument("--search", help="Search for a redirect by path")

    # create
    p_create = subparsers.add_parser("create", help="Create a redirect")
    p_create.add_argument("--source", required=True, help="Source path to redirect from (e.g. /old-path)")
    p_create.add_argument(
        "--destination-json",
        required=True,
        help=(
            "Destination JSON object. Example: {\"kind\": \"site-section\", \"siteSectionId\": \"...\"}. "
            "See GitBook docs for other destination kinds."
        ),
    )

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a redirect by ID")
    p_delete.add_argument("site_redirect_id", help="ID of the site redirect to delete")

    # update
    p_update = subparsers.add_parser("update", help="Update a redirect by ID")
    p_update.add_argument("site_redirect_id", help="ID of the site redirect to update")
    p_update.add_argument("--source", help="New source path")
    p_update.add_argument(
        "--destination-json",
        help="New destination JSON object (same format as in 'create')",
    )

    # get-by-source
    p_get = subparsers.add_parser("get-by-source", help="Get a redirect by its source path")
    p_get.add_argument("--source", required=True, help="Source path (e.g. /old-path)")
    p_get.add_argument("--share-key", help="Share key for sites published via share-links")

    return parser.parse_args(argv)


def load_destination_json(raw: Optional[str]) -> Optional[Dict[str, Any]]:
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON for destination: {e}", file=sys.stderr)
        sys.exit(1)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)

    token = args.token or os.getenv("GITBOOK_TOKEN")
    if not token:
        print("GitBook API token is required. Set GITBOOK_TOKEN or use --token.", file=sys.stderr)
        sys.exit(1)

    client = GitBookRedirectClient(token=token, organization_id=args.org_id, site_id=args.site_id)

    if args.command == "list":
        result = client.list_redirects(page=args.page, limit=args.limit, search=args.search)
    elif args.command == "create":
        dest = load_destination_json(args.destination_json)
        result = client.create_redirect(source=args.source, destination=dest)
    elif args.command == "delete":
        result = client.delete_redirect(site_redirect_id=args.site_redirect_id)
    elif args.command == "update":
        dest = load_destination_json(args.destination_json) if getattr(args, "destination_json", None) else None
        result = client.update_redirect(
            site_redirect_id=args.site_redirect_id,
            source=args.source,
            destination=dest,
        )
    elif args.command == "get-by-source":
        result = client.get_by_source(source=args.source, share_key=args.share_key)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

    if result is not None:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Pull the Oracle B2C Service metadata for the NCI CIS test instance, one component at a time.

Each kind of metadata is a registered component in components.py. This file is the runner:
it picks the components, adds any dependency an earlier run has not already satisfied, and
runs them in order against a dated extract folder. Nothing requests caller, staff or report
rows; the client refuses them before any network call.

Usage, from the repository root:

    export OSVC_SITE_URL=https://nci--tst.cx.usg.oraclecloud.com
    export OSVC_USER=<shared test account>
    python3 oracle/tools/pull_metadata.py --list          # the components
    python3 oracle/tools/pull_metadata.py --test          # catalog only
    python3 oracle/tools/pull_metadata.py                 # every component, today's folder
    python3 oracle/tools/pull_metadata.py --only mailboxes,standard-content
    python3 oracle/tools/pull_metadata.py --only report-definitions --into 2026-09-23 --report-ids 101125,101126

--into adds to an existing folder instead of today's. A selected component always runs; a
dependency runs only when that folder does not already hold its output.

Output: oracle/extracts/oracle-metadata/<YYYY-MM-DD>/ (gitignored).
See README.md for the folder layout. Bookkeeping in every folder:

    _scope.json      what was requested, skipped, classified, and which components ran when
    _manifest.jsonl  every request: time, URL, status, bytes, hash
    _errors.json     requests that did not return 200, with the likely cause
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from osvc_client import OsvcClient, RefusedRequest, load_credentials, load_site_url  # noqa: E402
from components import (  # noqa: E402,F401  (re-exported for callers and tests)
    REGISTRY,
    SCHEMA_SCOPE,
    Context,
    PullStop,
    field_names_from_named_id_listing,
    plan,
    pull_subtype_schemas,
    resource_names_from_catalog,
    run_component,
    save_menu,
)

TOOLS_DIR = Path(__file__).resolve().parent
EXTRACTS_DIR = TOOLS_DIR.parent / "extracts" / "oracle-metadata"

# The components the older --topup mode ran, kept as a named set.
TOPUP_COMPONENTS = ("menu-objects", "subtype-schemas", "custom-fields", "nested-named-ids")


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return body if isinstance(body, dict) else {}


def run_components(selected: list[str] | None, into: str | None = None,
                   report_ids: list[int] | None = None) -> int:
    """Run the selected components (all when None) into a dated folder. Returns an exit code."""
    folder = into or date.today().isoformat()
    out_dir = EXTRACTS_DIR / folder
    if into and not out_dir.is_dir():
        print(f"No earlier pull at {out_dir}.")
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    scope_path, errors_path = out_dir / "_scope.json", out_dir / "_errors.json"
    scope = _read_json(scope_path)
    errors: dict[str, str] = _read_json(errors_path)

    names = plan(selected if selected is not None else list(REGISTRY), out_dir, scope)
    site = load_site_url()
    client = OsvcClient(site, load_credentials(), manifest_path=out_dir / "_manifest.jsonl")
    scope.setdefault("site", site)
    scope.setdefault("date", folder)
    ctx = Context(client, out_dir, errors, scope, report_ids)

    print(f"Site: {site}")
    print(f"Output: {out_dir}")
    print(f"Components: {', '.join(names)}")
    code = 0
    try:
        for name in names:
            print(f"\n== {name}")
            run_component(ctx, name)
    except PullStop as exc:
        print(f"Stopped: {exc}")
        code = 1
    scope["refused_by_client"] = "see osvc_client.REFUSED_PREFIXES and the custom object classification"
    _save_json(scope_path, scope)
    _save_json(errors_path, errors)
    if errors:
        print(f"\n{len(errors)} entries in {errors_path}")
    if code == 0:
        print("Done. Next: python3 oracle/tools/build_data_dictionary.py")
    return code


def _save_json(path: Path, body: object) -> None:
    path.write_text(json.dumps(body, indent=2), encoding="utf-8")


def run(test_only: bool = False) -> int:
    """Every component into today's folder, or the catalog only with test_only."""
    return run_components(["catalog"] if test_only else None)


def topup(date_str: str) -> int:
    """Fetch what an earlier run of that folder missed: menu objects, sub-types, custom fields, nested menus."""
    return run_components(list(TOPUP_COMPONENTS), into=date_str)


def subtypes(date_str: str) -> int:
    return run_components(["subtype-schemas"], into=date_str)


def list_components() -> int:
    for comp in REGISTRY.values():
        deps = f"  (needs {', '.join(comp.depends_on)})" if comp.depends_on else ""
        print(f"{comp.name:22} {comp.description}{deps}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="list the components and stop")
    parser.add_argument("--test", action="store_true", help="connection test only: fetch the catalog listing and stop")
    parser.add_argument("--only", metavar="A,B", help="run only these components, plus any missing dependency")
    parser.add_argument("--into", metavar="YYYY-MM-DD", help="add to an existing extract folder instead of today's")
    parser.add_argument("--report-ids", metavar="ID,ID", help="report definitions to pull, instead of the keyword targeting")
    parser.add_argument("--topup", metavar="YYYY-MM-DD", help=f"same as --only {','.join(TOPUP_COMPONENTS)} --into YYYY-MM-DD")
    parser.add_argument("--subtypes", metavar="YYYY-MM-DD", help="same as --only subtype-schemas --into YYYY-MM-DD")
    args = parser.parse_args()
    try:
        if args.list:
            return list_components()
        if args.subtypes:
            return subtypes(args.subtypes)
        if args.topup:
            return topup(args.topup)
        if args.test:
            return run(test_only=True)
        only = [s.strip() for s in args.only.split(",") if s.strip()] if args.only else None
        report_ids = [int(s) for s in args.report_ids.split(",") if s.strip()] if args.report_ids else None
        return run_components(only, into=args.into, report_ids=report_ids)
    except RefusedRequest as exc:
        print(f"Stopped before sending a request: {exc}")
        return 2
    except ValueError as exc:
        print(exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

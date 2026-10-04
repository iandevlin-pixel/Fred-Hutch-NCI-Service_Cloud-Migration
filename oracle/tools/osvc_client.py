"""Read-only client for the Oracle B2C Service Connect REST API, for the NCI CIS metadata pull.

What it does:

1. GET requests only.
2. Requests only allowlisted schema and configuration resources, plus knowledge base
   answers. Answers are in migration scope and hold no caller PII (Ben Bolding, 2026-10-01).
   Every other record resource (incidents, contacts, tasks, accounts and the rest) and
   anything that runs a report are refused in code before any network call. The one query
   allowed is a ROQL query on the Answer object, through query_answers().
3. Rows of a custom object are allowed only when the pull has classified that object as a
   menu-only table (its fields are id, lookupName, display order and timestamps) and
   added it to the client's approved set at run time.
4. Appends every request to a JSON Lines manifest: time, URL, status, size, hash.

Credentials never live in code. The client reads OSVC_USER from the environment and the
password from OSVC_PASS or, by default, the macOS Keychain item with service name
"osvc-nci-tst" (store once with: security add-generic-password -a "$USER" -s osvc-nci-tst -w).
The site host comes from OSVC_SITE_URL.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

API_PATH = "/services/rest/connect/v1.4"
APP_CONTEXT = "Kicksaw NCI CIS metadata discovery"
KEYCHAIN_SERVICE = "osvc-nci-tst"
JSON = "application/json"
SCHEMA_JSON = "application/schema+json"

CUSTOM_OBJECT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*\.[A-Za-z][A-Za-z0-9_]*$")

# Path families where every sub-path is schema or menu structure.
ALLOWED_FAMILIES: tuple[str, ...] = ("metadata-catalog", "namedIDs", "namedIDHierarchies")

# Resources whose rows are configuration values, never caller or staff records.
ALLOWED_EXACT: frozenset[str] = frozenset(
    {
        "serviceCategories",
        "serviceDispositions",
        "serviceProducts",
        "countries",
        "holidays",
        "siteInterfaces",
        "channelTypes",
        "accountGroups",  # staff group names only; accounts rows are refused
        "analyticsReports",  # report definitions only; analyticsReportResults runs a report and is refused
        # Added 2026-09-23 on Ben Bolding's direction. Schemas checked first: no credential fields.
        "eventSubscriptions",  # outbound event notifications: name, class, event type, endpoint, status. integrationUser is stripped by the caller
        "mailboxes",  # mailbox name, type, interface, from and reply-to addresses, enabled flags. No passwords in the schema
        "serviceMailboxes",  # same shape as mailboxes
        "standardContents",  # canned agent replies; Mark Hubers cleared pulling them (via the UI, so the API too)
        # Added 2026-10-01 on Ben Bolding's direction: knowledge base articles are in migration
        # scope and are internal reference content, not caller PII. The constraint is PII.
        "answers",
        "answerVersions",
    }
)

# Named so the refusal message says why. Anything not allowed is refused anyway.
REFUSED_PREFIXES: tuple[str, ...] = (
    "queryResults",
    "analyticsReportResults",
    "incidents",
    "incidentResponse",
    "contacts",
    "organizations",
    "tasks",
    "chats",
    "accounts",
    "configurations",
    "opportunities",
    "assets",
    "campaigns",
    "mailings",
    "purchasedProducts",
    "bulkExtracts",
    "bulkExtractResults",
)

# A custom object is a menu table only when every property is one of these.
MENU_ONLY_FIELDS: frozenset[str] = frozenset(
    {"id", "lookupName", "displayOrder", "DisplayOrder", "Labels", "createdTime", "updatedTime", "links", "names"}
)

# Keys a menu option may carry. A named-ID or menu-object response with any other key is
# not a menu and is rejected before it is saved.
MENU_ITEM_KEYS: frozenset[str] = frozenset({"id", "lookupName", "links", "parents", "DisplayOrder", "displayOrder", "Labels", "Name", "createdTime", "updatedTime"})

# Named-ID fields whose option lists are people (staff accounts, contacts, organizations).
PEOPLE_FIELDS: frozenset[str] = frozenset(
    {"assignedTo", "account", "accounts", "contact", "contacts", "primaryContact", "organization",
     "organizations", "owner", "manager", "createdByAccount", "updatedByAccount", "assignedToAccount"}
)


class RefusedRequest(Exception):
    """Raised before any network call when a path is outside the allowlist."""


def is_people_field(field_name: str) -> bool:
    """True when a named-ID field's options are people. Exact names, plus *ByAccount."""
    return field_name in PEOPLE_FIELDS or field_name.endswith("ByAccount")


def non_menu_keys(items: object) -> set[str]:
    """Keys in a list of options that a menu option never carries. Empty set means a clean menu."""
    bad: set[str] = set()
    if not isinstance(items, list):
        return {"<not a list>"}
    for it in items:
        if not isinstance(it, dict):
            bad.add("<not an object>")
            continue
        bad |= set(it) - MENU_ITEM_KEYS
    return bad


def singular_resource(schema: object) -> dict:
    """The per-record definition inside an Oracle schema, or the schema itself.

    Oracle's metadata-catalog/<resource> schema describes the collection (properties: items)
    and puts the record's fields under definitions.singularResource.
    """
    if isinstance(schema, dict):
        sr = (schema.get("definitions") or {}).get("singularResource")
        if isinstance(sr, dict):
            return sr
        return schema
    return {}


def classify_custom_object(schema: object) -> str:
    """Return 'menu', 'data' or 'unknown' for a custom object's JSON Schema.

    'menu' means every property is a menu-table field (id, lookupName, display order,
    timestamps), so its rows are picklist values. Anything else is 'data' and its rows are
    never requested. 'unknown' means the schema shape was not recognised; treated as data.
    """
    sr = singular_resource(schema)
    props = _schema_properties(sr)
    if not props:
        return "unknown"
    extra = set(props) - MENU_ONLY_FIELDS
    # A Name label field is part of a menu only when Oracle itself flags the object as a menu.
    if sr.get("isMenu") is True:
        extra -= {"Name"}
    if extra:
        return "data"
    # Oracle flags menu-only objects with isMenu. Either signal alone would do; both must agree
    # when isMenu is present, so a mislabelled object stays data.
    if sr.get("isMenu") is False:
        return "data"
    return "menu"


def _schema_properties(schema: object) -> dict:
    if not isinstance(schema, dict):
        return {}
    if isinstance(schema.get("properties"), dict):
        return schema["properties"]
    merged: dict = {}
    for part in schema.get("allOf", []) or []:
        if isinstance(part, dict) and isinstance(part.get("properties"), dict):
            merged.update(part["properties"])
    return merged


def _keychain_password(service: str) -> str | None:
    try:
        out = subprocess.run(
            ["security", "find-generic-password", "-s", service, "-w"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def load_credentials() -> tuple[str, str]:
    user = os.environ.get("OSVC_USER")
    password = os.environ.get("OSVC_PASS") or _keychain_password(KEYCHAIN_SERVICE)
    if not user or not password:
        raise SystemExit(
            "Set OSVC_USER, and either OSVC_PASS or a Keychain item with service "
            f"'{KEYCHAIN_SERVICE}'. Nothing was sent."
        )
    return user, password


def load_site_url() -> str:
    site = os.environ.get("OSVC_SITE_URL", "").strip().rstrip("/")
    if not site:
        raise SystemExit("Set OSVC_SITE_URL, for example https://example.custhelp.com")
    parts = urlsplit(site)
    if parts.scheme != "https" or not parts.netloc:
        raise SystemExit("OSVC_SITE_URL must be an https URL with a host and nothing else")
    return f"{parts.scheme}://{parts.netloc}"


# Terms that would reach people or caller records from an Answer query (relationships such as
# UpdatedByAccount, or another object in a subquery). Matched anywhere, case-insensitively.
NON_ANSWER_TERMS = re.compile(
    r"incident|contact|organization|account|chat|task|opportunit|asset|campaign|mailing|purchasedproduct",
    re.IGNORECASE,
)
# Answer fields whose names contain a blocked term but describe an organization in the referral
# directory, not a caller. Allowed by Ben Bolding, 2026-10-02.
ANSWER_ALLOWED_FIELDS = (
    "customFields.c.referral_contact_email", "customFields.c.referral_contact_phone", "customFields.c.referral_contact",
)
ANSWER_QUERY_RE = re.compile(
    r"^select\s+.+?\s+from\s+answers?\b(?:\s+[a-z_]\w*)?(?:\s+(?:where|group\s+by|order\s+by|limit)\b.*)?$",
    re.IGNORECASE | re.DOTALL,
)


def check_answer_query(roql: str) -> str:
    """Return the ROQL query if it reads only the Answer object, or raise RefusedRequest."""
    q = (roql or "").strip()
    refusal = "Refused: only a single ROQL query on the Answer object is allowed. "
    if not q or ";" in q:
        raise RefusedRequest(refusal + "Got an empty query or more than one statement.")
    if len(re.findall(r"\bselect\b", q, re.IGNORECASE)) != 1 or len(re.findall(r"\bfrom\b", q, re.IGNORECASE)) != 1:
        raise RefusedRequest(refusal + "Subqueries are not allowed.")
    if not ANSWER_QUERY_RE.match(q):
        raise RefusedRequest(refusal + "The FROM clause must name Answer and nothing else.")
    scan = q
    for allowed in ANSWER_ALLOWED_FIELDS:
        scan = scan.replace(allowed, "")
    hit = NON_ANSWER_TERMS.search(scan)
    if hit:
        raise RefusedRequest(refusal + f"'{hit.group(0)}' could reach people or caller records.")
    return q


def check_path(relative_path: str, approved_menu_objects: frozenset[str] | set[str] = frozenset()) -> str:
    """Return the normalized relative path, or raise RefusedRequest."""
    rel = relative_path.strip().lstrip("/")
    if not rel or ".." in rel.split("/") or "?" in rel or "#" in rel:
        raise RefusedRequest(f"Malformed or empty path: {relative_path!r}")
    head = rel.split("/", 1)[0]
    if head in REFUSED_PREFIXES:
        raise RefusedRequest(
            f"Refused: '{head}' is a record, query or report-run resource. This tool pulls "
            "schema and configuration values only. See CLAUDE.md hard rules."
        )
    if head in ALLOWED_FAMILIES or head in ALLOWED_EXACT:
        return rel
    if CUSTOM_OBJECT_RE.match(head):
        if head in approved_menu_objects:
            return rel
        raise RefusedRequest(
            f"Refused: custom object '{head}' is not classified as a menu-only table. "
            "Its rows are data and are never requested."
        )
    raise RefusedRequest(
        f"Refused: '{head}' is not allowlisted. Add it deliberately, with a note on what it "
        "returns, before requesting it."
    )


class OsvcClient:
    def __init__(
        self,
        site_url: str,
        auth: tuple[str, str],
        manifest_path: Path,
        timeout: float = 60.0,
        session: requests.Session | None = None,
    ) -> None:
        self.base = f"{site_url}{API_PATH}"
        self.auth = auth
        self.manifest_path = manifest_path
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update({"OSvC-CREST-Application-Context": APP_CONTEXT})
        self.approved_menu_objects: set[str] = set()

    def approve_menu_object(self, name: str) -> None:
        """Allow rows of a custom object the pull has classified as a menu table."""
        self.approved_menu_objects.add(name)

    def get(
        self,
        relative_path: str,
        accept: str = JSON,
        params: dict[str, str | int] | None = None,
    ) -> tuple[int, bytes, dict[str, str]]:
        """GET an allowlisted path. Returns (status, body, headers) and logs to the manifest.

        Accept selects the representation: application/json returns the resource (for the
        catalog, the listing), application/schema+json returns the JSON Schema for it.
        params carries pagination only (limit, offset); the path itself may not contain a query.
        """
        rel = check_path(relative_path, self.approved_menu_objects)
        if params and set(params) - {"limit", "offset"}:
            raise RefusedRequest(f"Only limit and offset are allowed as query parameters, got {sorted(params)}")
        url = f"{self.base}/{rel}"
        started = time.monotonic()
        resp = self.session.get(url, auth=self.auth, timeout=self.timeout, headers={"Accept": accept}, params=params)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        body = resp.content
        logged_url = getattr(resp, "url", None) or url
        self._log(logged_url, resp.status_code, body, elapsed_ms, resp.headers.get("Content-Type", ""))
        return resp.status_code, body, dict(resp.headers)

    def get_json(
        self,
        relative_path: str,
        accept: str = JSON,
        params: dict[str, str | int] | None = None,
    ) -> tuple[int, object]:
        status, body, _ = self.get(relative_path, accept=accept, params=params)
        try:
            return status, json.loads(body or b"null")
        except json.JSONDecodeError:
            return status, {"_raw": body.decode("utf-8", errors="replace")}

    def get_all_items(self, relative_path: str, page_size: int = 100, max_pages: int = 50) -> tuple[int, list, list[dict]]:
        """Follow Oracle's offset pagination for a collection. Returns (last status, items, raw pages)."""
        items: list = []
        pages: list[dict] = []
        offset = 0
        status = 0
        for _ in range(max_pages):
            status, page = self.get_json(relative_path, params={"limit": page_size, "offset": offset})
            if status != 200 or not isinstance(page, dict):
                pages.append(page if isinstance(page, dict) else {"_raw": page})
                break
            pages.append(page)
            batch = page.get("items") or []
            items.extend(batch)
            if not page.get("hasMore") or not batch:
                break
            offset += len(batch)
        return status, items, pages

    def query_answers(self, roql: str) -> tuple[int, object]:
        """Run a ROQL query on the Answer object through queryResults. Any other query is refused."""
        q = check_answer_query(roql)
        url = f"{self.base}/queryResults"
        started = time.monotonic()
        resp = self.session.get(url, auth=self.auth, timeout=self.timeout, headers={"Accept": JSON}, params={"query": q})
        elapsed_ms = int((time.monotonic() - started) * 1000)
        body = resp.content
        self._log(getattr(resp, "url", None) or url, resp.status_code, body, elapsed_ms, resp.headers.get("Content-Type", ""))
        try:
            return resp.status_code, json.loads(body or b"null")
        except json.JSONDecodeError:
            return resp.status_code, {"_raw": body.decode("utf-8", errors="replace")}

    def _log(self, url: str, status: int, body: bytes, elapsed_ms: int, content_type: str) -> None:
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "method": "GET",
            "url": url,
            "status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "content_type": content_type,
            "elapsed_ms": elapsed_ms,
        }
        with self.manifest_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")


def diagnose(status: int) -> str:
    """One line on what a non-200 most likely means."""
    return {
        401: "401: credentials rejected, or the profile lacks Public SOAP API > Account Authentication.",
        403: "403: the profile's object permissions or the host allowlist blocked this resource.",
        404: "404: the resource or sub-path does not exist on this site.",
    }.get(status, f"{status}: unexpected. Read the saved body.")

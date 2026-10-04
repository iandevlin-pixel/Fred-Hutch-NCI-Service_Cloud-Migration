"""Counts-only queries on Oracle record objects, for data profiling.

Oracle does the counting. This module sends aggregate ROQL queries (count, min, max, grouped
by picklist or checkbox fields) and gets numbers back. It never selects a record's values:

1. The caller passes a structured AggregateQuery, never query text. The text is built here.
2. A field policy, read from the data dictionary, decides what each field may do:
   - picklists and checkboxes may be grouped (codes, not caller data);
   - createdTime, updatedTime and closedTime may be min, max or filtered;
   - every other field (free text, names, dates of birth, zip codes, ids, people) may only
     be counted as filled or not;
   - list sub-objects (threads, attachments, notes, phones, emails) are refused.
3. The finished text is checked again: one SELECT, no DELETE or UPDATE (Oracle's queryResults
   endpoint runs those too), no LIKE, no string literal other than a timestamp.
4. In a result grouped by two or more fields, a count from 1 to 10 is suppressed.
5. Requests are spaced out, and refused during CIS hours (9 a.m. to 9 p.m. Eastern) unless the
   caller sets allow_cis_hours. Ben Bolding, 2026-10-02: the test instance doesn't need the
   after-hours rule; keep it for anything that isn't a test instance.
6. The response body is never written to disk. The manifest logs its size and hash.

Ben Bolding, 2026-10-02: Fred Hutch approved data access on the test instance; profiling
runs as counts, outside CIS hours.
"""

from __future__ import annotations

import csv
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from osvc_client import JSON, OsvcClient, RefusedRequest

EASTERN = ZoneInfo("America/New_York")
CIS_OPEN_HOUR, CIS_CLOSE_HOUR = 9, 21
MIN_CELL = 11
TIME_FIELDS = frozenset({"createdTime", "updatedTime", "closedTime"})
# Dotted paths that are single values. Any other dotted path is a list or a related record.
SINGLE_VALUE_PREFIXES = ("customFields.", "statusWithType.", "assignedTo.staffGroup", "banner.importanceFlag")
# Personal-detail fields that may be counted as filled or empty, to measure what the retention
# scrub removes. Count only: the policy never lets them be grouped, filtered on or selected.
COUNT_ONLY_PATHS = frozenset({
    "name.first", "name.last", "emails.address", "phones.number",
    "address.street", "address.city", "address.postalCode",
})
# Picklists whose values are staff names, and fields that point at people.
PEOPLE_FIELDS = frozenset(
    {"customFields.c.ct_searcher", "customFields.c.lead_used", "primaryContact", "organization",
     "assignedTo.account", "createdByAccount", "updatedByAccount", "otherContacts", "asset"}
)
COUNT_STAR_ONLY = frozenset({"archivedIncidents"})
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PATH_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)*$")
UNSAFE_RE = re.compile(r"\b(delete|update|insert|describe|union|join|like|regexp|having|order\s+by|limit)\b", re.I)


@dataclass(frozen=True)
class AggregateQuery:
    """count(*) is always returned. `counts` adds count(field); `minmax` adds min and max."""

    object: str
    group_by: tuple[str, ...] = ()
    counts: tuple[str, ...] = ()
    minmax: tuple[str, ...] = ()
    where: tuple[tuple, ...] = ()  # (field, "ge"|"lt", timestamp) | (field, "is_null"|"not_null") | (field, "eq_id", int)


@dataclass
class AggregateResult:
    status: int
    columns: list[str] = field(default_factory=list)
    rows: list[list] = field(default_factory=list)
    suppressed_cells: int = 0
    truncated: bool = False
    error: str = ""
    roql: str = ""


class FieldPolicy:
    """What each field of each object may do, from data-dictionary.csv."""

    def __init__(self, rows: list[dict]) -> None:
        self.kinds: dict[str, dict[str, str]] = {}
        for r in rows:
            self.kinds.setdefault(r["object"], {})[r["field_path"]] = self._kind(r)

    @classmethod
    def from_csv(cls, path: Path) -> "FieldPolicy":
        with Path(path).open(encoding="utf-8", newline="") as fh:
            return cls(list(csv.DictReader(fh)))

    @staticmethod
    def _kind(r: dict) -> str:
        p = r["field_path"]
        if p in COUNT_ONLY_PATHS:
            return "countable"
        if "." in p and not p.startswith(SINGLE_VALUE_PREFIXES):
            return "excluded"
        if p in PEOPLE_FIELDS or p.endswith("ByAccount"):
            return "countable"
        if p in TIME_FIELDS:
            return "time"
        if str(r.get("is_menu", "")).lower() == "true":
            return "menu"
        if r.get("oracle_type") == "boolean":
            return "boolean"
        return "countable"

    def kind(self, obj: str, path: str) -> str:
        if obj not in self.kinds:
            raise RefusedRequest(f"Refused: object '{obj}' is not in the data dictionary.")
        if not PATH_RE.match(path or ""):
            raise RefusedRequest(f"Refused: malformed field path {path!r}.")
        k = self.kinds[obj].get(path)
        if k is None:
            raise RefusedRequest(f"Refused: '{path}' is not a field of {obj} in the data dictionary.")
        if k == "excluded":
            raise RefusedRequest(f"Refused: '{path}' is a list or related record on {obj}; it holds content.")
        return k

    def fields(self, obj: str, kinds: tuple[str, ...]) -> list[str]:
        return [p for p, k in self.kinds.get(obj, {}).items() if k in kinds]


def render(q: AggregateQuery, policy: FieldPolicy, menu_suffix: str = "lookupName", use_report: bool = False) -> str:
    """Build the ROQL text for a query, or raise RefusedRequest."""
    if menu_suffix not in ("lookupName", "id"):
        raise RefusedRequest("Refused: menu suffix must be lookupName or id.")
    if q.object in COUNT_STAR_ONLY:
        if q.group_by or q.counts or q.minmax or q.where:
            raise RefusedRequest(f"Refused: only count(*) is allowed on {q.object}.")
        select, where, group = ["count(*)"], [], []
    else:
        if q.object not in policy.kinds:
            raise RefusedRequest(f"Refused: object '{q.object}' is not in the data dictionary.")
        group = []
        for g in q.group_by:
            k = policy.kind(q.object, g)
            if k == "menu":
                group.append(f"{g}.{menu_suffix}")
            elif k == "boolean":
                group.append(g)
            else:
                raise RefusedRequest(f"Refused: '{g}' is not a picklist or checkbox, so it can't be a grouping.")
        select = list(group) + ["count(*)"]
        for c in q.counts:
            policy.kind(q.object, c)
            select.append(f"count({c})")
        for m in q.minmax:
            if policy.kind(q.object, m) != "time":
                raise RefusedRequest(f"Refused: min and max are allowed on system timestamps only, not '{m}'.")
            select += [f"min({m})", f"max({m})"]
        where = []
        for cond in q.where:
            f_, op = cond[0], cond[1]
            k = policy.kind(q.object, f_)
            if op in ("ge", "lt"):
                if k != "time" or not TIMESTAMP_RE.match(str(cond[2])):
                    raise RefusedRequest(f"Refused: '{f_}' {op} needs a system timestamp and a UTC ISO 8601 value.")
                where.append(f"{f_} {'>=' if op == 'ge' else '<'} '{cond[2]}'")
            elif op in ("is_null", "not_null"):
                where.append(f"{f_} IS {'NOT ' if op == 'not_null' else ''}NULL")
            elif op == "eq_id":
                if k != "menu" or not isinstance(cond[2], int):
                    raise RefusedRequest(f"Refused: eq_id needs a picklist field and an integer id, got '{f_}'.")
                where.append(f"{f_}.id = {cond[2]}")
            else:
                raise RefusedRequest(f"Refused: unknown filter '{op}'.")
    text = f"SELECT {', '.join(select)} FROM {q.object}"
    if where:
        text += " WHERE " + " AND ".join(where)
    if group:
        text += " GROUP BY " + ", ".join(group)
    assert_safe(text)
    return ("USE REPORT; " if use_report else "") + text


def assert_safe(text: str) -> None:
    """Second check on the finished statement, independent of how it was built."""
    if ";" in text or '"' in text:
        raise RefusedRequest("Refused: more than one statement, or a double quote.")
    if len(re.findall(r"\bselect\b", text, re.I)) != 1 or len(re.findall(r"\bfrom\b", text, re.I)) != 1:
        raise RefusedRequest("Refused: exactly one SELECT and one FROM are allowed.")
    if not re.match(r"^select\s", text, re.I) or UNSAFE_RE.search(text):
        raise RefusedRequest("Refused: the statement is not a plain counting SELECT.")
    if "*" in text.replace("count(*)", ""):
        raise RefusedRequest("Refused: '*' is allowed only inside count(*).")
    for literal in re.findall(r"'([^']*)'", text):
        if not TIMESTAMP_RE.match(literal):
            raise RefusedRequest("Refused: the only string literal allowed is a timestamp.")


def suppress(rows: list[list], n_group: int, min_cell: int = MIN_CELL) -> tuple[list[list], int]:
    """In a result grouped by two or more fields, blank any count from 1 to min_cell - 1."""
    if n_group < 2:
        return rows, 0
    hidden, out = 0, []
    for row in rows:
        new = list(row[:n_group])
        for v in row[n_group:]:
            n = int(v) if isinstance(v, str) and v.isdigit() else v
            if isinstance(n, int) and not isinstance(n, bool) and 0 < n < min_cell:
                new.append(None)
                hidden += 1
            else:
                new.append(v)
        out.append(new)
    return out, hidden


def in_cis_hours(now: datetime | None = None) -> bool:
    now = (now or datetime.now(EASTERN)).astimezone(EASTERN)
    return CIS_OPEN_HOUR <= now.hour < CIS_CLOSE_HOUR


class AggregateRunner:
    """Sends AggregateQuery objects through an OsvcClient, paced and counted."""

    def __init__(self, client: OsvcClient, policy: FieldPolicy, pause: float = 3.0, max_requests: int = 250,
                 menu_suffix: str = "lookupName", use_report: bool = False, timeout: float = 180.0,
                 clock=datetime.now, sleep=time.sleep, allow_cis_hours: bool = False) -> None:
        self.allow_cis_hours = allow_cis_hours
        self.client, self.policy = client, policy
        self.pause, self.max_requests = pause, max_requests
        self.menu_suffix, self.use_report, self.timeout = menu_suffix, use_report, timeout
        self.sent = 0
        self._clock, self._sleep = clock, sleep

    def run(self, q: AggregateQuery) -> AggregateResult:
        roql = render(q, self.policy, self.menu_suffix, self.use_report)
        if not self.allow_cis_hours and in_cis_hours(self._clock(EASTERN)):
            raise RefusedRequest("Refused: CIS is open (9 a.m. to 9 p.m. Eastern). Nothing was sent.")
        if self.sent >= self.max_requests:
            raise RefusedRequest(f"Refused: the run's budget of {self.max_requests} requests is used up.")
        if self.sent:
            self._sleep(self.pause)
        self.sent += 1
        url = f"{self.client.base}/queryResults"
        started = time.monotonic()
        resp = self.client.session.get(url, auth=self.client.auth, timeout=self.timeout,
                                       headers={"Accept": JSON}, params={"query": roql})
        body = resp.content
        self.client._log(getattr(resp, "url", None) or url, resp.status_code, body,
                         int((time.monotonic() - started) * 1000), resp.headers.get("Content-Type", ""))
        res = AggregateResult(status=resp.status_code, roql=roql)
        try:
            data = json.loads(body or b"null")
        except json.JSONDecodeError:
            res.error = "response was not JSON"
            return res
        if resp.status_code != 200:
            res.error = json.dumps({k: data.get(k) for k in ("title", "detail", "o:errorCode") if isinstance(data, dict)})[:400]
            return res
        table = (data.get("items") or [{}])[-1] if isinstance(data, dict) else {}
        res.columns = list(table.get("columnNames") or [])
        rows = [list(r) for r in (table.get("rows") or [])]
        res.truncated = len(rows) in (20000, 100000)
        res.rows, res.suppressed_cells = suppress(rows, len(q.group_by))
        return res

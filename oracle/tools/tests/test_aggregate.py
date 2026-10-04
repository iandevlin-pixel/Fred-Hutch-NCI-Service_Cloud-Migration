"""Tests for the counts-only query module. No network. Run with:

    python3 -m pytest oracle/tools/tests -q
"""

from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osvc_aggregate import (  # noqa: E402
    EASTERN, AggregateQuery, AggregateRunner, FieldPolicy, assert_safe, in_cis_hours, render, suppress,
)
from osvc_client import OsvcClient, RefusedRequest  # noqa: E402


def _row(path, is_menu=False, typ="string", obj="incidents"):
    return {"object": obj, "field_path": path, "is_menu": str(is_menu), "oracle_type": typ}


POLICY = FieldPolicy([
    _row("createdTime"), _row("updatedTime"), _row("subject"),
    _row("queue", True, "object"), _row("interface", True, "object"),
    _row("customFields.c.service_number", True, "object"),
    _row("customFields.c.ct_searcher", True, "object"),
    _row("customFields.c.ccr_patientfullname"), _row("customFields.c.zip_code_demo"),
    _row("customFields.c.ccr_aware", False, "boolean"),
    _row("primaryContact", False, "object"), _row("threads.text"),
    _row("id", False, "integer", obj="tasks"),
])


def test_count_and_group_by_picklists_render():
    q = AggregateQuery("incidents", group_by=("queue", "interface"), counts=("customFields.c.ccr_patientfullname",))
    assert render(q, POLICY) == (
        "SELECT queue.lookupName, interface.lookupName, count(*), count(customFields.c.ccr_patientfullname) "
        "FROM incidents GROUP BY queue.lookupName, interface.lookupName"
    )


def test_time_filter_minmax_and_report_prefix():
    q = AggregateQuery("incidents", minmax=("createdTime",), where=(("createdTime", "ge", "2022-01-01T00:00:00Z"),))
    text = render(q, POLICY, use_report=True)
    assert text.startswith("USE REPORT; SELECT count(*), min(createdTime), max(createdTime) FROM incidents WHERE createdTime >= ")


@pytest.mark.parametrize("q", [
    AggregateQuery("incidents", group_by=("subject",)),                      # free text as a grouping
    AggregateQuery("incidents", group_by=("customFields.c.zip_code_demo",)),  # zip code as a grouping
    AggregateQuery("incidents", group_by=("customFields.c.ct_searcher",)),    # staff names
    AggregateQuery("incidents", group_by=("primaryContact",)),                # a person
    AggregateQuery("incidents", counts=("threads.text",)),                    # a list holding content
    AggregateQuery("incidents", counts=("primaryContact.name.first",)),       # walking into a related record
    AggregateQuery("incidents", minmax=("customFields.c.ccr_patientfullname",)),
    AggregateQuery("incidents", where=(("subject", "ge", "2022-01-01T00:00:00Z"),)),
    AggregateQuery("incidents", where=(("createdTime", "ge", "' OR 1=1"),)),
    AggregateQuery("incidents", where=(("queue", "eq_id", "5; DELETE FROM incidents"),)),
    AggregateQuery("accounts"),                                               # not in the dictionary
    AggregateQuery("archivedIncidents", group_by=("queue",)),
    AggregateQuery("incidents", counts=("subject) FROM incidents; DELETE FROM incidents --",)),
])
def test_refused_queries(q):
    with pytest.raises(RefusedRequest):
        render(q, POLICY)


def test_final_text_check_refuses_writes_and_literals():
    assert_safe("SELECT count(*) FROM incidents")
    for bad in ("DELETE FROM incidents", "SELECT count(*) FROM incidents; DELETE FROM incidents",
                "SELECT * FROM incidents", "SELECT count(*) FROM incidents WHERE subject LIKE 'a'",
                "SELECT count(*) FROM incidents WHERE subject = 'smith'",
                "SELECT count(*) FROM incidents WHERE id IN (SELECT id FROM contacts)"):
        with pytest.raises(RefusedRequest):
            assert_safe(bad)


def test_small_cells_suppressed_only_with_two_or_more_groupings():
    rows = [["a", "x", 3, 500], ["a", "y", 11, "10"], ["b", "x", 0, 12]]
    out, hidden = suppress(rows, 2)
    assert out == [["a", "x", None, 500], ["a", "y", 11, None], ["b", "x", 0, 12]] and hidden == 2
    assert suppress([["a", 3]], 1) == ([["a", 3]], 0)


def test_cis_hours():
    assert in_cis_hours(datetime(2026, 10, 2, 9, 0, tzinfo=EASTERN))
    assert in_cis_hours(datetime(2026, 10, 2, 20, 59, tzinfo=EASTERN))
    assert not in_cis_hours(datetime(2026, 10, 2, 8, 59, tzinfo=EASTERN))
    assert not in_cis_hours(datetime(2026, 10, 2, 21, 0, tzinfo=EASTERN))


class _Resp:
    def __init__(self, body, status=200):
        self.status_code, self.content, self.headers, self.url = status, json.dumps(body).encode(), {"Content-Type": "application/json"}, "https://x/queryResults"


class _Session:
    def __init__(self, body, status=200):
        self.headers, self.calls, self._body, self._status = {}, [], body, status

    def get(self, url, **kw):
        self.calls.append((url, kw.get("params")))
        return _Resp(self._body, self._status)


def _runner(session, hour, **kw):
    tmp = Path(tempfile.mkdtemp())
    client = OsvcClient("https://x", ("u", "p"), tmp / "_manifest.jsonl", session=session)
    sleeps = []
    r = AggregateRunner(client, POLICY, clock=lambda tz: datetime(2026, 10, 2, hour, 0, tzinfo=EASTERN), sleep=sleeps.append, **kw)
    return r, sleeps, tmp


def test_runner_refuses_in_cis_hours_before_any_network_call():
    s = _Session({})
    r, _, _ = _runner(s, 10)
    with pytest.raises(RefusedRequest):
        r.run(AggregateQuery("incidents"))
    assert s.calls == []


def test_runner_paces_budgets_parses_by_position_and_logs_no_body():
    body = {"items": [{"columnNames": ["lookupName", "lookupName", "count(*)"], "rows": [["A", "X", "4"], ["A", "Y", "40"]]}]}
    s = _Session(body)
    r, sleeps, tmp = _runner(s, 7, max_requests=2)
    res = r.run(AggregateQuery("incidents", group_by=("queue", "interface")))
    assert res.rows == [["A", "X", None], ["A", "Y", "40"]] and res.suppressed_cells == 1
    r.run(AggregateQuery("incidents"))
    assert sleeps == [3.0]
    with pytest.raises(RefusedRequest):
        r.run(AggregateQuery("incidents"))
    assert len(s.calls) == 2 and s.calls[0][1]["query"].startswith("SELECT queue.lookupName")
    logged = (tmp / "_manifest.jsonl").read_text()
    assert '"sha256"' in logged and '"A"' not in logged


def test_error_response_keeps_message_not_rows():
    s = _Session({"title": "Invalid query", "detail": "bad field"}, status=400)
    r, _, _ = _runner(s, 7)
    res = r.run(AggregateQuery("incidents"))
    assert res.status == 400 and "Invalid query" in res.error and res.rows == []


def test_personal_detail_fields_are_count_only():
    pol = FieldPolicy([_row("name.first", obj="contacts"), _row("emails.address", obj="contacts"),
                       _row("customFields.c.pii_removed", False, "boolean", obj="contacts"), _row("phones.rawNumber", obj="contacts")])
    q = AggregateQuery("contacts", group_by=("customFields.c.pii_removed",), counts=("name.first", "emails.address"))
    assert "count(name.first), count(emails.address)" in render(q, pol)
    for bad in (AggregateQuery("contacts", group_by=("name.first",)), AggregateQuery("contacts", counts=("phones.rawNumber",)),
                AggregateQuery("contacts", where=(("name.first", "eq_id", 1),))):
        with pytest.raises(RefusedRequest):
            render(bad, pol)


def test_cis_hours_override_is_explicit():
    s = _Session({"items": [{"columnNames": ["count(*)"], "rows": [["1"]]}]})
    r, _, _ = _runner(s, 10, allow_cis_hours=True)
    assert r.run(AggregateQuery("incidents")).status == 200


def test_answer_guard_allows_referral_contact_fields_only():
    from osvc_client import check_answer_query
    check_answer_query("SELECT id, customFields.c.referral_contact, customFields.c.referral_contact_email FROM answers WHERE id > 0 LIMIT 5")
    for bad in ("SELECT id, updatedByAccount FROM answers", "SELECT id FROM answers, contacts"):
        with pytest.raises(RefusedRequest):
            check_answer_query(bad)

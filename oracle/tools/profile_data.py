"""Profile how CIS uses Oracle, with counts only. See osvc_aggregate.py for the safety rules.

Usage, from the repository root, outside CIS hours (9 a.m. to 9 p.m. Eastern):

    export OSVC_SITE_URL=https://nci--tst.cx.usg.oraclecloud.com
    export OSVC_USER=<the test account>
    python3 oracle/tools/profile_data.py --phase probes --dry-run
    python3 oracle/tools/profile_data.py --phase probes,inventory,fields,picklists,channels

Phases:
    probes     what Oracle's query language supports here, tested on answers (articles)
    inventory  per object: record count, oldest and newest, how many changed in the window
    fields     per inquiry field: filled ever, filled in the window
    picklists  per inquiry picklist: count per value, ever and in the window
    channels   inquiries by interface (language), channel, source, queue and service number
    types      per queue, service number and point of access: how often each inquiry field is filled
    pairs      picklist pairs counted together, for dependent picklists and duplicate field sets
    objects    fields and picklists for tasks, contacts, chats and the custom objects
    retention  what the contact scrub removes: personal-detail fields filled, by the PII Removed flag
    scif       count per value for the intake form's checkboxes

Output: oracle/extracts/data-profile/<date>/ (gitignored). results.jsonl holds one line per
query: its key, the query text, the status and the counts. A run resumes by skipping keys
already answered. No record values are requested or stored.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from osvc_aggregate import EASTERN, AggregateQuery, AggregateRunner, FieldPolicy, in_cis_hours, render  # noqa: E402
from osvc_client import OsvcClient, RefusedRequest, load_credentials, load_site_url  # noqa: E402

TOOLS_DIR = Path(__file__).resolve().parent
EXTRACTS = TOOLS_DIR.parent / "extracts"
OBJECTS = ["incidents", "tasks", "contacts", "answers", "chats", "SCIF.SCIF", "DEMOGR.Study", "DEMOGR.StudyQueue",
           "DEMOGR.CollectionMethod", "DEMOGR.CollectionStatistics", "Referrals.ReferralLanguages", "Referrals.ReferralQCs"]
WINDOW_MONTHS = 48
BATCH = 15
CHANNEL_GROUPS = [
    ("interface",), ("channel",), ("source",), ("language",), ("queue",),
    ("interface", "channel"), ("interface", "source"), ("interface", "queue"), ("channel", "source"),
    ("interface", "customFields.c.point_of_access"), ("interface", "customFields.c.service_number"),
    ("customFields.c.point_of_access", "channel"), ("customFields.c.service_number", "queue"),
    ("interface", "customFields.c.chat_type_request"), ("interface", "customFields.c.contact_type"),
    ("customFields.c.point_of_access", "customFields.c.special_code_1"),
    ("customFields.c.service_number", "customFields.c.clinical_trials"),
]


def latest_dictionary() -> Path:
    folders = sorted(p for p in (EXTRACTS / "oracle-metadata").iterdir() if (p / "data-dictionary.csv").exists())
    return folders[-1] / "data-dictionary.csv"


class Run:
    def __init__(self, out: Path, runner: AggregateRunner | None, policy: FieldPolicy, dry: bool, stop_at: str) -> None:
        self.out, self.runner, self.policy, self.dry, self.stop_at = out, runner, policy, dry, stop_at
        self.allow_cis_hours = bool(runner and runner.allow_cis_hours)
        self.path = out / "results.jsonl"
        self.done: dict[str, dict] = {}
        self.last_error, self.unmeasurable = "", []
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                rec = json.loads(line)
                if rec.get("status") == 200:
                    self.done[rec["key"]] = rec

    def ask(self, key: str, q: AggregateQuery, **render_kw) -> dict | None:
        """Send one query unless it is already answered. Returns the stored record."""
        if key in self.done:
            return self.done[key]
        if self.dry:
            try:
                print(f"{key}\n    {render(q, self.policy, **(render_kw or {'menu_suffix': 'lookupName'}))}")
            except RefusedRequest as e:
                print(f"{key}\n    REFUSED: {e}")
            return None
        now = datetime.now(EASTERN)
        if not self.allow_cis_hours and (in_cis_hours(now) or now.strftime("%H:%M") >= self.stop_at):
            raise SystemExit(f"Stopped at {now:%H:%M} Eastern: past the stop time or inside CIS hours. Rerun to resume.")
        saved = (self.runner.menu_suffix, self.runner.use_report)
        if render_kw:
            self.runner.menu_suffix = render_kw.get("menu_suffix", saved[0])
            self.runner.use_report = render_kw.get("use_report", saved[1])
        try:
            res = self.runner.run(q)
        except RefusedRequest as e:
            rec = {"key": key, "status": 0, "error": str(e)}
        else:
            rec = {"key": key, "status": res.status, "roql": res.roql, "columns": res.columns, "rows": res.rows,
                   "suppressed_cells": res.suppressed_cells, "truncated": res.truncated, "error": res.error,
                   "n_group": len(q.group_by), "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        finally:
            self.runner.menu_suffix, self.runner.use_report = saved
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        flag = "" if rec["status"] == 200 else f"  <- {rec.get('error', '')[:160]}"
        print(f"{rec['status']}  {key}  rows={len(rec.get('rows') or [])}{flag}", flush=True)
        self.last_error = rec.get("error", "")
        if rec["status"] == 200:
            self.done[key] = rec
            return rec
        return None


def months_back(iso: str, months: int) -> str:
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    y, m = divmod(d.year * 12 + d.month - 1 - months, 12)
    return f"{y:04d}-{m + 1:02d}-01T00:00:00Z"


def cutoff(run: Run) -> str | None:
    rec = run.done.get("inventory/incidents/all")
    if not rec or not rec["rows"]:
        return None
    newest = rec["rows"][0][2]  # count(*), min(createdTime), max(createdTime), ...
    return months_back(newest, WINDOW_MONTHS) if newest else None


def phase_probes(run: Run) -> None:
    a = "answers"
    run.ask("probe/count", AggregateQuery(a))
    run.ask("probe/multi-aggregate", AggregateQuery(a, counts=("keywords", "summary"), minmax=("createdTime", "updatedTime")))
    run.ask("probe/group-lookupName", AggregateQuery(a, group_by=("language",)), menu_suffix="lookupName")
    run.ask("probe/group-id", AggregateQuery(a, group_by=("language",)), menu_suffix="id")
    run.ask("probe/custom-menu-id", AggregateQuery(a, group_by=("customFields.c.answer_types",)), menu_suffix="id")
    run.ask("probe/time-filter", AggregateQuery(a, where=(("updatedTime", "ge", "2024-01-01T00:00:00Z"),)))
    run.ask("probe/not-null-filter", AggregateQuery(a, where=(("keywords", "not_null"),)))
    run.ask("probe/long-text-count", AggregateQuery(a, counts=("solution", "customFields.c.is_notes")))
    run.ask("probe/use-report", AggregateQuery(a), use_report=True)


def phase_inventory(run: Run) -> None:
    for obj in OBJECTS:
        if obj not in run.policy.kinds:
            print(f"skip {obj}: not in the data dictionary")
            continue
        times = tuple(t for t in ("createdTime", "updatedTime") if run.policy.kinds[obj].get(t) == "time")
        run.ask(f"inventory/{obj}/all", AggregateQuery(obj, minmax=times))
    run.ask("inventory/archivedIncidents/all", AggregateQuery("archivedIncidents"))
    since = cutoff(run)
    if not since:
        return
    for obj in OBJECTS:
        kinds = run.policy.kinds.get(obj, {})
        if f"inventory/{obj}/all" in run.done and kinds.get("updatedTime") == "time":
            run.ask(f"inventory/{obj}/updated-in-window", AggregateQuery(obj, where=(("updatedTime", "ge", since),)))
            run.ask(f"inventory/{obj}/created-in-window", AggregateQuery(obj, where=(("createdTime", "ge", since),)))
    year = int(since[:4])
    newest_year = int(run.done["inventory/incidents/all"]["rows"][0][2][:4])
    for y in range(year, newest_year + 1):
        run.ask(f"inventory/incidents/created-{y}", AggregateQuery(
            "incidents", where=(("createdTime", "ge", f"{y}-01-01T00:00:00Z"), ("createdTime", "lt", f"{y + 1}-01-01T00:00:00Z"))))


def _windows(run: Run) -> list[tuple[str, tuple]]:
    since = cutoff(run)
    return [("all", ())] + ([("window", (("createdTime", "ge", since),))] if since else [])


def phase_fields(run: Run, obj: str = "incidents") -> None:
    fields = run.policy.fields(obj, ("menu", "boolean", "countable", "time"))
    for label, where in _windows(run):
        if where and run.policy.kinds.get(obj, {}).get("createdTime") != "time":
            continue
        for i in range(0, len(fields), BATCH):
            batch, key = list(fields[i:i + BATCH]), f"fields/{obj}/{label}/{i // BATCH:02d}"
            # Oracle can't count some fields (relationships). It names the field; drop it and retry.
            for _ in range(len(batch)):
                if run.ask(key, AggregateQuery(obj, counts=tuple(batch), where=where)) or run.dry or not batch:
                    break
                bad = re.search(r"column[^']*'([^']+)'", run.last_error or "")
                hit = [f for f in batch if bad and (f == bad.group(1) or f.split(".")[-1] == bad.group(1).split(".")[-1])]
                if not hit:
                    break
                batch.remove(hit[0])
                run.unmeasurable.append((obj, hit[0]))


def phase_picklists(run: Run, obj: str = "incidents", kinds: tuple = ("menu", "boolean")) -> None:
    for label, where in _windows(run):
        if where and run.policy.kinds.get(obj, {}).get("createdTime") != "time":
            continue
        for f in run.policy.fields(obj, kinds):
            run.ask(f"picklists/{obj}/{label}/{f}", AggregateQuery(obj, group_by=(f,), where=where))


def phase_channels(run: Run) -> None:
    known = run.policy.kinds["incidents"]
    for label, where in _windows(run):
        for group in CHANNEL_GROUPS:
            if all(g in known for g in group):
                run.ask(f"channels/{label}/{'+'.join(g.split('.')[-1] for g in group)}", AggregateQuery("incidents", group_by=group, where=where))
    since = cutoff(run)
    if since:
        newest_year = int(run.done["inventory/incidents/all"]["rows"][0][2][:4])
        for y in range(int(since[:4]), newest_year + 1):
            run.ask(f"channels/year-{y}/interface+channel", AggregateQuery(
                "incidents", group_by=("interface", "channel"),
                where=(("createdTime", "ge", f"{y}-01-01T00:00:00Z"), ("createdTime", "lt", f"{y + 1}-01-01T00:00:00Z"))))


TYPE_DIMENSIONS = ["queue", "customFields.c.service_number", "customFields.c.point_of_access"]
PAIRS = [
    ("product", "category"), ("category", "disposition"), ("queue", "disposition"),
    ("customFields.c.subject_of_int_1", "customFields.c.cancer_site_1"),
    ("customFields.c.subject_of_int_1", "customFields.c.action_1"),
    ("customFields.c.subject_of_int_1", "customFields.c.soi_1"),
    ("customFields.c.special_code_1", "customFields.c.special_code_2"),
    ("queue", "customFields.c.special_code_1"), ("queue", "customFields.c.contact_type"),
    ("queue", "customFields.c.client_type"), ("queue", "statusWithType.status"),
    ("customFields.c.service_number", "customFields.c.va_promo"),
    ("customFields.c.smoking_counseling", "customFields.c.no_counseling"),
    ("customFields.c.referral_type_1", "queue"), ("customFields.c.clinical_trials", "queue"),
]


def phase_types(run: Run) -> None:
    """Field fill counts per queue, service number and point of access, in the window.

    Oracle has no call-type field, so these three stand in for inquiry type."""
    where = dict(_windows(run)).get("window", ())
    fields = run.policy.fields("incidents", ("menu", "boolean", "countable"))
    fields = [f for f in fields if f not in ("primaryContact", "otherContacts")]
    for dim in TYPE_DIMENSIONS:
        rest = [f for f in fields if f != dim]
        for i in range(0, len(rest), BATCH):
            run.ask(f"types/{dim.split('.')[-1]}/{i // BATCH:02d}", AggregateQuery("incidents", group_by=(dim,), counts=tuple(rest[i:i + BATCH]), where=where))


def phase_pairs(run: Run) -> None:
    where = dict(_windows(run)).get("window", ())
    known = run.policy.kinds["incidents"]
    for a, b in PAIRS:
        if known.get(a) in ("menu", "boolean") and known.get(b) in ("menu", "boolean"):
            run.ask(f"pairs/{a.split('.')[-1]}+{b.split('.')[-1]}", AggregateQuery("incidents", group_by=(a, b), where=where))


def phase_retention(run: Run) -> None:
    """What the contact scrub removes: personal-detail fields filled, by the PII Removed flag."""
    c, flag = "contacts", "customFields.c.pii_removed"
    run.ask("retention/contacts/single-fields", AggregateQuery(c, group_by=(flag,), counts=(
        "name.first", "name.last", "address.street", "address.city", "address.postalCode", "login", "lookupName")))
    run.ask("retention/contacts/emails", AggregateQuery(c, group_by=(flag,), counts=("emails.address",)))
    run.ask("retention/contacts/phones", AggregateQuery(c, group_by=(flag,), counts=("phones.number",)))
    run.ask("retention/contacts/flag+exempt", AggregateQuery(c, group_by=(flag, "customFields.c.exempt")))
    run.ask("retention/contacts/flag+sms_consent", AggregateQuery(c, group_by=(flag, "customFields.c.sms_consent")))
    newest = run.done.get("inventory/contacts/all")
    if not newest:
        return
    y, m = int(newest["rows"][0][2][:4]), int(newest["rows"][0][2][5:7])
    for back in range(0, 30):
        yy, mm = divmod(y * 12 + m - 1 - back, 12)
        ny, nm = divmod(yy * 12 + mm + 1, 12)
        run.ask(f"retention/contacts/created-{yy:04d}-{mm + 1:02d}", AggregateQuery(c, group_by=(flag,), where=(
            ("createdTime", "ge", f"{yy:04d}-{mm + 1:02d}-01T00:00:00Z"), ("createdTime", "lt", f"{ny:04d}-{nm + 1:02d}-01T00:00:00Z"))))
    for y_ in range(2012, y + 1):
        run.ask(f"retention/incidents/exempt-{y_}", AggregateQuery("incidents", group_by=("customFields.c.exempt",), where=(
            ("createdTime", "ge", f"{y_}-01-01T00:00:00Z"), ("createdTime", "lt", f"{y_ + 1}-01-01T00:00:00Z"))))


def phase_scif(run: Run) -> None:
    """Count per value for the intake form's checkboxes, in the window."""
    where = dict(_windows(run)).get("window", ())
    for f in run.policy.fields("SCIF.SCIF", ("boolean",)):
        run.ask(f"picklists/SCIF.SCIF/window/{f}", AggregateQuery("SCIF.SCIF", group_by=(f,), where=where))


def phase_objects(run: Run) -> None:
    for obj in OBJECTS:
        if obj in ("incidents", "answers") or f"inventory/{obj}/all" not in run.done:
            continue
        phase_fields(run, obj)
        phase_picklists(run, obj, kinds=("menu",) if obj == "SCIF.SCIF" else ("menu", "boolean"))


PHASES = {"probes": phase_probes, "inventory": phase_inventory, "fields": phase_fields,
          "picklists": phase_picklists, "channels": phase_channels, "types": phase_types,
          "pairs": phase_pairs, "objects": phase_objects, "retention": phase_retention, "scif": phase_scif}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--phase", required=True, help="comma-separated: " + ", ".join(PHASES))
    ap.add_argument("--into", default=date.today().isoformat(), help="dated output folder")
    ap.add_argument("--dry-run", action="store_true", help="print the queries, send nothing")
    ap.add_argument("--pause", type=float, default=3.0)
    ap.add_argument("--max-requests", type=int, default=250)
    ap.add_argument("--menu-suffix", default="lookupName", choices=["lookupName", "id"])
    ap.add_argument("--use-report", action="store_true", help="run on Oracle's report database")
    ap.add_argument("--stop-at", default="08:45", help="Eastern time, HH:MM, after which nothing is sent")
    ap.add_argument("--allow-cis-hours", action="store_true", help="run during CIS hours; for a test instance only")
    args = ap.parse_args(argv)

    policy = FieldPolicy.from_csv(latest_dictionary())
    out = EXTRACTS / "data-profile" / args.into
    out.mkdir(parents=True, exist_ok=True)
    runner = None
    if not args.dry_run:
        client = OsvcClient(load_site_url(), load_credentials(), out / "_manifest.jsonl", timeout=180.0)
        runner = AggregateRunner(client, policy, pause=args.pause, max_requests=args.max_requests,
                                 menu_suffix=args.menu_suffix, use_report=args.use_report, allow_cis_hours=args.allow_cis_hours)
    run = Run(out, runner, policy, args.dry_run, args.stop_at)
    for name in args.phase.split(","):
        if name not in PHASES:
            raise SystemExit(f"Unknown phase {name!r}. Choose from: {', '.join(PHASES)}")
        print(f"== {name}", flush=True)
        PHASES[name](run)
    if runner:
        print(f"Requests sent: {runner.sent}. Results: {run.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

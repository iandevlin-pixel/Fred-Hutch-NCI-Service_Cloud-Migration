"""Build the shareable data dictionary: field definitions, picklist values and usage in one CSV.

Reads three local pulls under oracle/extracts/ and writes one file into oracle/ that is safe to commit:

    python3 oracle/tools/build_dictionary_with_usage.py

Inputs (all gitignored):
    oracle-metadata/<date>/data-dictionary.csv   one row per field
    oracle-metadata/<date>/picklist-values.parquet
    data-profile/<date>/results.jsonl            counts only, from profile_data.py
    data-profile/<date>/picklist_usage.parquet

The output holds field definitions, picklist values and counts. It holds no records. Fields whose
picklist values are staff names keep their row and get no values.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[1]
STAFF_NAME_FIELDS = {("incidents", "customFields.c.ct_searcher"), ("incidents", "customFields.c.lead_used")}
SEPARATOR = re.compile(r"^[\s.\-_=*]*$")
COUNT_ITEM = re.compile(r"count\(([^)]+)\)")
SEP = ";"


def field_counts(results: Path) -> pl.DataFrame:
    """Filled counts per object and field, all time and in the window, from the fields phase."""
    out: dict[tuple[str, str], dict[str, int]] = {}
    for line in results.open():
        r = json.loads(line)
        parts = r["key"].split("/")
        if parts[0] != "fields" or r["status"] != 200 or not r["rows"]:
            continue
        obj, scope = parts[1], parts[2]
        items = COUNT_ITEM.findall(r["roql"].split(" FROM ")[0])
        row = r["rows"][0]
        total = int(row[0])
        for item, value in zip(items[1:], row[1:]):
            slot = out.setdefault((obj, item), {})
            slot[f"records_{scope}"] = total
            slot[f"filled_{scope}"] = int(value or 0)
    return pl.DataFrame(
        [{"object": o, "field_path": f, **v} for (o, f), v in out.items()],
        schema={"object": pl.Utf8, "field_path": pl.Utf8, "records_all": pl.Int64, "filled_all": pl.Int64,
                "records_window": pl.Int64, "filled_window": pl.Int64},
    )


def usage_label(rec_w, fill_w, fill_all) -> str:
    if fill_w is None and fill_all is None:
        return "not measured"
    if not fill_all and not fill_w:
        return "never used"
    if not fill_w:
        return "no records in 48 months" if not rec_w else "historical only"
    return "rare (<1%)" if fill_w / rec_w < 0.01 else "in use"


def defined_values(pv: pl.DataFrame) -> dict[tuple[str, str], list[str]]:
    pv = pv.with_columns(
        pl.col("lookup_name").alias("v")
    ).sort("object", "field_or_object", pl.col("display_order").fill_null(10**9), "id")
    out: dict[tuple[str, str], list[str]] = {}
    for obj, field, v in pv.select("object", "field_or_object", "v").iter_rows():
        if v is None or SEPARATOR.match(v):
            continue
        out.setdefault((obj, field), []).append(v.strip())
    return out


def local_lists(meta: Path) -> tuple[set[str], dict[str, list[str]]]:
    """Lists the pull holds outside picklist-values: which named-ID lists are empty in Oracle, and a few extra lists."""
    empty: set[str] = set()
    for f in (meta / "named-ids").glob("*.json"):
        if f.name.startswith(("_", "hierarchy.")):
            continue
        body = json.loads(f.read_text())
        if isinstance(body, dict) and body.get("items") == []:
            empty.add(f.stem)
    extra: dict[str, list[str]] = {"dataType": [], "operator": []}
    for f in sorted((meta / "report-defs").glob("*.json")):
        body = json.loads(f.read_text())
        if not isinstance(body, dict):
            continue
        for part in ("columns", "filters"):
            for item in body.get(part) or []:
                for name in ("dataType", "operator"):
                    v = (item.get(name) or {}).get("lookupName") if isinstance(item, dict) else None
                    if v and v not in extra[name]:
                        extra[name].append(v)
    boxes = json.loads((meta / "config-rows" / "mailboxes.json").read_text())
    extra["mailboxes"] = [b["lookupName"] for b in (boxes.get("items", []) if isinstance(boxes, dict) else boxes) if b.get("lookupName")]
    return empty, extra


INTERFACES = ("standardContents", "adminVisibleInterfaces")
# Menu fields whose values are deliberately not read, with the reason shown in the file.
NOT_READ: dict[tuple[str, str], str] = {
    ("accounts", "accountHierarchy"): "Values are staff accounts and are not published",
    ("eventSubscriptions", "integrationUser"): "Values are staff accounts and are not published",
    ("DEMOGR.Study", "CollectionMethod"): "Rows of DEMOGR.CollectionMethod (3), a custom object the pull treats as data and does not read. Empty on all 4 studies",
    ("tasks", "marketingSettings.campaign"): "Rows of Oracle's marketing campaigns, which are out of scope and not read",
}
SIBLING = {"answerVersions": "answers"}


def resolve(r: dict, values: dict, seen: dict, empty: set[str], extra: dict[str, list[str]]) -> tuple[list[str], str]:
    """The defined values for one field and where they came from."""
    obj, path, target = r["object"], r["field_path"], r["lookup_target"] or ""
    leaf = path.split(".")[-1]
    if (obj, path) in values:
        return values[(obj, path)], "This field's own list"
    if (target, target) in values:
        return values[(target, target)], f"Rows of {target}"
    sib = SIBLING.get(obj)
    if sib and (sib, path) in values:
        return values[(sib, path)], f"Same list as {sib}.{path}"
    if obj == "analyticsReports" and leaf in extra and extra[leaf]:
        return extra[leaf], "Values seen in the report definitions pulled; may not be the full list"
    if (obj, path) in NOT_READ:
        return [], NOT_READ[(obj, path)]
    if leaf in ("adminVisibleInterfaces", "endUserVisibleInterfaces"):
        return values[INTERFACES], "The site's interfaces"
    if leaf == "staffGroup":
        return values[("accounts", "staffGroup")], "Same list as accounts.staffGroup"
    same = {tuple(v) for (o, f), v in values.items() if f.split(".")[-1] == leaf and o != obj}
    if len(same) == 1:
        return list(same.pop()), f"Shared Oracle list for {leaf}"
    if target == "mailboxes":
        return extra["mailboxes"], "Names of the site's mailboxes"
    if (obj, path) in seen:
        return seen[(obj, path)], "Values seen in the data; the defined list was not pulled"
    if f"{obj}.{path}" in empty or (sib and f"{sib}.{path}" in empty):
        return [], "No values defined in Oracle"
    if any(e.split(".")[-1] == leaf for e in empty) and not any(f.split(".")[-1] == leaf for _, f in values):
        return [], "No values defined in Oracle"
    return [], "Values not pulled"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default="2026-09-23")
    ap.add_argument("--profile", default="2026-10-02")
    args = ap.parse_args()
    meta = ROOT / "extracts" / "oracle-metadata" / args.metadata
    prof = ROOT / "extracts" / "data-profile" / args.profile

    d = pl.read_csv(meta / "data-dictionary.csv", infer_schema_length=None)
    d = d.filter(pl.col("field_path").fill_null("") != "")
    values = defined_values(pl.read_parquet(meta / "picklist-values.parquet"))
    counts = field_counts(prof / "results.jsonl")
    pu = pl.read_parquet(prof / "picklist_usage.parquet").filter(pl.col("value") != "(blank)")
    used: dict[tuple[str, str], list[tuple[str, int]]] = {}
    seen: dict[tuple[str, str], list[str]] = {}
    for obj, field, value, _, n_w in pu.sort("n_window", descending=True).iter_rows():
        if SEPARATOR.match(value):
            continue
        seen.setdefault((obj, field), []).append(value.strip())
        if n_w:
            used.setdefault((obj, field), []).append((value.strip(), n_w))
    empty, extra = local_lists(meta)

    d = d.join(counts, on=["object", "field_path"], how="left")
    rows = []
    for r in d.iter_rows(named=True):
        key = (r["object"], r["field_path"])
        vals, source = resolve(r, values, seen, empty, extra) if r["is_menu"] else ([], "")
        u = used.get(key, [])
        note = r["note"] or ""
        if key in STAFF_NAME_FIELDS:
            vals, u, source = [], [], "Values are staff names and are not published"
        is_bool = r["oracle_type"] == "boolean"
        checked = next((n for v, n in u if v in ("1", "true", "True")), 0) if is_bool and key in used else None
        rec_w, fill_w = r["records_window"], r["filled_window"]
        label = usage_label(rec_w, fill_w, r["filled_all"])
        if is_bool and checked is not None:
            label = "never used" if checked == 0 and label != "not measured" else label
            note = (note + " " if note else "") + "Checkbox: use checked_48mo, since Oracle stores unchecked as a value"
        rows.append({
            **{k: r[k] for k in ("object", "field_path", "label", "classification", "is_menu", "oracle_type", "oracle_format",
                                 "max_length", "read_only", "lookup_target", "description", "suggested_sf_type")},
            "usage_48mo": label,
            "records_48mo": rec_w,
            "filled_48mo": fill_w,
            "pct_filled_48mo": round(100 * fill_w / rec_w, 1) if rec_w and fill_w is not None else None,
            "checked_48mo": checked,
            "filled_all_time": r["filled_all"],
            "picklist_value_count": len(vals) if vals else None,
            "picklist_values": SEP.join(vals),
            "picklist_values_source": source,
            "picklist_values_used_48mo_count": len(u) if u and not is_bool else None,
            "picklist_values_used_48mo": "" if is_bool else SEP.join(v for v, _ in u),
            "note": note,
        })
    out = pl.DataFrame(rows, infer_schema_length=None)
    dest = ROOT / f"oracle-data-dictionary-{args.profile}.csv"
    out.write_csv(dest)
    print(f"{dest.name}: {out.height} fields, {out.filter(pl.col('picklist_values') != '').height} with picklist values, "
          f"{out.filter(pl.col('usage_48mo') != 'not measured').height} with usage")


if __name__ == "__main__":
    main()

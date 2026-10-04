"""Build the Oracle configuration inventory workbook from a pulled extract folder.

One Excel workbook, one tab per list, so the team can read the complete lists behind the Oracle
org summary: mailboxes, queues, profiles, staff groups, channels, statuses, custom objects,
custom fields, the data dictionary, picklist values, products, categories and dispositions, the
standard content index, surveys, reports and holidays.

Reads the extract folder and the data-dictionary and picklist-values Parquet files that
build_data_dictionary.py writes there, so run that first. Nothing here touches the network.

Two exclusions are enforced here rather than left to whoever opens the file:

    PEOPLE_VALUE_LISTS   picklists whose values are staff names. Counted on the About tab, never listed
    standard content     index columns only. The reply text is never read into the workbook

Usage:

    python3 oracle/tools/build_config_inventory.py [extract-folder]
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import polars as pl
import xlsxwriter

from build_data_dictionary import _load, newest_extract_dir

# (object, field_or_object) of picklists whose values name people. Descriptions in the dictionary:
# ct_searcher "The person who conducted the CT search"; lead_used "The primary lead used for this interaction".
PEOPLE_VALUE_LISTS = {
    ("incidents", "customFields.c.ct_searcher"),
    ("incidents", "customFields.c.lead_used"),
}

# Oracle report IDs below this are the stock reports shipped with the product; custom reports start here.
CUSTOM_REPORT_MIN_ID = 100000

# Names that mark a profile as test, UAT or a copy. A reading of the name, not of the profile's use.
TEST_PROFILE_PATTERN = r"(?i)\btest\b|\buat\b|copy of|do not use|^z"

SERVICE_MENUS = ("serviceProducts", "serviceCategories", "serviceDispositions")


def _items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        data = data.get("items", [])
    return [d for d in data or [] if isinstance(d, dict)]


def _read(extract_dir: Path, rel: str) -> list[dict[str, Any]]:
    path = extract_dir / rel
    return _items(_load(path)) if path.exists() else []


def _frame(rows: list[dict[str, Any]], columns: dict[str, Any]) -> pl.DataFrame:
    return pl.DataFrame(rows, schema=columns) if rows else pl.DataFrame(schema=columns)


def _id_name(extract_dir: Path, rel: str) -> pl.DataFrame:
    rows = [{"id": r.get("id"), "name": r.get("lookupName")} for r in _read(extract_dir, rel)]
    return _frame(rows, {"id": pl.Int64, "name": pl.String})


def _is_separator(name: str | None) -> bool:
    return bool(name) and set(name.strip()) <= set("-.")


def _interface_names(extract_dir: Path) -> dict[int, str]:
    return {r["id"]: r.get("lookupName", "") for r in _read(extract_dir, "menus/siteInterfaces.json")}


def _interface_list(value: Any, names: dict[int, str]) -> str:
    ids = []
    for item in _items(value):
        if "id" in item:
            ids.append(item["id"])
        else:
            href = next((l.get("href", "") for l in item.get("links", []) if isinstance(l, dict)), "") or item.get("href", "")
            tail = href.rstrip("/").rsplit("/", 1)[-1]
            if tail.isdigit():
                ids.append(int(tail))
    return ", ".join(names.get(i, str(i)) for i in sorted(ids))


def mailboxes(extract_dir: Path) -> pl.DataFrame:
    rows = []
    for r in _read(extract_dir, "config-rows/mailboxes.json"):
        incoming = r.get("incomingEmailSettings") or {}
        outgoing = r.get("outgoingEmailSettings") or {}
        rows.append({
            "id": r.get("id"),
            "name": r.get("lookupName"),
            "type": (r.get("type") or {}).get("lookupName"),
            "interface": (r.get("interface") or {}).get("lookupName"),
            "is_default": r.get("isDefault"),
            "incoming_enabled": incoming.get("isEnabled"),
            "outgoing_enabled": outgoing.get("isEnabled"),
            "from_address_test_instance": outgoing.get("fromAddress"),
            "reply_to_address": outgoing.get("replyToAddress"),
        })
    return _frame(rows, {
        "id": pl.Int64, "name": pl.String, "type": pl.String, "interface": pl.String, "is_default": pl.Boolean,
        "incoming_enabled": pl.Boolean, "outgoing_enabled": pl.Boolean,
        "from_address_test_instance": pl.String, "reply_to_address": pl.String,
    })


def queues(extract_dir: Path) -> pl.DataFrame:
    """Queues in Oracle's order. Oracle separates groups with dash rows; section counts the groups."""
    rows, section = [], 1
    for r in _read(extract_dir, "named-ids/incidents.queue.json"):
        name = r.get("lookupName")
        separator = _is_separator(name)
        if separator:
            section += 1
        rows.append({"order": len(rows) + 1, "id": r.get("id"), "name": name, "is_separator": separator,
                     "section": None if separator else section})
    return _frame(rows, {"order": pl.Int64, "id": pl.Int64, "name": pl.String, "is_separator": pl.Boolean, "section": pl.Int64})


def profiles(extract_dir: Path) -> pl.DataFrame:
    return _id_name(extract_dir, "named-ids/accounts.profile.json").with_columns(
        pl.col("name").str.contains(TEST_PROFILE_PATTERN).fill_null(False).alias("test_or_uat_by_name")
    )


def channels(extract_dir: Path) -> pl.DataFrame:
    parts = [
        _id_name(extract_dir, rel).select(pl.lit(label).alias("list"), "id", "name")
        for label, rel in (
            ("Site interface", "menus/siteInterfaces.json"),
            ("Channel type", "menus/channelTypes.json"),
            ("Inquiry channel", "named-ids/incidents.channel.json"),
        )
    ]
    return pl.concat(parts)


def statuses(extract_dir: Path) -> pl.DataFrame:
    parts = [
        _id_name(extract_dir, f"named-ids/{obj}.statusWithType.status.json").select(pl.lit(obj).alias("object"), "id", "name")
        for obj in ("incidents", "tasks", "answers")
    ]
    return pl.concat(parts).with_columns(
        pl.col("name").map_elements(_is_separator, return_dtype=pl.Boolean).alias("is_placeholder")
    )


def custom_objects(extract_dir: Path, dictionary: pl.DataFrame) -> pl.DataFrame:
    kinds = (_load(extract_dir / "_scope.json") if (extract_dir / "_scope.json").exists() else {}).get(
        "custom_object_classification", {}) or {}
    counts = dict(dictionary.group_by("object").agg(pl.len().alias("n")).iter_rows())
    rows = [{"package": name.split(".", 1)[0], "object": name, "kind": kind, "dictionary_rows": counts.get(name, 0)}
            for name, kind in sorted(kinds.items())]
    return _frame(rows, {"package": pl.String, "object": pl.String, "kind": pl.String, "dictionary_rows": pl.Int64})


def custom_fields(dictionary: pl.DataFrame) -> pl.DataFrame:
    return dictionary.filter(pl.col("field_path").str.starts_with("customFields.")).with_columns(
        pl.col("field_path").str.split(".").list.get(1).alias("namespace")
    ).select("object", "namespace", "field_path", "label", "oracle_type", "is_menu", "max_length",
             "description", "suggested_sf_type")


def picklist_values(picklists: pl.DataFrame) -> pl.DataFrame:
    people = pl.lit(False)
    for obj, field in PEOPLE_VALUE_LISTS:
        people = people | ((pl.col("object") == obj) & (pl.col("field_or_object") == field))
    return picklists.filter(~people)


def service_menus(picklists: pl.DataFrame) -> pl.DataFrame:
    return picklists.filter(pl.col("object").is_in(SERVICE_MENUS)).select(
        pl.col("object").alias("menu"), "id", "lookup_name", "parent", "hierarchy_path", "visible_interfaces", "display_order"
    )


def standard_content_index(extract_dir: Path) -> pl.DataFrame:
    """Index columns only. contentValues is read for its content types; its text is never touched."""
    names = _interface_names(extract_dir)
    rows = []
    for r in _read(extract_dir, "config-rows/standardContents.json"):
        folder = r.get("folder") or {}
        path = [p.get("lookupName", "") for p in folder.get("parents", []) if isinstance(p, dict)]
        path.append(folder.get("lookupName", ""))
        types = sorted({(v.get("contentType") or {}).get("lookupName", "") if isinstance(v.get("contentType"), dict)
                        else str(v.get("contentType", "")) for v in r.get("contentValues", []) if isinstance(v, dict)})
        usage = r.get("usage") or {}
        rows.append({
            "id": r.get("id"),
            "name": r.get("lookupName"),
            "folder_path": " > ".join(p for p in path if p),
            "hot_key": r.get("hotKey"),
            "content_types": ", ".join(t for t in types if t),
            "has_html": any("html" in t.lower() for t in types),
            "used_in_inquiry_text": usage.get("incidentText"),
            "used_in_chat_text": usage.get("chatText"),
            "used_as_chat_url": usage.get("chatURL"),
            "used_in_rule_text": usage.get("ruleText"),
            "visible_interfaces": _interface_list(r.get("adminVisibleInterfaces"), names),
        })
    return _frame(rows, {
        "id": pl.Int64, "name": pl.String, "folder_path": pl.String, "hot_key": pl.String, "content_types": pl.String,
        "has_html": pl.Boolean, "used_in_inquiry_text": pl.Boolean, "used_in_chat_text": pl.Boolean,
        "used_as_chat_url": pl.Boolean, "used_in_rule_text": pl.Boolean, "visible_interfaces": pl.String,
    })


def reports(extract_dir: Path) -> pl.DataFrame:
    """Every report in the listing. Dates come from the listing, which was pulled before any definition."""
    defs = {}
    for path in (extract_dir / "report-defs").glob("*.full.json") if (extract_dir / "report-defs").exists() else []:
        d = _load(path)
        if isinstance(d, dict) and "id" in d:
            defs[d["id"]] = d
    rows = []
    for r in _read(extract_dir, "menus/analyticsReports.json"):
        d = defs.get(r.get("id"))
        rows.append({
            "id": r.get("id"),
            "name": r.get("lookupName"),
            "kind": "custom" if (r.get("id") or 0) >= CUSTOM_REPORT_MIN_ID else "Oracle stock",
            "created": (r.get("createdTime") or "")[:10] or None,
            "updated": (r.get("updatedTime") or "")[:10] or None,
            "definition_pulled": d is not None,
            "columns": len(d.get("columns", [])) if d else None,
            "filters": len(d.get("filters", [])) if d else None,
            "definition_date_changed_by_pull": bool(d) and (d.get("updatedTime") or "") > (r.get("updatedTime") or ""),
        })
    return _frame(rows, {
        "id": pl.Int64, "name": pl.String, "kind": pl.String, "created": pl.String, "updated": pl.String,
        "definition_pulled": pl.Boolean, "columns": pl.Int64, "filters": pl.Int64,
        "definition_date_changed_by_pull": pl.Boolean,
    })


def build(extract_dir: Path) -> dict[str, pl.DataFrame]:
    for name in ("data-dictionary.parquet", "picklist-values.parquet"):
        if not (extract_dir / name).exists():
            raise SystemExit(f"{name} missing in {extract_dir}. Run build_data_dictionary.py first.")
    dictionary = pl.read_parquet(extract_dir / "data-dictionary.parquet")
    picklists = pl.read_parquet(extract_dir / "picklist-values.parquet")
    return {
        "Mailboxes": mailboxes(extract_dir),
        "Queues": queues(extract_dir),
        "Chat queues": _id_name(extract_dir, "named-ids/incidents.chatQueue.json"),
        "Profiles": profiles(extract_dir),
        "Staff groups": _id_name(extract_dir, "menus/accountGroups.json"),
        "Channels": channels(extract_dir),
        "Statuses": statuses(extract_dir),
        "Custom objects": custom_objects(extract_dir, dictionary),
        "Custom fields": custom_fields(dictionary),
        "Data dictionary": dictionary,
        "Picklist values": picklist_values(picklists),
        "Products categories dispositions": service_menus(picklists),
        "Standard content index": standard_content_index(extract_dir),
        "Surveys": _id_name(extract_dir, "named-ids/tasks.marketingSettings.survey.json"),
        "Reports": reports(extract_dir),
        "Holidays": _id_name(extract_dir, "menus/holidays.json"),
    }


def summary(tabs: dict[str, pl.DataFrame]) -> pl.DataFrame:
    q, p, r, s = tabs["Queues"], tabs["Profiles"], tabs["Reports"], tabs["Statuses"]
    rows = [
        ("Mailboxes", tabs["Mailboxes"].height),
        ("Queues, named", q.filter(~pl.col("is_separator")).height),
        ("Queues, separator rows", q.filter(pl.col("is_separator")).height),
        ("Chat queues", tabs["Chat queues"].height),
        ("Profiles", p.height),
        ("Profiles named as test, UAT or a copy", p.filter(pl.col("test_or_uat_by_name")).height),
        ("Staff groups", tabs["Staff groups"].height),
        ("Site interfaces", tabs["Channels"].filter(pl.col("list") == "Site interface").height),
        ("Statuses (inquiry, task, answer)", s.height),
        ("Statuses that are placeholders", s.filter(pl.col("is_placeholder")).height),
        ("Custom objects", tabs["Custom objects"].height),
        ("Custom objects holding data", tabs["Custom objects"].filter(pl.col("kind") == "data").height),
        ("Custom fields", tabs["Custom fields"].height),
        ("Data dictionary rows", tabs["Data dictionary"].height),
        ("Picklists listed", tabs["Picklist values"].select("object", "field_or_object").unique().height),
        ("Picklist values listed", tabs["Picklist values"].height),
        ("Products, categories, dispositions", tabs["Products categories dispositions"].height),
        ("Standard content items", tabs["Standard content index"].height),
        ("Surveys", tabs["Surveys"].height),
        ("Reports", r.height),
        ("Reports, Oracle stock", r.filter(pl.col("kind") == "Oracle stock").height),
        ("Reports, custom", r.filter(pl.col("kind") == "custom").height),
        ("Reports with a pulled definition", r.filter(pl.col("definition_pulled")).height),
        ("Holidays", tabs["Holidays"].height),
    ]
    return pl.DataFrame(rows, schema={"item": pl.String, "count": pl.Int64}, orient="row")


def about(extract_dir: Path, tabs: dict[str, pl.DataFrame], picklists: pl.DataFrame) -> pl.DataFrame:
    scope = _load(extract_dir / "_scope.json") if (extract_dir / "_scope.json").exists() else {}
    held_back = [
        f"{field}: {picklists.filter((pl.col('object') == obj) & (pl.col('field_or_object') == field)).height} values, staff names, not listed"
        for obj, field in sorted(PEOPLE_VALUE_LISTS)
    ]
    rows = [
        ("Source", f"Oracle Service Cloud test instance, {scope.get('site', 'site not recorded')}"),
        ("Extract folder", extract_dir.name),
        ("Generated", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")),
        ("What this is", "Configuration and metadata lists. No records. Built by build_config_inventory.py"),
        ("Rebuild", "python3 oracle/tools/build_config_inventory.py " + extract_dir.name),
        ("Not included", "Standard content reply text; staff accounts; rows of data objects; report results"),
        *[("Held back", line) for line in held_back],
        ("Report dates", "Created and updated dates come from the report listing. Reports flagged "
                         "definition_date_changed_by_pull show a later date on their definition, set when the "
                         "definition was read on the pull date; the listing date is the meaningful one"),
        ("Inferred columns", "Queues.section counts the groups between Oracle's separator rows. "
                             "Profiles.test_or_uat_by_name reads the profile name only"),
        *[(f"Tab: {name}", f"{df.height} rows") for name, df in tabs.items()],
    ]
    return pl.DataFrame(rows, schema={"item": pl.String, "value": pl.String}, orient="row")


def write_workbook(extract_dir: Path, tabs: dict[str, pl.DataFrame], out_path: Path | None = None) -> Path:
    picklists = pl.read_parquet(extract_dir / "picklist-values.parquet")
    out_path = out_path or extract_dir / f"oracle-config-inventory-{extract_dir.name}.xlsx"
    sheets = {"About": about(extract_dir, tabs, picklists), "Summary": summary(tabs), **tabs}
    with xlsxwriter.Workbook(str(out_path)) as wb:
        for name, df in sheets.items():
            df.write_excel(workbook=wb, worksheet=name[:31], autofit=True, autofilter=True, freeze_panes=(1, 0),
                           table_style="Table Style Light 9")
    return out_path


def main(argv: list[str]) -> int:
    extract_dir = Path(argv[1]) if len(argv) > 1 else newest_extract_dir()
    tabs = build(extract_dir)
    out = write_workbook(extract_dir, tabs)
    with pl.Config(tbl_rows=-1):
        print(summary(tabs))
    print(f"Workbook: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

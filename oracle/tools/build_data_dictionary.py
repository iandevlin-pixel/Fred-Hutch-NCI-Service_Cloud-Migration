"""Build the data dictionary and the picklist value list from a pulled extract folder.

Reads schema/<resource>.json, named-ids/*.json, menu-objects/*.json and menus/*.json under
the newest (or a named) extract folder. Nothing here touches the network.

Outputs, next to the schemas, as Parquet plus a CSV for review:

    data-dictionary   one row per field: object, field_path, classification, oracle_type,
                      oracle_format, max_length, read_only, lookup_target, menu_source,
                      description, suggested_sf_type, note
    picklist-values   one row per picklist entry: source, object, field_or_object, id,
                      lookup_name, parent, display_order

Custom fields in the Connect REST API sit under customFields.c (legacy custom fields) and
customFields.<package> (custom attributes). The walker descends into both and labels the rows.

Usage:

    python3 oracle/tools/build_data_dictionary.py [extract-folder]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator

import polars as pl

TOOLS_DIR = Path(__file__).resolve().parent
EXTRACTS_DIR = TOOLS_DIR.parent / "extracts" / "oracle-metadata"

COLUMNS = [
    "object",
    "field_path",
    "label",
    "classification",
    "is_menu",
    "oracle_type",
    "oracle_format",
    "max_length",
    "read_only",
    "lookup_target",
    "menu_source",
    "description",
    "suggested_sf_type",
    "note",
]

PICKLIST_COLUMNS = [
    "source", "object", "field_or_object", "id", "lookup_name", "parent", "display_order",
    "hierarchy_path", "visible_interfaces",
]

# Menu resources whose full rows (config-rows/<name>.json) carry parent and interface visibility.
# When present they replace the flat listing in menus/<name>.json.
HIERARCHICAL_MENUS = ("serviceProducts", "serviceCategories", "serviceDispositions")

EXPAND_INLINE = {"statusWithType", "customFields", "c"}


def suggest_sf_type(oracle_type: str, oracle_format: str, max_length: int | None, lookup_target: str) -> str:
    t = (oracle_type or "").lower()
    f = (oracle_format or "").lower()
    if lookup_target:
        if lookup_target.lower().startswith("namedid") or "menu" in lookup_target.lower():
            return "Picklist"
        return "Lookup"
    if t == "boolean":
        return "Checkbox"
    if t in ("integer", "number"):
        return "Number"
    if f == "date-time":
        return "Date/Time"
    if f == "date":
        return "Date"
    if t == "string":
        if max_length is None:
            return "Text Area (Long) or Rich Text; confirm"
        if max_length > 255:
            return "Text Area (Long)"
        return f"Text({max_length})"
    if t == "object":
        return "Structured; see child rows"
    if t == "array":
        return "Related list or multi-select; confirm"
    return "Confirm"


def _ref_target(ref: str) -> str:
    return ref.rstrip("/").rsplit("/", 1)[-1] if ref else ""


def _resolve_local_ref(schema_root: dict[str, Any], ref: str) -> dict[str, Any] | None:
    if not ref.startswith("#/"):
        return None
    node: Any = schema_root
    for part in ref[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, dict) else None


def _menu_source(obj_name: str, path: str, lookup_target: str) -> str:
    """Where a menu field's values come from, matching the pull's file naming."""
    if lookup_target.lower().startswith("namedid"):
        top = path.split(".", 1)[0]
        return f"namedIDs/{obj_name}/{top}"
    if lookup_target and "." in lookup_target:
        return f"menu-object/{lookup_target}"
    return ""


def walk_properties(
    obj_name: str,
    props: dict[str, Any],
    schema_root: dict[str, Any],
    prefix: str = "",
    classification: str = "standard",
    depth: int = 0,
) -> Iterator[dict[str, Any]]:
    for name, spec in props.items():
        if not isinstance(spec, dict):
            continue
        path = f"{prefix}.{name}" if prefix else name

        if name == "customFields" and isinstance(spec.get("properties"), dict):
            for ns, ns_spec in spec["properties"].items():
                ns_props = ns_spec.get("properties") if isinstance(ns_spec, dict) else None
                if isinstance(ns_props, dict):
                    label = "custom (c)" if ns == "c" else f"custom attribute ({ns})"
                    yield from walk_properties(obj_name, ns_props, schema_root, f"{path}.{ns}", label, depth + 1)
                else:
                    yield _row(obj_name, f"{path}.{ns}", "custom (unparsed)", ns_spec if isinstance(ns_spec, dict) else {}, "container without properties; inspect raw schema")
            continue

        ref = spec.get("$ref", "")
        lookup_target = _ref_target(ref)
        resolved = _resolve_local_ref(schema_root, ref) if ref else None
        if resolved is not None and isinstance(resolved.get("properties"), dict) and depth < 4:
            yield from walk_properties(obj_name, resolved["properties"], schema_root, path, classification, depth + 1)
            continue

        child_props = spec.get("properties")
        if isinstance(child_props, dict) and depth < 4 and (name in EXPAND_INLINE or spec.get("type") == "object"):
            yield from walk_properties(obj_name, child_props, schema_root, path, classification, depth + 1)
            continue

        yield _row(obj_name, path, classification, spec, "", lookup_target)


def _row(obj_name: str, path: str, classification: str, spec: dict[str, Any], note: str, lookup_target: str = "") -> dict[str, Any]:
    oracle_type = spec.get("type", "")
    if isinstance(oracle_type, list):
        non_null = [str(t) for t in oracle_type if t != "null"]
        oracle_type = non_null[0] if len(non_null) == 1 else "|".join(non_null)
    oracle_format = spec.get("format", "")
    # Oracle marks dates with bounds, not a JSON Schema format.
    if not oracle_format:
        if "minimumDateTime" in spec or "maximumDateTime" in spec:
            oracle_format = "date-time"
        elif "minimumDate" in spec or "maximumDate" in spec:
            oracle_format = "date"
    max_length = spec.get("maxLength")
    if isinstance(max_length, str) and max_length.isdigit():
        max_length = int(max_length)
    if not isinstance(max_length, int):
        max_length = None
    read_only = bool(spec.get("readOnly", False)) or spec.get("isAvailableForPATCH") is False
    # Oracle marks yes/no fields enumerable too; those are checkboxes, not picklists.
    # A reference to staff accounts is a user lookup, not a picklist.
    is_menu = (bool(spec.get("isEnumerable", False)) and str(oracle_type) != "boolean"
               and _ref_target(spec.get("$ref", "")) != "accounts" and path != "id")
    if not lookup_target and isinstance(spec.get("items"), dict):
        lookup_target = _ref_target(spec["items"].get("$ref", ""))
    suggested = suggest_sf_type(str(oracle_type), str(oracle_format), max_length, lookup_target)
    if is_menu:
        suggested = "Picklist"
    elif lookup_target == "accounts":
        suggested = "Lookup(User)"
    return {
        "object": obj_name,
        "field_path": path,
        "label": str(spec.get("label", "")),
        "classification": classification,
        "is_menu": is_menu,
        "oracle_type": str(oracle_type),
        "oracle_format": str(oracle_format),
        "max_length": max_length,
        "read_only": read_only,
        "lookup_target": lookup_target,
        "menu_source": "",  # set in build() only when an option list was actually saved
        "description": str(spec.get("description", "") or spec.get("title", "")),
        "suggested_sf_type": suggested,
        "note": note,
    }


def _schema_properties(schema: dict[str, Any]) -> dict[str, Any] | None:
    sr = (schema.get("definitions") or {}).get("singularResource")
    if isinstance(sr, dict):
        schema = sr
    if isinstance(schema.get("properties"), dict):
        return schema["properties"]
    merged: dict[str, Any] = {}
    for part in schema.get("allOf", []) or []:
        if isinstance(part, dict) and isinstance(part.get("properties"), dict):
            merged.update(part["properties"])
    return merged or None


def rows_for_schema(obj_name: str, schema: dict[str, Any]) -> list[dict[str, Any]]:
    props = _schema_properties(schema)
    if not props:
        return [_row(obj_name, "", "unparsed", {}, "schema has no top-level properties; inspect raw file")]
    return list(walk_properties(obj_name, props, schema))


def _split_subtype_stem(stem: str) -> tuple[str, str]:
    """'incidents.statusWithType' -> ('incidents', 'statusWithType').
    'SCIF.SCIF.Notes' -> ('SCIF.SCIF', 'Notes'). Custom objects keep their package prefix."""
    parts = stem.split(".")
    if len(parts) >= 3 and parts[0][:1].isupper():  # Package.Object.sub...
        return f"{parts[0]}.{parts[1]}", ".".join(parts[2:])
    if len(parts) >= 2:
        return parts[0], ".".join(parts[1:])
    return "", ""


def build(extract_dir: Path) -> pl.DataFrame:
    schema_dir = extract_dir / "schema"
    rows: list[dict[str, Any]] = []
    for path in sorted(schema_dir.glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            rows.append(_row(path.stem, "", "unparsed", {}, "file is not JSON"))
            continue
        if not isinstance(schema, dict):
            rows.append(_row(path.stem, "", "unparsed", {}, "schema root is not an object"))
            continue
        rows.extend(rows_for_schema(path.stem, schema))
    # Custom field definitions fetched separately: schema-sub/<res>.customFields.<ns>.json
    for path in sorted((extract_dir / "schema-sub").glob("*.customFields.*.json")):
        res, _, ns = path.stem.split(".", 2)
        sub = _load(path)
        props = sub.get("properties") if isinstance(sub, dict) else None
        if not isinstance(props, dict):
            continue
        label = "custom (c)" if ns == "c" else f"custom attribute ({ns})"
        for field, spec in props.items():
            if isinstance(spec, dict):
                ref = _ref_target(spec.get("$ref", ""))
                # a custom menu's $ref points at its own definition; only a reference elsewhere is a lookup
                target = "" if ref == field else ref
                rows.append(_row(res, f"customFields.{ns}.{field}", label, spec, "", target))
    # Nested sub-type schemas: schema-sub/<object>.<sub>[.<sub2>].json (not customFields).
    # Each replaces the single "structured" row for that field with one row per sub-field.
    expanded: set[tuple[str, str]] = set()
    for path in sorted((extract_dir / "schema-sub").glob("*.json"), key=lambda p: p.stem.count(".")):
        if ".customFields" in path.stem:
            continue
        obj, prefix = _split_subtype_stem(path.stem)
        if not obj:
            continue
        sub = _load(path)
        props = _schema_properties(sub) if isinstance(sub, dict) else None
        if not props:
            continue
        expanded.add((obj, prefix))
        for field, spec in props.items():
            if not isinstance(spec, dict):
                continue
            fp = f"{prefix}.{field}"
            if (obj, fp) in expanded:
                continue
            rows.append(_row(obj, fp, "standard", spec, "", _ref_target(spec.get("$ref", ""))))
    rows = [r for r in rows if (r["object"], r["field_path"]) not in expanded]
    # drop sub-type rows that a deeper sub-type file expanded further
    rows = [r for r in rows if r["field_path"] != "customFields"]

    # Point every menu field at its saved option list. Exact matches only, in this order:
    # named-ID file for the field, nested named-ID files under a structured field, a menu
    # resource or hierarchy the field references, a menu-only custom object it references.
    option_files = {p.stem for p in (extract_dir / "named-ids").glob("*.json") if not p.name.startswith("_")}
    menu_objects = {p.stem for p in (extract_dir / "menu-objects").glob("*.json")}
    menu_resources = {p.stem for p in (extract_dir / "menus").glob("*.json")} - {"analyticsReports"}
    for r in rows:
        obj, path, target = r["object"], r["field_path"], r["lookup_target"]
        stem = f"{obj}.{path}"
        nested = sorted(f for f in option_files if f.startswith(stem + ".")) if not path.startswith("customFields.") else []
        if stem in option_files:
            r["menu_source"] = f"named-ids/{stem}"
        elif nested and (r["is_menu"] or r["oracle_type"] == "object"):
            r["menu_source"] = "named-ids/" + ", named-ids/".join(nested)
        elif target in menu_resources:
            r["menu_source"] = f"menus/{target}"
        elif f"hierarchy.{obj}.{target}" in option_files:
            r["menu_source"] = f"named-ids/hierarchy.{obj}.{target}"
        elif target in menu_objects:
            r["menu_source"] = f"menu-objects/{target}"
        if r["menu_source"]:
            r["is_menu"] = True
            r["suggested_sf_type"] = "Picklist"

    if not rows:
        return pl.DataFrame({c: [] for c in COLUMNS})
    return pl.DataFrame(rows, schema_overrides={"max_length": pl.Int64}).select(COLUMNS)


def _picklist_rows_from_items(source: str, obj: str, field: str, items: list) -> Iterator[dict[str, Any]]:
    for it in items:
        if not isinstance(it, dict):
            continue
        parents = it.get("parents")
        name = str(it.get("lookupName", it.get("name", "")))
        parent, path = "", ""
        if isinstance(parents, list):
            # Resolved hierarchy value: ancestors listed root first (hierarchy-parents component).
            names = [str(p.get("lookupName", p.get("id", ""))) if isinstance(p, dict) else str(p) for p in parents]
            parent = names[-1] if names else ""
            path = " > ".join(names + [name])
        elif isinstance(it.get("parent"), dict):
            parent = str(it["parent"].get("lookupName", it["parent"].get("id", "")))
        yield {
            "source": source,
            "object": obj,
            "field_or_object": field,
            "id": it.get("id"),
            "lookup_name": name,
            "parent": parent,
            "display_order": it.get("displayOrder"),
            "hierarchy_path": path,
            "visible_interfaces": "",
        }


def _load_optional(path: Path) -> Any:
    return _load(path) if path.exists() else None


def _interface_names(extract_dir: Path) -> dict[int, str]:
    body = _load_optional(extract_dir / "menus" / "siteInterfaces.json")
    items = body.get("items", []) if isinstance(body, dict) else []
    return {it["id"]: str(it.get("lookupName", it["id"])) for it in items if isinstance(it, dict) and "id" in it}


def _interface_ids(value: Any) -> list[int]:
    """Interface IDs from an expanded adminVisibleInterfaces list. Each item is a link ending in the ID."""
    items = value.get("items", []) if isinstance(value, dict) else []
    ids: list[int] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        if isinstance(it.get("id"), int):
            ids.append(it["id"])
        elif isinstance(it.get("href"), str) and it["href"].rsplit("/", 1)[-1].isdigit():
            ids.append(int(it["href"].rsplit("/", 1)[-1]))
    return sorted(ids)


def _hierarchical_menu_rows(name: str, rows: list, iface_names: dict[int, str]) -> Iterator[dict[str, Any]]:
    """Picklist rows for a product, category or disposition tree, with parent and full path."""
    by_id = {r["id"]: r for r in rows if isinstance(r, dict) and "id" in r}

    def parent_id(r: dict) -> Any:
        p = r.get("parent")
        return p.get("id") if isinstance(p, dict) else None

    for r in by_id.values():
        chain = [str(r.get("lookupName", r["id"]))]
        seen = {r["id"]}
        pid = parent_id(r)
        while pid is not None and pid in by_id and pid not in seen:  # guard against cycles
            seen.add(pid)
            chain.append(str(by_id[pid].get("lookupName", pid)))
            pid = parent_id(by_id[pid])
        parent = r.get("parent")
        yield {
            "source": "resource",
            "object": name,
            "field_or_object": name,
            "id": r["id"],
            "lookup_name": chain[0],
            "parent": str(parent.get("lookupName", parent.get("id", ""))) if isinstance(parent, dict) else "",
            "display_order": r.get("displayOrder"),
            "hierarchy_path": " > ".join(reversed(chain)),
            "visible_interfaces": ", ".join(iface_names.get(i, str(i)) for i in _interface_ids(r.get("adminVisibleInterfaces"))),
        }


def build_picklists(extract_dir: Path) -> pl.DataFrame:
    rows: list[dict[str, Any]] = []

    for path in sorted((extract_dir / "named-ids").glob("*.json")):
        if path.name.startswith("_"):
            continue
        body = _load(path)
        items = body.get("items", []) if isinstance(body, dict) else []
        stem = path.stem
        if not items:
            continue  # listing of sub-menus, no options of its own
        if stem.startswith("hierarchy."):
            _, obj, field = stem.split(".", 2)
            rows.extend(_picklist_rows_from_items("namedIDHierarchy", obj, field, items))
        else:
            obj, field = stem.split(".", 1)
            source = "customMenu" if field.startswith("customFields.") else "namedID"
            rows.extend(_picklist_rows_from_items(source, obj, field, items))

    for path in sorted((extract_dir / "menu-objects").glob("*.json")):
        body = _load(path)
        items = body.get("items", []) if isinstance(body, dict) else []
        rows.extend(_picklist_rows_from_items("menuObject", path.stem, path.stem, items))

    iface_names = _interface_names(extract_dir)
    for path in sorted((extract_dir / "menus").glob("*.json")):
        if path.stem in ("analyticsReports",):
            continue  # report definitions are not picklist values
        full = _load_optional(extract_dir / "config-rows" / f"{path.stem}.json") if path.stem in HIERARCHICAL_MENUS else None
        if isinstance(full, list) and full:
            rows.extend(_hierarchical_menu_rows(path.stem, full, iface_names))
            continue
        body = _load(path)
        items = body.get("items", []) if isinstance(body, dict) else []
        rows.extend(_picklist_rows_from_items("resource", path.stem, path.stem, items))

    if not rows:
        return pl.DataFrame({c: [] for c in PICKLIST_COLUMNS})
    return pl.DataFrame(rows, schema_overrides={"id": pl.Int64, "display_order": pl.Int64}).select(PICKLIST_COLUMNS)


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def newest_extract_dir() -> Path:
    candidates = sorted(p for p in EXTRACTS_DIR.glob("*") if p.is_dir())
    if not candidates:
        raise SystemExit(f"No extract folders under {EXTRACTS_DIR}. Run pull_metadata.py first.")
    return candidates[-1]


def main(argv: list[str]) -> int:
    extract_dir = Path(argv[1]) if len(argv) > 1 else newest_extract_dir()
    df = build(extract_dir)
    df.write_parquet(extract_dir / "data-dictionary.parquet")
    df.write_csv(extract_dir / "data-dictionary.csv")
    kinds: dict[str, str] = {}
    scope_path = extract_dir / "_scope.json"
    if scope_path.exists():
        kinds = _load(scope_path).get("custom_object_classification", {}) or {}
    summary = (
        df.group_by("object", "classification")
        .agg(pl.len().alias("fields"))
        .with_columns(pl.col("object").replace_strict(kinds, default="").alias("custom_object_kind"))
        .sort("object", "classification")
    )
    print(summary)
    print(f"Fields: {df.height}")

    pk = build_picklists(extract_dir)
    pk.write_parquet(extract_dir / "picklist-values.parquet")
    pk.write_csv(extract_dir / "picklist-values.csv")
    if pk.height:
        print(pk.group_by("source", "object", "field_or_object").agg(pl.len().alias("values")).sort("source", "object", "field_or_object"))
    print(f"Picklist values: {pk.height}")
    print(f"Outputs in {extract_dir}: data-dictionary.parquet/.csv, picklist-values.parquet/.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

"""The metadata components of the Oracle pull, one registered function each.

A component pulls one kind of metadata into the dated extract folder. Components talk to
each other only through files in that folder, never through memory, so any component can run
on its own against a folder an earlier run left behind (pull_metadata.py --only / --into).

Adding a component:

1. Write a function taking a Context and decorate it with @component(name, description,
   depends_on=..., done=...). Registration order is run order, so place it after the
   components it depends on.
2. If it requests an Oracle resource the client does not already allow, add that resource to
   ALLOWED_EXACT in osvc_client.py with a note on what it returns. The allowlist is the safety
   rule: a component can never reach a resource the client refuses.
3. Add a test in tests/test_tools.py.

Nothing here requests caller, staff or report rows. analyticsReportResults (which runs a report)
and every record resource are refused by the client before any network call.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from osvc_client import (
    CUSTOM_OBJECT_RE,
    SCHEMA_JSON,
    OsvcClient,
    classify_custom_object,
    diagnose,
    is_people_field,
    non_menu_keys,
    singular_resource,
)

API_MARKER = "/services/rest/connect/v1.4/"

# --- scope constants -------------------------------------------------------------------------

SCHEMA_SCOPE: dict[str, tuple[str, ...]] = {
    "core": (
        "incidents",
        "incidentResponse",
        "tasks",
        "answers",
        "answerVersions",
        "contacts",
        "organizations",
        "accounts",
        "accountGroups",
        "chats",
        "standardContents",
    ),
    "menus": (
        "serviceCategories",
        "serviceDispositions",
        "serviceProducts",
        "namedIDs",
        "namedIDHierarchies",
        "countries",
        "holidays",
        "channelTypes",
        "siteInterfaces",
    ),
    "site_configuration": (
        "configurations",
        "messageBases",
        "variables",
        "mailboxes",
        "serviceMailboxes",
        "analyticsReports",
    ),
}
CUSTOM_PACKAGES: tuple[str, ...] = ("SCIF", "DEMOGR", "Referrals", "OpenMethods")

# Resources whose named-ID menus are read. accounts is included for its own menus
# (for example staff group), with people-typed fields excluded by name.
NAMED_ID_RESOURCES: tuple[str, ...] = (
    "incidents",
    "tasks",
    "answers",
    "contacts",
    "organizations",
    "accounts",
    "chats",
    "standardContents",
)

# Core objects that carry custom fields (legacy "c" fields and package custom attributes).
CUSTOM_FIELD_RESOURCES: tuple[str, ...] = ("incidents", "tasks", "answers", "contacts", "organizations", "accounts")

# Menu structure resources whose rows are configuration values, saved as flat listings.
MENU_ROW_RESOURCES: tuple[str, ...] = (
    "serviceCategories",
    "serviceDispositions",
    "serviceProducts",
    "countries",
    "holidays",
    "channelTypes",
    "siteInterfaces",
    "accountGroups",
)

# Menu resources pulled again as full rows: parent, hierarchy, cross-links, interface visibility.
SERVICE_MENU_RESOURCES: tuple[str, ...] = ("serviceProducts", "serviceCategories", "serviceDispositions")
SERVICE_MENU_EXPAND: frozenset[str] = frozenset({
    "parent", "productHierarchy", "categoryHierarchy", "dispositionHierarchy",
    "categoryLinks", "dispositionLinks", "productLinks", "adminVisibleInterfaces", "endUserVisibleInterfaces",
})

# Report definitions pulled by default: names matching CIS-specific keywords, updated since
# go-live. Report names from 2007 are Oracle's stock reports. Override with --report-ids.
REPORT_KEYWORDS = re.compile(
    r"call ?back|\bcb\b|\bva\b|veteran|quit|smok|tobacco|\bccr\b|survey|sms|text|referral|scif|demog"
    r"|clinical|trial|spanish|retention|\bpii\b|purge|scrub",
    re.I,
)
REPORT_UPDATED_SINCE = "2012"

# Keys dropped from rows before saving: staff account references.
EVENT_SUBSCRIPTION_DROP: frozenset[str] = frozenset({"integrationUser"})


# --- helpers ---------------------------------------------------------------------------------

def resource_names_from_catalog(catalog: object) -> list[str]:
    """Names from the catalog listing (an object with an ``items`` array of ``name`` entries)."""
    names: list[str] = []
    items = []
    if isinstance(catalog, dict):
        items = catalog.get("items") or catalog.get("resources") or []
        if not items and "links" in catalog:
            items = catalog["links"]
    elif isinstance(catalog, list):
        items = catalog
    for item in items:
        if isinstance(item, str):
            names.append(item.rsplit("/", 1)[-1])
        elif isinstance(item, dict):
            name = item.get("name") or item.get("rel") or ""
            href = item.get("href") or ""
            if not name and href:
                name = href.rstrip("/").rsplit("/", 1)[-1]
            if name and name not in ("self", "canonical", "describedby", "alternate", "describes"):
                names.append(name)
    seen: set[str] = set()
    out = []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def field_names_from_named_id_listing(listing: object, resource: str) -> list[str]:
    """Menu field names from a ``namedIDs/<resource>`` listing.

    The listing carries links whose href ends in ``/namedIDs/<resource>/<field>``; some
    sites also include ``items[].name``. Both are read.
    """
    marker = f"/namedIDs/{resource}/"
    found: list[str] = []

    def visit(node: object) -> None:
        if isinstance(node, dict):
            name = node.get("name")
            if isinstance(name, str) and name and "/" not in name and node.get("links") is not None:
                found.append(name)
            href = node.get("href")
            if isinstance(href, str) and marker in href:
                tail = href.split(marker, 1)[1].strip("/")
                if tail and "/" not in tail:
                    found.append(tail)
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)

    visit(listing)
    seen: set[str] = set()
    out = []
    for n in found:
        if n not in seen and n not in ("self", "canonical"):
            seen.add(n)
            out.append(n)
    return out


def safe_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)


def _save(path: Path, body: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2), encoding="utf-8")


def _read(path: Path, default: object = None) -> object:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_menu(path: Path, body: object, errors: dict[str, str], key: str) -> int:
    """Save a menu response only if every option is a plain menu option. Returns option count.

    A response whose options carry any key beyond id, lookupName, parents, display order,
    labels and timestamps is not a menu. It is not saved; only the offending key names are
    recorded, so nothing unexpected is written to disk.
    """
    items = body.get("items") if isinstance(body, dict) else None
    if items is None:
        _save(path, body)  # a listing of sub-menus (links only), no options
        return 0
    bad = non_menu_keys(items)
    if bad:
        errors[key] = f"rejected: options carry non-menu keys {sorted(bad)}; not saved"
        return 0
    _save(path, {"items": items, "hasMore": body.get("hasMore", False)})
    if body.get("hasMore"):
        errors[key] = "hasMore=true: option list may be truncated"
    return len(items)


def load_schemas(out_dir: Path) -> dict[str, object]:
    schemas: dict[str, object] = {}
    for path in sorted((out_dir / "schema").glob("*.json")):
        try:
            schemas[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
    return schemas


def strip_links(value: object) -> object:
    """Drop Oracle's ``links`` keys at every level. Link-only list items (rel/href) are kept."""
    if isinstance(value, dict):
        return {k: strip_links(v) for k, v in value.items() if k != "links"}
    if isinstance(value, list):
        return [strip_links(v) for v in value]
    return value


def _rel(href: str) -> str:
    return href.split(API_MARKER, 1)[1]


def _is_link_only(value: object) -> bool:
    return isinstance(value, dict) and set(value) == {"links"}


def _items(body: object) -> list:
    return body.get("items", []) if isinstance(body, dict) else []


# --- context and registry --------------------------------------------------------------------

class PullStop(Exception):
    """A component found a condition that makes the rest of the run pointless."""


@dataclass
class Context:
    client: OsvcClient
    out_dir: Path
    errors: dict[str, str]
    scope: dict[str, object]
    report_ids: list[int] | None = None

    def listed(self) -> list[str]:
        """Resource names from the saved catalog."""
        return resource_names_from_catalog(_read(self.out_dir / "catalog.json", {}))

    def fail(self, key: str, status: int) -> None:
        self.errors[key] = diagnose(status)


@dataclass(frozen=True)
class Component:
    name: str
    description: str
    run: Callable[[Context], None]
    depends_on: tuple[str, ...] = ()
    done: Callable[[Path, dict], bool] | None = None  # outputs already present from an earlier run


REGISTRY: dict[str, Component] = {}


def component(name: str, description: str, depends_on: tuple[str, ...] = (),
              done: Callable[[Path, dict], bool] | None = None) -> Callable:
    def register(fn: Callable[[Context], None]) -> Callable[[Context], None]:
        missing = [d for d in depends_on if d not in REGISTRY]
        if missing:
            raise ValueError(f"{name} depends on {missing}, which must be registered first")
        REGISTRY[name] = Component(name, description, fn, depends_on, done)
        return fn
    return register


def is_done(comp: Component, out_dir: Path, scope: dict) -> bool:
    runs = scope.get("components_run") or {}
    if comp.name in runs:
        return True
    return bool(comp.done and comp.done(out_dir, scope))


def plan(selected: list[str], out_dir: Path, scope: dict) -> list[str]:
    """Selected components plus any dependency not already satisfied, in registry order.

    A dependency that is already done is not expanded further, so a folder from an earlier run
    can be topped up without refetching what it already holds.
    """
    unknown = [s for s in selected if s not in REGISTRY]
    if unknown:
        raise ValueError(f"Unknown components {unknown}. Known: {list(REGISTRY)}")
    wanted: set[str] = set()

    def add(name: str, explicit: bool) -> None:
        if name in wanted:
            return
        if not explicit and is_done(REGISTRY[name], out_dir, scope):
            return
        wanted.add(name)
        for dep in REGISTRY[name].depends_on:
            add(dep, explicit=False)

    for s in selected:
        add(s, explicit=True)
    return [n for n in REGISTRY if n in wanted]


def run_component(ctx: Context, name: str) -> None:
    REGISTRY[name].run(ctx)
    runs = ctx.scope.setdefault("components_run", {})
    runs[name] = datetime.now(timezone.utc).isoformat(timespec="seconds")


def _exists(*parts: str) -> Callable[[Path, dict], bool]:
    def check(out_dir: Path, scope: dict) -> bool:
        return (out_dir.joinpath(*parts)).exists()
    return check


def _nonempty(folder: str) -> Callable[[Path, dict], bool]:
    def check(out_dir: Path, scope: dict) -> bool:
        return any((out_dir / folder).glob("*.json"))
    return check


def _scope_has(key: str) -> Callable[[Path, dict], bool]:
    def check(out_dir: Path, scope: dict) -> bool:
        return key in scope
    return check


# --- components, in run order ----------------------------------------------------------------

@component("catalog", "Resource listing from metadata-catalog", done=_exists("catalog.json"))
def pull_catalog(ctx: Context) -> None:
    status, catalog = ctx.client.get_json("metadata-catalog")
    _save(ctx.out_dir / "catalog.json", catalog)
    if status != 200:
        raise PullStop(diagnose(status))
    listed = resource_names_from_catalog(catalog)
    if not listed:
        raise PullStop("Catalog returned 200 but no resource names were found; inspect catalog.json.")
    custom = [n for n in listed if CUSTOM_OBJECT_RE.match(n)]
    print(f"Catalog OK. {len(listed)} resources listed, {len(custom)} custom objects.")


def in_scope_custom_objects(names: list[str]) -> list[str]:
    return [n for n in names if CUSTOM_OBJECT_RE.match(n) and n.split(".", 1)[0] in CUSTOM_PACKAGES]


@component("schemas", "JSON Schema for every resource in scope, plus every object in the custom packages",
           depends_on=("catalog",), done=_nonempty("schema"))
def pull_schemas(ctx: Context) -> None:
    listed = ctx.listed()
    wanted = [r for group in SCHEMA_SCOPE.values() for r in group] + in_scope_custom_objects(listed)
    requested = [r for r in wanted if r in listed]
    ctx.scope.update({
        "schemas_requested": requested,
        "schemas_not_listed": [r for r in wanted if r not in listed],
        "schemas_skipped": [r for r in listed if r not in wanted],
    })
    saved = 0
    for name in requested:
        status, schema = ctx.client.get_json(f"metadata-catalog/{name}", accept=SCHEMA_JSON)
        _save(ctx.out_dir / "schema" / f"{safe_filename(name)}.json", schema)
        if status == 200:
            saved += 1
        else:
            ctx.fail(f"metadata-catalog/{name}", status)
    print(f"Schemas saved: {saved} of {len(requested)}")


@component("subtype-schemas", "Schemas of structured sub-types inside each object (statusWithType, threads, ...), 3 levels",
           depends_on=("schemas",), done=_scope_has("subtype_schemas_fetched"))
def subtype_schemas(ctx: Context) -> None:
    pull_subtype_schemas(ctx.client, ctx.out_dir, ctx.errors, ctx.scope)


def pull_subtype_schemas(client: OsvcClient, out_dir: Path, errors: dict[str, str], scope: dict[str, object],
                         max_depth: int = 3) -> None:
    """Schemas for structured sub-types (statusWithType, serviceSettings, name, threads and so on).

    A property is followed only when its $ref points under its own object's catalog entry,
    metadata-catalog/<object>/<property>[/...]. Schema only; no records.
    """
    fetched = 0
    queue: list[tuple[str, str, object]] = [(obj, "", singular_resource(s)) for obj, s in load_schemas(out_dir).items()]
    seen: set[str] = set()
    while queue:
        obj, prefix, node = queue.pop(0)
        props = node.get("properties") if isinstance(node, dict) else None
        if not isinstance(props, dict):
            continue
        base = f"/metadata-catalog/{obj}/" + (prefix.replace(".", "/") + "/" if prefix else "")
        for prop, spec in props.items():
            if not isinstance(spec, dict) or prop == "customFields":
                continue
            ref = spec.get("$ref", "") or ((spec.get("items") or {}).get("$ref", "") if isinstance(spec.get("items"), dict) else "")
            if not ref.endswith(base + prop):
                continue
            rel_path = ref.split(API_MARKER, 1)[-1]
            if rel_path in seen:
                continue
            seen.add(rel_path)
            status, sub = client.get_json(rel_path, accept=SCHEMA_JSON)
            sub_prefix = f"{prefix}.{prop}" if prefix else prop
            _save(out_dir / "schema-sub" / f"{safe_filename(obj)}.{safe_filename(sub_prefix)}.json", sub)
            if status != 200 or not isinstance(sub, dict):
                errors[rel_path] = diagnose(status)
                continue
            fetched += 1
            if sub_prefix.count(".") + 1 < max_depth:
                queue.append((obj, sub_prefix, singular_resource(sub)))
    scope["subtype_schemas_fetched"] = fetched
    print(f"Sub-type schemas saved: {fetched}")


@component("menu-objects", "Rows of custom objects that are menu tables; each object is classified first and data objects are never read",
           depends_on=("schemas",), done=_scope_has("custom_object_classification"))
def pull_menu_objects(ctx: Context) -> None:
    schemas = load_schemas(ctx.out_dir)
    custom = in_scope_custom_objects(list(schemas))
    classification = {name: classify_custom_object(schemas.get(name)) for name in custom}
    ctx.scope["custom_object_classification"] = classification
    print("Custom object classification (rows are requested for 'menu' only):")
    for name, kind in classification.items():
        print(f"  {kind:7}  {name}")
    saved = 0
    for name, kind in classification.items():
        if kind != "menu":
            continue
        ctx.client.approve_menu_object(name)
        status, items, pages = ctx.client.get_all_items(name)
        if status != 200:
            ctx.fail(name, status)
            continue
        bad = non_menu_keys(items)
        if bad:
            ctx.errors[name] = f"rejected: rows carry non-menu keys {sorted(bad)}; not saved"
            continue
        _save(ctx.out_dir / "menu-objects" / f"{safe_filename(name)}.json", {"items": items, "pages": len(pages)})
        saved += 1
    print(f"Menu-object option lists saved: {saved}")


def _named_ids_present(out_dir: Path, scope: dict) -> bool:
    return any(not p.name.startswith(("hierarchy.", "_hierarchy")) for p in (out_dir / "named-ids").glob("*.json"))


@component("named-ids", "Standard menu values per object (named IDs); fields that resolve to people are excluded and printed first",
           depends_on=("catalog",), done=_named_ids_present)
def pull_named_ids(ctx: Context) -> None:
    listed = ctx.listed()
    fields_by_res: dict[str, list[str]] = {}
    excluded: dict[str, list[str]] = {}
    for res in NAMED_ID_RESOURCES:
        if res not in listed:
            continue
        status, listing = ctx.client.get_json(f"namedIDs/{res}")
        _save(ctx.out_dir / "named-ids" / f"_listing.{res}.json", listing)
        if status != 200:
            ctx.fail(f"namedIDs/{res}", status)
            continue
        fields = field_names_from_named_id_listing(listing, res)
        excluded[res] = [f for f in fields if is_people_field(f)]
        fields_by_res[res] = [f for f in fields if not is_people_field(f)]
    ctx.scope["named_id_fields"] = fields_by_res
    ctx.scope["named_id_fields_excluded_people"] = excluded
    print("Named-ID fields excluded because they resolve to people:")
    for res, fields in excluded.items():
        if fields:
            print(f"  {res}: {', '.join(fields)}")
    saved = 0
    for res, fields in fields_by_res.items():
        for fld in fields:
            status, body = ctx.client.get_json(f"namedIDs/{res}/{fld}")
            _save(ctx.out_dir / "named-ids" / f"{res}.{safe_filename(fld)}.json", body)
            if status == 200:
                saved += 1
            else:
                ctx.fail(f"namedIDs/{res}/{fld}", status)
    print(f"Named-ID value lists saved: {saved}")


@component("nested-named-ids", "Standard menus one level down (statusWithType -> status), plus contact type",
           depends_on=("named-ids",), done=_scope_has("nested_named_id_lists_fetched"))
def pull_nested_named_ids(ctx: Context) -> None:
    fetched, options = 0, 0
    ctx.errors.pop("namedIDs/contacts/contactType", None)
    for path in sorted((ctx.out_dir / "named-ids").glob("*.json")):
        stem = path.stem
        if stem.startswith("_") or stem.startswith("hierarchy.") or ".customFields." in stem or stem.count(".") != 1:
            continue
        body = _read(path)
        if not isinstance(body, dict) or "items" in body:
            continue
        res, fld = stem.split(".", 1)
        for sub in body:
            if sub == "links" or is_people_field(sub):
                continue
            key = f"namedIDs/{res}/{fld}/{sub}"
            status, sub_body = ctx.client.get_json(key)
            if status != 200:
                ctx.fail(key, status)
                continue
            options += save_menu(ctx.out_dir / "named-ids" / f"{res}.{safe_filename(fld)}.{safe_filename(sub)}.json", sub_body, ctx.errors, key)
            fetched += 1
    # contactType was excluded by an earlier, broader people rule. It is a menu of contact types.
    status, body = ctx.client.get_json("namedIDs/contacts/contactType")
    if status == 200:
        options += save_menu(ctx.out_dir / "named-ids" / "contacts.contactType.json", body, ctx.errors, "namedIDs/contacts/contactType")
        fetched += 1
    ctx.scope["nested_named_id_lists_fetched"] = fetched
    print(f"Nested standard menu lists saved: {fetched} ({options} options)")


@component("named-id-hierarchies", "Hierarchical standard menus (for example source)",
           depends_on=("catalog",), done=_exists("named-ids", "_hierarchy_listing.incidents.json"))
def pull_named_id_hierarchies(ctx: Context) -> None:
    listed = ctx.listed()
    saved = 0
    for res in NAMED_ID_RESOURCES:
        if res not in listed:
            continue
        status, listing = ctx.client.get_json(f"namedIDHierarchies/{res}")
        _save(ctx.out_dir / "named-ids" / f"_hierarchy_listing.{res}.json", listing)
        if status != 200:
            ctx.fail(f"namedIDHierarchies/{res}", status)
            continue
        fields = [f for f in field_names_from_named_id_listing(listing, res) if not is_people_field(f)]
        if not fields:
            # The hierarchy listing may use the same href shape under /namedIDHierarchies/.
            marker = f"/namedIDHierarchies/{res}/"
            fields = sorted({
                h.split(marker, 1)[1].strip("/")
                for h in re.findall(r'"href":\s*"([^"]+)"', json.dumps(listing))
                if marker in h and "/" not in h.split(marker, 1)[1].strip("/")
            })
            fields = [f for f in fields if not is_people_field(f)]
        for fld in fields:
            status, body = ctx.client.get_json(f"namedIDHierarchies/{res}/{fld}")
            _save(ctx.out_dir / "named-ids" / f"hierarchy.{res}.{safe_filename(fld)}.json", body)
            if status == 200:
                saved += 1
            else:
                ctx.fail(f"namedIDHierarchies/{res}/{fld}", status)
    print(f"Hierarchical menu lists saved: {saved}")


@component("hierarchy-parents", "Ancestors of every hierarchical menu value, written into the hierarchy files; each value is fetched once and reused across objects",
           depends_on=("named-id-hierarchies",), done=_scope_has("hierarchy_parents_fetched"))
def pull_hierarchy_parents(ctx: Context) -> None:
    cache: dict[tuple[str, int], list[dict]] = {}
    fetched = 0
    for path in sorted((ctx.out_dir / "named-ids").glob("hierarchy.*.json")):
        _, res, fld = path.stem.split(".", 2)
        body = _read(path, {})
        items = _items(body)
        for it in items:
            if not isinstance(it, dict) or "id" not in it or isinstance(it.get("parents"), list):
                continue  # already resolved
            key = (fld, it["id"])  # the same field's values are one list across objects
            if key not in cache:
                status, parents = ctx.client.get_json(f"namedIDHierarchies/{res}/{fld}/{it['id']}/parents")
                if status != 200:
                    ctx.fail(f"namedIDHierarchies/{res}/{fld}/{it['id']}/parents", status)
                    continue
                cache[key] = [{"id": p.get("id"), "lookupName": p.get("lookupName")} for p in _items(parents) if isinstance(p, dict)]
                fetched += 1
            it["parents"] = cache[key]
        save_menu(path, {"items": items, "hasMore": body.get("hasMore", False) if isinstance(body, dict) else False},
                  ctx.errors, f"namedIDHierarchies/{res}/{fld}")
    ctx.scope["hierarchy_parents_fetched"] = fetched
    print(f"Hierarchy parents fetched: {fetched} values")


@component("custom-fields", "Custom field definitions per object and namespace, and the options of custom menu fields",
           done=_exists("schema-sub", "incidents.customFields.json"))
def pull_custom_fields(ctx: Context) -> None:
    cf = pull_custom_field_schemas(ctx)
    pull_custom_menu_options(ctx, cf)


def pull_custom_field_schemas(ctx: Context) -> dict[str, dict[str, dict]]:
    """Custom field definitions per resource and namespace. Schema only."""
    result: dict[str, dict[str, dict]] = {}
    for res in CUSTOM_FIELD_RESOURCES:
        status, top = ctx.client.get_json(f"metadata-catalog/{res}/customFields", accept=SCHEMA_JSON)
        _save(ctx.out_dir / "schema-sub" / f"{res}.customFields.json", top)
        if status != 200 or not isinstance(top, dict):
            ctx.fail(f"metadata-catalog/{res}/customFields", status)
            continue
        result[res] = {}
        for ns in (top.get("properties") or {}):
            status, sub = ctx.client.get_json(f"metadata-catalog/{res}/customFields/{ns}", accept=SCHEMA_JSON)
            _save(ctx.out_dir / "schema-sub" / f"{res}.customFields.{safe_filename(ns)}.json", sub)
            if status != 200 or not isinstance(sub, dict):
                ctx.fail(f"metadata-catalog/{res}/customFields/{ns}", status)
                continue
            result[res][ns] = sub.get("properties") or {}
    counts = {res: {ns: len(p) for ns, p in nss.items()} for res, nss in result.items()}
    print(f"Custom field definitions: {counts}")
    return result


def pull_custom_menu_options(ctx: Context, cf: dict[str, dict[str, dict]]) -> None:
    """Option lists for custom menu fields.

    A field is fetched only when it is enumerable and its $ref points at its own customFields
    definition (a menu). A field whose $ref points anywhere else is a relationship to another
    object; its "options" would be that object's records, so it is recorded and skipped.
    """
    fetched, skipped_rel, options = 0, [], 0
    for res, nss in cf.items():
        for ns, props in nss.items():
            for fld, spec in props.items():
                if not isinstance(spec, dict) or not spec.get("isEnumerable"):
                    continue
                if not spec.get("$ref", "").endswith(f"/customFields/{ns}/{fld}"):
                    skipped_rel.append(f"{res}.customFields.{ns}.{fld}")
                    continue
                key = f"namedIDs/{res}/customFields/{ns}/{fld}"
                status, body = ctx.client.get_json(key)
                if status != 200:
                    ctx.fail(key, status)
                    continue
                options += save_menu(ctx.out_dir / "named-ids" / f"{res}.customFields.{ns}.{safe_filename(fld)}.json", body, ctx.errors, key)
                fetched += 1
    ctx.scope["custom_menu_fields_fetched"] = fetched
    ctx.scope["custom_enumerable_fields_skipped_as_relationships"] = skipped_rel
    print(f"Custom menu option lists saved: {fetched} ({options} options)")
    if skipped_rel:
        print(f"Skipped as relationships, not menus: {skipped_rel}")


@component("menu-listings", "Flat listings of products, categories, dispositions, countries, holidays, channel types, interfaces and staff group names",
           depends_on=("catalog",), done=_exists("menus", "siteInterfaces.json"))
def pull_menu_listings(ctx: Context) -> None:
    listed = ctx.listed()
    for name in MENU_ROW_RESOURCES:
        if name not in listed:
            continue
        status, items, pages = ctx.client.get_all_items(name)
        _save(ctx.out_dir / "menus" / f"{safe_filename(name)}.json", {"items": items, "pages": len(pages)})
        if status != 200:
            ctx.fail(name, status)


def _fetch_rows(ctx: Context, resource: str, expand: Callable[[str, object], bool],
                drop: frozenset[str] = frozenset()) -> list[dict]:
    """Every row of a configuration resource, with chosen link-only fields fetched one level down."""
    status, items, _ = ctx.client.get_all_items(resource)
    if status != 200:
        ctx.fail(resource, status)
        return []
    rows: list[dict] = []
    for it in items:
        if not isinstance(it, dict) or "id" not in it:
            continue
        status, row = ctx.client.get_json(f"{resource}/{it['id']}")
        if status != 200 or not isinstance(row, dict):
            ctx.fail(f"{resource}/{it['id']}", status)
            continue
        row = {k: v for k, v in row.items() if k not in drop}
        for key, value in list(row.items()):
            if expand(key, value) and _is_link_only(value):
                target = next((l["href"] for l in value["links"] if l.get("rel") in ("self", "canonical")), None)
                if target:
                    s2, body = ctx.client.get_json(_rel(target))
                    row[key] = body if s2 == 200 else {"_status": s2}
        rows.append(row)
    return rows


@component("service-menus", "Products, categories and dispositions as full rows: parent, hierarchy, cross-links, interface visibility",
           depends_on=("menu-listings",), done=_exists("config-rows", "serviceDispositions.json"))
def pull_service_menus(ctx: Context) -> None:
    for resource in SERVICE_MENU_RESOURCES:
        rows = _fetch_rows(ctx, resource, lambda k, v: k in SERVICE_MENU_EXPAND)
        _save(ctx.out_dir / "config-rows" / f"{resource}.json", strip_links(rows))
        print(f"{resource}: {len(rows)} full rows")


@component("report-list", "Names of every report (analyticsReports listing)",
           depends_on=("catalog",), done=_exists("menus", "analyticsReports.json"))
def pull_report_list(ctx: Context) -> None:
    if "analyticsReports" not in ctx.listed():
        return
    status, items, pages = ctx.client.get_all_items("analyticsReports")
    _save(ctx.out_dir / "menus" / "analyticsReports.json", {"items": items, "pages": len(pages)})
    ctx.scope["analyticsReports_status"] = status
    if status != 200:
        ctx.fail("analyticsReports", status)
    print(f"Report list: status {status}, {len(items)} reports.")


def target_reports(listing: object, report_ids: list[int] | None = None) -> list[int]:
    """Report IDs to define: the given IDs, or CIS keyword matches updated since go-live."""
    if report_ids:
        return list(report_ids)
    return [
        it["id"] for it in _items(listing)
        if isinstance(it, dict) and "id" in it
        and REPORT_KEYWORDS.search(str(it.get("lookupName", "")))
        and str(it.get("updatedTime", "")) >= REPORT_UPDATED_SINCE
    ]


@component("report-definitions", "Columns and filters of targeted reports; no report is run",
           depends_on=("report-list",))
def pull_report_definitions(ctx: Context) -> None:
    ids = target_reports(_read(ctx.out_dir / "menus" / "analyticsReports.json", {}), ctx.report_ids)
    out = ctx.out_dir / "report-defs"
    saved = skipped = 0
    for rid in ids:
        path = out / f"{rid}.full.json"
        if path.exists():
            skipped += 1  # resume: an earlier run already saved this one
            continue
        status, head = ctx.client.get_json(f"analyticsReports/{rid}")
        record: dict[str, object] = {"id": rid, "status": status}
        if status == 200 and isinstance(head, dict):
            record.update({k: head.get(k) for k in ("lookupName", "createdTime", "updatedTime")})
            for part in ("columns", "filters"):
                s2, listing = ctx.client.get_json(f"analyticsReports/{rid}/{part}")
                entries = []
                for it in _items(listing):
                    href = it.get("href") if isinstance(it, dict) else None
                    if not href and isinstance(it, dict):
                        href = next((l["href"] for l in it.get("links", []) if l.get("rel") == "canonical"), None)
                    if not href:
                        continue
                    s3, body = ctx.client.get_json(_rel(href))
                    entries.append(strip_links(body) if s3 == 200 else {"_status": s3})
                record[part] = entries
        else:
            ctx.fail(f"analyticsReports/{rid}", status)
        _save(path, record)
        saved += 1
    ctx.scope["report_definitions"] = {
        "selection": "report ids given" if ctx.report_ids else f"keywords, updated since {REPORT_UPDATED_SINCE}",
        "targeted": len(ids), "saved": saved, "already_present": skipped,
    }
    print(f"Report definitions: {len(ids)} targeted, {saved} saved, {skipped} already present.")


@component("mailboxes", "Mailboxes and service mailboxes: name, type, interface, addresses, enabled flags",
           depends_on=("catalog",), done=_exists("config-rows", "serviceMailboxes.json"))
def pull_mailboxes(ctx: Context) -> None:
    for resource in ("mailboxes", "serviceMailboxes"):
        rows = _fetch_rows(ctx, resource, lambda k, v: True)
        _save(ctx.out_dir / "config-rows" / f"{resource}.json", strip_links(rows))
        print(f"{resource}: {len(rows)} rows")


@component("standard-content", "Canned agent replies with folder, usage, interfaces and full text",
           depends_on=("catalog",), done=_exists("config-rows", "standardContents.json"))
def pull_standard_content(ctx: Context) -> None:
    # contentValues resolves to a list of links, one per text version; each is fetched below.
    rows = _fetch_rows(ctx, "standardContents", lambda k, v: True)
    values = 0
    for row in rows:
        cv = row.get("contentValues")
        if isinstance(cv, dict) and _items(cv):
            fetched = []
            for it in _items(cv):
                href = it.get("href") if isinstance(it, dict) else None
                if not href:
                    continue
                status, body = ctx.client.get_json(_rel(href))
                fetched.append(body if status == 200 else {"_status": status})
                values += status == 200
            row["contentValues"] = fetched
    _save(ctx.out_dir / "config-rows" / "standardContents.json", strip_links(rows))
    print(f"standardContents: {len(rows)} items, {values} text values")


@component("event-subscriptions", "Outbound event notifications; the integration user (a staff account) is dropped",
           depends_on=("catalog",), done=_exists("config-rows", "eventSubscriptions.json"))
def pull_event_subscriptions(ctx: Context) -> None:
    rows = _fetch_rows(ctx, "eventSubscriptions", lambda k, v: True, drop=EVENT_SUBSCRIPTION_DROP)
    _save(ctx.out_dir / "config-rows" / "eventSubscriptions.json", strip_links(rows))
    print(f"eventSubscriptions: {len(rows)} rows")


# Menu fields on configuration resources whose schemas point at a named-ID list. Found in the
# schemas pulled 2026-09-23 (metadata-catalog/namedIDs/<resource>/<path> links). Staff references
# are listed separately and never fetched.
CONFIG_NAMED_ID_LISTS: tuple[str, ...] = (
    "configurations/dataType",
    "messageBases/usage",
    "mailboxes/type",
    "serviceMailboxes/type",
    "eventSubscriptions/eventType",
    "eventSubscriptions/status",
    "eventSubscriptions/objectVersion",
    "organizations/salesSettings/totalRevenue/currency",
    "organizations/salesSettings/totalRevenue/exchangeRate",
)
CONFIG_NAMED_ID_PEOPLE: tuple[str, ...] = ("eventSubscriptions/integrationUser",)


@component("config-named-ids", "Menu values for configuration resources (configuration data type, mailbox type, message base usage, event subscription fields, revenue currency); staff references are skipped",
           depends_on=("catalog",), done=_scope_has("config_named_id_lists_fetched"))
def pull_config_named_ids(ctx: Context) -> None:
    print("Skipped because they resolve to staff accounts: " + ", ".join(CONFIG_NAMED_ID_PEOPLE))
    fetched, options = 0, 0
    for rel in CONFIG_NAMED_ID_LISTS:
        assert rel not in CONFIG_NAMED_ID_PEOPLE and not is_people_field(rel.rsplit("/", 1)[1]), rel
        key = f"namedIDs/{rel}"
        status, body = ctx.client.get_json(key)
        if status != 200:
            ctx.fail(key, status)
            continue
        options += save_menu(ctx.out_dir / "named-ids" / f"{safe_filename(rel.replace('/', '.'))}.json", body, ctx.errors, key)
        fetched += 1
    ctx.scope["config_named_id_lists_fetched"] = fetched
    ctx.scope["config_named_id_lists_skipped_people"] = list(CONFIG_NAMED_ID_PEOPLE)
    print(f"Configuration menu lists saved: {fetched} ({options} options)")

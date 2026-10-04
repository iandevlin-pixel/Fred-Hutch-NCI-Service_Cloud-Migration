# Oracle metadata tooling

Pulls the data model and the picklist values of the NCI CIS Oracle Service Cloud test instance (`NCI__TST`) through the Connect REST API, and builds a field-level data dictionary and a picklist value list from them. Schema and configuration values, plus knowledge base answers. Every other record resource is refused in code before any network call.

**Answers are the one record exception** (Ben Bolding, 2026-10-01): the articles are in migration scope and are internal reference content, not caller PII. The constraint is PII. `answers` and `answerVersions` are allowlisted, and `OsvcClient.query_answers()` runs a ROQL query only when it reads the Answer object alone, with no subquery and no reach into incidents, contacts, accounts, chats or other people records. Answer data still lands under `extracts/` and never leaves this machine.

Design: [oracle-to-salesforce-mapping-framework-2026-09-23.md](../../migration/oracle-to-salesforce-mapping-framework-2026-09-23.md), sections 6 and 7.

## Access

| Item | Value |
| --- | --- |
| Site | `https://nci--tst.cx.usg.oraclecloud.com` |
| Account | `sthomas_RNT`, the shared test account. REST access confirmed 2026-09-23 |
| Password | macOS Keychain, service `osvc-nci-tst`. Never in a file, a shell command line, or the chat |
| Timing | Run when nobody is signed in as `sthomas_RNT`. The account allows one session |

## Setup

```bash
cd "/Users/ben/Desktop/Salesforce Projects/Fred_Hutch"
export OSVC_SITE_URL=https://nci--tst.cx.usg.oraclecloud.com
export OSVC_USER=sthomas_RNT
security add-generic-password -a "$USER" -s osvc-nci-tst -w   # once; prompts for the password
```

## Run

The pull is a set of **components**, one per kind of metadata, defined in [components.py](components.py). [pull_metadata.py](pull_metadata.py) is the runner.

```bash
python3 oracle/tools/pull_metadata.py --list   # the components and what each pulls
python3 oracle/tools/pull_metadata.py --test   # catalog listing only
python3 oracle/tools/pull_metadata.py          # every component, into today's folder
python3 oracle/tools/pull_metadata.py --only mailboxes,standard-content
python3 oracle/tools/pull_metadata.py --only report-definitions --into 2026-09-23 --report-ids 101125,101126
python3 oracle/tools/build_data_dictionary.py  # dictionary and picklists
python3 oracle/tools/build_config_inventory.py # the team workbook; run after the dictionary
```

| Option | Effect |
| --- | --- |
| `--only A,B` | Run these components. Any dependency the folder does not already hold runs first |
| `--into YYYY-MM-DD` | Add to that existing extract folder instead of today's |
| `--report-ids ID,ID` | Define these reports instead of the default targeting (CIS keywords, updated since 2012) |
| `--topup`, `--subtypes` | Older shortcuts, kept: `--only menu-objects,subtype-schemas,custom-fields,nested-named-ids` and `--only subtype-schemas`, each with `--into` |

A selected component always runs. A dependency is skipped when the folder already holds its output, either recorded under `components_run` in `_scope.json` or detected from its files. Report definitions resume: a report already saved is not requested again.

| Component | Pulls | Needs |
| --- | --- | --- |
| `catalog` | Resource listing | |
| `schemas` | JSON Schema for each resource in scope and every custom package object | catalog |
| `subtype-schemas` | Nested object schemas, three levels | schemas |
| `menu-objects` | Rows of menu-only custom objects, classified first | schemas |
| `named-ids` | Standard menu values; people fields excluded | catalog |
| `nested-named-ids` | Standard menus one level down, plus contact type | named-ids |
| `named-id-hierarchies` | Hierarchical standard menus | catalog |
| `hierarchy-parents` | Ancestors of each hierarchical menu value, written into the hierarchy files. Fetched once per value and reused across objects | named-id-hierarchies |
| `custom-fields` | Custom field definitions and custom menu options | |
| `menu-listings` | Flat lists of products, categories, dispositions, countries, holidays, channel types, interfaces, staff groups | catalog |
| `service-menus` | Products, categories, dispositions as full rows: parent, hierarchy, cross-links, interfaces | menu-listings |
| `report-list` | Every report name | catalog |
| `report-definitions` | Columns and filters of targeted reports | report-list |
| `mailboxes` | Mailboxes and service mailboxes | catalog |
| `standard-content` | Canned replies with full text | catalog |
| `event-subscriptions` | Outbound event notifications, integration user dropped | catalog |
| `config-named-ids` | Menu values for configuration resources: configuration data type, mailbox and service mailbox type, message base usage, event subscription type, status and version, revenue currency. The event subscription integration user (a staff account) is skipped. Added 2026-10-02 | catalog |

## Adding a component

1. In [components.py](components.py), write a function that takes a `Context` and decorate it with `@component(name, description, depends_on=..., done=...)`. Place it after the components it depends on; registration order is run order. Read inputs from the extract folder and write outputs to it; components never pass data in memory.
2. If it requests an Oracle resource the client does not yet allow, add that resource to `ALLOWED_EXACT` in [osvc_client.py](osvc_client.py) with a note on what it returns, after checking its schema for credential or people fields. This step is deliberate: the allowlist is what keeps records out, and a component cannot bypass it.
3. Add a test in [tests/test_tools.py](tests/test_tools.py) against a fake server, and a row to the component table above.

## What the pull requests

**Schemas, 47 resources, no records.**

| Group | Resources |
| --- | --- |
| Core and inquiry-related (11) | `incidents`, `incidentResponse`, `tasks`, `answers`, `answerVersions`, `contacts`, `organizations`, `accounts`, `accountGroups`, `chats`, `standardContents` |
| Menus and named IDs (9) | `serviceCategories`, `serviceDispositions`, `serviceProducts`, `namedIDs`, `namedIDHierarchies`, `countries`, `holidays`, `channelTypes`, `siteInterfaces` |
| Site configuration (6) | `configurations`, `messageBases`, `variables`, `mailboxes`, `serviceMailboxes`, `analyticsReports` |
| Custom packages (21) | every object in `SCIF`, `DEMOGR`, `Referrals`, `OpenMethods` |

Not requested: sales, marketing and asset resources, and API plumbing (`bulkExtracts`, `queryResults`, `analyticsReportResults`, `sSOTokenReferences`). `eventSubscriptions` is read by its own component, below.

**Picklist values.** Oracle stores them three ways, and the pull reads each.

| Mechanism | Read with | Output |
| --- | --- | --- |
| Named IDs (standard and custom menu fields) | `namedIDs/<resource>` to list the menu fields, then `namedIDs/<resource>/<field>` | `named-ids/<resource>.<field>.json` |
| Named-ID hierarchies (products, categories, dispositions, source) | `namedIDHierarchies/<resource>/<field>` | `named-ids/hierarchy.<resource>.<field>.json` |
| Custom menu fields (for example `special_code_1`) | `metadata-catalog/<resource>/customFields/<namespace>` for the definitions, then `namedIDs/<resource>/customFields/<namespace>/<field>` for the options. A custom field whose reference points at another object is a relationship and is skipped | `schema-sub/`, `named-ids/<resource>.customFields.<ns>.<field>.json` |
| Menu-only custom objects | The object's rows, only when Oracle flags it `isMenu` and every field is `id`, `lookupName`, `Name`, display order, labels or a timestamp | `menu-objects/<Package.Object>.json` |

Named-ID fields that resolve to people (`assignedTo`, account, contact, organization, created by, updated by, owner) are excluded, and the exclusion prints before any value is fetched. The custom object classification prints before any row is fetched.

**Field definitions versus field values.** A field's definition (name, label, type, length, whether it is a menu) comes from the schema. A menu field's full list of options comes from the named-ID or menu-object endpoints, and is the same for every record. What any given record holds in a field would come only from reading that object's rows, which the client refuses. Every option list is checked before it is saved: an option carrying any key beyond `id`, `lookupName`, `Name`, parents, display order, labels and timestamps is rejected and not written.

**Configuration rows.** `serviceCategories`, `serviceDispositions`, `serviceProducts`, `countries`, `holidays`, `channelTypes`, `siteInterfaces` (menu structure), `accountGroups` (staff group names only), and one attempt at `analyticsReports` (report definitions; `analyticsReportResults`, which runs a report, is refused).

**Added 2026-09-23 on Ben Bolding's direction**, each schema checked for credential fields first:

| Resource | Returns | Notes |
| --- | --- | --- |
| `eventSubscriptions` | Outbound event notifications: name, class, event type, endpoint, status | `integrationUser` is a staff account reference and is dropped before saving |
| `mailboxes`, `serviceMailboxes` | Mailbox name, type, interface, from and reply-to addresses, enabled flags | No password fields exist in the schema |
| `standardContents` | Canned agent replies with folder, usage and text | Mark Hubers cleared pulling standard content |
| `analyticsReports/<id>/columns`, `/filters` | Column headings and filter definitions of a report | Already allowed under `analyticsReports`. No report is run |

These are the `service-menus`, `report-definitions`, `mailboxes`, `standard-content` and `event-subscriptions` components. They write to `config-rows/` and `report-defs/` inside the dated extract folder.

**Never requested.** Rows of `incidents`, `tasks`, `answers`, `contacts`, `organizations`, `accounts`, `chats`, `SCIF.SCIF`, the `Referrals` and `DEMOGR` data objects, `configurations`, `queryResults`, `analyticsReportResults`.

## Output

Everything lands in `oracle/extracts/oracle-metadata/<date>/`, which git ignores.

| File | Contents |
| --- | --- |
| `catalog.json` | The resource listing |
| `schema/<resource>.json` | One JSON Schema per in-scope resource |
| `named-ids/`, `menu-objects/`, `menus/` | Picklist values and menu structure, as in the table above |
| `config-rows/` | Full rows of products, categories, dispositions, mailboxes, service mailboxes, standard content and event subscriptions |
| `report-defs/<id>.full.json` | One targeted report's columns and filters |
| `_scope.json` | What was requested, skipped and classified, and `components_run`: which components ran and when |
| `_manifest.jsonl` | Every request: time, URL, status, bytes, SHA-256 |
| `_errors.json` | Requests that did not return 200, with the likely cause |
| `schema-sub/` | Custom field definitions per object and namespace |
| `data-dictionary.parquet`, `.csv` | One row per field: object, path, label, standard or custom, menu flag, type, length, read-only, lookup target, the file its options came from, suggested Salesforce type. Yes/no fields are checkboxes and staff references are user lookups, not picklists |
| `oracle-config-inventory-<date>.xlsx` | The team workbook from [build_config_inventory.py](build_config_inventory.py): one tab per list (mailboxes, queues, profiles, staff groups, channels, statuses, custom objects, custom fields, the data dictionary, picklist values, products, categories and dispositions, the standard content index, surveys, reports, holidays), plus About and Summary tabs. Two exclusions are enforced in code: picklists whose values are staff names (`ct_searcher`, `lead_used`) are counted on the About tab and never listed, and standard content appears as an index without its reply text. Report dates come from the report listing |
| `picklist-values.parquet`, `.csv` | One row per picklist entry: source, object, field or object, id, name, parent, display order, hierarchy path, visible interfaces. Products, categories and dispositions read their full rows from `config-rows/` when present, which fills parent, the path (for example `Break Off-Pick One > Time Constraint`) and the interfaces each value shows on (`nci`, `nci1`, `nci2`, where `nci2` is Spanish) |

Counts printed by the dictionary build are field counts (properties in a schema) and picklist value counts. No count is a record count.

## Reading a failure

| Status | Likely cause |
| --- | --- |
| 401 | Credentials rejected, or the profile lacks Public SOAP API > Account Authentication |
| 403 | The profile's object permissions, or an IP allowlist, blocked the resource |
| 404 | The resource or sub-path does not exist on this site |

## Tests

No network:

```bash
python3 -m pytest oracle/tools/tests -q
```

They cover the allowlist and refusals, run-time approval of menu objects, pagination, the people exclusion, the custom object classification, the named-ID listing parser, the custom-field walk (`customFields.c` and `customFields.<package>`), the component registry and dependency planning, report targeting, the configuration components (including dropping the integration user and resuming report definitions), the picklist hierarchy, both outputs, and the inventory workbook's exclusions.

## Data profiling: counts only

Added 2026-10-02, on Ben Bolding's direction after Fred Hutch approved data access on the test instance.

`profile_data.py` profiles how CIS uses Oracle: record counts per object, which inquiry fields and picklist values are used, and how field use differs by queue. `osvc_aggregate.py` holds the rules it runs under:

- Oracle does the counting. The tool sends `count`, `min` and `max` queries, grouped only by picklist or checkbox fields, and stores the numbers. It never selects a record's values.
- Free text, names, dates of birth, zip codes and people fields can be counted as filled or empty, and nothing else.
- The caller passes a structured query, never query text. The finished text is checked again and anything that isn't a single counting SELECT is refused. Oracle's query endpoint also runs DELETE, so this check matters.
- In a result grouped by two or more fields, a count from 1 to 10 is hidden.
- Nothing is sent between 9 a.m. and 9 p.m. Eastern, requests are 3 seconds apart, and a run has a request budget.
- Responses are not written to disk; the manifest logs their size and hash.

```bash
export OSVC_SITE_URL=https://nci--tst.cx.usg.oraclecloud.com
export OSVC_USER=<the test account>
python3 oracle/tools/profile_data.py --phase probes,inventory --dry-run     # print the queries, send nothing
python3 oracle/tools/profile_data.py --phase inventory,fields,picklists,channels,types,pairs,objects --use-report
```

Output goes to `oracle/extracts/data-profile/<date>/` (gitignored). A run resumes where it stopped. What Oracle's query language supports here, found by the `probes` phase on 2026-10-02: several counts in one query, `count(field)` skips empty values, grouping by a picklist's `id` or `lookupName`, timestamp filters, and the report database (`--use-report`). A text field can't be used in a filter, and relationship fields (primary contact) can't be counted.

`profile_answers.py` pulls articles in full, with their products, categories, siblings, related articles and attachment details (names, types and sizes; the files are not downloaded). It goes through `query_answers()`, which allows a single SELECT on answers and nothing else. Output goes to `oracle/extracts/answers/<date>/`.

Two changes on 2026-10-02, both on Ben Bolding's direction: the retention phase may count a contact's name, email and address fields as filled or empty, to measure what the 15-month scrub removes; and `--allow-cis-hours` lets a run go ahead during CIS hours on a test instance.

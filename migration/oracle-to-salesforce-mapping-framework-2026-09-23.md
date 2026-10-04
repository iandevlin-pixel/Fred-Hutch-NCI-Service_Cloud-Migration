# Oracle Service Cloud to Salesforce: mapping framework for NCI CIS

> **Frozen 2026-09-29.** Published to the Notion Project Library as [Oracle Service Cloud to Salesforce: mapping framework](https://app.notion.com/p/3ead4b877417816383aff1369c4596d1). The Notion page is the live copy; edit there, not here. The "Proposed RAID rows" section below stayed local and is not on the Notion page.

How the Oracle Service Cloud (RightNow) configuration that runs the NCI Cancer Information Service maps onto Salesforce Service Cloud, Salesforce Knowledge, and Amazon Connect in Government Cloud, how Kicksaw reaches the Oracle instance, and what it pulls to do the mapping without touching caller data.

**Audience:** internal Kicksaw. Ben Bolding, Avi Rabinovitch, Ian Devlin, Hannah Oanca. Working document, not a client deliverable and not pushed anywhere. The object mapping, the channel table, and the access section can be lifted into a session guide or a design document once the metadata pull confirms them.

Built 2026-09-23 from the 2025-07-29 reverse demo, discovery sessions 1 to 3, the 2026-09-21 Oracle test environment tour, the executed SOW, Oracle B2C Service documentation, and the first catalog read from the Oracle test instance.

---

## Summary

- Inquiry maps to Case, business rules to record-triggered Flows, workspaces to Lightning record pages with Dynamic Forms, profiles to permission set groups, Standard Text to Quick Text, and Answers to Knowledge. Voice routes in Amazon Connect, not Omni-Channel.
- CIS uses five Oracle objects in the specialist workflow (Inquiry, callback Task, SCIF, Answer, Contact) plus surveys and reports. It does not use Organizations, Assets, Opportunities, or SLA entitlements.
- The SCIF is its own custom object with seven menu objects behind it. Two other custom packages, `DEMOGR` (the demographics survey) and `Referrals`, exist alongside it and are part of the mapping.
- Kicksaw reaches the Oracle test instance through the Connect REST API and the Agent Browser UI from a Mac. The REST metadata catalog gives the data model and the picklist values; Element Manager gives business rules, workspaces, navigation sets, and standard text. REST access is confirmed and the first pull is scoped in section 7.
- The queue, rule, and field cleanup decisions belong to Adrianna Gutierrez and Holly Fernandez-Johnson; scope belongs to Mike Griffin. This document is a design input.

## Premise

| Question | Position | Source |
| --- | --- | --- |
| Configuration | Rebuilt in Salesforce and Amazon Connect from the Oracle configuration inventory, not lifted. Mark Hubers: the permission model gets designed fresh | Oracle tour, 2026-09-21, 25:39 |
| Knowledge content | Migrates. About 5,000 English and Spanish answers with the sibling linkage. Never exported before | Session 1, 2026-09-15; session 2, 2026-09-17, 1:00:14; SOW Addendum A assumptions 10 and 11 |
| Inquiry and caller history | Open. The SOW puts data migration inside the configuration phase; session 2 leaned to starting fresh on Analytics history; data cleansing ownership (RAID-7, legacy D12) is unresolved | SOW; session 2; register |
| Contact records | Purged on a rolling window, 13 months per the reverse demo, 15 months per session 1; what is deleted versus hidden is unverified (RAID-24, legacy Q7) | Reverse demo, 2025-07-29; session 1 |

The mapping covers configuration and knowledge. Where a row depends on the open history decision, the row says so.

## Terminology

| Term | Means | Do not use |
| --- | --- | --- |
| Inquiry | The primary CIS record. Oracle's `incident` table, workspace NCI Inquiry v2.1 | Incident, except when naming the Oracle table or REST resource |
| Answer | An Oracle knowledge article. Oracle Knowledge Foundation, reachable from the inquiry | Knowledge item |
| SCIF | Smoking Cessation Intake Form. Custom object `SCIF.SCIF`, completed for every counseling client. Spelled "skiff" and "SKIF" in older transcripts | SKIF |
| Callback task | An Oracle Task used to schedule a future call, up to 12 per client, with its own workspace and rules | Task, alone |
| Standard Text | Oracle's canned response library (F9 in the console). REST resource `standardContents` | Standard Content, macros |
| Workspace rules | Client-side rules inside a workspace definition (show, hide, require, on load, on change). Exported with the workspace | Business rules |
| Business rules | Server-side rules under Site Configuration > Rules, one tab per object: inquiry, answer, contact, content, organization, task, opportunity | Workspace rules, workflows |
| Navigation set | The console navigation bundle assigned by profile | Nav bar, app |
| Menu | An Oracle picklist. Stored as a named ID, a named-ID hierarchy, or a menu-only custom object (section 6) | Picklist, when referring to the Oracle side |

## 1. Object mapping

| Oracle entity | What CIS does with it | Salesforce or Amazon target | Notes and dependencies |
| --- | --- | --- | --- |
| Inquiry (`incident`) | Every phone, chat, or email interaction creates one. Hand-keyed contact, service number, and queue. Carries the coding fields, the point of access, and the custom fields grouped by originating project (ECRF and others) | `Case`, one record type per call type (D17, workspace streamlined by call type) | Fields and menus come from the metadata pull. An external ID for the Oracle reference number matters only if inquiry history migrates |
| Callback task (`task`) | Schedules future calls, months or years out. Up to 12 per client. Own workspace with rules. Lands on a report that Pinpoint reads for SMS reminders | `Task` or a custom callback object, decided with the callback and SMS design | Tied to [../salesforce/sms-reminders-options-2026-09-22.md](../salesforce/sms-reminders-options-2026-09-22.md) and to how Amazon Connect places the outbound call |
| SCIF (`SCIF.SCIF` plus seven menu objects: gender, interval, quit confidence, standard yes/no, reason to quit, positive influence, tobacco used) | Intake form completed for every smoking cessation counseling client. The VA's requirements for it are unknown; the client has volunteered it for reduction | A child object of `Case` with picklists built from the seven menu objects, entered through a Screen Flow | Blocked on the VA question (tour question 8). Field set comes from the `SCIF.SCIF` schema |
| Answer | About 5,000 articles, English and Spanish siblings linked, inserted into messages from the Messages tab. Suggest and propose exist but go unused. Inserting an article sends staff-only notes to the caller | `Knowledge__kav` with a bilingual record structure and data categories for the product and category tags. A sendable version separated from staff notes | Migration mechanism open (session 2, 1:00:14). Melissa's team owns the content |
| Message thread | Email bodies and chat history on the Messages tab. Response versus private note. Send on save. NIH inboxes forward into Oracle and Oracle sends as nih.gov | Email: `EmailMessage` on the Case through Email-to-Case. Private notes: internal feed posts. Chat transcripts: follow the chat channel decision | Sending as nih.gov needs the same authority in Salesforce, an open item for the email design |
| Standard Text | Repository of templates for emails and messages, LiveHelp standard responses, the F9 response library | Quick Text (scoped by channel) for snippets; Lightning email templates for letters | Content pull is a separate ask to Mark; the pull gives the structure only |
| Staff account | About 40 to 45 specialists plus administrators. Grouped by staff group and queue | `User` with Service Cloud and Knowledge licenses; Amazon Connect user with a routing profile | Skills and tiers are RAID-26 (legacy Q10). Staff group names come from the pull; staff records do not |
| Contact | A placeholder `anonymous@anonymous` contact for chat; hand-keyed for others; purged on the retention window; no repeat-caller persistence (D14) | Design decision: a single placeholder contact, a contact per interaction purged by a scheduled Flow, or no contact | Depends on RAID-24 and on what demographics must survive anonymized |
| Demographics survey (`DEMOGR.Study`, `StudyQueue`, `CollectionMethod`, `CollectionStatistics`) | Survey Explorer plus an add-in that pops the demographics survey into the workspace by queue; follow-up surveys for callbacks | Not settled. Salesforce Feedback Management licensing is short (300 responses per term, found 2026-09-22); Amazon Connect phone surveys are the alternative on record | Own finding. The `DEMOGR` schemas show what the add-in configures; the surveys grant on the test account is still pending |
| Referrals (`Referrals.ReferralQCs`, `ReferralLanguages`, four menu objects: QC type, language, country, state) | A referral quality-check model, not yet walked on a call | To be placed once the schemas are read; likely a Case-related object if it is the VA Direct referral record (D20) | Confirm with Adrianna Gutierrez which workflow uses it |
| Report | 14 years of Oracle Analytics reports. Definitions can be exported; the data cannot be separated from PHI, so report rows are never pulled | Salesforce reports and dashboards; Amazon Connect metrics for telephony | Definition inventory comes from the pull if the API allows it |
| Telephony bridge (`OpenMethods.HarmonyConfiguration`, `InteractionWorkflow`, `License`) | Cisco Finesse bridge and PopFlow screen pop | Retired with Service Cloud Voice | Schema pulled for completeness; nothing maps |
| Organization, Asset, Opportunity, SLA entitlement | Not used in the specialist workflow. Present only as rules editor tabs | None | Entitlements and milestones revisited only if reporting needs response-time measures |

## 2. Permissions and visibility

The design goal, per Mark Hubers on 2026-09-21, is to cover the same capability set with Salesforce and Amazon Connect primitives rather than mirror Oracle profiles.

| Oracle construct | What it bundles at CIS | Target |
| --- | --- | --- |
| Profile | Object permissions, field access through workspace assignment, language, clinical trials chat eligibility, knowledge read, knowledge edit, navigation set, administrative rights | A minimal-access profile plus permission set groups per role (specialist, bilingual specialist, clinical trials specialist, knowledge author, supervisor, administrator). Field-level security in the permission sets |
| Navigation set | Which explorers and buttons the console shows | Lightning apps with a navigation bar per role |
| Staff group | Reporting and queue membership | Public groups and queues; Amazon Connect routing profiles for voice |
| Queue (phone, email, chat, PIQ, clinical trials, ProActor, Impact) | Assignment and reporting. Which are live is undocumented | Salesforce queues for email and Salesforce-native work; Amazon Connect queues for voice. The list is decided by Adrianna Gutierrez and Holly Fernandez-Johnson (tour decision 4) |
| Field access on the workspace | Fields hidden or read-only per workspace | Field-level security plus Dynamic Forms visibility. Security lives in the permission set so it holds in reports, list views, and the API |

Organization-wide default for `Case` is a design choice once the contact model is settled; Private with role-hierarchy roll-up to supervisors is the starting assumption.

## 3. Agent experience

| Oracle construct | CIS specifics | Target |
| --- | --- | --- |
| Workspace (NCI Inquiry v2.1, the task workspace) | Multi-tab layout with the coding fields, Messages tab, SCIF, demographics tab. Tabs appear by queue through workspace rules. Rule count is capped because of race conditions | Lightning record page in the Service Console, one per record type, with Dynamic Forms sections and component visibility by call type |
| Workspace rules | Show, hide, require, on load, on change; the queue drives which tabs show | Dynamic Forms visibility rules for show and hide; validation rules or before-save Flows for required-by-condition |
| Agent scripting and workflows | PopFlow drives the screen pop from Cisco; NCI Workflow v1 holds the inquiry workspace | Screen Flows in the console side panel for guided intake (SCIF, coding); the screen pop moves to Service Cloud Voice |
| Desktop add-ins | Harmony (telephony bridge), the survey add-in, the Pinpoint report trigger codes | Retired. Telephony is Service Cloud Voice; surveys and SMS are their own designs |
| Console utilities | LiveHelp window, F9 standard text, suggest button | Omni-Channel utility, Service Cloud Voice softphone, Quick Text, Knowledge component |

Starting console layout: caller context on one side, the inquiry and its feed in the center, knowledge and the guided script on the other, with Omni-Channel and the softphone in the utility bar. What goes in the caller-context column depends on the contact decision.

## 4. Automation

Oracle evaluates business rules top down per object, with states, functions, and an explicit stop. Salesforce splits the same logic by timing.

```text
Inquiry saved
   |
   v
Before-save Flow (fast field updates)
   - defaults from call type and queue
   - daylight-saving time adjustment (Mark, session 3, 36:01)
   - coding normalization
   |
   v
Record committed
   |
   v
After-save Flow (actions and related records)
   - route to a Salesforce queue (email and Salesforce-native work only)
   - create the callback task
   - send notifications, post to the feed
   - write the SMS reminder trigger (per the SMS options note)
   |
   v
Stop Processing  ->  the outcome ends at an End element; nothing downstream runs
```

Rules for the translation:

- Only active rules carry forward (tour decision 3, directional; Adrianna Gutierrez to confirm). The intent behind the original launch consultants' rules is tour question 10.
- Each Oracle object tab becomes its own pair of Flows on its target object. Inquiry rules land on `Case`; task rules on the callback object; answer rules on `Knowledge__kav`.
- No hard-coded IDs. Queues and record types are fetched by developer name.
- Object event handlers (custom processes), if the Element Manager export finds any, are the one place Apex may be needed; everything else is declarative.
- Voice routing lives in Amazon Connect contact flows and routing profiles, not in Flow.

## 5. Channels and routing

| Channel | Today | Target | Where routing lives | Status |
| --- | --- | --- | --- | --- |
| Voice, about 10 inbound numbers, English and Spanish | Cisco Finesse plus Verizon IVR, Harmony bridge, PopFlow screen pop | Service Cloud Voice with Amazon Connect, bring-your-own AWS GovCloud `us-gov-west-1` | Amazon Connect contact flows, queues, routing profiles; Omni-Channel presence only | Settled (D2, D13) |
| Chat (LiveHelp) | Oracle LiveHelp window, `anonymous@anonymous` contact, clinical trials chat by profile | Not settled in any document this note cites | Depends on the chat decision | Open |
| Email | NIH inboxes auto-forward to Oracle; Oracle sends as nih.gov; PIQ and clinical trials queues | Email-to-Case (session 3 guide) | Salesforce queues plus Omni-Channel or assignment rules | Channel settled, send-as authority open |
| SMS reminders | Pinpoint reads the callback report, texts 24 hours and 1 hour before, writes status back | Two options sized in the SMS options note; Pinpoint retires 2026-10-30 | Per option | Open, client has not chosen |
| Outbound callbacks | Specialist places the call from the task | Amazon Connect outbound from the callback record | Amazon Connect | Design with the callback task |

## 6. Oracle configuration inventory: what to pull and from where

| Artifact | Mechanism | Mac | Returns caller data | Status |
| --- | --- | --- | --- | --- |
| Object list, standard and custom fields, types, lengths, read-only flags, lookup targets | Connect REST `metadata-catalog` and `metadata-catalog/<resource>` (JSON Schema) | Yes | No | Tooling ready; scope in section 7 |
| Picklist values | Three mechanisms, table below | Yes | No | Same |
| Business rules, all object tabs, with states and functions | Element Manager export package (`BusinessRule`, `BusinessRuleVariable`) | Yes, Agent Browser UI | No | Depends on site version and profile access |
| Workspace definitions with their workspace rules | Element Manager (`Workspace`, `WorkspaceScript`), or the console's export to XML (1 MB cap, notes excluded) | Element Manager yes; console needs the Windows VM | No | Same |
| Navigation sets, customizable menus, standard text structure, variables, message bases, configuration settings | Element Manager (`NavigationSet`, `CustomizableMenu`, `StandardText`, `Variable`, `MessageBase`, `ConfigurationSetting`) | Yes | Standard Text carries template content; held for a separate ask | Same |
| Report definitions | REST `analyticsReports` (definitions only; `analyticsReportResults` runs a report and is never called) or Element Manager (`Report`) | Yes | Definitions no | One API attempt in the pull; Mark if it returns 403 |
| Staff groups | REST `accountGroups` | Yes | Group names only | In the pull |
| Profiles and staff accounts | Console: Staff Management > Profiles export (format unknown, tour question 4) | Console | Staff names and emails | Test what the export produces; no staff records through the API |
| Surveys and the demographics add-in | REST schemas for the `DEMOGR` package; console Surveys explorer for the survey definitions | Schemas yes; explorer needs the grant | Survey definitions no; responses yes and never pulled | Grant pending with Mark |

**How Oracle stores picklists.** Three mechanisms, each read differently.

| Mechanism | Where the values live | How to read them | Example |
| --- | --- | --- | --- |
| Named IDs (standard and custom menu fields) | Site menus, not the schema | `namedIDs/<resource>` lists the menu fields; `namedIDs/<resource>/<field>` returns `id` and `lookupName` pairs | `namedIDs/incidents/severity` |
| Named-ID hierarchies (products, categories, dispositions, source) | Hierarchical menus | `namedIDHierarchies/<resource>/<field>` returns every entry with its parents | `namedIDHierarchies/incidents/source` |
| Menu-only custom objects | Rows of a custom object whose only fields are `id`, `lookupName`, display order, and timestamps | The object's rows, which are the values | `SCIF.mGender`, `Referrals.mReferralState` |

Named IDs that resolve to people (assigned to, account, contact, organization, created by, updated by, owner) are excluded, because their value lists are staff or contact names.

**Element Manager.** Works only on the Agent Browser UI. Supported element types: Report, Workspace, AddIn, NavigationSet, CustomObject, SystemAttribute, StandardText, Variable, ObjectEventHandler, ConfigurationSetting, MessageBase, BusinessRule, BusinessRuleVariable, WorkspaceScript, ExternalObject, CustomScript, CustomizableMenu, Product, Category, Disposition, CustomBusinessEvent. Business rule support was added across the 2020 to 2021 releases, so it depends on the site version, which is one of the facts still needed from Mark.

## 7. Remote access and the first pull

### Access

| Item | Value |
| --- | --- |
| Site | `https://nci--tst.cx.usg.oraclecloud.com`, test clone `NCI__TST` (a full copy of production from two to three months earlier), interface `nci`. The `usg` domain indicates Oracle's US Government cloud |
| Account | `sthomas_RNT`, the shared test account Mark Hubers set up 2026-09-21. Configuration access; no reports; surveys grant pending. Password held in the macOS Keychain, never in a file or a chat |
| REST | Connect REST API v1.4 at `/services/rest/connect/v1.4/`. Basic authentication over HTTPS. The `OSvC-CREST-Application-Context` header on every call. The profile carries the Public SOAP API > Account Authentication permission, which is what REST basic authentication uses. Confirmed 2026-09-23: the catalog lists 63 resources |
| Object permissions on the API | Oracle's `SERVER_ACCESS_CONTROL_ENABLED` setting carries the profile's object permissions onto SOAP and REST calls. The test account's exclusions (reports, PHI objects) therefore hold on the API as well |
| Browser | Agent Browser UI at `/AgentWeb/` for Element Manager. Same account |
| Console | Windows VM only, for the profiles export and anything Element Manager does not cover |
| Sessions | The account allows one session. Pulls run when nobody is signed in as `sthomas_RNT` |
| Still needed from Mark Hubers | Site version (Help > About), the surveys grant, report definition access if the API refuses it, and a password rotation |

### Guards

The tooling under [oracle/tools/](../oracle/tools/README.md) enforces the rule in code, before any network call:

- GET only, and only limit and offset as query parameters.
- An allowlist of schema and configuration resources. Rows of `incidents`, `tasks`, `answers`, `contacts`, `organizations`, `accounts`, `chats`, `standardContents`, `configurations`, `mailboxes`, `queryResults` (ROQL), and `analyticsReportResults` (running a report) are refused by name; anything not allowlisted is refused by default.
- Rows of a custom object are allowed only after its schema shows it is a menu-only table, and the classification prints before any row is fetched.
- Every request is appended to a manifest (time, URL, status, size, hash) so the pull is auditable if Fred Hutch asks what Kicksaw retrieved.
- All output lands under the gitignored `extracts/` folder. Only curated outputs (the data dictionary, the picklist list, the inventory document) move into the repository, and to Notion or Jira only on Ben's direction.

### Scope of the first pull

**Schemas, 47 of the 63 listed resources, no records.**

| Group | Resources |
| --- | --- |
| Core and inquiry-related (11) | `incidents`, `incidentResponse`, `tasks`, `answers`, `answerVersions`, `contacts`, `organizations`, `accounts`, `accountGroups`, `chats`, `standardContents` |
| Menus and named IDs (9) | `serviceCategories`, `serviceDispositions`, `serviceProducts`, `namedIDs`, `namedIDHierarchies`, `countries`, `holidays`, `channelTypes`, `siteInterfaces` |
| Site configuration (6) | `configurations`, `messageBases`, `variables`, `mailboxes`, `serviceMailboxes`, `analyticsReports` |
| Custom packages (21) | `SCIF` (8), `DEMOGR` (4), `Referrals` (6), `OpenMethods` (3) |

Not pulled: the 10 sales, marketing, and asset resources, and the 6 API plumbing resources (`bulkExtracts`, `bulkExtractResults`, `queryResults`, `analyticsReportResults`, `eventSubscriptions`, `sSOTokenReferences`).

**Configuration rows: picklist values and structure only.** Named-ID values and hierarchies for the core resources with the people exclusion; the seven menu structure resources; `accountGroups` names; rows of the custom objects classified as menu tables; one attempt at `analyticsReports` definitions.

**Never pulled.** Rows of any core object, `SCIF.SCIF`, the `Referrals` and `DEMOGR` data objects, `configurations`, `mailboxes`, `serviceMailboxes`, `queryResults`, `analyticsReportResults`.

**Outputs.** Raw JSON under `extracts/oracle-metadata/<date>/`; a data dictionary (one row per field, with the menu source for picklist fields) and a picklist value list, as Parquet plus CSV for review; an inventory document in `oracle-service-cloud/` with field counts and picklist value counts. No count is a record count.

## 8. Rebuild sequence

| Phase | Work | Inputs |
| --- | --- | --- |
| 1. Inventory | REST pull, Element Manager package, data dictionary, picklist list, rule and workspace inventory, live-versus-dead list from Adrianna and Holly | Section 7 |
| 2. Foundation | Case record types and fields, SCIF child object, Knowledge object and data categories, queues, public groups, profile, permission set groups, Amazon Connect instance and users | Data dictionary, picklists, tour decisions 2 and 4 |
| 3. Experience | Service Console app, record pages with Dynamic Forms, Screen Flows for SCIF and coding, Quick Text, email templates, Service Cloud Voice softphone | Workspace export, standard text structure |
| 4. Automation and routing | Before-save and after-save Flows per object, Amazon Connect contact flows and routing profiles, Email-to-Case, the SMS reminder option once chosen | Rule export, live rule list |
| 5. Validation | Flow path tests, permission set field checks, specialist simulation by call type against the session 3 walkthroughs | Everything above |

Everything named in the Salesforce column is core platform (Knowledge, data categories, Dynamic Forms, Flow, Omni-Channel, Quick Text, Email-to-Case, Service Cloud Voice). Nothing depends on an AppExchange package or an Einstein feature, which keeps the Government Cloud boundary rule intact.

## Open questions

| # | Question | Owner | Needed by |
| --- | --- | --- | --- |
| 1 | Site version, so Element Manager business rule support can be checked | Mark Hubers | Before the rule inventory |
| 2 | Does a basic-auth API call end an open console session? | Ben Bolding, on the first scoped pull | First pull |
| 3 | Does the API return report definitions (`analyticsReports`) for this profile? | Ben Bolding, on the first scoped pull; Mark Hubers if 403 | Report inventory |
| 4 | Surveys grant on the test account | Mark Hubers | Before survey design |
| 5 | What does the VA require from the SCIF? (tour question 8) | Adrianna Gutierrez, Holly Fernandez-Johnson | Before SCIF design |
| 6 | Which queues, service numbers, and rules are live? (tour question 5) | Adrianna Gutierrez, Holly Fernandez-Johnson | Before routing design |
| 7 | Which workflow uses the `Referrals` package? | Adrianna Gutierrez | Before the object mapping is final |
| 8 | Contact model given the purge and the anonymized demographics | Ben Bolding to propose; Mike Griffin to decide | Before the Case OWD is set |
| 9 | Knowledge export mechanism and whether staff-only notes separate cleanly | Mark Hubers, Melissa's team | Before knowledge migration design |
| 10 | Whether Answer and Standard Text content may be pulled through the API | Ben Bolding to ask Mark Hubers | Before the content pull |

## Proposed RAID rows (not applied)

| Type | Proposal | Visibility |
| --- | --- | --- |
| Decision | Kicksaw pulls Oracle metadata through the Connect REST metadata catalog and Element Manager with the shared test account, against an allowlist that excludes every record resource. Extends tour decision 6 | Client-safe |
| Action | Mark Hubers: site version, surveys grant, report definition access if the API refuses it, password rotation | Client-safe |
| Decision | The SCIF is a custom object with seven menu objects and maps to a child object of Case, not to fields on the inquiry | Client-safe |
| Risk | Element Manager business rule export depends on the site version, which is unknown. Fallback is the console's Excel and PDF rule export in the Windows VM | Internal only until the version is known |

## Sources

- Transcripts: 2025-07-29 reverse demo; 2026-09-15 discovery session 1; 2026-09-17 discovery session 2; 2026-09-21 Oracle test environment tour; 2026-09-22 discovery session 3
- Executed SOW, July 20, 2026 client-redlined version, Kicksaw Google Drive
- Register: [../pm/raid/decision-register.csv](../pm/raid/decision-register.csv) rows Q5, Q6, Q7, Q10, R3, D12, D14, D16, D17, D19, D20; [../pm/raid/raid-import-2026-09-18.csv](../pm/raid/raid-import-2026-09-18.csv)
- Oracle test instance, catalog read 2026-09-23, under `oracle/extracts/`
- Oracle documentation, fetched 2026-09-23: REST API for Oracle B2C Service, Quick Start, named IDs and named ID hierarchies; Using B2C Service, Administration Permissions; Using B2C Service, exporting and importing workspaces; Element Manager on the Agent Browser UI; REST API for Element Manager, create an export package; Configure B2C Service for OAuth Authorization; Oracle B2C Service release notes 20A, 21A, 21C
- Oracle support answers, fetched 2026-09-23: custom fields in REST API (11152); enforcing profile permissions on SOAP and REST API calls (7156); access denied with SOAP API (6756); restricting hosts that can access the console (245); Element Manager export and import options (11002)
- [reference/oracle-to-salesforce-framework-gemini-2026-09-23.md](reference/oracle-to-salesforce-framework-gemini-2026-09-23.md), source draft
- [../salesforce/sms-reminders-options-2026-09-22.md](../salesforce/sms-reminders-options-2026-09-22.md) and [../project/amazon-product-sow-alignment-2026-09-21.md](../project/amazon-product-sow-alignment-2026-09-21.md), for the channel table

## Change log

| Date | Change |
| --- | --- |
| 2026-09-23 | Created: terminology, object mapping, permissions, agent experience, automation, channels, configuration inventory, remote access, rebuild sequence |
| 2026-09-23 | Revised after the first catalog read: REST access confirmed, the `SCIF`, `DEMOGR`, `Referrals` and `OpenMethods` packages added to the object mapping, the three picklist mechanisms and the scope of the first pull recorded, open questions and RAID proposals updated |

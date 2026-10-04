# Project scope

What the Fred Hutch NCI CIS engagement is building, where scope is recorded, and the decisions that shape it. Internal Kicksaw document.

## The goal

Replace the contact center stack that Fred Hutch runs for the National Cancer Institute Cancer Information Service (CIS), and land it inside FedRAMP-authorized government clouds.

| Today | Replaced by | Who builds it |
| --- | --- | --- |
| Oracle Service Cloud (since 2012): inquiries, tasks, callbacks, knowledge | Salesforce Service Cloud in the Government Cloud Plus org | Kicksaw |
| Cisco Finesse and Verizon IVRs | Salesforce Voice with Amazon Connect, bring-your-own instance in AWS GovCloud `us-gov-west-1` | Kicksaw on the Salesforce side; the AWS team owns all AWS configuration |
| Verint workforce and quality management | Calabrio ONE | Calabrio's own services team |

The service it has to carry: roughly 40 to 45 remote, bilingual English and Spanish agents; about 10 inbound numbers; hours 9 a.m. to 9 p.m. ET; phone, email, chat and SMS; roughly 5,000 English and Spanish knowledge articles; demographic data capture, embedded surveys, 13-month retention with PII scrubbing, and NCI reporting.

Phases run over 24 weeks from the 2026-09-08 kickoff: discovery and planning, configuration, SIT, UAT, training and go-live, hypercare. Target go-live is Wednesday, January 27. Earlier notes record the year as 2026, which cannot be right for a September 2026 kickoff; read it as 2027.

## Where scope lives

| Source | Role |
| --- | --- |
| [Scope tracker](https://docs.google.com/spreadsheets/d/1tqBE3dywkXV_XJvXEzY1aa3HvHwSS9EAHdzl_YR2A_k/edit) (Google Drive `1tqBE3dywkXV_XJvXEzY1aa3HvHwSS9EAHdzl_YR2A_k`), Scope Tracker tab | **Source of truth for what is in scope.** The team's working reading of the SOW, one row per scope item with a status. The team edits it |
| [Executed SOW, July 20, 2026 version](https://drive.google.com/file/d/1Dt3mlE0QTSltDJC_utDyGtLsIQURlUUK/view) | The contract. Governs where it and the tracker disagree. The filename reads "KS Updated", so confirm the countersigned copy with Hannah Oanca before a contractual argument |
| [Snapshots](scope-tracker/) | Dated local copies of the tracker, so changes can be traced with git. Never the source of truth |
| The RAID Log in Notion | Decisions that move scope. See [notion-conventions.md](notion-conventions.md) |

**Reading the tracker.** Before stating what is in or out of scope, read the live tracker through the Google Drive connector. Check its modified time first. If it is newer than the latest snapshot, save a new snapshot as `project/scope-tracker/snapshot-YYYY-MM-DD.md` in the format of the existing one, and note what changed. Cite rows by their tracker ID with a descriptor, for example "tracker TO-5 (callbacks and SMS reminders)". Tracker IDs D-1 to D-5 collide with old register IDs, so always prefix them with "tracker".

**Handling.** The tracker carries hours, fees and billing terms. Scope summaries that leave the team drop them.

## The tracker at a glance

As of the [2026-09-24 snapshot](scope-tracker/snapshot-2026-09-24.md), last edited in Drive on 2026-09-17. Read the live tracker for current status.

| Workstream | Rows | Status |
| --- | --- | --- |
| Discovery and planning | D-1 to D-5 | All in scope |
| Salesforce and Amazon Connect configuration | SC-1 to SC-5 | All in scope |
| Telephony and omnichannel | TO-1 to TO-8 | All in scope |
| CRM and knowledge base | CK-1 to CK-6 | All in scope |
| Scheduling and WFM (Calabrio) | WF-1 to WF-3 | 1 in scope (Salesforce-side visibility), 2 out (Calabrio's own setup and recording) |
| Real-time reporting | RT-1 to RT-4 | All in scope |
| Data migration | DM-1 to DM-3 | 2 deferred, 1 out (cleansing) |
| SIT and backlog closeout | SIT-1 to SIT-4 | All in scope |
| UAT | UAT-1 to UAT-3 | All in scope |
| Training and go-live | TG-1 to TG-4 | 3 in scope, 1 out (delivering the sessions) |
| Hypercare | HC-1 to HC-4 | 3 in scope, 1 out (support after week 24) |
| Compliance and security | CS-1 to CS-8 | 7 in scope, 1 needs decision (vaccines, only if on site) |
| Out of scope and assumptions | OOS-1 to OOS-9 | 7 out, 2 need decision (a WFM product other than Calabrio; the billing structure) |

## Decisions that shape scope

Settled outside the tracker. Each is recorded in the RAID Log or a project document.

| Decision | Effect on scope | Where recorded |
| --- | --- | --- |
| No standard Salesforce org migration, 2026-09-15 | The only source system is Oracle Service Cloud | Register D1; [Scope history](#scope-history), below |
| Amazon Connect runs in AWS GovCloud `us-gov-west-1`, 2026-09-14 | No cross-partition integration to commercial AWS services | Register D2 |
| FedRAMP Moderate is the requirement | The GovCloud Plus org is authorized at High, which satisfies Moderate | [CLAUDE.md](../CLAUDE.md), environment posture |
| The AWS team owns all AWS configuration, 2026-09-23 | Kicksaw builds the Salesforce side of Voice only. FIPS is AWS's; transcription is Calabrio's | [amazon-product-sow-alignment-2026-09-21.md](amazon-product-sow-alignment-2026-09-21.md) |
| Start fresh on data, tentative, 2026-09-17 | Knowledge, scheduled callbacks and in-flight work are the exceptions. NCI concurrence still open | Tracker DM-1; session 2 transcript |
| Email is Salesforce Email-to-Case | Amazon Connect has no email channel in AWS GovCloud | Session 3 guide; alignment doc |
| SMS runs on Salesforce Digital Engagement, per the SOW | The callback reminders are open between Digital Engagement and AWS End User Messaging; the org's 1,000 blast-conversation entitlement is the constraint | [sms-reminders-options-2026-09-22.md](../salesforce/sms-reminders-options-2026-09-22.md) |
| No AppExchange package in the Government Cloud org, held as a design constraint | Any package needs an Authorizing Official review with lead time the schedule cannot absorb | Alignment doc |

## Where the tracker disagrees with a settled decision

Open against the tracker, not corrected in it. The team owns the tracker; raise these with whoever maintains it.

| Tracker row | What it says | Conflict |
| --- | --- | --- |
| D-5 (Amazon Connect instance planning) | "Kicksaw provisions the Amazon Connect instance" | The AWS team owns all AWS configuration (2026-09-23) |
| SC-5 and CS-1 (GovCloud compliance) | Calabrio must be GovCloud approved and operate within GovCloud | Calabrio runs in its own FedRAMP Moderate environment, inside neither GovCloud |
| TO-3 (core telephony features) | Lists email among telephony features | Email is Email-to-Case, not an Amazon Connect channel |
| TO-8 (channels and numbers) | "Live Chat (Chatbot and SMS)" in scope | No clean chatbot route: Amazon Connect AI agents are unavailable in GovCloud, Einstein Bots are Interoperable only, Agentforce needs an NIH-level AI approval |
| DM-1, DM-2 versus SC-4 | Data migration deferred in the Data Migration rows, in scope in SC-4 | SC-4 predates the 2026-09-17 start-fresh call |

## Scope history

Moved here from the project CLAUDE.md on 2026-10-01 so scope lives in one document. Kept as history; D1 settled the source-system question.

**Before D1 (2026-09-15), four accounts of what was being migrated were on the record and they did not agree:**

| Source | What it says |
| --- | --- |
| Kickoff deck and client call, 2026-09-08 | Oracle Service Cloud to Salesforce Service Cloud in Government Cloud |
| Internal knowledge transfer, 2026-09-01 | "Migrating their Salesforce call center environment from a standard instance to a Salesforce GovCloud instance" |
| Executed SOW | Addendum A: implement Salesforce Service Cloud "to replace the existing Oracle Service Cloud." Current-state inventory lists Oracle Service Cloud, Cisco Finesse, Calabrio ONE and Cisco Unified Intelligence Center, and **no Salesforce org**. Data migration **is** in scope, inside the 10-week configuration phase |
| Client reverse demo, 2025-07-29 | 96 minutes walking the current stack. Oracle Service Cloud as a .NET desktop app since 2012, Verint, Cisco. No Salesforce anywhere in the agent workflow |
| Tony McCune in Slack, 2026-09-14 | "We are already supporting their current org which uses another BYOT solution on commercial cloud... Kicksaw setup the org originally... We are migrating their processes from one service cloud to another" |

The 2026-09-02 internal session recorded four conflicting accounts of scope across Tony McCune's verbal description, the IKT document, and two SOW versions, on a project that had been in flight 427 days through at least three handoffs. The 2026-09-03 review resolved which paper governs (the most recently signed, client-redlined SOW) and the team agreed not to reopen scope with the client at kickoff, since they have already signed. Resolving which document governs is not the same as resolving what gets built. The guidance at the time was to treat the scope question as open and record both framings until it was settled.

**Resolved 2026-09-15 (D1, Decided):** no standard Salesforce org migration is in scope. The migration is Oracle Service Cloud to Salesforce Government Cloud. Mark Hubers confirmed at discovery session 1 that Oracle and telephony are the only systems in the specialist workflow, and the Government Cloud target org is already provisioned with Mark Hubers and Jennifer Macabeo granting access. The conflicting accounts above are kept as history; the "Salesforce call center environment" wording in the IKT and Tony McCune's Slack description do not describe the NCI CIS agent workflow.

## Change log

| Date | Change |
| --- | --- |
| 2026-09-24 | Created. The live scope tracker named as source of truth, with a snapshot procedure; goal, workstream summary, scope-shaping decisions and tracker conflicts recorded |
| 2026-10-01 | Became the single home for scope. The scope history and the D1 resolution moved here from the project CLAUDE.md, which now only points to this document |

# Fred Hutch NCI/CIS Service Center Migration

**What this file is for.** Working rules for Claude Code and any other assistant in this repository: what names mean, which surfaces may be written to and when, how the RAID Log and Notion are handled, and the hard rules. It is loaded automatically at the start of every session. For what the project is, its scope at a high level, who's who and where things live, read [README.md](README.md) first. For the list of every document, read [project/README.md](project/README.md).

Kicksaw delivery engagement. Ben Bolding is the Principal Solution Architect. Kicked off 2026-09-08, 24 weeks, target go-live Wednesday 2026-01-27.

**The client:** Fred Hutch Cancer Center operates the National Cancer Institute Cancer Information Service (NCI CIS) contact center under contract to NCI. Adrianna Gutierrez described it on the kickoff as "an NCI contract, we are contractors for the National Cancer Institute," running about 35 years at Fred Hutch. Roughly 40 to 45 agents, nearly all remote, bilingual English and Spanish, about 10 inbound numbers, hours 9 a.m. to 9 p.m. ET.

## Premise

The work replaces the NCI CIS contact center stack (Oracle Service Cloud, Cisco Finesse and Verizon IVRs, Verint) with Salesforce Service Cloud and Voice in Government Cloud, Amazon Connect in AWS GovCloud, and Calabrio.

**Scope lives in one place: [project/project-scope.md](project/project-scope.md).** Read it before stating, writing or filing anything about what is or is not in scope, including RAID rows, client questions and status drafts. It names the team's live Scope Tracker in Google Drive as the source of truth and says how to read and snapshot it. This file carries no scope detail of its own: do not infer scope from anything here, and record scope changes only in that document. The root [README.md](README.md) carries a short dated summary of it for orientation; when scope changes, update that summary in the same change.

## Environment posture

**Which environment a name refers to** is defined in the Environments section of [project/README.md](project/README.md#environments): every system we connect to, its identifiers, access and status. Three rules to apply everywhere:

- **"Oracle" alone means the Oracle test instance** (`NCI__TST`, `https://nci--tst.cx.usg.oraclecloud.com`), the only Oracle environment we connect to. Kicksaw has no access to Oracle production; say "Oracle production" explicitly when you mean it.
- **"Production" alone means Salesforce production**, the connected Government Cloud org below. It never means Oracle production.
- **A Salesforce sandbox is always named.** None exists as of 2026-09-23.

- Target is Salesforce Government Cloud, per the SOW. That part is settled.
- **The target org is provisioned and connected as of 2026-09-16.** Org ID `00Dcs00000LoZ05EAF`, named "Fred Hutchinson Cancer Center - NCI Call Center GovCloud Plus Org", Unlimited Edition, production (not a sandbox), instance `USA9014`, My Domain `fredhutchnci.my.salesforce.com`. Note the org name says GovCloud Plus, which is authorized at FedRAMP High. That does not change the project's compliance obligation: High controls are a superset of Moderate, so a High-authorized platform satisfies a Moderate system, and the required level comes from the data categorization rather than the platform's maximum authorization. The project adheres to Moderate. No conflict with Calabrio.
- **The AWS partition is settled: GovCloud, `us-gov-west-1`.** Confirmed 2026-09-14 (D2). Amazon Connect runs in no other GovCloud region, and the partition is `aws-us-gov` with no cross-partition integration to commercial Lex, Lambda, Kinesis, S3 or CloudWatch. This supersedes Ken Daugherty's kickoff guidance that 80 to 90 percent of FedRAMP moderate customers build commercial.
- **FedRAMP moderate.** High is not a stated requirement. Calabrio supports moderate only and cannot support high. The IKT's reference to "FedRAMP Level 3" is almost certainly a transcription error, since FedRAMP has Low, Moderate and High.
- All integrations must reside inside the Government Cloud boundary. Standard AppExchange packages with external integrations cannot simply be installed.
- No one at Kicksaw has prior FedRAMP or GovCloud delivery experience. Sahil Kumar has roughly three years of public sector experience and is the only depth on the team. Becoming internally credible on GovCloud is an explicit team goal.

## Teams

**Kicksaw**

| Person | Role |
| --- | --- |
| Hannah Oanca | Engagement Manager |
| Avi Rabinovitch | Lead Solutions Consultant, primary point of contact for requirements. Replaced Jon Conway on 2026-09-10. Runs client calls; Los Angeles |
| Ben Bolding | Principal Solution Architect |
| Sarah Tirey | Project Manager, from 2026-09-23. Replaced Claire Jacobs. Owns the RAID Log, the client-facing timeline and the Notion hub page, and syncs with Mike Griffin as Fred Hutch's PM (slack:#internal_fredhutchinson_nci, 2026-09-25). Claire's register rows (project management tooling, D5; discovery meeting cadence, D7) still sit with Avi Rabinovitch as a holding position |
| Ian Devlin | Lead Salesforce Administrator, owns build and configuration |
| Sahil Kumar | VP of Delivery, escalation and FedRAMP depth |
| Kenny Goldman | CEO, executive sponsor |
| Tony McCune | GM, HLS Practice, holds the broader Fred Hutch relationship |

**Fred Hutch / NCI CIS**

| Person | Role |
| --- | --- |
| Mike Griffin | Fred Hutch Project Manager and **Product Owner**, confirmed at kickoff |
| Adrianna Gutierrez | Program Director, NCI Contact Center. 21 years, former Business Applications Manager, built most of the Oracle workspace, manages the contracts and correspondence with the government |
| Mark Hubers | Business Application Manager, CIS, a little over 5 years. Hands-on configuration and tier 1 to 1.5 support |
| Jennifer Macabeo | Systems Administrator, 21 years with the contact center, started with Adrianna |
| Holly Fernandez-Johnson | Manager of the Contact Center |
| Reynaldo "Ray" Quijano | Workforce Manager. 7 years at CIS, new in the role. Pulls reports, owns scheduling |
| Reetu Ghumman | Budget Analyst, about 15 years, started as an information specialist in the same cohort as Holly |
| Suchi Panda | Manages the Fred Hutch cloud team |

Adrianna, Reetu, Holly, Jennifer and Mark are the core CIS systems and user administrator team. Everyone from Fred Hutch except Mike Griffin is on it, all configure the current platforms, and Mark expects them to configure the new one. Melissa leads the knowledge base team.

**Partners:** Chris Holman (Calabrio, Account Executive), Trevor Holt (Calabrio, PM), Ken Daugherty and Binu Pazhoor (AWS).

**Roster caveats.** The kickoff deck predates the call and is wrong in four places: Nannette Ivey has left and is replaced by Ray Quijano; Stephanie Langston is replaced by Mike Griffin; the deck's open Product Owner slot resolved to Mike Griffin; and Reetu Ghumman and Suchi Panda are absent from the deck entirely. Spellings settled 2026-09-15 against the calendar invite and Chorus labels: Macabeo, Adrianna, Ghumman, Quijano. "Macavio", "Kihano" and "Guman" in older documents are transcription mangles. The IKT names **Tom Klug** and **Isabel** as client stakeholders; neither appears anywhere in the kickoff and both are unverified for this engagement, most likely belonging to the separate Fred Hutch Salesforce work.

## Live risks

- **US-only staffing. Resolved as a hard requirement.** Fred Hutch emailed on 2026-09-09 saying they "would like to keep staffing to US employees." The soft phrasing reads like a preference; it is not. It applies to everyone staffed on this engagement. See Q1 and R1.
- **Timeline compression.** Client wants January 1 rather than January 27, because the Oracle contract renews and NCI does not want to double-pay. Internally read as a push toward 12 weeks against a 24-week SOW.
- **Oracle data is the biggest unknown.** Shape, quality and completeness are unverified. The client states caller records are purged on a rolling basis; that claim is not fully trusted internally and needs verification against an actual export.
- **Calabrio timeline mismatch.** Calabrio's own implementation cycle runs roughly 20 weeks against a 10-week build window, and its Government Cloud readiness is unverified. No Salesforce-to-Calabrio integration requirement exists today; chat into Calabrio is a nice-to-have only.
- **AWS ownership gap.** If GovCloud is chosen, who spins up and manages the new AWS organization is unanswered. Suchi Panda flagged it as "a very big ask" if it lands on the Fred Hutch cloud team.
- **Relationship history.** A prior Kicksaw implementation left unmet assumptions and the client asked for a different team. First impressions and proactive communication matter more here than usual.

## Orientation

- **Start at [README.md](README.md)**, the project orientation for the team and their assistants, then [project/README.md](project/README.md), the single index of everything in this workspace
- **Transcripts:** client calls live in the [Fred Hutch Transcripts](https://app.notion.com/p/86bd4b8774178253913101a054ef9a85) database in Notion (data source `593d4b87-7417-83f7-bfc8-0789adf965d3`), the source of truth. Read and cite them there. [discovery/transcripts/README.md](discovery/transcripts/README.md) holds the conventions, the intake routes, and the index that maps each call to its Notion page and any local working copy. No transcript is committed to git
- **Decisions:** [pm/raid/decision-register.csv](pm/raid/decision-register.csv) is the register. [decision-register-guide.md](pm/raid/decision-register-guide.md) is how a human edits it
- **Sync:** [project/sync-manifest.md](project/sync-manifest.md) records what has been pushed where. The Notion and Jira split is settled; see Which surface for what, below
- **Working surfaces:** the section below maps every place this engagement lives: the repo, Notion, Jira, Slack, the org, and the file shares

## Working surfaces

The engagement lives in six places. The local repo is the drafting source of truth. Everything else is where the team reads, tracks, talks or stores. **Reading any of them is free. Writing to any of them happens only on Ben's explicit direction**, and every push is recorded in [project/sync-manifest.md](project/sync-manifest.md).

| Surface | Where | What it carries |
| --- | --- | --- |
| Local repo | `/Users/ben/Desktop/Salesforce Projects/Fred_Hutch`, git, branch `main`, pushed to the private GitHub repo `bbold-bb/fred-hutch-nci-migration` | Discovery documents, DX metadata, and the Oracle metadata tools. Source of truth for anything Ben drafts. Local-only material (call transcripts, the decision register, drafts awaiting review) is gitignored and never reaches GitHub |
| Notion | [Fred Hutchinson Cancer Center - NCI Service Center Migration (SOPS)](https://app.notion.com/p/a59d4b877417832abac401ee25d13daa), at `Delivery Home / SOPS` in the Kicksaw workspace | The team hub. Timeline, RAID log, transcripts, meeting notes, agendas, artifacts, UAT. Kicksaw-only; Fred Hutch has no access. **The connector has read and write access as of 2026-09-18**, granted by connecting the integration to the hub page; it inherits to every database beneath |
| Jira | Project `FHCCNSMS`, "Fred Hutchinson Cancer Center - NCI Service Center Migration (SOPS)", id 13053, on `kicksaw.atlassian.net` (cloud ID `16eedb79-bb2b-46ad-aad3-8d1f00096d2d`) | Tickets, stories and build items. Classic software project, 11-status workflow, effectively empty as of 2026-09-16 |
| Slack | `#internal_fredhutchinson_nci`, channel ID `C0B7MFZPFHS` | The internal team channel and a first-class source. Search it the way you would search transcripts, and cite it as `slack:#internal_fredhutchinson_nci` plus the date |
| Salesforce | `fredhutchinson_cis@kicksaw.com`, org ID `00Dcs00000LoZ05EAF`, alias `FredHutch-GovCloud`, `fredhutchnci.my.salesforce.com` | The Government Cloud target org. Read freely, write only on Ben's direction |
| File shares | Kicksaw Google Drive (kickoff deck, SOW, delivery manifest, epic backlog), Lucid (three architecture and cutover diagrams), Fred Hutch SharePoint (client-owned) | Upstream source material. Inventory lives in the inbound reference table of the sync manifest |

**Slack posting is the sharpest edge.** Draft messages for Ben and never send one without his explicit go on the exact text.

### Which surface for what

Settled 2026-09-17. Notion and Jira are not interchangeable and the division is deliberate.

- **Notion is the knowledge base.** It is what the team reads and what the team's LLMs read. Transcripts, meeting notes, agendas, discovery findings, decisions, the RAID log, reference material. Treat it as the place a question about *what is true* gets answered. Internal for the most part.
- **Jira is the work.** Tickets, release items, sprints, build items. Treat it as the place a question about *what is being done and by whom* gets answered. **The goal is for Fred Hutch to work in Jira alongside Kicksaw and move their own tasks forward**, so Jira is on a path to being client-visible in a way Notion is not.
- **Level of effort lives in Jira as T-shirt sizing. Hours do not go in Jira at all.** Do not add hour estimates, time tracking or burn to Jira issues. Hours are tracked elsewhere.
- When a piece of work could go either way, ask which it is rather than guessing. Something that is both (a decision that also spawns build work) gets recorded in Notion and ticketed in Jira, not duplicated wholesale.


### Notion: the SOPS hub

This is where a lot of the work lands, and where transcripts get loaded. The hub is a Kicksaw SOPS template, so some fields belong to a different engagement; see the caveat below.

| Page or database | URL | Use |
| --- | --- | --- |
| 📝 Fred Hutch Transcripts | <https://app.notion.com/p/86bd4b8774178253913101a054ef9a85> | **Where call transcripts are loaded.** Fields: Date, Meeting Type (Discovery, Refinement, Demo, Kickoff, Check-in, Other), Participants, Notes, Source Link, Status (Raw, Ready for Review, Processed, Archived), relation to Agendas and Meeting Notes |
| 📬 RAID Log | <https://app.notion.com/p/c62d4b877417826a940681acafb41f31> | Risks, Actions, Issues, Decisions. Type is one of Decision, Issue, Action, Risk. Status runs New, Hold, Open Questions, In progress, Approved, Done. Views split by type |
| 📅 Timeline | <https://app.notion.com/p/ca1d4b87741782f19fc78194347d1e71> | Phases and milestones |
| 📁 Documents | <https://app.notion.com/p/d31d4b87741783f7bf280155863d9f91> | Documents received and produced, with URL, date provided and who submitted them |
| 🗓️ This Week's Agenda | inline view on the hub, backed by the Agendas database | The running agenda. RAID items surface here when "Show in Agenda?" is checked |
| 📓 Meeting Notes | <https://app.notion.com/p/fecd4b877417827fba788146086236d9> | Notion's own meeting capture, related to Agendas |
| 📚 Artifacts | <https://app.notion.com/p/c73d4b87741783e6bc8e81554aa5b220> | Deliverables |
| 🤓 Shared Knowledge Artifacts | <https://app.notion.com/p/3ded4b87741780c1b5d4c042cff1b432> | Reference material shared across the team |
| 🗃️ Project Library | <https://app.notion.com/p/3ead4b87741781f98506e27dccd37967> | **Where Ben's write-ups go when he picks them for the team**: discovery findings, Oracle discovery, research, options notes, design baselines, admin handoffs. Kicksaw Team toggle on the hub. Inline database, data source `fcef366a-f7c6-40b5-b772-d91c7aafbd03`, properties Type, Workstream, Systems (RAID Log values), Status, As of, Visibility, Owner. **Once published, the Notion page is the live copy and the local file is frozen**; never re-push over it. **HTML files are the exception** (Ben, 2026-10-01): they're embedded as files and Ben makes decisions from the local copy, so the local file stays the source and every change is re-uploaded to replace the embed on the same page. Created 2026-09-29 |
| 🔁 UAT | <https://app.notion.com/p/5f1d4b87741783e88680016878aebbe0> | UAT feedback, typed Training, UI/UX Adjustment, Feature Request, Bug |
| 👩‍🏭 My Space | <https://app.notion.com/p/241d4b8774178378801881c93df90800> | Personal view filtered to tasks assigned to you |

**Clone provenance, verified 2026-09-17.** The hub was cloned from a Kicksaw SOPS template with a Lantern lineage. Two categories, and they are not the same risk:

- **Inert leftovers, safe to reshape.** The RAID Log's `Lantern Dept` field, its `Worksteam` picklist (Data Migration, Data 360) and `Phase/Categories`, and the Documents database's `Chartis` option under "Submitted By". These live only in our copy. The Fred Hutch RAID Log is database `c62d4b877417826a940681acafb41f31`, data source `9a2d4b87-7417-83c0-85f2-870b704fa4b0`, and it is **empty**. Lantern's RAID Log is a different object entirely (`246d4b87741781f0ae6de728809b3034`), so editing ours cannot touch Lantern's work. Reshaping these to fit NCI CIS is approved in principle and pending Ben's sign-off on the specific values.
- **Cross-project relations. Do not populate these.** Three relations point outside the Fred Hutch hub. Investigated 2026-09-17 against the theory that a shared agenda database is deliberate centralisation. It is not, or at least not universally:
  - **Transcripts `📒 Agendas & Meeting Notes` is a duplication artifact, not a design.** It resolves to `36ad4b87-7417-8193-86d8-000b1c393f07`, which lives in **Healthcare Legal Solutions under Pod 9 SPACE**. That database holds 13 rows, all June to August 2026, all one engagement's meetings (Kickoff Prep, Readout Prep, Avi PTO Prep, Data Mapping and Sprint 2 Planning). No Fred Hutch meetings, no Lantern meetings, nothing central about it. Our Transcripts database is a **duplicate of that project's Transcripts database**: both carry identical property option UUIDs (Meeting Type key `Z2Neeg`, "Discovery" option `YTMyNDg3Mzkt…`), which only happens through duplication, and the copy kept its parent's relation target. Filling that field on a Fred Hutch transcript puts a Fred Hutch backlink inside another client's project.
  - **The Agendas relation is genuinely shared with Lantern, and unresolved.** The hub's "This Week's Agenda" view, the RAID Log's `Related Meeting` relation, and the Meeting Notes `📒 Agendas` relation all resolve to `246d4b87-7417-8115-9198-000b8af5f3b2`. Lantern's own agenda view is backed by that same data source, so the two hubs share it. Our integration cannot read that data source, so **whether it holds many projects' agendas or only Lantern's is unverified and needs a human with access to look.** Against the centralisation theory: Healthcare Legal Solutions runs its own separate agendas database, so there is no single Kicksaw-wide one.
  - The `Related User Story` relation on the RAID Log, Documents and UAT points at a `User Stories` database that is inside our hub but **in the trash**, and whose picklists carry `Jarrard Migration` and `Lantern Write Ups`. Its deletion is consistent with the Notion and Jira split, since stories, sprints, releases and `Est. Hours` now belong in Jira.

  Fixing these relations, not just the picklists, is the real cleanup. Leave them alone until Ben directs the change.

**The register has moved to the Notion RAID Log. Executed 2026-09-18**, mechanics and the full RAID-to-legacy mapping in [register-to-raid-migration-plan-2026-09-18.md](pm/raid/register-to-raid-migration-plan-2026-09-18.md), exact imported values in [raid-import-2026-09-18.csv](pm/raid/raid-import-2026-09-18.csv).

**41 of the 45 rows are live as `RAID-1` to `RAID-41`**, numbered chronologically by `Raised` so the ID reads as a rough timeline. D11, Q11, R5 and R6 stayed behind. Five rows (Q1, D8, R1, R7, A3) migrated sanitised and the local register keeps their full text. **The RAID Log is now the source of truth for project substance. File new project rows there, not in the CSV.**

**Status vocabulary settled 2026-09-18.** Four terminal states, all kept because each is the end state for a different type: `Approved` (a Decision that stands), `Done` (a completed Action or Issue), `Closed` (stopped mattering without being decided or delivered), `Superseded` (another row took over, named in `Supersedes`). RAID-5 is Closed and RAID-9 is Superseded. **Notion silently defaults a blank `Status` to `New`**, so always set it explicitly; leaving it unset makes a finished item read as live work.

**`Owner` is still a text property.** Converting it to a select must happen in the Notion UI, because converting a property's type through the API spawns a duplicate. The API can drop a column, so a duplicate can be removed (verified 2026-09-29 on a scratch database; record in the salesforce-pm-agent repo at `docs/verification/2026-09-29-notion-capabilities.md`).

**Transcript linking, settled 2026-09-18.** RAID rows link to the call they came from through a **`Related Transcript`** relation into the [Fred Hutch Transcripts](https://app.notion.com/p/86bd4b8774178253913101a054ef9a85) database (`593d4b87-7417-83f7-bfc8-0789adf965d3`), with a `RAID Items` back-relation so a transcript shows every item it produced. Rules:

- **Client calls only.** Internal sessions are never added to the Transcripts database; that would be the push the hard rules prohibit. They stay as text in `Source`.
- **Where a Notion transcript exists, `Source` cites it instead of the local path**, as `Notion Transcripts: <name>`. Internal, Slack, SOW and Ben-direction citations keep their existing text, because there is nothing to replace them with.
- `Related Meeting` (Lantern's agendas) and `Related User Story` (trashed database) both **stay but are hidden in every view**, reserved for a separate project. Neither is populated. A new relation was added rather than repointing `Related Meeting`, because the API cannot alter a relation in place without spawning a duplicate.

**Done 2026-09-18: 35 of 41 rows linked**, to Discovery Session 2026-09-15 (18 rows) and the Kickoff 2026-09-08 (22 rows), five rows linking to both. Zero client-call local paths remain in `Source`.

**The 2026-09-08 kickoff transcript was loaded into the Transcripts database** at [CIS Contact Center Migration // Kickoff 2026-09-08](https://app.notion.com/p/3dfd4b877417813dbf24e7369b84f046). **Only the `## Raw transcript` section was pushed.** The local file is a Kicksaw working document, not a raw transcript: its first half carries a "Hidden slides: what the client did not see" section that the file itself marks as internal Kicksaw material, plus register-impact notes. That half stays local. **Apply the same split to any future transcript push: the verbatim section travels, the analysis does not.**

**The six rows still unlinked cannot be linked**, because they cite only internal sessions, Slack, the SOW or Ben's direction: R4, R8, Q9, Q13, R3 and D12. Five are already `Internal only`; D12 is the single legitimate Client-safe exception.

**Useful property of this relation: it independently checks the visibility rule.** A `Client-safe` row with no linkable client transcript is suspicious. Exactly one exists, RAID-7 (D12, data cleansing), and it is legitimate because its source is the executed SOW rather than a call.

**What the RAID Log is for, settled 2026-09-18.** It has two jobs at once and the design has to serve both.

- **It is the complete record**, beginning of project through today, including items already closed. Nothing is collapsed or merged to keep the current-state view tidy. `Raised` and `Approval Date` are both populated so it reads as a timeline, not a snapshot.
- **It is the working surface for surfacing questions.** Sorting and filtering are first-class: by raise date, due date, priority, completion date, owner, workstream. Different jobs get different saved views.
- **The client never sees the log itself.** Fred Hutch has no Notion access and is not getting any. Client exposure happens by pulling items out into a filtered view on a screen share, an export, or a slide. That is per-item and deliberate, which is what makes it safe to keep candid material in the log at all.

**Three rules settled 2026-09-18:**

- **The RAID Log is strictly a log.** Decisions, risks, issues and actions about the project. No commentary on how Kicksaw is working, what the team has or has not verified internally, or anything about the engagement rather than the client's systems. The [sync-manifest](project/sync-manifest.md) test governs: substance about the client's systems goes, commentary about our own process does not. This applies to everything filed after the migration, not just the migration itself.
- **The local register is not retired. Its role changes.** It stops being the team's source of truth for project substance and becomes Ben's and the assistant's working tool: analysing internal transcripts, tracking Ben's own action items, holding the context that informs calls, and feeding the project plan. It is not shared with the wider team, and it is the home for the four held rows, the full unsanitised text of the five rows that migrate sanitised, and anything else failing the log-purity rule.
- **Visibility is a property of the row, not of the view.** `Include in Status Report` answers "show this week"; it does not answer "is this showable at all". A `Visibility` select (`Client-safe` / `Internal only`) is proposed so that every export and client-facing view filters on Client-safe first. Until it exists, anyone building a status report from a filtered view can pull an internal row into a client deck.

**The internal/external line, settled 2026-09-18.** A RAID row is **Client-safe only if it passes both tests. Anything borderline is Internal only.**

- **Evidence.** It cites at least one source the client can see: a client call transcript, the executed SOW, or a client email. **A claim we can support only by citing our own internal conversation is not a claim we can put in front of them.** Client-visible sources today are the 2026-09-08 kickoff, the 2026-09-15 and 2026-09-17 discovery sessions, the 2025-07-29 reverse demo, the 2026-09-14 Calabrio kickoff, and the executed SOW.
- **Content.** Its Description and Resolution describe the client's systems, contract or decisions, not Kicksaw's own uncertainty, internal disagreement, commercial structure, or a candid read of the client.

**`Source` is never exported.** It stays on the row because it is what makes the log trustworthy, but it names internal transcript files and the internal Slack channel. Every client-facing view, export and deck drops the column.

A row that fails the evidence test but would otherwise be client-safe is a **work item, not a permanent state**: raising it with the client produces the citable source that flips it. Four of the 41 migrating rows are in that position (R4, R8, Q9, R3), and R3, the Oracle data unknown, is the most important of them.

**Identity decided 2026-09-17.** The local register's D, Q, R and A numbers **retire** at cutover. The Notion RAID Log's own record ID becomes the permanent unique identifier, and that is what gets cited going forward. Two things follow, and neither is done yet:

- **Done 2026-09-18: the RAID Log now has an `ID` auto-increment property**, created with prefix `RAID`, so rows cite as `RAID-1` onward. The log was empty when it was added, so numbering starts clean. The prefix is not exposed through the API and has not been visually confirmed in the UI. **Notion's unique-ID counter never reclaims numbers**, so do not create throwaway rows; a test row permanently consumes `RAID-1`.
- **Done 2026-09-18: a `Legacy Register ID` text property was added** and left empty. It holds the old D, Q, R or A value on each migrated row so that existing citations stay traceable. D1 alone is cited 22 times, Q5 ten times, Q1 nine times, across 13 files: CLAUDE.md, the discovery README, the register guide, all four system READMEs and four transcripts. **Populating it is not authorised yet**; Ben is checking with the team before any items land in the RAID Log.
- **`ID` is the first column in all five views** (All RAID Items, Risks, Action Items, Issues, Decisions), set 2026-09-18, matching how the UAT database in the same hub presents its ID. `Legacy Register ID` is hidden in all five by design: it is reference data for the assistant, not something the team reads.

**Settled 2026-09-18:** which rows carry over (41 of 45, the four holds being D11, Q11, R5 and R6), the type mapping (all 45 fit the existing four types with no picklist additions), the status mapping (`Closed` and `Superseded` need adding by hand), and numbering (**chronological by `Raised` ascending**, tie-broken by register ID, so `RAID-1` is the oldest item and the ID reads as a rough timeline). A2 and Q13 duplicate each other and both migrate as separate readable rows; `Supersedes` is a cross-reference, not a collapse.

Still open, and Ben decides with the assistant before anything moves:

- **Schema additions**: `Visibility`, `Owner Org`, converting `Owner` from text to select, and a first pass at `Priority`, which the register does not have at all.
- **The `Needed By` to `Due Date` conversion**, which lands roughly 15 open rows visibly overdue because discovery weeks 1 and 2 have passed.
- **Drift on the migrated rows**, proposed as a `RAID ID` column in the CSV and freezing those rows as local history.
- **Whether the assistant may now edit the local CSV directly**, given the audience change above.
- **The four template leftovers**: `Files & media 1`, `Phase/Categories`, `Related Meeting`, `Related User Story`.
- What happens to `register-evidence/`, which has no counterpart in the RAID Log.

## Repo layout

| Path | Contents |
| --- | --- |
| `README.md` | Project orientation for the team and their AI assistants: what the project is, who's who, where the work lives, the repo map, and what stays local. Added 2026-10-01 |
| `project/` | How the engagement runs: `README.md` (the document index and the Environments table), `project-scope.md`, `sync-manifest.md`, `notion-conventions.md`, the SOW alignment, and `reference/` (public source documents). Local only: ways of working, `scope-tracker/` |
| `oracle/` | Source system, Oracle Service Cloud: the org summary, console checklists, `tools/` (metadata pull and data profiling scripts) and `extracts/` |
| `salesforce/` | Target system, the Salesforce Government Cloud org: documents about the org and its platform decisions (security baseline, voice, SMS, chat). The org's metadata is in `force-app/` |
| `migration/` | Work spanning both systems: the mapping framework, system landscape, visuals. Field mapping, the data migration plan and the cutover plan go here |
| `discovery/` | The discovery sessions: template, guides, agendas, client requests. `discovery/transcripts/` holds local working copies of calls, client and internal, plus the README index and `_TEMPLATE.md`; the whole folder is gitignored and client calls live in the Notion Transcripts database |
| `pm/` | The PM agent's working area. `raid/` holds the local decision register, its guide, evidence and the RAID migration plans; `extracts/` holds run outputs. Gitignored except its README, until the register moves through the PM agent |
| `archive/` | Superseded documents by month. Gitignored except its README |
| `*/extracts/` | Local data pulls. Gitignored. Never commit, never send anywhere |
| `sfdx-project.json` | Salesforce DX project root, added 2026-09-16. `sourceApiVersion` 67.0, matching the org |
| `force-app/main/default/` | Metadata for the Government Cloud org. Empty until the first retrieve |
| `manifest/package.xml` | Retrieval manifest. Still the stock code-types-only file; not yet tailored to this engagement |
| `config/`, `.vscode/` | Scratch org definition, editor settings |
| `package.json` and toolchain | eslint, jest, prettier, husky. Dormant until someone runs `npm install`. See the prettier rule below |

## Hard rules

- **Client data never enters version control and never leaves this machine.** Real Fred Hutch or NCI data may live locally under an `extracts/` folder. It is never committed, never pushed to Notion, Jira, SharePoint, or any external service, and never attached to a message. Treat it as restricted federal information by default.
- **GitHub is the only remote: the private repo `bbold-bb/fred-hutch-nci-migration`, shared only with people Ben invites.** It lives in Ben's personal account because the Kicksaw-Consulting org gives its Engineering team admin on every repo, so access there can't be limited. Push only on Ben's explicit direction, and never add another remote without it. The `main` branch history starts fresh on 2026-10-01. The earlier commits stay on the local `master` branch and are never pushed, because they hold a client call transcript and the local register. Anything gitignored under "Local only" stays on this machine.
- **Client call transcripts are not committed.** The [Fred Hutch Transcripts](https://app.notion.com/p/86bd4b8774178253913101a054ef9a85) database in Notion is their home. Local copies under `discovery/transcripts/` are gitignored working files, and documents cite the Notion transcript, not the local file. Decided by Ben 2026-09-30. The 2026-09-08 kickoff transcript was committed before this rule and remains only in the local `master` history.
- **Internal Kicksaw calls are gitignored by the `-internal-` filename pattern.** They hold candid client-relationship, capacity and commercial material. Never push one to Notion, Jira, SharePoint or any client-visible surface. Quote from one only through a client-safe deliverable.
- **Two 2026-09-08 sessions are excluded from this repo entirely**, not merely gitignored: the Sahil / Ben 1:1 and the post-kickoff debrief. Their project-relevant substance was extracted into `2026-09-08-internal-kickoff-day-context.md`; the raw transcripts are not reproduced anywhere here. Do not re-import them.
- **The register: propose, never apply.** Never silently edit or renumber rows. Propose changes and let Ben apply or approve them. IDs are permanent once assigned. **This rule stands today.** Its original reason was that the register is shared with the team including the PM; the 2026-09-18 decision above changes that audience to Ben and the assistant, so whether the assistant may edit the local CSV directly after migration is an open question for Ben. Propose-only for the Notion RAID Log either way.
- **Org access exists as of 2026-09-16.** `fredhutchinson_cis@kicksaw.com`, org ID `00Dcs00000LoZ05EAF`, alias `FredHutch-GovCloud`, set as the project-local default target org. Read operations (describes, SOQL, metadata retrieve) are fine. Deploys, DML and anything that writes to the org happen only on Ben's explicit direction.
- **Nothing syncs anywhere autonomously.** Every push and pull to Notion, Jira or SharePoint happens on Ben's explicit direction.
- **Do not remove the documentation guard in `.prettierignore`.** The DX toolchain's `lint-staged` config runs `prettier --write` on staged `*.md`. Without the guard, every commit would re-pad markdown tables and normalize list and heading markers across the discovery docs, producing large whitespace-only diffs on files the team reviews. `*.md`, `CLAUDE.md` and the seven document folders are excluded deliberately.
- **No em dashes in any document.**
- **Every new document gets a row in `project/README.md`.** That file is the single index.
- **Every folder has a README that states its purpose.** A new folder gets one in the same change.
- **File a document by system.** One system: `oracle/` or `salesforce/`. Both systems: `migration/`. A discovery session: `discovery/`. How the engagement runs: `project/`.
- Client-facing deliverables produced as Office files are Kicksaw-branded: use the `kicksaw-branding` skill for identity and `kicksaw-deliverable-build` for construction. Markdown working documents stay plain.

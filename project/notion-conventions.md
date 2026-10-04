# Notion conventions

How the Fred Hutch hub in Notion is laid out, what each part is for, and the rules for writing to it. Verified against the live hub on 2026-09-24 by a read-only sweep. Internal Kicksaw document.

Notion is the team's knowledge base: what is true. Jira holds the work. Fred Hutch has no Notion access and is not getting any; client exposure is always a deliberate, per-item pull into a screen share, export or slide.

## The hub

[Fred Hutchinson Cancer Center - NCI Service Center Migration (SOPS)](https://app.notion.com/p/a59d4b877417832abac401ee25d13daa), at Delivery Home / SOPS. Cloned from a Kicksaw SOPS template on 2026-09-16, which is why some parts still point at other clients (see [Cross-client hazards](#cross-client-hazards)).

| Part | ID (data source) | Rows | State |
| --- | --- | --- | --- |
| 📬 RAID Log | `c62d4b877417826a940681acafb41f31` (`9a2d4b87-7417-83c0-85f2-870b704fa4b0`) | 41 | **In use.** The project log. See below |
| 📝 Fred Hutch Transcripts | `86bd4b8774178253913101a054ef9a85` (`593d4b87-7417-83f7-bfc8-0789adf965d3`) | 6 | **In use.** Client call transcripts. See below |
| 🤓 Shared Knowledge Artifacts | `3ded4b87741780c1b5d4c042cff1b432` | 2 | In use: the session 3 client-facing guide, and a blank "User Story/AC Skill" page |
| 📚 Artifacts | `c73d4b87741783e6bc8e81554aa5b220` | 2 | Template rows only ("Lucid Diagrams", "Google Drive"), links empty |
| Documents | `d31d4b87741783f7bf280155863d9f91` (`fd0d4b87-7417-8352-92fd-079999599aae`) | 0 | Unused |
| 📓 Meeting Notes | `fecd4b877417827fba788146086236d9` (`b22d4b87-7417-8303-a84a-8765394f5feb`) | 0 | Unused |
| 🔁 UAT | `5f1d4b87741783e88680016878aebbe0` (`ff5d4b87-7417-8213-83d6-07701ee40f7a`) | 0 | Unused until UAT |
| 👩‍🏭 My Space | `241d4b8774178378801881c93df90800` | | Personal views: RAID items assigned to you (none are assigned yet), and an agenda view of **Lantern's** calendar |
| 📅 Timeline | `ca1d4b87741782f19fc78194347d1e71` | 0 | **Broken.** A view of the trashed User Stories database; it will always be empty |
| This Week's Agenda (hub, right column) | Lantern's Agendas (`246d4b87-7417-8115-9198-000b8af5f3b2`) | | **Shows Lantern's calendar**, 544 Lantern rows, none for Fred Hutch |
| Open Action Items & Requests (hub body) | RAID Log | | Inline view of the RAID Log with 6 tabs; its Open RAID tab shows `Source` and `Related Meeting` |
| User Stories | `5ddd4b87741782b491c8816f3da5929c` | 0 | **In the trash.** Carries Jarrard and Lantern schema |

## RAID Log

**What it is for.** Two jobs at once. It is the complete record of the project's risks, actions, issues and decisions from the start, closed items included, and nothing is merged away to tidy the current view. It is also the working surface for raising questions, so sorting and filtering by raise date, due date, priority, owner and workstream are first-class.

**What goes in.** Decisions, risks, issues and actions about the client's systems, contract and decisions. Not commentary on how Kicksaw is working or what we have not yet verified internally; that stays in the local register.

**The local register** ([decision-register.csv](../pm/raid/decision-register.csv)) is now Ben's and the assistant's working tool. It holds the four rows that never migrated (D11, Q11, R5, R6), the full text of the five rows that migrated sanitised (Q1, D8, R1, R7, A3), and anything that fails the log-purity rule. File new project rows in the RAID Log, not the CSV.

### Properties and how to fill them

| Property | Type | Fill with |
| --- | --- | --- |
| Name | title | A short statement of the item |
| ID | unique ID, prefix `RAID` | Automatic. **The permanent identifier; cite as `RAID-nn`.** Numbers are never reclaimed, so never create a throwaway row |
| Type | select | Decision, Issue, Action, Risk |
| Status | status | Always set it explicitly; Notion defaults a blank Status to New. See below |
| Priority | select | Critical, High, Medium, Low |
| Visibility | select | Client-safe or Internal only. See below |
| Owner | **text** | The owner's name. Converting to a select must be done in the Notion UI; the API cannot drop the column and an in-place conversion leaves a duplicate |
| Owner Org | select | Kicksaw, Fred Hutch, AWS, Calabrio |
| Workstream | select | Scope, Architecture, Security & Compliance, Data Migration, Knowledge, Telephony, WFM/QM, Reporting, Delivery Ops, Commercial |
| Systems | multi-select | Oracle SC, SF Source, SF GovCloud, Amazon Connect, Calabrio, All, N/A |
| Raised | date | When the item arose |
| Due Date | date | When it must close |
| Approval Date | date | When it reached a terminal status |
| Description, Resolution, Mitigation | text | Mitigation for Risks |
| Source | text | Where the claim comes from. Cite `Notion Transcripts: <name>` where a Notion transcript exists; otherwise the internal file, Slack, SOW or Ben's direction. **Never exported** |
| Supersedes | text | For a Superseded row, which row took over |
| Legacy Register ID | text | The old D, Q, R or A number, populated on all 41 migrated rows. Reference only; hidden in every view |
| Related Transcript | relation | The Fred Hutch Transcripts row the item came from. Client calls only |
| Depends On, Blocks | relation | Other RAID rows |
| Include in Status Report, Show in Agenda? | checkbox | Unused so far |
| Assigned To | person | Unused so far |
| Related Meeting, Related User Story, Phase/Categories, Files & media 1 | | **Do not populate.** See hazards |

Row templates exist for each type: 🏹 New Action, 🎯 New Decision, ‼️New Risk, 🔔 New Issue.

**Status.** Four live states (New, Hold, Open Questions, In progress) and four terminal ones, each the end state for a different kind of row: `Approved` (a Decision that stands), `Done` (a completed Action or Issue), `Closed` (stopped mattering without being decided or delivered), `Superseded` (another row took over, named in Supersedes).

**Numbering.** RAID-1 to RAID-41 are the rows migrated on 2026-09-18, numbered by Raised date so the ID reads as a rough timeline. New rows take the next number automatically.

### Visibility: client-safe or internal

Visibility is a property of the row, not of the view. A row is **Client-safe only if it passes both tests; anything borderline is Internal only.**

- **Evidence.** It cites at least one source the client can see: a client call, the executed SOW, or a client email. A claim we can support only from our own internal conversation cannot go in front of the client.
- **Content.** Its Description and Resolution describe the client's systems, contract or decisions, not Kicksaw's own uncertainty, internal disagreement, commercial terms, or a candid read of the client.

`Include in Status Report` answers "show this week", not "is this showable at all". Every client-facing export or view filters on Client-safe first and drops the Source column. A row that fails only the evidence test is a work item: raising it with the client produces the citable source that flips it.

As of 2026-09-24: 29 Client-safe, 12 Internal only.

### Views

| View | Where | Shows | Known issue |
| --- | --- | --- | --- |
| All RAID Items | RAID Log database | Everything | |
| Risks, Issues, Decisions | RAID Log database | One type each | Show the dead `Related User Story` column |
| Action Items | RAID Log database | Actions with Show in Agenda? checked | **Always empty today**: no row has the box checked |
| Open RAID, Risks, Actions, Issues, Decisions, Completed RAID | Hub home page, inline | Open or completed items | Open RAID shows **Source** and the dead `Related Meeting` column, and does not lead with ID. Mind this on a screen share |

No view filters on Visibility yet. Build a Client-safe view before the first client-facing export.

## Transcripts

**Client calls only.** Internal sessions never go in; they stay in the repo as gitignored `-internal-` files.

**Only the verbatim transcript travels.** A local transcript file is a Kicksaw working document; its analysis, hidden-slide notes and register impacts stay local. Push the `## Raw transcript` section only.

**How rows arrive today.** One row (the 2026-09-08 kickoff) was loaded by hand. The other five appear to come from a tl;dv integration (inferred from their content; the creator could not be read). tl;dv rows carry AI-written notes with date errors, Participants with names and email addresses run together, and no Status.

| Property | Use |
| --- | --- |
| Date | The call date. Check it: the kickoff row reads 2026-09-18 and should read 2026-09-08 |
| Meeting Type | Discovery, Refinement, Demo, Kickoff, Check-in, Other |
| Status | Raw, Ready for Review, Processed, Archived. Set it; five rows have none |
| Participants, Notes, Source Link | As received |
| RAID Items | Back-relation from the RAID Log's Related Transcript |
| 📒 Agendas & Meeting Notes | **Do not populate.** See hazards |

Linking a RAID row to its transcript also checks the visibility rule: a Client-safe row with no linkable client transcript is suspicious unless its source is the SOW.

## Cross-client hazards

The template clone left parts of the hub pointing at other clients' databases. Writing to any of them puts Fred Hutch material inside another client's project.

| Hazard | Points at | Rule |
| --- | --- | --- |
| RAID Log `Related Meeting`, Meeting Notes `📒 Agendas` | Lantern's Agendas database (544 Lantern rows) | Never populate |
| Transcripts `📒 Agendas & Meeting Notes` | A Healthcare Legal Solutions database under Pod 9 SPACE (`36ad4b87-7417-8193-86d8-000b1c393f07`) | Never populate |
| `Related User Story` on the RAID Log, Documents and UAT; the Timeline | The trashed User Stories database, with Jarrard and Lantern schema | Never populate; never restore without deciding its future |
| This Week's Agenda, My Space agenda view | Lantern's calendar | Read nothing into it; it is not ours |
| Documents `Submitted By` option "Chartis" | Another engagement's name | Harmless, but reshape it before the database is used |

Lantern's own RAID Log (`246d4b87741781f0ae6de728809b3034`) is a separate database; editing ours cannot touch it. The connector can read other clients' areas, so a search can return their pages; check the path before using a result.

## Writing to Notion

- Every write happens on Ben's explicit direction and is recorded in the [sync manifest](sync-manifest.md).
- The connector writes only to pages the integration is connected to. The hub is connected, and that inherits to every database beneath it. A write that returns 404 on something that reads fine means the integration is not connected there.
- Always set Status explicitly. Never create a row to test something.
- Propose RAID changes; Ben applies or approves them.
- **A Project Library page opens with its summary.** The first block is one or two sentences on what the page covers, because Slack builds its link preview from the first text on the page. The same sentence goes in the Description property. Notes about the page itself (live copy, frozen local file, audience, where an embedded HTML file's source lives) go in an "About this page" section at the bottom, never in a callout at the top. Decided by Ben 2026-10-02.

## Change log

| Date | Change |
| --- | --- |
| 2026-09-24 | Created from the Notion section of CLAUDE.md and a read-only sweep of the live hub. Corrected: Visibility, Owner Org, Priority, Workstream and Systems exist and are populated; Legacy Register ID is populated; our RAID Log never had Lantern Dept or Worksteam; Related User Story is visible in four views; the Agendas database is readable and is Lantern's. Added: the hub map, the broken Timeline, the Lantern calendar views, tl;dv-written transcripts, view issues |
| 2026-10-02 | Added the rule that a Project Library page opens with its summary and carries its provenance notes in an "About this page" section at the bottom |

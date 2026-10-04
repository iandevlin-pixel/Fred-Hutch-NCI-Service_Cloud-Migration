# Fred Hutch NCI CIS service center migration

Kicksaw's working repository for the Fred Hutch NCI Cancer Information Service (CIS) contact center migration. It holds discovery documents, design research, the Oracle metadata tools, and the Salesforce DX project for the target org. It's Kicksaw-internal. Fred Hutch staff don't have access.

Owner: Ben Bolding, Principal Solution Architect.

## What the project is

Fred Hutch Cancer Center runs the CIS contact center under contract to the National Cancer Institute (NCI). About 40 to 45 remote, bilingual English and Spanish agents answer cancer questions by phone, email, chat, and SMS.

Kicksaw is replacing the contact center's Oracle Service Cloud platform with Salesforce Service Cloud in Government Cloud Plus. Calls move from Cisco Finesse and Verizon IVRs to Salesforce Voice with Amazon Connect in AWS GovCloud. Calabrio replaces Verint for workforce and quality management, delivered by Calabrio's own team.

| Fact | Value |
| --- | --- |
| Kickoff | 2026-09-08. The SOW runs 24 weeks |
| Target go-live | Wednesday, 2027-01-27. The client wants an earlier date, so treat it as open (Go-live date, RAID-16) |
| Compliance | FedRAMP Moderate. Every integration stays inside the government cloud boundary |
| Staffing | Fred Hutch requires the delivery team to be US employees |

## Scope at a high level

This is a summary. The team's live [Scope Tracker](https://docs.google.com/spreadsheets/d/1tqBE3dywkXV_XJvXEzY1aa3HvHwSS9EAHdzl_YR2A_k/edit) in Google Drive is the source of truth, and the executed SOW is the contract. [project/project-scope.md](project/project-scope.md) explains how to read the tracker, the decisions that shape scope, and where the tracker and a settled decision disagree. Read it before you tell anyone what is in or out of scope. Statuses here are as of the tracker copy taken 2026-09-24.

**What Kicksaw builds**

| Area | What it covers |
| --- | --- |
| Discovery and planning | Requirements workshops, the current-state review, the project plan |
| Salesforce Service Cloud | Case management for inquiries, the agent workspace, the knowledge base inside the console |
| Telephony and channels | Salesforce Voice with Amazon Connect in AWS GovCloud for calls and the phone menu, in English and Spanish. Email, chat, and text messages on the Salesforce side |
| Real-time reporting | Supervisor and operational reporting in Salesforce |
| Compliance and security | A FedRAMP Moderate configuration inside the government cloud boundary |
| Testing | System integration testing and support for user acceptance testing |
| Training and go-live | Training materials for trainers, and the go-live itself |
| Hypercare | Support for the four weeks after go-live |

**What Kicksaw doesn't build**

| Item | Who owns it |
| --- | --- |
| AWS accounts and AWS configuration | The Fred Hutch cloud team and AWS. Kicksaw builds the Salesforce side of Voice |
| Calabrio workforce and quality management, and call recording | Calabrio's services team. Kicksaw keeps the Salesforce side visible to it |
| Knowledge article content | The CIS knowledge team |
| Data cleansing and deduplication | Fred Hutch |
| Delivering training sessions | Fred Hutch |
| Support after week 24 | A separate contract |
| Hardware and network upgrades | Fred Hutch |

**What is still open**

- **Data migration.** Fred Hutch tentatively decided on 2026-09-17 to start fresh on data. Knowledge articles, scheduled callbacks, and work in flight at cutover are the exceptions. NCI hasn't confirmed.
- **Callback reminder texts.** The product that sends them isn't settled.
- **The go-live date.** See RAID-16 in the RAID Log.

## Who's who

| Kicksaw | Role |
| --- | --- |
| Hannah Oanca | Engagement Manager |
| Avi Rabinovitch | Lead Solutions Consultant. Runs client calls |
| Ben Bolding | Principal Solution Architect |
| Sarah Tirey | Project Manager. Owns the RAID Log and the timeline |
| Ian Devlin | Lead Salesforce Administrator. Owns build and configuration |
| Sahil Kumar | VP of Delivery. Escalation |
| Tony McCune | GM, HLS Practice |
| Kenny Goldman | CEO, executive sponsor |

| Fred Hutch | Role |
| --- | --- |
| Mike Griffin | Project Manager and Product Owner |
| Adrianna Gutierrez | Program Director, NCI Contact Center |
| Mark Hubers | Business Application Manager. Grants Oracle access |
| Jennifer Macabeo | Systems Administrator |
| Holly Fernandez-Johnson | Contact Center Manager |
| Ray Quijano | Workforce Manager |
| Reetu Ghumman | Budget Analyst |
| Suchi Panda | Manages the Fred Hutch cloud team |

Partners: Calabrio (Chris Holman, Trevor Holt) and AWS (Ken Daugherty, Binu Pazhoor). For how NCI, CIS, Fred Hutch, and Kicksaw fit together, see the [who's who diagram](migration/cis-organizations-2026-10-01.html). GitHub shows HTML as source code, so download it and open it in a browser.

## Where the work lives

| Place | What it holds |
| --- | --- |
| This repository | Working documents, the Oracle metadata tools, and the Salesforce DX project |
| [Notion hub](https://app.notion.com/p/a59d4b877417832abac401ee25d13daa) | The team's knowledge base: [RAID Log](https://app.notion.com/p/c62d4b877417826a940681acafb41f31), timeline, [call transcripts](https://app.notion.com/p/86bd4b8774178253913101a054ef9a85), meeting notes, and the [Project Library](https://app.notion.com/p/3ead4b87741781f98506e27dccd37967). Kicksaw only |
| [Jira project FHCCNSMS](https://kicksaw.atlassian.net/browse/FHCCNSMS) | Tickets and build work, sized in T-shirt sizes. No hours. Fred Hutch is expected to work here alongside Kicksaw |
| [Slack #internal_fredhutchinson_nci](https://kicksaw.enterprise.slack.com/archives/C0B7MFZPFHS) | The team channel |
| Salesforce production | The Government Cloud Plus org at `fredhutchnci.my.salesforce.com`. No sandbox exists yet |
| Oracle test instance | `NCI__TST`, a copy of Oracle production. Kicksaw reads its configuration and metadata only, and has no access to Oracle production |
| Google Drive | The Scope Tracker, the SOW, and the kickoff deck |

**Notion is the live copy of a published document.** When a document here is published to the Notion Project Library, a note at the top of the file says so and links the page. Edit the Notion page, not the file. HTML files are the exception: the file in this repository stays the source, and each change is uploaded again to Notion.

## How this repository is organized

| Path | Contents |
| --- | --- |
| [project/](project/README.md) | How the engagement runs. Its README is the index of every document and holds the Environments table that defines what each system name means. Also here: [project-scope.md](project/project-scope.md), the sync manifest, the Notion conventions, and public source documents |
| [oracle/](oracle/README.md) | The source system, Oracle Service Cloud: the org summary, the console capture checklists, and `tools/`, the Python scripts that pull Oracle metadata and profile its data |
| [salesforce/](salesforce/README.md) | The target org and its platform decisions: the FedRAMP Moderate security baseline, pre-sandbox build tasks, and the voice, SMS, and chat research |
| [migration/](migration/README.md) | What spans both systems: the Oracle to Salesforce mapping framework, the system landscape, and the visuals. Field mapping, the data migration plan, and the cutover plan go here |
| [discovery/](discovery/README.md) | The discovery sessions: the template, each session's guide and agenda, and the requests sent to the client |
| [pm/](pm/README.md) | The PM agent's working area. Its contents stay on Ben Bolding's machine for now |
| [archive/](archive/README.md) | Superseded documents. Its contents stay on Ben Bolding's machine |
| `force-app/`, `manifest/`, `config/`, `sfdx-project.json` | The Salesforce DX project for the Government Cloud org, API version 67.0. It sits at the root because the Salesforce CLI and the VS Code extensions expect it there. `salesforce/` holds documents about the org; `force-app/` holds the org's metadata |
| [CLAUDE.md](CLAUDE.md) | Working rules and conventions for Claude Code and for anyone writing in this repository |
| `pm-project.yaml` | The project profile (people, Notion and Jira identifiers) that the PM agent skills read |

## What's not in this repository

| What | Where it lives |
| --- | --- |
| Call transcripts | The [Fred Hutch Transcripts](https://app.notion.com/p/86bd4b8774178253913101a054ef9a85) database in Notion |
| Internal call notes and internal prep documents | Ben Bolding's machine only |
| The local decision register | Ben Bolding's machine, until it moves to the Notion RAID Log through the PM agent. The RAID Log is the team's copy |
| Scope Tracker snapshots | Ben Bolding's machine. The live tracker is in Google Drive |
| Client data and Oracle extracts | Never committed. `extracts/` folders are gitignored, and their contents never leave the machine that pulled them |
| Drafts awaiting review | Ben Bolding's machine until they're approved |

Some links in [project/README.md](project/README.md) point to these files, so they don't open on GitHub.

## Rules for everyone

- Never put client data in this repository, a commit, or a message. Treat it as restricted federal information.
- Never commit a call transcript.
- To change a published document, edit its Notion page.
- When you add a document, add its row to [project/README.md](project/README.md).
- Talk to Ben Bolding before you push to `main`.

## Where to start

1. Read this file.
2. Read [project/project-scope.md](project/project-scope.md).
3. Read [project/README.md](project/README.md), especially the Environments table. It lists every document.
4. Open the folder for the system you're working on, [oracle/](oracle/README.md) or [salesforce/](salesforce/README.md), and read its README.
5. If you use Claude Code, it loads [CLAUDE.md](CLAUDE.md) automatically. If you use another AI assistant, point it at this file and CLAUDE.md before it writes anything.

# Oracle console pull checklist

> **Frozen 2026-09-29.** Published to the Notion Project Library as [Oracle console pull checklist](https://app.notion.com/p/3ead4b87741781c2a7a4ff31806351f5). The Notion page is the live copy; edit there, not here.

This is the Oracle configuration that the Connect REST API does not expose. It has to be captured from the Oracle console, on the Oracle test instance (`NCI__TST`), by an admin with console access. The REST pull already covers the data model, every picklist value, queue names, SLA names, statuses, report columns and filters, mailboxes, standard text and event subscriptions, so none of those are on this list.

Status: saved for later. Nobody has been assigned to pull it yet. The admin's version, with the steps only, is [oracle-console-capture-admin-tasks-2026-09-28.md](oracle-console-capture-admin-tasks-2026-09-28.md). This document keeps the counts, the Salesforce targets, the path checks and the Element Manager detail.

## Before you start

- **Change nothing.** Some exports require you to open an item in its designer. When that happens, close the designer without saving.
- **Sign in only when nobody else is using `sthomas_RNT`.** The account allows one session, so signing in ends anyone else's session.
- **Download each export or screenshot to your machine, then upload it to the Google Drive folder Ben Bolding shares with you.** Keep them in that folder only, not in Slack, Notion or Jira.
- **Name each file after what it holds**, for example `workspace-nci-inquiry-v2.1.xml` or `rules-incident.png`. Don't edit an exported workspace file. Oracle hashes it, and any change makes the file invalid.
- **Where a count says "Unknown," screenshot the list first.** That screenshot gives the count, so the rest of the item can be sized before you start it.

## Objects in scope

This list is proposed. It covers the core of Oracle Service Cloud that CIS uses in the specialist workflow, and it sets which rule bases and custom objects the admin captures.

| Oracle object | What it is at CIS | In scope |
| --- | --- | --- |
| Inquiry (`incidents`) | Every phone, chat and email interaction | Yes |
| Callback task (`tasks`) | Scheduled callbacks | Yes |
| Contact (`contacts`) | The caller, often a placeholder | Yes |
| Answer (`answers`) | Knowledge articles, English and Spanish | Yes |
| Chat | Chat sessions and chat routing | Yes |
| Staff account (`accounts`) | Specialists and administrators. Profiles only, no staff records | Yes |
| Organization (`organizations`) | Present in the rules editor but not used in the specialist workflow | Rules only, if its rule base has any |
| SCIF (`SCIF` package) | Smoking cessation intake form | Yes |
| Demographics (`DEMOGR` package) | Demographics survey tracking | Yes |
| Referrals (`Referrals` package) | Referral quality checks tied to answers | Yes, pending confirmation of which workflow uses it |
| Opportunity, Asset | Sales and asset objects, not used by CIS | No |
| OpenMethods (`OpenMethods` package) | Cisco telephony bridge, retired with Service Cloud Voice | No. Its add-in settings are captured once in item 14 for reference |

## How many of each

The counts come from Oracle's own menus and schemas, pulled 2026-09-23, and from the client calls. Several settings repeat per interface, and the site has three interfaces: `nci`, `nci1` and `nci2` (Spanish).

| # | Item | Count | Where the count comes from |
| --- | --- | --- | --- |
| 1 | Workspaces and workflows | Unknown. One inquiry workspace is confirmed, NCI Inquiry v2.1, which Mark Hubers called the only inquiry workspace in use. Task, contact and SCIF workspaces are expected | 2026-09-21 Oracle tour |
| 2 | Business rule bases | 6 in scope: inquiry, task, contact, answer, chat and organization. Opportunity is out. Rules per base unknown. SCIF, DEMOGR and Referrals may hold their own rules | 2026-09-21 Oracle tour, 23:02 |
| 3 | Profiles | 40 profiles, covering 56 inquiry queues and 6 chat queues | Oracle profile and queue menus |
| 4 | Custom fields | 160 fields: 116 on inquiries, 16 on tasks, 3 on contacts, 19 on answers, and 6 Referrals attributes on answers. Organizations have none | Oracle schemas |
| 5 | Custom objects that hold settings | 7 objects, 174 fields: SCIF (1 object, 116 fields), DEMOGR (4 objects, 40 fields), Referrals (2 objects, 18 fields). The counts include system fields such as ID and created time. The 11 menu-only objects are skipped, because their values are already pulled | Oracle schemas |
| 6 | Custom processes | Unknown | None yet |
| 7 | Agent scripts and guided assistance guides | Unknown | None yet |
| 8 | Navigation sets | Unknown, at most one per profile (40) | Oracle profile menu |
| 9 | SLAs and response requirements | 0 SLAs in Oracle's SLA menu, so likely none are in use. One screenshot confirms it. Response requirements are set per interface (3) | Oracle SLA menu |
| 10 | Message templates | Unknown. Templates repeat per interface (3) | None yet |
| 11 | Surveys | At least 3: demographics, client satisfaction, and the tobacco follow-up surveys | 2026-09-17 discovery session 2, 13:36 |
| 12 | Data retention settings | 2 searches in Configuration Settings, plus the Data Lifecycle policies | None yet |
| 13 | Chat setup | 6 chat queues. Chat hours per interface (3) | Oracle chat queue menu |
| 14 | Add-ins | At least 2: OpenMethods (telephony) and the demographics pop-up add-in | Oracle schemas (3 OpenMethods objects), 2026-09-17 discovery session 2, 15:26 |

## Priority items

Pull items 1 to 3 first, then item 4. They drive the record type design, the page layouts and the routing.

| # | Item | Where | How to capture | What it becomes in Salesforce | Path |
| --- | --- | --- | --- | --- | --- |
| 1 | Workspaces and workflows: NCI Inquiry v2.1, task, contact, SCIF, and any others in the NCI folder | Configuration > Application Appearance > Workspaces/Workflows | Screenshot the folder listing. For each workspace, right-click, select **Open**, then **File** > **Export Workspace**. Close without saving | Record types, Dynamic Forms visibility by queue, page layouts | Verified |
| 2 | Business rules for the objects in scope: inquiry, task, contact, answer, chat and organization, plus any rules on SCIF, DEMOGR and Referrals | Configuration > Site Configuration > Rules. Mark Hubers also showed rules under the Database area | Use the console's export or print option if it offers one. If not, screenshot each rule base's states, rules, functions and variables | Omni-Channel routing, record-triggered flows | To confirm |
| 3 | Profiles, all 40 | Configuration > Staff Management > Profiles | For each profile, capture the **Interfaces** section (navigation set, workspace per record type) and the permissions, including queue access and pull policy | Profiles, permission sets, queue membership | Verified |
| 4 | Custom field visibility, all 160 | Configuration > Database > Custom Fields | Capture the visibility settings for inquiry, task, contact and answer fields. The REST pull already holds type, length, read-only, menu, lookup and description | Which fields agents use, so unused fields can be dropped | Verified (settings). To confirm (path) |

## Remaining items

| # | Item | Where | How to capture | What it becomes in Salesforce | Path |
| --- | --- | --- | --- | --- | --- |
| 5 | Optional: custom object field defaults for SCIF, DEMOGR and Referrals (7 objects) | Configuration > Database > Object Designer | Capture default values only. The REST pull holds everything else. Not on the admin's list; confirm during build if needed | Default values on custom object fields | To confirm |
| 6 | Custom processes (object event handlers) | Process Designer, under Site Configuration | Screenshot the list of processes and the object and event each one runs on | Apex or flows. This is automation that the business rules don't show | To confirm |
| 7 | Agent scripts and guided assistance guides, if used | Application Appearance | Screenshot the list. Export any script that has an export option | Screen flows | To confirm |
| 8 | Navigation sets | Configuration > Application Appearance > Navigation Sets | Screenshot each set's buttons and explorer items | Lightning apps per role | Verified |
| 9 | SLAs and response requirements | Configuration > Service > Service Level Agreements, and response requirements in the same area | Screenshot the SLA list and the default response requirements for each interface | Entitlements and milestones | Verified |
| 10 | Message templates | Configuration > Site Configuration > Message Templates | Screenshot or copy each template that CIS changed from the default | Email templates | Verified |
| 11 | Surveys | Survey Explorer. Blocked until Mark Hubers grants surveys access on the account | Screenshot each survey's questions and settings | Survey design (in scope under the SOW) | To confirm |
| 12 | Data retention settings | Configuration > Site Configuration > Configuration Settings (search `PURGE` and `ARCHIVE`), plus Data Lifecycle policies in the Agent Browser UI | Capture only the purge, archive and retention settings. Don't copy any setting that holds a password, key or endpoint credential | Checks the claim that caller records are purged on a rolling basis. Feeds the retention design | Verified (Configuration Settings). To confirm (Data Lifecycle path) |
| 13 | Chat setup | Chat hours, and the chat queues in the Chat rule base | Screenshot the chat hours for each interface and the settings of the 6 chat queues | Messaging hours and routing | To confirm |
| 14 | Add-in configuration: OpenMethods and the demographics pop-up | Add-In Manager in the console, or Extension Manager in the Agent Browser UI | Screenshot the add-in list, each add-in's settings (including the demographics percentage and its queues), and the profiles each add-in is assigned to | How telephony and the demographics prompt connect to the agent workspace today | To confirm |

**Path column.** "Verified" means the menu location matches Oracle's documentation, checked 2026-09-27. "To confirm" means the feature exists but the exact menu path was not confirmed, so it may sit under a slightly different name in this instance.

## Appendix: Element Manager

Element Manager is Oracle's tool for moving configuration between sites. It isn't on the account's Agent Browser UI navigation today. Ask Mark Hubers whether it can be turned on for the account, because it could replace most of the console capture.

**What it exports.** Workspaces, business rules, navigation sets, reports, custom objects, object event handlers, add-ins, standard text, variables, message bases, configuration settings, customizable menus, and products, categories and dispositions.

**What an export looks like.** One zip file per package, containing:

- `EEMManifest.xml`, which lists every item in the package and what each depends on
- `MetaData.json`, which lists the permissions the items need on a target site
- A folder per element type, for example `Report/`, holding the definitions

Oracle's documentation doesn't describe the file format of each definition inside those folders. The way to find out is one test export of a single workspace.

**It also has a REST API.** It sits at `/AgentWeb/api/elementmanager/` on the same site, and it signs in with a user name and password. It can do three things:

- Search for items by type, which would give the counts that are still unknown
- Create an export package
- Download the zip

This means the export could run from the Mac without the admin. Two things are unconfirmed. First, whether the account's profile carries the Element Manager permissions. Second, whether the API needs Element Manager on the navigation set. Creating a package is a write to the site, even though it changes no configuration, so it needs Ben Bolding's go before anyone runs it.

**The ask to Mark Hubers.** Add Element Manager (Components > Common) to the account's navigation set, and confirm the permissions for each element type: Workspace Designer for workspaces, Rules Edit for business rules, Administration for navigation sets, and Analytics Administrator for reports. The account uses it only to export.

## Sources

- [How You Export and Import Workspaces](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Exporting-and-importing-workspaces-ac1394366.html) and [Export a Workspace](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Export-a-workspace-ac1394377.html): Oracle B2C Service, the export steps, the 1 MB limit, notes excluded, the hash check
- [Customizing Profiles](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Customizing-profiles-ar1294709.html): profiles under Staff Management, with the navigation set and workspaces in the Interfaces section
- [Create a Navigation Set for the Administrator](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Create-a-navigation-set-for-the-administrator-am1206889.html): Navigation Sets under Application Appearance
- [Overview of Service Level Agreements](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-css-admin-SLAs.html): the Service Level Agreements folder under Service
- [Accessing the Process Designer](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Accessing-the-process-designer-bs1130847.html): object event handlers
- [Data Lifecycle Policies, 24D](https://docs.oracle.com/en/cloud/saas/readiness/service/24d/b2c-svc24d/24D-b2c-service-wn-f35614.htm) and [Archived Incidents](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Archiving-incidents-automatically-aa1422780.html): retention and purge policies
- [Set Chat Hours](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Set-chat-hours-ac1149758.html) and [Pull Policy](https://docs.oracle.com/en/cloud/saas/b2c-service/22a/famdg/pull-policy.html)
- [Oracle test environment tour, 2026-09-21](../discovery/transcripts/2026-09-21-oracle-test-environment-access.md) and [discovery session 2, 2026-09-17](../discovery/transcripts/2026-09-17-discovery-session-2-reports-surveys-routing-email.md): workspace, rule base, survey and add-in counts
- Oracle metadata pull, 2026-09-23, in `extracts/oracle-metadata/2026-09-23/`: profile, queue, chat queue, SLA and interface menus, custom field and custom object schemas
- [REST API for Element Manager in B2C Service](https://docs.oracle.com/en/cloud/saas/b2c-service/cxemg/c_em_quick_start.html): base path, sign-in, [search](https://docs.oracle.com/en/cloud/saas/b2c-service/cxemg/op-elementmanager-search-emelements-post.html), [create export package](https://docs.oracle.com/en/cloud/saas/b2c-service/cxemg/op-elementmanager-export-empackages-post.html) and [package contents](https://docs.oracle.com/en/cloud/saas/b2c-service/cxemg/c_em_migrate_resources.html)
- [oracle-to-salesforce-mapping-framework-2026-09-23.md](../migration/oracle-to-salesforce-mapping-framework-2026-09-23.md): the configuration inventory this checklist carries out

## Change log

| Date | Change |
| --- | --- |
| 2026-09-27 | Created from the list of Oracle configuration that the REST pull does not cover. Console paths checked against Oracle documentation |
| 2026-09-27 | Removed the record-handling guidance, since the account has no access to records |
| 2026-09-27 | Added a count for each item. Moved the Element Manager note to an appendix as a question for Mark Hubers, and removed the "Not on this list" section. Added the demographics add-in to item 14 |
| 2026-09-28 | Files go to a shared Google Drive folder instead of the repo. Added the proposed objects in scope and narrowed business rules to them. Expanded the Element Manager appendix with the export package format and its REST API |
| 2026-09-28 | Added a trimmed admin version with the steps only. Narrowed item 4 to custom field visibility and made item 5 optional, because the REST pull already holds the rest of the field definitions |

# How Oracle works, for a Salesforce team

> **Frozen 2026-10-02.** Published to the Notion Project Library as [How Oracle works, for a Salesforce team](https://app.notion.com/p/3edd4b87741781c383a7c276afbbbae5). The Notion page is the live copy; edit there, not here. The diagrams are in [oracle-concepts-visual-2026-10-02.html](oracle-concepts-visual-2026-10-02.html), which stays the source for the embed on that page.

- **Owner:** Ben Bolding
- **As of:** 2026-10-02
- **Audience:** Kicksaw consultants who know Salesforce and have never used Oracle B2C Service (the product CIS calls RightNow or Oracle Service Cloud)
- **Purpose:** for each Oracle term that shows up in calls and documents, say what it is, what it connects to inside Oracle, and the nearest thing in Salesforce. Read it before the data profile, the mapping framework, or a design session

**How to trust it.** Statements about Oracle come from Oracle's documentation, listed under Sources. Statements about CIS come from the 2026-09-21 tour of the test instance and the metadata pulled on 2026-09-23. Anything marked "inferred" is Kicksaw's reasoning and hasn't been confirmed. The Salesforce side describes standard Service Cloud behavior; three items that need a Government Cloud check are listed at the end.

## The short version

Five ideas explain most of the differences.

1. **The profile does far more in Oracle.** One Oracle profile decides what a person can do, which screens they get, which queues they can take work from, and how work is handed to them. In Salesforce that is a profile, permission sets, an app, page assignments, queue membership and an Omni-Channel presence configuration.
2. **A queue is a field value, not an owner.** An Oracle inquiry has a queue and an assigned person at the same time. A Salesforce record is owned by a queue or by a user, never both.
3. **Oracle has no record types.** One workspace (the screen layout) shows and hides tabs and fields with rules. Where Salesforce would use a record type, Oracle uses a workspace rule.
4. **An interface is a copy of the configuration.** CIS has an English interface and a Spanish one over the same database. Mailboxes, message templates, chat hours and settings are set per interface. Salesforce has one configuration with language and channel settings inside it.
5. **Logic lives in two places.** Workspace rules run on the specialist's screen while they work. Business rules run on the server when the record saves, and win when the two disagree. Salesforce splits the same work across Dynamic Forms, validation rules, Flows and routing rules.

## How the pieces connect

```text
Staff account ── has one ──> Profile
                               ├── per interface: a navigation set (menus and reports)
                               ├── per record type: a workspace or workflow (the screen)
                               ├── permissions (read, edit, send, delete)
                               ├── queues it can take work from, in rank order
                               ├── pull policy, pull quantity, inbox limit
                               └── add-ins and browser extensions

Inquiry (incident) ── has ──> primary contact (required)
                   ── has ──> queue  AND  assigned person and staff group
                   ── has ──> interface, mailbox, channel, source
                   ── has ──> thread (messages, notes, chat)
                   ── has ──> tasks (callbacks), intake form (SCIF)

Business rules (one rule base per object) ── set ──> queue, status, fields; send responses
Workspace rules (inside the workspace)    ── set ──> hidden, required, read-only, values
```

## What a queue is

This is the term most likely to mislead a Salesforce reader.

**In Oracle.** A queue is a value on a system menu (Configuration, Application Appearance, Customizable Menus, System Menus, Incident Queues). The inquiry has a `queue` field that holds one. Three things use it:

- **Business rules put inquiries into queues.** An incident rule has a "Set Field, Queue ID" action. Email arrives through the mailbox, becomes an inquiry, and rules assign its queue.
- **Profiles decide who works a queue.** The profile lists the queues its people can access, ranks them, and sets how work is taken: the pull policy (manual, strict priority, or first due), how many at a time, and the inbox limit.
- **Specialists pull work.** By default nobody is handed an inquiry. A specialist clicks Fill Inbox on a report and takes unresolved inquiries from their queues. Round-robin queue types exist for automatic assignment.

**Chat queues are a separate list.** Chats are routed by the Chat rule base into chat session queues, and chats are pushed to agents by default. The inquiry carries both a `queue` and a read-only `chatQueue`.

**At CIS.** Oracle does not route phone calls. Cisco routes the call, and the specialist then opens an inquiry and picks the service number and the queue by hand. So for phone, the queue is a label the specialist applies: it records what kind of call it was. It works as coding, not routing (inferred). That is why the data profile can use queue as a stand-in for inquiry type. Email is sorted and assigned by hand on an early shift. CIS has 51 named inquiry queues and 6 chat queues, and the two lists are separate even where the names look alike.

**In Salesforce.** Three separate things:

| Oracle queue does this | Salesforce equivalent |
| --- | --- |
| Holds waiting work | A Queue as the record owner |
| Decides who gets it and how | Omni-Channel routing configuration and queue membership (push), or a list view (pull) |
| Labels the kind of inquiry, kept after assignment | A field on the Case, or the record type |

**What it means for the build.** When a specialist takes a Case, the queue stops being the owner. If reports need "which queue did this come from" afterwards, that has to be its own field. Phone queues become Amazon Connect queues, not Salesforce queues. The labels CIS uses today for the kind of inquiry (program, channel, language) become record type and fields.

## Terms, one by one

### People and access

| Oracle term | What it is | Connected to | Salesforce equivalent | What differs |
| --- | --- | --- | --- | --- |
| Profile | Access, screens and work distribution in one object | One per staff account. Holds the navigation set per interface, a workspace per record type, permissions, queues with rank, pull policy, add-ins | Profile, permission sets, Lightning app, page assignment, queue membership, Omni-Channel presence configuration | One Oracle object becomes five or six. Queue access moves off the profile onto the queue |
| Staff account | The user | One profile; filed in a staff group | User | |
| Staff group | A folder of accounts by job duty | Stamped on the inquiry alongside the assigned person | Public group or role | Salesforce doesn't record a group on the owner |
| Navigation set | The menus, lists and reports a person sees | Assigned on the profile, per interface | Lightning app and its navigation items | Oracle's lists are mostly reports, and reports double as work lists |

At CIS: 40 profiles, 8 of them test or copies, and 8 staff groups. "Language" is not a setting on an Oracle profile. A bilingual specialist is one whose profile can reach the Spanish interface and the Spanish queues (inferred).

### Screens and logic

| Oracle term | What it is | Connected to | Salesforce equivalent | What differs |
| --- | --- | --- | --- | --- |
| Workspace | The screen layout for one record type | Assigned on the profile. Holds its own rules | Lightning record page with Dynamic Forms, page layout | No record types in Oracle |
| Workspace rules | "When this, then that" rules on the screen: hide, require, make read-only, set a value, filter a menu | Stored inside the workspace. Run before business rules | Dynamic Forms visibility, validation rules, a before-save Flow | Oracle sets values live as the specialist types. Dynamic Forms only shows and hides; setting a value needs a Flow on save or a component |
| Desktop workflow | A chain of workspaces, scripts and decisions | Assigned on the profile in place of a workspace | Screen Flow | |
| Business rules | "If this, then that" rules on the server. One rule base per object, built from states and functions | Set queues, statuses and fields, send responses, call custom code | Record-triggered Flows, assignment and escalation rules, Omni-Channel flows | One ordered rule base per object in Oracle; several automation types in Salesforce. If a record matches several rules, all of them act |
| Custom process (object event handler) | PHP code that runs when a record is created, updated or deleted | Loaded in Process Designer. Can also be called from a rule | Apex trigger or record-triggered Flow | |
| Custom script | PHP code stored in File Manager's custom scripts folder | Can be run on a schedule by the Job Scheduler | Scheduled Flow or scheduled Apex | This is where the contact scrub is believed to live |

**Where "is this field required or visible" is decided in Oracle.** Three layers, and the last one can override the others:

1. On the field: who can see and edit it (staff, customers, chat), and whether it's required.
2. On the workspace: hidden, required and read-only per screen.
3. In workspace rules: the same three, set by conditions.
4. Business rules run after all of that and can change the record anyway.

So a field's settings alone don't say whether specialists use it. The workspace export and the usage counts in the data profile do.

At CIS: one live inquiry workspace (NCI Inquiry v2.1, under NCI Workflow v1). Business rules sit under Site Configuration, Rules, with a tab per object, separate from the workspace rules.

### Records

| Oracle term | What it is | Connected to | Salesforce equivalent | What differs |
| --- | --- | --- | --- | --- |
| Incident (CIS says Inquiry) | The service record for one interaction | A primary contact (required), queue, assigned person, interface, mailbox, thread, tasks | Case | Oracle requires a contact, which is why CIS uses a placeholder contact for anonymous chats. A Salesforce Case doesn't need one |
| Status and status type | Each status maps to one of three types: Unresolved, Solved, Waiting | Inquiry | Case Status with a Closed flag | Salesforce has open or closed only |
| Thread | Every message, note and chat on the inquiry, in one list (the Messages tab) | Inquiry | Email messages, Case feed posts, Messaging Session entries, Voice Call | One list becomes several objects |
| Contact | The customer | One organization, inquiries, tasks | Contact | A Salesforce Contact with no Account is visible only to its owner |
| Organization | A company | Contacts | Account | Not used at CIS |
| Task | A scheduled activity | An inquiry or a contact. Has its own rule base | Task, or a custom callback object | At CIS each callback attempt is a new task |
| Channel and source | Channel is how the latest message arrived. Source is how the inquiry was created, set by the system and not editable | Inquiry | Case Origin | CIS added its own Point of Access and Service Number fields |

### Knowledge

| Oracle term | What it is | Connected to | Salesforce equivalent | What differs |
| --- | --- | --- | --- | --- |
| Answer | A knowledge article | Products, categories, access levels, siblings | Knowledge article | |
| Answer status | Draft, Proposed, Public, Retired and so on. CIS's live status is Internally Published | Answer | Publication status (Draft, Published, Archived) and validation status | |
| Access level | Who can see an answer. Tied to interfaces | Answer, interface | Channel visibility (internal, customer, public) | |
| Sibling answers | Separate answers that share products, categories and attachments. Often one per language | Answer | A translation of an article | An Oracle sibling is its own record. A Salesforce translation is a language version of one article and needs a master |
| Related answers | Links between answers, set by hand or learned from use | Answer | Related articles | Not the same thing as siblings |
| Products, categories | Trees, up to six levels, that group both inquiries and answers | Inquiry, answer | Data categories on Knowledge; picklists on Case | One Oracle tree serves both. Salesforce data categories don't apply to Cases |
| Dispositions | A tree for how an inquiry was resolved. Inquiries only | Inquiry | A picklist on Case | |

At CIS: English and Spanish pairs are siblings, not related answers. The article pull on 2026-10-02 found 1,784 sibling links and 36 related-answer links. Products are filled on articles and never on inquiries.

### Fields and objects

| Oracle term | What it is | Salesforce equivalent | What differs |
| --- | --- | --- | --- |
| Custom field | An older-style field on a standard object. Appears in the API as `customFields.c.<name>` | Custom field | |
| Custom attribute | A newer field on a standard object, stored in a package. Appears as `customFields.<Package>.<name>` | Custom field | |
| Custom object | A new table, stored in a package (up to 25 objects per package) | Custom object | Salesforce has no package grouping without a managed package |
| Menu-only object | A table that holds only the values for a menu field | Picklist values or a global value set | Oracle values are rows with numeric ids. Salesforce values are text, so migration maps id to value |

At CIS: 160 custom fields, and four packages (SCIF, DEMOGR, Referrals, OpenMethods) holding 21 objects, 11 of them menu-only.

### Channels and content

| Oracle term | What it is | Connected to | Salesforce equivalent | What differs |
| --- | --- | --- | --- | --- |
| Interface | A separate configuration over the same database | Profiles, mailboxes, settings, message templates, chat hours, response requirements, answer access | No single equivalent: language on the Case, an Email-to-Case address per mailbox, a chat deployment per language, Knowledge languages | See the short version, point 4 |
| Mailbox (Techmail) | Reads a mailbox, matches or creates the contact, creates the inquiry | Interface, business rules | Email-to-Case routing address | Email-to-Case matches a Contact but doesn't create one |
| Standard text | Prepared text a specialist inserts with a hotkey | Interfaces, rules, chat | Quick Text, email templates, macros | The hotkey is F8 in Oracle's documentation; earlier Kicksaw notes say F9 |
| Message templates | The system's notification and email wording, per interface | Interface | Email templates and auto-response settings | |
| Surveys | Oracle's own survey tool | Tasks, contacts | Salesforce Surveys or Feedback Management | |
| SLA and response requirements | SLAs are service contracts. Response requirements set a default due time per interface | Inquiry | Entitlements, milestones, business hours | Oracle's default applies to every inquiry with no setup. CIS has no SLAs and uses response requirements |
| Add-ins and extensions | Plug-ins for the Windows console and the browser version | Profile and interface | Lightning components, Service Cloud Voice | At CIS: the OpenMethods phone add-in and the demographics pop-up |

At CIS: interfaces `nci` (English), `nci2` (Spanish) and `nci1` (unused). Five mailboxes. 352 standard text items.

### Administration

| Oracle term | What it is | Salesforce equivalent | What differs |
| --- | --- | --- | --- |
| Service Console (.NET) | The Windows desktop client CIS uses | Lightning Service Console | Oracle has two clients |
| Agent Browser UI | The browser client, at `/AgentWeb/` | The same | Element Manager, Data Lifecycle Management and the Job Scheduler exist only here |
| Element Manager | Packages configuration to move between sites: workspaces, rules, navigation sets, custom scripts and more | Metadata API, change sets | The Connect REST API can't read rules, workspaces, profiles or scripts. Element Manager can |
| File Manager | Holds files for the site, including the custom scripts folder | Static resources and Apex classes | |
| Job Scheduler | Runs a custom script on a schedule | Scheduled Flow or scheduled Apex | |
| Analytics reports | Oracle's reports. Can run on a copy of the database (the report database) and can carry PHP that changes the output | Reports and dashboards | No replica and no code on a Salesforce report |
| Data Lifecycle Management | Policies that archive and purge old inquiries, contacts and logs | A scheduled Flow or batch Apex | Salesforce has no built-in rule-based purge |

## Retention, in Oracle's terms

Oracle offers purge policies for contacts and inquiries, but they delete. For removing personal details from specific fields while keeping the record, Oracle's own guidance is custom processing: a PHP script, which the Job Scheduler can run on a schedule. That matches what CIS described (a script in File Manager) and what the data shows (contacts kept and flagged, not deleted). See the data profile for the counts.

To find the script in the browser client: open File Manager, then the custom scripts folder. The Job Scheduler lists which scripts run and when. Process Designer lists any code that runs when a record changes.

## Corrections to earlier Kicksaw documents

Found while checking this document against Oracle's documentation:

| Document | Says | Correct |
| --- | --- | --- |
| Mapping framework | Lists a "content" rule base | Oracle has no content rule base; it has a Chat one. Likely a mis-hearing on the tour |
| Mapping framework | Standard text hotkey is F9 | Oracle documents F8 |
| System landscape | Chat queues are counted within the 51 queues | Chat queues are a separate list of 6 |
| System landscape | English and Spanish pairs link through related answers | They are siblings |
| System landscape, org summary | Contacts are deleted after 15 months | Contacts are scrubbed and kept |
| Console pull checklist | Retention settings are under Configuration Settings and Data Lifecycle | The scrub is a custom script: File Manager, Job Scheduler, Process Designer |
| Console pull checklist | Element Manager's export list omits custom scripts | It includes them, which is the route to the scrub script |

These documents are published in Notion, so the corrections go there.

## Three Salesforce items to check for Government Cloud

Not verified in this pass: whether Privacy Center is available, whether Unified Routing is available, and the response limit on Salesforce Surveys.

## Sources

Oracle B2C Service documentation, read 2026-10-02:

- [Customizing Profiles](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Customizing-profiles-ar1294709.html) and [Add or Edit a Profile](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Add-or-edit-a-profile-ar1236480.html)
- [How You Route Incidents to Queues](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Incident-queues-be1131228.html), [Add or Edit an Incident Queue](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Add-or-edit-an-incident-queue-be1364503.html) and [Fill Your Inbox](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Fill-your-inbox.html)
- [Add or Edit a Chat Session Queue](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Add-or-edit-a-chat-session-queue-ac1130168.html) and [Pulling Chats from the Wait Queue](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Pulling-chats-from-the-wait-queue-ac1130571.html)
- [Overview of Multiple Interfaces](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-crm-admin-multiple-interfaces.html) and [When to Use Multiple Interfaces](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Configuring-multiple-interfaces.html)
- [Overview of Workspaces](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-dad-workspaces.html), [Overview of Workspace Rules](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Overview-of-workspace-rules-ac1134767.html) and [Custom Field Visibility Settings](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Setting-custom-field-visibility-bx1138190.html)
- [Overview of Business Rules](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-crm-admin-business-rules-management.html) and [How are Rules Processed](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-How-are-rules-processed-bq1201220.html)
- [Overview of Navigation Sets](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-crm-admin-nav-sets.html) and [Overview of Staff Management](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-crm-admin-staff-management.html)
- [Overview of Contacts](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Contacts-overview--bz1130094.html) and [How Email Works in Service](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Email-handling-in-Service.html)
- [Sibling Answers](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Sibling-answers-aq1387538.html), [How You Control Answer Access](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Answer-access-levels.html) and [Products, Categories, and Dispositions](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Organizing-information-with-products,-categories,-and-dispositions-be1130596.html)
- [Custom Object Types](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Creating-custom-objects-bf1193791.html) and [Custom Object Packages](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Organizing-custom-objects-bf1193834.html)
- [Custom Scripts](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-custom-scripts.html), [Overview of Custom Processes](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Overview-custom-processes-bs1142110.html) and [Job Scheduler](https://documentation.custhelp.com/euf/assets/devdocs/buiadmin/topicrefs/c_overview_of_job_scheduler.html)
- [Data Lifecycle Management](https://documentation.custhelp.com/euf/assets/devdocs/buiadmin/topicrefs/c_bui_Data_lifecycle_management.html) and Oracle's [Product and Service Feature Guidance, April 2022](https://cx.rightnow.com/euf/assets/cc_resources/answerdocs/answer9433/Oracle_B2C_Service-APRIL_2022.pdf)
- [Element Manager REST: create an export package](https://docs.oracle.com/en/cloud/saas/b2c-service/cxemg/op-elementmanager-export-empackages-post.html) and [Connect REST endpoints](https://docs.oracle.com/en/cloud/saas/b2c-service/cxsvc/rest-endpoints.html)

Four statements rest on a search excerpt because the Oracle page wouldn't load: the pull policy names and limits, chat hours and response requirements being per interface, and status types.

CIS facts: the Oracle test environment tour of 2026-09-21 (Notion Transcripts), the metadata pull of 2026-09-23 in `oracle/extracts/oracle-metadata/2026-09-23/`, and the [org summary](oracle-org-summary-2026-09-30.md).

## Change log

| Date | Change |
| --- | --- |
| 2026-10-02 | Created |

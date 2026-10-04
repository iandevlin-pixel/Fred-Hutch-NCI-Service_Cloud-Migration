# Oracle org summary and Salesforce comparison

> **Frozen 2026-09-30.** Published to the Notion Project Library as [Oracle org summary and Salesforce comparison](https://app.notion.com/p/3ebd4b87741781ed8026e13760663dda). The Notion page is the live copy; edit there, not here.

What the CIS Oracle Service Cloud org holds, what the Salesforce Government Cloud org holds today, and where each piece goes. Written for the Kicksaw team. This is a living page: it changes as more Oracle information arrives, and the Change Log at the end records each update.

**"Oracle" on this page means the test instance `NCI__TST`**, a copy of production taken two to three months before 2026-09-21. Kicksaw has no access to Oracle production. Every count here is test-instance configuration, and production may differ in places.

**Full lists** live in the Oracle configuration inventory workbook, one tab per list: [link added once the workbook is in Kicksaw Google Drive]. The workbook leaves out two picklists whose values are staff names (CT Searcher and Lead), and it carries no standard content text.

Each item below is marked with where it goes:

- **Carry forward**: the thing, or the need behind it, exists in the new system.
- **Not coming over**: it exists in Oracle and stays there. It's recorded here so nobody rebuilds it by accident.
- **To confirm**: the record doesn't settle it yet. The Still open section says who answers.

## At a glance

| Area | In Oracle | In Salesforce today | Going forward |
| --- | --- | --- | --- |
| Phone lines | 8 service numbers | None. Amazon Connect is not provisioned | 4 lines on the phone menu move to Amazon Connect. The Public Inquiries line stays at Fred Hutch. 3 numbers to confirm |
| Email mailboxes | 5 | 0 Email-to-Case routing addresses | 2 carry forward to Email-to-Case. 3 not coming over |
| Chat | 2 cancer.gov entry pages, 6 chat queues | 0 messaging channels | Enhanced Chat |
| Text reminders | Amazon Pinpoint, VA callbacks only | None | Rebuilt off Pinpoint |
| Queues | 51 named, plus 5 separator rows | 1 sample queue | 17 carry forward, 6 not coming over, 28 to confirm |
| Profiles | 40, of which 8 are named as test, UAT or copies | 20 standard profiles | A minimal profile plus permission set groups. Only active users move |
| Custom objects | 21, in 4 packages | 2 from the org template | SCIF becomes a Case child object. OpenMethods retires. DEMOGR and Referrals are not placed yet |
| Custom fields | 160 | 34 from the org template | Rebuilt by design, not lifted as-is |
| Picklists | 142 lists, 3,842 values | None built | Rebuilt. 66 separator and placeholder values are dropped |
| Knowledge | About 5,000 articles, English and Spanish | 6 Salesforce sample articles | Migrate |
| Standard content | 352 canned replies | 10 sample Quick Text entries, 26 sample email templates | Rebuilt as Quick Text and email templates |
| Surveys | 28 | Not set up | Target not settled |
| Reports | 2,073: 1,051 Oracle stock, 1,022 custom | 113 sample reports | Rebuilt for the reports the CIS team names |
| Integrations | Telephony bridge (3 objects), Pinpoint, Cisco Finesse, Verint. 0 event subscriptions | 0 call centers | Service Cloud Voice with Amazon Connect, and Calabrio |

## What this page is based on

| Source | What it gives | Date |
| --- | --- | --- |
| Oracle metadata pull | Schemas, picklist values, queue, profile and status names, mailboxes, standard content structure, report list and 190 report definitions. 6,294 read-only requests; no records | 2026-09-23 |
| Reverse demo of the current stack | The four phone lines and phone menus, social media on hold | 2025-07-29 |
| Scope tracker snapshot | The NCIinfo@nih.gov address, "approximately 10 inbound phone numbers", interaction tracking scope | 2026-09-24 |
| Oracle test environment tour with Mark Hubers | Object model, rules editor, custom field folders, queues, profiles | 2026-09-21 |
| Discovery session 2 (Notion Transcripts) | Reports, surveys, routing, email; the start-fresh data decision | 2026-09-17 |
| Workflow discovery session, clinical trials (Notion Transcripts: "CIS Contact Center Migration // Workflow Discovery Session - Clinical Trials, Smoking Cessation, Etc. 2026-09-24") | How clinical trials and CCR calls arrive | 2026-09-24 |
| Discovery session 5 (Notion Transcripts: "CIS Contact Center Migration // Discovery Session 2026-09-29") | Which mailboxes, lines and interfaces are live; SLAs; profiles; reports | 2026-09-29 |
| Salesforce production queries | What the Government Cloud org holds, read-only | 2026-09-30 |
| RAID Log, [mapping framework](https://app.notion.com/p/3ead4b877417816383aff1369c4596d1), [console pull checklist](https://app.notion.com/p/3ead4b87741781c2a7a4ff31806351f5) | Decisions, Salesforce targets, and what still needs capturing from the Oracle console | Various |

Session 5 quotes carry their timestamps. The transcript's speaker labels are unreliable, so quotes are attributed to the CIS team unless the speaker is certain.

**What the test instance can't show.** Its five mailboxes are switched off and carry test relay addresses, so it says nothing about how production mail is set up. It exposes no phone numbers or dialed-number data. It has no event subscriptions.

**What the REST API doesn't expose.** Workspaces, business rules, queue routing, what each profile is allowed to do, survey content, report folders, and chat rules. These come from the Oracle console; the [console pull checklist](https://app.notion.com/p/3ead4b87741781c2a7a4ff31806351f5) lists them. Nobody is assigned to capture them yet.

**One date in the pull isn't meaningful.** 28 report definitions show a last-updated date of 2026-09-23, the second they were read by the pull. The report list was pulled four hours earlier, and its dates are the ones this page and the workbook use.

## Entry points: two mailboxes and five phone lines carry forward

The public entry points (the phone numbers, the cancer.gov chat entry, and the email address) stay the same, and everything behind them changes (Entry points do not change, RAID-38). The items marked "not coming over" here are entry points Oracle still holds that nobody uses.

### Phone

Oracle records which number a call came in on through a service number picklist on the inquiry. It has 8 values.

| Oracle service number | Line | Status | Going forward | Basis |
| --- | --- | --- | --- | --- |
| 4CANCER | 1-800-4-CANCER | Live, on the phone menu (IVR) | Amazon Connect | Verified. Session 5, 39:16; reverse demo |
| 44U QUIT | Smoking quitline, 1-877-44U-QUIT | Live, on the phone menu | Amazon Connect | Line verified, session 5, 39:16. Number match inferred from RAID-38 |
| VA Quit Smoking | VA quitline, 1-855-QUIT-VET | Live, on the phone menu | Amazon Connect | Line verified, session 5, 39:16. Number match inferred from RAID-38 |
| CCR | Center for Cancer Research line | Live, on the phone menu. Calls land in the clinical trials queue; Oracle has no CCR phone queue | Amazon Connect | Verified. Session 5, 39:16; reverse demo; clinical trials session, 03:27; metadata pull |
| PIQ | Public Inquiries line | Live, but separate from the phone menu. "It's a private phone, so they get manually entered." The line lives at Fred Hutch | Stays at Fred Hutch. Salesforce needs a Public Inquiries value so specialists can record these calls | Verified. Session 5, 40:17 to 40:53 |
| QUIT NOW | Not one of the public numbers in RAID-38 | Unknown | To confirm | Nothing on record |
| Proact Study Number | Proactive study calls | Unknown | To confirm | Nothing on record |
| NIDCD | NIDCD line | Unknown. Likely never used: Mark Hubers said of NIDCD, "We set it up proactively thinking that we might be getting traffic, but we never actually did" | To confirm | Inferred. Session 5, 28:41, in answer to a question about the NIDCD email queue |

The scope tracker and the kickoff describe "approximately 10 inbound phone numbers." Five lines are confirmed live. Whether the other five are dialed-number variants of the same lines or retired numbers is to confirm.

### Email

| Oracle mailbox | Interface | Status | Going forward | Basis |
| --- | --- | --- | --- | --- |
| NCI | English | Live. The public address is NCIinfo@nih.gov, which auto-forwards into Oracle | Email-to-Case | Verified. Session 5, 25:17; scope tracker |
| NCI Español | Spanish | Live. Production address not on record | Email-to-Case | Verified. Session 5, 25:17 |
| NCI Mobile | English | "The mobile ones are no longer active" | Not coming over | Verified. Session 5, 25:13 |
| NCI Móvil Español | Spanish | No longer active | Not coming over | Verified. Session 5, 25:13 |
| Bouncebacks | English | "An Oracle-configured mailbox for the bounce-back messages" | Not coming over as a mailbox. Bounce handling is designed with Email-to-Case | Verified that it is Oracle-internal. Session 5, 25:17 |

Three things carry forward with the two live mailboxes:

- **Domain authentication.** Oracle has a DKIM relationship today, with a domain Mark Hubers recalled as "mail dot mail dot cancer dot gov, I think" (session 5, 26:12). He called setting it up "a federal government thing" that the CIS team can't do itself (session 5, 25:56).
- **Permission to forward.** NIH allows auto-forwarding to Oracle only. "We have permission to send it to Oracle, but we need to get permission to send it to Salesforce." Session 5, 28:02.
- **Mailbox validation.** The CIS team has access to the mailboxes to confirm Salesforce's verification emails. Session 5, 25:52.

### Chat

| In Oracle | Going forward | Basis |
| --- | --- | --- |
| English and Spanish chat pages on cancer.gov link to an Oracle-hosted launch page, plus pop-up invitations | Enhanced Chat, decided 2026-09-28. Cam Bennett, the cancer.gov contact, redirects the links and pop-ups | Session 5, 17:19 to 20:27; session 5 guide |
| 6 chat queues: Cancer Inquiry, Smoking Cessation, Clinical Trial, each in English and Spanish | Carry forward into chat routing | Metadata pull |
| Transcripts offered to the client by email at the end of a chat | Carry forward | Session 5, 20:33 |
| Spam chats blocked by IP address | Carry forward. IP addresses also feed Adrianna Gutierrez's Tableau map of where chats come from | Session 5, 22:27 and 56:32 |

### Text reminders

Amazon Pinpoint texts opted-in VA callback clients before certain callback attempts, not every one, and writes a status note back to the inquiry. Clinical trials callbacks get no texts (session 5, 35:57 and 41:08). Replies go to a CIS mailbox at Fred Hutch that isn't linked to Oracle (session 5, 38:14). Pinpoint runs in commercial AWS under an exception, and the CIS team wants it in GovCloud (session 5, 34:02).

Going forward, the reminders are rebuilt off Pinpoint, because AWS ends Pinpoint support on 2026-10-30 (SMS callback reminders are rebuilt off Amazon Pinpoint, RAID-39). AWS End User Messaging is the named successor. Its availability in the GovCloud region is unverified.

### Social media

Oracle has eight social queues: Facebook, Twitter, YouTube and Instagram, each in English and Spanish. The channel was on hold in July 2025, but Mark Hubers still described the social queues on 2026-09-21, and the scope tracker keeps social media in interaction tracking. To confirm.

### Interfaces

Oracle separates English and Spanish work by interface.

| Interface | Use | Going forward | Basis |
| --- | --- | --- | --- |
| `nci` | English console | Carry forward the need: tell English and Spanish work apart | Session 5, 46:35 to 48:11 |
| `nci1` | "We don't really use NCI 1. That's like a staging one" | Not coming over | Verified. Session 5, 47:00 |
| `nci2` | Spanish console. A Spanish page sets the interface, and the interface sets the mailbox, the queue and the spell-check language | Carry forward the need. "However Salesforce does that, I think we're open" (Mark Hubers) | Session 5, 47:00 to 48:11 |

## Data model: 21 custom objects and 160 custom fields, none lifted as-is

The core objects in use are Inquiry (`incidents`), Task, Contact, Answer, Chat and Staff account. Organization, Asset, Opportunity and SLA entitlement exist but aren't used in the specialist workflow. The Salesforce target for each is in section 1 of the [mapping framework](https://app.notion.com/p/3ead4b877417816383aff1369c4596d1): Inquiry becomes `Case` with one record type per call type, and Answer becomes Knowledge.

### Custom objects

| Package | Objects | Hold data | Picklist objects | What it is | Going forward |
| --- | --- | --- | --- | --- | --- |
| SCIF | 8 | 1 (`SCIF.SCIF`, 116 fields) | 7 | Smoking cessation intake form | A `Case` child object entered through a Screen Flow. The VA's requirements for the form are unknown, and the CIS team has offered to shorten it |
| DEMOGR | 4 | 4 | 0 | Demographics survey configuration | Not settled; depends on the survey target |
| Referrals | 6 | 2 | 4 | Referral quality check and languages, attached to answers | Not placed yet |
| OpenMethods | 3 | 3 | 0 | The Cisco Finesse telephony bridge (Harmony) | Not coming over. Retires with Service Cloud Voice |
| **Total** | **21** | **10** | **11** | | |

### Custom fields

| Object | Picklist | Text | Date or date-time | Yes/No | Number | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Inquiry | 62 | 34 | 7 | 10 | 3 | 116 |
| Answer | 10 | 13 | 0 | 2 | 0 | 25 |
| Task | 5 | 3 | 2 | 5 | 1 | 16 |
| Contact | 0 | 0 | 0 | 3 | 0 | 3 |
| **Total** | **77** | **50** | **9** | **20** | **4** | **160** |

Answer's 25 include 6 Referrals attributes. Accounts and organizations have no custom fields.

Most inquiry fields group by name prefix. The meanings are read from the field labels, so they're inferred.

| Prefix | Fields | Likely purpose |
| --- | --- | --- |
| `ct_` | 24 | Clinical trials search |
| `ccr_` | 16 | Center for Cancer Research intake: patient details, scans, markers |
| `od_` | 10 | OD, which is also a queue, a staff group and a product |
| `referral_` | 6 | Referral coding |
| `action_`, `subject_of_int_`, `soi_`, `cancer_site_`, `special_code_` | 20 | Interaction coding |
| `smoking_`, `va_`, `arra_` | 5 | Smoking, VA and a study |
| Other | 35 | Mixed |

Task fields carry the callback (number, attempts, status), the Pinpoint text flags, the smoking follow-up answers, and the caller's time zone. The three contact fields are `exempt`, `pii_removed` and `sms_consent`.

## Picklists: 142 lists, rebuilt without separator values

Oracle holds 3,842 picklist values in 142 lists.

| List | Values | Note |
| --- | --- | --- |
| Source (inquiries, contacts, organizations) | 263 each | Oracle system list, identical on all three |
| Referral country | 236 | Referrals package |
| How the caller found NCI (`locating_nci`) | 120 | |
| Subject of interest 1 to 4 | 102 to 103 each | Coding |
| Task document | 97 | Oracle's marketing document list |
| Subject of interest 5 | 76 | Coding |
| SOI 1 to 4 | 71 to 74 each | Coding |
| Queue | 56 | Includes 5 separator rows |

Three lists are trees:

| Tree | Values | Top-level values | Depth |
| --- | --- | --- | --- |
| Products | 7 | 7 | 1 (flat) |
| Categories | 29 | 15 | 3 |
| Dispositions | 25 | 5 | 2 |

The seven products (Knowledge, Referral, Standard Response, Internal Information, PIQ, OD, National Organizations) look like knowledge base structure rather than inquiry types. That reading is inferred.

66 values are separators and placeholders, such as dashes and dots, used to lay out long lists. They aren't coming over.

## Queues, statuses and profiles: rebuilt around what's live

### Queues

Routing is redesigned rather than copied: universal, longest-waiting queuing across voice and chat (Universal queuing across voice and chat, RAID-35). This table sorts Oracle's 51 named queues by where the work goes.

| Group | Queues | Going forward | Basis |
| --- | --- | --- | --- |
| Phone, main lines | English and Spanish Cancer, Smoking and Clinical Trial Phone Call (6) | Carry forward to Amazon Connect | Session 5, 39:16 |
| Phone, VA | VA English and Spanish Quit Smoking (2) | Carry forward | Session 5, 39:16 |
| Phone, Public Inquiries | English PIQ Phone Call (1) | Carry forward as Salesforce work; the line stays at Fred Hutch | Session 5, 40:38 |
| Phone, POS | English and Spanish POS Phone Call (2) | Not coming over | Session 5, 28:41 to 28:55; Oracle tour |
| Phone, programs | Proact Study, IMPACT, English and Spanish NIDCD (4) | To confirm. NIDCD is likely never used | NIDCD inferred from session 5, 28:41 |
| Chat | English and Spanish Cancer, Smoking and Clinical Trial Chat (6) | Carry forward to Enhanced Chat | Decided 2026-09-28 |
| Email, main inboxes | English Email, Spanish Email (2) | Carry forward to Email-to-Case | Session 5, 25:17 |
| Email, mobile | Mobile English, Mobile Spanish (2) | Not coming over | Inferred: their mailboxes are inactive (session 5, 25:13) |
| Email, retired programs | POS Email, NIDCD Email (2) | Not coming over | Verified. Session 5, 28:41 to 28:55 |
| Email, CCR and Public Inquiries | CCR English Email, CCR Spanish Email, PIQ Email, PIQ Spanish Email (4) | To confirm. A CCR email queue is in use for web forms | Clinical trials session, 21:02 |
| Review and back office | English Review, Spanish Review, CT Review, PIQ Review, PIQ Triage, Customer Responses, Custom Email/Letters, Control Email/Letters, Science Writer, SPAM, Bounced Emails, OD (12) | To confirm | Nothing on record |
| Social | Facebook, Twitter, YouTube and Instagram, English and Spanish (8) | To confirm | See Social media |
| **Total** | **51** | 17 carry forward, 6 not coming over, 28 to confirm | |

### Statuses

| Object | Statuses | Note |
| --- | --- | --- |
| Inquiry | 13 | 10 real statuses (Unassigned, Assigned, In Progress, Review, Review Complete, Completed, Resource Support, CT Search, Customer Response, Waiting) plus 3 placeholders (`....`, `...`, `.....`) that aren't coming over |
| Task | 5 | Not Started, In Progress, Completed, Waiting, Deferred |
| Answer | 7 | Draft, Proposed, Public, System Review, In Review, Retired, Internally Published |

Oracle has 0 SLAs. "We don't really use service level agreements. We're using those response requirements," which set each inquiry's due date (session 5, 43:50 to 45:36). The due-date need carries forward; SLAs don't. Oracle also holds 17 holidays for 2025 to 2027.

### Profiles and staff groups

Oracle has 40 profiles. Each one bundles language, clinical trials chat eligibility, knowledge access and a navigation set. Eight are named as test, UAT or copies, for example "Oracle Test Admin (do not use)" and "Copy of SOAP API." The CIS team said "a lot of these aren't even used anymore," and "we're only taking active users with us, so we'll be able to eliminate a lot of those profiles" (session 5, 50:35 and 51:48).

Going forward, permissions are designed fresh: a minimal profile plus permission set groups per role (Oracle tour; [mapping framework](https://app.notion.com/p/3ead4b877417816383aff1369c4596d1), section 2). Oracle's 8 staff groups (RightNow, Supervisors, Technical, NCI, Information Specialists, Remote Monitors, OD, special group) inform public groups and queue membership.

## Content: knowledge articles move, standard content and reports are rebuilt

### Knowledge

About 5,000 articles, English and Spanish, linked as siblings. They migrate to Salesforce Knowledge. Melissa Hoard-Silver owns them, and the knowledge base session is 2026-10-01 (session 5, 1:02:05). Everything else starts fresh: "We're not taking… the historical data from this system" (session 5, 51:48).

### Standard content

352 canned replies used in chat, email and inquiries. The target is Quick Text and email templates.

| Oracle folder | Items |
| --- | --- |
| LH SRL (English chat replies) | 107 |
| SP LH SRL (Spanish chat replies) | 95 |
| Public Inquiries | 48 |
| Spanish Email SRLs | 47 |
| English Email Templates/Suggested Language | 34 |
| Spanish Email Templates | 21 |
| **Total** | **352** |

151 items have an HTML version, 327 have a hot key, and 37 aren't visible on the Spanish interface. The workbook indexes each item; the reply text stays in Oracle.

### Surveys

Oracle holds 28 surveys:

- satisfaction surveys for phone, email and chat in English and Spanish
- demographics surveys (general, by chat, by specialist, VA)
- VA follow-ups at 4, 7 and 13 months
- clinical trials callback, follow-up and search surveys
- training and check-in surveys

At least three survey types are live: demographics, client satisfaction and tobacco follow-up. The Salesforce target isn't settled; Feedback Management is capped at 300 responses per term. Which of the 28 are live is to confirm.

### Reports

| Reports | Count |
| --- | --- |
| Oracle stock reports (IDs below 100000, all dated 2007-02-01) | 1,051 |
| Custom reports, created 2012 to 2025 | 1,022 |
| Custom, last updated 2012 to 2014 | 582 |
| Custom, last updated 2015 to 2020 | 391 |
| Custom, last updated 2021 or later | 49 |
| Custom, named with test, old or copy | 35 |
| **Total** | **2,073** |

The CIS team called many of them "prototypes that then became final," and will show which ones they use (session 5, 30:35 to 30:48). Only the reports they name are rebuilt, as Salesforce reports and dashboards, with Amazon Connect metrics for telephony. Report data is never pulled, because it can't be separated from protected health information.

## Integrations and automation: the telephony bridge retires, and rules wait on the console capture

| Oracle today | Going forward |
| --- | --- |
| Cisco Finesse phone bar, bridged by OpenMethods Harmony with PopFlow screen pop | Service Cloud Voice with Amazon Connect. The bridge isn't coming over |
| Cisco Unified Intelligence Center for real-time monitoring | Amazon Connect metrics |
| Verint for quality and workforce management | Calabrio |
| Amazon Pinpoint text reminders | Rebuilt off Pinpoint (RAID-39) |
| Tableau from manual report exports | Exports from Salesforce and Calabrio. A direct connection isn't required (session 5, 57:51) |
| 0 event subscriptions | Nothing to carry |

Workspaces, business rules and custom processes don't come through the REST API. What's known: NCI Inquiry v2.1 is the only live inquiry workspace, and inactive business rules aren't migrated (Oracle tour). Business rules become before-save and after-save Flows ([mapping framework](https://app.notion.com/p/3ead4b877417816383aff1369c4596d1), section 4).

The contact purge carries forward as a requirement. Contacts are deleted after 15 months, and deleting one also hides the inquiry's message tab so no health information stays visible (session 5, 58:52 to 59:49). The CIS team placed the purge configuration in Oracle's File Manager: "I want to say File Manager" (session 5, 1:00:08).

## The Salesforce org holds only provisioning content

Salesforce production was queried read-only on 2026-09-30. Everything in it came with the org on 2026-06-15, apart from two permission set groups added by later Salesforce releases. Nothing is Kicksaw build yet.

| Item | Count | What it is |
| --- | --- | --- |
| Custom objects | 2 | Knowledge and ForecastingItem, from the org template |
| Custom fields | 34 | Template fields on Knowledge, ForecastingItem and Opportunity |
| Queues | 1 | "Q1" |
| Profiles | 20 | Standard |
| Custom permission sets | 1 | `cases_Permisssion_Set`, spelled as in the org |
| Permission set groups | 9 | Salesforce-provided (Sales Cloud, partner, catalog) |
| Email-to-Case routing addresses | 0 | |
| Messaging channels | 0 | |
| Call centers | 0 | |
| Knowledge articles | 6 | Salesforce samples |
| Reports | 113 | Salesforce samples |
| Quick Text entries | 10 | Salesforce samples |
| Email templates | 26 | Salesforce samples |
| Active users | 10 | |

```sql
-- Tooling API
SELECT COUNT() FROM CustomObject
SELECT COUNT() FROM CustomField
-- Standard API
SELECT COUNT() FROM Group WHERE Type = 'Queue'
SELECT COUNT() FROM Profile
SELECT COUNT() FROM PermissionSet WHERE IsOwnedByProfile = false AND NamespacePrefix = null
SELECT COUNT() FROM PermissionSetGroup
SELECT COUNT() FROM EmailServicesAddress
SELECT COUNT() FROM MessagingChannel
SELECT COUNT() FROM CallCenter
SELECT COUNT() FROM Knowledge__kav
SELECT COUNT() FROM Report
SELECT COUNT() FROM QuickText
SELECT COUNT() FROM EmailTemplate
SELECT COUNT() FROM User WHERE IsActive = true AND UserType = 'Standard'
```

## Not coming over

These exist in Oracle and stay there.

| Item | What it is | Why | Basis |
| --- | --- | --- | --- |
| NCI Mobile and NCI Móvil Español mailboxes | Mobile email inboxes, English and Spanish | "The mobile ones are no longer active" | Verified. Session 5, 25:13 |
| Mobile English and Mobile Spanish queues | Queues for those inboxes | Their mailboxes are inactive | Inferred from session 5, 25:13 |
| Bouncebacks mailbox | Oracle's own mailbox for bounced messages | An Oracle mechanism. Bounces are handled in the Email-to-Case design | Oracle-internal: verified, session 5, 25:17. Treatment: inferred |
| NIDCD email queue | Set up for traffic that never came | "NIDCD, I don't think we ever used" | Verified. Session 5, 28:41 |
| POS email and phone queues (3) | A program that ended | "The POS stuff… was ended a long time ago" | Verified. Session 5, 28:41 to 28:55; Oracle tour |
| `nci1` interface | A staging console | "We don't really use NCI 1" | Verified. Session 5, 47:00 |
| SLAs | Oracle service level agreements, 0 configured | Response requirements set due dates instead | Verified. Session 5, 45:36; metadata pull |
| Historical data and inactive users | 14 years of inquiries and contacts, and deactivated staff accounts | Start fresh; only active users move | Verified. Session 5, 51:48; session 2 |
| Unused profiles | Test, UAT and outdated profiles | Permissions are designed fresh | Verified. Session 5, 50:35; Oracle tour |
| Separator and placeholder values (66) | Dashes and dots in queues, statuses and coding lists | Layout devices, not data | Metadata pull |
| Unused objects | Organization, Asset, Opportunity, SLA entitlement | Not in the specialist workflow | Oracle tour; mapping framework |
| Telephony bridge | OpenMethods Harmony (3 objects) and PopFlow | Retires with Service Cloud Voice | Mapping framework |
| Pinpoint campaigns and journeys | Text reminder mechanics | AWS ends Pinpoint support on 2026-10-30; reminders are rebuilt | RAID-39 |
| Reports nobody names | Most of the 1,022 custom reports | "Prototypes that then became final." Only reports the CIS team names are rebuilt | Session 5, 30:48 |

## Still open

| Open item | Who answers | Where it's tracked |
| --- | --- | --- |
| Whether the QUIT NOW, Proact Study and NIDCD numbers are live | CIS team | Next discovery session |
| How "approximately 10 inbound numbers" maps to the 5 live lines | CIS team, with the Verizon account | Next discovery session |
| The NCI Español production address and the DKIM domain | CIS team, NCI | Email design |
| NIH permission to forward mail to Salesforce | CIS team with NIH | The federal approvals list Sarah Tirey asked for (session 5, 54:05) |
| Which of the 28 to-confirm queues are live | Adrianna Gutierrez and Holly Fernandez-Johnson | Queue design |
| Whether social media comes back | CIS team | Channel scope |
| Which profiles, reports and surveys are in use | CIS team | Permission design, report list, survey design |
| Whether scheduled callbacks and in-flight work still migrate. Session 2 said yes; session 5 described articles only | CIS team | Data migration plan |
| Text reminder timing and triggers. The record has both 24 hours and 3 hours, and 24 hours, 1 hour and a final text | CIS systems team | Next discovery session (session 5, 39:10) |
| Workspaces, business rules, navigation sets, retention settings | An admin with console access | [Console pull checklist](https://app.notion.com/p/3ead4b87741781c2a7a4ff31806351f5), not assigned |
| Volumes: interactions, callbacks, texts, users, articles | CIS team | [Counts Request Session 5](https://app.notion.com/p/3ead4b87741781f0bb0cdf0d694678b0) |

## Change Log

| Date | Change |
| --- | --- |
| 2026-09-30 | First version. Built from the 2026-09-23 metadata pull, sessions 2, 4 and 5, and read-only Salesforce production queries |

# Discovery session 2 guide: workflows, roles, and systems

Prep guide for the second discovery session with the Fred Hutch NCI Cancer Information Service (CIS) team. Two sections, one per Kicksaw lead:

- **Avi's section:** process and workflow. Call walkthroughs, what the specialist does, how work moves. Avi runs the call
- **Ben's section:** architecture, permissions, data, and vendors. Design decisions, access model, retention, migration inputs

## How this guide works across sessions

- Every question carries a permanent ID: `A-nn` for Avi's, `B-nn` for Ben's. IDs never renumber. A question that is not reached keeps its ID in the next guide
- **Origin** says where the question first came up. `Jul-25` is the 2025-07-29 reverse demo, `S1` is discovery session 1 on 2026-09-15, `S2` is new for this session
- **Status** is blank before the session. **Filled 2026-09-17 against the session 2 transcript** at transcripts/2026-09-17-discovery-session-2-reports-surveys-routing-email.md. After the transcript is filed, mark each row `Answered`, `Partial`, or `Not reached`, with the transcript timestamp. Not reached and Partial rows open the next session's guide
- **On record** lines give what the client has already said, with the source, so a question becomes a read-back instead of a repeat
- Sessions are grouped by call type. Items deferred by design (smoking cessation and VA this time) sit in the section they belong to with status `Deferred`

**Review copy:** none. Pushed to Notion 2026-09-17 and deleted by Ben the same day as not yet ready for the team. Local markdown is the working copy; the Notion transcript database is the source of truth for what was said on the call.

Revised 2026-09-17 against the 2025-07-29 reverse demo, the 2026-09-08 kickoff, the 2026-09-14 Calabrio kickoff, session 1, the decision register, and Avi Rabinovitch's plan for this call.

---

## Session details

- **Topic:** Workflows for two of three call types (general cancer, clinical trials), plus protected items from Ben's section
- **Duration:** 60 minutes. The client has confirmed only Wednesday and Thursday 4:00 to 5:00 PM ET, and Thursday afternoon collides with the Fred Hutch IT change board (R9, client availability constrains the discovery cadence). Plan for the hour
- **Participants:** Fred Hutch CIS team and Kicksaw. **AWS attendance is a decision, not a default.** Binu Pazhoor pitched an Amazon Connect Agent Workspace architecture on session 1 and the client heard two designs on one call. Ben owes an alignment with Binu Pazhoor and Ken Daugherty before the next joint AWS session (D13, agent desktop is Salesforce). Until that happens, run without AWS. Calabrio does not belong on a call-type session
- **Client attendees to expect:** Mark Hubers, Adrianna Gutierrez, Jennifer Macabeo, Mike Griffin, Ray Quijano, Reetu Ghumman. Holly Fernandez-Johnson owns quality management and missed session 1; the escalation and supervision questions need her

## Agenda

Avi's walkthrough is the spine. Ben's protected items take about eight minutes in total.

| Time | Lead | Topic | Items |
| --- | --- | --- | --- |
| 3 min | Avi | Recap and promised artifacts | A-01 to A-04, and B-20 (record count and sample export, never yet asked) |
| 22 min | Avi | General cancer walkthrough | A-05 to A-12 |
| 22 min | Avi | Clinical trials walkthrough, including CCR | A-13 to A-21 |
| 8 min | Ben | Protected items | B-15 (retention length), B-16 (delete versus hide), B-01 (tiers or flat), and a stated commitment to the client that roles and escalation get their own session |
| 5 min | Avi | Next steps | Confirm the smoking cessation and VA session, the roles and escalation session, and the knowledge base session |

Anything in Ben's section not listed in the agenda is expected to carry forward. Say so to the client rather than skipping silently. Roles and access was the client's own first agenda item on session 1 and was not reached.

---

## Avi's section: process and workflow

### Recap and promised artifacts

All promised on session 1, 2026-09-15.

| ID | Item | Owner on client side | Origin | Status |
| --- | --- | --- | --- | --- |
| A-01 | Workspace rules list, workspace definition, and custom field list including the special codes | Adrianna Gutierrez, Mark Hubers | S1 | Not reached. New related promise: report definitions export (6:14) |
| A-02 | Full call type list, including Jennifer Macabeo's document from the last migration | Adrianna Gutierrez, Jennifer Macabeo | S1 | Not reached |
| A-03 | Restricted Oracle account for Kicksaw, without reports explorer or contacts | Adrianna Gutierrez | S1 | Answered: Oracle test environment access next week, reports excluded (6:14, 18:31, 1:00:17) |
| A-04 | Authoritative inbound number, DNIS, and IVR list. Mark's recall did not match cancer.gov on session 1. Avi's plan references a DNIS sheet with "CTS" reserved routing; confirm its source and file it | Mark Hubers | S1 | Not reached. Skill list with coding requested instead (33:31) |

### General cancer (1-800-4-CANCER, Cancer Line queue)

On record:

- Every interaction creates an inquiry. Contact fields first, then notes, then coding after the interaction (S1, Adrianna at 48:02 on coding after)
- Subject 1 through 4 are cancer topics mirroring cancer.gov. **Subject 1 is the primary topic**, then descending. Four fields exist only because Oracle had no multi-select (S1 at 7:42, Jul-25 at 42:32)
- Anonymity is the governing constraint. Contact details are asked only when the client wants email follow-up or a callback (Jul-25). Chat requires nothing to start (S1 at 33:49)
- Standard text is a repository of templated responses with F9 hotkeys, separate from knowledge. Email threads to the inquiry as responses; private notes are internal and used for review feedback (S1, 37:56 to 47:57). Inbound email lands in an NIH Outlook inbox (Jul-25)
- Statuses mix stock and custom values (in progress, for review, review complete) and support a review workflow. Deferred on S1 to this session (46:21)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-05 | Walk one call from answer to close. What does the specialist fill in before, during, and after the call? Read back the contact, notes, coding order and let them correct it | S2 | Not reached |
| A-06 | Which fields are required before an inquiry can close? Which are optional or exist only for reports? Does it differ by call type? | S2 | Not reached |
| A-07 | How do they choose Subject 1 to 4 on a live call? Confirm Subject 1 is always primary. Then ask whether any NCI extract or report depends on the primary versus secondary distinction. (Feeds B-11, the multi-select design decision) | S2 | Not reached |
| A-08 | When does a general call need email follow-up? What goes out (standard text, knowledge article, links), and from which mailbox? | S2 | Not reached |
| A-09 | When a caller stays anonymous, what is the minimum captured? Can an inquiry close with no contact? | S2 | Not reached |
| A-10 | When a general call turns into a clinical trials or smoking question: new inquiry, re-coded, or transferred? Include the CCR case, where a general clinical trials call becomes a CCR conversation (S1 at 21:41, described as infrequent) | S2 | Not reached |
| A-11 | Which statuses does a general inquiry move through, who moves it, and what does review complete unlock? | S1 | Partial: email review statuses walked (51:35 to 54:03); phone inquiry statuses not covered |
| A-12 | How long does a typical call run, and how much is after-call work? (Feeds Calabrio workforce management forecasting and the service level gap never covered on S1) | S2 | Partial: calls run up to an hour, quality not speed (24:13); no averages given |

### Clinical trials (Clinical Trial queue), including CCR

On record:

- Clinical trials coding is "similar but more detailed" than general cancer, with additional fields when it is CCR (S1, Mark at 20:57 to 21:13)
- A CCR inquiry is identified by the dedicated CCR phone number or the CCR website email template (S1 at 21:24 to 21:29)
- CCR data is emailed to CCR from a customized Oracle report after capture (Jul-25 at 608)
- Clinical trial searches generate up to two follow-up callbacks (S1, Adrianna at 32:04). New on S1; July recorded VA as the only case-managed population
- Specialists search external clinical trial websites, which are out of scope (D20, scope boundaries)
- Skill groups today: English cancer, English tobacco, Spanish, English clinical trials, Spanish clinical trials. The specialist groups are reserved deliberately so low-volume queues are not starved by general volume (Jul-25 at 21:29). This answers the "CTS reserved routing" question; confirm rather than ask

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-13 | What extra detail is captured beyond general cancer: diagnosis, stage, location, travel limits, prior treatment? And what more for CCR? | S2 | Not reached |
| A-14 | Which external sites do they search, and what comes back into the inquiry: trial IDs, links, notes, or nothing? | S2 | Not reached |
| A-15 | The two callbacks: what triggers each, how many days apart, who owns them, and what counts as done? Same task mechanism as the VA callbacks? | S1 | Not reached |
| A-16 | How do search results reach the client: email, phone, or both? Is there a standard template? | S2 | Not reached |
| A-17 | If the client does not answer a callback, how many attempts, and when does it close? (Ask once here; the answer likely applies to the four VA callbacks too, A-25) | S2 | Not reached |
| A-18 | Confirm the clinical trials specialist group and reserved routing. Which specialists carry more than one skill? | Jul-25 | Partial: skill hierarchy described, reserved routing to be dropped at launch (31:32 to 38:44) |
| A-19 | When a general clinical trials call becomes a CCR conversation, what changes on the inquiry, and does the CCR report still pick it up? | S2 | Not reached |
| A-20 | Is the CCR email report a requirement to rebuild as is, or is a scheduled Salesforce report to the same recipients acceptable? | S2 | Not reached |
| A-21 | Do clinical trials inquiries follow the same statuses and review workflow as general cancer? | S2 | Not reached |

### Smoking cessation and VA

Not planned for this session by design. Carried forward with status `Deferred`.

On record:

- VA clients arrive by the VA toll-free number (the majority), clinic referral, or chat. Referrals come through VA Direct, a secured VA system that cannot be integrated. Specialists copy referrals into Oracle as contacts and create callback tasks (S1 at 31:08 to 31:45; D20)
- The Smoking Call Intake Form (SKIF) is a guide, not a script, completed for everyone who gets a counseling session (Jul-25 at 32:08, S1)
- Callbacks are opt-in. Tobacco cessation gets four, more if wanted. Scheduled callbacks exist in Oracle months and years ahead and must migrate. Specialists work half-hour blocks from a report; clients are told a 30-minute window. Fred Hutch asked for a calendar view. No queued or automated dialing (Jul-25 at 616 to 650)
- SMS reminders go 24 hours and about two hours ahead to clients with SMS consent yes and callback enrollment yes, no PII or PHI (S1 at 50:10 to 51:27)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-22 | Which fields does a specialist copy from a VA Direct referral to create the contact and the first callback? Ask for a redacted example | S1 | Deferred |
| A-23 | Should the SKIF present as a guided screen flow or as a tab of fields in any order? Does it change between the first session and later callbacks? | S2 | Deferred |
| A-24 | Confirm the calendar view is still the ask. Who works a callback block: the specialist who did the intake, or whoever is scheduled? | Jul-25 | Deferred |
| A-25 | Unanswered VA callbacks: attempts, and when the series closes | S2 | Deferred |
| A-26 | What is the exact SMS reminder text today? | S2 | Deferred |

---

## Ben's section: architecture, permissions, data, and vendors

### Roles, permissions, and administration

On record:

- Five CIS staff (everyone from Fred Hutch except Mike Griffin) configure the current platforms and expect to configure the new one. Fred Hutch holds full admin rights in Oracle and self-serves configuration, users, fields, reports, and custom codes (Jul-25 at 604, S1 at 6:02 and 1:01:20)
- Knowledge authoring is restricted to Melissa's team. Oracle's suggest and propose feature goes unused; specialists email instead (S1, 53:03 to 54:04)
- **Not on record:** specialist tiers, what access each carries, and supervisor functions. Q10 (agent tiers, access levels, skill structure) has been open since kickoff. Mark's "tier 1 to 1.5 support" describes his IT support role, not a specialist tier

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-01 | Are information specialists organized in formal tiers with different access, or is the role flat with skills per person? | S1 | Partial: hierarchical skill groups, PIQ second-tier email subset, supervisors and above for reports, leads scheduled through the day (5:14, 31:32, 47:52, 52:46) |
| B-02 | Where is the administration boundary in the new platform? Which changes do the five CIS administrators make directly (picklist values, standard text, report folders, routing skills), and which go through Fred Hutch IT or Suchi Panda's cloud team? | S2 | Partial: administrators edit shared reports, supervisors and above view (5:14). Fred Hutch IT boundary not reached |
| B-03 | Does the Fred Hutch IT change approval board govern Salesforce configuration changes? (It meets Thursday afternoons, per R9) | S2 | Not reached |
| B-04 | Which supervisor functions are needed day to day: managing queues, real-time availability, reassigning inquiries, reviewing private notes? | S2 | Partial: real-time traffic management, moving agents between channels, email review queue (30:11, 51:35) |
| B-05 | Does a knowledge proposal path inside Salesforce matter, or does email stay the working process? (Move to the knowledge base session if time is short) | S1 | Not reached. Knowledge session set for 2026-09-24 |

### Routing and language

On record:

- Every IVR asks English or Spanish first. The IVR passes ANI and the menu selection, nothing else (S1 at 33:22)
- Spanish volume is too low to dedicate specialists, so the Spanish console in Oracle went unused. Mark stated a preference for the interface to switch to Spanish on a Spanish call, which Oracle could not do (S1, 43:37 to 46:14)
- Routing is least-skilled-available so specialist queues are not starved (Jul-25 at 21:29). Preserved in D15 (universal queuing restored)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-06 | Is Spanish a skill on bilingual specialists inside the least-skilled-available model, and is a Spanish-language console on a Spanish call still wanted? | S1 | Partial: Spanish stays a skill split, but not reserved routing (38:26) |
| B-07 | With universal queuing restored, does chat carry the same skill groups as voice, or does any specialist take any chat? | S2 | Partial: universal queuing, longest-waiting available, vanilla at launch (36:21 to 38:44) |

### Escalation and supervision

On record:

- Escalation queue and manager listen-in was asked on Jul-25 at 60:19, deferred to the Verint section, and never answered. Not asked on S1. No requirement exists
- Live audio monitoring is wanted and comes through Amazon Connect, not Calabrio. Live screen monitoring is declined; no STUN/TURN server (Calabrio kickoff, 2026-09-14)
- Call control today is in Cisco Jabber, separate from Oracle (S1 at 15:39). Supervisors move specialists between phone and chat by telling them to (Jul-25 at 23:21)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-08 | Is there an escalation queue or second-line group? Who takes a call the specialist cannot resolve? | Jul-25 | Not reached |
| B-09 | On a distressing or crisis call, how does a specialist get a supervisor's attention, and what does the supervisor do? | S2 | Not reached |
| B-10 | Beyond live audio monitoring, are whisper coaching and barge-in required? On a transfer, what context must travel: the inquiry, coding so far, notes? | S2 | Not reached |

### Coding data model

On record:

- Consolidating Subject 1 to 4 and Special Code 1 to 2 into multi-select was agreed directionally with no objection (Jul-25, decision 7; D17 notes)
- Subject 1 is the primary topic and the order is meaningful (S1 at 7:42)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-11 | Design decision, informed by A-07: a multi-select picklist does not preserve order. If NCI reporting depends on the primary subject, the design is a primary subject field plus a multi-select for the rest. Confirm the reporting dependency, then decide | S2 | Not reached |
| B-12 | Caller identity values seen so far are patient, spouse, friend. Confirm the full value list from the custom field export (A-01) rather than on the call | S1 | Not reached |

### Demographic survey

On record:

- Federal quota: 25 percent of cancer interactions, randomized, and 100 percent of VA interactions. A custom Oracle add-in prompts the specialist when the running rate drops below 25 percent. Demographics attach to the inquiry, never to a contact. An automated post-call survey is the client's stated biggest request (Jul-25 at 720 to 746)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-13 | Confirm the design: an IVR post-call survey randomizing to 25 percent of cancer and 100 percent of VA interactions, stored on the inquiry with no contact link. Who defines the randomization rule, CIS or NCI? What happens to the quota when the caller declines? | Jul-25 | Answered: exact configurable percentage, OMB approved, refusals count, follows the medium, 90-day VA rule, phone and chat, tobacco included (12:33 to 23:54) |

### SMS reminders

On record:

- Rebuilt rather than carried over (D19, SMS callback reminders rebuilt off Amazon Pinpoint). AWS ends Pinpoint campaigns, journeys, and segments on 2026-10-30
- **Verified 2026-09-17:** AWS End User Messaging is available in GovCloud US-West and US-East per the AWS GovCloud service page. Text to voice is US-West only. This closes Ben's S1 action
- Several workspace codes exist only to trigger the Pinpoint reports and Adrianna wants them gone (S1 at 51:27)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-14 | Where does SMS consent live today: on the contact, on the inquiry, or both? Consent has to survive the retention scrub for as long as callbacks are scheduled | S2 | Not reached |

### Retention and historical data

On record:

- Jul-25: a 13-month rolling daily scrub that hides the contact tab and message tab, leaving anonymous coding. S1: Adrianna said "about 15 months" and "all the contact records get deleted," and chat transcripts go with the message tab. Q7 (are caller records actually purged) carries the conflict
- Coding data is kept permanently in Oracle Analytics for aggregate reporting: "this data never gets deleted" (S1 at 12:02)
- Repeat callers within the window pop the existing contact and always get a new inquiry. **Decided**, D14 (repeat-caller contact pops within the retention window). Read back, do not reopen
- Scheduled future callbacks are the one Oracle data set the client has committed to migrating (Jul-25). Nobody has asked how many there are
- Q5 (Oracle object list, volumes, sample exports) has been open since kickoff. Record counts and a sample export have never been requested on any call

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-15 | Is the retention period 13 months or 15 months, and is it written in an NCI requirement the client can share? | S1 | Not reached |
| B-16 | Does the scrub delete the contact, messages, and chat transcripts, or suppress display and keep the rows? Decides whether Salesforce runs a hard delete job or field-level masking | S1 | Not reached |
| B-17 | Does the permanent coding history in Oracle Analytics migrate to Salesforce, stay in Oracle Analytics, or land in a separate reporting store? | S2 | Answered: start fresh; coding history stays in Oracle exports and government monthly summaries (11:12 to 12:29) |
| B-18 | How many scheduled future callbacks exist in Oracle today, and how far out do they run? | S2 | Not reached. Callbacks named as a possible migration exception (11:57) |
| B-19 | Confirm repeat-caller behavior as decided in D14. Read-back only | S1 | Partial: frequent flyers raised by Mark as a post-launch option (24:13, 38:01) |
| B-20 | Request record counts per Oracle object and a sample export. Ask in the recap slot | Kickoff | Superseded in part: historical data not migrating. Still needed for knowledge articles and callbacks |

### Agent environment and network

On record:

- Nearly all specialists work from home on Fred Hutch-provided machines over the Fred Hutch VPN on a special subnet, 80 Mbps home bandwidth minimum enforced, no browser lockdown (Jul-25 at 868 to 872). The VPN product was never named; do not call it GlobalProtect until Fred Hutch IT confirms
- Amazon Connect voice media uses WebRTC over UDP and AWS advises against a full-tunnel VPN

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-21 | Is the Fred Hutch VPN full-tunnel or split-tunnel for the specialist subnet? For Fred Hutch IT, not the CIS team. Belongs in the AWS roles and responsibilities conversation Avi is scheduling with Binu Pazhoor | S2 | Not reached |

---

## Settled decisions, do not reopen

| Register row | Decision |
| --- | --- |
| D2, Amazon Connect in AWS GovCloud | `us-gov-west-1`, partition `aws-us-gov` |
| D13, agent desktop is Salesforce | Specialists receive and control calls in Salesforce through Service Cloud Voice. Amazon Connect is telephony and routing |
| D14, repeat-caller contact pops within the retention window | Pop the existing contact if one exists, always open a new inquiry, nothing persists past the scrub |
| D15, universal queuing restored | Voice and chat to the next available specialist through Omni-Channel, least-skilled-available |
| D16, web-based single-sign-on agent experience | Browser only, SSO against standard Microsoft Active Directory with Fred Hutch logins |
| D17, inquiry workspace streamlined by call type | Layouts by call type, coding on every type |
| D18, entry points do not change | Numbers, chat page, email address stay |
| D19, SMS callback reminders rebuilt | Rebuilt on AWS End User Messaging, available in GovCloud |
| D20, scope boundaries | VA Direct stays manual, external trial search sites out of scope |

Target org: Salesforce Government Cloud Plus, instance `USA9014`, org `00Dcs00000LoZ05EAF`.

## Proposed register updates

For Ben to apply or approve. None applied.

| Row | Proposed change | Basis |
| --- | --- | --- |
| D19 (SMS callback reminders rebuilt off Amazon Pinpoint) | Add note: AWS End User Messaging is available in GovCloud US-West and US-East, verified 2026-09-17 against the AWS GovCloud service page. Text to voice is US-West only. Design dependency closed | AWS documentation |
| Q5 (Oracle object list, volumes, sample exports) | Add the Oracle Analytics coding history and the scheduled future callback count as named sub-questions | S1 and this guide |
| D17 (inquiry workspace streamlined by call type) | Add note: Subject 1 ordering must be preserved or explicitly dropped; confirm the NCI reporting dependency before consolidating to multi-select | Jul-25 at 42:32, S1 at 7:42 |

## Technical reference

### Amazon Web Services

- [AWS Pinpoint migration guide](https://docs.aws.amazon.com/pinpoint/latest/userguide/migrate.html). Journeys, campaigns, and segments retire 2026-10-30
- [AWS End User Messaging SMS user guide](https://docs.aws.amazon.com/sms-voice/latest/userguide/what-is-service.html)
- [AWS End User Messaging in AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-eum.html). Both GovCloud regions listed; text to voice US-West only
- [Amazon Connect network connectivity guidance](https://docs.aws.amazon.com/connect/latest/adminguide/troubleshooting-network-connectivity.html)
- [Amazon Connect in AWS GovCloud (US)](https://docs.aws.amazon.com/connect/latest/adminguide/govcloud.html)

### Calabrio

- The FedRAMP Moderate authorized product is Calabrio GovSuite. A previous marketplace link (product FR2110283088) returned 404 on 2026-09-17. Search [the FedRAMP marketplace](https://marketplace.fedramp.gov/) for the current listing and confirm the product name with Trevor Holt
- Open from the Calabrio kickoff, 2026-09-14: Salesforce chat into Calabrio is a stated client requirement absent from both statements of work, Trevor Holt owns feasibility and cost (D10 under revision). Amazon Connect keeps interval data only a few days, so Calabrio must capture from Connect's first call. 60 QM and 60 WFM licenses against 40 to 45 agents is unreconciled

### Salesforce

- [Service Cloud Voice implementation guide](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_intro.htm)

### NCI public channels

Per [the NCI contact directory](https://www.cancer.gov/contact). The authoritative CIS list is A-04.

- Cancer Information Service: 1-800-4-CANCER (1-800-422-6237)
- Tobacco Quitline: 1-877-44U-QUIT (1-877-448-7848)
- Veterans Quitline: 1-855-QUIT-VET (1-855-784-8838)
- CCR line: number not yet provided

## Change log

- **2026-09-17, revision 2.** Restructured into Avi's and Ben's sections with permanent IDs, origin, and status columns. Merged Avi Rabinovitch's plan: his 14 questions became A-05 to A-18, with Ben's aligned items folded in (required fields, statuses, Subject ordering, CCR, callbacks, external sites). Smoking cessation and VA deferred by design. Protected eight minutes for Ben's retention and tiers questions
- **2026-09-17, revision 1.** Checked every question against the record. Removed answered questions (repeat caller, quota tracking, CCR identification, calendar view). Added Subject ordering gap, review workflow, callback volume, record count request, Holly Fernandez-Johnson attendance. Corrected the VPN claim, the Calabrio product and link, and verified AWS End User Messaging in GovCloud

# Discovery session 3 guide: call-type workflows, live in Oracle

Prep guide for the third discovery session with the Fred Hutch NCI Cancer Information Service (CIS) team. Same two-section structure as session 2:

- **Avi's section:** process and workflow. Call walkthroughs, what the specialist does, how work moves. Avi runs the call
- **Ben's section:** architecture, permissions, data, and vendors. Design decisions, access model, retention, migration inputs

**This is part two of the workflow discovery.** Session 2 on 2026-09-17 was planned as the call-type walkthrough and became reports, surveys, routing and email instead. Almost the whole of Avi's section went unreached. Those questions carry their original IDs into this guide, unrenumbered.

## How this guide works across sessions

- Every question carries a permanent ID: `A-nn` for Avi's, `B-nn` for Ben's. IDs never renumber. A question that is not reached keeps its ID in the next guide
- **Origin** says where the question first came up. `Jul-25` is the 2025-07-29 reverse demo, `S1` is 2026-09-15, `S2` is 2026-09-17, `Oracle-tour` is the 2026-09-21 environment walkthrough with Mark Hubers, `AWS-21` is the Amazon product and SOW alignment research of 2026-09-21, `S3` is new for this session
- **Status** is blank before the session. **Filled 2026-09-22 against the session 3 transcript** at transcripts/2026-09-22-discovery-session-3-general-cancer-callbacks.md, as `Answered`, `Partial`, `Not reached`, or `Not for the call` for items held off the agenda by design. Not reached and Partial rows open the session 4 guide
- **On record** lines give what the client has already said, with the source, so a question becomes a read-back instead of a repeat
- New IDs this session start at `A-27` and `B-22`

**Audience:** internal Kicksaw. Ben Bolding and Avi Rabinovitch. Not a client deliverable and not pushed anywhere.

Built 2026-09-22 against the session 2 guide, the session 2 transcript, the 2026-09-21 Oracle test environment transcript, the Amazon product and SOW alignment document, the decision register, and the calendar.

---

## Session details

- **Date and time:** Tuesday 2026-09-22, 2:00 to 3:00 PM ET. 60 minutes. Microsoft Teams, Mike Griffin organizing
- **Topic:** the inquiry live in Oracle, by call type. Mark Hubers set this up on 2026-09-21 (27:06): Holly Fernandez-Johnson will be "live, hands on in this," showing general cancer, smoking cessation, VA, clinical trials and CCR. Avi's own ask at the close of session 2 (58:56) was the handshake from system to specialist for phone, chat and email, and the data captured per call type, where they converge and where they differ
- **Client attendees on the invite:** Adrianna Gutierrez, Mark Hubers, Jennifer Macabeo, Holly Fernandez-Johnson, Reetu Ghumman, Ray Quijano, Mike Griffin
- **Kicksaw attendees on the invite:** Ben Bolding, Hannah Oanca. **Avi Rabinovitch and Ian Devlin are not on the Tuesday series.** They are on the Thursday series as optional. Fix before the call if Avi is running it
- **Partners on the invite:** Binu Pazhoor and Ken Daugherty (AWS), Mitchell Rabin (Salesforce). See the AWS attendance note below

### AWS attendance is still a live decision

The position carried from session 2 has not changed and has not been actioned. Binu Pazhoor pitched an Amazon Connect Agent Workspace architecture on session 1, the client heard two designs on one call, and Ben owes Binu Pazhoor and Ken Daugherty an alignment on the agent desktop decision (D13, agent desktop is Salesforce) before the next joint AWS session. That alignment has not happened.

Three of the sharpest new architecture items (B-28 transcription, B-29 FIPS endpoints, B-31 Connect feature gaps) are **AWS questions, not client questions.** Putting them to AWS in front of the client turns an internal verification exercise into a visible gap in Kicksaw's own understanding.

**Recommendation:** do not raise the FIPS or transcription items on this call, whoever is present. Reason: neither has an answer yet, both read to the client as "the platform you bought may not do what we said," and the honest version of that conversation needs the AWS answer in hand first. B-22 (email) is the exception and is handled differently; see below.

---

## Agenda

**Avi's plan, sent by email and surfaced in Slack 2026-09-22 at 1:26 PM. This supersedes the five-type agenda in revision 1.**

Workflows, in this order:

1. General cancer
2. Clinical trials, including CCR and the trial search handoff
3. Smoking cessation, including VA. **The callback series, VA referrals and SMS reminders get their own session**
4. Anything that does not fit the three above

For each one, the same four questions:

| # | Avi's question | Guide items it answers |
| --- | --- | --- |
| Q1 | What does the specialist capture, and at what point in the conversation? | A-05, A-09, A-13, A-14, A-23, B-14 |
| Q2 | Which codes are required, and which exist only to trigger something or feed a report? | A-06, A-07, B-11, A-29, B-25 (SCIF), B-24 (dead queues and rules) |
| Q3 | What changes depending on whether it is a call, a chat or an email? | A-08, A-16, B-22 (email is Email-to-Case), B-23 (chat entry) |
| Q4 | How does it end: status, follow-up, callbacks and any survey offered? | A-11, A-15, A-17, A-21, A-12 (after-call work) |

**Deferred again to the callback and VA session:** A-22 (VA Direct referral fields), A-24 (calendar view and callback ownership), A-25 (unanswered VA callbacks), A-26 (SMS reminder text), B-18 (count of scheduled callbacks).

**No protected Ben slot in Avi's plan.** Ben's items ride inside the four questions:

- **B-22, email** lands naturally in Q3 on general cancer, the first time email comes up. Say it once as a confirmation there
- **B-23, chat entry** also lands in Q3. Answer Mark there
- **B-24, cleanup deciders** lands in Q2 whenever a code or queue turns out to exist only for a report or a dead program
- **B-09, crisis escalation** fits in bucket 4, anything that does not fit
- **B-15, B-16, retention** do not fit today's structure. Carry them unless bucket 4 has room

## Avi's section: process and workflow

### Recap and outstanding artifacts

| ID | Item | Owner on client side | Origin | Status |
| --- | --- | --- | --- | --- |
| A-01 | Workspace rules list, workspace definition, and custom field list including the special codes | Adrianna Gutierrez, Mark Hubers | S1 | **Largely superseded.** Kicksaw can now export these directly from the test environment (Oracle-tour, 18:55 and 19:52). Ask only for what the export cannot give: which rules are actually live. Not reached on the call |
| A-02 | Full call type list, including Jennifer Macabeo's document from the last migration | Adrianna Gutierrez, Jennifer Macabeo | S1 | Still outstanding. Ask again. Not reached on the call |
| A-04 | Authoritative inbound number, DNIS and IVR list | Mark Hubers | S1 | Still outstanding. Compounds with the service numbers list Mark showed on 2026-09-21, which nobody can say is current. Not reached on the call |
| A-27 | Report definitions export from Oracle Analytics, promised at session 2 (6:14) | Adrianna Gutierrez, Mark Hubers | S3 | Not reached |
| A-28 | Full skill list with associated coding, and the current AUX code list, asked in chat at session 2 (33:31) | Holly Fernandez-Johnson, Jennifer Macabeo | S3 | Not reached |

### General cancer (1-800-4-CANCER, Cancer Line queue)

On record:

- Every interaction creates an inquiry. Contact fields first, then notes, then coding after the interaction (S1, Adrianna at 48:02)
- Subject 1 through 4 are cancer topics mirroring cancer.gov. **Subject 1 is the primary topic**, then descending. Four fields exist only because Oracle had no multi-select (S1 at 7:42, Jul-25 at 42:32)
- **Coding has one universal section then type-specific sections.** Mark, Oracle-tour at 09:16: "all calls will have this filled out, whether it's a cancer or a clinical trials or smoking." Confirms D17 (inquiry workspace streamlined by call type) from the configuration rather than from a demo
- Anonymity governs. Contact details are asked only for email follow-up or a callback (Jul-25). Chat requires nothing to start (S1 at 33:49)
- Standard text is templated responses with F9 hotkeys, separate from knowledge. The Messages tab carries inbound email bodies and full chat history on the inquiry (Oracle-tour, 10:47)
- Calls run up to an hour. "We are not a speed of service group. We are a quality service" (S2, Mark at 24:13)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-05 | Walk one call from answer to close. What does the specialist fill in before, during and after? Read back the contact, notes, coding order and let them correct it | S2 | **Answered** (4:50 to 26:43). Specialist opens the inquiry by hand from Finesse; queue selection creates a placeholder contact and triggers demographics; point of access, service number, queue and phone **used to auto-fill and no longer do**; knowledge and standard text during the call; a lead helps over Teams; coding is passive and mostly after the call; send on save; close; specialist sets themselves available by hand |
| A-06 | Which fields are required before an inquiry can close? Which are optional or exist only for reports? Does it differ by call type? | S2 | **Partial** (9:53 to 10:45). Contact is system-required, so a placeholder is used; name and email are not required. No full list of required fields |
| A-07 | How do they choose Subject 1 to 4 on a live call? Confirm Subject 1 is always primary. Then ask whether any NCI extract or report depends on the primary versus secondary distinction. (Feeds B-11) | S2 | Not reached |
| A-08 | When does a general call need email follow-up? What goes out (standard text, knowledge article, links), and from which mailbox? | S2 | **Partial** (16:18, 19:23). Email goes out when something was offered, by send on save. General cancer is not reviewed except for new specialists after training. Knowledge inserts carry internal notes and need a sendable version (10:46 to 13:14). Hard copy mailings go through a resource specialist report. Sending mailbox not covered |
| A-09 | When a caller stays anonymous, what is the minimum captured? Can an inquiry close with no contact? | S2 | **Answered** (9:53 to 10:45). Phone number on calls; `anonymous@anonymous` placeholder on chat; name and email only when something is sent. The inquiry always has a contact, sometimes a blank one |
| A-10 | When a general call turns into a clinical trials or smoking question: new inquiry, re-coded, or transferred? Include the CCR case (S1 at 21:41, infrequent) | S2 | Not reached |
| A-11 | Which statuses does a phone inquiry move through, who moves it, and what does review complete unlock? Email statuses were walked on session 2; phone was not | S1 | **Partial** (16:18, 25:55). Close after send; a "resource support" status routes mailings to a report. No phone status list walked |
| A-12 | How much of an interaction is after-call work? Session 2 gave "up to an hour" but no averages. Calabrio workforce management forecasting needs a number | S2 | **Partial** (16:18, 25:55). Most coding happens after the call; no automatic return to available. No averages |

### Clinical trials (Clinical Trial queue), including CCR

On record:

- Clinical trials coding is "similar but more detailed" than general cancer, with additional fields when it is CCR (S1, Mark at 20:57)
- A CCR inquiry is identified by the dedicated CCR phone number or the CCR website email template (S1 at 21:24). CCR inbound forms arrive through the NIH inbox (S2, Holly at 40:27)
- **CCR has an outbound report.** Mark, Oracle-tour at 10:00: "We built this report to have an ability to email. So we forward the contents of this report to them." CCR and VA are different recipients; Mark corrected Ben on that at 10:19
- Clinical trial searches generate up to two follow-up callbacks (S1, Adrianna at 32:04)
- Specialists search external clinical trial websites, which are out of scope (D20, scope boundaries)
- A clinical trial email needing a search goes to a different agent for the search and comes back. History is retained so anyone can reply (S2, Ray at 50:11)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-13 | What extra detail is captured beyond general cancer: diagnosis, stage, location, travel limits, prior treatment? And what more for CCR? | S2 | Not reached. Thursday 2026-09-24 |
| A-14 | Which external sites do they search, and what comes back into the inquiry: trial IDs, links, notes, or nothing? | S2 | Not reached. Thursday 2026-09-24 |
| A-15 | The two callbacks: what triggers each, how many days apart, who owns them, and what counts as done? Same task mechanism as the VA callbacks? | S1 | **Partial** (51:19). Clinical trials is "now down to 2" callbacks. Same task and report mechanism as VA implied, not confirmed. Triggers and spacing not covered |
| A-16 | How do search results reach the client: email, phone, or both? Is there a standard template? | S2 | Not reached. Thursday 2026-09-24 |
| A-17 | If the client does not answer a callback, how many attempts, and when does it close? (Ask once here; the answer likely applies to VA too, A-25) | S2 | **Answered for VA** (52:06 to 54:46). Three attempts per callback: within the scheduled hour, 15 minutes later, next business day at the original time. All three fail and the series ends. Not confirmed for clinical trials |
| A-19 | When a general clinical trials call becomes a CCR conversation, what changes on the inquiry, and does the CCR report still pick it up? | S2 | Not reached. Thursday 2026-09-24 |
| A-20 | Is the CCR email report a requirement to rebuild as is, or is a scheduled Salesforce report to the same recipients acceptable? | S2 | Not reached. Thursday 2026-09-24 |
| A-21 | Do clinical trials inquiries follow the same statuses and review workflow as general cancer? | S2 | **Partial** (19:23). Every clinical trials outbound message is reviewed before send. Statuses not covered |

A-18 (confirm the clinical trials specialist group and reserved routing) is **closed.** Session 2 settled it: launch routing is vanilla, longest-waiting available, no reserved groups, language as the only skill split (36:21 to 38:44). Do not reopen.

### Smoking cessation and VA

Deferred by design on session 2. In scope today because Holly is covering all five types.

On record:

- VA clients arrive by the VA toll-free number (the majority), clinic referral, or chat. Referrals come through VA Direct, which cannot be integrated. Specialists copy referrals into Oracle as contacts and create callback tasks (S1 at 31:08; D20)
- **The SCIF is the Smoking Cessation Intake Form**, a separate document added to an inquiry from the smoking cessation tab (Oracle-tour, 07:46). It is a guide, not a script, completed for everyone who gets a counseling session (Jul-25 at 32:08)
- **The SCIF exists primarily for the VA and is over-collected.** Mark, Oracle-tour at 08:19: "the VA likes a lot of data, which is why we have so many things." At 08:32: "We don't know exactly what they do with that data, and we do know that we don't regularly collect a lot of data. It's kind of random. So this is one of those things that we can probably revisit or clear up some." The client volunteered the reduction
- Callbacks are opt-in. Tobacco cessation gets four, more if wanted. Scheduled callbacks exist months and years ahead and must migrate. Specialists work half-hour blocks from a report; clients get a 30-minute window. Fred Hutch asked for a calendar view. No queued or automated dialing (Jul-25 at 616 to 650)
- SMS reminders go 24 hours and about two hours ahead, to clients with SMS consent and callback enrollment, no PII or PHI (S1 at 50:10)
- **Tobacco is in the 25 percent demographic survey population**, not just cancer (S2, Adrianna at 12:33). VA is 100 percent, with a 90-day no-resurvey rule

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-22 | Which fields does a specialist copy from a VA Direct referral to create the contact and the first callback? Ask for a redacted example | S1 | Not reached |
| A-23 | Should the SCIF present as a guided screen flow or as a tab of fields in any order? Does it change between the first session and later callbacks? | S2 | Not reached |
| A-24 | Confirm the calendar view is still the ask. Who works a callback block: the specialist who did the intake, or whoever is scheduled? | Jul-25 | **Partial** (36:33 to 40:57). No one is assigned a callback: shift specialists work the report one at a time, off inbound for the shift. Whoever makes a callback schedules the next. Calendar view not reconfirmed |
| A-25 | Unanswered VA callbacks: attempts, and when the series closes | S2 | **Answered** (49:18 to 56:51). Three attempts per callback, each a new task; the series ends if all fail. VA typically up to 4 callbacks, extendable to about 9. The VA wants callback and attempt numbers |
| A-26 | What is the exact SMS reminder text today? | S2 | **Partial** (43:56 to 45:45). Standard text, no PII or PHI, "We're going to call you at 9:30 AM." Sent 24 hours and **one hour** before, which conflicts with about two hours at S1. Replies get an automated "call us." Pinpoint writes status back to Oracle. Exact text not supplied |
| A-29 | **The SCIF reduction, raised as the client's own idea.** Mark offered it; Holly and Adrianna have to size it. Which SCIF fields does the VA actually consume, and who at the VA can say? Do not propose dropping fields until that is answered (B-25) | Oracle-tour | Not reached |

### Convergence

The close of Avi's section, and the thing the whole session is for.

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-30 | Read back the common spine: every interaction is an inquiry, universal coding on every type, then a type-specific section. Confirm or correct | S3 | **Answered** (14:37 to 14:41). Mark and Holly confirmed that universal coding is filled out on every interaction type and channel, **except callback tasks, which have their own fields** |
| A-31 | Which call type is the **most complex** to get right, in their view? The answer sets build sequence, and only they can rank it | S3 | **Partial** (58:34 to 59:10). Clinical trials "is gonna take a while," with lots of little pieces; VA is the most complex smoking line. No explicit ranking |

---

## Ben's section: architecture, permissions, data, and vendors

### The email channel, which is a statement rather than a question

**This is the most important eight minutes on the agenda and it is new since session 2.**

Amazon Connect has **no email channel in AWS GovCloud.** AWS documents email, outbound campaigns and customer profiles as unavailable in `us-gov-west-1`, which is the only GovCloud region Amazon Connect runs in, and the partition decision (D2, Amazon Connect in AWS GovCloud) is settled.

Session 2 spent roughly 20 minutes on the email workflow: two NIH inboxes auto-forwarding into Oracle, send-as authority on behalf of nih.gov, manual triage, mandatory review before send, and tracked editing. Avi named Email-to-Case as the pattern and Mark asked for the Salesforce equivalent so the forward can be repointed. **That instinct was right and it is now the only option, not a preference.** Nothing said on session 2 is invalidated. What changes is that the architecture is no longer a choice.

| ID | Item | Origin | Status |
| --- | --- | --- | --- |
| B-22 | **State it:** email is delivered by Salesforce Email-to-Case. Amazon Connect carries voice and chat. Record it as a decision. Then confirm nothing in the session 2 email workflow assumed otherwise | AWS-21 | Not reached. Email-to-Case was not stated |

**How to say it:** as a confirmation of the design they already heard, not as a discovery. "Email comes in through Salesforce, not the telephony layer. That is what Avi described on Thursday and it is what we are building." It only becomes a problem if someone asks why, and the answer is straightforward: the Government Cloud region does not carry Connect's email channel, and the Salesforce path is the better one anyway because the review and tracked-editing requirement lives on the case.

**Recommendation:** do not volunteer the GovCloud limitation unprompted. Reason: the outcome is identical to what they were told, the limitation is not a constraint anyone at CIS can act on, and naming an absence invites a question about what else is absent, which is exactly the question Kicksaw cannot yet answer (B-28, B-29).

### Chat entry architecture, which Mark asked and is owed an answer

On record:

- The Live Help button on cancer.gov launches Oracle chat directly. The pop-up window is Oracle, not the website (S2, Jennifer and Mark at 25:40)
- Mark, S2 at 27:28: "Will that go through AWS? I thought that would go through Salesforce." **Deferred to Ben and not yet answered**
- Universal queuing across voice and chat is settled (D15). Chat at launch carries the same longest-waiting-available model

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-23 | Chat entry: Salesforce Messaging for Web, or Amazon Connect chat? And who re-points the cancer.gov Live Help button, since the NCI web team owns that page and is not in this room? | S2 | Not reached. **Carried a third time** |

**Recommendation:** answer Mark directly this session even if the answer is "here is the decision and here is why," rather than carrying it a third time. Reason: he asked a precise architecture question in front of his colleagues and was deferred. Coming back with it unprompted is worth more to the relationship than the answer itself. The dependency to flag regardless of which way it goes is that **a third party outside this room has to change a button on cancer.gov**, and that has lead time nobody has scoped.

### Configuration cleanup, and who decides it

On record, all from the 2026-09-21 Oracle tour:

- Queues and service numbers are fourteen years of accumulation. "Some of these are no longer in use, but we still have the records in here" (11:31). "We can definitely clean some of this stuff up" (11:37)
- COVID-era queues added speculatively and never removed (13:32). "POS phone calls, we don't do anymore, I don't think" (13:22). "ProActor" and "Impact": Mark does not know if they are live
- **There is no documented drop list.** Mark, 12:54: "This was built out over the last 14 years by Adrianna... those are all discussions that we'll have to hear from Adrianna and Holly, because I don't have the background on it"
- Business rules live in two separate places and they are different rules: workspace rules driving the agent UI (NCI Inquiry v2.1) and site configuration rules driving system processing across seven object tabs. Mark, 23:39: "Most of this was either set up by Adrianna or was set up by consultants when we first launched it"
- Mark agreed directionally that only active rules carry forward, but said "I believe so." Adrianna has to confirm

**Adrianna Gutierrez and Holly Fernandez-Johnson are both on this call. They are the only two people who can answer this and they are rarely both available.**

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-24 | Queues, service numbers and business rules: what is actually live, and what gets dropped? No documented list exists and Mark cannot decide it. Frame it as a scope reduction opportunity, not a request for homework | Oracle-tour | Not reached. Adds to the inventory: task workspace rules (47:56), and "proactive calls" may be the ProActor queue (41:19) |
| B-25 | What does the VA actually require from the SCIF? Without it, the field set cannot be safely reduced. (Pairs with A-29) | Oracle-tour | Not reached |
| B-32 | Who can explain the **intent** behind the rules set up by the original launch consultants, if anyone still can? | Oracle-tour | Not reached |

**Recommendation:** ask for a working session on rationalization rather than a list. Reason: asking Adrianna to produce a drop list for fourteen years of configuration is a large unbounded homework item that will not come back; walking the live list with her for an hour will.

### Retention and historical data

On record:

- **Start fresh is decided.** Historical coding, interaction and phone data are not migrated. Exceptions named by Mark: the knowledge base, scheduled callback tasks "potentially," and in-flight work at cutover (S2 at 11:12 to 12:29). Do not reopen; read back only if challenged
- Jul-25 recorded a 13-month rolling scrub hiding the contact and message tabs. S1, Adrianna said "about 15 months" and "all the contact records get deleted." **The conflict is unresolved**
- Coding data is kept permanently in Oracle Analytics: "this data never gets deleted" (S1 at 12:02). That now stays in Oracle exports and government monthly summaries
- Repeat callers within the window pop the existing contact and always get a new inquiry (D14). Decided
- **NCI's own position on historical data is still unconfirmed.** Adrianna spoke for CIS. July 2025 recorded that historical data scope "would have to be a discussion with NCI"

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-15 | Is the retention period 13 months or 15 months, and is it written in an NCI requirement the client can share? | S1 | Not reached |
| B-16 | Does the scrub delete the contact, messages and chat transcripts, or suppress display and keep the rows? Decides hard delete versus field-level masking in Salesforce | S1 | Not reached |
| B-18 | How many scheduled future callbacks exist in Oracle today, and how far out do they run? One of only three data sets still migrating and nobody has asked for a count | S2 | **Partial** (41:57). Adrianna took outbound volume away as a follow-up |
| B-33 | Has NCI confirmed it is comfortable with historical data staying in Oracle exports and the government monthly summaries? | S2 | Not reached |

**B-33 is the one to be careful with.** It is a real gap and it is also the client's own decision being questioned five days after Avi locked it in. Ask it as a paperwork question, not a challenge: what does NCI need to see to have this on the record.

### Permissions and administration

On record:

- **The permission model is not lift-and-shift.** Mark, Oracle-tour at 25:39: "We don't need a lift and shift with this. We can do it however, whatever makes sense in Salesforce and AWS." Decision-grade and unprompted
- An Oracle profile bundles four concerns: languages spoken, clinical trials chat eligibility, knowledge base read, knowledge base edit (25:13)
- Skill groups are hierarchical today: everyone cancer, some add tobacco, then clinical trials, then Spanish. Built to reserve agents for low-volume queues, and "not the most helpful for us now" (S2, Holly at 31:32)
- Reports: supervisors and above view, administrators edit the shared ones. Access was cut back after reports "kept disappearing" (S2 at 5:14)
- Email has a second-tier PIQ subset at CIS discretion (S2 at 46:32)
- Five CIS staff configure the current platform and expect to configure the new one (S1 at 6:02)

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-02 | Where is the administration boundary in the new platform? Which changes do the five CIS administrators make directly, and which go through Fred Hutch IT or Suchi Panda's cloud team? | S2 | Not reached |
| B-03 | Does the Fred Hutch IT change approval board govern Salesforce configuration changes? | S2 | Not reached |
| B-34 | Read back the capability list a profile has to cover: language, clinical trials chat, knowledge read, knowledge edit, report view, report edit, email review, PIQ. Is anything missing? This replaces mirroring the Oracle profile taxonomy | Oracle-tour | Not reached. Two capabilities to add: lead or supervisor live view of notes, and resource specialist mailing |

B-01 (tiers or flat) is answered well enough by session 2 to close as a question and become a design input. Holly described the hierarchy and said it no longer fits.

### Escalation and supervision

Never answered on any call. Asked on Jul-25 at 60:19, deferred to the Verint section, never returned to. Not asked on S1 or S2. **No requirement exists.**

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-08 | Is there an escalation queue or second-line group? Who takes a call the specialist cannot resolve? | Jul-25 | **Partial** (13:14, 22:00). Designated leads help live over Teams. No escalation queue described |
| B-09 | On a distressing or crisis call, how does a specialist get a supervisor's attention, and what does the supervisor do? | S2 | Not reached |
| B-10 | Beyond live audio monitoring, are whisper coaching and barge-in required? On a transfer, what context must travel: the inquiry, coding so far, notes? | S2 | **Partial** (22:00 to 22:36). The context ask is a lead seeing the specialist's notes live. Avi floated full call transcripts, which depends on B-28 |

These have been carried three sessions. Holly owns quality management and is on this call. **If the walkthrough runs long, B-09 is the one to save**, because a cancer information line with no defined crisis escalation path is a design gap, not just an unanswered question.

### Coding data model

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-11 | A multi-select picklist does not preserve order. If NCI reporting depends on the primary subject, the design is a primary subject field plus a multi-select for the rest. Confirm the reporting dependency, then decide. Informed by A-07 | S2 | Not reached |
| B-12 | Caller identity values: patient, spouse, friend seen so far. **Now answerable from the custom field export**, not from the call. Do not spend session time on it | S1 | **Partial** (15:05 to 15:39). Client type is the person contacting. The patient distinction matters only for clinical trials and CCR, including whether the patient knows |

### SMS consent

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-14 | Where does SMS consent live today: on the contact, on the inquiry, or both? Consent has to survive the retention scrub for as long as callbacks are scheduled. Sharper now that callbacks are one of only three migrating data sets | S2 | Not reached |

### Oracle environment logistics

Small items, all from the 2026-09-21 tour. Mark owns all three and none needs session time. **Handle by email or Slack, not on this call.**

| ID | Item | Owner | Origin | Status |
| --- | --- | --- | --- | --- |
| B-26 | The surveys grant did not take. Mark intended it, and at 28:27 found Kicksaw has no surveys access. The demographics survey is the single artifact Kicksaw most needs from that environment | Mark Hubers | Oracle-tour | Not for the call |
| B-27 | One shared Oracle login, one concurrent session. Ben's login ejected Mark mid-demo. Ben and Ian cannot work in parallel. Named accounts? | Mark Hubers | Oracle-tour | Not for the call |
| B-35 | Console session timeout length, and what the staff profiles export button actually produces | Mark Hubers, Ian Devlin | Oracle-tour | Not for the call |

### AWS items: not for this call

Recorded here so they are not lost, and deliberately excluded from the agenda. All three are Kicksaw-to-AWS, owned by Ben with Ken Daugherty and Binu Pazhoor.

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-28 | Real-time transcription in AWS GovCloud. The GovCloud service page lists conversational analytics AI features as unavailable; AWS separately announced Contact Lens general availability in GovCloud US-West on 2025-07-01 including call transcription. Both cannot be complete. Get it in writing | AWS-21 | Not for the call. AWS absent |
| B-29 | FIPS endpoints for Amazon Connect in `us-gov-west-1`. Salesforce requires FIPS-compliant telephony endpoints; AWS publishes Connect FIPS endpoints in three regions and `us-gov-west-1` is not among them. Ask for control plane and voice media path separately, with CMVP certificate numbers | AWS-21 | Not for the call. AWS absent |
| B-30 | Does the Government Cloud org expose AWS GovCloud as a selectable region during contact center setup, or does that need a Salesforce support case? | AWS-21 | Not for the call |
| B-21 | Is the Fred Hutch VPN full-tunnel or split-tunnel for the specialist subnet? Fred Hutch IT, not CIS. Belongs in the AWS roles and responsibilities conversation | S2 | Not for the call |

One AWS-derived item **is** a legitimate client question and costs thirty seconds:

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-31 | Confirm CIS is inbound only, with no outbound dialing campaigns. Outbound campaigns are unavailable in AWS GovCloud. July 2025 recorded no queued or automated dialing, so this is a read-back that closes a gap quietly | AWS-21 | **Answered, and it is not inbound only** (32:49 to 54:46, 41:19). Callbacks, proactive calls and phone follow-up surveys are **manual, agent-dialed outbound calls**. No campaigns or automated dialing, which fits July. Inferred, not verified: agent-initiated outbound in Amazon Connect is separate from outbound campaigns. Confirm with AWS |

### Commercial item, Ben's judgment call

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-36 | Three vendors landed on 60 licenses against a stated 40 to 45 agents: Salesforce user licenses, Salesforce Voice with Partner Telephony, Calabrio Quality Management, Calabrio Workforce Management. It was raised at the Calabrio kickoff and nobody questioned it. What is 60 based on? | AWS-21 | Not for the call |

**Recommendation:** not on this call. Reason: it is a procurement question in a workflow session, Mike Griffin and Reetu Ghumman are the right audience for it, and it lands better as a line in a status conversation than as an aside during Holly's demo.

---

## Settled decisions, do not reopen

| Register row | Decision |
| --- | --- |
| D1, scope | Oracle Service Cloud to Salesforce Government Cloud. No standard Salesforce org migration |
| D2, Amazon Connect in AWS GovCloud | `us-gov-west-1`, partition `aws-us-gov` |
| D13, agent desktop is Salesforce | Specialists receive and control calls in Salesforce through Service Cloud Voice. Amazon Connect is telephony and routing |
| D14, repeat-caller contact pops within the retention window | Pop the existing contact if one exists, always open a new inquiry, nothing persists past the scrub |
| D15, universal queuing restored | **Revised by session 2.** Launch routing is longest-waiting available, universal across voice and chat, language as the only skill split, no reserved groups. Supersedes the July least-skilled-available reasoning |
| D16, web-based single-sign-on agent experience | Browser only, SSO against Microsoft Active Directory with Fred Hutch logins |
| D17, inquiry workspace streamlined by call type | Layouts by call type, universal coding on every type. Independently confirmed from Oracle configuration 2026-09-21 |
| D18, entry points do not change | Numbers, chat page, email address stay |
| D19, SMS callback reminders rebuilt | On AWS End User Messaging, available in GovCloud. Pinpoint campaigns and journeys retire 2026-10-30 |
| D20, scope boundaries | VA Direct stays manual, external trial search sites out of scope |
| New, session 2 | Start fresh on data. Only the knowledge base, scheduled callbacks and in-flight work migrate |
| New, session 2 | Demographic survey moves off the in-call pop-up to an automated post-interaction prompt following the medium |
| New, Oracle tour | The permission model is designed fresh against Salesforce and Amazon Connect primitives, not mirrored from Oracle profiles |
| New, session 2 | AI features require explicit Fred Hutch and NIH approval; nothing trains on CIS data. Parked |

Target org: Salesforce Government Cloud Plus, instance `USA9014`, org `00Dcs00000LoZ05EAF`. Telephony model: Partner Contact Center with Amazon Connect, bring-your-own, 60 seats licensed and 0 assigned. No AppExchange package required.

---

## What has to happen before 2:00 PM

| # | Item | Owner |
| --- | --- | --- |
| 1 | Get Avi Rabinovitch and Ian Devlin onto the Tuesday invite, or forward the Teams link. Neither is on the series | Ben Bolding |
| 2 | Decide whether AWS joins, and if they do, hold B-28 and B-29 | Ben Bolding |
| 3 | Decide the answer to B-23 (chat entry) so Mark's question gets answered rather than deferred a third time | Ben Bolding |
| 4 | Confirm Holly has the Oracle test environment ready, and that Ben is **not** logged into the shared account during her demo. One concurrent session only, and Ben's login ejected Mark on 2026-09-21 | Ben Bolding |

Item 4 is not housekeeping. The same shared login that Holly will be demonstrating from is the one Kicksaw uses, and it has already kicked a client presenter out of a live call once.

---

## Change log

- **2026-09-22, revision 3.** Status filled against the session 3 transcript. General cancer was walked end to end and the VA callback model was covered in depth despite the deferral; clinical trials was not reached and moves to Thursday 2026-09-24 with Spanish. AWS did not attend. B-31 answered the other way: CIS makes manual outbound calls. B-23 (chat entry) carried a third time
- **2026-09-22, revision 2.** Agenda replaced with Avi Rabinovitch's plan: three call types plus a catch-all, four questions each. Mapped guide items onto the four questions. Callback series, VA referrals and SMS reminders deferred to their own session (A-22, A-24, A-25, A-26, B-18). Ben's protected slot removed; his items ride inside Q2, Q3 and bucket 4
- **2026-09-22, revision 1.** Created as the session 3 guide. Carried every unreached item from the session 2 guide at its original ID. Added A-27 to A-31 (outstanding artifacts, SCIF reduction, convergence read-back) and B-22 to B-36 (email channel, chat entry, configuration cleanup, NCI historical-data concurrence, capability read-back, Oracle logistics, the four AWS-owned items, inbound-only confirmation, the 60-license basis). Closed A-18 and B-01 against session 2. Marked B-12 answerable from export rather than from the call. Recorded the Avi and Ian invite gap and the unresolved AWS alignment

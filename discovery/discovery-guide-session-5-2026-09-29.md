# Discovery session 5 guide: channels, handoffs, and what leaves CIS

> **Frozen 2026-09-29.** Published to the Notion Project Library as [Discovery session 5 guide](https://app.notion.com/p/3ead4b87741781e9bee3dde9e5e08f9b). The Notion page is the live copy; edit there, not here.

Prep guide for the fifth discovery session with the Fred Hutch NCI Cancer Information Service (CIS) team. Avi Rabinovitch is on PTO and Mike Griffin is out all week, so Ben Bolding and Ian Devlin run it. The guide keeps the two-section structure, with Ian's section in place of Avi's:

- **Ben's section:** the four channels (chat, email, text reminders, phone), routing, review before sending, clinical trials handoffs, what leaves CIS, and retention. Ben runs the call
- **Ian's section:** the virtual private network (VPN), the change approval board, and migration exports
- **Counts:** a separate section that Ben reads aloud. The same list goes out in writing as the counts request sheet

Every question has been checked against the transcripts, so nothing below repeats something the client already answered. Where they did answer, the question is a read-back.

## How this guide works across sessions

- Every question carries a permanent ID: `A-nn` for process, `B-nn` for architecture and data. IDs never renumber. A question that is not reached keeps its ID in the next guide
- **Carried items keep their ID** even when the wording changes. Today that covers B-03, B-15, B-16, B-18, B-21, B-22, B-23, A-04, A-18 and A-27
- **New IDs this session run from B-37 to B-61.** No new A-IDs, because Avi is out
- **Origin** says where the question first came up. `Jul-25` is the 2025-07-29 reverse demo, `S1` is 2026-09-15, `S2` is 2026-09-17, `Oracle-tour` is 2026-09-21, `AWS-21` is the Amazon product and SOW alignment research of 2026-09-21, `S3` is 2026-09-22, `S4` is the 2026-09-24 clinical trials session, `AWS-24` is the 2026-09-24 AWS GovCloud call, and `S5` is new for this session
- **Labels:** `Verified` means a transcript, the Oracle metadata or official documentation says it. `Inferred` means reasoned from those, not stated. `Unverified` means nobody has said it
- **Status** is blank before the session. After the call, record it against the session 5 transcript for each ID listed in the [run of show](#run-of-show), as `Answered`, `Partial`, `Not reached`, or `Moved to email`

**Audience:** internal Kicksaw. Ben Bolding, Ian Devlin and Sarah Tirey. Not a client deliverable.

Built 2026-09-29 against the session 1 to 3 transcripts, the 2026-09-24 clinical trials and AWS transcripts in Notion, the 2025-07-29 reverse demo, the Oracle metadata pull of 2026-09-23, the session 3 guide, the Enhanced Chat research, the SMS reminders options document, the voice and Amazon Connect gaps document, and official AWS and Salesforce documentation.

---

## Session details

- **Date and time:** Tuesday 2026-09-29, 2:00 to 3:00 PM ET. 60 minutes. Microsoft Teams
- **Organizer:** Mike Griffin, who is out all week. Nobody from Fred Hutch is running the room
- **Kicksaw:** Ben Bolding (runs the call), Ian Devlin (his section), Sarah Tirey (introduced as the new Kicksaw project manager)
- **CIS:** Adrianna Gutierrez, Mark Hubers, Jennifer Macabeo, Holly Fernandez-Johnson, Ray Quijano, Reetu Ghumman
- **Partners:** Ken Daugherty and Binu Pazhoor (AWS), Mitchell Rabin (Salesforce)
- **Not invited:** Suchi Panda, Jason Shamp and John Soltys, the Fred Hutch cloud and security people. Anything that needs them becomes a "who should we work with" question, not a design question

## Run of show

The list is long on purpose. When time runs short, move the items in the last column to the follow-up email. Never cut B-43 (Pinpoint), because it has a deadline.

| # | Block | Lead | Minutes | IDs | Move to email if short |
| --- | --- | --- | --- | --- | --- |
| 1 | Open, introductions, Sarah Tirey as project manager | Ben | 4 | | |
| 2 | Chat | Ben | 5 | B-23, B-37, B-38 | B-38 |
| 3 | Email | Ben | 6 | B-22, B-39 to B-42 | B-42 |
| 4 | Text reminders | Ben | 6 | B-43 to B-47, A-26 | B-45, B-46 |
| 5 | Phone | Ben | 6 | B-48, A-04, B-49, B-50 | B-50 |
| 6 | Clinical trials routing | Ben | 3 | A-18 | |
| 7 | Review before sending | Ben | 4 | B-51, B-52 | B-52 |
| 8 | Clinical trials handoffs | Ben | 5 | B-53 to B-55 | B-55 |
| 9 | What leaves CIS | Ben | 6 | B-56, B-57, A-27, B-58 | A-27, B-58 |
| 10 | Retention | Ben | 3 | B-15, B-16, B-59 | B-59 |
| 11 | Counts | Ben | 3 | B-18, B-60 | Whole block (it goes in writing anyway) |
| 12 | Ian's section | Ian | 5 | B-21, B-03, B-61 | B-03 |
| 13 | Close: what we send today | Ben, Sarah | 4 | | |
| | **Total** | | **60** | | |

---

## Ben's section

### Chat

**On record**

- Website chat moves to Salesforce Enhanced Chat, in the Salesforce console next to calls and email. Decided 2026-09-28, closing the chat entry question carried three sessions (B-23)
- Today's chat: separate English and Spanish pages, one required topic choice (clinical trials, cancer information, quitting smoking), Monday to Friday, 9 a.m. to 9 p.m. Eastern. Verified, [Enhanced Chat research](../salesforce/enhanced-chat-research-2026-09-28.md)
- Enhanced Chat lets anonymous visitors download a PDF transcript at the end. Outside business hours the chat button does not appear, and there is no offline form or banner. Verified, same document
- The pages stay at livehelp.cancer.gov and livehelp-es.cancer.gov, hosted by NCI with Salesforce's chat code. The NCI web team is not in the room. Verified, same document

**Why it matters.** The NCI web team has to publish the new pages, and that is lead time nobody has scoped. The after-hours question decides whether we need custom work, since Enhanced Chat shows nothing after hours.

**Read-back (B-23)**

> Chat has two pages, English and Spanish. The chatter picks clinical trials, cancer information or quitting smoking. Hours are Monday to Friday, 9 a.m. to 9 p.m. Eastern. Chat moves to Salesforce, in the same screen as calls and email.

**B-37. Transcript download** (S5)

> Do you want chatters to be able to download a transcript at the end?

**B-23. The NCI web team** (S2, carried)

> The National Cancer Institute (NCI) would host two simple pages at the same livehelp addresses with our chat code and today's notices. Who on the NCI web team do we work with, and who controls those addresses?

**B-38. Outside hours** (S5)

> What does a visitor see today outside hours or when nobody is available?

### Email

**On record**

- Two NIH inboxes, English and Spanish, auto-forward into Oracle. NIH authorized Oracle to send replies on behalf of nih.gov. Mark asked for the Salesforce equivalent so the forward can be repointed. Verified, session 2, Mark 39:05, 39:45, 42:29
- Oracle has five mailboxes: NCI, NCI Español, NCI Mobile, NCI Móvil Español and Bouncebacks. Verified, Oracle metadata 2026-09-23
- "The email address listed on their website is NCIinfo, which is our normal inbox." Verified, Mark, S4, 36:06
- CCR referrals are forwarded from the individual specialist's account, so nurses' replies reach one person who may be on vacation. Holly wants them sent from the general email instead. Verified, Holly, S4, 12:01 to 12:54
- Oracle also has email queues for NIDCD and POS, plus CCR English and Spanish. Verified that they exist. "POS phone calls, we don't do anymore, I don't think." Mark, Oracle-tour, 13:22. Whether NIDCD is live is Unverified
- Amazon Connect has no email channel in AWS GovCloud, so Email-to-Case is the only path. Verified in the session 3 guide (B-22). Do not volunteer the GovCloud limit

**Why it matters.** Every mailbox needs a forwarding rule, a verified sending address and a Reply-To in Salesforce. Somebody at NIH has to set up forwarding and validate the addresses, and nobody knows who that is yet.

**Statement (B-22)**

> Email comes into Salesforce as cases. The two National Institutes of Health (NIH) inboxes keep forwarding, to Salesforce instead of Oracle, and replies still go out as nih.gov.

**B-39. The five mailboxes** (S5)

> For each of Oracle's five mailboxes (NCI, NCI Español, NCI Mobile, NCI Móvil Español and Bouncebacks):
>
> 1. What is the public NIH address that forwards into it?
> 2. What From and Reply-To address do clients see on your replies?
> 3. Which are still in use?

**B-40. Forwarding at NIH** (S5)

> Who at NIH set up the forwarding, or is able to set up forwarding and validate those email addresses?

**B-41. CCR forwards from the shared inbox** (S4)

> Confirming what you told us: Center for Cancer Research (CCR) forwards should go out from the shared inbox, so the nurses' replies come back to the team. Is NCIinfo the right sending address for those?

**B-42. Other email queues** (Oracle-tour, feeds B-24)

> Oracle also has email queues for the National Institute on Deafness and Other Communication Disorders (NIDCD) and one labeled POS. Are those still in use?

POS is not spelled out on purpose. Nothing on record defines it, so ask what it stands for if they keep it.

### Text reminders

**On record**

- Pinpoint reads a callback report from Oracle, texts opted-in clients 24 hours and 1 hour before a scheduled callback, and writes delivery status back to Oracle. Replies get an automated "call us." Verified, S3, Adrianna 43:56 to 44:01, Mark 44:32 and 45:52, Adrianna 45:16
- Timing is decided: 24 hours and 1 hour before. Decided 2026-09-28
- "A few other follow up reminders" exist beyond the two texts. Verified, S1, Mark 50:10 to 50:33. What they are is Unverified
- **AWS ends Amazon Pinpoint support on 2026-10-30.** Campaigns, journeys, segments and analytics retire. The SMS sending API continues under AWS End User Messaging. Verified, [AWS Pinpoint end of support](https://docs.aws.amazon.com/pinpoint/latest/userguide/migrate.html)
- Not on record anywhere: who built the integration, whether it uses campaigns or a direct send, the sending number, monthly volume. Unverified. See the [SMS reminders options](../salesforce/sms-reminders-options-2026-09-22.md)

**Why it matters.** If today's setup uses Pinpoint campaigns or journeys, the reminders stop on 2026-10-30, three months before go-live. That makes B-43 the one item on this call with a hard external deadline.

**Read-back**

> Texts go to clients who agreed to texts and are enrolled in callbacks. They go 24 hours before and 1 hour before the call, with standard wording and no personal details. Replies get an automatic "please call us," and delivery status is written back to Oracle.

**B-43. Pinpoint, urgent** (S5)

> Amazon Web Services (AWS) ends support for parts of Amazon Pinpoint on October 30. Does your reminder setup use Pinpoint campaigns or journeys, or does it send each text directly? Who at Fred Hutch or AWS built it and can check?

**B-44. Sending number** (S5)

> Which phone number sends the texts, and does it need to stay the same number?

**B-45. Other follow-up reminders** (S1)

> Mark mentioned "a few other follow-up reminders" besides the two texts before a callback. What are those?

**B-46. Write-back and replies** (S3)

> Besides delivery status, what gets written back to Oracle, and where do staff see a client's reply?

**B-47. Clinical trials callbacks** (S4)

> Do clinical trials callbacks get texts too, or only Veterans Affairs (VA) and smoking cessation callbacks?

**Written asks:** the message text in English and Spanish (A-26, carried). Monthly volume goes on the counts sheet.

### Phone

**On record**

- Four lines: 1-800-4-CANCER, the smoking quitline, the VA quitline and the CCR line. Language first, then 1-800-4-CANCER offers cancer information, clinical trials and quitting smoking. Verified, [system landscape](../archive/2026-09/system-landscape-2026-09-12.md) from the July 2025 demo
- Entry points do not change (D18). Numbers stay the same
- Oracle lists eight service numbers: 4CANCER, 44U QUIT, QUIT NOW, VA Quit Smoking, **PIQ**, Proact Study Number, **NIDCD** and CCR. Verified, Oracle metadata 2026-09-23. "I think we'll probably keep PIQ, but I don't know if we need these other ones, but we do need CCR." Verified, Mark, Oracle-tour, 12:10
- Numbers can stay with Verizon and be repointed to Amazon Connect, instead of porting. Verified 2026-09-28 against AWS Prescriptive Guidance, "NGN backend repointing." Unverified: that Fred Hutch's Verizon service can be repointed, and that the caller's number arrives intact
- If numbers stay with Verizon and callbacks need to show 1-800-4-CANCER, AWS needs a Support case with proof of ownership for custom caller ID. Verified, [AWS: Set up outbound caller ID](https://docs.aws.amazon.com/connect/latest/adminguide/queues-callerid.html). Whether custom caller ID is offered in GovCloud is Unverified. The caller ID question itself goes to email

**Why it matters.** Who holds each number decides who signs anything with Verizon, and it sets the cutover plan and the fallback on cutover day.

**Read-back**

> There are four lines, 1-800-4-CANCER, the smoking quitline, the Veterans Affairs (VA) quitline and the Center for Cancer Research (CCR) line. Each asks English or Spanish first, and 1-800-4-CANCER then offers cancer information, clinical trials and quitting smoking. Hours are Monday to Friday, 9 a.m. to 9 p.m. Eastern. The numbers stay the same.

**B-48. The public inquiries line** (Oracle-tour, feeds B-24)

> Oracle also lists a public inquiries (PIQ) line. Is that still in use?

**A-04. Every number that rings in** (S1, carried; written ask)

> Could you send the full list of numbers that ring in today, including unpublished ones, and where each one goes?

**B-49. Repoint or move** (S5)

> After go-live, the numbers can either stay with Verizon and be repointed to the new system, or move to Amazon. Repointing keeps the numbers where they are and makes it easy to switch back on cutover day.
>
> 1. Who holds each number with Verizon, Fred Hutch or the National Cancer Institute (NCI)?
> 2. Could that person ask Verizon whether your toll-free service can be repointed to a number we provide?
> 3. Does the Verizon contract continue past go-live?

**B-50. What callers hear** (S5)

> What do callers hear when you're closed, on a holiday, or while they wait? Could you send the scripts or recordings?

### Clinical trials routing

**On record**

- Today, skill groups are hierarchical: everyone takes cancer, some add tobacco, then clinical trials, then Spanish. Verified, S2, Holly 31:32
- "Our ideal would be kind of starting out bare bones, no reserving agents, basically just first in, first helped." Spanish still needs a skill distinction. Verified, S2, Holly 36:21 and 38:26
- Oracle profiles carry "clinical trials chat eligibility." Verified, Oracle-tour, 25:13
- **The session 3 guide over-read session 2.** The guide closed A-18, and the session 3 client agenda told the client "Language is the only skill split at launch." Session 2 said no reserved agents, which is not the same as dropping the clinical trials skill. Recorded 2026-09-28. A-18 is reopened here, and the question also corrects what the session 3 agenda told them

**Why it matters.** It decides whether the routing has two skills (language and clinical trials) or one. It also decides whether a Spanish clinical trials call waits for the few people who have both.

**A-18. Clinical trials skill at go-live** (S1, reopened)

> Today, clinical trials calls go only to specialists skilled for clinical trials, and Spanish calls only to specialists who speak Spanish. When we go live, should clinical trials calls and chats still go only to specialists skilled for clinical trials? That would mean a Spanish clinical trials call goes to someone who is skilled for clinical trials and also speaks Spanish. Or should any specialist who speaks the caller's language take them? On session 2 you said you want to start without reserving agents, and we want to make sure that doesn't mean dropping the clinical trials skill.

### Review before sending

**On record**

| Email type | Review rule heard | Source | Label |
| --- | --- | --- | --- |
| All email | "All of our emails do go through a review and kind of approval process" | Mark, S2, 51:19 | Verified |
| General cancer | Reviewed only for new specialists, for a period after training | Holly, S3, 17:22 | Verified. Holly was describing follow-ups after a call |
| Clinical trials | Always reviewed, by the supervisors who cover clinical trials | Holly, S3, 19:23. Mark and Holly, S4, 27:42 to 28:09 | Verified |
| Public inquiries (PIQ) | Never stated. Oracle has a PIQ Review queue | Holly, S4, 56:52. Oracle metadata | Inferred that it is reviewed |
| Smoking | Never stated. Rare, and Oracle has no smoking email queue | Holly, S2, 46:42. Mark, S2, 46:50 | Inferred that it follows general cancer |

Oracle has four review queues: English Review, Spanish Review, CT Review and PIQ Review. Verified that they exist.

**Why it matters.** It decides whether the "can't send until reviewed" gate applies to every email case or only on conditions (type, or a new specialist). The session 2 summary recorded "email review before send stays mandatory" (row 8), which needs scoping by type after the call.

**B-51. Review by email type** (S2)

> We've heard review described two ways: that every email goes to a supervisor before it sends, and that only some do. Here's what we have. Please confirm or correct each one:
>
> - General cancer: reviewed only for new specialists, for a period after training
> - Clinical trials: always reviewed, by the supervisors who cover clinical trials
> - Public inquiries (PIQ): Oracle has a PIQ Review queue, so we assume always reviewed
> - Smoking: rare, and we assume it follows the general cancer rule

Only if they say "it depends": is it different for a reply to an email that came in versus a follow-up after a call?

**B-52. The new specialist period** (S3)

> For new specialists, how long does the review period last, and who decides when it ends?

### Clinical trials handoffs

**On record**

- The searcher assigns the whole inquiry to themselves, and so does the reviewing supervisor. Someone has to assign it back "so that when we pull all of our data for the month, we know who took that original call," and people often forget. Verified, Holly, S4, 39:59 and 46:15
- Holly: "can we have a way to just assign the search to someone? Just like, yeah, who did the review?... that would be lovely." And "we'd be very interested in something like that." Verified, S4, 49:00 and 51:03
- Oracle already has a **CT Searcher** field, a pick list of 57 names described as "The person who conducted the CT search," and a **Lead** field. There is no reviewer field. Verified, Oracle metadata 2026-09-23. Whether CT Searcher is filled in today is Unverified
- Steps on a clinical trials inquiry: take the call and fill in the clinical trials details, consult a lead, forward to CCR, run the search (status "CT Search"), review (status "Review"), send the follow-up. Verified, S4, 22:15, 28:09, 39:59, 46:15, and S3, 16:18

**Not decided.** Avi floated "an inquiry team with roles" as a possibility only: "I'm not trying to, like, design a solution" (S4, 50:24 to 50:53). No design is chosen. How to record roles belongs in the design document.

**Why it matters.** Today's reassigning breaks monthly credit and loses inquiries. Migration also inherits the problem: where someone forgot to assign an inquiry back, the historical Assigned field names the searcher or reviewer. Inferred.

**B-53. The requirement** (S4)

> On the 24th you told us a clinical trials inquiry gets reassigned each time someone searches or reviews it. Someone has to remember to assign it back so the monthly numbers credit the person who took the call. You said you'd like a way to record who did the search and who did the review without passing the inquiry around. We're treating that as a requirement for the new system. Is that right?

**B-54. The CT Searcher field** (S5)

> Oracle already has a "CT Searcher" (clinical trials searcher) field. Do specialists fill it in today?

**B-55. Steps and reporting** (S5)

> Here are the steps we heard on a clinical trials inquiry:
>
> - taking the call
> - forwarding to the Center for Cancer Research (CCR)
> - the search
> - the review
> - the follow-up email
>
> 1. Do you need to know who did each step?
> 2. If so, what do you need to report on it? For example, how many of each step a person did in a month, or how long an inquiry waits at each step?

**Written ask (optional):** the monthly report used today to credit specialists. It travels with A-27.

### What leaves CIS

**On record**

- "We submit... regular deliverables to the government where they get all of our monthly data." Verified, Adrianna, S2, 11:12. "The government does have a monthly summary for the last number of years of our data in Excel spreadsheets." Verified, Mark, S2, 12:15
- The VA wants callback data: answer rates, effort until contact, callbacks per client, total work. Verified, Adrianna, S3, 55:07
- CCR gets a report by email. Verified, Mark, Oracle-tour, 10:00
- Tableau is fed by manual exports: "export the phone data and export the RightNow data... and then put them each into Tableau," joined on phone number or the RightNow ID. Verified, Adrianna, S2, 9:05, and July 2025, 83:51. Tableau stays and is out of scope
- Oracle has no event subscriptions, and two API profiles: "SOAP API" and "Copy of SOAP API." Verified, Oracle metadata. Which accounts use them is Unverified. The Oracle pull deliberately excluded staff records ("profiles only, no staff records"), so this goes to Mark rather than a query
- About 1,700 report names and 198 full definitions came back in the 2026-09-23 pull. Deliverable-like names: VA Yearly Report, VA Report, three VA Study Reports, VA Follow-up at 4, 7 and 13 months, VA Demographics Results, CCR Weekly Report, and a monthly clinical trials study data export. Verified that they exist, Unverified that they are used. **The list stays local.** It sits under `extracts/` and some names include staff names
- Session 2 said Kicksaw's access would exclude reports and CIS would export the definitions (Mark, 6:14 to 6:45). The API returned the definitions anyway, with no data. A-27 is reframed to "which reports do you use"

**Why it matters.** These are contract obligations that must work in the first month after go-live. The go-live month is split across Oracle and Salesforce, because session 2 decided to start fresh on interaction data. Inferred. An unknown system writing to Oracle breaks silently at cutover.

**Read-back**

> Each month you send data to the government, and the government keeps a monthly summary going back years in Excel. The VA wants callback data: how often people answer, how much effort it takes to reach them, and how many callbacks each person gets. The Center for Cancer Research (CCR) gets a report by email.
>
> Tableau stays. Your exports will come from Salesforce and Amazon Connect instead of Oracle and Cisco, and the Salesforce case number replaces the RightNow ID as the link.

**B-56. The monthly deliverables** (S2)

> Can you walk us through what goes out in a normal month? For each one:
>
> - what's in it
> - who receives it
> - what format
> - who sends it

**Written ask:** one example of each monthly deliverable, with personal details removed.

**B-57. Other systems and the API accounts** (S5, ask Mark)

> Besides the text reminders, does any other system read from or write to Oracle? Oracle has two application programming interface (API) profiles, "SOAP API" and "Copy of SOAP API." Which accounts use them, and what system is behind each one?

**A-27. Which reports you use** (S3, carried, reframed)

> On session 2 you offered to export your report definitions. We can now read the report list ourselves, so we only need to know which reports you run in a normal month. Those get rebuilt first.

**B-58. The go-live month** (S5)

> The month we go live, part of the data will be in Oracle and part in Salesforce. Who puts that month's deliverable together?

### Retention

**On record**

| Point | Source | Label |
| --- | --- | --- |
| "A government requirement to scrub... the PII every 13 months" | Mark, Jul-25, 39:20 | Verified |
| "Every 13 months on the workspace, it hides the contact tab... and it gets rid of the message tab" | Adrianna, Jul-25, 39:56 | Verified |
| "We keep the contact information for about 15 months. And then it gets scrubbed" | Adrianna, S1, 8:20 | Verified |
| "All the contact records get deleted. Every 15 months per our government requirement," including chat transcripts | Adrianna, S1, 11:24 and 12:02 | Verified |
| VA follow-up survey calls at 4, 7 and 13 months. Oracle has a "VA Follow-up: 13 mos" report | Holly, S3, 28:16. Oracle metadata | Verified |

A 13-month scrub would erase the phone number just as the 13-month follow-up call is due, so the window may have moved to 15 months for that reason. Inferred.

**Why it matters.** Deleting means a scheduled job that removes contacts, emails and chat transcripts, including the recycle bin and field history. Hiding means masking fields and keeping the rows. The length also sets the repeat-caller window (RAID-34, repeat-caller contact pops). Retention controls are in the SOW.

**B-15 and B-16. Length, delete or hide, and where it is written** (S1, carried)

> We've heard retention described two ways. In July 2025, contact details were scrubbed every 13 months, and the contact and message tabs were hidden. On session 1, contacts were kept about 15 months and then deleted, including emails and chat transcripts.
>
> 1. Which is right: 13 or 15 months?
> 2. Is the contact deleted or hidden?
> 3. Where is the rule written? Could you send us the contract language?

**B-59. The 13-month follow-up** (S3)

> Is the 15 months there so the 13-month VA follow-up call can still reach the client?

Call recordings are left out on purpose. The question pulls in Calabrio, who are not invited. Calabrio's plan keeps audio 12 months and screen recordings 6 months (Calabrio kickoff, 2026-09-14).

---

## Counts: Ben reads these aloud

Several of these were promised on session 3. Frame the list as pulling those together, not as new homework. The same list goes out in writing as the [counts request sheet](counts-request-2026-09-29.md).

**B-60. The counts request** (S5, carries B-18)

> We'll send this list in writing today. Some of it Adrianna already offered to pull on the 22nd. Here's what we need:
>
> 1. Interactions per month for the last 12 months, by channel, by line or chat topic, and by language. For email, by type: general cancer, clinical trials, public inquiries and smoking
> 2. Callback attempts, follow-up survey calls and proactive calls per month, split by VA and clinical trials
> 3. How many callbacks and follow-up calls are scheduled in Oracle today, and how far ahead the latest one is booked
> 4. Text reminders sent per month
> 5. Active users on each Oracle profile
> 6. Headcount by role
> 7. Knowledge articles by language, and how many are public versus internal only
>
> Who's the right person for each, and when is realistic?

| Count | Already promised? |
| --- | --- |
| 1. Interactions per month | Yes. Adrianna, S3 open question 1. It settles "35,000 a year" versus "25 to 40 a day" |
| 2. Outbound calls per month | Yes. Adrianna took it away, S3, 41:57 |
| 3. Scheduled callbacks and follow-ups | Carried as B-18. The follow-up calls are new: they are booked up to 13 months ahead and have to migrate |
| 4. Text reminders | New today (B-43 block) |
| 5. Active users per profile | New. Oracle has 40 profiles (metadata). Kicksaw does not pull staff records |
| 6. Headcount by role | New |
| 7. Knowledge articles | New. The SOW says about 5,000 in English and Spanish |

---

## Ian's section

### VPN

**On record**

- "We have to use the Fred Hutch VPN network and we are on a special subnet for the traffic to flow." Verified, Jennifer, Jul-25, 46:01. Specialists are almost all remote
- Whether all traffic goes through the VPN or only Fred Hutch traffic: Unverified. Carried as B-21 since session 2
- Softphone audio needs UDP port 3478 to the `us-gov-west-1` media endpoint and port 443 to the Amazon Connect domains. AWS warns remote-agent audio issues are "compounded if a VPN is required." Verified, [AWS: Set up your network for the CCP](https://docs.aws.amazon.com/connect/latest/adminguide/ccp-networking.html)

**Why it matters.** The network team owns the answer and is not in the room. This question finds the person.

**B-21. Who to work with** (S2, carried, reworded)

> Specialists work from home on the Fred Hutch virtual private network (VPN). Who on your team should we work with to make sure the VPN is set up to let the new system's call traffic through?

### Change approval board

**On record**

- Thursdays 2 to 3 "is our IT CAB change approval board." Verified, Mike, S1, 1:01:46
- Whether it governs Salesforce and Amazon Connect: Unverified. Carried as B-03 since session 2
- Ben's working rule since 2026-09-24: configuring the empty production org needs no client approval. Scoped to after go-live on purpose, so the question does not invite a process into the build

**B-03. After go-live** (S2, carried, rescoped)

> Mike mentioned the Fred Hutch IT change approval board meets Thursdays. After go-live, do changes to Salesforce and Amazon Connect go through it? If so, how far ahead does a change need to be submitted?

### Migration exports

**On record**

- "I think we're going to start fresh." Verified, Adrianna, S2, 11:12. Exceptions: "Knowledge base and potentially the callback tasks depending on what that looks like," and "some things that we have to continue workflow on." Verified, Mark 11:57, Adrianna 12:03
- Kicksaw has no access to Oracle production. The test copy is two to three months old. Verified, project brief and Mark, Oracle-tour, 29:02
- **VA follow-up survey calls are booked at 4, 7 and 13 months.** A client enrolled in December has calls due into early 2028, so those tasks and their phone numbers have to move. That means some contact details migrate despite "start fresh." Inferred, from Holly, S3, 28:16

**B-61. Who exports, in what format, and what counts as in progress** (S2)

> On session 2 you decided to start fresh, except for:
>
> - the knowledge base
> - callbacks already scheduled
> - work still in progress at cutover
>
> 1. Who at CIS can run the exports from Oracle production?
> 2. What format can you export in?
> 3. What counts as work in progress at cutover? For example: open inquiries, scheduled callbacks, and the VA follow-up calls already booked months ahead.

---

## Decided since session 3

| Date | Decision | Effect on this guide |
| --- | --- | --- |
| 2026-09-28 | Website chat moves to Salesforce Enhanced Chat | Closes the B-23 architecture question. B-23 keeps its NCI web team half |
| 2026-09-28 | Text reminders go 24 hours and 1 hour before the callback | Read-back, not a question |
| 2026-09-28 | Sarah Tirey is the Kicksaw project manager | Introduced at the open |
| 2026-09-28 | The session 3 guide over-read session 2 on routing. The clinical trials skill is open | A-18 reopened |
| 2026-09-29, Ben | Specialists go back to available by hand at launch, the same as today. An after-call timer with an extend button is a later enhancement | Not asked. Closes session 3 open question 6. A-12's averages are not pursued |
| 2026-09-29, Ben | A voicemail on a callback counts as a missed attempt | Not asked |
| 2026-09-29, Ben | The callbacks block comes off the call | Voicemail and caller ID go to email |
| 2026-09-29, Ben | The API account question goes to Mark on the call, not a query against Oracle | B-57 |

## Settled decisions, do not reopen

| Register row | Decision |
| --- | --- |
| D1, scope | Oracle Service Cloud to Salesforce Government Cloud. No standard Salesforce org migration |
| D2, Amazon Connect in AWS GovCloud | `us-gov-west-1`, partition `aws-us-gov` |
| D13, agent desktop is Salesforce | Specialists receive and control calls in Salesforce through Service Cloud Voice |
| D14, repeat-caller contact pops within the retention window | Pop the existing contact if one exists, always open a new inquiry |
| D15, universal queuing restored | Longest-waiting available, universal across voice and chat, no reserved agents. **Whether the clinical trials skill stays is open (A-18).** A correction to the register wording is proposed and pending Ben |
| D17, inquiry workspace streamlined by call type | Layouts by call type, universal coding on every type |
| D18, entry points do not change | Numbers, chat addresses and email addresses stay |
| D19, SMS callback reminders rebuilt | On AWS End User Messaging. Pinpoint campaigns and journeys retire 2026-10-30 |
| D20, scope boundaries | VA Direct stays manual, external trial search sites out of scope |
| Session 2 | Start fresh on data. The knowledge base, scheduled callbacks and in-flight work migrate |
| Oracle tour | Permissions are designed fresh, not mirrored from Oracle profiles |

---

## Follow-up email, not the call

Ben's go is needed before anything is sent.

| Item | ID or origin |
| --- | --- |
| Spam volume and reporting back to NIH | S2 |
| A sample web form submission | S4 |
| Subject 1 as the primary subject, and whether any NCI report depends on it | A-07, B-11 |
| The patient record | 2026-09-28 prep |
| Statuses nobody has explained. Oracle has three placeholder statuses named "....", "..." and ".....", which are probably the ones meant (Inferred) | 2026-09-28 prep, Oracle metadata |
| The callback calendar view | A-24 |
| Where demographics survey results go | 2026-09-28 prep |
| Live dashboards | 2026-09-28 prep |
| Chase the callback knowledge article and the "callback coding logistics" document Adrianna promised (S3, 57:23), and ask: "Do specialists ever leave a voicemail on a callback?" | S3 |
| "What number shows on the client's phone when you call back?" Ties to B-49 and AWS custom caller ID | S5 |
| The RACI (responsibility chart), the design document and the security sign-off, to the 2026-09-24 group. Ask Adrianna where the offline security conversation landed, since Mike is out | AWS-24 |

**Working session, not email:** the required-fields list (A-06).

**Backlog:** the after-call timer with an extend button.

## Carried items not on today's agenda

The items the session 3 guide scheduled for the 2026-09-24 clinical trials session have not been checked against that transcript. Their status is **not filled**, not assumed answered.

| ID | Item | Where it stands |
| --- | --- | --- |
| A-01 | Workspace rules, workspace definition, custom fields | Largely superseded by the Oracle export |
| A-02 | Full call type list | Carried |
| A-06 | Required fields before close | Working session |
| A-07, B-11 | Subject 1 as primary, and its reporting dependency | Follow-up email |
| A-08 | General cancer follow-up email | Partial. The sending mailbox now rides on B-39 |
| A-10 | A general call that turns into clinical trials or smoking | Carried |
| A-11 | Phone inquiry statuses | Partial, carried |
| A-12 | After-call work averages | Not pursued (Ben, 2026-09-29) |
| A-13 to A-17, A-19 to A-21 | Clinical trials detail, searches, callbacks, CCR | Scheduled for 2026-09-24. Status against that transcript not filled |
| A-22, A-23, A-29 | VA Direct fields, SCIF presentation, SCIF reduction | Carried |
| A-24 | Callback calendar view | Follow-up email |
| A-28 | Skill list and AUX code list | Carried. Still owed by Holly and Jennifer |
| A-31 | Most complex call type | Partial, carried |
| B-02 | Administration boundary | Carried |
| B-08, B-09, B-10 | Escalation, crisis calls, whisper and barge | Carried. **B-09 (crisis escalation) has now gone four sessions without an answer** |
| B-12 | Caller identity values | Answerable from the Oracle export |
| B-14 | Where SMS consent lives | Carried. Consent has to survive the retention scrub while callbacks are scheduled |
| B-24 | Queue, number and rule cleanup | Partly today through B-42 and B-48 |
| B-25, B-32 | What the VA needs from the SCIF, intent behind consultant rules | Carried |
| B-26, B-27, B-35 | Oracle logistics for Mark | Not for the call |
| B-28, B-29, B-30 | AWS transcription, FIPS endpoints, region selection | Not for the call. Kicksaw to AWS |
| B-33 | NCI's position on historical data | Carried |
| B-34 | Capability read-back for profiles | Carried |
| B-36 | The 60-license basis | Not for the call |

---

## Before 2:00 PM

| # | Item | Owner |
| --- | --- | --- |
| 1 | Review the [client agenda](discovery-session-5-agenda-2026-09-29.md) and decide whether it goes to the client | Ben Bolding |
| 2 | Optional, not on the call: ask Mitchell Rabin whether Salesforce's voicemail for Service Cloud Voice has a Government Cloud path. The client hasn't asked for voicemail, so it isn't raised with them | Ben Bolding |
| 3 | Keep B-28, B-29 and B-30 off the call even though AWS attends. Same reasoning as session 3 | Ben Bolding |

## After the call

- Record status for each ID in the run of show, against the session 5 transcript
- Send the counts request sheet and the follow-up email, on Ben's go
- Propose RAID rows, not apply them: the clinical trials role-tracking requirement (B-53) with the design left open; the D15 correction; the scoping of session 2 row 8 (email review) by type; the voicemail rule
- Still pending Ben's go from 2026-09-28: add Verizon repointing to the voice and Amazon Connect gaps document and the RACI phone numbers row; move RAID-13 and RAID-15 to Sarah Tirey and add a note on RAID-28
- If the transcript goes to Notion, push only the verbatim section. It is a client call, so it qualifies

---

## Change log

- **2026-09-29, revision 2.** Removed the ID index; status is recorded against the IDs in the run of show. Dropped the Teams link check (everyone has it). The Mitchell Rabin voicemail question is optional and stays off the call, since the client hasn't asked for voicemail. The client agenda goes out only after Ben reviews it. Published to the Project Library with the client agenda and the counts request
- **2026-09-29, revision 1.** Created as the session 5 guide, with Ian Devlin's section in place of Avi's. Walked every question against the transcripts with Ben. Added B-37 to B-61. Reopened A-18 (clinical trials skill). Reworded B-21 (VPN) to finding the right contact, and scoped B-03 (change approval board) to after go-live. Reframed A-27 now that the report list is readable through the API. Cut the callbacks block and moved voicemail and caller ID to email. Dropped the after-call work question by Ben's decision. Moved counts to their own read-aloud section

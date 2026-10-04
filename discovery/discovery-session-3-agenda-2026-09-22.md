# Discovery session 3: how each call type works today

**Tuesday, September 22, 2026, 2:00 to 3:00 PM ET**
Prepared by Kicksaw for the Fred Hutch NCI Cancer Information Service (CIS) team

## What we want to leave with today

A clear picture of how a specialist handles each call type from start to finish, so we can design the Salesforce inquiry around the way the team works. Holly is walking us through each one live in Oracle.

We'll cover three call types in this order, then leave time for anything that doesn't fit:

1. General cancer
2. Clinical trials, including CCR and the trial search handoff
3. Smoking cessation, including VA
4. Anything else

The VA callback series, VA referrals, and SMS reminders get their own session, so we'll skip them today.

## The four questions for each call type

1. What does the specialist capture, and at what point in the conversation?
2. Which codes are required, and which ones exist only to trigger something or feed a report?
3. What changes depending on whether it's a call, a chat, or an email?
4. How does it end: status, follow-up, callbacks, and any survey?

## What we've heard so far

We've pulled these from earlier sessions so we can confirm them rather than ask again. The source is in parentheses.

**Across all call types**

- Every interaction creates an inquiry. Contact details come first, then notes, then coding after the conversation ends. (Session 1)
- Every call gets the same general coding section. Then there's a section specific to the call type: smoking cessation for smoking calls, clinical trials for clinical trials and CCR calls. (Oracle walkthrough, September 21)
- Callers can stay anonymous. Contact details are collected only when the caller wants an email follow-up or a callback. (July 2025 demo)
- Calls can run up to an hour. The team focuses on quality of service, not speed. (Session 2)

**What's decided for the new system**

- Calls and chats go to the specialist who's been waiting longest. Language is the only skill split at launch, and no specialists are held back for low-volume queues. (Session 2)
- Email comes in through Salesforce. The two NIH inboxes forward into Salesforce the same way they forward into Oracle today, and replies still go out on behalf of nih.gov. (Session 2)
- Historical coding and phone data stay in Oracle. The knowledge base, scheduled callbacks, and any work that's still open at cutover move to Salesforce. (Session 2)
- Permissions are designed fresh in Salesforce rather than copied from the Oracle profiles, covering the same abilities. (Oracle walkthrough, September 21)

## General cancer

**What we've heard**

- Subject 1 through 4 hold the cancer topics, with Subject 1 as the primary topic. There are four fields because Oracle doesn't support selecting more than one value in a field. (July 2025 demo, Session 1)
- Standard text holds templated responses with F9 shortcuts. It's separate from the knowledge base. (Session 1)
- Every outgoing email is reviewed before it's sent. Reviewers want to be able to edit a draft and see who changed what. (Session 2)

**What we'd like to confirm**

- Walk us through one call from answer to close.
- Which fields must be filled before an inquiry can close?
- How do specialists choose Subject 1 through 4 on a live call? Does any NCI report depend on which subject is primary?
- When does a general call need an email follow-up, and what goes out?
- If the caller stays anonymous, what's the minimum captured?
- If a general call turns into a clinical trials or smoking question, does the specialist start a new inquiry or change the existing one?
- Which statuses does a phone inquiry move through? We covered email statuses in session 2.
- About how much time goes to work after the call ends?

## Clinical trials, including CCR

**What we've heard**

- Clinical trials coding is similar to general cancer, with more detail. CCR calls add more fields. (Session 1)
- A CCR inquiry comes from the dedicated CCR phone number or the CCR website email form. (Session 1)
- CCR receives a regular emailed report built in Oracle. (Oracle walkthrough, September 21)
- A trial search can lead to up to two follow-up callbacks. (Session 1)
- When an email needs a trial search, it goes to a specialist for the search, then comes back. Anyone can reply because the history stays on the inquiry. (Session 2)

**What we'd like to confirm**

- What does the specialist capture beyond a general cancer call, such as diagnosis, stage, location, or travel limits? What more for CCR?
- Which outside sites do specialists search, and what comes back into the inquiry?
- How do search results reach the caller: email, phone, or both?
- What triggers each of the two callbacks, and when is a callback considered done?
- If a general clinical trials call becomes a CCR conversation, what changes on the inquiry?
- Does the CCR report need to be rebuilt as it is today, or would a scheduled Salesforce report to the same people work?
- Do clinical trials inquiries follow the same statuses and review steps as general cancer?

## Smoking cessation, including VA

**What we've heard**

- The Smoking Cessation Intake Form (SCIF) is a guide, not a script. It's added to the inquiry from the smoking cessation tab. (July 2025 demo, Oracle walkthrough)
- The SCIF exists mainly for the VA quit smoking program, and Mark suggested it could be simplified. (Oracle walkthrough, September 21)
- Tobacco calls are part of the 25 percent demographic survey. VA calls are surveyed at 100 percent, except for anyone surveyed in the last 90 days. (Session 2)

**What we'd like to confirm**

- What does the specialist capture on a first smoking cessation call?
- Should the SCIF work as a guided step-by-step screen, or as a set of fields filled in any order?
- Which SCIF fields does the VA actually use? We'd like to know that before we suggest removing any.

## Anything else

- **Getting help on a difficult call.** When a caller is in distress, how does a specialist get a supervisor's attention, and what does the supervisor do?
- **Website chat.** Where does the Live Help button on cancer.gov point after launch, and who on the NCI web team makes that change?
- **Queues, service numbers, and rules to retire.** Oracle has queues, service numbers, and rules that are no longer used, built up over 14 years. Adrianna and Holly are best placed to decide what carries over. Could we schedule a working session to go through the list together?

## Items we're still waiting on

| Item | Who | Requested |
| --- | --- | --- |
| Full list of call types | Adrianna, Jennifer | Session 1 |
| Current list of inbound numbers and IVR menus | Mark | Session 1 |
| Report definitions export from Oracle | Adrianna, Mark | Session 2 |
| Skill list with coding, and the current AUX code list | Holly, Jennifer | Session 2 |
| Surveys access for the Kicksaw Oracle account | Mark | Oracle walkthrough |

## Coming up

- **Thursday, September 24:** knowledge base session with Melissa
- **To schedule:** VA callbacks, VA referrals, and SMS reminders

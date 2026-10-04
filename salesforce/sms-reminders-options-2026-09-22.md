# SMS callback reminders: what exists today and two ways to rebuild it

Options note for the callback reminder texts that Amazon Pinpoint sends today from Oracle Service Cloud. It records what the client has, two candidate rebuild patterns with level of effort, what the executed SOW says about each, the evidence behind each, and the questions still open.

**Audience:** internal Kicksaw. Ben Bolding, Avi Rabinovitch, Ian Devlin, Hannah Oanca. Not a client deliverable and not pushed anywhere. The question list in the section "Questions to close before sizing" is written client-safe so it can move into a session guide.

Built 2026-09-22 from the 2025-07-29 reverse demo, discovery sessions 1 and 3, the executed SOW (July 20, 2026 version in Drive), AWS and Salesforce documentation fetched the same day, and two queries against the Government Cloud org.

---

## Summary

- Today, Pinpoint reads a callback report from Oracle, texts opted-in clients 24 hours and 1 hour before a scheduled callback, and writes delivery status back to Oracle. Replies get an automated "call us." It is one-way notification texting with a status write-back, not two-way conversation.
- AWS ends Amazon Pinpoint support on 2026-10-30. Campaigns, journeys, segments, endpoints, and analytics retire. The SMS, voice, push, and OTP APIs continue under AWS End User Messaging.
- Two patterns are viable in Government Cloud. Option 2, Salesforce to the End User Messaging SMS API in AWS GovCloud, is the closest match to what the client described on the calls and sizes M to L. Option 1, native Salesforce Digital Engagement, is what the SOW assumes for SMS and sizes S to M. Amazon Connect SMS and Bring Your Own Channel are unavailable in Government Cloud and are ruled out.
- The executed SOW lists "SMS/Text Reminders" for callback participants as a functional requirement and assumes SMS runs on Digital Engagement. It does not name Pinpoint or an AWS integration. How the two options sit against the SOW is recorded in the section "What the SOW says" and is a conversation to have, not a conclusion.
- Apart from reminder timing (24 hours and 1 hour before, decided 2026-09-28), nothing is decided or approved. The client has not said whether it wants the reminders rebuilt, kept as they are, or dropped. Kicksaw takes no position on that choice.
- Mike Griffin decides scope. Mark Hubers and Adrianna Gutierrez own the current-state answers. Ken Daugherty and Binu Pazhoor own the AWS answers.

## Status

This note exists so Kicksaw has an answer ready if the client asks what a rebuild involves. It is not a design and no build is committed. The two options are sized so either can be written up for the client in a day if asked. Where the client's own preference matters, this note records what the client said and stops there.

## What the client has today

Every line here comes from a client call. Nothing is inferred.

| Fact | Source |
| --- | --- |
| Oracle holds callback tasks scheduled "months, years in advance." An integration between Oracle and "Pinpoint AWS" sends "those SMS messages proactively out to those people that have opted in for those reminder messages." Mark Hubers: "that's another integration that we would like to keep" | 2025-07-29 reverse demo, Mark Hubers, 27:50 to 28:38 |
| "For those that agree to it, we do send them SMS reminders. And that is currently done through an AWS solution. Part of that solution is being retired... We will want to kind of recreate the SMS. It's a very simple process, and it just sends a text reminder. 24 hours in advance and like 2 hours in advance, I think. And then a few other follow up reminders. No PII included, no PHI included" | Session 1, 2026-09-15, Mark Hubers, 50:10 to 50:33 |
| "That does connect to the API. And it's basically looking at each inquiry. And so if SMS consent says yes, and they are also enrolled in callbacks, yes, then it sends their information, these reports, over to Pinpoint to send the text messages." Several workspace codes exist only to trigger those reports, and Adrianna wants them gone | Session 1, Adrianna Gutierrez, 51:18 to 51:27 |
| The callback report "also gets sent to Amazon Pinpoint. And so Pinpoint knows when somebody's going to get a callback and it texts them 24 hours in advance... And then it also texts them an hour before" | Session 3, 2026-09-22, Adrianna Gutierrez, 43:56 to 44:01 |
| "There is no PII or PHI in the text. It's just standard text. We're going to call you at 9:30 AM" | Session 3, Mark Hubers, 44:32 |
| "It's also only one-way communication. So if the client wants to change their appointment, they can't text it back" | Session 3, Holly Fernandez-Johnson, 44:43 |
| "They can text back and we do see them, but they get an automated message that... you need to call if you want to talk to somebody" | Session 3, Adrianna Gutierrez, 45:16 |
| Asked whether two-way confirm or cancel is wanted: "Maybe" | Session 3, Mike Griffin, 45:50 |
| "Pinpoint does write back to Oracle. So we know whether or not an SMS message was successful or not... it's a 2-way integration with AWS" | Session 3, Mark Hubers, 45:52 |
| "They connect to the API of Oracle... and so they're getting those reports. So it's an integration" | Session 3, Adrianna Gutierrez, 46:12 |

Not on record anywhere: who built the integration, which AWS account and region it runs in, whether it uses Pinpoint campaigns or a raw SMS API call, the sender number type, monthly volume, how STOP replies are handled, and where SMS consent is stored (guide item B-14, still not reached). **Timing is decided: 24 hours and 1 hour before the callback** (Ben Bolding, 2026-09-28), matching session 3 and repeated statements since. Session 1's "like 2 hours" was a hedged recollection.

## What the SOW says

The governing document is the July 20, 2026 client-redlined SOW. Three lines in Addendum A touch this topic.

| Addendum A text | Where | What it means for this note |
| --- | --- | --- |
| "The ability to schedule call-back activities for future dates for the smoking cessation program participants as well as SMS/Text Reminders" | Functional Requirements, Telephony and Omnichannel | Reminder texts for callback participants are named in the requirements |
| "SMS support is provided by the Salesforce Omnichannel digital engagement product which must be licensed to support the omnichannel engagement requirements" | Assumptions | The SOW assumes SMS runs on Salesforce Digital Engagement, which the org licenses today. This is the basis for Option 1 |
| "Any customizations beyond the scope outlined in this proposal will be addressed through a change request process and may incur additional costs" | Assumptions | The clause that would apply if the team and the client agree Option 2 goes beyond the proposal |

Pinpoint, End User Messaging, and AWS SMS do not appear in the SOW. The SOW also lists "SMS text" among core telephony features and "universal queuing... across both voice and SMS," which describe the inbound SMS channel rather than the reminders. Those are separate scope and are not sized here.

**How the options sit against this.** Option 2 is what the client described: keep sending through the AWS SMS API, with Salesforce in Oracle's place. Option 1 is what the SOW assumption implies. The SOW does not say which one delivers the reminder requirement. Whether Option 2 counts as a customization beyond the proposal is a judgment for Ben and Hannah Oanca with the client, and this note does not make it.

## Option 1: native Digital Engagement reminders (what the SOW assumes)

### Pattern

1. SMS consent and callback enrollment live as fields on the Salesforce contact or the callback record. Consent has to survive the 13-month retention scrub for as long as callbacks are scheduled.
2. A scheduled Flow on the callback record fires at the 24-hour and 1-hour marks (or 2-hour, once the client confirms) and calls the **Send Conversation Messages** action with a Messaging Component. One component in English, one in Spanish.
3. The outbound message creates a `MessagingSession` with a `ConversationEntry` per message. Delivery status is on the session, so the "did it send" write-back is native and needs no integration.
4. A reply opens or reopens the session. A Flow can auto-respond with the "call us" text and close it, or Omni-Channel can route it to a specialist. STOP and HELP are handled by Salesforce.
5. Reschedule or cancel: the Flow re-evaluates from the callback record, so a moved callback gets a new reminder and a cancelled one gets none.

Number: a Salesforce-provisioned toll-free or 10DLC long code, or a short code purchased through the account executive. Salesforce Help 000390004 also allows an existing Amazon Connect voice number to be SMS-enabled by support case, US and Canada only, if the client wants reminders from the same number that calls them.

### Constraints

| Constraint | Detail |
| --- | --- |
| Billed blast conversations | The org entitlement is 1,000 for the whole term to 2027-07-02. Each business-initiated reminder is expected to count as a blast conversation. Two texts per callback means roughly 500 callbacks before the cap. The real monthly volume is unknown (question 4) |
| Number provisioning | Toll-free and 10DLC registration through Salesforce commonly takes weeks. Short codes take longer and cost more |
| Provisioning path | After Digital Engagement is enabled, the org calls Salesforce's channel provisioning service, which "runs in the public Salesforce environment." The carrier channel is outside the Salesforce FedRAMP boundary. State this to the client as a compliance caveat, not a blocker |
| Bilingual | Two Messaging Components and a language field on the record |

### Level of effort

| Scope | T-shirt | Assumptions |
| --- | --- | --- |
| Flow, two Messaging Components, auto-reply, consent fields | S | Callback object already designed; consent field decided; number already provisioned |
| The same plus number provisioning, consent modelling, and reschedule handling | M | Kicksaw drives the provisioning case and the 10DLC or toll-free registration; consent model is a design item with the retention scrub |

### Evidence for Option 1

| Source | What it is | What it told us | How it shaped the approach |
| --- | --- | --- | --- |
| [Executed SOW, July 20, 2026 version](https://drive.google.com/file/d/1Dt3mlE0QTSltDJC_utDyGtLsIQURlUUK/view), Addendum A | Contract | SMS/Text Reminders are a functional requirement; SMS is assumed to run on Digital Engagement; customizations beyond the proposal go through change request | The SOW assumption is the reason this option exists |
| [Digital Engagement and Enhanced Messaging for Government Cloud](https://help.salesforce.com/s/articleView?language=en_US&id=ind.government_cloud_digital_engagement_messaging.htm&type=5) | Salesforce Help article | Digital Engagement SMS is available in Government Cloud Plus, FedRAMP High and IL5 authorized. The carrier channel is outside the Salesforce boundary. "Bring Your Own Channel (BYOC) and Bring Your Own Channel for Contact Center as a Service (CCaaS) aren't available in Government Cloud." Provisioning calls a public Salesforce service. Short code, broadcast messaging, and additional SMS conversations are Yes for Government Cloud Plus | Confirms the product works in this org's environment and sets the compliance caveat to state to the client |
| SOQL on `FredHutch-GovCloud`, `PermissionSetLicense` and `TenantUsageEntitlement`, 2026-09-22 | Org query | Messaging User 30 seats, 0 used. Partner Messaging User 30 seats, 0 used. 750 billed agent conversations per month. 1,000 billed blast conversations once for the term to 2027-07-02 | Licensing exists today. The blast cap is the sizing constraint and drives questions 4 and 17 |
| [Send Automated Messages in Enhanced Messaging Channels](https://help.salesforce.com/s/articleView?language=en_US&id=service.messaging_automated_enhanced.htm&type=5) | Salesforce Help article | The Flow action Send Conversation Messages (API 59.0 and later) sends outbound messages on enhanced SMS channels using a Messaging Component | The build is declarative, which is why it sizes S |
| [SMS Supported Countries for Messaging in Digital Engagement](https://help.salesforce.com/s/articleView?id=000381060&language=en_US&type=1) | Salesforce Help article, June 1, 2026 | United States supports Long Code (with MMS), Short Code, and Toll Free | Number type choices for provisioning |
| [Salesforce Voice: Use Your Amazon Connect Phone Number for SMS in Salesforce](https://help.salesforce.com/s/articleView?id=000390004&language=en_US&type=1) | Salesforce Help article, June 16, 2026 | An existing Amazon Connect number can be provisioned for Salesforce SMS by support case. US and Canada only. "Not all Amazon Connect numbers can be provisioned"; eligibility depends on carrier and number type | Gives the "same number as the callback caller ID" option (question 13). This is not a Pinpoint sync; it moves the number into Salesforce's own SMS supply chain |
| [Digital Engagement SMS Messaging Reference](https://help.salesforce.com/s/articleView?id=000380703&language=en_US&type=1) | Salesforce Help article, June 2, 2026 | Number types, A2P rules, opt-in and opt-out concepts, carrier filtering, TCPA and CTIA context | Consent and STOP handling are native. Informs question 7 |

## Option 2: Salesforce to the End User Messaging SMS API in AWS GovCloud (what the client described)

This is the closest equivalent to what runs today, with Salesforce in Oracle's place and AWS End User Messaging in Pinpoint's place. The SMS API the client relies on continues past 2026-10-30. What does not continue is the Pinpoint console and any campaign or journey the client may have built around it.

### Pattern

1. A Platform Event fires on callback create, change, and cancel, carrying the callback ID, phone, language, and scheduled time. No PII beyond the phone number leaves the org.
2. Salesforce Event Relay forwards the event to an Amazon EventBridge partner event bus in `us-gov-west-1`. Event Relay is supported for Government Cloud civilian orgs and can target AWS GovCloud regions.
3. EventBridge Scheduler (or a Step Functions wait state) holds the 24-hour and 1-hour sends. A cancel event deletes the pending schedules.
4. A Lambda calls the End User Messaging SMS and Voice v2 `SendTextMessage` API with the English or Spanish template.
5. An End User Messaging configuration set streams delivery events to a Lambda, which writes status back to Salesforce through the REST API or an inbound Platform Event. This reproduces the "Pinpoint writes back to Oracle" behavior.
6. Two-way SMS on the number routes replies to an SNS topic. A Lambda sends the "call us" auto-reply. STOP and HELP are handled by End User Messaging at the platform level unless the client wants replies routed to specialists.

Number: a new toll-free, 10DLC, or short code requested in End User Messaging in `us-gov-west-1`, or the client's current number ported in if AWS supports that move (question 16). Origination identities are region-specific and cannot be shared across regions, so the existing commercial-region number does not carry over on its own.

### Constraints

| Constraint | Detail |
| --- | --- |
| AWS ownership | Someone has to own End User Messaging, Lambda, EventBridge, and the number registration in the Fred Hutch GovCloud account. Suchi Panda called new AWS work "a very big ask" for the Fred Hutch cloud team at kickoff |
| Custom code | Three Lambdas and a scheduler are maintained code, not configuration |
| Data path | Event Relay processes events on Hyperforce in the United States before delivery to EventBridge. Salesforce states that "it's possible for data to leave the FedRAMP authorized environment" depending on configuration. The payload here is a phone number and a time, which keeps the exposure small, but the client's compliance lead has to accept it |
| Spend threshold | The End User Messaging default is USD 1 per account and must be raised before production |
| Number | Registration lead time as in Option 1, plus the porting question |

### Level of effort

| Scope | T-shirt | Assumptions |
| --- | --- | --- |
| Platform Event, Event Relay, scheduler, send Lambda, status write-back, auto-reply | M | Fred Hutch owns and provisions the AWS account and grants Kicksaw access; number already registered; one language template each way |
| The same plus AWS account setup, IAM, number registration or port, and monitoring | L | Kicksaw stands up the AWS side end to end and hands it over |

### Evidence for Option 2

| Source | What it is | What it told us | How it shaped the approach |
| --- | --- | --- | --- |
| Client transcripts: [2025-07-29 reverse demo](../discovery/transcripts/2025-07-29-nci-call-center-reverse-demo.md) at 27:50; [Session 1](../discovery/transcripts/2026-09-15-discovery-session-1-contact-center-reverse-demo.md) at 50:10 to 51:27; [Session 3](../discovery/transcripts/2026-09-22-discovery-session-3-general-cancer-callbacks.md) at 43:17 to 46:12 | Client calls | Oracle to Pinpoint through the Oracle API, filtered on SMS consent and callback enrollment. Reminders at 24 hours and 1 hour. No PII. Delivery status written back. Replies get an automated "call us" | Defines the functional shape to reproduce: outbound send, status write-back, auto-reply |
| [Amazon Pinpoint end of support](https://docs.aws.amazon.com/pinpoint/latest/userguide/migrate.html) | AWS documentation | End of support 2026-10-30. "Use of APIs related to SMS, Voice, Mobile Push, OTP and Phone Number Validate will not be affected by this change." Endpoints, segments, campaigns, journeys, and analytics retire. AWS recommends Amazon Connect outbound campaigns as the replacement for campaigns and journeys | Confirms the API path survives. Raises question 1 on which API the client calls today, because the page names the SMS and Voice v2 API and is silent on legacy application-scoped calls |
| [AWS GovCloud (US) product details](https://aws.amazon.com/govcloud-us/details/) and [AWS End User Messaging in AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-eum.html) | AWS documentation | Amazon Pinpoint is not listed as a GovCloud service. End User Messaging is available in GovCloud (US-West) and (US-East). Text to voice is US-West only | Today's Pinpoint runs in a commercial AWS account. A GovCloud rebuild lands in `us-gov-west-1` |
| [AWS End User Messaging endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/end-user-messaging.html) | AWS General Reference | FIPS endpoints exist: `sms-voice-fips.us-gov-west-1.amazonaws.com`. Default quotas: 25 phone numbers per account, 1 message per second to a single recipient, spend threshold USD 1 per account | FIPS satisfies the boundary requirement. The spend threshold must be raised before go-live |
| [AWS services in scope by compliance program: FedRAMP](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/) | AWS compliance page | "Amazon Pinpoint and End User Messaging" is FedRAMP High in GovCloud and Moderate in US East and West. Lambda, EventBridge, SNS, Lex, and Amazon Connect are the same | No compliance objection to the pattern |
| [Event Relay Considerations](https://help.salesforce.com/s/articleView?id=platform.ev_relay_considerations.htm&language=en_US&type=5) | Salesforce Help article | "Event Relay is available for customers using Salesforce Government Cloud orgs in civilian environments. GovCloud customers can configure event relay to send events to AWS GovCloud regions." Processing occurs on Hyperforce in the United States. Data can leave the FedRAMP environment depending on configuration | Enables event-driven outbound instead of polling. Adds the Hyperforce data-path caveat |
| [Engaging Salesforce Customers with Bidirectional SMS Using AWS](https://aws.amazon.com/blogs/apn/engaging-salesforce-customers-with-bidirectional-sms-using-aws/) | AWS Partner Network blog, November 17, 2022 | Outbound: a `GenericSMS` Platform Event, Event Relay, EventBridge, Step Functions, SNS publish. Inbound: Pinpoint two-way to SNS to Lambda to an EventBridge API destination that posts an inbound Platform Event. Auth by Connected App OAuth | The custom pattern is AWS-documented. Swap Pinpoint for the End User Messaging `SendTextMessage` call |
| [Two-way SMS messaging](https://docs.aws.amazon.com/sms-voice/latest/userguide/two-way-sms.html) and [example payload](https://docs.aws.amazon.com/sms-voice/latest/userguide/two-way-sms-payload.html) | AWS documentation | Inbound goes to an SNS topic or Amazon Connect. Payload fields: `originationNumber`, `destinationNumber`, `messageKeyword`, `messageBody`, `inboundMessageId`, `previousPublishedMessageId`. STOP and HELP are answered at the platform level and not forwarded unless self-managed opt-out is enabled | The auto-reply is one Lambda. Opt-out costs nothing unless replies must route to people |
| [Choosing an origination identity](https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-number-types.html) | AWS documentation | Toll-free: 1 to 3 message parts per second, registration required. 10DLC: brand and campaign registration, 7 to 10 days after approval. Short code: 8 to 12 weeks. "Origination identities are resources that are unique to each AWS Region, so they can't be shared across AWS Regions" | Number provisioning is on the critical path. The commercial-region number does not move on its own (question 16) |

## What both options share

These items are design work regardless of option, and none of them is answered yet.

- Where SMS consent lives in Salesforce and how it survives the 13-month scrub (B-14).
- Reschedule and cancel behavior. Today's behavior in Oracle is unknown (question 9).
- The exact reminder text in English and Spanish (A-26, still not supplied).
- Timing: 24 hours and 1 hour before the callback (decided 2026-09-28), plus whatever the "few other follow up reminders" turn out to be (question 6).
- The reply policy: auto "call us" only, or route to a specialist. Mike Griffin's "Maybe" on two-way confirm or cancel is a backlog item, not a requirement.
- Number type and provisioning lead time, which is on the critical path for either option.

## Ruled out, with evidence

| Pattern | Why it is out | Source |
| --- | --- | --- |
| Amazon Connect native SMS channel | The Amazon Connect messaging integrations table lists SMS as **No** for AWS GovCloud (US-West). Outbound campaigns, Customer Profiles, and Cases are also absent from GovCloud | [Availability of Amazon Connect features by Region](https://docs.aws.amazon.com/connect/latest/adminguide/regions.html) |
| Salesforce Contact Center with Amazon Connect (digital channels) | Depends on Connect SMS and chat in the same region, and on Bring Your Own Channel for CCaaS on the Salesforce side. Both are unavailable | Same region table; [Government Cloud messaging article](https://help.salesforce.com/s/articleView?language=en_US&id=ind.government_cloud_digital_engagement_messaging.htm&type=5); [Amazon product and SOW alignment](../project/amazon-product-sow-alignment-2026-09-21.md), AppExchange table |
| Bring Your Own Channel for CCaaS (now Partner Contact Center Messaging) | "Bring Your Own Channel (BYOC) and Bring Your Own Channel for Contact Center as a Service (CCaaS) aren't available in Government Cloud." The org's 30 Partner Messaging User seats are unexplained (question 19) | [Government Cloud messaging article](https://help.salesforce.com/s/articleView?language=en_US&id=ind.government_cloud_digital_engagement_messaging.htm&type=5) |
| Pinpoint campaigns, journeys, and segments | Retire 2026-10-30. AWS's recommended replacement, Amazon Connect outbound campaigns, is not available in GovCloud | [Amazon Pinpoint end of support](https://docs.aws.amazon.com/pinpoint/latest/userguide/migrate.html); [Amazon Connect region table](https://docs.aws.amazon.com/connect/latest/adminguide/regions.html) |
| An installed package | None exists for Pinpoint plus Salesforce. AWS sample code (`aws-samples/amazon-pinpoint-salesforce-channel` and a Pinpoint-to-CRM sync) targets the retiring engagement features. Zapier and Workload connectors run outside any FedRAMP boundary | GitHub `aws-samples`; AWS blog index |

## Questions to close before sizing

Written client-safe. Each row names who answers and why it matters.

### Current state

| # | Question | Who | Why it matters |
| --- | --- | --- | --- |
| 1 | Does today's integration use Pinpoint campaigns or journeys, or only an SMS send API called from a script or Lambda? Which API: the SMS and Voice v2 `SendTextMessage`, or the older application-scoped Pinpoint send? | Mark Hubers | Decides whether anything stops on 2026-10-30, and whether "keep using the API" is safe as-is |
| 2 | Which AWS account and region runs it, and who owns that account? | Mark Hubers, Adrianna Gutierrez | Pinpoint is not a GovCloud service, so today's setup is commercial. Ownership decides who can change it |
| 3 | What is the sender number type (toll-free, 10DLC, short code), under whose brand registration, and does it need to stay the same? | Mark Hubers | Provisioning lead time and the porting question |
| 4 | Monthly volume: callbacks scheduled per month, times two reminders, plus any follow-ups | Adrianna Gutierrez, Ray Quijano | Decides Option 1 against the 1,000 blast conversation entitlement |
| 5 | The exact message text, English and Spanish | Holly Fernandez-Johnson | Template content (A-26) |
| 6 | Timing is decided: 24 hours and 1 hour before the callback. What are the "few other follow up reminders" Mark mentioned on session 1? | Mark Hubers, Adrianna Gutierrez | Any reminders beyond the two change the build |
| 7 | Where does SMS consent live today, and how does it survive the 13-month scrub? How do STOP replies reach Oracle? | Mark Hubers | Consent model in Salesforce (B-14) |
| 8 | What is written back to Oracle: delivery status only, or reply text too? What does the specialist see? | Mark Hubers | The write-back requirement |
| 9 | When a callback is rescheduled or cancelled, does Pinpoint get told, and are queued texts withdrawn? | Mark Hubers, Holly Fernandez-Johnson | Reschedule handling in either option |
| 10 | Who built it and who maintains it? Is there code or configuration to review? | Adrianna Gutierrez | Whether there is anything to inspect before sizing |

### Requirements

| # | Question | Who | Why it matters |
| --- | --- | --- | --- |
| 11 | Is two-way confirm or cancel in scope for go-live, or backlog? | Mike Griffin | Mike said "Maybe" at session 3 |
| 12 | Is a new number acceptable with notice to clients, or must the number stay the same? | Mike Griffin, Adrianna Gutierrez | A ported number adds lead time and may not be possible in GovCloud |
| 13 | Should reminders come from the same number that places the callback, or a separate one? | Holly Fernandez-Johnson | Decides whether the Connect number SMS-enable path (Help 000390004) is worth pursuing |

### AWS

| # | Question | Who | Why it matters |
| --- | --- | --- | --- |
| 14 | Is Amazon Connect SMS on the GovCloud (US-West) roadmap before January 2027? The region table says No today | Ken Daugherty, Binu Pazhoor | Would reopen the Connect channel pattern |
| 15 | For Option 2, who operates End User Messaging, Lambda, and EventBridge in the Fred Hutch GovCloud account? | Ken Daugherty, Suchi Panda | The AWS ownership gap already on the RAID Log |
| 16 | Can a commercial-region number be ported into `us-gov-west-1` End User Messaging? Lead time, and does registration carry? | Binu Pazhoor | Origination identities are region-specific |

### Salesforce account team

| # | Question | Who | Why it matters |
| --- | --- | --- | --- |
| 17 | Cost and mechanism to raise billed blast conversations above 1,000 for the term. Do reminder texts count as blast or agent conversations? | Mitchell Rabin | The Option 1 sizing constraint |
| 18 | Digital Engagement number provisioning lead time in Government Cloud Plus | Mitchell Rabin | Critical path for Option 1 |
| 19 | Why does the org carry 30 Partner Messaging User seats when Help says Bring Your Own Channel is unavailable in Government Cloud? | Mitchell Rabin | Either inert or a sign of a plan nobody has explained |

### Already answered by documentation

| Question | Answer | Source |
| --- | --- | --- |
| Does the Pinpoint SMS API survive October 2026? | Yes. SMS, voice, push, OTP, and phone number validate APIs continue under End User Messaging | Amazon Pinpoint end of support page |
| Is End User Messaging in AWS GovCloud? | Yes, US-West and US-East, with FIPS endpoints | AWS GovCloud End User Messaging page; AWS General Reference |
| Is it FedRAMP authorized? | High in GovCloud, Moderate in US East and West | AWS services in scope |
| Can Amazon Connect carry the SMS in GovCloud? | No, SMS is not offered in GovCloud (US-West) | Amazon Connect region table |
| Can Bring Your Own Channel bring Connect SMS into Salesforce? | No, not in Government Cloud | Government Cloud messaging article |
| Is Salesforce's own SMS usable in this org? | Yes. Digital Engagement is available in Government Cloud Plus, FedRAMP High, and the org licenses it | Government Cloud messaging article; org query |
| Can Salesforce push events to AWS GovCloud? | Yes, Event Relay supports Government Cloud civilian orgs and GovCloud targets | Event Relay Considerations |
| How do replies and STOP work on End User Messaging? | Replies go to SNS or Connect with a documented payload; STOP and HELP handled at the platform level | Two-way SMS pages |
| Which US number types exist and how long do they take? | Toll-free (weeks, registration), 10DLC (7 to 10 days after approval), short code (8 to 12 weeks) | Choosing an origination identity |
| Is there an installed package? | No | GitHub and AWS blog search |

## Proposed register and RAID changes, not applied

Propose only. Ben applies or approves.

**RAID-39, legacy D19, SMS callback reminders rebuilt off Amazon Pinpoint.** Proposed Description and Resolution changes:

- Replace "whether AWS End User Messaging SMS is available in us-gov-west-1 is unverified" with: verified 2026-09-17 and 2026-09-22, available in GovCloud (US-West) and (US-East) with FIPS endpoints.
- Add the session 3 requirements: delivery status writes back to the system of record, as Pinpoint writes back to Oracle today; replies get an automated redirect to call; reminders go 24 hours and 1 hour before the callback (decided 2026-09-28).
- Add the SOW position: reminders are a named requirement; the SOW assumes SMS runs on Digital Engagement and does not name Pinpoint or AWS.
- Add the constraint: 1,000 billed blast conversations for the term in the org.
- Soften the resolution from "rebuilt on the new platform" to "two options identified, native Digital Engagement or End User Messaging in GovCloud; neither chosen." Amazon Connect SMS and Bring Your Own Channel are unavailable in Government Cloud.
- Source: add Session 3 at 43:17 to 46:12 and this note.

**New Risk proposal.** If today's reminders use Pinpoint campaigns or journeys, they stop on 2026-10-30, three months before go-live, while Oracle is still the live system. Owner Ben Bolding. Client-safe once question 1 is put to Mark Hubers. Contingent on the answer; if the client calls only the SMS API, close it.

**New Action proposals.**

| Action | Owner | Source |
| --- | --- | --- |
| Put questions 14 to 16 to Ken Daugherty and Binu Pazhoor, off the client call | Ben Bolding | This note |
| Put questions 17 to 19 to Mitchell Rabin | Ben Bolding | This note |
| Put question 1 to Mark Hubers before the SMS session, because it gates the new Risk | Avi Rabinovitch | This note |

## Proposed session guide additions

For the dedicated session on VA callbacks, referrals, and SMS reminders, which is still to be scheduled. New IDs continue from the session 3 guide: Avi's start at A-32, Ben's at B-37. Existing items A-22, A-24, A-25, A-26, B-14, and B-18 carry forward unrenumbered.

### Avi's section

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| A-32 | Walk through what a client sees: the two reminder texts, what happens when they reply, and what happens when the callback moves. Read back "We're going to call you at 9:30 AM" and ask for the full text in both languages | S3 | |
| A-33 | Reminder timing is decided: 24 hours and 1 hour before. Are there other reminders after the callback? | S1, S3 | |
| A-34 | Is two-way confirm or cancel wanted for go-live, or is it a later enhancement? Mike Griffin said "Maybe" | S3 | |
| A-35 | Does a client need to see the same number every time, and does it need to match the number that calls them? | S3 | |

### Ben's section

| ID | Question | Origin | Status |
| --- | --- | --- | --- |
| B-37 | Which Pinpoint features run today: campaigns or journeys, or an SMS API call from a script or Lambda? Which API? | S3, AWS-22 | |
| B-38 | Which AWS account and region hosts Pinpoint, who owns it, and who built and maintains the integration? | S3 | |
| B-39 | Sender number type and registration, and whether it must stay the same | S3 | |
| B-40 | Monthly reminder volume, from the callback count. Read back the 1,000 blast conversation entitlement internally only, not on the call | S3, AWS-22 | |
| B-41 | What Pinpoint writes back to Oracle, and what the specialist sees on the inquiry | S3 | |
| B-42 | Reschedule and cancel: does Pinpoint learn about the change, and are queued texts withdrawn? | S3 | |

`AWS-22` is this note's research of 2026-09-22.

## Sources

Every source is cited in exactly one evidence table in the sections "Evidence for Option 1," "Evidence for Option 2," and "Ruled out, with evidence." This list is the index.

- Executed SOW, July 20, 2026 client-redlined version, Kicksaw Google Drive
- Transcripts: 2025-07-29 reverse demo; 2026-09-15 discovery session 1; 2026-09-22 discovery session 3
- Org queries against `FredHutch-GovCloud` on 2026-09-22: `PermissionSetLicense`, `TenantUsageEntitlement`
- Salesforce Help: Digital Engagement and Enhanced Messaging for Government Cloud; Event Relay Considerations; Send Automated Messages in Enhanced Messaging Channels; articles 000381060, 000390004, 000380703
- AWS: Amazon Pinpoint end of support; AWS GovCloud (US) product details; AWS End User Messaging in AWS GovCloud (US); End User Messaging endpoints and quotas; AWS services in scope by compliance program (FedRAMP); Availability of Amazon Connect features by Region; Two-way SMS messaging and example payload; Choosing an origination identity; APN blog, Engaging Salesforce Customers with Bidirectional SMS Using AWS
- [Amazon product and SOW alignment, 2026-09-21](../project/amazon-product-sow-alignment-2026-09-21.md), for the Salesforce Contact Center with Amazon Connect finding

## Change log

| Date | Change |
| --- | --- |
| 2026-09-22 | Created. Current state from three client calls, SOW position recorded, two options sized, one family of patterns ruled out, 19 questions listed with owners, register and guide changes proposed and not applied |
| 2026-09-28 | Reminder timing decided by Ben: 24 hours and 1 hour before the callback. Removed as an open conflict; question 6 now asks only about the other follow-up reminders |
| 2026-09-23 | Reframed per Ben. Option 2 presented as what the client described, Option 1 as what the SOW assumes. Removed the contracted-versus-change-request headline; the SOW clause is noted, the call is left open |

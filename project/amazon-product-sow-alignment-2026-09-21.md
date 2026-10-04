# Amazon product and SOW alignment

- **Date:** 2026-09-21
- **Author:** Ben Bolding, with assistant research
- **Handling:** internal Kicksaw working document. Parts fail the client-safe test because they describe what Kicksaw has and has not verified. See [Producing a client-safe version](#producing-a-client-safe-version)
- **Purpose:** establish which Amazon product the engagement is actually delivering, and where that product does and does not line up with the executed statement of work

## The statement of work this document measures against

Two versions of the NCI Service Center Migration statement of work exist in the Kicksaw Google Drive, both from July 2026. This document measures against the later one.

| Version | Location | Link |
| --- | --- | --- |
| **July 20, 2026, governing** | `Fred Hutchinson Cancer Center / PSA-SOW` | [Kicksaw NCI Service Center Migration SOW 7202026-KS Updated.docx](https://drive.google.com/file/d/1Dt3mlE0QTSltDJC_utDyGtLsIQURlUUK/view) |
| July 2, 2026, superseded | `Fred Hutchinson Cancer Center / Sales Notes` | [Kicksaw NCI Service Center Migration SOW 7022026](https://docs.google.com/document/d/1JP0scimahB3evBTgb0pdqE0Kq-FmE--FO57CRPr8DVg/edit) |

The July 20 version is treated as governing on three grounds: it is the later of the two, it sits in the contracts folder rather than the sales folder, and the internal review on 2026-09-03 resolved that the most recently signed, client-redlined statement of work governs.

**One caveat.** The July 20 filename reads "KS Updated," which describes a Kicksaw revision rather than a countersigned document. Drive metadata cannot confirm signature status. Anyone relying on this document for a contractual argument should confirm the executed artifact with Hannah Oanca or Tony McCune first.

Three other Fred Hutch statements of work sit in the same Drive account folder and belong to different engagements: a compliance statement of work dated May 15, 2026, an Admin on Demand statement of work dated February 18, 2025, and the 2024 statement of work from the prior implementation.

## The scope tracker this document reads alongside

Ben Bolding shared the [Fred Hutch CIS Project Plan + Scope Tracker](https://docs.google.com/spreadsheets/d/1tqBE3dywkXV_XJvXEzY1aa3HvHwSS9EAHdzl_YR2A_k/edit?gid=1999232366#gid=1999232366) on 2026-09-23 as the quick reference for what is in and out of scope. It is the team's working reading of the statement of work, not a replacement for it, and it is not a schedule: the Project Plan tab carries no dates, and its Build phase still holds a template task from another engagement ("Intake & Surgeon Profile"). The Scope Tracker tab is the part this document uses.

| Attribute | Value |
| --- | --- |
| Created | 2026-09-17, last modified the same day, which is the day of discovery session 2 |
| Scope rows | 66, across 13 workstreams |
| Status key | In Scope, Needs Decision, Deferred / Future Phase, Out of Scope, Added Scope |
| In Scope | 49 |
| Needs Decision | 3: on-site vaccine requirements (CS-8), a different WFM product than Calabrio (OOS-7), the milestone billing structure (OOS-9) |
| Deferred | 2: data mapping and migration execution (DM-1, DM-2) |
| Out of Scope | 12 |

**Citation note.** The tracker numbers its discovery rows D-1 to D-5, which collide with the local register's decision IDs. Tracker rows are cited here as "tracker" plus the ID and a descriptor, so tracker D-5 (Amazon Connect instance planning) is never confused with the partition decision (D2).

### How the tracker reads each finding in this document

| Finding | Tracker rows | What the tracker says | What follows |
| --- | --- | --- | --- |
| Amazon Connect has no email channel in AWS GovCloud | TO-3 (core telephony features) and TO-8 (channels and numbers), both In Scope | Email is in scope and listed among telephony features, with no note that Amazon Connect cannot carry it in GovCloud | Finding stands. Scope is unaffected because Email-to-Case delivers it. The tracker should say so under TO-3, so nobody reads email as an Amazon Connect channel |
| Real-time transcription is unresolved | None | Silent. No row names transcription, Contact Lens, or call analytics | Finding stands and the tracker cannot arbitrate it. If the client expects transcription, it needs a row |
| No FIPS endpoint for Amazon Connect in `us-gov-west-1` | CS-1 (all systems within GovCloud) is the nearest | Silent on endpoints | Finding stands |
| Salesforce chat into Calabrio | WF-2 (Kicksaw support within Service Cloud for data and workflow visibility alongside Calabrio ONE), In Scope. OOS-1 note limits Kicksaw to Service Cloud integration touchpoints with Calabrio | Broader than this document first stated. The statement of work gives Kicksaw a supporting role for Salesforce-side touchpoints; it does not name a chat feed into Calabrio | Severity stays Medium. The finding is narrowed below: the feed is unnamed, the supporting role is not |
| Surveys entitled at 300 responses, `enableSurvey` off | TO-6 (post-call demographic prompts) and CK-4 (embedded surveys), both In Scope, no licensing note | The tracker flags SMS licensing as a Fred Hutch dependency under TO-2 and carries no equivalent note for surveys | Gap stands. The tracker should carry the same kind of dependency note |
| AWS account ownership | D-5 (Amazon Connect instance planning): Kicksaw provisions the Amazon Connect instance during implementation; Fred Hutch procures Salesforce and Amazon Connect licenses | Consistent with bring-your-own. Fred Hutch owns the AWS account and the licenses, Kicksaw builds the instance inside it | Sharpens open item 5: the unanswered question is account, identity and billing administration, not who builds the Connect instance |
| Outbound campaigns unavailable in AWS GovCloud | TO-1 (outbound calls with configurable caller IDs) and TO-5 (scheduled callbacks), both In Scope | CIS is not inbound only. Both rows describe agent-placed calls, which are core Amazon Connect, not the outbound campaigns dialer feature | Low bearing confirmed, wording corrected in the email section |
| Calabrio compliance question misframed | SC-5 (Government Cloud environment configuration) and CS-1 (compliance and security): all Salesforce, Amazon Connect and Calabrio licenses must be FedRAMP/GovCloud approved and all systems must operate within GovCloud | Carries the same conflation this document corrects. Calabrio runs in its own FedRAMP Moderate environment, inside neither GovCloud | Reword both rows so a reviewer does not place Calabrio inside a GovCloud boundary |

### Two things the tracker adds

**A chatbot is in scope, and its delivery route is not clean.** TO-8 lists "Live Chat (Chatbot and SMS)" as In Scope. Amazon Connect AI agents are unavailable in AWS GovCloud, so a chatbot has to be Salesforce-side. The Government Cloud available products article, published 2026-09-16, lists Einstein Bots as Interoperable only, meaning functionally tested but outside the FedRAMP authorization boundary, and lists Agentforce customer agents as authorized. Discovery session 2 recorded Mark Hubers as saying Fred Hutch is "very strict" on AI and that anything AI needs explicit approval from Fred Hutch and probably NIH. Either route therefore needs an approval that has not started. Recorded as a fifth misalignment below and as open item 11.

**Data migration is now Deferred.** DM-1 and DM-2 are Deferred with the note that Adrianna Gutierrez tentatively decided against data migration on the 2026-09-17 call. The session 2 transcript records the same position as "start fresh," with the knowledge base, scheduled callback tasks and in-flight work as the exceptions, and NCI concurrence still open. This sits outside the product question, and is noted because the alignment table below lists knowledge article migration as aligned. That row survives the deferral, since knowledge is one of the exceptions.

### Proposed tracker updates

The tracker is a team surface in Google Drive. These are proposals for whoever maintains it, not changes made here.

| Row | Proposed change | Reason |
| --- | --- | --- |
| TO-3 (core telephony features) | Add a note: email is delivered by Salesforce Email-to-Case, since Amazon Connect has no email channel in AWS GovCloud | Stops email being read as a Connect channel during Voice design |
| TO-6 and CK-4 (surveys) | Add a dependency note in the TO-2 pattern: base Salesforce Surveys entitlement is 300 responses for the term, sizing waits on Oracle volumes, any additional purchase is Fred Hutch's | The tracker flags the SMS license and not the survey one, and both are Fred Hutch procurement items |
| TO-8 (channels) | Split the chatbot into its own row at Needs Decision | Delivery route and AI approval path are both unresolved |
| SC-5 and CS-1 (compliance wording) | Replace "operate within GovCloud" with "hold a FedRAMP Moderate or higher authorization" | Calabrio is outside both GovClouds and the current wording cannot be satisfied as written |
| New row, Telephony & Omnichannel | Real-time transcription and Contact Lens in AWS GovCloud, at Needs Decision, owner AWS | Headline Voice capability with contradictory AWS documentation |
| New row, Compliance & Security | FIPS endpoint for Amazon Connect in `us-gov-west-1`, at Needs Decision, owner AWS | Salesforce requires one and none is published |

## Ownership boundary

Set by Ben Bolding on 2026-09-23, and it governs how every finding below is read:

| Area | Owner | Kicksaw's part |
| --- | --- | --- |
| All AWS configuration, including security, discovery and questions | The AWS team (Ken Daugherty, Binu Pazhoor) with Fred Hutch | None, unless the AWS team asks a Salesforce-specific question |
| FIPS configuration and endpoints | AWS, as part of the AWS configuration | None |
| Transcription | Calabrio, inside its own product | Answering Salesforce questions only |
| Salesforce Government Cloud org, Voice setup on the Salesforce side, Email-to-Case, surveys, knowledge, reporting | Kicksaw | Everything |

Findings about AWS or Calabrio stay in this document because they bear on the statement of work premise, not because Kicksaw resolves them. Each one now states what, if anything, is left for Kicksaw.

## Summary

The statement of work premise and the product Fred Hutch bought line up. Salesforce Service Cloud Voice with Amazon Connect is the contracted telephony direction, and the license in the Government Cloud org is the model that Government Cloud supports. No AppExchange package is required to deliver it.

Five things do not line up, and one of them was never asked correctly:

| Misalignment | Severity | Owner |
| --- | --- | --- |
| Amazon Connect has no email channel in AWS GovCloud, and email is an unchanged entry point | High | Kicksaw, delivered by Email-to-Case |
| Real-time transcription availability in AWS GovCloud is unresolved, and it is a headline Voice capability | High for the premise, not Kicksaw's to resolve | Calabrio for transcription; AWS for Contact Lens if a transcript in the agent console is expected |
| No FIPS endpoint is published for Amazon Connect in `us-gov-west-1`, and Salesforce requires one | High for the premise, not Kicksaw's to resolve | AWS |
| Salesforce chat into Calabrio is a stated client requirement that neither statement of work names, though the Kicksaw statement of work gives Kicksaw a supporting role for Salesforce-side touchpoints (tracker WF-2) | Medium | Trevor Holt (Calabrio) |
| A chatbot is in scope (tracker TO-8) and neither delivery route is clean: Amazon Connect AI agents are unavailable in AWS GovCloud, Einstein Bots are Interoperable only in Government Cloud Plus, and Agentforce needs an AI approval Fred Hutch says must go through NIH | Medium | Kicksaw with CIS |

## What the Amazon product is

### The telephony model is settled

The Government Cloud org holds one Voice license, and only one:

| Permission set license | API name | Total | Used |
| --- | --- | --- | --- |
| Salesforce Voice User (Partner Telephony) | `ServiceCloudVoiceExternalTelephonyPsl` | 60 | 0 |

The Salesforce-provisioned Amazon Connect variant does not appear in the org at all, at any quantity. Salesforce currently names these models as follows:

| Former name | Current name | AWS account owner |
| --- | --- | --- |
| Salesforce Voice (Native Telephony) | Agentforce Contact Center Voice | No AWS account |
| Salesforce Voice with Partner Telephony | Partner Contact Center Voice | The telephony vendor |
| Salesforce Voice with Amazon Connect | Partner Contact Center with Amazon Connect | Salesforce |
| Salesforce Voice with Partner Telephony from Amazon Connect | Partner Contact Center with Amazon Connect - Bring Your Own | **The customer** |

The license in the org is the bring-your-own model. Fred Hutch owns the AWS account and the Amazon Connect instance.

Two independent facts confirm this. The Salesforce Government Cloud documentation states that "Government Cloud is supported only via Salesforce Voice with Partner Telephony." Ben Bolding confirmed on 2026-09-21 that Fred Hutch purchased an AWS GovCloud instance for this project, and that it is greenfield.

### No AppExchange package is required

Salesforce documents the setup path for this model as a native Setup page:

> If you have the Salesforce Voice with Partner Telephony license, you see the Partner Telephony Setup page in the Setup menu.
>
> From Setup, enter Partner Telephony Setup in the Quick Find box, then select Partner Telephony Setup. Select Turn On Salesforce Voice.

There is no install step. Configuration consists of an AWS Identity and Access Management role in the Fred Hutch AWS account, plus contact flows on the Amazon Connect side.

The org confirms no telephony work has started:

| Check | Result |
| --- | --- |
| Installed packages | 4, all standard Salesforce |
| Amazon Connect CTI Adapter | Not installed |
| Salesforce Contact Center with Amazon Connect | Not installed |
| Call centers configured | 0 |
| Voice licenses assigned | 0 of 60 |
| `VoiceCall` records | 0 |

### The AppExchange Government Cloud filter is not evidence

The filter that prompted this research does not mean what it appears to mean. Salesforce states:

> Salesforce makes no compliance or interoperability claims associated with these apps. The independent software vendor (ISV) has only confirmed and reported that their app can be installed and successfully used in the Salesforce Government Cloud Plus and Government Cloud Plus - Defense environments.
>
> An app that isn't indicated as compatible with Government Cloud can work with the Government Cloud Plus and Government Cloud Plus - Defense environments but likely hasn't been tested or reported by the ISV.

Two consequences. Absence from the filter means the vendor has not self-reported, not that the product fails. Presence on the filter proves nothing about FedRAMP compliance, because Salesforce disclaims the claim.

Kicksaw should not offer the filter to NCI as evidence of anything. The evidence NCI will accept is the Government Cloud product authorization list and written statements from AWS.

### The three AppExchange listings examined are all off the delivery path

| Listing | Product | Why it is not the answer |
| --- | --- | --- |
| `a0N4V00000IYf0nUAD` | AWS Partner CRM Connector | Unrelated. Handles AWS partner co-sell and AWS Marketplace private offers |
| `a0N3A00000EJH4yUAH` | Amazon Connect CTI Adapter | Legacy Open CTI adapter. A fallback that gives up native transcription, Omni-Channel voice routing, and the unified supervisor experience |
| `edd960cb-4bef-4af1-a2b9-0630e70eebf5` | Salesforce Contact Center with Amazon Connect | Requires Digital Engagement licensing to deliver Amazon Connect digital channels, most of which AWS GovCloud does not support |

## Alignment against the statement of work

| Statement of work element | Evidence | Verdict |
| --- | --- | --- |
| Replace Oracle Service Cloud with Salesforce Service Cloud | 60 Salesforce licenses, 10 used. Knowledge enabled | Aligned |
| Replace Cisco Finesse and Verizon IVRs with Service Cloud Voice and Amazon Connect | Voice with Partner Telephony licensed at 60 seats | Aligned |
| Replace Verint with Calabrio | Calabrio contracted separately, sources data from Amazon Connect | Aligned, with a scope gap |
| Migrate roughly 5,000 English and Spanish knowledge articles | Knowledge enabled. Only `en_US` configured, 6 sample articles present | Aligned, configuration outstanding |
| Embedded surveys | Base Surveys entitled at 300 responses for the term. `enableSurvey` is `false` | **Gap** |
| Anonymized demographic data | Custom build, no product dependency | Aligned |
| Retention controls | Native or custom, no product dependency | Aligned |
| Dashboards and reporting | Native reporting plus Service Analytics Apps at 60 | Aligned |
| All integrations inside the Government Cloud boundary | No packages required for the core build | Aligned, and strengthened |

## Where the product and the statement of work do not align

### Amazon Connect has no email channel in AWS GovCloud

Amazon Connect runs in one GovCloud region, AWS GovCloud (US-West), which is `us-gov-west-1`. AWS documents these features as unavailable there:

| Unavailable in AWS GovCloud | Bearing on NCI CIS |
| --- | --- |
| Email channel | Direct. Email is an unchanged entry point |
| Outbound campaigns | Low. CIS places outbound calls with configurable caller IDs and scheduled callbacks (tracker TO-1 and TO-5), but those are agent-placed calls, not the campaigns dialer feature. Confirm no campaign-style dialing is expected |
| Customer profiles | Low. Demographic capture belongs in Salesforce |
| Cases | None. Salesforce Cases apply |
| Agentic CX designer, AI agents, Apple Business Chat, live media streaming | None |

The entry point decision (D18, entry points do not change) records that the email address stays the same. Discovery session 2 on 2026-09-17 covered email in detail. When Mark Hubers asked where the NIH inbox auto-forward should point, Avi Rabinovitch named Email-to-Case as the pattern, so nothing in that session assumed Amazon Connect carries email. The scope tracker (TO-3, core telephony features) still lists email among telephony features, which is the one place the wrong reading could take hold.

**Recommendation:** confirm that email is delivered by Salesforce Email-to-Case, not Amazon Connect, and record it as a decision. Reason: the architecture is sound either way, but only one of the two options exists in the chosen partition.

### Real-time transcription availability is unresolved

The AWS GovCloud service page lists "conversational analytics AI features" as unavailable in AWS GovCloud. AWS separately announced Contact Lens general availability in AWS GovCloud (US-West) on July 1, 2025, including call transcription, and real-time dashboards in May 2025.

These two statements cannot both be complete. Either the GovCloud service page is stale, or "conversational analytics AI features" refers only to newer generative capabilities such as Amazon Q in Connect.

This matters because real-time transcription is a headline Service Cloud Voice capability and part of what justifies leaving Cisco Finesse. Kicksaw cannot resolve it from published documentation, and under the ownership boundary it does not try to.

**Ownership.** Transcription is Calabrio's, inside Calabrio ONE, for quality management and analytics. That covers the leader-facing use Holly Fernandez-Johnson and Ray Quijano described. It does not produce a live transcript in the agent's Salesforce console; that comes from Contact Lens in Amazon Connect, which is the AWS team's to confirm and configure. Kicksaw's only part is not to represent a console transcript as delivered until AWS confirms it.

**Recommendation:** hand the Contact Lens contradiction to the AWS team as their question, and keep a console transcript out of any Kicksaw demo or design until they answer. Reason: the capability is AWS's to provide, and a demo that shows it before AWS confirms it creates an expectation Kicksaw cannot meet.

### No FIPS endpoint is published for Amazon Connect in AWS GovCloud

Salesforce requires FIPS-compliant telephony endpoints before connecting:

> Customers must enable Federal Information Processing Standards (FIPS)-compliant endpoints on their telephony services before connecting to Salesforce.

AWS publishes Amazon Connect FIPS endpoints in three regions, and `us-gov-west-1` is not among them:

| Region | Standard endpoint | FIPS endpoint |
| --- | --- | --- |
| `us-east-1` | Yes | Yes |
| `us-west-2` | Yes | Yes |
| `ca-central-1` | Yes | Yes |
| `us-gov-west-1` | Yes | **None published** |

AWS also states that GovCloud endpoints are not FIPS-validated by default: "If you require FIPS 140-3 compliance you should use the FIPS Endpoints linked in the following section."

Two caveats keep this from being a confirmed blocker. The published endpoint table covers the control plane, and Salesforce's wording does not specify which plane it means. The GovCloud partition is also built for FedRAMP High and DoD Impact Level 5, so Amazon Connect there may satisfy FIPS by design without a separate hostname.

**Ownership.** FIPS configuration is entirely part of the AWS configuration and belongs to the AWS team. Kicksaw's part is the Salesforce side of Voice setup, where the Connect instance is entered as given; the endpoint choice behind it is theirs.

**Recommendation:** pass the question to the AWS team as written here, which endpoints satisfy FIPS 140-3 for both the control plane and the voice media path in `us-gov-west-1` and the Cryptographic Module Validation Program certificate numbers, and record their written answer in the RAID Log. Reason: the claim will reach NCI, so the evidence needs to come from the party that owns the configuration.

### Salesforce chat into Calabrio sits in neither statement of work

On the Calabrio kickoff of 2026-09-14, Mark Hubers raised that chat flowing into Calabrio had appeared in the Calabrio demonstrations but "never became part of the statement of work," and asked whether it is possible and what it costs. A second CIS voice described the current workaround and noted that "chat and phone data has always been separate, which makes forecasting challenging." Trevor Holt took the action.

The gap has no owner:

| Boundary | Status |
| --- | --- |
| Calabrio scope | Third-party application integration explicitly excluded |
| Kicksaw statement of work | A chat feed into Calabrio is not named. The Calabrio row (tracker WF-2) gives Kicksaw a supporting role for Service Cloud data and workflow visibility alongside Calabrio ONE, and the assumptions row (OOS-1) limits that to Service Cloud integration touchpoints |
| Calabrio statement of work | Not present |
| Current owner | Trevor Holt, for feasibility and cost only |

Narrowed on 2026-09-23 against the scope tracker. The feed itself is unnamed in both statements of work, but the Kicksaw statement of work does give Kicksaw a supporting role for Salesforce-side touchpoints. If Calabrio builds the ingestion, the Salesforce-side work to expose chat data may already sit inside that role. That changes who pays for it, not whether an Authorizing Official review applies.

This is the single route by which an AppExchange package could still enter the Government Cloud org. If the answer is a Salesforce-side integration, it triggers an Authorizing Official review, which Salesforce documents as a precondition:

> Before you install an app on your Government Cloud org, ensure that the app meets your organizational requirements. Work with your Authorizing Official (AO) to verify the appropriate list of controls for your organization.

**Recommendation:** treat "no AppExchange packages" as a design constraint to defend, not merely a current fact. Reason: an Authorizing Official review on a federal contract carries lead time that a 24-week engagement under compression pressure cannot absorb.

### The chatbot in scope has no clean delivery route

The scope tracker lists "Live Chat (Chatbot and SMS)" as In Scope (TO-8, channels and numbers). Three routes exist and none is clean:

| Route | Status |
| --- | --- |
| Amazon Connect AI agents | Unavailable in AWS GovCloud |
| Einstein Bots | Interoperable only in Government Cloud Plus: functionally tested, outside the FedRAMP authorization boundary, so use is a risk-based decision for the Authorizing Official |
| Agentforce customer agents | Authorized in Government Cloud Plus, but an AI capability Fred Hutch says needs explicit approval, probably from NIH |

Discovery session 2 recorded the client's position on AI directly: emails carry PHI and diagnoses, and "NIH would not approve of any company like Salesforce training anything on our data." Avi Rabinovitch committed to get Salesforce's position and parked it as not phase one. A scripted, non-generative bot is the least exposed option, and it is still Einstein Bots, which is still outside the boundary.

**Recommendation:** move the chatbot to Needs Decision on the tracker and put two questions to the client: whether a chatbot is required at go-live, and whether the Authorizing Official will accept an Interoperable product. Reason: both routes carry an approval lead time, and neither approval has started.

## What this research settles

### AWS account ownership

The bring-your-own license model answers the question Suchi Panda raised at kickoff: "Is this a new AWS organization that we are going to spin up?" The answer is yes, and Fred Hutch owns it. What remains open is day-to-day administration, not architecture.

The scope tracker agrees and adds the division of labor: Kicksaw provisions the Amazon Connect instance during implementation, and Fred Hutch procures the Salesforce and Amazon Connect licenses (tracker D-5, Amazon Connect instance planning). So the open administration question is about the AWS account itself, identity and billing, not about who builds the Connect instance.

### The partition decision is corroborated

The AWS partition decision (D2, GovCloud `us-gov-west-1`) is confirmed by AWS documentation showing Amazon Connect available in AWS GovCloud (US-West) only. One nuance was not previously recorded: Salesforce defaults new contact centers to AWS commercial regions, and exposing AWS GovCloud as a selectable region may require a Salesforce support case.

### The Calabrio compliance question was misframed

The Calabrio readiness question (Q9, is the Calabrio package Government Cloud ready) rests on the premise that "Calabrio is installed as an AppExchange package." The Calabrio kickoff contradicts that premise:

| Premise in the register | What Calabrio stated |
| --- | --- |
| Installs as an AppExchange package | Third-party application integration is out of scope, and Salesforce is named as falling under that heading |
| Deploys into a Salesforce boundary | Calabrio needs tenant access to its own environment. Users register at `success.calabrio.com` |
| Salesforce-side install | The Smart Desktop Client installs on agent desktops, and CIS performs the installation |
| Integrates with Salesforce | Data comes from Amazon Connect. Single sign-on uses Microsoft Active Directory |

Calabrio deploys into neither Salesforce Government Cloud nor AWS GovCloud. It is Calabrio's own software as a service, outside both.

The scope tracker carries the same conflation in two rows, SC-5 (Government Cloud environment configuration) and CS-1 (compliance and security), both of which read that Calabrio must operate within GovCloud. The proposed rewording is in the tracker section above.

The question that was never asked: can Calabrio's environment, which supports FedRAMP Moderate only, reach Amazon Connect in AWS GovCloud `us-gov-west-1` across the partition boundary, and does the resulting data flow satisfy NCI?

**Recommendation:** correct the closure note on the Calabrio readiness question (Q9) and raise the partition connectivity question with Trevor Holt. Reason: as written, the register reads as though Calabrio package compliance was assessed and dismissed, when the real exposure was never examined.

## Open items

| # | Item | Owner | Blocks |
| --- | --- | --- | --- |
| 1 | FIPS endpoint path for Amazon Connect in `us-gov-west-1`, with certificate numbers | AWS team (Ken Daugherty, Binu Pazhoor). Not Kicksaw's | Compliance evidence for NCI |
| 2 | Contact Lens availability in AWS GovCloud, only if a transcript in the agent console is expected. QM transcription is Calabrio's | AWS team (Ken Daugherty, Binu Pazhoor). Not Kicksaw's | Whether a console transcript can be shown |
| 3 | Confirmation that email is Salesforce Email-to-Case, not Amazon Connect | Avi Rabinovitch with CIS | Channel architecture |
| 4 | Number porting lead time for roughly 10 inbound numbers | AWS team. Not Kicksaw's | Go-live date |
| 5 | Day-to-day administration owner for the Fred Hutch AWS GovCloud organization | Suchi Panda, Mike Griffin | Build start |
| 6 | Whether the Government Cloud org exposes AWS GovCloud as a selectable region | Kicksaw, during Voice setup | Build start |
| 7 | Calabrio connectivity from a FedRAMP Moderate environment into AWS GovCloud | Trevor Holt | Calabrio readiness |
| 8 | Salesforce chat into Calabrio: feasibility, cost, delivery route | Trevor Holt | Whether a package enters the org |
| 9 | Amazon Connect technical detail for Calabrio: addresses, system names, hours, time zone | AWS team, with Kicksaw answering Salesforce questions if asked | Calabrio project plan. Trevor Holt follows up the week of 2026-09-21 |
| 10 | Survey response volume from Oracle, to size the Salesforce purchase | Mark Hubers, blocked on the failed surveys grant | Survey design and procurement |
| 11 | Chatbot: whether it is required at go-live, and whether the Authorizing Official accepts an Interoperable product (tracker TO-8) | Avi Rabinovitch with CIS; Kicksaw for the Government Cloud product status | Chat channel design |

## Licensing quantities remain unreconciled

Three vendors have landed on the same number against a stated agent population of 40 to 45:

| Vendor | Product | Quantity |
| --- | --- | --- |
| Salesforce | Salesforce user licenses | 60 |
| Salesforce | Voice with Partner Telephony | 60 |
| Calabrio | Quality Management | 60 |
| Calabrio | Workforce Management | 60 |

The consistency suggests 60 is a deliberate procurement number rather than an error. It was raised at the Calabrio kickoff and nobody questioned it.

**Recommendation:** confirm the basis for 60 before it becomes a budget conversation. Reason: the question changes from "did a vendor oversell" to "what is 60 based on," and only Fred Hutch can answer it.

## Producing a client-safe version

This document fails the client-safe content test in three places. Removing them produces a version suitable for Fred Hutch:

| Section | Why it is internal |
| --- | --- |
| The AppExchange filter is not evidence | Describes Kicksaw's own research path and a corrected assumption |
| The Calabrio compliance question was misframed | Describes an error in Kicksaw's internal register |
| Licensing quantities remain unreconciled | Raises a commercial question about a partner's sale |

The product findings, the alignment table, and the open items list all cite client-visible sources and can travel as they are.

## Evidence

| Source | Type |
| --- | --- |
| [Kicksaw NCI Service Center Migration SOW 7202026-KS Updated.docx](https://drive.google.com/file/d/1Dt3mlE0QTSltDJC_utDyGtLsIQURlUUK/view), governing | Google Drive, `PSA-SOW` |
| [Kicksaw NCI Service Center Migration SOW 7022026](https://docs.google.com/document/d/1JP0scimahB3evBTgb0pdqE0Kq-FmE--FO57CRPr8DVg/edit), superseded | Google Drive, `Sales Notes` |
| Salesforce Voice for Government Cloud (`ind.government_cloud_service_cloud_voice.htm`) | Salesforce Help |
| Filter for Government Cloud Apps in AppExchange (`ind.government_cloud_filter_government_cloud_apps.htm`) | Salesforce Help |
| Compliance of AppExchange Apps for Government Cloud (`ind.government_cloud_app_exchange_compliance.htm`) | Salesforce Help |
| Choose Your Voice Telephony Model (`service.voice_telephony_models.htm`) | Salesforce Help |
| Turn on Salesforce Voice with Partner Telephony from Amazon Connect (`service.voice_setup_amazon_enable.htm`) | Salesforce Help |
| [Fred Hutch CIS Project Plan + Scope Tracker](https://docs.google.com/spreadsheets/d/1tqBE3dywkXV_XJvXEzY1aa3HvHwSS9EAHdzl_YR2A_k/edit?gid=1999232366#gid=1999232366), Scope Tracker tab, 66 scope rows, read 2026-09-23 | Google Drive |
| Government Cloud Available Products and Features (`000396813`), publish date 2026-09-16 | Salesforce Knowledge |
| Amazon Connect in AWS GovCloud (US) | AWS GovCloud User Guide |
| Amazon Connect endpoints and quotas | AWS General Reference |
| Service Endpoints, AWS GovCloud (US) | AWS GovCloud User Guide |
| Contact Lens general availability in AWS GovCloud (US-West), July 1, 2025 | AWS announcement |
| Government Cloud org `00Dcs00000LoZ05EAF` | Direct query, 2026-09-21 |
| Calabrio kickoff, 2026-09-14 | Client call transcript |
| Discovery session 1, 2026-09-15 | Client call transcript |
| Discovery session 2, 2026-09-17 | Client call transcript |
| NCI CIS migration kickoff, 2026-09-08 | Client call transcript |

## Change log

| Date | Change |
| --- | --- |
| 2026-09-21 | Created. Telephony model confirmed as bring-your-own Amazon Connect from the org license. Four misalignments recorded. Calabrio readiness question (Q9) identified as misframed |
| 2026-09-23 | Added the governing statement of work link, resolved against Google Drive, with the superseded July 2 version named alongside it. Recorded that the July 20 filename does not confirm signature status |
| 2026-09-23 | Read the scope tracker against every finding. Narrowed the Calabrio chat finding (the Kicksaw statement of work gives Kicksaw a supporting role, tracker WF-2). Corrected the outbound campaigns row (CIS places outbound calls). Added a fifth misalignment, the chatbot delivery route, with Einstein Bots Interoperable only in Government Cloud Plus. Added proposed tracker updates and open item 11 |
| 2026-09-23 | Recorded the ownership boundary set by Ben Bolding: the AWS team owns all AWS configuration, security, questions and discovery; FIPS is AWS's; transcription is Calabrio's; Kicksaw answers Salesforce questions on request. Added an Owner column to the summary, reframed the transcription and FIPS findings around what is left for Kicksaw, and reassigned open items 1, 2, 4 and 9 |

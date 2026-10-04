# Pre-sandbox build tasks: Government Cloud production org

Internal Kicksaw working document. Written for Ian Devlin ahead of the 2026-09-24 build review with Ben Bolding. Nothing here has been applied to the org.

## The approach

The production org (`00Dcs00000LoZ05EAF`, alias `FredHutch-GovCloud`) is greenfield and has no sandbox. Org-wide settings and feature enablement go into production first, so every sandbox created afterwards starts from them. Objects, fields, automation and pages get built in a sandbox and deployed, so the deployment path is proven before the build ramps up.

Some configuration does not copy into a sandbox, or copies switched off. The "Copies" column marks it.

| Copies | Meaning |
| --- | --- |
| Y | Build once in production; every sandbox inherits it |
| Redo | Copies switched off or not at all; set up again in each org |
| n/a | Not org configuration: a decision, a request or a document |

Sizes are T-shirt sizes (XS, S, M, L). No hours, matching Jira.

## Pre-flight

| Check | State |
| --- | --- |
| Kicksaw configures production directly | Cleared. Fred Hutch goes with Kicksaw's recommendation; no separate approval needed (Ben Bolding, 2026-09-24) |
| Sandbox allowance | Confirmed in Setup, Sandboxes. Unlimited Edition includes 100 Developer, 5 Developer Pro, 1 Partial Copy and 1 Full. Government Cloud sandboxes land on a Government Cloud sandbox server and sign in through the sandbox My Domain |
| Before-state | The org state table below. The org is empty, so there is little else to capture |

## Org state today

Queried read-only on 2026-09-23 and 2026-09-24. This is the before-state for rollback.

| Area | State |
| --- | --- |
| Time zone and default business hours | America/Los_Angeles. CIS works 9 AM to 9 PM ET |
| Holidays | 0 |
| Languages | `en_US` only. Translation Workbench off |
| Security | Session timeout 2 hours, 8-character passwords, 90-day expiry, lockout after 10 attempts, no single sign-on |
| Users | 10 of 60 Salesforce licenses used. All 9 Fred Hutch and Kicksaw users are System Administrators, Tom Kluge included |
| Permission set groups | 9, all Salesforce defaults |
| Service Cloud | Omni-Channel on, skills-based routing off. Email-to-Case on, no routing addresses. Lightning Knowledge on, `en_US` only. Surveys off. One queue, "Q1" |
| Voice | 60 Salesforce Voice User (Partner Telephony) licenses, 0 used. No contact center |
| Messaging | 90 Enhanced Chat User, 30 Messaging User and 30 Partner Messaging User licenses, 0 used. No channels |

## 1. Org foundation

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Set the org default time zone to America/New_York | Every sandbox and every new user inherits it; reports and SLAs read in it | None | Y | Ian | XS |
| Set default business hours to 9 AM to 9 PM ET | Omni-Channel, case age and reports read business hours | Operating days (weekends, early closes) confirmed by Holly Fernandez-Johnson | Y | Ian | XS |
| Load CIS holidays | Same as business hours | The Oracle holidays menu from the metadata pull is the starting list; CIS confirms it is current | Y (inferred) | Ian | XS |
| Turn on Translation Workbench and add Spanish | Spanish surveys, Spanish messaging components and Enhanced Chat labels cannot be translated without it, and it translates data category labels. It can be turned off again. It does not translate Knowledge articles, Quick Text or email templates | None | Y (inferred: it is a metadata setting) | Ian | XS |
| Write naming conventions. Adopt Oracle's names for fields, menus, queues and statuses wherever they meet our standards, so specialists see familiar terms. Our standards still govern API names, required descriptions and help text, and no sensitive data in Amazon Connect resource names | Everything built afterwards follows it | The Oracle data dictionary and picklist list from the metadata pull | n/a | Ben, Ian | S |

## 2. Security baseline (FedRAMP Moderate)

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Get NCI's control values (Mike Griffin), and Oracle production's IP restriction and login hours settings (Mark Hubers) | NCI's values override ours. FedRAMP Moderate governs everything else; Oracle is a starting point only where Moderate sets no value | None | n/a | Ben to request | S |
| Apply the security baseline: 15-minute session timeout with forced logout; passwords 15 characters minimum, no composition rules, never expire; lockout after 5 attempts for 30 minutes | Security settings copy into every sandbox; set once, no gap between orgs. Values and reasons in the [security baseline](security-baseline-fedramp-moderate-2026-09-24.md). Adjust later if NCI's values differ | Ben's go on the baseline | Y | Ian | S |
| Turn on passkeys and security keys as the verification methods, and have every user register one | FedRAMP Moderate asks for phishing-resistant multi-factor authentication. Salesforce Authenticator is not authorized in Government Cloud Plus. Single sign-on is not in the SOW, so this is how specialists sign in | None | Y (setting); users register per org | Ian | S |
| Decide on Shield Event Monitoring | Native logs do not record data access, and setup and login history last only 6 months against 12 months retrievable | Licensing, through Mitchell Rabin; Fred Hutch budget | n/a | Ben | XS |
| Reduce System Administrator assignments to named admins | All 9 users are System Administrators. Users copy into sandboxes, so the excess copies too | Admin boundary (B-02) | Y | Ben, Ian | S |

## 3. Service Cloud features

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Turn on Knowledge multiple languages and add Spanish | About 5,000 English and Spanish articles migrate, and the SOW calls for "linkage between the common articles." **One-way:** once on, Knowledge cannot go back to one language, and an added language can be deactivated but never removed. **Hold** until the client confirms the Spanish code | Which Spanish code the articles use (es, es_MX or es_US; es_US has no Salesforce-supplied screens), and whether every Spanish article is a translation of an English one | Y | Ian, on Ben's go | S |
| Data category group skeleton, top level only | Article visibility and the Knowledge migration map onto it | Taxonomy agreed with Melissa's knowledge team. **Hold until then** | Y | Ian | M |
| Decide on skills-based routing | English and Spanish routing is the likely reason to turn it on | Routing design | Y | Ben | XS |
| Turn on Salesforce Surveys | Embedded surveys are in scope and Surveys is off | Confirm Salesforce Surveys is the survey tool | Y | Ian | XS |

## 4. Voice (Salesforce Voice with Partner Telephony, bring-your-own Amazon Connect)

The AWS team owns every AWS-side step. Kicksaw builds the Salesforce side.

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Check that the Partner Telephony contact center setup lists the AWS GovCloud region; if not, open a support case (B-30) | A support case has lead time, and Voice cannot start without it | None | n/a | Ian | XS |
| Give the AWS team Salesforce's requirements: an instance set up for SAML logins, the GovCloud IAM policy with account `383319876315`, and the existing storage bucket, contact record stream, video stream and Contact Lens stream | AWS is building the instance now. Salesforce Help: "supports Amazon Connect instances of type SAML only" | None | n/a | Ben | XS |
| Create the Partner Telephony contact center in production | Production is the only org with an AWS account today | AWS instance ID and IAM role ARN | **Redo** | Ian | M |
| Decide which sandbox, if any, gets Voice | Each Voice sandbox needs "an AWS Account that's solely dedicated to the new sandbox org". That is a Fred Hutch and AWS cost | Fred Hutch, AWS team | n/a | Ben | S |
| Voice number porting and the phone number quota increase | AWS says to open porting "several months before pending go-live dates"; the default is 10 numbers per instance, and AWS notes an older account's default may be lower, against about 10 inbound numbers, which leaves no headroom | AWS team | n/a | AWS team | n/a |

## 5. Digital engagement

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Decide the chat entry (B-23). Recommendation: Salesforce Enhanced Chat | Decides which channel gets built | Ben's sign-off | n/a | Ben | n/a |
| Turn on Messaging in production | Channels build on it. Messaging starts off in a sandbox; turning it on there copies channels in switched off | None | Redo | Ian | XS |
| Build the Enhanced Chat channel and deployment | Enhanced Chat runs only on four server groups (USA9014, USA9026, USA9016s, USA9018s). Production is on USA9014; a sandbox may need a support case to land on one | B-23, a cancer.gov web team contact | Redo | Ian | M |
| Request the production SMS number | Longest lead item. Toll-free: 3 to 5 business days to assign, then 1 to 2 weeks after verification. Registration likely needs NCI's legal name and EIN (verified for AWS, inferred for Salesforce) | NCI details, through Mike Griffin | Redo: a number belongs to one org, so a sandbox needs its own | Ben | S |
| Check the Messaging license count | 30 Messaging User licenses against 40 to 45 agents. If every specialist handles SMS, 30 is short (inferred). Question for Mitchell Rabin | None | n/a | Ben | XS |

## 6. Access model skeleton

Shells only, so every sandbox shares the same names. Contents get built in the sandbox.

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Persona list: English specialist, bilingual specialist, supervisor, CIS administrator, knowledge editor, Kicksaw build | Everything in the access model hangs off it | Admin boundary (B-02) for the CIS administrator persona | n/a | Ben | S |
| One permission set group per persona, with the Service, Voice and Messaging licenses mapped | Users are assigned by group from day one | Persona list | Y | Ian | M |
| Service Console app shell | Every record page and utility gets built into it | None | Y | Ian | S |

## 7. DevOps baseline

| Task | Why before the sandbox | Depends on | Copies | Owner | Size |
| --- | --- | --- | --- | --- | --- |
| Tailor `manifest/package.xml` to settings, permission set groups, apps, Knowledge and Omni-Channel | It is still the stock code-only manifest | None | n/a | Ian | S |
| Retrieve into `force-app/` and commit once the foundation is in | The starting point for source tracking and the sandbox pipeline | The manifest | n/a | Ian, Ben | S |
| Sandbox plan. Recommendation: a Developer Pro sandbox for build now, the Full sandbox later for SIT, UAT and Knowledge migration testing, one Voice sandbox at most | Salesforce recommends a full-copy sandbox for Knowledge migration testing; each Voice sandbox costs an AWS account | Voice sandbox decision | n/a | Ben, Ian | S |
| Choose the deployment tooling from sandbox to production | Every change after the foundation goes through it | Sandbox plan | n/a | Ben, Ian | S |

## Set up again in every org

| Item | What happens in a sandbox |
| --- | --- |
| Voice contact center | Not copied. Rebuilt with its own dedicated AWS account |
| Messaging channels | Copied switched off, after Messaging is turned on. SMS channels do not move |
| SMS numbers | One org at a time. The sandbox needs its own |
| Email-to-Case routing addresses | Reset. Regenerated per org |
| Users | Copied. Emails get `.invalid` appended; email deliverability defaults to system email only |
| Knowledge articles | Only in Partial Copy and Full sandboxes (inferred: articles are records) |

## Build in the sandbox, not in production

Case record types and fields, the SCIF child object, queues, flows, record pages, Quick Text, email templates and Email-to-Case routing. From the security baseline: the login banner flow and the 90-day inactive-user deactivation flow. Built in the sandbox and deployed, so the deployment path gets tested on real changes.

## Rollback

The org is empty and the work is additive. To reverse a setting, set it back to the value in the org state table; to reverse an added component, delete it.

The one exception is a feature that cannot be turned off once on. Knowledge multiple languages is confirmed one-way. Check Salesforce Help before turning on Messaging, Surveys or the Voice contact center; anything one-way goes ahead on Ben's go.

## For the call

1. Walk the seven areas and agree owners and sizes.
2. Agree the sandbox plan and the Voice sandbox question.
3. After review, Ben says go on Jira tickets for the agreed tasks. T-shirt sizes, no hours.

## Sources

| Claim | Source |
| --- | --- |
| Voice contact centers not copied; a dedicated AWS account per sandbox | [Salesforce Help: Voice sandbox guidelines](https://help.salesforce.com/s/articleView?id=service.voice_sandbox_guidelines.htm) |
| SAML instance only; setup inputs; existing streams reused | [Salesforce Help: existing Amazon Connect setup](https://help.salesforce.com/s/articleView?id=service.voice_existing_byoa_auto.htm) |
| GovCloud IAM policy and account `383319876315` | [Salesforce Help: Voice roles and policies](https://help.salesforce.com/s/articleView?id=service.voice_amazon_reference_roles_policies.htm) |
| Messaging off in sandboxes; channels copied switched off; SMS channels don't move | [Salesforce Help: Messaging sandbox data](https://help.salesforce.com/s/articleView?id=service.messaging_sandbox_data.htm) |
| Separate SMS numbers per org | [Salesforce Help: test SMS](https://help.salesforce.com/s/articleView?id=service.messaging_test_sms.htm) |
| Sandbox allowance by edition | [Salesforce Help: sandbox environments](https://help.salesforce.com/s/articleView?id=platform.data_sandbox_environments.htm) |
| Government Cloud sandbox server and My Domain | [Salesforce Help 000313753](https://help.salesforce.com/s/articleView?id=000313753) |
| User emails get `.invalid` | [Salesforce Help 000386507](https://help.salesforce.com/s/articleView?id=000386507) |
| Full-copy sandbox for Knowledge migration testing | [Salesforce Help: Knowledge migration plan](https://help.salesforce.com/s/articleView?id=service.knowledge_migration_tool_plan.htm) |
| Org state and licenses | Read-only queries against `FredHutch-GovCloud`, 2026-09-23 and 2026-09-24 |
| B-02, B-03, B-23, B-30 | [Session 3 discovery guide](../discovery/discovery-guide-session-3-2026-09-22.md) |

## Change log

| Date | Change |
| --- | --- |
| 2026-09-24 | Created for the build review with Ian Devlin |
| 2026-09-24 | Translation Workbench on before the sandbox; Knowledge multiple languages held as one-way; naming follows Oracle where it meets our standards; single sign-on removed as outside the SOW; security rows rebuilt on the FedRAMP Moderate baseline, which governs over Oracle's current settings |
| 2026-09-24 | Production approval cleared and sandbox allowance confirmed. Dropped the metadata baseline and Health Check as pre-flight steps; rollback now reverts to the recorded org state |
| 2026-09-24 | Corrected the Amazon Connect phone number quota from 5 to 10 per instance, checked against the AWS service quotas page |

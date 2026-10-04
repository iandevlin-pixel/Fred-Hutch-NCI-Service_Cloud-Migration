# Salesforce Voice and Amazon Connect setup: where the web outline falls short

> **Frozen 2026-09-29.** Published to the Notion Project Library as [Salesforce Voice and Amazon Connect setup](https://app.notion.com/p/3ead4b877417813e8ef1efe7ca66d9bb). The Notion page is the live copy; edit there, not here. The "Documents to update" section below stayed local and is not on the Notion page.

- **Date:** 2026-09-28
- **Author:** Ben Bolding, with assistant research
- **Handling:** internal Kicksaw working document. It describes what Kicksaw has and has not done before, so it fails the client-safe test as a whole. The environment, voicemail and phone number findings cite only official documentation and can travel on their own
- **Purpose:** grade a web-sourced setup outline for Service Cloud Voice with Amazon Connect against official Salesforce and AWS documentation for this engagement's model, and list what the outline misses before Kicksaw builds the Amazon Connect side. Also the prep for the 2026-09-29 knowledge transfer with Jason

## Kicksaw now builds the Amazon Connect side

The ownership boundary of 2026-09-23 had the AWS team doing all AWS configuration. That no longer holds for the Connect build.

| Source | What it says |
| --- | --- |
| Governing SOW (July 20), Salesforce and Amazon Connect configuration phase | "This phase also includes replacing Cisco Finesse with Amazon Connect. This effort involves setting up inbound and outbound call functionalities, IVR, and multi-language telephony support. It will include configuring call routing, voicemail, and callbacks while integrating these features seamlessly into Salesforce." |
| Governing SOW, assumptions | "Fred Hutch will allow Kicksaw to provision the Amazon Connect instance during the Implementation phase" |
| Draft RACI from the 2026-09-24 GovCloud discussion | Fred Hutch's cloud team owns the GovCloud accounts, landing zone guardrails, audit logging and security monitoring. Kicksaw is Responsible for creating the Connect instances, instance storage, contact flows, queues, routing profiles, skills and callbacks |
| Slack, 2026-09-24 and 2026-09-28 | Kicksaw builds the call flows "same as usual for a SCV project". Sarah Tirey raised the Amazon Connect knowledge gap as a risk and booked Jason for 2026-09-29 |

The SOW is silent on AWS accounts, number porting and FIPS, which is consistent with the RACI giving those to Fred Hutch.

## Summary

The web outline describes the commercial setup, where Salesforce provisions everything in one account per org. Two decisions are now settled, and five items remain open.

**Decided, Ben Bolding, 2026-09-28:**

| Decision | Detail |
| --- | --- |
| Two AWS accounts | One for the non-production contact center paired with the Salesforce Full sandbox, one for production paired with Salesforce production |
| Voice lives in the Full sandbox | The Full sandbox holds Voice, and likely the whole build, because the contact center, its routing maps, phone channel and users are rebuilt per org rather than deployed |

**Open:**

| # | Item | Why it matters | Severity | Owner | Next step |
| --- | --- | --- | --- | --- | --- |
| 1 | Salesforce's voicemail captures messages with live media streaming, which AWS GovCloud does not offer | Voicemail is SOW scope. Calls, call recording and Contact Lens transcription are not affected | High | Kicksaw | Choose a voicemail design with Jason; ask Salesforce whether it has a GovCloud path |
| 2 | Phone number porting: 30-day filing window, a wet-signed authorization that must match Verizon's records exactly, default quotas at 10 | Sets the go-live critical path | High | Fred Hutch with AWS Support, Kicksaw supporting | Identify the account holder of record for each number |
| 3 | Moving the AWS configuration from the sandbox account to production is partly import (flows) and partly rebuild (everything else) | Sets the build approach and the effort estimate | Medium | Kicksaw | Agree the approach with Jason |
| 4 | Kicksaw's documented Amazon Connect experience is commercial and Salesforce-provisioned only | Bring-your-own, GovCloud, porting and a bilingual IVR are new ground | High | Hannah Oanca, Sahil Kumar | Settle Jason's role on 2026-09-29 |
| 5 | The GovCloud region has to appear in Salesforce's contact center setup | If it doesn't, setup stops until Salesforce Support enables it | Low | Kicksaw (Ian Devlin) | Look at the region list the first time Voice is set up in the Full sandbox |

One earlier finding reverses. AWS's FIPS page, last updated 2026-09-28, lists `connect.us-gov-west-1.amazonaws.com` as the Amazon Connect FIPS endpoint in the GovCloud column. The FIPS gap recorded in the 2026-09-21 alignment document is resolved for the API endpoint. FIPS on the voice media path is still the AWS team's to confirm.

## How the pieces fit

The setup runs in four hands, in this order:

1. **Fred Hutch cloud team** creates the two GovCloud accounts. Each GovCloud account needs a paired standard account. They apply guardrails and logging, and grant Kicksaw console access.
2. **Kicksaw, in each AWS account,** creates an IAM role named exactly `ProvisioningRole`. It uses Salesforce's `SCVGovProvisioningPolicy.json` and trusts Salesforce's GovCloud account `383319876315`.
3. **Kicksaw, in each Salesforce org,** turns on Omni-Channel and the Identity Provider, turns on Salesforce Voice from **Partner Telephony Setup**, then creates the contact center. The recommended option is **(Recommended) Create an Amazon Connect Instance**. The inputs are the GovCloud region and the role ARN.
4. **Salesforce, using that role,** deploys into the AWS account:
   - two CloudFormation stacks, one account-level and one for the contact center
   - the Connect instance, set up for SAML
   - the `SalesforceServiceVoiceIdp` identity provider
   - the integration Lambdas, including `InvokeTelephonyIntegrationApiFunction`
   - the `CTRStream` and `ContactLensStream` Kinesis streams
   - S3 buckets for recordings and CloudTrail
   - secrets and keys
   - approved origins (inferred from the policy and Salesforce's stack)
   - the "Sample SCV" contact flows

After that, Kicksaw builds the working contact center:

- contact flows, prompts, hours, queues and routing profiles
- voicemail and callbacks
- users added to the contact center
- queue routing maps and the phone channel in Salesforce
- quota increases and phone numbers

Kicksaw's own step is the Salesforce contact center, which creates the instance, not the instance built by hand in the AWS console. The existing-instance path also requires a Kinesis video stream, which GovCloud cannot feed. The RACI row "Create the dev/test and production Connect instances" should read that way.

## The outline, step by step

| Outline step | Verdict | What holds for this engagement |
| --- | --- | --- |
| Enable My Domain | Correct, already done | `fredhutchnci.my.salesforce.com` is deployed. Not on Salesforce's Voice prerequisites page |
| Enable Identity Provider | Correct | Required before turning on Voice. Salesforce warns: "If you enable the Identity Provider, you cannot disable the Identity Provider." One-way, so it waits on Ben's go in production. This is Salesforce signing agents into Amazon Connect, not the user-login SSO removed from scope on 2026-09-24 |
| Enable Omni-Channel | Correct | "Before you can turn on Voice, enable Omni-Channel" |
| "Service Cloud Voice Settings", toggle Turn On Voice | Wrong page | The license exposes **Partner Telephony Setup** with **Turn On Salesforce Voice** |
| Assign "Service Cloud Voice with Partner Telephony" permission set | Wrong name | The org holds three, queried 2026-09-28: `ContactCenterAdminExternalTelephony` (Admin), `ContactCenterAgentExternalTelephony` (Rep) and `ContactCenterSupervisorExternalTelephony` (Supervisor), all on the 60-seat Partner Telephony license, 0 used |
| IAM cross-account role for the "Contact Center Health Check Stack" | Partly correct | The role lets Salesforce build the whole contact center. A health check stack exists but is only a diagnostic. GovCloud uses its own policy file and trust account |
| Setup, **Amazon Contact Centers**, "Use Your Own AWS Account (BYOA)", enter AWS Account ID and role ARN | Partly correct | The page is **Partner Telephony Contact Centers**. There is no BYOA option and no account ID field. The choice is create new (recommended) or use existing, and the inputs are region, role ARN and an optional external ID |
| CloudFormation or Serverless Application Repository package provisions instance, streams and Lambdas | Partly correct | CloudFormation, yes. No evidence of Serverless Application Repository |
| Download key pair, certificate or XML call center definition | Wrong for this path | The XML file belongs only to the manual path. The key pair expires yearly and is rotated in place with **Update Key** |
| Add the sandbox domain to Approved Origins by hand | Probably unnecessary | Salesforce's policy grants `connect:AssociateApprovedOrigin` and its stack declares the My Domain and Lightning domains. Check after setup; do not plan on it |
| Inbound flow calls `InvokeTelephonyIntegrationApiFunction` with `methodName` `createVoiceCall` | Correct | The auto-installed "Sample SCV Inbound Flow" already does it. Kicksaw's notes add an 8-second timeout and one retry for a cold Lambda |
| Production: repeat the steps, both instances in one AWS account | Wrong | Salesforce requires one AWS account per org. Decided: two accounts |
| Change sets or DevOps Center for contact center metadata, queues, presence statuses and routing configurations | Partly correct | Omni-Channel metadata deploys. The contact center does not. DevOps Center is "Interoperable (Not Authorized)" in Government Cloud Plus |

## Decided: two AWS accounts

Salesforce's sandbox guidelines name this model explicitly:

> Each org should point to an AWS Account that's solely dedicated to that org. Don't share the AWS Account between orgs.
>
> For Salesforce Voice with Partner Telephony from Amazon Connect, you must create an AWS Account that's solely dedicated to the new sandbox org and completely separate from the production org and its AWS Account.
>
> While it's possible for multiple orgs to share the same AWS Account, you'll lose the auto-provisioning benefits.

The mechanics explain why:

- The role name is fixed.
- The external ID works only when the account backs no other contact center.
- The account-level stack creates one identity provider and one CloudTrail per account.
- AWS's default is two Connect instances per Region per account.

AWS Well-Architected also says account-level separation "is strongly recommended for isolating production workloads from development and test workloads."

The draft RACI's "one workload account holding both Connect instances" needs revising before Fred Hutch creates accounts (Order of Work step 3). With paired standard accounts, that is four AWS accounts in total.

## Decided: Voice lives in the Full sandbox

The contact center, its user membership, the phone channel and the queue routing maps are rebuilt in each org rather than deployed. Building Voice in the Full sandbox, and likely the rest of the build with it, keeps that rebuild to once before production.

Three consequences to plan around:

- **Refresh breaks the pairing.** A refresh leaves the Full sandbox without its contact center. Re-pairing follows Salesforce's sandbox refresh procedure, and Kicksaw's Sandbox Refreshes guide covers the same ground. The Full sandbox should not be refreshed between Voice setup and the end of UAT.
- **Non-Voice metadata still deploys to production.** Case fields, flows and pages go from the Full sandbox to production, so the deployment path gets exercised before go-live.
- **UAT runs in the build org.** Build changes need to pause while the business tests.

This revises the Developer Pro recommendation in the pre-sandbox build tasks.

## Open 1: Salesforce's voicemail uses live media streaming

**What live media streaming is.** It is an optional Amazon Connect feature that copies a caller's audio, in real time, into Kinesis Video Streams, so that a separate program can process it while the call is running. Calls themselves don't use it. The audio goes between the caller, Amazon Connect and the agent's softphone. Call recording doesn't use it either: Amazon Connect records to its own S3 bucket. On both of those, AWS carries the audio and Salesforce never does.

AWS's GovCloud page lists "Live media streaming" among the features Amazon Connect does not offer in GovCloud.

**What in Salesforce's package depends on it:**

| Feature | Evidence | Read |
| --- | --- | --- |
| Voicemail, Salesforce native | Salesforce's published "Sample SCV Voicemail Subflow" contains `UpdateContactMediaStreamingBehavior` blocks that turn media streaming on (shown as **Start media streaming** in the flow designer) to capture the message. `VoiceMailAudioProcessingFunction` then "Gets the voicemail recordings from Amazon Kinesis... Converts the chunks of recordings into a WAV file" | Does not work in GovCloud as shipped (verified from the flow and the AWS list) |
| Real-time transcription through Amazon Transcribe | Salesforce's stack describes `kvsTranscriber` as sending "transcription data based on the amazon connect's video stream" | Unavailable in GovCloud (inferred) |
| Real-time transcription through Contact Lens | Contact Lens real-time and post-call analytics are available in GovCloud for US English and US Spanish, and use a Kinesis data stream, not media streaming | Works. This is the route to a transcript in the agent console, if one is wanted |

**Voicemail routes that avoid media streaming:**

- **Voicemail Express version 3,** AWS's supported solution. It changed to Amazon Connect's built-in IVR recording, "With the change from KVS, all solution components are now available in GovCloud." It removed its Salesforce options and delivers voicemail as Amazon Connect tasks or email. Getting the message into Salesforce as a VoiceCall or Case is Kicksaw build work.
- **Salesforce's voicemail with the capture step changed** to IVR recording. This is unsupported, and Salesforce's contact center updates overwrite customized Lambdas.
- **A Salesforce GovCloud path,** if Salesforce has one. The Government Cloud Voice article does not mention voicemail.

Kicksaw's Notion says Voicemail Express is sunset. That refers to the Salesforce-specific version 2, which is archived, not to version 3.

**Recommendation:** ask Salesforce first, then design around Voicemail Express version 3 if Salesforce has no GovCloud path. Reason: it is the only documented GovCloud voicemail, and the remaining work, delivering into Salesforce, uses the standard REST API Lambda Kicksaw already knows.

## Open 2: phone numbers and what porting involves

### Today's phone stack

The current telephony is Cisco and Verizon, and Amazon Connect replaces it outright. It is a competing product, not an overlapping one.

| Piece | Today | After go-live |
| --- | --- | --- |
| Agent phone | Cisco Jabber softphone for answer, hold and resume, separate from Oracle (session 1, 2026-09-15). The SOW names Cisco Finesse, Cisco's agent desktop, for "inbound and outbound calls, voicemail, chat, and call transfer" | Amazon Connect softphone inside the Salesforce console |
| Routing | "A Cisco routing system delivers to the least skilled available agent" across five skill groups (reverse demo, 2025-07-29) | Amazon Connect routing profiles and queues |
| IVRs | Four IVRs, "all Verizon-owned and operated," all asking English or Spanish first (reverse demo) | Amazon Connect contact flows |
| Carrier and circuit | A Verizon-owned router on campus is the demarcation point (the reverse demo transcript says "DMARC," most likely a mishearing of "demarc"). The stack moved into a FedRAMP environment around July 2025 | Amazon Connect is the carrier; numbers ported from Verizon |
| Real-time reporting | Cisco Unified Intelligence Center, 15-second refresh | Salesforce and Amazon Connect reporting |
| AWS | None for the call center. Mark Hubers: "Hutch has AWS in use... but the needs of a call center for the live audio are a little bit different than general research" (reverse demo). The draft RACI extends Fred Hutch's existing commercial landing zone into GovCloud | New GovCloud accounts, greenfield (confirmed 2026-09-21) |

### What porting is

Porting moves a phone number from one carrier (Verizon, the "losing carrier") to another (Amazon Connect's carrier), so callers keep dialing the same numbers. The numbers in scope are 1-800-4-CANCER, the Federal quit line, the VA line and the CCR line. The public numbers are 1-800-4-CANCER, 1-877-44U-QUIT and 1-855-QUIT-VET per cancer.gov. The authoritative list, about 10 numbers in all, comes from CIS.

### The steps, per AWS

| Step | What happens | Who |
| --- | --- | --- |
| 1. Open a support case | Service **Connect (Number Management)**, category **Number Porting North America**. Include the production instance ARN, the numbers, the exact flow name for each, the port date and time, the current carrier, and the contact authorized to change the phone service. One case per losing carrier | Fred Hutch's AWS account owner, with Kicksaw supplying the ARN and flow names |
| 2. Complete the Letter of Authorization | AWS sends the letter. Company name, address and contact "must match what is on the current carrier's CSR" (Customer Service Record) exactly. Needs "a traditional handwritten signature," dated within 15 days. Up to 10 toll-free numbers per letter, with a spreadsheet beyond that | The account holder of record with Verizon |
| 3. Upload documents | Through a secure S3 link AWS sends, which expires after 10 days. Include the CSR or latest phone bill | Fred Hutch |
| 4. Carriers validate | Verizon and AWS's carrier check the letter against the CSR and agree a port date and time. Any mismatch means a new letter | AWS and the carriers |
| 5. Pre-port setup | About three to four days before, AWS loads the numbers into the production instance. Attach each to its flow, and file quota increases at least five days before | Kicksaw |
| 6. Port day | Weekday business hours only. Confirm traffic stops on Verizon, place test calls, keep agents logged in. Routes can take hours to settle across carriers | Kicksaw, CIS, AWS |

Three timing rules:

- US porting requests "cannot be submitted with more than 30 days notification."
- Ports take "two to four weeks... after phone number portability has been verified."
- AWS stops work on a request if the requester takes longer than 30 days to respond.

### What Fred Hutch has to supply

- **The account holder of record for each number.** The letter must match Verizon's records exactly, so if a number is in NCI's name, NCI signs. Nobody has confirmed who holds 1-800-4-CANCER.
- **A Customer Service Record or recent bill** from Verizon for each account.
- **A target port date**, a weekday, agreed with the go-live plan.

### Around the port

- **GovCloud eligibility.** AWS's telecoms coverage guide lists US DID and toll-free as "All regions," and one AWS page reads ambiguously about GovCloud. Porting into GovCloud is likely supported; the AWS team should confirm it.
- **Test numbers.** The sandbox instance claims its own new numbers for testing, which AWS recommends before any port. Production numbers port straight to the production instance and never pass through the sandbox.
- **Quotas.** The defaults are 10 phone numbers, 10 concurrent calls and 100 flows per instance, against about 10 numbers and 40 to 45 agents. Increases can take up to three weeks and can only be requested once the instance exists.
- **E911.** 911 works from the agent softphone by default in GovCloud. AWS's remote-agent address pattern stores addresses in Customer Profiles and validates them through a Chime service, and neither is available in GovCloud. Remote-agent E911 needs its own design (RACI open question 6).
- **Rollback.** AWS documents no fast rollback after a port. The cutover plan needs one agreed with Verizon and AWS Support before the port date.

## Open 3: moving the AWS configuration from the sandbox account to production

Amazon Connect has no whole-instance export. What moves depends on the object.

| Object | How it gets to production |
| --- | --- |
| Contact flows and flow modules | **Import.** Export each as JSON from the sandbox instance (**Save**, **Export flow**), then import into a new flow of the same type in production |
| Queues, hours of operation, routing profiles, prompts, quick connects, security profiles, agent statuses | **Rebuild.** No console import. Recreate by hand, or by script through the Connect API or CloudFormation |
| Phone numbers | **Ported** straight to production. Never moved from the sandbox account |
| Users | **Added** from Salesforce production through the contact center |
| Salesforce's Lambdas, streams, buckets and sample flows | **Created automatically** when the production contact center is set up |

How flow import resolves references:

- It looks up each queue, prompt, hours of operation and flow by ARN, then by name. Because the ARNs differ between accounts, it matches on name. When production has objects with identical names, the references reconnect by themselves.
- A flow will not publish while a required reference is unresolved. Supporting objects therefore go in first.
- Lambda references need re-pointing by hand. Kicksaw's experience is that Lambda blocks error on import and are easiest deleted and re-added.
- Flow import is "currently in Beta status." Each flow must stay under 200 blocks and 1 MB.

**Recommendation (Simple):**

1. Recreate the supporting objects in production by hand from a checklist, with names identical to the sandbox.
2. Import the flows, subflows before the main flows.
3. Re-point the Lambda blocks and publish.

Reason: CIS has five skill groups and four IVRs, so the supporting objects number in the tens, and a checklist is faster than building and testing a script.

**Comprehensive, if wanted:** script the export and recreation through the Connect API, keeping the JSON in this repo. It repays itself only if production is rebuilt more than once. Kicksaw should skip AWS's `amazon-connect-copy` sample either way. It hard-codes the commercial `arn:aws:` partition and was last updated in 2023.

Production build order:

1. Production account ready; request quota increases.
2. Create the production contact center from Salesforce production.
3. Deploy the Omni-Channel metadata.
4. Recreate the supporting objects in production: prompts, hours, queues, routing profiles, quick connects.
5. Import the flows, re-point the Lambdas and publish.
6. Add users, security profiles, routing maps and the phone channel.
7. Claim a test number and run end-to-end tests.
8. File the port request within the 30-day window, then verify each number's flow and outbound caller ID after the port.

## Open 4: what Kicksaw's playbook offers

Kicksaw's Notion comes from commercial, Salesforce-provisioned builds between 2022 and 2024, and much of it still applies. The following is useful here even though none of it covers bring-your-own or GovCloud.

| Item | What it gives this build | Where |
| --- | --- | --- |
| Importable sample flows | `createVoiceCall` with an 8-second timeout and one retry for a cold Lambda; REST API query and update; a customer queue flow with a 2-minute break-out | [Jason's SCV Scratch Page](https://app.notion.com/p/bc4178ec998c4e1a92d33f65c06d8b4d) |
| Inbound flow pattern and routing setup | Intro (logging, recording, `createVoiceCall`), then IVR, then transfer. One routing profile per unique queue combination, named `R-Persona-QueueAbbrevs`. Presence status mapping and the Salesforce-to-Connect queue mapping | [SCV02 routing write-up](https://app.notion.com/p/561ae394d2c44dc98ca18230427a9433) |
| REST API Lambda authentication | Key and certificate steps. The subject goes in Parameter Store, not a Lambda environment variable as Salesforce's docs say. Username or email for the subject is unsettled; ask Jason | [SCV01 write-up](https://app.notion.com/p/30e1aaf2090d454e980712f544795f80) |
| Lessons from a production audit | Create the VoiceCall at the front of the flow, or abandoned calls miss reporting. Keep business logic out of Lambdas and use a post-call Salesforce flow. Voice hard-codes a 20-second ring timeout, so secondary-queue delays under 60 seconds reach only one agent. Unmapped queues break routing and Omni Supervisor. Give callers a loop-count escape from endless hold. Missed calls sign agents out unless presence returns them to Available | [Cell Signaling audit](https://app.notion.com/p/8f0f89f1f48748cc84c1ca43e2345176) |
| Callback pattern | A callback queue per group, **Set callback number**, an option for the caller to key a different number, and a check on initiation method in the outbound flow | [Cell Signaling Callback page](https://app.notion.com/p/6ea35f927b374d6c8df3a751c62a8c12) |
| Routing behavior | Amazon Connect has no round robin; it routes to the longest-available eligible agent. CIS reserves specialists today, which routing profile priorities and delays reproduce | [SCV06 round robin](https://app.notion.com/p/30e83e0c0b824814a0f9baf7c15a046f) |
| Holidays | A custom holiday approach from when Connect had no native option. Re-check current Connect before building it | [SCV07 holidays](https://app.notion.com/p/52293371528a440ab25306d14cc85bbb) |
| Debugging | Debug prompts after each block, Contact Search filtered to voice, the CloudWatch log groups to watch, and the fix for a user sync error (remove the user, re-add, reset the routing profile) | [Debug Guide](https://app.notion.com/p/4f13e12cc48940a1ae136832ea7e8041) |
| Agent browser | Console app only, microphone allowed, one browser tab, and the Salesforce and AWS domains excluded from Chrome Memory Saver | [Debug Guide](https://app.notion.com/p/4f13e12cc48940a1ae136832ea7e8041), [TailorCare findings](https://app.notion.com/p/247d4b87741780c6becbe295c6b793ec) |
| Sandbox refresh re-pairing | Restoring Voice to a refreshed sandbox. Relevant now that Voice lives in the Full sandbox | [Sandbox Refreshes](https://app.notion.com/p/6ecce5f6bc2c47df9550533746ccff59) |
| Admin Guide template | A client-facing admin guide, including a table mapping Salesforce permission sets to Connect security profiles | [Admin Guide](https://app.notion.com/p/120d4b877417801796f5f72a611fda43) |
| Scoping heuristics | About 10 hours per call path; voicemail at 16 hours plus 12 per environment | [Selling CAPP guide](https://app.notion.com/p/459142c244fa4ac28d7761bd747ba1b6) |

The native voicemail write-up (SCV05) builds on Salesforce's media-streaming voicemail, so it does not carry over to GovCloud (inferred).

## Open 5: confirm the GovCloud region at first setup

When the contact center is created, Salesforce's setup asks which AWS region to build in. Salesforce's default list is commercial regions. Its new-instance article says "If you operate in the public sector domain in the US... the list is populated with the AWS GovCloud regions." Its Government Cloud article says "If your GovCloud org does not display AWS GovCloud as a region, open a Salesforce customer support case."

For a Government Cloud Plus org, the GovCloud regions will most likely appear. If they don't, contact center setup cannot proceed until Support acts, and a support case has lead time against a build start the week of October 12.

**Recommendation:** check the region list the first time Voice is set up in the Full sandbox, and open a case only if GovCloud is missing. Reason: the check costs nothing in a sandbox, and a case opened now would ask about something that probably works.

Two related documentation inconsistencies are low risk:

- **The stack region.** Salesforce documents its account-level stack in `us-east-1`, which does not exist in GovCloud. Salesforce's GovCloud policy allows its stacks in any region of the GovCloud partition, so this is commercial wording.
- **The role name.** The setup article says `ProvisioningRole`, and the roles matrix says `SCVProvisioningRole`. Follow the setup article, since the wizard looks for the role "by name." A wrong name fails immediately and visibly.

## Operational items the outline skips

- **Key pair.** "Key pairs expire after one year... If a key pair expires, then your contact center can't connect to the service, and customer calls go unanswered." Rotate with **Update Key**. Reminders come 30 and 5 days out. This belongs in the admin runbook.
- **SAML certificate rotation** causes "a brief period when single sign-on (SSO) is unavailable."
- **Contact center updates.** Reapply the latest provisioning policy to the role first. Updates overwrite customized Lambdas and their environment variables.
- **User sync runs one way.** "Deactivating a user in Salesforce doesn't deactivate them from Amazon Connect," and changing a user's alias breaks SSO. The 90-day inactive-user flow in the security baseline has to reach Connect too.
- **Connect settings.** The After Call Work timeout in Amazon Connect must be 0.
- **Routing limits.** Salesforce does not support moving a call already in one queue to another with **Transfer to queue**, which bears on the English and Spanish routing design.
- **Agent network.** Voice media goes by UDP 3478 straight to the GovCloud TURN endpoints, and AWS says to avoid full-tunnel VPN. The SOW assumes "Existing hardware... and network infrastructure will support the implementation of Amazon Connect without additional upgrades." Fred Hutch's remote-agent VPN posture decides whether that assumption holds.
- **Browser and trusted URLs.** Supported browsers are the latest three versions of Chrome, Edge and Firefox. Safari is not supported, and third-party cookies must be allowed. Salesforce Trusted URLs need `*.amazon.com` and `*.amazonaws.com`. Whether `*.govcloud.connect.aws` also needs adding is not documented, so add it and test.
- **Recording encryption.** Salesforce's provisioning creates the recording bucket and keys. Whether that meets Fred Hutch security's encryption requirement (the RACI's instance storage row) needs checking against the sandbox build.
- **Resource names.** AWS forbids export-controlled data in any Connect configuration metadata (names, aliases, descriptions, tags) and in support cases.

## Questions

### For Jason, 2026-09-29

1. Has he built a bring-your-own (Partner Telephony from Amazon Connect) contact center, or only Salesforce-provisioned ones?
2. How has he moved flows between instances, and what breaks on import besides Lambda blocks?
3. Which voicemail approach did he last use, and has he delivered Voicemail Express tasks or messages into Salesforce?
4. Contact Lens or Amazon Transcribe for transcription in his builds?
5. Has he ported numbers, including toll-free?
6. For the REST API Lambda subject, username or email? His notes disagree with the SCV01 write-up.
7. What patterns does he use for a bilingual IVR: language attribute passed to Salesforce, Polly voices or recorded prompts?
8. What effort does he see for the Connect build, using his roughly 10 hours per call path heuristic?

### For Salesforce Support

1. Is there a supported voicemail path for Partner Telephony from Amazon Connect in AWS GovCloud, given that live media streaming is unavailable there?
2. Only if GovCloud is missing from the region list in the Full sandbox: enable it.

### For the Fred Hutch cloud team and AWS

1. Revise the RACI to two GovCloud workload accounts, each with its paired standard account.
2. Who creates `ProvisioningRole` in each account: the cloud team from Salesforce's published policy, or Kicksaw with scoped `iam:CreateRole` rights? This answers RACI open question 2.
3. For each number: the account holder of record with Verizon, the Customer Service Record or latest bill, and a target port date. Confirm that porting into GovCloud is supported.
4. A remote-agent E911 design without Customer Profiles.
5. Remote-agent VPN posture and the network allowlist.
6. FIPS on the voice media path.

## Documents to update

Proposed, not applied.

| Document | Change |
| --- | --- |
| [project-scope.md](../project/project-scope.md) | Replace "the AWS team owns all AWS configuration" (Cisco row and the settled-positions table) with the RACI split. Add the two decisions |
| [pre-sandbox-build-tasks-2026-09-24.md](pre-sandbox-build-tasks-2026-09-24.md) | Section 4 opening line; the Voice sandbox row (decided: Full sandbox, dedicated AWS account); the sandbox plan row (Full sandbox for Voice and likely the build) |
| [../project/amazon-product-sow-alignment-2026-09-21.md](../project/amazon-product-sow-alignment-2026-09-21.md) | Mark the FIPS finding resolved for the API endpoint; update the ownership boundary section |
| [../discovery/aws-govcloud-call-questions-2026-09-24.md](../discovery/aws-govcloud-call-questions-2026-09-24.md) | Voicemail appendix: Voicemail Express version 3 has no Salesforce mode, and Salesforce's own voicemail uses media streaming |
| Draft RACI (Google Sheet) | Two workload accounts; "create the contact center in Salesforce, which creates the instance"; answer open question 2. Ben edits; the connector cannot write to Sheets |
| RAID Log | Two Decision rows (two AWS accounts; Voice in the Full sandbox). Candidate rows: voicemail route in GovCloud (risk), porting timeline and number ownership (risk), remote-agent E911 (issue). Proposed only |

## Sources

| Source | Where |
| --- | --- |
| Governing SOW, July 20, 2026 | [Google Drive](https://drive.google.com/file/d/1Dt3mlE0QTSltDJC_utDyGtLsIQURlUUK/view) |
| CIS Contact Center, GovCloud and Amazon Connect RACI (draft) | [Google Drive](https://docs.google.com/spreadsheets/d/1kIemrlPj9SC_cmYzH3hwkCQRrbQgkfNG0t8yMuwsvkw/edit) |
| Amazon Connect network architecture for GovCloud (PDF shared by Tony McCune) | Slack, `#internal_fredhutchinson_nci`, 2026-09-24 |
| Current phone stack | [Reverse demo transcript, 2025-07-29](../discovery/transcripts/2025-07-29-nci-call-center-reverse-demo.md); [Discovery session 1, 2026-09-15](../discovery/transcripts/2026-09-15-discovery-session-1-contact-center-reverse-demo.md) |
| Voice sandbox guidelines | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_sandbox_guidelines.htm&type=5) |
| Create a contact center with a new instance | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_new_byoa.htm&type=5) |
| Use an existing instance integrated by Salesforce | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_existing_byoa_auto.htm&type=5) |
| IAM role for Voice | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_ac_iam_role.htm&type=5) |
| Voice IAM roles and policies, GovCloud policy | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_amazon_reference_roles_policies.htm&type=5); [SCVGovProvisioningPolicy.json](https://github.com/service-cloud-voice/examples-from-doc/blob/main/iam_policies/SCVGovProvisioningPolicy.json) |
| Salesforce Voice for Government Cloud | [Salesforce Help](https://help.salesforce.com/s/articleView?id=ind.government_cloud_service_cloud_voice.htm&type=5) |
| Voice limitations | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_limitations.htm&type=5) |
| Identity Provider for Voice | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_setup_idp.htm&type=5) |
| Key pair rotation | [Salesforce Help](https://help.salesforce.com/s/articleView?id=service.voice_update_key_pair.htm&type=5) |
| InvokeTelephonyIntegrationApiFunction | [Voice Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_lambda_invoketelephonyintegration.htm) |
| Salesforce voicemail setup and its audio Lambda | [Enable voicemail support](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_example_voicemail.htm); [VoiceMailAudioProcessingFunction](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_lambda_voicemailaudioprocessingfunction.htm) |
| Sample SCV Voicemail Subflow (media streaming blocks) | [GitHub, service-cloud-voice/examples-from-doc](https://github.com/service-cloud-voice/examples-from-doc/tree/main/ContactFlows) |
| Transcription setup | [Voice Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_example_set_up_transcription.htm) |
| Government Cloud available products (DevOps Center status) | Salesforce Knowledge 000396813 |
| Amazon Connect in AWS GovCloud (US) | [AWS GovCloud User Guide](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-con.html) |
| FIPS endpoints by service, updated 2026-09-28 | [AWS](https://aws.amazon.com/compliance/fips/) |
| Service quotas | [Amazon Connect Admin Guide](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-service-limits.html) |
| Porting: steps and Letter of Authorization | [How to port your numbers](https://docs.aws.amazon.com/connect/latest/adminguide/about-porting.html) |
| Porting: timing | [How long porting takes](https://docs.aws.amazon.com/connect/latest/adminguide/how-long-for-number-porting.html) |
| Porting: country requirements and business hours | [Phone number requirements](https://docs.aws.amazon.com/connect/latest/adminguide/phone-number-requirements.html) |
| Porting: test before you port | [Verify flows before porting](https://docs.aws.amazon.com/connect/latest/adminguide/verify-flows-before-porting.html) |
| Moving numbers between instances | [Move a phone number across instances](https://docs.aws.amazon.com/connect/latest/adminguide/move-phone-number-across-instances.html) |
| Telecoms coverage by region | [Amazon Connect Telecoms Coverage Guide (PDF)](https://d1v2gagwb6hfe1.cloudfront.net/Amazon_Connect_Telecoms_Coverage.pdf) |
| Emergency calling | [Amazon Connect Admin Guide](https://docs.aws.amazon.com/connect/latest/adminguide/setup-us-emergency-calling.html) |
| Flow import and export | [Import and export flows](https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html); [Migrate flows at scale](https://docs.aws.amazon.com/connect/latest/adminguide/migrate-contact-flows.html) |
| Network setup and browsers | [Set up your network](https://docs.aws.amazon.com/connect/latest/adminguide/ccp-networking.html); [Supported browsers](https://docs.aws.amazon.com/connect/latest/adminguide/browsers.html) |
| Account separation | [AWS Well-Architected, security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/aws-account-management-and-separation.html) |
| Voicemail Express | [GitHub](https://github.com/amazon-connect/voicemail-express-amazon-connect) |
| amazon-connect-copy | [GitHub](https://github.com/aws-samples/amazon-connect-copy) |
| Kicksaw prior Voice work | Notion links in [Open 4](#open-4-what-kicksaws-playbook-offers), plus the [Telephony Wiki](https://app.notion.com/p/1168fdb2c9c948e1a7efdc19adb08c5d) |
| Government Cloud org `00Dcs00000LoZ05EAF` | Direct query, 2026-09-28: Voice permission sets, license use, call centers, sandboxes |

## Change log

| Date | Change |
| --- | --- |
| 2026-09-28 | Created. Graded the web outline against Salesforce and AWS documentation; six gaps; FIPS endpoint finding reversed; questions for Jason, Salesforce Support and the Fred Hutch cloud team; document updates proposed |
| 2026-09-28 | Recorded two decisions from Ben: two AWS accounts, and Voice in the Full sandbox (likely the whole build). Narrowed the live media streaming finding to voicemail and Transcribe-based transcription, verified from Salesforce's voicemail subflow; calls, recording and Contact Lens are unaffected. Expanded porting into steps with AWS links and described today's Cisco and Verizon stack. Reframed promotion around importing the AWS configuration, with a Simple default. Expanded the playbook section with what carries over. Downgraded the GovCloud region item to a first-setup check; the `us-east-1` stack wording is commercial, per the GovCloud policy |

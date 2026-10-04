# Enhanced Chat for CIS: research findings

> **Frozen 2026-09-29.** Published to the Notion Project Library as [Enhanced Chat for CIS: research findings](https://app.notion.com/p/3ead4b87741781729e8ed15273cd7313). The Notion page is the live copy; edit there, not here.

How Salesforce Enhanced Chat (Messaging for In-App and Web) replaces the Oracle LiveHelp chat for the NCI Cancer Information Service, what the Government Cloud Plus org already has for it, where it falls short of today's chat, and what still has to be confirmed.

**Audience:** internal Kicksaw (Ben Bolding, Ian Devlin). Not client-facing.

**Decision this builds on:** website chat moves to Salesforce Enhanced Chat, handled in the Salesforce console next to Salesforce Voice and Email-to-Case. This answers chat entry (B-23).

**Sources:** official Salesforce and AWS documentation, read from the rendered pages on 2026-09-28. Org facts come from read-only queries against `FredHutch-GovCloud` the same day. Each claim is marked Verified (documented, with source), Inferred (reasoned from documentation, not stated), or Unverified (documentation is silent).

## Summary

- Enhanced Chat is FedRAMP High authorized in Government Cloud Plus, on four instances only. This org is on **USA9014**, one of the four.
- The org already holds **90 Enhanced Chat User licenses**, none assigned. Unlimited Edition needs no add-on.
- Chat pages stay at livehelp.cancer.gov and livehelp-es.cancer.gov, hosted by NCI with Salesforce's chat code. Nothing Salesforce-hosted sits in the visitor's path.
- Recommended routing is **Omni-Channel Unified Routing**, so one engine owns every agent's capacity across calls and chats. Its availability in Government Cloud Plus is not documented and has to be confirmed.
- Two gaps need design work: **deleting chat content for the 13 or 15 month purge**, and **survey sampling** after chats.

## What the org has today

Read-only queries, 2026-09-28.

| Item | Value | Why it matters |
| --- | --- | --- |
| Instance and edition | USA9014, Unlimited Edition, production | USA9014 is one of the four instances where Enhanced Chat is authorized |
| Enhanced Chat User permission set licenses | 90 total, 0 used | One per chat agent. Covers 40 to 45 agents |
| Service User permission set licenses | 60 total, 1 used | Service Console access |
| Salesforce Voice User (Partner Telephony) | 60 total, 0 used | Voice agents |
| Messaging User permission set licenses | 30 total, 0 used | Other messaging channels such as SMS. Not used for Enhanced Chat |
| Salesforce user licenses | 60 total, 10 used | |
| Guest User License | 25 | Unauthenticated site access |
| Messaging channels configured | 0 | Nothing set up yet |
| Digital Experiences | Not enabled (the `Network` object is not available) | A prerequisite for an Enhanced Chat deployment |
| Maximum Billed Agent Conversations for Messaging | 750 per month | Whether web chat counts against this is not documented. See open item 2 |
| Maximum Billed Blast Conversations for Messaging | 1,000, once | Outbound messaging. Relevant to SMS reminders, not chat |
| Maximum survey responses allowed for an org | 300, once | Caps Salesforce Surveys without Feedback Management licensing |
| Maximum Public Experience Page Views | 0 per month | Rules out serving public chat pages from an Experience Cloud site without more entitlement |
| Experience Cloud CDN bandwidth | 0 per year | Consistent with CDNs being off for Government Cloud sites |

## Availability and licensing

| Question | Answer | Confidence |
| --- | --- | --- |
| Is Enhanced Chat authorized in Government Cloud Plus? | Yes, at FedRAMP High and DoD IL5, on instances USA9014, USA9026, USA9016s and USA9018s only. Help 000396813: "Digital Engagement (Enhanced Chat, Messaging In-App and Web**) \| Yes \| Not Applicable \| Yes", footnote "Available for customers in Salesforce Government Cloud Plus only in cells USA9014, USA9026, USA9016s, USA9018s." | Verified |
| Legacy Chat | Retired. Help 001790618: "Salesforce ended support for Legacy Chat products (LiveAgent, Salesforce Chat, Embedded Chat, and Service Chat) on February 14, 2026." | Verified |
| Edition and add-ons | Unlimited Edition needs no add-on. Enhanced Chat FAQ: "If you have Unlimited edition, no add-ons are needed." | Verified |
| What each agent needs | The Enhanced Chat User permission set license, a custom permission set with the "Enhanced Chat Rep" app permission, and the Service Cloud User feature license. The standard "Messaging for In-App and Web user" permission set "doesn't apply to service reps using Enhanced Chat." | Verified |
| Conversation allowance | The Digital Engagement rate card (September 2026) sets per-conversation billing for Facebook Messenger, Apple Messages for Business, WhatsApp and SMS, with no web chat row. The org nonetheless carries a 750 per month "Billed Agent Conversations for Messaging" entitlement | Unverified for web chat |
| Enablement touches a service outside Government Cloud | "After you enable Digital Engagement, your instance calls the channel provisioning service, which runs in the public Salesforce environment." | Verified |
| Features not authorized | Einstein Bots, Reply Recommendations, Article Recommendations and Case Classification are Interoperable only, which means outside the FedRAMP authorization. AppExchange apps are Interoperable only | Verified |
| Enhanced Chat v2 (newer chat window) | Not stated in Government Cloud documentation | Unverified |
| .gov sites | "Enhanced Chat isn't supported on .mil sites." Nothing is stated about .gov | Verified for .mil only |

## Hosting the chat pages

**Approach:** NCI hosts two simple pages at the existing addresses, livehelp.cancer.gov (English) and livehelp-es.cancer.gov (Spanish), each carrying Salesforce's Enhanced Chat code snippet and today's notices. The addresses stay the same, which keeps the settled decision that entry points do not change (D18).

Why NCI-hosted rather than Salesforce-hosted:

- Government Cloud turns off the Salesforce CDN for new sites because "the Salesforce CDN provider operates outside of the Government Cloud Plus authorization boundary" (Government Cloud content delivery networks article). Verified.
- The org's public Experience Cloud page view entitlement is 0.
- An external host needs no Salesforce custom domain, certificate hosting or Experience Cloud site.

What the setup requires:

| Requirement | Owner | Confidence |
| --- | --- | --- |
| Set the chat deployment's domain to `cancer.gov`, which covers subdomains ("Enter the top level Domain name of the website, such as example.com. This name covers any subdomains") | Kicksaw | Verified |
| Add the two page URLs to the org's CORS allowlist | Kicksaw | Verified |
| The pages must not include `<meta name="referrer" content="no-referrer" />` | NCI web team | Verified |
| If cancer.gov sends a Content Security Policy header, allow the org's chat site and the hosts in the generated snippet | NCI web team | Inferred. Salesforce documents no CSP values for external pages |
| Point the two addresses at NCI's hosting, away from Oracle, at cutover | NCI or NIH DNS owner | Inferred |
| Carry the Privacy Act statement (system of records 09-90-1901), accessibility notice and "not medical advice" disclaimer on each page | NCI web team, wording from CIS | Inferred from today's pages |
| Enable Digital Experiences in the org ("Enable digital experiences in your org" is a deployment prerequisite) | Kicksaw (Ian Devlin) | Verified |

## The chatter's experience

| Today (Oracle LiveHelp) | Enhanced Chat | Confidence |
| --- | --- | --- |
| Anonymous, no name or email | Supported. Leave name and email off the pre-chat form. The chatter shows as "Guest" | Verified |
| One required dropdown: Clinical Trials, Cancer Information, Quitting Smoking | A custom dropdown marked Required. Up to 5 custom dropdowns, 200 values each. The dropdown passes its API value, not its label, into the Omni-Channel flow | Verified |
| Separate English and Spanish pages | The language code is set in each page's snippet. Pre-chat labels, dropdown values, Terms and Conditions and auto-responses are entered per language. Whether the standard window text ships translated into Spanish is not documented for Enhanced Chat | Verified for labels. Unverified for window text |
| Monday to Friday, 9 a.m. to 9 p.m. Eastern | A Business Hours record on the deployment. Outside hours "the chat button appears only during your business hours." There is no offline form or banner | Verified |
| Nobody available during hours | The chat waits in queue. Estimated wait time shows only if a rep accepted a chat in the last 10 minutes. Hiding the button when no reps are online needs custom JavaScript | Verified for queueing. Inferred for hiding |
| No transcript offered on the launch page | Anonymous visitors can download a PDF transcript after the session ends, up to 200 entries, timestamps in GMT. No email-a-copy option | Verified |
| Privacy Act statement and disclaimers on the page | Required Terms and Conditions before chatting, per language, with a hyperlink. 1,000 characters per label, so the full statement links out. Terms and Conditions stop working if the pre-chat form uses custom LWC components | Verified |
| Accessibility | Salesforce's June 2026 conformance report for the Enhanced Chat v2 window covers WCAG 2.0, 2.1 and 2.2 A/AA and Revised Section 508, with "Partially Supports" on criteria 1.3.1, 2.4.3, 2.4.7, 4.1.2 and 4.1.3 | Verified |

## The specialist's experience

| Need | Enhanced Chat | Confidence |
| --- | --- | --- |
| Standard text with F9 hotkeys | Quick Text works in Enhanced Chat, with predictive suggestions and the Lightning shortcut to open the Quick Text browser. No per-message hotkey equivalent found | Verified for Quick Text. Inferred for hotkeys |
| Insert knowledge, sendable portion only | A Communication Channel Mapping picks which article fields go to the chat channel. Chat receives plain text only | Verified |
| See the chat on the case | The conversation shows in the Enhanced Conversation component on the Messaging Session record. Showing it on a case needs a custom component | Verified |
| Report on chat content | Message text is stored in a separate Salesforce-managed database; reports and SOQL cannot read it | Verified |

## Routing and universal queuing

Government Cloud supports Salesforce Voice only through Partner Telephony. For this org that is "Salesforce Voice with Partner Telephony from Amazon Connect", the bring-your-own model. Two routing models apply to it.

| | Blended routing (default) | Omni-Channel Unified Routing |
| --- | --- | --- |
| Who assigns calls to agents | Amazon Connect ("the telephony provider identifies the right rep and performs the actual routing") | Omni-Channel ("designates Omni-Channel as the final allocator of all agent work, including voice calls") |
| How double-booking is prevented | Presence status sync, and Respect Rep Capacity auto-declines a call to an agent already using capacity | One engine holds all capacity |
| Documented weaknesses | "Voice calls are assigned only if a rep has completed all other assigned work items." Chats win race conditions. Statuses drift if an agent closes the browser without logging out | Needs contact center version 18.0 or later and auto-accept in Amazon Connect. Salesforce needs permission to update Amazon Connect queues and routing profiles. Outbound calls ignore capacity |
| Skills-based routing for calls | Not supported | Supported |
| Declined or missed call | Agent set to Offline and the call moves on | Call returns to the queue and is not offered to the same agent until they log back in |
| Government Cloud Plus | Supported | Not stated. Enhanced Omni-Channel in Government Cloud Plus depends on the org running on Hyperforce |

In both models a call takes 100 percent of the agent's capacity: "Voice calls take up all of a rep's capacity." Voice should stay on tab-based capacity, because status-based capacity does not work with After Conversation Work or with Unified Routing callbacks.

**Recommendation (Inferred):** Omni-Channel Unified Routing on Enhanced Omni-Channel. Universal queuing is the client's highest-value outcome, and Salesforce itself points blended-routing customers toward Unified Routing. Start with queue-based routing on four queues: English voice, Spanish voice, English chat and Spanish chat, plus the Amazon Connect holding queue. Bilingual agents join both language queues. "Most Available" or "Least Active" routing breaks ties by giving work to "the service rep who hasn't received work in the longest time," which matches the client's longest-available rule. Record the chat topic on the session for reporting and do not route on it until the client confirms it should drive assignment. Pass the caller's language choice from the Amazon Connect menu into the Omni-Channel flow.

**Chat routing by language and topic:** Enhanced Chat pre-chat fields, visible and hidden, map to Omni-Channel flow input variables, and the flow can branch to a queue or add skill requirements (up to 10 per action, 20 per work item). Verified.

**Not yet reconciled:** the voice setup document ([voice-amazon-connect-setup-gaps-2026-09-28.md](voice-amazon-connect-setup-gaps-2026-09-28.md)) and Kicksaw's Salesforce Voice playbook describe routing in Amazon Connect routing profiles. Adopting Unified Routing moves agent assignment into Omni-Channel and changes the draft RACI row "Queues, routing profiles, skills and callbacks." That document also covers the Kinesis video stream requirement of the existing-instance path and the recommended create-instance path.

## Retention and deletion

**This is the largest open risk for chat.**

- No retention or automatic purge setting exists for Enhanced Chat content. Verified by absence in the documentation reviewed.
- The documented deletion route is the Conversation Data API "Delete a Conversation Participant," which removes "a Messaging end user and all of their messaging-related data." It fails with 412 Precondition Failed if the person has an open session, and certain linked records block it. Verified.
- In the UI, "Sessions can't be mass-deleted, but you can delete individual sessions on the session record page." Verified.
- Unverified: whether the API is available in Government Cloud Plus, whether deleting a Messaging Session removes the message text from the separate database, how attachments are deleted, and how anonymous web visitors map to end-user records.

A rolling 13 or 15 month purge needs a custom design once these are confirmed. The retention period itself is still unsettled with the client (13 months and hidden, or 15 months and deleted).

## Post-chat survey

- The documented mechanism sends a Feedback Management survey link in the channel's End Conversation auto-response, which fires on every session end. Verified.
- There is no built-in sampling, so the 25 percent rule and the 100 percent VA rule need a custom design. Verified by absence.
- Responses from anonymous users are not linked to the session. Verified.
- Salesforce Surveys and Feedback Management are both authorized in Government Cloud Plus. Verified.
- The org is capped at 300 survey responses without more licensing, and the documented setup lists Surveys licensing plus "Salesforce Advanced Features Starter OR Salesforce Surveys Advanced Features." The minimum license for this use is Unverified.

## Gaps compared with today's chat

| Gap | Effect | Direction |
| --- | --- | --- |
| No retention setting; deletion is per end user through an API | The purge requirement needs a custom build | Confirm the API with Salesforce, then design |
| No survey sampling; 300-response cap | The demographics survey needs a sampling design and likely licensing | Survey session; licensing with Mitchell Rabin |
| Transcript not on the case; reports cannot read chat text | Reviewers and reports may need a custom component | Design item |
| No per-message hotkeys | Specialists lose the F9 habit | Confirm on the knowledge session; training |
| Button disappears outside hours; no offline message | Visitors see nothing in the chat window after hours | Hours text on NCI's page |
| Partial WCAG AA support | NCI accessibility review may ask | Have the conformance report ready |
| Bots not authorized | No chatbot or after-hours bot | Consistent with the scope position on chatbots |

## Open items

| # | Item | Owner |
| --- | --- | --- |
| 1 | Is Unified Routing supported for Partner Telephony from Amazon Connect in Government Cloud Plus, is contact center version 18.0 or later available, and is USA9014 on Hyperforce? | Salesforce (Mitchell Rabin) |
| 2 | Does Enhanced Chat count against the org's 750 per month "Billed Agent Conversations for Messaging"? | Salesforce (Mitchell Rabin) |
| 3 | How chat content is deleted in Government Cloud Plus: Conversation Data API availability, message text removal, attachments, anonymous visitor records | Salesforce Support |
| 4 | What data the channel provisioning service outside Government Cloud receives at enablement, for NCI's security documentation | Salesforce (Mitchell Rabin) |
| 5 | Minimum survey licensing for post-chat surveys, given the 300-response cap | Salesforce (Mitchell Rabin) |
| 6 | Is Enhanced Chat v2 available and authorized in Government Cloud Plus, and does the standard window text ship in Spanish? | Salesforce Support |
| 7 | Unified Routing lets Salesforce update Amazon Connect queues and routing profiles through the IAM role. Does the Fred Hutch cloud team accept that? Do auto-accept, predefined attributes, routing criteria and the UpdateContactRoutingData quota work in us-gov-west-1? | Fred Hutch cloud team, AWS |
| 8 | Enable Digital Experiences in the org | Kicksaw (Ian Devlin) |

## Client questions for the 2026-09-29 session

Only the client can answer these. Everything else above is settled by documentation or goes to Salesforce and AWS.

| Question | What it decides |
| --- | --- |
| Does the chat topic decide who gets the chat, for example clinical trials chats only to clinical trials specialists, or does it only label the chat? Session 2 said language is the only routing split; Oracle profiles carry "clinical trials chat eligibility" | Whether routing needs topic skills or language alone |
| We can offer chatters a downloadable transcript at the end. Do you want that? | Whether to turn on transcript download |
| NCI would host two simple pages at the same livehelp addresses with our chat code and today's notices. Who on the NCI web team do we work with, and who controls those addresses? | The outside dependency and its lead time |
| What does a visitor see today outside hours or when nobody is available? | Hours text and the no-agent experience |

## Sources

| Topic | Source |
| --- | --- |
| Government Cloud Plus authorization | [Help 000396813](https://help.salesforce.com/s/articleView?id=000396813&type=1); [Digital Engagement and Messaging in Government Cloud Plus](https://help.salesforce.com/s/articleView?id=ind.government_cloud_digital_engagement_messaging.htm&type=5); [Messaging for In-App and Web in Government Cloud](https://help.salesforce.com/s/articleView?id=ind.government_cloud_messaging_in_app_and_web.htm&type=5) |
| Legacy Chat retirement | [Help 001790618](https://help.salesforce.com/s/articleView?id=001790618&type=1); [release note](https://help.salesforce.com/s/articleView?id=release-notes.rn_chat_retirement.htm&release=252&type=5) |
| Editions and licenses | [Enhanced Chat FAQ](https://help.salesforce.com/s/articleView?id=service.miaw_faq.htm&type=5); [Messaging editions](https://help.salesforce.com/s/articleView?id=service.messaging_editions.htm&type=5); [Prepare users](https://help.salesforce.com/s/articleView?id=service.miaw_prepare_users.htm&type=5); [Service Cloud User feature license](https://help.salesforce.com/s/articleView?id=service.console2_assign_service_feature_license.htm&type=5); [Digital Engagement rate card](https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/legal/Agreements/product-specific-terms/digital-engagement-rate-pricing-sheet.pdf) |
| Deployment and hosting | [Considerations and limitations](https://help.salesforce.com/s/articleView?id=service.miaw_considerations_and_limitations.htm&type=5); [Configure a web deployment](https://help.salesforce.com/s/articleView?id=service.miaw_configure_web_deployment_1.htm&type=5); [Domains overview](https://help.salesforce.com/s/articleView?id=platform.domain_mgmt_overview.htm&type=5); [Experience Cloud license types](https://help.salesforce.com/s/articleView?id=platform.users_license_types_communities.htm&type=5); [Government Cloud content delivery networks](https://help.salesforce.com/s/articleView?id=ind.government_cloud_content_delivery_networks.htm&type=5) |
| Pre-chat, languages, hours | [Custom pre-chat](https://help.salesforce.com/s/articleView?id=service.miaw_custom_prechat_2.htm&type=5); [Custom field example](https://help.salesforce.com/s/articleView?id=service.miaw_custom_field_example.htm&type=5); [Map pre-chat to flows](https://help.salesforce.com/s/articleView?id=service.miaw_map_messaging_2.htm&type=5); [Custom labels](https://help.salesforce.com/s/articleView?id=service.miaw_custom_labels.htm&type=5); [Translate messaging components](https://help.salesforce.com/s/articleView?id=service.messaging_components_translate.htm&type=5); [Business hours](https://help.salesforce.com/s/articleView?id=service.miaw_business_hours.htm&type=5); [Estimated wait time](https://help.salesforce.com/s/articleView?id=service.miaw_estimated_wait_time.htm&type=5); [Terms and Conditions](https://help.salesforce.com/s/articleView?id=service.messaging_terms_and_conditions.htm&type=5) |
| Transcripts and data storage | [Download transcript](https://help.salesforce.com/s/articleView?id=service.miaw_download_transcript.htm&type=5); [Conversation transcripts in the AWS database](https://help.salesforce.com/s/articleView?id=service.conversation_transcripts_aws_database.htm&type=5); [Access conversations](https://help.salesforce.com/s/articleView?id=service.conv_transcript_access_conv_aws.htm&type=5); [Messaging session life cycle](https://help.salesforce.com/s/articleView?id=service.messaging_life_cycle.htm&type=5) |
| Deletion | [Conversation Data API: delete a participant](https://developer.salesforce.com/docs/service/conversation-data-api/guide/delete-conversation-participant.html); [Troubleshoot errors](https://developer.salesforce.com/docs/service/conversation-data-api/guide/troubleshoot-errors.html) |
| Quick Text and Knowledge | [Quick Text setup](https://help.salesforce.com/s/articleView?id=service.quick_text_setting_up.htm&type=5); [Messaging console app](https://help.salesforce.com/s/articleView?id=service.livemessage_create_console_app.htm&type=5); [Insert article content](https://help.salesforce.com/s/articleView?id=service.knowledge_insert_article_content_email.htm&type=5) |
| Surveys | [Post-chat survey](https://help.salesforce.com/s/articleView?id=service.messaging_components_post_chat_survey.htm&type=5); [Automated messages](https://help.salesforce.com/s/articleView?id=service.messaging_automated_enhanced.htm&type=5) |
| Accessibility | [Salesforce accessibility conformance reports](https://www.salesforce.com/company/legal/508_accessibility/) |
| Voice models and routing | [Partner Telephony from Amazon Connect setup](https://help.salesforce.com/s/articleView?id=service.voice_pt_amazon_setup.htm&type=5); [Existing instance](https://help.salesforce.com/s/articleView?id=service.voice_existing_byoa_auto.htm&type=5); [Understanding routing](https://help.salesforce.com/s/articleView?id=service.voice_understanding_routing.htm&type=5); [Route with queues](https://help.salesforce.com/s/articleView?id=service.voice_route_queues.htm&type=5); [Unified Routing](https://help.salesforce.com/s/articleView?id=service.voice_omni_unified_routing.htm&type=5); [Unified Routing GA release note](https://help.salesforce.com/s/articleView?id=release-notes.rn_omnichannel_unified_routing.htm&release=256&type=5); [Skills-based routing](https://help.salesforce.com/s/articleView?id=service.omnichannel_route_using_skills.htm&type=5); [Voice editions](https://help.salesforce.com/s/articleView?id=service.voice_editions.htm&type=5); [Routing options](https://help.salesforce.com/s/articleView?id=service.service_presence_routing_options.htm&type=5) |
| Capacity and presence | [Voice queue setup](https://help.salesforce.com/s/articleView?id=service.voice_queue_setup.htm&type=5); [Respect rep capacity](https://help.salesforce.com/s/articleView?id=service.voice_respect_agent_capacity.htm&type=5); [Voice limitations](https://help.salesforce.com/s/articleView?id=service.voice_limitations.htm&type=5); [Presence status sync](https://help.salesforce.com/s/articleView?id=service.voice_pt_setup_sync_agent_presence_statuses.htm&type=5); [Map presence statuses](https://help.salesforce.com/s/articleView?id=service.voice_map_presence_status.htm&type=5); [Status-based capacity](https://help.salesforce.com/s/articleView?id=service.omnichannel_status_based_capacity.htm&type=5) |
| Government Cloud voice | [Salesforce Voice in Government Cloud](https://help.salesforce.com/s/articleView?id=ind.government_cloud_service_cloud_voice.htm&type=5); [Enhanced Omni-Channel on Hyperforce in Government Cloud](https://help.salesforce.com/s/articleView?id=release-notes.rn_omnichannel_gov_cloud_on_hyperforce.htm&type=5); [AWS GovCloud Amazon Connect differences](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-con.html); [Amazon Connect regions](https://docs.aws.amazon.com/connect/latest/adminguide/regions.html) |
| Today's chat pages | [livehelp.cancer.gov](https://livehelp.cancer.gov/app/chat/chat_launch); [livehelp-es.cancer.gov](https://livehelp-es.cancer.gov/app/chat/chat_launch) |

## Change log

| Date | Change |
| --- | --- |
| 2026-09-28 | Created from documentation research and read-only org queries, after the decision to use Salesforce Enhanced Chat |

# Discovery session 6: the knowledge base

> **Frozen 2026-10-01.** Published to the Notion Project Library as [Discovery session 6: the knowledge base](https://app.notion.com/p/3ecd4b87741781e69bf0e8572dad59d3). The Notion page is the live copy; edit there, not here.

> **Internal document.** Two sections are client-facing: the [Agenda](#agenda), which the project manager emails before the call, and the [Call summary](#call-summary), written after the call. Everything else stays inside Kicksaw. Built from [the discovery session template](_DISCOVERY_SESSION_TEMPLATE.md).

- **Owner:** Ben Bolding
- **Call:** Thursday 2026-10-01, 2:00 to 3:00 PM ET, Microsoft Teams
- **Stage:** Pre-call
- **Transcript:** added after the call

---

## Agenda

*Client-facing. The project manager emails this section as is.*

**Thursday, October 1, 2026, 2:00 to 3:00 PM ET**
Prepared by Kicksaw for the Fred Hutch National Cancer Institute (NCI) Cancer Information Service (CIS) team

### What we want to leave with

A shared picture of how the knowledge base moves into Salesforce: what it holds, how the English and Spanish articles relate, who sees and edits what, and how the articles come out of Oracle. Melissa, we'd like to start with you walking us through a few articles, then work through the questions.

### Topics

1. Introductions: who does what on the knowledge base team
2. Walkthrough: Melissa shows a few articles, from search to what the client receives
3. Size and language: how many articles, and how the English and Spanish versions relate
4. What the knowledge base holds: the seven kinds of content in Oracle, including referrals and standard responses, and the categories specialists search by
5. Who sees what: whether any articles are limited to some staff, and separating the part you send from staff-only notes
6. Writing and review: who writes, approves and publishes, and how review dates work
7. Getting the articles out of Oracle: who runs the export, in what format, and when changes stop before go-live
8. Next steps: what we'll send after the call

### Before the call

Answers on the call are fine for everything here.

**Articles for the walkthrough.** Pick three or four that between them show:

- an English article and its Spanish sibling
- a referral or National Organizations entry
- an article with images, attachments, or links to other articles
- an article with staff-only notes

If there's time, we'd also like to see how an article gets written, translated and published, and the report you use to find articles past their review date.

**Rough counts,** if they're easy to get:

- Articles by language (English, Spanish)
- Articles by status (for example Public, Internally Published, Draft, Retired)
- Articles by product (Knowledge, Referral, Standard Response, Internal Information, PIQ, OD, National Organizations)
- English articles with no Spanish sibling, and Spanish articles with no English sibling
- Articles that are a web link or a file rather than written text
- Articles with images or attachments
- People who write or edit articles, and people who only read them

**Questions to think about**

1. What do PIQ and OD stand for, and are all seven products still in use?
2. Is every Spanish article a translation of an English one? Are there Spanish-only articles, and do the two versions change together?
3. Oracle has an IS Notes field on each answer. Do staff-only notes go there, or are they mixed into the article text?
4. Where does article content come from, and who writes, approves and publishes it? Does anyone outside CIS approve content?
5. Separate from the VA clinic referrals: how do specialists use the referral entries in the knowledge base, the outside organizations you point callers to, and who keeps them current?
6. Should outdated articles be retired before the export, so only current articles move?
7. Where are the images in your articles stored: on the Oracle site, or on a Fred Hutch or NCI web server?
8. Who at CIS can run the knowledge base export from Oracle production?
9. When a specialist gives a referral or sends an article, is that recorded on the inquiry, and does any report count it?

### What we'll assume unless you tell us otherwise

- Articles stay internal to CIS. There's no public help site at launch.
- English and Spanish versions stay linked, with one click between them.
- Each article has a part you can send and a staff-only part. Only the sendable part goes into emails and chats.
- Standard text moves to Salesforce as reusable replies, separate from the articles.
- Only the articles specialists can use today move. Drafts, proposals and retired articles stay behind, along with older versions.
- Your products and categories carry over as they are today.

### What we'll send after the call

- A summary of what we agreed, with who owns each open item
- A short follow-up email with anything we didn't get to

---

## Discovery guide

*Internal.*

Prep guide for the sixth discovery session with the Fred Hutch NCI Cancer Information Service (CIS) team, the knowledge base session. Melissa, who owns the knowledge base, walks the team through it. Anyone on the Kicksaw team can run the call from this guide:

- **Prep briefing:** how answers, the kinds of content in them, and referrals work in Oracle today, with each point labeled by basis. Read before the call
- **Topics, in call order:** the walkthrough, volume and language, what the knowledge base holds, who sees what, writing and review, people and licenses, and export and import
- **The [Agenda](#agenda)** at the top of this document, which the project manager emails ahead of the call, carries the walkthrough request, the counts, the questions to think about, and the assumptions the CIS team can correct

Every question has been checked against the transcripts, so nothing below repeats something the client already answered. Where they did answer, the question is a read-back.

### How this guide works across sessions

- Every question carries a permanent ID: `A-nn` for process, `B-nn` for architecture and data. IDs never renumber. A question that is not reached keeps its ID in the next guide
- **Carried items keep their ID** even when the wording changes. Today that covers B-05 (the proposal path), B-20 (counts, knowledge slice) and B-61 (exports, knowledge slice)
- **New IDs this session run from B-62 to B-82, plus A-36**
- **Treatment** sits under each question, so whoever runs the call knows what to drop when time runs short: `Must ask`; `Ask, short`; `Read-back` (state it, and ask only if they object); `Agenda only` (asked in writing, raised only if unanswered); `Email` (follow-up email unless time is left); `Not on this call`. Agreed with Ben 2026-09-30
- **Origin** says where the question first came up. Codes from earlier guides stand. New codes: `Map-23` is the [Oracle to Salesforce mapping framework](../migration/oracle-to-salesforce-mapping-framework-2026-09-23.md), `Build-24` is the [pre-sandbox build tasks](../salesforce/pre-sandbox-build-tasks-2026-09-24.md), `Chat-28` is the [Enhanced Chat research](../salesforce/enhanced-chat-research-2026-09-28.md), `Prep-30` is the team's knowledge prep document of 2026-09-30, [Fred Hutch - Knowledge](https://docs.google.com/document/d/193PwZmhMzZ9PyqLEnKj_rKwzM6JMhXk6L3kX8LqACQg/edit), whose questions are merged in here, and `S6` is new for this session
- **Labels:** `Verified` means a transcript, the Oracle metadata, a query against the org, or official documentation says it. `Inferred` means reasoned from those, not stated. `Unverified` means nobody has said it
- **Status** is blank before the session. After the call, the post-call agent records it in the [Question status](#question-status) table for each question ID in this guide, as `Answered`, `Partial`, `Not reached`, or `Moved to email`

**Audience:** internal Kicksaw. Not a client deliverable.

Built 2026-09-30 against the session 1 to 5 transcripts and the 2026-09-24 workflow session in Notion, the 2025-07-29 reverse demo, the executed SOW, the Oracle metadata pull of 2026-09-23, the [Oracle org summary](../oracle/oracle-org-summary-2026-09-30.md), the [system landscape](../migration/system-landscape-2026-09-30.md), read-only queries against the Government Cloud org on 2026-09-30, and official Salesforce and Oracle documentation.


### Session details

- **Date and time:** Thursday 2026-10-01, 2:00 to 3:00 PM ET. 60 minutes. Microsoft Teams
- **Organizer:** Mike Griffin. The invite's agenda reads "Walk through knowledge base with CIS KB SME," and asks Jennifer Macabeo to invite Melissa
- **Kicksaw:** Ben Bolding and Hannah Oanca are invited, with Ian Devlin and Avi Rabinovitch optional. **Sarah Tirey is not on the invite.** Avi is out through 2026-10-02 and Hannah from 2026-10-01 to 2026-10-06 (Slack display names, internal)
- **CIS:** Adrianna Gutierrez, Mark Hubers, Jennifer Macabeo, Holly Fernandez-Johnson, Ray Quijano, Reetu Ghumman, Mike Griffin. **Melissa is not on the guest list** as of the invite's last update on 2026-09-23. Her surname appears only in a machine transcript as "Hoard-Silver" and is unverified. Her title is resource specialist: "Melissa as our resource specialist is her official title" (Mark, S2, 59:47)
- **Partners:** Mitchell Rabin (Salesforce), Ken Daugherty and Binu Pazhoor (AWS). Nothing on this agenda needs AWS

### Prep briefing: how the knowledge base works today

*Background for whoever runs the call. Read it before the call. It isn't for use on the call or with the client.*

Each point carries its basis:

- **Said on a call:** the CIS team described it
- **Configuration only:** the Oracle metadata shows the setup exists. That doesn't show CIS uses it that way. Validate these on the call, and never state them to the client as fact
- **Guess:** reasoned, with nothing on record behind it

#### What an answer is

Oracle calls a knowledge base record an answer. It's a standard object, separate from the inquiry and opened from it: "answers as a separate entity... accessible via the inquiry" (Mark, Oracle test environment call, 07:24). Said on a call.

| Part | What it holds | Basis |
| --- | --- | --- |
| Summary | The title, up to 240 characters | Configuration only |
| Question, Answer, Special Response | HTML content. The Answer tab is the body. Special Response is a short version Oracle uses for search excerpts and chat | Configuration only, and Oracle documentation |
| Oracle answer type | HTML (written content), URL (points to a web page), or File Attachment (a file) | Configuration only |
| Products and categories | 7 products at one level, 29 categories three levels deep | Configuration only. Searching by them is said on a call |
| Language and siblings | English (`en_US`) or Spanish (`es_ES`), with the two versions linked as siblings | Siblings said on a call. Codes are configuration only |
| Status and review date | 7 statuses. When the Review On date passes, Oracle moves the answer into review | Configuration only, and Oracle documentation |
| 25 custom fields | The CIS Type field, referral directory fields, tobacco topic tags (`cig`), IS Notes, and fields left over from the 2012 import | Configuration only |

#### One object, several kinds of content

The CIS Type field has five values, and the products add two more kinds of content. So "5,000 answers" isn't 5,000 health articles. It's a mix, and each kind may land somewhere different in Salesforce.

| Type or product | What it appears to be | Basis | Likely Salesforce home (Guess) |
| --- | --- | --- | --- |
| Knowledge | Health information articles | Guess from the name. On-call examples fit, such as a keyword search for ivermectin (session 1) | Knowledge |
| Referral | Directory entries for outside organizations | Configuration only. Never discussed on a call | A Knowledge record type, or a structured object |
| Standard Response | Reusable wording, overlapping the F9 standard text library | Configuration only | Quick Text |
| PIQ | Email templates and standard language, under the categories PIQ Email Library and PIQ Standard Text | Configuration only. Meaning unknown. Possibly Public Inquiries, after the Public Inquiries line in session 5 (Guess) | Email templates or Quick Text |
| OD | Unknown | Nothing on record | Unknown |
| Internal Information (product) | Staff procedures, such as the callback article | Said on a call: "It's internal information" (Adrianna, session 3, 53:17) | Knowledge, internal only |
| National Organizations (product) | Likely more directory entries | Configuration only. It's the one product Oracle's settings let end users see | Same as Referral |

#### How specialists use answers today

All said on a call unless marked.

- **Finding:** keyword search, or product and category filters (Adrianna, session 1, 39:43), mostly from the inquiry's Messages tab (mapping framework)
- **Using, three ways:** read during the call as guidance, inserted into the email or chat reply, or pasted in pieces into larger printed mailings. "You can add it to your answer, to your message, or you can copy and paste from it" (Adrianna, session 1, 39:43). Printed mailings: session 3, 13:14
- **The leak:** inserting sends everything, staff notes included (Holly, session 3, 10:46)
- **Language:** a specialist jumps from an English answer to its Spanish sibling (Adrianna, session 1, 41:47). Agents don't log into the Spanish console: "we basically don't use the Spanish console at all" (session 1, 43:48). But Spanish chats and the Spanish mailbox run on the Spanish interface through business rules (Adrianna, session 5, 47:00)
- **Audience:** internal only (Holly, reverse demo, 50:54)
- **Upkeep:** Melissa's team edits. Specialists email suggestions rather than using Oracle's propose feature. Expired answers and broken links are found by hand (session 1, 51:13 to 52:20)
- **Reporting:** the QuitVet report reads answers, filtering on Public, System Review and Internally Published and excluding Internal Information. Configuration only

#### Referrals mean two different things

- **Inbound, the only sense used on calls so far.** VA clinics refer veterans to smoking cessation through VA Direct, and the smoking supervisors key them in by hand as contacts and callback tasks (Mark, session 1, 27:25 and 30:03, speaker inferred at 27:25; Adrianna, 29:30). Out of scope, and it stays manual
- **Outbound, the knowledge base sense. Never discussed on a call.** These are the organizations CIS points callers to. Adrianna described callers wanting "to find a doctor... financial assistance... treatment information... a clinical trial" (reverse demo, 06:04), without using the word referral. Everything else is configuration only:
  - Referral answers carry a type (International, National, State), contact name, email, phone, city, county, zip code, state, country, up to four languages served, former names, and an NCI database flag. There's no street address field
  - A quality-check log sits on each answer: last verified date, who checked, the result (Approved, Reject, Verification), and notes
  - The inquiry has six coding fields, Referral 1 to Referral 6, sharing a 32-value list, for example NCI-Designated Cancer Center, Smoking Quitline, and Genetics Services
  - The SOW requires "tracking and reporting of all interactions, including... referral types." 88 Oracle report names contain "referral"
- **On the call, open B-67 by naming the difference** ("Separate from the VA clinic referrals..."), or the answer will be about VA Direct
- The mapping framework guesses the Referrals package is the VA Direct record. Both Referrals tables link to answers, so it's the outbound directory

#### What to validate on the call

The configuration-only points the plan leans on, and the question that tests each.

| Assumption | Tested by |
| --- | --- |
| The CIS Type field and the products are the real classification, and all seven kinds are in use | B-66 |
| Referral entries are an outbound directory that specialists use on calls | B-67 |
| The Referral 1 to 6 coding is filled in and reported | B-82 |
| Staff notes sit in IS Notes, not in the body | B-72 |
| Special Response is in use, for example for chat | B-72 |
| Specialists search only Public, System Review and Internally Published answers | B-73 |
| System Review is Oracle's automatic "past review date" state | B-75 |
| Nothing is restricted by staff group | B-71 |
| Images load from a URL, host unknown | B-70 |
| Siblings, not related answers, pair the languages | B-62, B-63 |
| Answer versioning is off | B-76 |

### What we need to leave with

Five answers unblock build work that is on hold today:

| # | Answer | What it unblocks |
| --- | --- | --- |
| 1 | Whether every Spanish article is a translation of an English one | Turning on Knowledge multiple languages, which is one-way (Build-24). The Spanish code is settled from the Oracle metadata (B-64) |
| 2 | Whether products and categories carry over as they are | The data category group skeleton, on hold for the taxonomy (Build-24) |
| 3 | Where staff-only notes sit today, and who separates them | The Knowledge record design and the import mapping |
| 4 | What migrates: which statuses, which products, and whether referrals and standard responses are articles at all | The migration scope and the article count |
| 5 | Who exports from Oracle production, in what format, and when edits stop | The migration plan and the cutover timeline |

### Walkthrough

The walkthrough comes first because the invite promises it and it answers half the questions before they're asked. Skip any later question it answers.

**B-62. Walk us through a few articles** (S6, Prep-30 show list)

*Treatment: Must ask.*

> Melissa, could you walk us through three or four articles: how a specialist finds one, what's in it, and what the client ends up receiving? An English and Spanish pair, a referral, and one with staff-only notes would cover most of what we need. If there's time, we'd also like to see how an article gets written, translated and published, and the report you use to find articles past their review date.

**Walkthrough checklist.** Tick these off as they appear; each one answers or narrows a later question.

| Watch for | Answers |
| --- | --- |
| Which fields hold the article: summary (the title), question, answer, special response, keywords, IS Notes | Import mapping, B-72 |
| Where staff-only notes sit: a separate field, a marked section, or mixed in | B-72 |
| How the Spanish sibling is reached, and whether the link is a field or a hyperlink in the text | B-63, B-65 |
| Product and category on the article, and how search filters by them | B-66, B-69 |
| Images (and where they load from), attachments, and links to other answers inside the text | B-70, B-80 |
| Status, review date, banner, and whether the article sits in the Relationships tab's Sibling Answers section | B-63, B-73, B-75 |
| What happens when the specialist inserts the article into an email or chat | B-72 |
| How an article is written, translated and published, including setting the sibling link | B-63, B-74 |
| The report used to find articles past their review date | B-75 |
| The Proposed queue, even if it's empty | B-05 |
| When in the interaction the specialist searches | A-36 |

**A-36. When specialists search** (Prep-30 question 8)

*Treatment: Watch for it in the walkthrough. Ask, short, only if it doesn't show.*

> At what point do specialists look up an article: during the call, while coding afterwards, or while writing the follow-up email?

Internal note: the answer places the Knowledge component on the console and decides what any later article suggestion would key off.

### Volume and language

**On record**

- "Like 5,000 or more knowledge base articles in both English and Spanish." Verified, Mark, S1, 37:55. No exact count exists yet
- English and Spanish versions are linked as siblings. "These are knowledge base siblings, and siblings are like related answers... I redesigned the sibling function so that people could access Spanish answers." Verified, Adrianna, S1, 41:47. "We often do have like a hyperlink to switch between the English version and the Spanish version." Verified, Mark, S1, 38:52
- **Sibling answers and related answers are separate Oracle features.** Siblings "share the same products, categories, or file attachments," and are Oracle's way to pair languages. Related answers are "see also" links. Verified, [Oracle: sibling answers](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Sibling-answers-aq1387538.html) and [Oracle: answer relationships](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Managing-answer-relationships-aq1131673.html). The draft system landscape says "related answers, repurposed," which the transcript doesn't support
- Oracle has exactly two answer languages: `en_US` and `es_ES`. The `nci` interface is English and `nci2` is Spanish. Verified, Oracle metadata
- The SOW requires "both english and spanish options with linkage between the common articles." Verified, SOW Addendum A
- Whether any article has no sibling: Inferred from Mark's "often," not stated
- On language on screen: "Our need is to be able to distinguish the two, so however Salesforce does that, I think we're open." Verified, Mark, S5, 48:11. Ben's follow-up at 48:20 got no captured answer
- The org has Lightning Knowledge on, with English (`en_US`) the only language. Verified, org query 2026-09-30
- Turning on Knowledge multiple languages is one-way, and it is on hold until the Spanish code is settled and the client confirms whether every Spanish article is a translation. Verified, Build-24

**Why it matters.** Salesforce holds a translation inside its primary article, and the translation inherits the primary's data categories and channels. Oracle siblings are two separate answers joined by a link. Because Oracle siblings already share products and categories, the translation model is the likely fit (Inferred). If every Spanish article translates an English one and they change together, it fits. If some Spanish articles stand alone or drift from the English, they're better as separate primary articles joined by a custom link. That choice has to be right before the one-way language switch is turned on.

**Platform facts**

| Fact | Label |
| --- | --- |
| The parent article holds every version in every language. A translation's `MasterVersionId` points to its source | Verified, [Knowledge Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/knowledge_development_object_managing_articles.htm) |
| With Multiple Languages on, authors can write an article directly in Spanish. A language can't be removed once added, and the setting can't go back | Verified, [Salesforce Help: multilingual setup](https://help.salesforce.com/s/articleView?id=service.knowledge_setup_multilingual.htm&type=5) |
| A Spanish article can be a primary article with no English version. The import file sets its language | Verified, [Salesforce Help: import CSV](https://help.salesforce.com/s/articleView?id=service.knowledge_article_importer_02csv.htm&type=5) |
| Translations inherit data categories from the primary article and can't set their own | Verified, [Salesforce Help: data categories](https://help.salesforce.com/s/articleView?id=service.category_whatis.htm&type=5) |
| `es` and `es_MX` are fully supported languages. `es_US` is an end-user language only | Verified, [Salesforce Help: supported languages](https://help.salesforce.com/s/articleView?id=xcloud.faq_getstart_what_languages_does.htm&type=5) |
| Salesforce doesn't translate. Submitting an article for translation creates a blank draft | Verified, [Salesforce Help 000395085](https://help.salesforce.com/s/articleView?id=000395085&type=1) |
| Search returns the user's language plus the default language, with a language filter. Documented under Einstein Search, whose Government Cloud Plus availability is unverified | Verified behavior; availability Unverified, [Salesforce Help: search languages](https://help.salesforce.com/s/articleView?id=ai.search_esk_multi_support.htm&type=5) |
| Unlimited Edition defaults: 150,000 articles, 10 languages, 10 versions kept per article | Verified, [Salesforce Help 000392616](https://help.salesforce.com/s/articleView?id=000392616&type=1) |

**B-20. Counts, knowledge slice** (Kickoff, carried)

*Treatment: Agenda only.*

In writing, on the Agenda. Read aloud only if the Agenda went unanswered.

> Rough counts of articles by language, by status, and by product, and how many English articles have no Spanish sibling, or the other way round.

**B-63. Translations or separate articles** (Build-24, Prep-30 question 15)

*Treatment: Must ask.*

> Is every Spanish article a translation of an English one? Are there Spanish-only articles, or English-only ones? Who translates, and is it always English first? When an English article changes, does the Spanish one change with it? And does any English article have more than one Spanish partner?

**B-64. Which Spanish** (Build-24)

*Treatment: Not asked. Answered from the Oracle metadata.*

Answered from the Oracle metadata, not asked. Oracle holds one Spanish, `es_ES`, so Salesforce needs one Spanish. Position: use `es` (Spanish), which is fully supported. `es_MX` would imply a regional variant nobody has asked for, and `es_US` has no Salesforce-supplied screens (Build-24). This releases the Build-24 hold on the language code; the translation question (B-63) still holds it.

**B-65. Language on screen** (S5, Prep-30 question 11)

*Treatment: Email.*

> When a Spanish-speaking caller is on the line, should a specialist's search show only Spanish articles, or both languages? And do bilingual specialists need to jump between the two versions of an article with one click, the way they do today?

### What the knowledge base holds

**On record**

- Oracle has seven answer products, all at one level: Knowledge, Referral, Standard Response, Internal Information, PIQ, OD, and National Organizations. They look like knowledge base structure rather than inquiry topics. Verified values, Oracle metadata; the reading is Inferred
- **Three labels for the same idea.** A custom `Type` field on the answer repeats five of the products (Knowledge, Referral, Standard Response, PIQ, OD), and the QuitVet report calls products "Answer Type." Verified, Oracle metadata
- 29 categories, 15 at the top level, three levels deep. Four top-level categories are directory-style (NCI-Designated Cancer Centers, State Organizations, International, Referrals to HP/Treatment Facility). Two hold reusable wording: PIQ Email Library, and PIQ Standard Text with Templates, Empathy and Standard Language beneath it. Verified, Oracle metadata
- A custom `cig` field tags answers with 19 tobacco cessation topics, such as QuitVet, Cravings and Withdrawals, and E-Cigarettes. Verified, Oracle metadata
- The answer carries 25 custom fields, six from the Referrals package: country, state, and four languages. Other custom fields hold referral type (International, National, State), city, county, zip code, contact name, contact email, contact phone, former names, an NCI database flag, and a quick link flag. A separate referral quality-check log records the last verified date, who checked, and a result of Approved, Reject or Verification. Verified, Oracle metadata
- The SOW requires "tracking and reporting of all interactions, including... referral types." Verified, SOW Addendum A. Referrals stored as answers have never come up on a call
- Specialists search "by keyword, or... by our products and categories." Verified, Adrianna, S1, 39:43
- Articles also hold internal procedures, such as the callback entry: "It's internal information." Verified, Adrianna, S3, 53:17
- Standard text is separate from the knowledge base: "a repository of standard templates for emails and messages... you press F9." Verified, Adrianna, S1, 35:34. 352 standard text items in 44 folders, 327 with hot keys, with English and Spanish in parallel folders rather than a language field. Verified, Oracle metadata
- Enhanced Chat has no per-message hot keys, which the chat research marked for this session. Verified, Chat-28
- The mapping framework maps Standard Text to Quick Text and Answers to Knowledge. Map-23

**Why it matters.** Knowledge is the right home for articles a specialist reads and sends. Referral and National Organizations entries look like directory records (an organization, an address, a phone number, languages served), which may fit better as structured records that specialists can filter by state and language, and that NCI can report on by referral type. Standard Response answers overlap with standard text, which becomes Quick Text. Each product needs its own placement decision before the migration count means anything.

**B-66. The seven products** (Map-23, Prep-30 questions 4 to 6)

*Treatment: Ask, short.*

> Oracle sorts your answers into seven products: Knowledge, Referral, Standard Response, Internal Information, PIQ, OD, and National Organizations. What do PIQ and OD stand for? Are all seven still in use, and which ones do specialists open most? Oracle also has a Type field on answers with five of the same values. Which one does your team go by? And of the custom fields on an answer, which does your team actually fill in?

**B-67. Knowledge base referrals, not VA clinic referrals** (Map-23, question 7)

*Treatment: Must ask.*

> Separate from the VA clinic referrals, we'd like to understand the referral entries in the knowledge base: the outside organizations you point callers to, with their contact details and the languages they serve. How do specialists find them on a call: by state, by language, or by keyword? Do they read the details out, or send them? Who keeps them current, and is the quality check (last verified date and result) still in use? Roughly how many are there, and do they have Spanish versions?

**B-82. Recording referrals and articles on the inquiry** (Prep-30 question 9, SOW)

*Treatment: Ask, short.*

> When a specialist gives a caller a referral or sends an article, is that recorded on the inquiry? Oracle has six referral fields on the inquiry. Are they filled in on every call, and which reports, for you or for NCI, count referrals or articles?

**Why it matters.** The SOW requires "tracking and reporting of all interactions, including... referral types." The inquiry carries six coding fields, Referral 1 to Referral 6, sharing a 32-value list (configuration only). In Salesforce, attaching an article to a case creates a record that reports can count. Verified, [Object Reference: CaseArticle](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_casearticle.htm). An article inserted into chat isn't attached to the case. Verified, [Salesforce Help: agent article contents](https://help.salesforce.com/s/articleView?id=service.knowledge_agent_article_contents_lex.htm&type=5). So if article use has to be reported, chat needs a design.

**B-68. Standard responses versus standard text** (S1, Chat-28, Prep-30 question 12)

*Treatment: Ask, short.*

> The Standard Response product, the PIQ Standard Text and PIQ Email Library categories, and the F9 standard text library all hold reusable wording. What's the difference between them? Should any standard text become an article, or the reverse? In chat, do specialists rely on the F9 hot keys, or do they pick from a list?

Position: standard text moves to Salesforce Quick Text, separate from Knowledge. Standard Response answers go with whichever side the client says they belong to.

**B-69. Categories** (Build-24)

*Treatment: Read-back.*

> We plan to carry your products and categories over as they are, so specialists search the way they do today. Is there anything in the category list you'd change now, before we build it?

Position: carry the trees over unchanged at launch. Restructuring is Fred Hutch content work under the SOW ("any required knowledge base content updates or structural changes will be handled by Fred Hutch's internal team").

**Platform fit.** Data categories allow 5 groups (3 active), 100 categories per group, 5 levels, and 8 categories from one group on a single article. Verified, [Salesforce Help: Unlimited Edition limits](https://help.salesforce.com/s/articleView?id=xcloud.overview_limits_unlimited.htm&type=5). Products and categories as two groups fit easily. Ask in the walkthrough whether any article carries more than eight categories. Inferred: that's the only limit Oracle's trees could hit.

**B-70. Links, files and images** (S6, Prep-30 question 3)

*Treatment: Agenda only.*

The Agenda's counts cover most of this. Ask only what the walkthrough and counts leave open.

> How many answers are a web link or a file rather than written text? Where are the images in your articles stored: on the Oracle site, or on a Fred Hutch or NCI web server? Are any articles very long, for example with big tables pasted in from Word? And roughly how many links does a typical article carry, to cancer.gov or to other articles?

**Why the image question matters.** Oracle answers don't store images; "all answer images must be referenced by URL." If they load from the Oracle site, they break when the contract ends, so they have to be downloaded and carried into Salesforce. The long-article question matters because an Oracle content field holds up to 1,048,576 characters and a Salesforce rich text field holds 131,072, HTML included.

| Fact | Label |
| --- | --- |
| Oracle answer types are HTML, URL and File Attachment. Only HTML answers have text and attachments | Verified, Oracle metadata; [Oracle: add an answer](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Add-an-answer-aq1151175.html) |
| Oracle stores question, answer and special response as HTML, up to 1,048,576 characters each. Summary, the title, is 240 | Verified, Oracle metadata; [Oracle: HTML answers](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Adding-HTML-answers-aq1131124.html) |
| "All answer images must be referenced by URL" | Verified, [Oracle: insert an image](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Insert-an-image-answers.html) |
| Links to other answers are inserted by answer ID. The stored tag is probably `<rn:answer_xref answer_id="N" />`, and pasted `/app/answers/detail/a_id/N` links may also exist | Verified for the ID, [Oracle: answer links](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Insert-an-answer-link-answers.html); tag format Inferred |
| Siblings share `commonAttachments`; each answer also has its own file attachments | Verified, Oracle metadata |
| Salesforce: a rich text field holds 131,072 characters including HTML. Unsupported tags, JavaScript and CSS are stripped | Verified, [Salesforce Help: field allocations](https://help.salesforce.com/s/articleView?id=platform.custom_field_allocations.htm&type=5) and [rich text areas](https://help.salesforce.com/s/articleView?id=platform.fields_using_rich_text_area.htm&type=5) |
| Salesforce import: images as .png, .gif or .jpeg up to 1 MB each; attachments become Files, up to 5 MB each | Verified, [Salesforce Help: import CSV](https://help.salesforce.com/s/articleView?id=service.knowledge_article_importer_02csv.htm&type=5) |
| Salesforce smart links between articles survive URL name changes. One rich text field can link to at most 100 articles | Verified, [Salesforce Help: smart links](https://help.salesforce.com/s/articleView?id=service.knowledge_article_smartlink_lex.htm&type=5) and [Lightning Knowledge limitations](https://help.salesforce.com/s/articleView?id=service.knowledge_lightning_limitations.htm&type=5) |

### Who sees what, and what gets sent

**On record**

- Nothing is public. "These are all internal knowledge based articles. They're not external, they're not client facing at all." Verified, Holly, Jul-25, 50:54
- Editing is restricted: "It's done by specific people on the team, so not everybody can edit... there's security around it." Verified, Mark, S1, 51:13. Oracle profiles carry knowledge view and edit rights. Verified, Mark, Oracle-tour, 25:38
- Inserting an article sends staff notes to the client: "It includes everything... notes that are just for our staff... it'd be lovely if we could like pick and choose what gets in there." Verified, Holly, S3, 10:46. Avi proposed "a sendable version and the internal only I see version," and the answer was "Exactly." Verified, S3, 12:41 to 13:14
- Articles go out in emails and chats, and as part of larger printed mailings, not as single printed articles. Verified, S3, 13:14; speaker inferred
- Articles restricted to some staff groups: never discussed
- **Oracle doesn't limit articles by staff group today.** It uses only the two default access levels, Everyone and Help. Staff can see every product and category on all three interfaces. End users can see only National Organizations. Verified, Oracle metadata. The conclusion is Inferred
- Oracle has an `IS Notes` custom field (information specialist notes) on each answer, and a Special Response field, which Oracle uses as a short version of the answer for search excerpts and chat. Whether CIS uses either: Unverified. Verified fields, Oracle metadata; [Oracle: special response](https://docs.oracle.com/en/cloud/saas/b2c-service/famdg/special-response.html)
- Oracle can hide part of an answer by access level with conditional sections. Verified, [Oracle: conditional sections](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Insert-a-conditional-section-answers.html). Whether CIS uses them: Unverified

**Why it matters.** The sendable and staff-only split is an agreed requirement, and it shapes every article's structure. If staff notes are already in their own field, the import maps them. If they are mixed into the text, someone has to separate them article by article, which is content work, and it has to be planned before the export.

**Platform facts**

| Fact | Label |
| --- | --- |
| **Email carries only mapped fields.** Insert Article into Email uses a Communication Channel Mapping that picks which fields go out, per record type and channel. It needs Email-to-Case and the send email action with an HTML body | Verified, [Salesforce Help: insert article into email](https://help.salesforce.com/s/articleView?id=service.knowledge_insert_article_content_email.htm&type=5) |
| Sending an internal article needs the "Share internal Knowledge articles externally" permission. Every CIS article is internal, so every specialist needs it | Verified, same page; the consequence is Inferred |
| Emails leave out smart links and embedded video. Related files attach by default | Verified, same page |
| **Chat inserts plain text only**, and the article isn't attached to the case. The page says "Chat or Messaging" and doesn't name Enhanced Chat. Which fields go into chat is not stated | Verified; Enhanced Chat behavior and field choice Unverified, [Salesforce Help: agent article contents](https://help.salesforce.com/s/articleView?id=service.knowledge_agent_article_contents_lex.htm&type=5) |
| **Lightning Knowledge has no printable view** and no "attach article as PDF" action | Verified, [Salesforce Help: Lightning Knowledge limitations](https://help.salesforce.com/s/articleView?id=service.knowledge_lightning_limitations.htm&type=5) |
| Field-level security hides a field from users completely. Search still matches on the hidden field and returns the article without it | Verified, [Salesforce Help: Knowledge field security](https://help.salesforce.com/s/articleView?id=service.knowledge_custom_field_fls.htm&type=5) |
| With no data category visibility set up, everyone sees everything. Standard sharing for Knowledge is optional and off in the org | Verified, [Salesforce Help: category visibility](https://help.salesforce.com/s/articleView?id=service.category_visibility_whatis.htm&type=5); org query 2026-09-30 |

**The design this points to** (Inferred, to confirm in the sandbox): two rich text fields per article, a sendable part and a staff-only part. Specialists read both. The email channel mapping sends only the sendable part. Field-level security is the wrong tool here, because it would hide staff notes from the specialists who need them. Chat is the open risk: whether Enhanced Chat respects the same field choice needs a sandbox test.

**B-71. Restricted articles** (S6)

*Treatment: Read-back.*

> In Oracle today, every specialist can see every article, and only your team edits. We plan to keep it that way. Is there anything that should be limited, such as supervisor-only procedures? And is anything, such as the National Organizations list, shown outside the specialist console?

Position: every specialist reads every published article, and only Melissa's team edits. That keeps visibility to one rule and avoids data category visibility per role.

**B-72. Staff-only notes** (S3, Map-23 question 9, Prep-30 questions 7 and 10)

*Treatment: Must ask.*

> Oracle has an IS Notes field on each answer. Do staff-only notes go there, or are they mixed into the article text? If they're mixed in, are they always in the same part of the article, so they could be split out automatically? If not, who on your team would separate them, and would that happen before the export or after the articles are in Salesforce? When specialists send an article, do they usually send it whole or copy pieces? And do you use the Special Response field?

**B-81. Chat and printed mailings** (S3, S6, Prep-30 question 13)

*Treatment: Ask, short.*

> When a specialist puts article text into a chat, does the formatting or the links matter, or is plain text fine? And for printed mailings, which articles get printed, how does the text get into the mailing today, and who puts it together?

Internal note: chat inserts plain text only, and Lightning Knowledge has no printable view. If printed mailings matter, say so on the call; it's a gap to design around, not a detail. Hard copies go through a resource specialist report today (Holly, S3, 16:18 to 17:22), and Melissa's title is resource specialist, so she may own the mailing step.

### Writing, review and publishing

**On record**

- Oracle's propose feature went unused: "We don't utilize it. We tried to, the staff didn't like doing it." Specialists email suggestions to "the knowledge base team, Melissa and her folks." Verified, Adrianna, S1, 51:30 to 52:20
- Every article has a review date, and review is manual: "It's a lot of manual... to find which ones have expired... to see if... the links still work." Verified, Adrianna, S1, 52:20
- Oracle has seven answer statuses: Draft, Proposed, Public, System Review, In Review, Retired, Internally Published. The last three are custom. Each maps to a Public or Private status type; the pull doesn't say which. Verified, Oracle metadata
- The QuitVet report filters on Public, System Review and Internally Published, so those are likely the statuses specialists search. Verified filter, Oracle report definition; the reading is Inferred
- Oracle moves an answer into a review status on its own when its "Review On" date passes. The custom System Review status is probably that. Verified behavior, [Oracle: answer visibility](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Controlling-answer-visibility-aq1130135.html); the mapping is Inferred
- Answer versioning is off unless someone turned it on. Whether it's on here: Unverified. [Oracle: answer versioning](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Answer-versioning.html)
- Tony McCune asked in July who approves and publishes; the answer is not in the transcript. Verified, Jul-25, 55:05
- The SOW puts content with Fred Hutch: "Any required knowledge base content updates or structural changes will be handled by Fred Hutch's internal team," and "Fred Hutch will be responsible for doing a quality of review of both english and spanish knowledge articles during the SIT phase." Verified, SOW Addendum A

**Why it matters.** The statuses decide what migrates. The approval chain decides whether publishing needs an approval process in Salesforce or stays with Melissa's team.

**Platform facts**

| Fact | Label |
| --- | --- |
| Publication status is Draft, Online (published) or Archived. A separate validation status is Validated or Not Validated, and it's on in the org | Verified, [Object Reference: Knowledge__kav](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_knowledge__kav.htm); org settings 2026-09-30 |
| Approval processes cover draft to publication only, not translation or archiving. Flow-based approvals for Knowledge are available in Unlimited Edition | Verified, [Salesforce Help: Knowledge approvals](https://help.salesforce.com/s/articleView?id=service.knowledge_setup_wflow_approvals.htm&type=5) |
| `NextReviewDate` is a standard field, set by hand or by Flow | Verified, [Salesforce release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_knowledge_next_review_date.htm&release=244&type=5) |
| No built-in expiry. Archiving on a date can't be scheduled in Lightning; Salesforce suggests a Flow | Verified for archiving, [Salesforce Help: Lightning Knowledge limitations](https://help.salesforce.com/s/articleView?id=service.knowledge_lightning_limitations.htm&type=5); no expiry feature Unverified |
| 10 versions kept per article by default, plus any version attached to a case | Verified, [Salesforce Help: article versions](https://help.salesforce.com/s/articleView?id=service.knowledge_article_versions.htm&type=5) |

Seven Oracle statuses collapse to three publication states plus validation. Oracle's review date maps to `NextReviewDate`, and a report of articles past review replaces today's manual hunt. Inferred.

**B-73. Statuses in use** (S6)

*Treatment: Must ask, together with B-76.*

> Oracle has seven statuses for an answer: Draft, Proposed, Public, System Review, In Review, Retired, and Internally Published. One of your reports filters on Public, System Review and Internally Published, which suggests those are the ones specialists search. Is that right? And what's the difference between Public and Internally Published when nothing is public?

**B-74. Who approves** (Jul-25, Prep-30 questions 2 and 14)

*Treatment: Ask, short.*

> Where does article content come from: does your team write it, or is it adapted from cancer.gov or other NCI sources? Who writes, reviews and publishes an article, and who's on Melissa's team? Does anyone outside CIS, for example at NCI, approve content before it goes live?

**B-75. Review dates** (S1, Prep-30 question 16)

*Treatment: Email.*

> Each article has a review date. What's the review cycle, and when an article passes its date and goes into review, who works it and how?

**B-76. What moves** (S6, Prep-30 questions 1 and 19)

*Treatment: Must ask, together with B-73.*

> We'd like to move only the articles specialists can use today, and leave drafts, proposals and retired articles behind, along with older versions. Does that work, or do you need any article history? And would your team rather retire outdated articles before the export, or after they're in Salesforce?

Position: searchable articles only (Public, Internally Published, System Review, pending B-73), current version only, with cleanup before the export. Version history stays in Oracle, in line with start fresh. The SOW makes cleansing Fred Hutch's work ("Data for migration will be provided in clean, consumable formats... Kicksaw is not responsible for data cleansing").

**B-05. The proposal path** (S1, carried, Prep-30 question 17)

*Treatment: Read-back.*

> Today specialists email suggestions to Melissa's team. We plan to keep that at launch. Does that work?

Internal note: the prep doc's "flag this article" button (Prep-30 question 17) is a later option, not a launch item. Salesforce's Knowledge Feedback needs Surveys, and its Government Cloud availability is unverified, so it isn't offered on the call.

### People and licenses

**On record**

- 60 Salesforce licenses, 10 used. Two active users hold the Knowledge User permission. Verified, org query 2026-09-30
- Headcount by role, including the knowledge base team, is item 6 on the counts request, still open
- Nothing on any call, in Slack, or in the SOW about the number of authors or Knowledge licenses

**Why it matters.** Authors need the Knowledge User feature license. The count of authors, and anyone outside CIS who needs access, has to fit the license pool.

**Platform facts**

| Fact | Label |
| --- | --- |
| Knowledge is included in Unlimited Edition with Service Cloud | Verified, [Salesforce Help: Service Cloud editions](https://help.salesforce.com/s/articleView?id=service.service_editions_reference.htm&type=5) |
| Users with Read on Knowledge plus "Allow View Knowledge" can read and search published articles. The Knowledge User license is needed "to do more than read": create, edit, publish, archive | Verified, [Salesforce Help: Knowledge users](https://help.salesforce.com/s/articleView?id=service.knowledge_setup_users_lex.htm&type=5) |
| **The docs conflict.** The Object Reference says internal users need the Knowledge User license to access `Knowledge__kav` at all | Verified conflict, [Object Reference: Knowledge__kav](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_knowledge__kav.htm). Settle it by testing a reader without the license in the org |
| How many Knowledge User licenses the contract includes | Unverified. Setup, Company Information, Feature Licenses |
| Storage is not a constraint: about 4 KB of data storage per article, against 10 GB plus 120 MB per user. Inline images count as file storage | Verified, [Salesforce Help 000383664](https://help.salesforce.com/s/articleView?id=000383664&type=1) and [storage overview](https://help.salesforce.com/s/articleView?id=xcloud.overview_storage.htm&type=5) |

**B-77. Writers and readers** (S6, Prep-30 question 22)

*Treatment: Ask, short.*

> How many people write or edit articles, and how many only read them? Does anyone outside the specialist team, for example NCI staff, need to read or review articles in the new system?


### Export and import

**On record**

- Fred Hutch plans the export: "We will be exporting the knowledge base to hopefully import those knowledge base answers into Salesforce." Verified, Adrianna, S1, 38:02. Mark asked for "Excel templates or whatever to get the format right to import." Verified, S1, 38:35. Avi committed to work through it together, programmatically where possible (S1, 38:42). No record the templates were sent
- It has never been exported: "No, we've never exported it before." Verified, Holly, S2, 1:00:14
- "When you end an account with Oracle... you are allowed 1 full export of the instance." Verified but hedged, Adrianna, S5, 14:12 and 15:38 ("I think, 1"). Oracle's hosting policy says something different: for 60 days after the contract ends, Oracle keeps content available "in a structured, machine-readable format" or keeps the system accessible. Verified, [Oracle Cloud Hosting and Delivery Policies](https://www.oracle.com/contracts/docs/ocloud_hosting_delivery_policies_3089853.pdf), version 3.12, section 6.1. Neither limits API reads while the contract runs (Inferred)
- Kicksaw has no access to Oracle production. The test environment is a copy "as of like 2 or 3 months ago." Verified, Mark, Oracle-tour, 29:04. Kicksaw's test account can create articles. Verified, Mark, S5, 10:40
- Kicksaw's REST API access to the test environment works. The 2026-09-23 metadata pull read no answer rows. Verified, Map-23

**Why it matters.** An export at contract end is too late to build and test an import. The import has to be built and rehearsed on real articles weeks before cutover, then run once more on a final export taken before the Oracle contract ends, not in the 60 days after.

**Oracle export options**

| Method | What it returns | Label |
| --- | --- | --- |
| Connect REST API, one call per answer, plus attachment downloads | Every field, including full HTML, siblings and attachment links. The only method known to return everything | Fields Verified, [Oracle: answers REST](https://docs.oracle.com/en/cloud/saas/b2c-service/cxsvc/op-services-rest-connect-v1.4-answers-post.html); completeness of long HTML Inferred |
| ROQL query (`queryResults`) | Up to 20,000 rows, or 100,000 with `USE REPORT`. Oracle doesn't say whether long HTML fields come back in full | Verified limits, [Oracle: ROQL](https://docs.oracle.com/en/cloud/saas/b2c-service/cxsvc/c_osvc_roql_tabular_queries.html) |
| Analytics report export | At most 10,000 rows per call. Suits counts, not content | Verified, [Oracle: report results](https://docs.oracle.com/en/cloud/saas/b2c-service/cxsvc/op-services-rest-connect-v1.4-analyticsreportresults-post.html) |
| Bulk Extract API | Documented for incidents only, not answers | Verified, [Oracle: bulk extract](https://docs.oracle.com/en/cloud/saas/b2c-service/cxsvc/c_osvc_bulk_extract.html) |
| Attachments | One at a time, or all of a record's attachments as one .tgz file. 20 MB per file | Verified, [Oracle: file attachments](https://docs.oracle.com/en/cloud/saas/b2c-service/cxsvc/c_osvc_managing_file_attachments.html) |

**Salesforce import options**

| Fact | Label |
| --- | --- |
| Import Articles takes one .zip: one CSV, one .properties file, and folders of HTML and images. Up to 20 MB per .zip, 10 MB per file, and 10,000 CSV rows including the header. About 5,000 articles plus their translations needs several batches | Verified, [Salesforce Help: import .zip](https://help.salesforce.com/s/articleView?id=service.knowledge_article_importer_04zip.htm&type=5) |
| Translations import in the same CSV: an `isMasterLanguage` column, with each translation row straight after its primary | Verified, [Salesforce Help: import CSV](https://help.salesforce.com/s/articleView?id=service.knowledge_article_importer_02csv.htm&type=5) |
| Set the encoding to UTF-8. The default is ISO 8859-15, which puts Spanish characters at risk | Verified, [Salesforce Help: import parameters](https://help.salesforce.com/s/articleView?id=service.knowledge_article_importer_03parameters.htm&type=5) |
| The `RecordTypeId` column takes the 15-character ID. A tool requirement, and an exception to the 18-character rule | Verified, [Salesforce Help 000384025](https://help.salesforce.com/s/articleView?id=000384025&type=1) |
| An import can stop after an hour, and "Completed" doesn't mean it succeeded. Check the email log | Verified, [Salesforce Help: import status](https://help.salesforce.com/s/articleView?id=service.knowledge_article_importer_05status.htm&type=5) |
| Through the API, `Knowledge__kav` supports create, update and upsert. Publishing is `KbManagement.PublishingService.publishArticle` in Apex, not Data Loader | Verified, [Salesforce Help 000381649](https://help.salesforce.com/s/articleView?id=000381649&type=1) and [Apex reference](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_classes_knowledge_kbManagement.htm) |
| Whether Import Articles lands articles as drafts or published, and whether Bulk API 2.0 supports `Knowledge__kav` | Unverified. Test in the sandbox |
| Salesforce recommends a full-copy sandbox for Knowledge migration testing | Verified, Build-24 |

**B-61. Who exports, and in what format** (S2, carried, knowledge slice)

*Treatment: Must ask.*

> Who at CIS can run the knowledge base export from Oracle production? The Oracle API is the only route we know that returns the full article text, images and attachments, so could that person run a script we provide, or could we have a read-only API account on production for the final export?

**B-78. Build the import on the test environment** (S6, Prep-30 question 18)

*Treatment: Not on this call. It belongs to migration planning.*

Position for migration planning. The test environment holds nearly current articles, and Kicksaw already has API access to it. Reading the answers there lets Kicksaw build and rehearse the extract and the import before touching production. The same script then runs once against production for the final export (B-61). The articles stay on Kicksaw's machine under `extracts/`, like every other Oracle pull.

> The test environment has a copy of your articles from a few months ago. Could we read the articles there through the API, to build and test the import before the real export from production?

The prep doc asks the client instead to export a sample of 20 articles, including a Spanish pair, from Oracle's answer export (Prep-30 question 18). Same aim, more work for CIS, and a smaller sample.

**B-79. When edits stop** (S6)

*Treatment: Email.*

> At cutover, there'll be a short window when articles can't change, between the final export and go-live. How long a freeze can your team live with, and is there a time of month that's quieter for article updates?

**B-80. Links into the knowledge base** (S6, Prep-30 question 20)

*Treatment: Email.*

> Do other things link to specific answers by their Oracle number, such as standard text, email templates, other articles, cancer.gov pages, or saved bookmarks? When the articles move, those links need to point at the new ones.

Internal note: keep each Oracle answer ID on the Salesforce article, so answer links inside article text (by answer ID, see B-70) can be rewritten to Salesforce smart links after import, and every migrated article traces back to its source.


### Settled decisions, do not reopen

| Source | Decision |
| --- | --- |
| RAID-2, knowledge base migration | In scope. About 5,000 English and Spanish articles migrate |
| Session 2, start fresh | Historical interaction data does not migrate. The knowledge base is the exception |
| SOW Addendum A | Fred Hutch owns content updates, structural changes, and the English and Spanish quality review in SIT |
| Session 2, AI | Any AI needs Fred Hutch and NIH approval, and AI article suggestions are not a launch requirement |

**If AI article suggestions come up.** Einstein Article Recommendations and Reply Recommendations are "Interoperable only" in Government Cloud Plus, meaning outside the FedRAMP authorization (Chat-28, Verified). The answer on the call: not at launch, and any AI needs Fred Hutch and NIH approval first, which is what the team said in session 2. Mitchell Rabin is on the invite if the client wants Salesforce's own position.

**Left off the call from the prep doc**

| Prep doc question | Why it's off the call |
| --- | --- |
| 21. Which Salesforce edition was bought | Known. The org is Unlimited Edition, which includes Knowledge. The Knowledge User license count is a Setup check |
| 23. Einstein or Agentforce features in the order | A question for Mitchell Rabin, not the client. Article Recommendations is outside the FedRAMP authorization in Government Cloud Plus |
| 24. Starting the AI approval conversation | Settled in session 2: not at launch, and any AI needs Fred Hutch and NIH approval |

### Follow-up email, not the call

| Item | ID or origin |
| --- | --- |
| Anything from the Agenda not answered on the call | Agenda |
| The callback knowledge article and the "callback coding logistics" document Adrianna promised | S3, 57:23, carried from session 5 |
| Element Manager access for Kicksaw's test account, which Mark wasn't sure of | S5, 15:18 |

### Carried items not on today's agenda

All carried items listed in the [session 5 guide](discovery-guide-session-5-2026-09-29.md#carried-items-not-on-todays-agenda) stay carried. Session 5 status against its transcript is not filled yet. Two touch knowledge:

| ID | Item | Where it stands |
| --- | --- | --- |
| B-34 | Capability read-back for profiles, including knowledge read and knowledge edit | Carried. B-71 and B-77 cover the knowledge half |
| B-36 | The 60-license basis | Not for the call. B-77 feeds it |


### Question status

*Filled after the call.*

| ID | Status | Where |
| --- | --- | --- |
| B-62 | | |
| A-36 | | |
| B-20 | | |
| B-63 | | |
| B-65 | | |
| B-66 | | |
| B-67 | | |
| B-82 | | |
| B-68 | | |
| B-69 | | |
| B-70 | | |
| B-71 | | |
| B-72 | | |
| B-81 | | |
| B-73 | | |
| B-74 | | |
| B-75 | | |
| B-76 | | |
| B-05 | | |
| B-77 | | |
| B-61 | | |
| B-78 | | |
| B-79 | | |
| B-80 | | |

---

## Transcript

*Internal. Added after the call.*

Not yet loaded.

---

## Call summary

*Client-facing. Written after the call from the transcript. The project manager may email it as is.*

Not yet written.

---

## Change log

- **2026-10-01, revision 6.** The guide holds discovery content only. Removed the pre-call task and decision list, the after-the-call list, and the ID collision note. Proposed positions now read as positions. B-78 moved off this call to migration planning
- **2026-09-30, revision 5.** Merged the team's knowledge prep document (Prep-30) into the topics, using its wording where it added something, and listed the three questions left off the call. Added B-82 (recording referrals and articles on the inquiry) and A-36 (when specialists search). Reframed B-67 to separate knowledge base referrals from VA clinic referrals. Recorded Ben's agreement to the question review as a treatment under each question. Agenda: walkthrough extras, content origin, referral wording, and a ninth question
- **2026-09-30, revision 4.** Made ownership neutral so anyone can run the call: removed the named lead sections and the run of show, and named Ben Bolding as the record owner. Topics now sit directly under the guide in call order
- **2026-09-30, revision 3.** Added the prep briefing: what an answer is, the kinds of content it holds, how specialists use answers, the two meanings of referral, and the configuration-only assumptions to validate on the call
- **2026-09-30, revision 2.** Merged the guide and the client agenda into one document in the four-part shape: Agenda, Discovery guide, Transcript, Call summary. Agenda rewritten as lists so it pastes cleanly into email. Added the Question status table
- **2026-09-30, revision 1.** Created as a separate guide and agenda, with Ian Devlin's section in place of Avi's. Carried B-05, B-20 and B-61. Added B-62 to B-81. B-64 (which Spanish) answered from the Oracle metadata rather than asked. Platform facts sourced from Salesforce and Oracle documentation

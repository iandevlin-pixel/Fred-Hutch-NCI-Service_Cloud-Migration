# Salesforce Government Cloud (target)

The FedRAMP-approved Salesforce Government Cloud org that the NCI CIS contact center lands in. Confirmed as the target platform in the SOW and at kickoff (register row A2). FedRAMP moderate; high is not a requirement (A1).

Deliverables about the target go here: org configuration, the agent workspace and inquiry model, omnichannel routing, Service Cloud Voice, permissions and persona design, knowledge structure, reporting.

**Constraints that make this different from a standard Salesforce build:**

- All integrations must reside inside the Government Cloud boundary. Standard AppExchange packages with external integrations cannot simply be installed, and the FedRAMP-approved product set is very limited (R8)
- Deployment ownership is unconfirmed. Some agencies do not permit the systems integrator any production access
- FedRAMP-approved deployment tooling and CI/CD constraints are unconfirmed
- AI development tool restrictions are unconfirmed
- No one at Kicksaw has prior Government Cloud delivery experience (R5)

Note that the AWS partition for Amazon Connect (GovCloud or commercial) is a separate and unresolved question, register row D2. This folder is the Salesforce side only.

## What's in this folder

| Document | What it is |
| --- | --- |
| [security-baseline-fedramp-moderate-2026-09-24.md](security-baseline-fedramp-moderate-2026-09-24.md) | Recommended org security settings for FedRAMP Moderate |
| [pre-sandbox-build-tasks-2026-09-24.md](pre-sandbox-build-tasks-2026-09-24.md) | What to configure in production before the first sandbox is created |
| [voice-amazon-connect-setup-gaps-2026-09-28.md](voice-amazon-connect-setup-gaps-2026-09-28.md) | Setting up Salesforce Voice with Amazon Connect in GovCloud, and the gaps found |
| [sms-reminders-options-2026-09-22.md](sms-reminders-options-2026-09-22.md) | Options for the callback reminder texts that Amazon Pinpoint sends today |
| [enhanced-chat-research-2026-09-28.md](enhanced-chat-research-2026-09-28.md) | Salesforce Enhanced Chat as the replacement for Oracle chat |

This folder holds documents about the org. The org's metadata is in `force-app/` at the repository root, where the Salesforce CLI expects it.

`extracts/` holds local data pulls. It is gitignored and never leaves this machine.

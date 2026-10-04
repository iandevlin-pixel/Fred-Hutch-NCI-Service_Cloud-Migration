# PM

The working area for the PM agent, the Claude Code plugin that keeps the RAID Log, requirements, and status reports in order. The agent isn't live on this project yet.

The project's source of truth for risks, actions, issues, and decisions is the [RAID Log](https://app.notion.com/p/c62d4b877417826a940681acafb41f31) in Notion. File new rows there.

## How the agent finds the project

The agent reads `pm-project.yaml` at the repository root. That file names the people, the Notion databases, the Jira project, and the Slack channel, and labels each one internal or client-facing. It holds identifiers only.

## What's in this folder

Everything here except this README stays on Ben Bolding's machine.

| Path | Contents |
| --- | --- |
| `raid/` | The local decision register that predates the RAID Log, its guide, its evidence folder, the values imported into Notion on 2026-09-18, the two RAID migration plans, and the audit of the RAID Log against the RAID standard |
| `extracts/` | Outputs of agent runs, such as RAID classification results |

The register moves to the Notion RAID Log through the PM agent. Until then it's Ben Bolding's working copy and isn't shared.

# Oracle Service Cloud (source, being retired)

The legacy NCI CIS platform, in place since 2012. Oracle B2C Service, still called RightNow by the client. Holds the inquiry model (the `incident` table, workspace NCI Inquiry v2.1), the callback tasks, the SCIF intake form, the knowledge base (roughly 5,000 English and Spanish answers), surveys, and 14 years of Oracle Analytics reports. Bridged to Cisco Finesse telephony through OpenMethods Harmony and PopFlow. Runs as a Windows-only .NET console; a web version exists but the client stayed on the desktop client because Harmony had no web version.

**Access, as of 2026-09-21.** Kicksaw has one shared login to the test clone `NCI__TST`, a full copy of production from two to three months earlier, granted by Mark Hubers on the [Oracle test environment tour](../discovery/transcripts/2026-09-21-oracle-test-environment-access.md). The grant covers configuration and was meant to cover surveys; the surveys grant did not take and reports are excluded because their data cannot be separated from PHI. Console access needs a Windows VM. REST API access with the same account was confirmed on 2026-09-23 against `https://nci--tst.cx.usg.oraclecloud.com`; the catalog lists 63 resources including 21 custom objects in the `SCIF`, `DEMOGR`, `Referrals` and `OpenMethods` packages.

**What is known first-hand:** the object model, the rules editor layout, the database directory with the custom fields grouped by originating project, staff groups and profiles. **What is not:** record counts and volumes (RAID-23, legacy Q5), what the retention purge deletes versus hides (RAID-24, legacy Q7), and the site version. The data risk row is RAID-30 (legacy R3).

## What's in this folder

| Path | Contents |
| --- | --- |
| [oracle-concepts-for-salesforce-teams-2026-10-02.md](oracle-concepts-for-salesforce-teams-2026-10-02.md) | Start here if you know Salesforce and not Oracle: what each Oracle term is, what it connects to, and its Salesforce equivalent |
| [oracle-concepts-visual-2026-10-02.html](oracle-concepts-visual-2026-10-02.html) | The same ideas as eight diagrams, Oracle next to Salesforce. Download it and open it in a browser |
| [oracle-data-dictionary-2026-10-02.csv](oracle-data-dictionary-2026-10-02.csv) | The data dictionary: one row per field for 46 Oracle objects (1,186 fields). Each row has the field's definition and a suggested Salesforce type, how much it was used in the last 48 months, and for picklists the defined values and the values used, separated by semicolons. No records. Two fields whose values are staff names (CT Searcher, Lead) carry no values. Built by [tools/build_dictionary_with_usage.py](tools/build_dictionary_with_usage.py) |
| [oracle-org-summary-2026-09-30.md](oracle-org-summary-2026-09-30.md) | What the Oracle test instance holds, by object, queue, profile, and picklist, compared with the Salesforce org |
| [oracle-console-pull-checklist-2026-09-27.md](oracle-console-pull-checklist-2026-09-27.md) | The configuration the REST API doesn't expose, with counts and where to find each item in the console |
| [oracle-console-capture-admin-tasks-2026-09-28.md](oracle-console-capture-admin-tasks-2026-09-28.md) | The admin's steps for capturing that configuration |
| [tools/](tools/README.md) | Python scripts that pull Oracle metadata, build the data dictionary, and profile the data |
| `extracts/` | Every raw pull. Gitignored. It never leaves the machine that pulled it |

Deliverables about this system go here: the data dictionary, the configuration inventory, the data profile, and the knowledge export analysis. How Oracle maps onto Salesforce and Amazon Connect is in [migration/](../migration/README.md).

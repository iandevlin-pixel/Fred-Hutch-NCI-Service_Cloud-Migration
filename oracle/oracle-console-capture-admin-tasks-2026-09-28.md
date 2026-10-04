# Oracle console capture

> **Frozen 2026-09-29.** Published to the Notion Project Library as [Oracle console capture: admin tasks](https://app.notion.com/p/3ead4b87741781e18eeaca728d8e79df). The Notion page is the live copy; edit there, not here.

You're capturing how CIS has Oracle Service Cloud configured, so Kicksaw can rebuild it in Salesforce. Everything on this list is configuration: exports and screenshots from the Oracle console. The account can't see caller records.

- **System:** the Oracle test instance, signed in as `sthomas_RNT`
- **Result:** a set of exports and screenshots in the Google Drive folder Ben Bolding shares with you

## Before you start

- Sign in only when nobody else is using `sthomas_RNT`. The account allows one session, so signing in ends anyone else's.
- Change nothing. When an export opens an item in its designer, close the designer without saving.
- Upload every file to the shared Google Drive folder, and keep the files only there.
- Name each file after what it holds, for example `workspace-nci-inquiry-v2.1.xml` or `rules-inquiry-01.png`.
- Don't edit an exported workspace file. Oracle rejects any file that has been changed.
- Menu names come from Oracle's documentation and may differ slightly in this instance.

## Do these first

### 1. Workspaces and workflows

In **Configuration** > **Application Appearance** > **Workspaces/Workflows**, open the NCI folder.

1. Screenshot the folder listing.
2. Right-click a workspace and select **Open**.
3. Select **File** > **Export Workspace**, and save the file.
4. Close the designer without saving.
5. Repeat for each workspace. Start with NCI Inquiry v2.1, then the task, contact and SCIF workspaces.

### 2. Business rules

In **Configuration** > **Site Configuration** > **Rules**, capture these six rule bases: inquiry, task, contact, answer, chat and organization. Skip opportunity.

1. Open a rule base.
2. Use its export or print option if it has one. If not, screenshot its states, rules, functions and variables.
3. Repeat for each rule base.
4. Capture any rules on the SCIF, DEMOGR and Referrals objects as well. Mark Hubers showed more rules under the **Database** area.

### 3. Profiles (40)

In **Configuration** > **Staff Management** > **Profiles**, screenshot two things for each profile:

- The **Interfaces** section, which shows the navigation set and the workspace for each record type
- The permissions, including queue access and pull policy

## Then these

4. **Navigation sets.** In **Configuration** > **Application Appearance** > **Navigation Sets**, screenshot each set's buttons and explorer items.
5. **Custom field visibility (160 fields).** In **Configuration** > **Database** > **Custom Fields**, screenshot the visibility settings for inquiry, task, contact and answer fields.
6. **Custom processes.** In **Process Designer**, under **Site Configuration**, screenshot the list of processes. Include the object and event each one runs on.
7. **Agent scripts and guided assistance.** Under **Application Appearance**, screenshot the list, and export any script that offers an export. Skip this if there are none.
8. **SLAs.** In **Configuration** > **Service** > **Service Level Agreements**, take one screenshot of the list. Oracle shows none, so this confirms it. Also screenshot the default response requirements.
9. **Message templates.** In **Configuration** > **Site Configuration** > **Message Templates**, screenshot each template that CIS changed from the default.
10. **Chat setup.** Screenshot the chat hours for each of the three interfaces (`nci`, `nci1` and `nci2`) and the settings of the six chat queues.
11. **Data retention.** In **Configuration** > **Site Configuration** > **Configuration Settings**, search for `PURGE`, then for `ARCHIVE`, and screenshot the results. If the Agent Browser UI lets you reach the Data Lifecycle policies, screenshot those too. Skip any setting that holds a password, key or credential.
12. **Add-ins.** In **Add-In Manager** (console) or **Extension Manager** (Agent Browser UI), screenshot three things: the add-in list, the settings of the OpenMethods and demographics pop-up add-ins, and the profiles each add-in is assigned to.
13. **Surveys.** Wait until Ben Bolding confirms that Mark Hubers has granted survey access. Then, in **Survey Explorer**, screenshot each survey's questions and settings. Expect at least three: demographics, client satisfaction and tobacco follow-up.

## When you're done

Tell Ben Bolding that the Drive folder is complete. List anything you skipped or couldn't reach.

## Appendix: Element Manager

Element Manager is Oracle's tool for exporting configuration in bulk. It isn't turned on for this account, which is why this list uses the console. If Mark Hubers turns it on, one export could cover workspaces, business rules and navigation sets (tasks 1, 2 and 4), and Ben Bolding will send updated steps. Until then, use the console steps above.

## Sources

- [Export a Workspace](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Export-a-workspace-ac1394377.html)
- [Customizing Profiles](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Customizing-profiles-ar1294709.html)
- [Custom Field Visibility Settings](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Setting-custom-field-visibility-bx1138190.html)
- [Create a Navigation Set for the Administrator](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Create-a-navigation-set-for-the-administrator-am1206889.html)
- [Accessing the Process Designer](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-Accessing-the-process-designer-bs1130847.html)
- [Overview of Service Level Agreements](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/c-css-admin-SLAs.html)
- [Set Chat Hours](https://docs.oracle.com/en/cloud/saas/b2c-service/famug/t-Set-chat-hours-ac1149758.html)

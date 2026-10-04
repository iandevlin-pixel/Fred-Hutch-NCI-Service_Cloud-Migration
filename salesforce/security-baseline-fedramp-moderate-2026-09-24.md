# Security baseline: FedRAMP Moderate settings for the Government Cloud org

> **Frozen 2026-09-30.** Published to the Notion Project Library as [Security baseline: FedRAMP Moderate settings for the Government Cloud org](https://app.notion.com/p/3ebd4b87741781bead19f77477a4681e). The Notion page is the live copy; edit there, not here.

Recommended security settings for the NCI CIS Salesforce Government Cloud org, written to go into the solution design. Each recommendation carries its reason and source. Nothing here has been applied to the org.

## How the values are chosen

This is a new environment built to FedRAMP Moderate. Three sources, in this order:

1. **NCI's own system authorization.** FedRAMP values bind Salesforce as the cloud provider. The settings inside the org belong to the agency's authorization: FedRAMP's agency guidance says "The agency authorization should document what the agency configures." Where NCI has set a value, it wins.
2. **FedRAMP Moderate.** Where NCI has not set a value, we recommend the FedRAMP Moderate value, whatever Oracle Service Cloud does today. These are the numbers assessors and agency security staff recognize.
3. **Oracle Service Cloud, only where Moderate sets nothing.** For settings Moderate leaves open, such as login hours or IP restrictions, we start from Oracle's current setting so agents keep what they know.

Two changes in 2026 affect how the sources read:

- **FedRAMP moved to new rules on June 23, 2026.** Its Rev 5 baseline spreadsheet now opens "This is a legacy document that is being replaced by the FedRAMP Consolidated Rules for 2026... Use with extreme caution." The new rules no longer set values for account management, lockout, the login banner, session timeout or audit retention. We still use the legacy Moderate values below as the benchmark, because no newer value exists and agency reviewers know them.
- **The federal logging memo FedRAMP cites was withdrawn.** OMB M-26-14 (May 22, 2026): "Effective immediately, OMB Memorandum M-21-31 is rescinded." Its replacement asks for logs "actively searchable for a minimum of 6 months" and retrievable for a year.

Single sign-on is not in the executed SOW, so this baseline assumes specialists sign in to Salesforce directly with multi-factor authentication. Salesforce therefore holds the passwords, and the password and lockout settings below carry real weight.

## Recommended settings

| Area | Requirement | Salesforce setting | Recommended | Org today |
| --- | --- | --- | --- | --- |
| Session timeout | 15 minutes of inactivity (AC-11); 15 minutes for user sessions, 10 for privileged sessions (SC-10) | Session Settings timeout; options start at 15 minutes | 15 minutes, force logout on timeout on, timeout warning left on | 2 hours |
| Session length | Sessions end within 24 hours (NIST SP 800-63B-4, AAL2) | No maximum-length setting. Profile login hours end a session when the window closes | Agent profile login hours around the 9 AM to 9 PM ET operating window. Admin profiles limited to the admin workday (AC-2(5)) | None set |
| Multi-factor authentication | Phishing-resistant, for privileged and non-privileged accounts (IA-2(1), IA-2(2)) | Passkeys and security keys are the phishing-resistant options. Salesforce Authenticator is "Interoperable (Not Authorized)" in Government Cloud Plus. Authenticator apps count only as standard MFA | Passkeys or security keys for every user. Physical security keys for admins | Multi-factor authentication required for direct logins (Salesforce enforces it) |
| Password length | Minimum 15 characters when a password is the only factor; 8 within multi-factor (SP 800-63B-4). Legacy FedRAMP: 14 where multi-factor is not possible | Minimum password length, 5 to 50 | 15. API logins do not go through multi-factor authentication, and 15 meets both the NIST and legacy FedRAMP figures | 8 |
| Password rules | No composition rules and no forced rotation (SP 800-63B-4). Legacy FedRAMP: "shall not enforce special character or minimum password rotation requirements" | Complexity; expiration | Complexity: no restriction. Expiration: never | Alphanumeric; 90 days |
| Password history | No NIST requirement | Passwords remembered | 3 (the default) | 3 |
| Lockout | In line with SP 800-63B, which allows up to 100 failures and lets agencies set fewer (AC-7) | Maximum invalid login attempts (3, 5, 10, no limit); lockout period (15, 30, 60 minutes, or until an admin resets) | 5 attempts, 30-minute lockout | 10 attempts |
| Login banner | U.S. Government system notice that users acknowledge before access (AC-8) | No native acknowledgement banner. A Login Flow can require "I agree" after sign-in. The My Domain login page can show text beside the login form | Login Flow on every profile requiring acknowledgement, plus the banner text on the login page | None |
| Network location | No FedRAMP Moderate value. Org-wide trusted IP ranges do not block anyone; profile login IP ranges deny every other address | Profile Login IP Ranges; enforce on every request | Only if remote agents connect through a VPN or fixed exit addresses. At minimum on admin and integration profiles | None set |
| Account deactivation | Disable accounts after 90 days of inactivity (AC-2(3)); act on a termination within 8 hours (AC-2(h)); disable high-risk accounts within 1 hour (AC-2(13)) | No native inactivity setting. Freeze stops logins immediately | A daily scheduled flow that deactivates users with no login in 90 days, plus an exceptions report. Offboarding runbook: freeze first, then deactivate | None |
| Access review | Privileged access quarterly, everyone else annually (AC-2(j)) | User, profile and permission set reports | Quarterly admin review, annual review for all users | None |
| Audit logging | Log admin activity, authentication, authorization, data access, changes and deletions (AU-2) | Setup Audit Trail, Login History and field history cover changes and logins. **Data access has no native log**; it needs Shield Event Monitoring | Shield Event Monitoring, which is authorized in Government Cloud Plus, and field history on the key objects | Defaults only |
| Audit retention | 6 months searchable, 12 months retrievable (OMB M-26-14) | Setup Audit Trail 180 days; Login History 6 months; field history 18 months (24 through the API); Event Monitoring log files 1 year | Event Monitoring, exported to Fred Hutch's security monitoring system. Without Shield, a monthly export of Setup Audit Trail and Login History | Defaults only |

## Where Salesforce falls short of the benchmark

| Gap | What we recommend |
| --- | --- |
| Privileged sessions must end after 10 minutes; Salesforce's shortest timeout is 15 | 15 minutes on admin profiles, plus a shorter screen lock on admin computers. Record it as a documented deviation, or as inherited from Salesforce if its customer responsibility matrix says so |
| No screening of new passwords against a compromised-password list | Record the gap. Built-in rules still block the username and very simple passwords |
| Salesforce's password security question conflicts with SP 800-63B-4 | Set the question to "cannot contain password" and obscure the answer. Record the conflict |
| No time window on failed-login counting | Record as not configurable |
| No native 90-day inactivity deactivation | The scheduled flow above |
| Native log retention stops at 6 months for setup and login history | Shield Event Monitoring or the monthly export above |

## Needed from Fred Hutch and NCI

| Item | Why |
| --- | --- |
| NCI's control values from its system authorization or security plan | They override every value above |
| Oracle production's IP restriction and login hours settings | A starting point where FedRAMP Moderate sets no value |
| The approved system use banner text | NCI or HHS wording for the login banner |
| Whether remote agents connect through a VPN or fixed exit addresses | Decides whether profile IP ranges are usable |
| Log retention period, the security monitoring system logs go to, and a decision on Shield | Audit retention cannot reach 12 months natively |
| The admin workday and agent login-hours window | Login hours per profile |
| The offboarding process that notifies the Salesforce admins | The 8-hour and 1-hour deactivation deadlines |
| The screen-lock policy on agent and admin computers | Covers the device-lock part of AC-11 and the 10-minute privileged gap |
| Named owners for access reviews and unusual-activity alerts | AC-2 reviews need a named owner |
| Access to Salesforce's Government Cloud Plus compliance documentation | Holds the customer responsibility split, which confirms what Salesforce already covers |

## Sources

| Claim | Source |
| --- | --- |
| Legacy Moderate values and the June 2026 legacy notice | FedRAMP legacy Rev 5 baseline spreadsheet, Moderate Baseline tab, `github.com/FedRAMP/docs-legacy` |
| 2026 rules | FedRAMP Consolidated Rules, `github.com/FedRAMP/rules`, version 2026.09.13.02 |
| Agency authorization documents what the agency configures | FedRAMP 2026 agency guidance, `github.com/FedRAMP/2026-markdown` |
| Passwords, lockout, session length | [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) |
| Log retention, M-21-31 rescinded | OMB Memorandum M-26-14, May 22, 2026 |
| Products authorized in Government Cloud Plus (Shield authorized; Salesforce Authenticator interoperable only) | [Salesforce Help 000396813](https://help.salesforce.com/s/articleView?id=000396813) |
| Phishing-resistant verification methods | [Salesforce Help 005321563](https://help.salesforce.com/s/articleView?id=005321563) and [available verifiers](https://help.salesforce.com/s/articleView?id=xcloud.mfa_config_available_verifiers.htm) |
| Password policy options | [Salesforce Help: password policies](https://help.salesforce.com/s/articleView?id=xcloud.admin_password.htm) |
| Session settings | [Salesforce Help: session settings](https://help.salesforce.com/s/articleView?id=xcloud.admin_sessions.htm) |
| Login flows | [Salesforce Help: login flows](https://help.salesforce.com/s/articleView?id=xcloud.security_login_flow.htm) |
| Login IP ranges and trusted IP ranges | [Profile login IP ranges](https://help.salesforce.com/s/articleView?id=platform.login_ip_ranges.htm), [network access](https://help.salesforce.com/s/articleView?id=xcloud.security_networkaccess.htm) |
| Login hours | [Salesforce Help: login hours](https://help.salesforce.com/s/articleView?id=platform.login_hours.htm) |
| Audit retention periods | [Setup Audit Trail](https://help.salesforce.com/s/articleView?id=xcloud.admin_monitorsetup.htm), [Login History](https://help.salesforce.com/s/articleView?id=xcloud.users_login_history.htm), [field history](https://help.salesforce.com/s/articleView?id=xcloud.tracking_field_history.htm) |
| Org today | Read-only queries against `FredHutch-GovCloud`, 2026-09-23 |

## Change log

| Date | Change |
| --- | --- |
| 2026-09-24 | FedRAMP Moderate governs over Oracle's current settings; Oracle is a starting point only where Moderate sets no value |
| 2026-09-24 | Created. FedRAMP Moderate benchmark mapped to Salesforce settings, gaps, and what Fred Hutch and NCI supply. Assumes no single sign-on, per the SOW |

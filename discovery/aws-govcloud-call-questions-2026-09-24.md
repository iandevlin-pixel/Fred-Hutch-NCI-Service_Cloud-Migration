# Questions for the AWS team: Amazon Connect and Salesforce Voice

- **Date:** 2026-09-24, for the CIS Contact Center Migration AWS GovCloud Discussion
- **From:** Kicksaw (Salesforce side)
- **Context:** Salesforce Voice with Partner Telephony, bring-your-own Amazon Connect in AWS GovCloud (`us-gov-west-1`). The AWS team builds and owns the Amazon Connect side. Kicksaw builds the Salesforce side and connects the two.

## Needed now

**1. Is the Amazon Connect instance being created with SAML 2.0 identity management?**

- Why: Salesforce connects only to Amazon Connect instances that use SAML identity management. AWS does not allow the identity option to change after the instance is created; changing it means deleting and recreating the instance, which loses its configuration.
- Sources:
  - Salesforce: [Set up Salesforce Voice with an existing Amazon Connect instance](https://help.salesforce.com/s/articleView?id=service.voice_existing_byoa_auto.htm) ("supports Amazon Connect instances of type SAML only")
  - AWS: [Plan your identity management in Amazon Connect](https://docs.aws.amazon.com/connect/latest/adminguide/connect-identity-management.html) ("You cannot change the option you select for identity management after you create an instance")

**2. What state is the instance in today?**

- Has it been created? Are any contact flows built or phone numbers claimed? Do the recording storage bucket, contact record stream and Contact Lens stream exist yet?
- Why: Salesforce setup reuses existing storage and streams, so knowing what exists avoids duplicate resources.
- Source: [Set up Salesforce Voice with an existing Amazon Connect instance](https://help.salesforce.com/s/articleView?id=service.voice_existing_byoa_auto.htm)

**3. When can Kicksaw receive the instance ID and the IAM role ARN for Salesforce?**

- The role needs Salesforce's GovCloud trust policy, which names Salesforce's GovCloud AWS account `383319876315`.
- Why: Kicksaw cannot create the contact center in Salesforce without both values.
- Source: [Salesforce Voice roles and policies](https://help.salesforce.com/s/articleView?id=service.voice_amazon_reference_roles_policies.htm)

## Design decisions to settle together

**4. Please confirm that voice routing lives in Amazon Connect.**

- Our working assumption is that queues, routing profiles and contact flows are built in Amazon Connect, and Salesforce shows the call to the agent. AWS described it this way in the 2026-09-15 discovery session.
- Why: both sides need the same answer before either one builds.

**5. Where does phone number porting stand?**

- Have porting requests started for the inbound numbers, and what is the cutover date?
- Two default quotas need raising for a 40 to 45 agent center: **phone numbers per instance (10)** and **concurrent active calls per instance (10)**. Increases can be requested only after the instance exists, and can take up to 3 weeks.
- Why: AWS asks for porting requests to be open "several months before pending go-live dates."
- Sources: [How long porting takes](https://docs.aws.amazon.com/connect/latest/adminguide/how-long-for-number-porting.html), [Amazon Connect service quotas](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-service-limits.html)

## Appendix: voicemail is not included in Amazon Connect

Amazon Connect is a contact center service and does not include voicemail. Voicemail has to be added as a separate solution, installed and configured in the Amazon Connect instance, with a way to deliver recordings to Salesforce. We're raising it now so nobody assumes it comes with the platform.

AWS's supported option is Voicemail Express, the successor to the retired Voicemail for Amazon Connect solution. Its project page says all components are available in AWS GovCloud and includes a GovCloud installation guide.

- Source: [Voicemail Express for Amazon Connect](https://github.com/amazon-connect/voicemail-express-amazon-connect)

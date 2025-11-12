# Forge release phases: EAP, Preview, and GA

At Atlassian, we aim to be transparent and clear in our roadmap. In line with this, we maintain a public Forge roadmap in Jira Product Discovery.

[View the Forge Roadmap](https://ecosystem.atlassian.net/jira/polaris/projects/ROADMAP/ideas/view/5062047)

We maintain this public roadmap to help shed insight on the future of the Forge platform. This roadmap is available for informational purposes only, and not as a binding commitment. For more information about the development status of specific features, you can reach out to us through the Forge developer community.

[Join the Forge developer community](https://community.developer.atlassian.com/c/forge/)

Before releasing high-impact features under General Availability (GA), we typically make them available under two categories:

* Forge Early Access Program (EAP)
* Forge Preview

## Forge Early Access Program (EAP)

Some features are available as part of the Forge Early Access Program (EAP). This program allows Forge users to provide feedback on features that are in the early stages of development. In turn, this provides us with insights that will help inform our development decisions. Ultimately, EAP participants help us validate our assumptions about a feature early in the development process.

Each EAP feature is managed by one engineering team within Atlassian. This team is responsible for:

* recruiting participants to test and review the EAP
* providing the documentation required to to do
* enabling and disabling the EAP feature for participants
* scheduling and announcing the start and end of the EAP

Whenever possible, EAP features will only be enabled on a participant's development environment. In addition, the team managing the EAP has full discretion on selecting participants.

### Disclaimer for use

Every EAP feature is still governed by the same policies and terms as the Forge platform. As such, EAP
participants acknowledge and abide by the following agreements:

As EAP features are under active development, they:

* are not supported or recommended for production use
* are subject to change any time, without notice
* may be cancelled or ended, without notice
* may contain bugs
* may be incomplete

Atlassian does not guarantee that any EAP features will be fully supported in the future. They are only available to selected users for demand, viability, and suitability testing. Releasing a feature as an EAP helps us gather insights that inform future development decisions.

For more information about the terms governing EAPs, see **Section 10** of the
[Atlassian Developer Terms](/platform/marketplace/atlassian-developer-terms/)

## Forge Preview

A Forge feature is in *preview* once we are confident that it's suitable and operationally supported for production apps. We release preview features so they can be studied, tested, and integrated by partners and developers prior to GA release. Preview features will also ship with public documentation and marked accordingly.

### Preview feature availability

Forge preview features are available to all users, and enjoy the same level of support as GA features. However, preview features are usually turned off by default (although they can be enabled on production environments); for instructions on enabling them, refer to their documentation.

### Preview deprecation

Any breaking changes to a preview feature are subject to a minimum 1-month deprecation period. This helps provide users with the necessary time to adapt to such changes. Once a preview feature transitions to GA, any breaking changes will be subject to a 6-month deprecation period.

## EAP, preview, and GA

The following table helps simplify the differences between EAP, preview, and GA features in terms of support, availability, and other criteria:

|  | EAP | Preview | GA |
| --- | --- | --- | --- |
| Documentation availability | Only to EAP participants | All Forge users | All Forge users |
| Feature availability | Only to EAP participants, and can only be enabled on development environments | All Forge users, and can be enabled on production environments | All Forge users |
| Operational commitment | No guarantees | Has passed Atlassian standards for stability, reliability, and security | Has passed Atlassian standards for stability, reliability, and security |
| Opt-in | Required | Required | Not required |
| Deprecation policy (for breaking changes) | None; feature may be changed or removed without notice | 1 month minimum deprecation | 6 months minimum deprecation |

In some cases, a critical security patch could involve disabling a preview or GA feature. When this occurs, the feature could be disabled without a deprecation period altogether. See [Forge deprecation policy](/platform/forge/deprecation-policy/) for related information.

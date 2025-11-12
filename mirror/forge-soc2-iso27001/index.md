# Forge and compliance with SOC 2 and ISO 27001

In partnership with [Vanta](https://www.vanta.com/), Atlassian conducted an analysis to determine how the Forge platform can make it easier for developers to meet System and Organization Controls (SOC) 2, and International Organization for Standardization (ISO) 27001 requirements, given that the Forge platform is SOC 2 attested and ISO 27001 certified.

Building apps on Forge can help you inherit controls to meet:

* **Up to 20% of ISO 27001 requirements** (focused on Annex A)
* **30% of SOC 2** (focused on Security, Availability, and Confidentiality Trust Services Criteria)

*Assuming the scope of each partner's assessment is their Forge application*.

To support this, below is a mapping of security domain areas with Atlassian security responsibilities, and the ISO 27001 and SOC 2 criteria these responsibilities help address:

| Vulnerability management | SOC 2 / ISO 27001 criteria |
| --- | --- |
| Ensuring the Forge platform infrastructure is hardened and providing a secure runtime for apps that prevents bypassing security controls | (SOC 2 - CC 6.6; ISO 27001 - A 8.18, A 8.26) |
| Scanning for security misconfiguration vulnerabilities | (SOC 2 - CC 7.1; ISO 27001 - A 8.8) |

| Access control | SOC 2 / ISO 27001 criteria |
| --- | --- |
| Ensuring that access to the underlying Forge platform components and related storage is restricted to authorized users | (SOC 2 - CC 6.1, 6.2,  6.3; ISO 27001 - A 8.2) |
| Configuring strict password policy and authentication configurations for access to the underlying Forge platform components and related storage | (SOC 2 - CC 6.1, 6.2, 6.3; ISO 27001 - A 8.5) |

| Physical security | SOC 2 / ISO 27001 criteria |
| --- | --- |
| Utilizing cloud service providers with strict physical protections, access, and redundancy configurations to provide the Forge platform | (SOC 2 - CC 6.4, 6.5; ISO 27001 - A 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.8, 7.10, 7.11, 7.12, 7.13, 7.14) |

| Network security | SOC 2 / ISO 27001 criteria |
| --- | --- |
| Using TLS 1.2 or higher to encrypt data in transit | (SOC 2 - CC 6.7; ISO 27001 - A 8.24) |
| CConfiguring network configurations for Forge platform components to only allow authorized network connections | (SOC 2 - CC 6.6; ISO 27001 - A 8.20, 8.21) |

| Logging, monitoring & alerting | SOC 2 / ISO 27001 criteria |
| --- | --- |
| Maintaining robust logging that includes an audit trail of actions performed by an app | (SOC 2 - CC 7.2; ISO 27001 - A 8.15) |
| Proactively monitor the health of the platform raising alerts in response to degraded performance, security, or abuse events | (SOC 2 - CC 7.2, A 1.1; ISO 27001 - A 8.6, 8.16) |

| Data security & availability | SOC 2 / ISO 27001 criteria |
| --- | --- |
| Using AES-256 to encrypt data at rest for data stored within Forge app storage. | (SOC 2 - CC 6.1; ISO 27001 - A 8.12, 8.24) |
| Ensuring data stored by Atlassian on behalf of your app (in Forge data storage) is backed up, and can be restored in an incident | (SOC 2 - CC 5.3, A 1.1; ISO 27001 - A 8.10, 8.13, 8.14) |

Please note that some of the responsibilities above include shared responsibilities. For example, while Forge manages the data stored on behalf of your Forge applications, you are responsible for backing up the code you deploy for the Forge application itself. You can review the [Shared responsibility model](/platform/forge/shared-responsibility-model/) for a full list of detailed responsibilities that you and Atlassian share when using the Forge platform.

The control domains above are also only a subset of the requirements for SOC 2 and ISO 27001 compliance. Many of the other requirements are based on operations and process needs that are outside the scope of the Forge platform. A great example of this is ISO 27001, which requires you to establish an **Information Security Management System (ISMS)** based on the standard's published clauses. Forge does not fulfil any of these clause requirements for you, so you must create your own security governance program for your organization.

## Shared responsibilities

While the Forge platform can assist with certain ISO 27001 shared responsibilities, it remains **your obligation** to ensure full compliance with all relevant ISO 27001 requirements.

Please review the information about Marketplace Partners—ISO 27001 responsibilities for additional details on the ISO 27001 requirements.

## Inherited controls

SOC 2 and ISO 27001 control inheritance only applies to data that resides within the Forge platform boundary.

Think of the Forge platform as a defined boundary. While your data and application reside within this boundary, they inherit the controls specified above. However, once any data leaves this boundary, the inheritance of those controls ceases for that data. You then become responsible for establishing your own controls for the data and system components outside the boundary.

## Key reminders

* **Shared responsibility**: Some controls are shared. For example, Atlassian backs up Forge-stored data, but you must back up your app code and any data outside Forge.
* **Boundary**: SOC 2 and ISO 27001 control inheritance only applies to data and apps within the Forge platform boundary. Once data leaves Forge (e.g., sent to a third-party API), you are responsible for its security and compliance.
* **Full compliance**: Forge helps you meet a subset of requirements, but you must ensure your organization meets all relevant SOC 2 and ISO 27001 requirements, including operational and process controls.

### Example

If you build an app that uses Forge's [runtime](/platform/forge/runtime-reference/), [hosted storage](/platform/forge/storage/) and has no data egress, you can rely on the SOC 2 and ISO 27001 control inheritance outlined above.

Let’s say you now update your app to make a call to a third-party API. The SOC 2 and ISO 27001 control inheritance ends for any data that leaves the Forge platform boundary and is sent to the third-party API. You now become responsible for implementing SOC 2 or ISO 27001 controls for the data that has left the boundary.

### Further reading

If you want to learn more about SOC 2 and ISO 27001, please visit the pages below:

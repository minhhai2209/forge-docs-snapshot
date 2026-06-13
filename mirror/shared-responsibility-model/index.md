# Shared responsibility model

Building a Forge app brings with it new capabilities and responsibilities
beyond those set out in the
[Cloud shared responsibility model](/developer-guide/cloud-shared-responsibility-model/).

For example, Forge apps can choose to implement one or more of the following
capabilities, which change the division of security responsibilities between
you and Atlassian.

* [Custom UI](/platform/forge/custom-ui/), which lets you define app user interfaces using
  static resources, such as HTML, CSS, JavaScript, and images.
* [UI kit](/platform/forge/ui-kit/), which lets you build intuitive and familiar app user interfaces by composing built-in Atlassian components.
* [Web triggers](/platform/forge/manifest-reference/modules/web-trigger/), which is
  a mechanism to invoke Forge applications through incoming HTTP calls.

This page is intended to help you understand your responsibilities when
building and supporting a Forge app, and what responsibilities Atlassian
takes care of. Also make sure you have read and are adhering to the [Developer terms](/platform/marketplace/atlassian-developer-terms/) and [Marketplace partner agreement](https://www.atlassian.com/licensing/marketplace/partneragreement).

## App elements

### Authentication of requests to the app

Ensure that every request made to the application is sufficiently authenticated.

**Your responsibilities**:

**Atlassian's responsibilities**:

* Authenticate the user before invoking your Forge application.

### Authorization of requests to the app

Ensure that every request made to the application is sufficiently authorized.

**Your responsibilities**

* You must use `asUser()` whenever you are performing an operation on behalf
  of a user. This ensures your app has at most the permissions of
  the calling user.
* Before making calls `asApp()`, you must verify expected permissions
  (for example, from Atlassian app context) with the permissions REST APIs
  before making the request.

**Atlassian's responsibilities**

* Ensure that only users with access to the site can interact with apps.

### Input validation and output encoding

Ensure sufficient input validation and output encoding is applied within the application.

**Your responsibilities**

**Atlassian's responsibilities:**

* Appropriately encode all HTML output for UI kit components.

### Application logic

**Your responsibilities**

### Application framework

Ensure the framework used to build apps is free of security bugs, and fixes
are delivered in line with [Atlassian's security bug fix policy SLOs](https://www.atlassian.com/trust/security/bug-fix-policy).

**Your responsibilities:**

* Ensure the frameworks used in your Custom UI app are up-to-date with
  the latest security patches.

**Atlassian's responsibilities**

* Apply secure development culture and practices when building the app framework.
* Remediate defects and vulnerabilities within the framework.
* Publish security bug fixes within the [security bug fix SLO](https://www.atlassian.com/trust/security/bug-fix-policy).

### Data storage

Ensure that data is appropriately stored and read by your app.

**Your responsibilities**

* Ensure that sensitive security data, such as pre-shared keys, API keys, or
  encryption keys are not hardcoded in the source code. Secure storage,
  such as encrypted environment variables, should be used to supply keys
  at runtime.
* Ensure that keys are rotated on a regular basis. You should rotate
  sensitive API keys at least every 90 days.
* Ensure that authorisation controls exist to segregate data access between
  different user roles within the same tenant.

**Atlassian's responsibilities**

* Encrypt data at rest for data stored within Forge app storage.
* Segregate data storage to prevent cross-tenant access. This includes Forge app storage.

### Software development lifecycle (SDLC) activities

[Apply secure software development practices](/platform/marketplace/app-security-guidelines/#software-development-lifecycle--sdlc--activities) when building and maintaining your app.

**Your responsibilities**

* Periodically scan for vulnerabilities in third-party dependencies using tools, such as
  [OWASP Dependency-Check](https://www.owasp.org/index.php/OWASP_Dependency_Check) or other similar tools.
* Perform regular [threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
  to identify and prioritize threats that may impact the security of your app.
* Perform static analysis of your app to identify patterns of insecure code.

### Tenant safety

Developers and Atlassian are jointly responsible for tenant safety. If your app is deployed on this runtime, the following responsibilities apply:

**Your responsibilities**

* Keep data in memory only within an invocation context. **Do not write tenant-specific data to
  module-level (global) variables** — the Forge runtime may reuse a warm execution process across
  multiple tenant invocations without clearing module-level state. Data stored in global variables
  during one tenant's invocation can persist into the next invocation, which may belong to a
  different tenant.
* If you use in-memory caches, always partition them by a tenant identifier such as `cloudId`. Do
  not use identifiers that are not globally unique (such as Jira issue keys) as global cache keys,
  because the same key can exist in multiple tenants' instances.
* Do not write tenant-specific data to the local filesystem in a way that persists after the
  invocation finishes.
* Prefer [Forge Storage](/platform/forge/storage/) for any data that must persist across
  invocations. Forge Storage is automatically scoped per app installation, making it inherently
  tenant-safe.

**Atlassian's responsibilities**

* An app installed on tenant A cannot request data from an app installed on tenant B.
* Segregate data storage to prevent cross-tenant access. This includes Forge app storage.

A common source of cross-tenant data leaks is module-level caching — a standard Node.js pattern
that is unsafe in Forge's shared runtime environment. See
[Tenant data isolation in Forge apps](/platform/forge/tenant-data-isolation/) for safe and unsafe
code examples, and an audit checklist for your app.

With the legacy runtime, Atlassian was responsible for tenant isolation. An app installed on tenant A
could not communicate with an app installed on tenant B.

## Operational elements

### Data residency

When listing your app on the Atlassian Marketplace with data residency support, ensure that you are correctly
declaring your app’s eligibility and data collection policy.

**Your responsibilities**

* Accurately define, document, and communicate what data is in-scope for data residency in your app listing’s
  Privacy and Security tab. See [In-Scope End-User Data](/platform/forge/data-residency/#in-scope-end-user-data)
  for more information.
* If your app uses any remote back ends, declare them in your manifest file with the properties matching their
  purpose. See [Remotes](/platform/forge/manifest-reference/remotes/#data-residency) for more information.

### Logging

**Your responsibilities**

* Ensure your application does not log personally identifiable information (PII),
  authentication tokens, and user-generated content (UGC), or confidential data.

**Atlassian's responsibilities**

* Maintain robust logging that includes an audit trail of actions performed by an app.
* Restrict access to logs based on organization permissions.

### Monitoring and alerting

**Atlassian's responsibilities**

* Proactively monitor the health of the platform raising alerts in response to
  degraded performance, security, or abuse events.

### Network security

**Atlassian's responsibilities**

* Use TLS to encrypt all traffic, including HSTS.
* Ensure data is appropriately handled. This includes ensuring
  caching of data does not negatively impact the security of apps or the platform.

### Runtime/Server security

**Atlassian's responsibilities**

* Ensure the platform infrastructure is hardened.
* Scan for security misconfiguration vulnerabilities.
* Provide a secure runtime for apps that prevents bypassing security controls.

### Vulnerability management and disclosure

**Your responsibilities**

**Atlassian's responsibilities**

* Disable applications that haven't mitigated vulnerabilities within [the set timelines](/platform/marketplace/security-bugfix-policy/).
* Mitigate security vulnerabilities in the platform within the
  [Security bug fix policy](https://www.atlassian.com/trust/security/bug-fix-policy).
* Communicate with Marketplace partners about vulnerabilities in the platform
  or applications that may affect their apps.

### Bug bounty

**Your responsibilities**

**Atlassian's responsibilities**

* Maintain a bug bounty program that includes the Forge platform in scope.

### Security incident response

Effective security incident response is a collaborative effort. You're responsible for promptly reporting incidents to Atlassian, keeping your security contacts up to date, acknowledging Atlassian's notifications, and containing incidents on your side. Atlassian provides triage and investigative support, ranging from asynchronous guidance to real-time joint collaboration where required.

**Your responsibilities**

* Establish a [security incident response plan](/platform/marketplace/app-security-incident-management-guidelines/)
  , so you are better prepared to respond to security breaches and incidents.
* Review and follow the [Partner Security Incident Response Program](/platform/marketplace/partner-security-incident-response-program/), which defines how to report incidents and how Atlassian shares platform logs during an incident.
* Detect and remediate incidents originating in systems you control, taking immediate action on discovery to limit impact (for example, rotating compromised credentials and shipping fixes).
* Promptly notify Atlassian upon discovery of any security incident in accordance with the [Atlassian developer terms](/platform/marketplace/atlassian-developer-terms/).
* Promptly respond to Atlassian-initiated incident notifications when Atlassian detects security issues involving your app.
* Keep security contact information up to date for timely mitigation of security incidents.
* Coordinate with Atlassian over the communication channels established for the incident, including asynchronous ticket updates, chat, or video calls.
* Notify your affected customers of confirmed incidents involving your app.
* Safely handle any logs that Atlassian shares with you in line with its data classification.

**Atlassian's responsibilities**

* Maintain a [security incident response plan](https://www.atlassian.com/trust/security/security-incident-management)
  that includes the ability to detect and respond to app security incidents.
* Proactively notify you when Atlassian detects a security incident that may affect your app or its customers.
* Provide incident triage and investigative support, ranging from asynchronous guidance on tickets to real-time joint collaboration over chat or video calls where required.
* Share the platform-side logs relevant to your app's activity, subject to privacy review and data-minimization.
* Coordinate the joint response, including discussing containment options and supporting customer notification where appropriate.

**Responsibilities per hosting model**

Incident response responsibilities depend on where your app runs. When your app runs entirely on our platform, Atlassian can fully support investigation, containment, and log sharing while you remediate your app and notify customers. For any components of your app that are hosted outside the Atlassian Platform (such as Forge Remote and Connect on Forge modules), you are responsible for detection, containment, and recovery on your infrastructure, while Atlassian provides platform-side investigative support and coordinates the joint response where required.

It is your responsibility to notify customers of incidents involving your app. For incidents originating from the Atlassian platform, Atlassian will coordinate with you on next steps.

| Responsibility | Detect | Contain | Fix | Notify Customers |
| --- | --- | --- | --- | --- |
| **Runs on Atlassian** | Atlassian & You | Atlassian & You | You | You |
| **Forge Remote** | You | You | You | You |
| **Connect on Forge** | You | You | You | You |

### Disaster recovery

**Your responsibilities**

* Establish a disaster recovery and business continuity plan to minimize or
  eliminate interruptions to the functioning of your apps during an incident.

**Atlassian's responsibilities**

* Ensure data stored by Atlassian on behalf of your app (in Forge data storage)
  is backed up, and can be restored in an incident.
* Maintain incident response plans.

## Security features

### User identity and access management

**Atlassian's responsibilities**

### DoS protection

**Atlassian's responsibilities**

* Detect DoS attacks against applications, or caused by applications.
* Mitigate DoS attacks against applications.
* Suspend apps that may be misbehaving/performing a high volume of requests.

### Abuse prevention

**Your responsibilities**

**Atlassian's responsibilities**

* Detect and mitigate apps that disrupt the normal operation of Forge or other Forge apps.
* Enforce platform limits (storage, request throughput, etc).

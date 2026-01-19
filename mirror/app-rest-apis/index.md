# Forge app REST APIs (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge app REST APIs let your app expose its own HTTP endpoints so that external systems can call
your app code running on Forge.

You can expose app REST APIs so that another system can call your app’s logic directly through a secure,
controlled endpoint. For example, you might expose an endpoint that lets a customers internal HR system read
employee data your app manages, or allow a reporting service to trigger a long‑running calculation
in your app.

Currently, this functionality is only available for Jira and Confluence apps, and is *not* available
for apps on Isolated Cloud.

This page explains what app REST APIs are in Forge, when to use them, and how they are secured.
For reference documentation and tutorials, see:

[API route

Reference for defining app REST API endpoints in your manifest using the apiRoute module.](/platform/forge/manifest-reference/modules/api-route/)

## What are app REST APIs?

A REST API is a way for software systems to communicate over HTTP using predictable URLs and standard methods like `GET`, `POST`, `PUT`, and `DELETE`.

In Forge, an **app REST API** is:

* An HTTP endpoint that belongs to a specific Forge app and environment.
* Defined in the app’s manifest using the [`apiRoute` module](/platform/forge/manifest-reference/modules/api-route/).
* Implemented by a Forge function that runs on Atlassian infrastructure.
* Protected by developer‑defined scopes and 3LO (OAuth 2.0) so only authorized callers can invoke it.

This is different from:

* **Atlassian app REST APIs**, which are the Atlassian-provided endpoints for Jira, Confluence, and other
  Atlassian apps that let you access and manage Atlassian app data. See [Atlassian app REST APIs](/platform/forge/apis-reference/product-rest-api-reference/).
* **Web triggers**, which expose a generic URL for a Forge function but do not use app‑defined scopes
  or the same admin controls as app REST APIs. See [Web triggers](/platform/forge/runtime-reference/web-trigger/).

Apps that expose Forge app REST APIs using `apiRoute` are eligible for
**Runs on Atlassian** status, provided they meet all other Runs on Atlassian requirements.

For more details, see [Runs on Atlassian](/platform/forge/runs-on-atlassian/).

## Use cases

As a Forge app developer, you should consider exposing app REST APIs when:

* You own domain‑specific data or logic in your app, and external systems need to **call your app**, not Jira or Confluence directly.
* You want your customers to integrate their internal tools with your app in a **supported, well‑defined, URL‑based** way.
* You need **strong, customer‑controlled security**, where:
  * The site/org admin must opt in to enabling the app’s REST APIs.
  * Customers can decide which exact app‑defined scopes a 3LO integration is allowed to use.
* You want a stable, readable URL structure for your app’s capabilities (for example, `/getEmployeeName`, `/employees/{id}`).

You would typically **not** use app REST APIs when:

* A simple inbound webhook using a **web trigger** is sufficient and you do not need app‑defined
  scopes or admin controls.
* Your integration pattern is primarily **event‑driven** (for example, reacting to Jira or Confluence
  events) and does not require external systems to invoke your app on demand.

## Implementation

Forge app REST APIs are defined and enforced by a combination of manifest configuration, app code, and admin/customer controls:

## Security and customer control

Forge app REST APIs are designed so customers remain in control of who can call their installed app and what data can be accessed.

### Admin controls

* For each site, app REST APIs are **disabled by default**.
* A site/org admin must explicitly enable a Forge app’s REST APIs in **Connected Apps** in [Atlassian Administration](https://admin.atlassian.com/).
* Admins can enable or disable this capability per site. Disabling it stops all app REST API calls for that site.

For detailed instructions, see [Access REST APIs exposed by a Forge app](/platform/forge/access-forge-rest-apis/#admin-enabling-of-rest-apis-in-a-forge-app).

### Security model

* App REST APIs use **3LO (OAuth 2.0)** as the security mechanism.
* Only **members of the site** where the app is installed can create the 3LO integration that is allowed to call the app’s REST APIs.
* During authorization, the customer chooses:
  * Which **app‑defined scopes** (for example, `read:employee:custom`) to grant.
  * Which **Atlassian app‑level Forge scopes** (for example, `read:forge-app:jira`) are needed.
* An access token is only issued once the customer consents; that token is required on every API call.

This means:

* External parties that are not members of the customer’s site cannot create 3LO integrations for the app.
* Even trusted integrations can only perform the actions and access the data covered by the scopes that the customer explicitly approved.

## Best practices

### Scopes

Developer-defined scopes are a key part of how app REST APIs are secured and should be designed with
care. Follow these best practices:

* **Keep scope names consistent**: Every developer-defined scope name must end with the suffix
  `:custom`.
* **Avoid excessive granularity**: There is a limit of 20 developer-defined scopes per app per
  environment. Avoid declaring overly granular scopes that are hard to manage over time.
* **Avoid overly broad scopes**: Don’t create generic catch‑all scopes just to future‑proof your
  APIs. Each scope should represent a clear, specific permission.
* **Use verb + noun naming**: Ideally, each scope name should contain:
  * A **verb** that indicates the action. For example, `read`, `write`, or `delete`.
  * A **noun** that indicates the object. For example, `employee`, `user`, or `payroll`.
  * Examples:
    * `read:employee:custom` for reading employee data.
    * `write:employee:custom` for writing employee data.
* **Only reuse scopes where it makes sense**: Reuse a scope across multiple APIs only when those
  APIs grant the same logical permission. For example, `write:employee:custom` might be reused by
  `/editEmployeeName` and `/editEmployeeDob`, but should not be used for `/getEmployeeName`, which
  should map to a read scope instead.

For details on how to declare and register developer-defined scopes in `custom-scopes.yaml`, see
[Expose Forge app REST APIs](/platform/forge/expose-forge-app-rest-apis/#step-1-declare-developer-defined-scopes).

### Documentation

If you are distributing this app to customers via Atlassian Marketplace, you will need to publish
developer documentation specifying the mapping between REST APIs and scopes for your Forge app.

This helps customers decide which scopes to grant when configuring access to your APIs.

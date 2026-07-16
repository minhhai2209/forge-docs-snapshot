# Build apps with the global:ui module (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.

To join the EAP for `global:ui`, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/19016?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzgyMzUxNTgzNDkwIiwic291cmNlIjoiY29uZmx1ZW5jZSJ9).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

An app that uses the `global:ui` module delivers its own end-to-end, full-page experience
within the Atlassian platform. Instead of extending a surface inside Jira or Confluence, the app
controls its own side navigation, gets its own place in the app switcher, and has a complete canvas
for your content, while the Atlassian platform provides the surrounding top navigation.

The `global:ui` module lets your app:

* Deliver a full-screen experience with side navigation that you control and top navigation provided
  by the Atlassian platform.
* Appear in the Atlassian app switcher, so users reach your app from anywhere in the platform.
* Connect to one or more Atlassian apps through [multi-app compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility), and optionally
  surface data across them.
* Build on platform capabilities such as Teamwork Graph, Forge Agents, Rovo Search, and Rovo Chat.

## Tutorials and examples

## Reference

## How it works

When you build a Forge app today, it lives inside an Atlassian app. A Jira issue panel, a Confluence
macro, or a project page extends the underlying Atlassian app surface, and its navigation,
installation, and licensing are all inherited from the host app.

An app that uses the `global:ui` module works differently. You install it through
[multi-app compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility)
with a required Atlassian app, such as Confluence. Once installed, the app
appears in the Atlassian app switcher alongside core Atlassian apps and can optionally connect to
additional Atlassian apps. Users experience the app as an independent, standalone tool, not as an add-on to an Atlassian app.

## Compared to embedded apps

|  | Embedded app | App using `global:ui` |
| --- | --- | --- |
| UI | Extends surfaces defined by the host app. | Provides an end-to-end UI experience with side navigation it controls, within the platform's top navigation. |
| Discoverability | Only accessible within a host app. | Discoverable in the Atlassian app switcher of the required Atlassian app. |
| Access | Inherited from the host app's user access. | Inherited from the required Atlassian app. Only users with access to the required Atlassian app can access the global:ui surface. |

## When to use the global:ui module

Consider using the `global:ui` module when:

* Users think of your app as a primary tool, not an add-on to an Atlassian app.
* Your app needs to work across multiple Atlassian apps, or deliver an independent workflow.
* You want users to navigate to your app directly from the Atlassian app switcher.

If your app's primary purpose is to extend a single Atlassian app (for example, adding a panel to a
Jira issue or embedding content in a Confluence page, an embedded app is likely the better fit).

## Use cases

Apps that use the `global:ui` module suit two broad categories of work.

**New end-to-end tasks targeting new customer verticals** - workflows that sit entirely outside the
scope of existing Atlassian apps:

* Technical architecture diagramming tools for software architects.
* Human resourcing and training campaign management.
* Logistics and route planning for field operations teams.

**New ways of managing existing tasks across multiple apps** - apps that consolidate or provide a
unified view of work spanning multiple Atlassian apps:

* Senior management dashboards that surface work across multiple Atlassian apps.
* Enterprise data backup and resilience tools.
* CRM and analytics tools that pull data from Jira and Confluence instances.

## The global:ui module compared to the full page module

Forge's full page module also provides a full-screen canvas. The two modules serve different purposes.

|  | Full page module | `global:ui` module |
| --- | --- | --- |
| Navigation | No built-in side or top navigation. | Integrates the Atlassian top navigation. Side navigation that can be configured. |
| Platform integration | Cannot be accessed from the app switcher. | Can be accessed from the app switcher. |

## Access and licensing

Access to the app is determined by the required Atlassian app declared in your manifest:

* Only users licensed to the **required Atlassian app** can access the `global:ui` surface and see the
  app in the app switcher.
* Unlicensed users cannot access the `global:ui` view or see the app switcher entry. They can still
  see embedded extension modules (such as `confluence:macro` or `jira:issuePanel`) that inherit their
  parent app's access permissions.

Licensing follows the same model as any other cross-app Forge app, so no new licensing setup is
needed. For more details, see [App compatibility](/platform/forge/app-compatibility/).

## EAP scope and limitations

This EAP releases the `global:ui` module on the existing [multi-app compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility) installation model. Keep the
following limitations in mind:

* **Installation model**: The EAP runs on multi-app compatibility, with one required Atlassian app. The same `global:ui` module is forward-compatible with the installation models that follow
  this phase.
* **Launch URLs are interim**: During the EAP, apps launch on an existing site hostname using a
  specific URL format. These URLs may change in a later phase. Set expectations accordingly and avoid
  hard-coding them. See [Access your app](/platform/forge/global-ui/global-ui-module/#access-your-app).
* **No Marketplace or production use**: Apps that use `global:ui` cannot be published to the
  Atlassian Marketplace or used in production during the EAP.

## Key terms

| Term | Meaning |
| --- | --- |
| `global:ui` module | The UI module that gives your app its own side navigation and main content area, plus a place in the Atlassian app switcher. |
| `global:ui` UI Kit components | The Forge-provided navigation components (`Global`, `Sidebar`, `Main`, `LinkMenuItem`, `ExpandableMenuItem`, and others) that you use within the `global:ui` module. |

For more details on required and optional Atlassian apps, see [App compatibility](/platform/forge/app-compatibility/).

## Next steps

Follow the [Getting started](/platform/forge/global-ui/getting-started/) tutorial to create your first
app with the `global:ui` module and deploy it to your Atlassian site.

Once you have a working app, see [Add custom content using Frame](/platform/forge/global-ui/frame-routing/)
to embed Custom UI in the main content area and wire up sidebar navigation.

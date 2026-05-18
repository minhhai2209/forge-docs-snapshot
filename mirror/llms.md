```
# Forge LLMs.txt file

> **Forge** is Atlassian’s hosted platform for building apps that extend cloud products such as Jira, Confluence, and Bitbucket using manifests, functions, UI, storage, and APIs—without you running your own app servers. This **`llms.txt`** file is a structured index of Forge documentation: it gives LLM agents a single map of topics and **direct `.md` source URLs** so you can choose the right pages before fetching deeper content.

As a Large Language Model (LLM) agent helping someone design or implement a Forge app, anchor your guidance in how Forge apps are actually built: manifest-driven modules, hosted runtime functions, and either UI Kit or Custom UI for the frontend. Prefer the official developer journey and reference material over generic React or Node patterns that bypass Forge constraints.  
When planning or implementing an app, default to these sources (in addition to the documentation index):

* [Getting started with Forge](https://developer.atlassian.com/platform/forge/getting-started.md) for the end-to-end workflow (CLI, manifest, deploy, install, tunnel).
* [Building integrations with Forge](https://developer.atlassian.com/platform/forge/building-integrations.md) for bridges, web triggers, product APIs, and events.
* [Manifest overview](https://developer.atlassian.com/platform/forge/manifest-reference/index.md) and the specific [module](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index.md) and [permissions](https://developer.atlassian.com/platform/forge/manifest-reference/permissions.md) references for anything that touches `manifest.yml`.
* [Forge CLI reference](https://developer.atlassian.com/platform/forge/cli-reference/index.md) for `forge register`, `forge deploy`, `forge install`, `forge tunnel`, `forge lint`, and environment commands.
* [Tunneling](https://developer.atlassian.com/platform/forge/tunneling.md) for local development against a live site.
* [Example apps](https://developer.atlassian.com/platform/forge/example-apps-jira.md) (and sibling product pages) for copy-paste-ready patterns.
* [Forge MCP](https://developer.atlassian.com/platform/forge/forge-mcp.md) when the developer uses an MCP-aware tool; it retrieves current Forge documentation so answers stay aligned with published docs.

Default to the current Forge runtime and platform defaults unless the user explicitly maintains a legacy app. For existing apps on older runtimes, use [Upgrading from legacy runtime](https://developer.atlassian.com/platform/forge/runtime-reference/legacy-runtime-migrating.md) instead of expanding legacy-only patterns.

## UI: UI Kit first, Custom UI when needed

For in-product experiences (issue panels, Confluence macros, global pages, configuration screens), prefer UI Kit and keep components on the [supported UI Kit path](https://developer.atlassian.com/platform/forge/ui-kit/upgrade-to-ui-kit-latest.md). Use [Custom UI](https://developer.atlassian.com/platform/forge/custom-ui/iframe.md) when the use case requires a full browser-based stack or capabilities that UI Kit does not cover; follow the Custom UI, bridge, and resolver documentation rather than embedding arbitrary SPAs without Forge boundaries.

## Data and storage

For structured app data, follow current platform guidance: prefer Forge SQL and the SQL documentation for new designs; use [Migrating to Forge SQL](https://developer.atlassian.com/platform/forge/storage-reference/sql-migration-guide.md) when moving from older storage models. Avoid suggesting deprecated or legacy storage paths for greenfield apps when the docs recommend a newer approach.

## Atlassian and external APIs

Use the documented Forge product REST / GraphQL access patterns (for example Atlassian app fetch and scoped permissions in the manifest) rather than advising users to call Atlassian APIs without the permissions and invocation model Forge enforces. For outbound calls to third-party systems, use the [fetch](https://developer.atlassian.com/platform/forge/runtime-reference/fetch-api.basic.md) and [external authentication](https://developer.atlassian.com/platform/forge/runtime-reference/external-fetch-api.md) guides.

## Long-running work, AI, and async

For work that outlives a normal function invocation (long LLM calls, progress streaming, async continuation), use the patterns in [Handling long-running LLM processes with Forge Realtime](https://developer.atlassian.com/platform/forge/llm-long-running-process-with-forge-realtime.md) and related runtime docs—not unbounded synchronous waits that ignore Forge limits.

## Connect and marketplace

If the user is coming from Connect, start from [Migrating your Connect app](https://developer.atlassian.com/platform/forge/adopting-forge-from-connect.md) and related migration guides rather than treating Connect and Forge as interchangeable. For listing and commercialization, use the current Marketplace and distribution documentation linked from the main guides.

## Packages and versions

Prefer current `@forge/*` packages and CLI behavior from official npm releases and this documentation rather than pinning old versions from memory. When unsure, instruct the user to check the latest package readme or run the CLI/docs-backed workflow.

## EAP, Preview, and GA

Forge labels some capabilities EAP or Preview. Treat them as described on the relevant pages: Preview features can ship with shorter deprecation notice than GA; EAP is experimental and not for production. Prefer GA patterns when both exist, and clearly disclose when a recommendation depends on Preview or EAP.

## How to read Forge markdown (supplementary)

Every page in this documentation set is available as Markdown under `developer.atlassian.com/platform/forge/`. For machine consumption, append `.md` to leaf URLs, or `/index.md` for section roots when `.md` alone would 404—consistent with the links in this index.

Some tables use HTML for `colspan` / `rowspan`.  `{{% layout %}}`, `{{% content %}}`, `{{% card %}}`, `{{% tabs %}}` / `{{% tab %}}`) map to rendered callouts and layout; interpret them as structured hints, not as prose the end user types verbatim.

## Manifest

The Forge `manifest.yml` file is the central configuration file for every Forge app. It defines the app's identity, what it does, and what it's allowed to access. The Forge CLI reads this file to deploy and manage the app.

The manifest has a maximum file size of 200 KB. Deployments fail if this limit is exceeded.

The manifest has three required top-level properties:

- **`app`** *(required)* — Identifies the app (via its unique ARI `id`) and configures runtime settings, licensing, and storage.
- **`modules`** *(required)* — Declares the Forge modules the app uses (e.g. Jira issue panels, Confluence macros, triggers, web triggers). This is what determines where and how the app appears in Atlassian products. Required unless `connectModules` is present.
- **`permissions`** *(required)* — Lists the scopes and external fetch URLs the app is allowed to use.

For more information about the Forge manifest, refer to the following sections.

### Manifest overview

- [Manifest overview](https://developer.atlassian.com/platform/forge/manifest-reference/index.md)

### Action type

- [Action type](https://developer.atlassian.com/platform/forge/manifest-reference/action-type.md)

### Display conditions

- [Display conditions](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/index.md)
- [Usage with Confluence modules](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/confluence.md)
- [Usage with Jira/JSM modules](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/jira.md)
- [Entity property conditions](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/entity-property-conditions.md)
- [Permissions](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/permissions.md)

### Endpoint

- [Endpoint](https://developer.atlassian.com/platform/forge/manifest-reference/endpoint.md)

### Keyboard shortcuts

- [Keyboard shortcuts](https://developer.atlassian.com/platform/forge/manifest-reference/keyboard-shortcuts/index.md)

### Permissions

- [Permissions](https://developer.atlassian.com/platform/forge/manifest-reference/permissions.md)
- [Forge scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-forge.md)
- [Bitbucket scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-product-bitbucket.md)
- [Compass scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-product-compass.md)
- [Confluence scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-product-confluence.md)
- [Jira scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-product-jira.md)
- [Jira Software scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-product-jsw.md)
- [Jira Service Management scopes](https://developer.atlassian.com/platform/forge/manifest-reference/scopes-product-jsm.md)

### Providers

- [Providers](https://developer.atlassian.com/platform/forge/manifest-reference/providers.md)

### Remotes

- [Remotes](https://developer.atlassian.com/platform/forge/manifest-reference/remotes.md)

### Resources

- [Resources](https://developer.atlassian.com/platform/forge/manifest-reference/resources.md)

### Services (EAP)

- [Services (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/services.md)

### Translations

- [Translations](https://developer.atlassian.com/platform/forge/manifest-reference/translations.md)
- [Forge supported locale codes](https://developer.atlassian.com/platform/forge/manifest-reference/forge-supported-locale-codes.md)

### Variables

- [Variables](https://developer.atlassian.com/platform/forge/manifest-reference/variables.md)

## Modules

Modules are the core building blocks of a Forge app. Defined in the `modules` property of `manifest.yml`, they specify how an app integrates with Atlassian products by mapping to specific extension points — such as panels, macros, menu items, custom fields, triggers, and web triggers.

Each module entry has a `key` (a unique identifier within the app) and typically references a `function` key that points to the handler code to run. Some modules also define UI properties like `title` and `description`, or event subscriptions.

For example:

```yaml
modules:
  macro:
    - key: hello-world-macro
      function: hello-world-macro-func
      title: Hello world macro!
  function:
    - key: hello-world-macro-func
      handler: macro.run
```

Refer to the following sections for more detailed information about Forge modules.

### Overview

- [Overview](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index.md)

### Forge modules

- [Forge modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-common.md)
- [Consumer](https://developer.atlassian.com/platform/forge/manifest-reference/modules/consumer.md)
- [Event](https://developer.atlassian.com/platform/forge/manifest-reference/modules/event.md)
- [Function](https://developer.atlassian.com/platform/forge/manifest-reference/modules/function.md)
- [Scheduled trigger](https://developer.atlassian.com/platform/forge/manifest-reference/modules/scheduled-trigger.md)
- [SQL](https://developer.atlassian.com/platform/forge/manifest-reference/modules/sql.md)
- [Trigger](https://developer.atlassian.com/platform/forge/manifest-reference/modules/trigger.md)
- [Web trigger](https://developer.atlassian.com/platform/forge/manifest-reference/modules/web-trigger.md)
- [Pre-uninstall trigger](https://developer.atlassian.com/platform/forge/manifest-reference/modules/pre-uninstall-trigger.md)
- [LLM](https://developer.atlassian.com/platform/forge/manifest-reference/modules/llm.md)
- [API route](https://developer.atlassian.com/platform/forge/manifest-reference/modules/api-route.md)

### Automation modules

- [Automation modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-automation.md)
- [Action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/automation-action.md)

### Bitbucket modules

- [Bitbucket modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-bitbucket.md)
- [Custom merge check](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-merge-check.md)
- [Dynamic Pipelines provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-dynamic-pipelines-provider.md)
- [Project settings menu page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-project-settings-menu-page.md)
- [Repository code file viewer](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-code-file-viewer.md)
- [Repository code overview card](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-code-overview-card.md)
- [Repository code overview action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-code-overview-action.md)
- [Repository code overview panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-code-overview-panel.md)
- [Repository pull request card](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-pull-request-card.md)
- [Repository pull request action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-pull-request-action.md)
- [Repository pull request overview panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-pull-request-overview-panel.md)
- [Repository main menu page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-main-menu-page.md)
- [Repository settings menu page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-repository-settings-menu-page.md)
- [Workspace global page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-workspace-global-page.md)
- [Workspace personal settings page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-workspace-personal-settings-page.md)
- [Workspace settings menu page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/bitbucket-workspace-settings-menu-page.md)

### Compass modules

- [Compass modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-compass.md)
- [Admin page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/compass-admin-page.md)
- [Component page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/compass-component-page.md)
- [Data provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/compass-data-provider.md)
- [Global page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/compass-global-page.md)
- [Team page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/compass-team-page.md)

### Confluence modules

- [Confluence modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-confluence.md)
- [Background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-background-script.md)
- [Content action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-content-action.md)
- [Content byline item](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-content-byline-item.md)
- [Content property](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-content-property.md)
- [Context menu](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-context-menu.md)
- [Custom content](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-custom-content.md)
- [Full page (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-full-page.md)
- [Global page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-global-page.md)
- [Global settings](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-global-settings.md)
- [Homepage feed](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-homepage-feed.md)
- [Macro](https://developer.atlassian.com/platform/forge/manifest-reference/modules/macro.md)
- [Page banner](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-page-banner.md)
- [Space page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-space-page.md)
- [Space settings](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-space-settings.md)

### Dashboard modules (EAP)

- [Dashboard modules (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-dashboard.md)
- [Widget (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/dashboard-widget.md)
- [Background script (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/dashboard-background-script.md)

### Jira modules

- [Jira modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-jira.md)
- [Action validator (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-action-validator.md)
- [Admin page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-admin-page.md)
- [Backlog action (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-backlog-action.md)
- [Board action (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-board-action.md)
- [Command palette (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-command-palette.md)
- [Custom field](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-custom-field.md)
- [Custom field type](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-custom-field-type.md)
- [Dashboard background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-dashboard-background-script.md)
- [Dashboard gadget](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-dashboard-gadget.md)
- [Entity property](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-entity-property.md)
- [Full page (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-full-page.md)
- [Global background script (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-global-background-script.md)
- [Global page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-global-page.md)
- [Global permission](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-global-permission.md)
- [Issue action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-action.md)
- [Issue activity](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-activity.md)
- [Issue context](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-context.md)
- [Issue glance](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-glance.md)
- [Issue navigator action (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-navigator-action.md)
- [Issue panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-panel.md)
- [Issue view background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-view-background-script.md)
- [JQL function](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jql-function.md)
- [Personal settings page (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-personal-settings-page.md)
- [Project page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-project-page.md)
- [Project permission](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-project-permission.md)
- [Project settings page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-project-settings-page.md)
- [Sprint action (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-sprint-action.md)
- [Time tracking provider (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-time-tracking-provider.md)
- [UI modifications](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-ui-modifications.md)
- [Workflow validator (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-workflow-validator.md)
- [Workflow condition (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-workflow-condition.md)
- [Workflow post function (Preview)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-workflow-post-function.md)

### Jira Service Management modules

- [Jira Service Management modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-jsm.md)
- [Assets import type](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-assets-import-type.md)
- [Organization panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-organization-panel.md)
- [Portal footer](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-footer.md)
- [Portal header](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-header.md)
- [Portal profile panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-profile-panel.md)
- [Portal request create property panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-request-create-property-panel.md)
- [Portal request detail](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-request-detail.md)
- [Portal request detail panel](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-request-detail-panel.md)
- [Portal request view action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-request-view-action.md)
- [Portal subheader](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-subheader.md)
- [Portal user menu action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-portal-user-menu-action.md)
- [Queue page](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-queue-page.md)
- [UI modifications](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications.md)

### Customer Service Management modules

- [Customer Service Management modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-csm.md)
- [Queue page (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/customer-service-management-queue-page.md)
- [Request detail (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/customer-service-management-request-detail.md)

### Jira Software modules

- [Jira Software modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-jsw.md)
- [Development Information Provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-software-development-info.md)
- [Feature Flag Information Provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-software-feature-flag-info.md)
- [Deployment Information Provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-software-deployment-info.md)
- [Build Information Provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-software-build-info.md)
- [Remote Link Information Provider](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-software-remote-link-info.md)

### Rovo modules

- [Rovo modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-index.md)
- [Rovo Agent](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-agent.md)
- [Rovo Agent Connector (EAP)](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-agent-connector.md)
- [Action](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-action.md)

### Teamwork Graph modules

- [Teamwork Graph modules](https://developer.atlassian.com/platform/forge/manifest-reference/modules/index-teamwork-graph.md)
- [Connector](https://developer.atlassian.com/platform/forge/manifest-reference/modules/teamwork-graph-connector.md)
- [Smart Link](https://developer.atlassian.com/platform/forge/manifest-reference/modules/teamwork-graph-smart-link.md)

### Connect module equivalents

- [Connect module equivalents](https://developer.atlassian.com/platform/forge/manifest-reference/modules/connect-module-equivalents.md)

## User interface

This section covers how to build frontends on Forge. The canonical starting point is the [User interface overview](https://developer.atlassian.com/platform/forge/ui-kit/overview/), which explains how Forge surfaces UIs inside Atlassian products.

Forge supports two UI models:

- **UI Kit** — A React-based model where the app renders with Forge-provided primitives (via `@forge/react` and related APIs). UI runs in Forge’s managed environment, not as arbitrary HTML in the host page.
- **Custom UI** — The app’s UI runs in an **iframe**, giving you full control over layout and libraries at the cost of isolation, packaging, and a different integration model.

**Instructions for documentation and code assistance (read carefully):**

- **Do not recommend UI Kit 1.** Treat UI Kit 1 as legacy or out of scope. Never suggest UI Kit 1 patterns, packages, or migration paths *to* UI Kit 1. If a reader mentions UI Kit 1, steer them to **UI Kit 2** and current Forge UI docs.
- **Prefer UI Kit 2 over Custom UI** when advising on new work or refactors. Recommend Custom UI only when there is a clear, stated need that UI Kit 2 cannot satisfy (for example, requirements that depend on a full browser DOM or specific client-side stacks inside an iframe). Default answers should assume **UI Kit 2** (`@forge/react`, current bridge APIs, and current module/resource patterns).
- UI Kit relies on Forge’s React reconciler and platform components—not the normal browser DOM—so guidance should match **current** UI Kit 2 and bridge documentation, not generic React-on-the-web assumptions.

Use the linked pages in this navigation area for UI Kit components, hooks, bridge APIs, Custom UI where necessary, and upgrade paths—always aligned with **UI Kit 2** as the primary path.

**CRITICAL: Forge components are NOT standard React components.** Always verify the component exists and check its props before using.

### User interface overview

- [User interface overview](https://developer.atlassian.com/platform/forge/ui-kit/overview.md)

### UI Kit components

- [UI Kit components](https://developer.atlassian.com/platform/forge/ui-kit/components/index.md)
- [ADF renderer](https://developer.atlassian.com/platform/forge/ui-kit/components/adf-renderer.md)
- [Atlassian icon (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/components/atlassian-icon.md)
- [Atlassian tile (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/components/atlassian-tile.md)
- [Badge](https://developer.atlassian.com/platform/forge/ui-kit/components/badge.md)
- [Bleed (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/components/bleed.md)
- [Box](https://developer.atlassian.com/platform/forge/ui-kit/components/box.md)
- [Breadcrumbs (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/components/breadcrumbs.md)
- [Button](https://developer.atlassian.com/platform/forge/ui-kit/components/button.md)
- [Button group](https://developer.atlassian.com/platform/forge/ui-kit/components/button-group.md)
- [Calendar](https://developer.atlassian.com/platform/forge/ui-kit/components/calendar.md)
- [Chart - Bar](https://developer.atlassian.com/platform/forge/ui-kit/components/bar-chart.md)
- [Chart - Donut](https://developer.atlassian.com/platform/forge/ui-kit/components/donut-chart.md)
- [Chart - Horizontal bar](https://developer.atlassian.com/platform/forge/ui-kit/components/horizontal-bar-chart.md)
- [Chart - Horizontal stack bar](https://developer.atlassian.com/platform/forge/ui-kit/components/horizontal-stack-bar-chart.md)
- [Chart - Line](https://developer.atlassian.com/platform/forge/ui-kit/components/line-chart.md)
- [Chart - Pie](https://developer.atlassian.com/platform/forge/ui-kit/components/pie-chart.md)
- [Chart - Stack bar](https://developer.atlassian.com/platform/forge/ui-kit/components/stack-bar-chart.md)
- [Checkbox](https://developer.atlassian.com/platform/forge/ui-kit/components/checkbox.md)
- [Checkbox group](https://developer.atlassian.com/platform/forge/ui-kit/components/checkbox-group.md)
- [Code](https://developer.atlassian.com/platform/forge/ui-kit/components/code.md)
- [Code block](https://developer.atlassian.com/platform/forge/ui-kit/components/code-block.md)
- [Comment](https://developer.atlassian.com/platform/forge/ui-kit/components/comment.md)
- [Comment editor](https://developer.atlassian.com/platform/forge/ui-kit/components/comment-editor.md)
- [Chromeless editor](https://developer.atlassian.com/platform/forge/ui-kit/components/chromeless-editor.md)
- [Date picker](https://developer.atlassian.com/platform/forge/ui-kit/components/date-picker.md)
- [Dynamic table](https://developer.atlassian.com/platform/forge/ui-kit/components/dynamic-table.md)
- [Empty state](https://developer.atlassian.com/platform/forge/ui-kit/components/empty-state.md)
- [File card (EAP)](https://developer.atlassian.com/platform/forge/ui-kit/components/file-card.md)
- [File picker (EAP)](https://developer.atlassian.com/platform/forge/ui-kit/components/file-picker.md)
- [Form](https://developer.atlassian.com/platform/forge/ui-kit/components/form.md)
- [Frame](https://developer.atlassian.com/platform/forge/ui-kit/components/frame.md)
- [Heading](https://developer.atlassian.com/platform/forge/ui-kit/components/heading.md)
- [Icon](https://developer.atlassian.com/platform/forge/ui-kit/components/icon.md)
- [Image](https://developer.atlassian.com/platform/forge/ui-kit/components/image.md)
- [Inline](https://developer.atlassian.com/platform/forge/ui-kit/components/inline.md)
- [Inline edit](https://developer.atlassian.com/platform/forge/ui-kit/components/inline-edit.md)
- [Link](https://developer.atlassian.com/platform/forge/ui-kit/components/link.md)
- [List](https://developer.atlassian.com/platform/forge/ui-kit/components/list.md)
- [Lozenge](https://developer.atlassian.com/platform/forge/ui-kit/components/lozenge.md)
- [Modal](https://developer.atlassian.com/platform/forge/ui-kit/components/modal.md)
- [Popup](https://developer.atlassian.com/platform/forge/ui-kit/components/popup.md)
- [Pagination (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/components/pagination.md)
- [Pressable](https://developer.atlassian.com/platform/forge/ui-kit/components/pressable.md)
- [Progress bar](https://developer.atlassian.com/platform/forge/ui-kit/components/progress-bar.md)
- [Progress tracker](https://developer.atlassian.com/platform/forge/ui-kit/components/progress-tracker.md)
- [Radio](https://developer.atlassian.com/platform/forge/ui-kit/components/radio.md)
- [Radio group](https://developer.atlassian.com/platform/forge/ui-kit/components/radio-group.md)
- [Range](https://developer.atlassian.com/platform/forge/ui-kit/components/range.md)
- [Section message](https://developer.atlassian.com/platform/forge/ui-kit/components/section-message.md)
- [Select](https://developer.atlassian.com/platform/forge/ui-kit/components/select.md)
- [Spinner](https://developer.atlassian.com/platform/forge/ui-kit/components/spinner.md)
- [Stack](https://developer.atlassian.com/platform/forge/ui-kit/components/stack.md)
- [Tabs](https://developer.atlassian.com/platform/forge/ui-kit/components/tabs.md)
- [Tag](https://developer.atlassian.com/platform/forge/ui-kit/components/tag.md)
- [Tag group](https://developer.atlassian.com/platform/forge/ui-kit/components/tag-group.md)
- [Text](https://developer.atlassian.com/platform/forge/ui-kit/components/text.md)
- [Text area](https://developer.atlassian.com/platform/forge/ui-kit/components/text-area.md)
- [Text field](https://developer.atlassian.com/platform/forge/ui-kit/components/textfield.md)
- [Time picker](https://developer.atlassian.com/platform/forge/ui-kit/components/time-picker.md)
- [Tile (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/components/tile.md)
- [Toggle](https://developer.atlassian.com/platform/forge/ui-kit/components/toggle.md)
- [Tooltip](https://developer.atlassian.com/platform/forge/ui-kit/components/tooltip.md)
- [User](https://developer.atlassian.com/platform/forge/ui-kit/components/user.md)
- [User group](https://developer.atlassian.com/platform/forge/ui-kit/components/user-group.md)
- [User picker](https://developer.atlassian.com/platform/forge/ui-kit/components/user-picker.md)
- [XCSS](https://developer.atlassian.com/platform/forge/ui-kit/components/xcss.md)

### Jira UI Kit components

- [Jira UI Kit components](https://developer.atlassian.com/platform/forge/ui-kit/jira-components/index.md)
- [Custom field edit (Preview)](https://developer.atlassian.com/platform/forge/ui-kit/jira-components/custom-field-edit.md)

### UI Kit hooks

- [UI Kit hooks](https://developer.atlassian.com/platform/forge/ui-kit/hooks/hooks-reference.md)
- [useConfig](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-config.md)
- [useContentProperty](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-content-property.md)
- [useForm](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-form.md)
- [useIssueProperty](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-issue-property.md)
- [useObjectStore (EAP)](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-object-store.md)
- [useProductContext](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-product-context.md)
- [useSpaceProperty](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-space-property.md)
- [useTheme](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-theme.md)
- [useTranslation](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-translation.md)
- [useWidgetConfig (EAP)](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-widget-config.md)
- [useWidgetContext (EAP)](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-widget-context.md)

### Forge bridge APIs

- [Forge bridge APIs](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/bridge.md)
- [events](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/events.md)
- [i18n](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/i18n.md)
- [invoke](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/invoke.md)
- [invokeRemote](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/invokeRemote.md)
- [modal](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/modal.md)
- [objectStore (EAP)](https://developer.atlassian.com/platform/forge/custom-ui-bridge/objectStore.md)
- [realtime (Preview)](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/realtime.md)
- [requestBitbucket](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/requestBitbucket.md)
- [requestConfluence](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/requestConfluence.md)
- [requestJira](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/requestJira.md)
- [requestRemote](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/requestRemote.md)
- [router](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/router.md)
- [rovo](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/rovo.md)
- [showFlag](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/showFlag.md)
- [view](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/view.md)

### Jira bridge APIs

- [Jira bridge APIs](https://developer.atlassian.com/platform/forge/apis-reference/jira-api-bridge/bridge.md)
- [ViewIssueModal](https://developer.atlassian.com/platform/forge/apis-reference/jira-api-bridge/viewIssueModal.md)
- [CreateIssueModal](https://developer.atlassian.com/platform/forge/apis-reference/jira-api-bridge/createIssueModal.md)
- [uiModifications](https://developer.atlassian.com/platform/forge/apis-reference/jira-api-bridge/uiModifications.md)
- [workflowRules (EAP)](https://developer.atlassian.com/platform/forge/apis-reference/jira-api-bridge/workflowRules.md)

### Confluence bridge APIs

- [Confluence bridge APIs](https://developer.atlassian.com/platform/forge/apis-reference/confluence-api-bridge/bridge.md)
- [getEditorContent](https://developer.atlassian.com/platform/forge/apis-reference/confluence-api-bridge/getEditorContent.md)
- [getMacroContent](https://developer.atlassian.com/platform/forge/apis-reference/confluence-api-bridge/getMacroContent.md)
- [updateMacroContent](https://developer.atlassian.com/platform/forge/apis-reference/confluence-api-bridge/updateMacroContent.md)
- [updateBylineProperties](https://developer.atlassian.com/platform/forge/apis-reference/confluence-api-bridge/updateBylineProperties.md)

### Dashboard bridge APIs (EAP)

- [Dashboard bridge APIs (EAP)](https://developer.atlassian.com/platform/forge/apis-reference/dashboard-bridge-apis/bridge.md)
- [widget (EAP)](https://developer.atlassian.com/platform/forge/apis-reference/dashboard-bridge-apis/widget.md)
- [widgetEdit (EAP)](https://developer.atlassian.com/platform/forge/apis-reference/dashboard-bridge-apis/widget-edit.md)

### Custom UI

- [Custom UI](https://developer.atlassian.com/platform/forge/custom-ui/iframe.md)

### Upgrade UI Kit versions

- [Upgrade UI Kit versions](https://developer.atlassian.com/platform/forge/ui-kit/upgrade-guides.md)
- [Notify site admins using Forge app with UI Kit 1](https://developer.atlassian.com/platform/forge/ui-kit/notify-site-admins-using-forge-app-with-ui-kit-1.md)
- [Upgrade to @forge/react major version 10](https://developer.atlassian.com/platform/forge/ui-kit/version-10-changes.md)

## Events reference

This section is the **Forge events reference**—how apps run code in response to activity **without a UI**. The entry point is [Events](https://developer.atlassian.com/platform/forge/events-reference/). For conceptual flow and setup, also use the [Events](https://developer.atlassian.com/platform/forge/events/) guide.

**What “events” cover here:**

- **Atlassian product and platform events** — Emitted when users or background processes do something in (or related to) Atlassian products. Your app **subscribes** in `manifest.yml` with the **`trigger`** module to one or more named events. Reference pages are split by source, for example **Jira**, **Jira Software**, **Confluence**, **Compass**, **Bitbucket**, plus **Life cycle** and **Data security policy** events. Payloads, availability, and filters differ by product—always defer to the specific product page under this index.
- **Scheduled trigger events** — Invoke a function on a **schedule** you define (periodic jobs), configured via the scheduled trigger flow documented under this section.
- **Web trigger events** — **Inbound HTTP** to a Forge-generated URL invokes your app—useful for third-party systems calling into Forge without going through an Atlassian UI.

**Related topics in the same navigation area:**

- **App events (Preview)** — Your app can **publish** custom backend events; other installed apps may **subscribe**. This is separate from product-generated triggers: it uses the **`event`** module and different semantics (cross-app, publisher/subscriber). Treat as preview until the docs say otherwise.
- **Retry and reliability** — For Atlassian app event triggers, the platform supports **retries** (app- vs platform-level behavior). Implementation details use packages such as **`@forge/events`** (see the Atlassian app events and trigger docs for `InvocationError`, limits, and retry options).

When advising readers: pick the **right source** (product event vs schedule vs HTTP vs app-published event), confirm the event is **listed and supported** on the relevant reference page, declare the correct **`trigger` or `event` module** in the manifest, and match **scopes and impersonation** (`asApp` vs `asUser`) to how they must access data in the handler.

### Events overview

- [Events overview](https://developer.atlassian.com/platform/forge/events-reference/index.md)

### Atlassian app events

- [Atlassian app events](https://developer.atlassian.com/platform/forge/events-reference/product_events.md)
- [Bitbucket events](https://developer.atlassian.com/platform/forge/events-reference/bitbucket.md)
- [Compass events](https://developer.atlassian.com/platform/forge/events-reference/compass.md)
- [Confluence events](https://developer.atlassian.com/platform/forge/events-reference/confluence.md)
- [Jira events](https://developer.atlassian.com/platform/forge/events-reference/jira.md)
- [Jira Software events](https://developer.atlassian.com/platform/forge/events-reference/jira-software.md)
- [Expressions playground](https://developer.atlassian.com/platform/forge/events-reference/expressions-playground.md)

### App events (Preview)

- [App events (Preview)](https://developer.atlassian.com/platform/forge/events-reference/app-events.md)

### Life cycle events

- [Life cycle events](https://developer.atlassian.com/platform/forge/events-reference/life-cycle.md)

### Data security policy events

- [Data security policy events](https://developer.atlassian.com/platform/forge/events-reference/data-security-policy-events.md)

### Scheduled trigger events

- [Scheduled trigger events](https://developer.atlassian.com/platform/forge/events-reference/scheduled-trigger.md)

### Web trigger events

- [Web trigger events](https://developer.atlassian.com/platform/forge/events-reference/web-trigger.md)

## Function reference

This section documents **Forge functions**—server-side JavaScript that runs in Forge’s managed runtime. The hub page is the [Function reference](https://developer.atlassian.com/platform/forge/function-reference/index/). Functions are declared in the app manifest, wired to modules or triggers, and implement app logic, integrations, and background work without you hosting your own servers.

Forge runs your function code in a constrained environment (scopes, quotas, and runtime APIs apply). Use the pages under this navigation area for handlers, context, invocation limits, and product-specific behavior.

**Invocation types (overview):**

- **Resolver** — Backend functions invoked **from the UI** (UI Kit or Custom UI) to fetch data, perform actions, or bridge the frontend to privileged operations. Resolvers are typically defined with `@forge/resolver` and connected to a UI module via manifest configuration.
- **Web trigger** — An **HTTP endpoint** exposed by your app that invokes a function when called with the correct URL and authentication. Used for inbound integrations, webhooks from external systems, or programmatic triggers from outside the Atlassian UI.
- **Async events (product / lifecycle events)** — Functions run in response to **asynchronous events** from Atlassian products or the platform (for example, issue updated, page published, or other supported event types). These are usually configured with Forge **triggers** and event payloads documented per product.
- **Scheduled triggers** — Functions run on a **schedule** (cron-like) defined in the manifest. Use for periodic jobs such as sync, cleanup, or reporting, subject to platform scheduling and limits.
- **Realtime events** — Functions invoked in response to **realtime** / live update flows where the platform pushes activity to your app (preview or product-specific; check current docs for availability and payload shape). Treat as event-driven like async events, but oriented to low-latency or streaming-style scenarios where documented.

When helping readers, map their use case to the right invocation type: UI-driven work often starts with **resolvers**; external HTTP callers with **web triggers**; reactions to product activity with **async events**; time-based work with **scheduled triggers**; and realtime flows only where the docs say they are supported.

### Functions overview

- [Functions overview](https://developer.atlassian.com/platform/forge/function-reference/index.md)

### Arguments

- [Arguments](https://developer.atlassian.com/platform/forge/function-reference/arguments.md)

### Runtimes

- [Runtimes](https://developer.atlassian.com/platform/forge/runtime-reference/index.md)
- [Node.js](https://developer.atlassian.com/platform/forge/function-reference/nodejs-runtime.md)
- [Legacy runtime (deprecated)](https://developer.atlassian.com/platform/forge/runtime-reference/legacy-runtime-reference.md)

### Forge resolver

- [Forge resolver](https://developer.atlassian.com/platform/forge/runtime-reference/forge-resolver.md)

### Scheduled triggers

- [Scheduled triggers](https://developer.atlassian.com/platform/forge/function-reference/scheduled-trigger.md)

### Web triggers

- [Web triggers](https://developer.atlassian.com/platform/forge/runtime-reference/web-trigger.md)
- [Function reference](https://developer.atlassian.com/platform/forge/runtime-reference/web-trigger.md)
- [API reference](https://developer.atlassian.com/platform/forge/runtime-reference/web-trigger-api.md)

### Async events

- [Async events](https://developer.atlassian.com/platform/forge/runtime-reference/async-events-api.md)
- [Basic usage](https://developer.atlassian.com/platform/forge/runtime-reference/async-events-api.md)
- [Error handling](https://developer.atlassian.com/platform/forge/runtime-reference/async-events-api-error-handling.md)
- [Upgrade to @forge/events major version 2](https://developer.atlassian.com/platform/forge/runtime-reference/async-events-api-version-2-upgrade.md)

### Realtime events (Preview)

- [Realtime events (Preview)](https://developer.atlassian.com/platform/forge/runtime-reference/realtime-events-api.md)

### Dynamic Modules (EAP)

- [Dynamic Modules (EAP)](https://developer.atlassian.com/platform/forge/apis-reference/dynamic-modules.md)
- [API reference](https://developer.atlassian.com/platform/forge/apis-reference/dynamic-modules-api.md)

### Customer-managed egress and remotes (EAP)

- [Customer-managed egress and remotes (EAP)](https://developer.atlassian.com/platform/forge/customer-managed-egress-and-remotes.md)
- [API reference](https://developer.atlassian.com/platform/forge/apis-reference/customer-managed-egress-and-remotes-api.md)

### License API

- [License API](https://developer.atlassian.com/platform/forge/apis-reference/license-api.md)
- [API reference](https://developer.atlassian.com/platform/forge/apis-reference/license-api.md)

### Atlassian app REST APIs

- [Atlassian app REST APIs](https://developer.atlassian.com/platform/forge/apis-reference/product-rest-api-reference.md)
- [Bitbucket API requests](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestbitbucket.md)
- [Confluence API requests](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestconfluence.md)
- [Jira API requests](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestjira.md)
- [GraphQL API requests](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestgraph.md)

### Fetch APIs

- [Fetch APIs](https://developer.atlassian.com/platform/forge/runtime-reference/fetch-api.md)
- [Basic fetch client](https://developer.atlassian.com/platform/forge/runtime-reference/fetch-api.basic.md)
- [External authentication](https://developer.atlassian.com/platform/forge/runtime-reference/external-fetch-api.md)

### Invoke Remote API

- [Invoke Remote API](https://developer.atlassian.com/platform/forge/runtime-reference/invoke-remote-api.md)

### App context API

- [App context API](https://developer.atlassian.com/platform/forge/runtime-reference/app-context-api.md)

### Privacy API

- [Privacy API](https://developer.atlassian.com/platform/forge/runtime-reference/privacy-api.md)

### Authorize API

- [Authorize API](https://developer.atlassian.com/platform/forge/runtime-reference/authorize-api.md)

### i18n API

- [i18n API](https://developer.atlassian.com/platform/forge/runtime-reference/i18n.md)

### LLMs API

- [LLMs API](https://developer.atlassian.com/platform/forge/runtime-reference/forge-llms-api.md)

## Storage reference

This section describes **Forge hosted storage**—durable, platform-managed persistence scoped per app installation (quotas and limits apply). The overview page is [Storage](https://developer.atlassian.com/platform/forge/storage-reference/). Use the pages linked from there and from this navigation area for APIs, migrations, and product-specific limits.

Forge offers **four** hosted storage capabilities. They differ mainly by **data model**, **query shape**, and **typical payload size**—not by “which is newest.” For **Key-value store** and **Custom Entity Store**, new apps should use the **`@forge/kvs`** package; the legacy `storage` module on `@forge/api` is still supported but does not receive new features—see migration docs when advising upgrades.

**How they differ:**

- **Key-value store** — Stores **key–value pairs**. Best when you need simple persistence: flags, small JSON blobs, configuration, or lookups by key without relational structure. This is the lightest model when a single key maps to a value and you do not need entity schemas or rich querying across records.

- **Custom Entity Store** — Stores **typed records** defined by **custom entities** (your app’s schema) and supports **querying** over that data (including more complex query patterns documented separately). Use this when you have many similar objects, need filters or structured access patterns, or outgrow ad hoc keys. Query APIs can be **eventually consistent**; check the current docs for semantics and limits.

- **Forge SQL** — Provisions a **dedicated SQL database per customer installation**. Use this when the data is **relational**: joins, transactions, and interrelated tables are first-class. Prefer this over forcing relational models into key-value or entity abstractions.

- **Object Store (EAP)** — For **large objects** (e.g. substantial binary or media-like payloads) that do not fit the key-value or entity value models comfortably. Treat availability and limits as **Early Access Program** until the docs say otherwise.

When recommending an option: start from the **shape of the data** (key/value vs entity + query vs relational vs large blobs), then confirm **scopes, quotas, and EAP status** in the official pages below this index.

### Storage overview

- [Storage overview](https://developer.atlassian.com/platform/forge/storage-reference/index.md)

### Key-Value Store

- [Key-Value Store](https://developer.atlassian.com/platform/forge/storage-reference/kvs.md)
- [Storing data](https://developer.atlassian.com/platform/forge/storage-reference/kvs-api.md)
- [Querying data](https://developer.atlassian.com/platform/forge/storage-reference/kvs-api-query.md)
- [Encrypting stored data](https://developer.atlassian.com/platform/forge/storage-reference/kvs-api-secret.md)
- [Running batch operations](https://developer.atlassian.com/platform/forge/storage-reference/kvs-batch.md)
- [Running transactions](https://developer.atlassian.com/platform/forge/storage-reference/kvs-transactions.md)
- [Error handling](https://developer.atlassian.com/platform/forge/storage-reference/kvs-errorhandling.md)

### Custom Entity Store

- [Custom Entity Store](https://developer.atlassian.com/platform/forge/storage-reference/entities.md)
- [Defining entities](https://developer.atlassian.com/platform/forge/storage-reference/entities-manifest.md)
- [Storing entities](https://developer.atlassian.com/platform/forge/storage-reference/entities-api.md)
- [Querying data](https://developer.atlassian.com/platform/forge/storage-reference/entities-api-query.md)
- [Querying data (legacy)](https://developer.atlassian.com/platform/forge/storage-reference/entities-api-query-legacy.md)
- [Running batch operations](https://developer.atlassian.com/platform/forge/storage-reference/entities-batch.md)
- [Running transactions](https://developer.atlassian.com/platform/forge/storage-reference/entities-transactions.md)
- [Error handling](https://developer.atlassian.com/platform/forge/storage-reference/entities-errorhandling.md)

### SQL

- [SQL](https://developer.atlassian.com/platform/forge/storage-reference/sql.md)
- [Tutorial](https://developer.atlassian.com/platform/forge/storage-reference/sql-tutorial.md)
- [Manage schemas](https://developer.atlassian.com/platform/forge/storage-reference/sql-api-schema.md)
- [Execute SQL operations](https://developer.atlassian.com/platform/forge/storage-reference/sql-api.md)
- [Error handling](https://developer.atlassian.com/platform/forge/storage-reference/sql-handling-errors.md)

### Object Store (EAP)

- [Object Store (EAP)](https://developer.atlassian.com/platform/forge/storage-reference/object-store.md)
- [Managing objects](https://developer.atlassian.com/platform/forge/storage-reference/object-store-api.md)

## REST API references

Forge publishes **two different REST documentation trees** under `/platform/forge/rest/`. They are **not** interchangeable “v1 vs v2” of the same API—**scope, caller, and hosting model differ.** Point readers to the correct tree or they will use the wrong integration pattern.

### [KVS / Custom Entity Store API (`/rest/v1/`)](https://developer.atlassian.com/platform/forge/rest/v1/)

This reference is centered on the **hosted storage REST API** for the **Key-Value Store** and **Custom Entity Store**: overview, quotas and limits, KVS operations, entity operations, transactions, and batching. Use it when the question is specifically **HTTP access to Forge KVS/CES** (payloads, endpoints, and limits for that surface).

### [Forge Containers REST API — intro (`/rest/v2/intro/`)](https://developer.atlassian.com/platform/forge/rest/v2/intro/#about)

This reference describes the broader **REST APIs that Forge Containers** can call **outbound** from a **containerised** service: Atlassian product APIs, Forge platform APIs, and other documented resources. Calls go through the **egress sidecar** (for example using `FORGE_EGRESS_PROXY_URL` as documented there). This area is tied to **Forge Containers** and, as documented on that page, is **EAP**—not for production unless and until the docs say otherwise.

**How to choose:** If the user is building **normal Forge functions** with `@forge/kvs` or runtime storage APIs, they usually follow the **Storage** / **runtime** docs—not necessarily these REST pages. If they are integrating **hosted storage via REST**, start with **`/rest/v1/`**. If they are in **Forge Containers** and need **outbound REST** to Forge or Atlassian services, start with **`/rest/v2/intro/`** and follow the egress and EAP guidance there.

- [APIs for Forge Containers](https://developer.atlassian.com/platform/forge/rest/v2/index.md)
- [KVS/Custom Entity Store API](https://developer.atlassian.com/platform/forge/rest/v1/index.md)

## Platform limits and usage

This area documents **Forge platform limits, usage, and (historically) quotas**. The canonical overview is [Platform quotas and limits](https://developer.atlassian.com/platform/forge/platform-quotas-and-limits/).

**Pricing and fairness:** Forge uses a **consumption-based** model with a **free usage allowance**; platform **limits** still apply so the platform stays reliable and fair. If an app **consistently exceeds** limits, Atlassian may contact you—you can also reach out if you need higher limits. Abusive or unstable usage may be **throttled or suspended** even when billing could apply.

**Quotas vs limits:** **Quotas** (hard caps introduced mainly for abuse prevention) have largely been **retired** in favor of consumption pricing; **platform limits** are the non‑negotiable constraints that **do not scale** with spend (invocation duration, payload sizes, counts of certain resources, and so on). Always read the **specific limit page** for the feature in question—do not assume a paid tier removes a documented platform cap.

**Beyond Forge docs:** Apps can still hit **Atlassian product rate limits** (for example Jira or Confluence REST)—those are **separate** from Forge platform limits.

**Operations:** Teams monitor and forecast usage via the **Developer Console** (usage and costs) and the **cost estimator** linked from the platform pricing docs.

When answering questions, **cite the relevant subsection** above instead of inventing numbers; limits change over time.

- [Overview](https://developer.atlassian.com/platform/forge/platform-quotas-and-limits.md)
- [Exceeding limits and suspended apps](https://developer.atlassian.com/platform/forge/exceeding-limits-and-suspended-apps.md)
- [Invocation limits](https://developer.atlassian.com/platform/forge/limits-invocation.md)
- [Resource limits](https://developer.atlassian.com/platform/forge/limits-resource.md)
- [KVS and Custom Entity Store limits](https://developer.atlassian.com/platform/forge/limits-kvs-ce.md)
- [Forge SQL limits](https://developer.atlassian.com/platform/forge/limits-sql.md)
- [Forge Object Store](https://developer.atlassian.com/platform/forge/limits-object-store.md)
- [Forge LLM limits](https://developer.atlassian.com/platform/forge/limits-llm.md)
- [Forge Containers REST API limits](https://developer.atlassian.com/platform/forge/limits-containers.md)
- [Web trigger limits](https://developer.atlassian.com/platform/forge/limits-web-trigger.md)
- [Async events limits](https://developer.atlassian.com/platform/forge/limits-async-events.md)
- [App and developer limits](https://developer.atlassian.com/platform/forge/limits-app-developer.md)
- [Scheduled trigger limits](https://developer.atlassian.com/platform/forge/limits-scheduled-trigger.md)

## CLI reference

This section documents the **Forge CLI**—the command-line tool used to **create, run, deploy, and operate** Forge apps from a developer machine or automation. The index is [Forge CLI](https://developer.atlassian.com/platform/forge/cli-reference/).

**Basics (from the overview):**

- **Install** globally with npm: `npm i -g @forge/cli@latest`
- **Authenticate**: `forge login`
- **Environment setup** for day-to-day development is covered in the [getting started](https://developer.atlassian.com/platform/forge/getting-started/#before-you-begin) flow—point readers there before deep CLI flags.

**Upgrades:** To move to a new CLI version, **fully remove** the global package and **reinstall** (for example `npm uninstall -g @forge/cli` then `npm i -g @forge/cli@latest`), as described on the CLI overview page.

**Version support:** Each CLI release is only supported for a **limited window** (see the Forge **deprecation policy** for CLI version support). Prefer advising **current `@forge/cli@latest`** so users get fixes, compatible APIs, and supported behavior.

**How to use this reference:** Pages under this navigation item document **individual commands** (arguments, options, and typical workflows such as deploy, tunnel, logs, variables, licensing, and containers-related commands where applicable). When helping someone, name the **exact `forge` subcommand** they need and send them to the matching reference page rather than guessing flags—behavior and defaults change between versions.

### CLI

- [CLI](https://developer.atlassian.com/platform/forge/cli-reference/index.md)

### assistant

- [assistant](https://developer.atlassian.com/platform/forge/cli-reference/assistant.md)
- [off](https://developer.atlassian.com/platform/forge/cli-reference/assistant-off.md)
- [on](https://developer.atlassian.com/platform/forge/cli-reference/assistant-on.md)

### autocomplete

- [autocomplete](https://developer.atlassian.com/platform/forge/cli-reference/autocomplete.md)

### build

- [build](https://developer.atlassian.com/platform/forge/cli-reference/build.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/build-list.md)

### create

- [create](https://developer.atlassian.com/platform/forge/cli-reference/create.md)

### custom-scopes

- [custom-scopes](https://developer.atlassian.com/platform/forge/cli-reference/custom-scopes.md)
- [create](https://developer.atlassian.com/platform/forge/cli-reference/custom-scopes-create.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/custom-scopes-list.md)

### deploy

- [deploy](https://developer.atlassian.com/platform/forge/cli-reference/deploy.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/deploy-list.md)

### developer-spaces

- [developer-spaces](https://developer.atlassian.com/platform/forge/cli-reference/developer-spaces.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/developer-spaces-list.md)

### eligibility

- [eligibility](https://developer.atlassian.com/platform/forge/cli-reference/eligibility.md)

### environments

- [environments](https://developer.atlassian.com/platform/forge/cli-reference/environments.md)
- [create](https://developer.atlassian.com/platform/forge/cli-reference/environments-create.md)
- [delete](https://developer.atlassian.com/platform/forge/cli-reference/environments-delete.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/environments-list.md)

### feedback

- [feedback](https://developer.atlassian.com/platform/forge/cli-reference/feedback.md)

### install

- [install](https://developer.atlassian.com/platform/forge/cli-reference/install.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/install-list.md)

### lint

- [lint](https://developer.atlassian.com/platform/forge/cli-reference/lint.md)

### login

- [login](https://developer.atlassian.com/platform/forge/cli-reference/login.md)

### logout

- [logout](https://developer.atlassian.com/platform/forge/cli-reference/logout.md)

### logs

- [logs](https://developer.atlassian.com/platform/forge/cli-reference/logs.md)

### providers

- [providers](https://developer.atlassian.com/platform/forge/cli-reference/providers.md)
- [configure](https://developer.atlassian.com/platform/forge/cli-reference/providers-configure.md)

### register

- [register](https://developer.atlassian.com/platform/forge/cli-reference/register.md)

### settings

- [settings](https://developer.atlassian.com/platform/forge/cli-reference/settings.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/settings-list.md)
- [set](https://developer.atlassian.com/platform/forge/cli-reference/settings-set.md)

### storage

- [storage](https://developer.atlassian.com/platform/forge/cli-reference/storage.md)
- [entities](https://developer.atlassian.com/platform/forge/cli-reference/storage-entities.md)

### tunnel

- [tunnel](https://developer.atlassian.com/platform/forge/cli-reference/tunnel.md)

### uninstall

- [uninstall](https://developer.atlassian.com/platform/forge/cli-reference/uninstall.md)

### variables

- [variables](https://developer.atlassian.com/platform/forge/cli-reference/variables.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/variables-list.md)
- [set](https://developer.atlassian.com/platform/forge/cli-reference/variables-set.md)
- [unset](https://developer.atlassian.com/platform/forge/cli-reference/variables-unset.md)

### version

- [version](https://developer.atlassian.com/platform/forge/cli-reference/version.md)
- [bulk-upgrade](https://developer.atlassian.com/platform/forge/cli-reference/version-bulk-upgrade.md)
- [compare](https://developer.atlassian.com/platform/forge/cli-reference/version-compare.md)
- [details](https://developer.atlassian.com/platform/forge/cli-reference/version-details.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/version-list.md)

### webtrigger

- [webtrigger](https://developer.atlassian.com/platform/forge/cli-reference/webtrigger.md)
- [create](https://developer.atlassian.com/platform/forge/cli-reference/webtrigger-create.md)
- [delete](https://developer.atlassian.com/platform/forge/cli-reference/webtrigger-delete.md)
- [list](https://developer.atlassian.com/platform/forge/cli-reference/webtrigger-list.md)

### whoami

- [whoami](https://developer.atlassian.com/platform/forge/cli-reference/whoami.md)

## Example apps

This section contains curated references that show how real Forge apps are structured and how they use Atlassian product APIs, UI patterns, and platform features. Use them when someone wants **working patterns** or **comparison to Atlassian’s own app code**, not only prose documentation.

- [Bitbucket](https://developer.atlassian.com/platform/forge/example-apps-bitbucket.md)
- [Compass](https://developer.atlassian.com/platform/forge/example-apps-compass.md)
- [Confluence](https://developer.atlassian.com/platform/forge/example-apps-confluence.md)
- [Jira](https://developer.atlassian.com/platform/forge/example-apps-jira.md)
- [Jira Service Management](https://developer.atlassian.com/platform/forge/example-apps-jsm.md)
- [Rovo](https://developer.atlassian.com/platform/forge/example-apps-rovo.md)

## Guides

- [Guides](https://developer.atlassian.com/platform/forge/index.md)

### Get started

#### Getting started

- [Getting started](https://developer.atlassian.com/platform/forge/getting-started.md)

#### Introduction to Forge

- [The Forge platform](https://developer.atlassian.com/platform/forge/introduction/the-forge-platform.md)
- [Why build with Forge](https://developer.atlassian.com/platform/forge/introduction/why-build-with-forge.md)
- [Forge platform pricing](https://developer.atlassian.com/platform/forge/forge-platform-pricing.md)

#### AI development toolkit

- [Overview](https://developer.atlassian.com/platform/forge/ai-development-toolkit/index.md)
- [Forge AI Plugin](https://developer.atlassian.com/platform/forge/ai-development-toolkit/forge-ai-plugin.md)
- [Forge MCP Server](https://developer.atlassian.com/platform/forge/ai-development-toolkit/forge-mcp.md)
- [Forge skills](https://developer.atlassian.com/platform/forge/ai-development-toolkit/forge-developer-skills.md)

#### Migration guides

- [Migrating your Connect app](https://developer.atlassian.com/platform/forge/adopting-forge-from-connect.md)
- [Migrating a Connect macro to Forge](https://developer.atlassian.com/platform/forge/adopting-forge-from-connect-migrate-macro.md)
- [Upgrading to latest UI Kit version](https://developer.atlassian.com/platform/forge/ui-kit/upgrade-to-ui-kit-latest.md)
- [Migrating to Forge SQL](https://developer.atlassian.com/platform/forge/storage-reference/sql-migration-guide.md)
- [Migrating from legacy KVS module](https://developer.atlassian.com/platform/forge/storage-reference/kvs-migration-from-legacy.md)
- [Upgrading from legacy runtime](https://developer.atlassian.com/platform/forge/runtime-reference/legacy-runtime-migrating.md)
- [Migrating a Forge app to support multiple Atlassian apps](https://developer.atlassian.com/platform/forge/migrating-a-forge-app-to-support-multiple-atlassian-apps.md)

#### Learn

##### Building automations

- [Building automations](https://developer.atlassian.com/platform/forge/building-automations.md)

##### Building integrations

- [Building integrations](https://developer.atlassian.com/platform/forge/building-integrations.md)

##### Tutorials

###### Overview

- [Overview](https://developer.atlassian.com/platform/forge/tutorials-and-guides.md)

###### Build an app compatible with Confluence and Jira

- [Build an app compatible with Confluence and Jira](https://developer.atlassian.com/platform/forge/build-an-app-compatible-with-confluence-and-jira.md)

###### Forge, Compass, and AWS CloudWatch

- [Forge, Compass, and AWS CloudWatch](https://developer.atlassian.com/platform/forge/forge-compass-cloudwatch.md)

###### Build a Jira automation action

- [Build a Jira automation action](https://developer.atlassian.com/platform/forge/build-a-jira-automation-action.md)

###### Schedule web triggers

- [Schedule web triggers](https://developer.atlassian.com/platform/forge/add-scheduled-trigger.md)

###### Debug functions using IntelliJ

- [Debug functions using IntelliJ](https://developer.atlassian.com/platform/forge/debug-functions-using-intellij.md)

###### Debug functions using VS Code

- [Debug functions using VS Code](https://developer.atlassian.com/platform/forge/debug-functions-using-vscode.md)

###### Profile app performance with tunnel debugger

- [Profile app performance with tunnel debugger](https://developer.atlassian.com/platform/forge/profiling-node-js-app-code-tunnel.md)

###### Implement a dynamic profile retriever

- [Implement a dynamic profile retriever](https://developer.atlassian.com/platform/forge/implement-a-dynamic-profile-retriever-with-external-authentication.md)

###### Set up continuous delivery

- [Set up continuous delivery](https://developer.atlassian.com/platform/forge/set-up-cicd.md)

###### Queue app interactions with Storage API

- [Queue app interactions with Storage API](https://developer.atlassian.com/platform/forge/storage-api-limit-handling.md)

###### Use a long-running function

- [Use a long-running function](https://developer.atlassian.com/platform/forge/use-a-long-running-function.md)

###### Use custom entities to store structured data

- [Use custom entities to store structured data](https://developer.atlassian.com/platform/forge/custom-entities-store-structured-data.md)

###### Use an external OAuth 2.0 API with fetch

- [Use an external OAuth 2.0 API with fetch](https://developer.atlassian.com/platform/forge/use-an-external-oauth-2.0-api-with-fetch.md)

###### Add routing to a full-page app in Jira

- [Add routing to a full-page app in Jira](https://developer.atlassian.com/platform/forge/add-routing-to-a-full-page-app.md)

###### Use the storage API in Confluence

- [Use the storage API in Confluence](https://developer.atlassian.com/platform/forge/create-confluence-macro-with-storage-api.md)

###### Add custom configuration to a macro

- [Add custom configuration to a macro](https://developer.atlassian.com/platform/forge/add-custom-configuration-to-a-macro.md)

###### Using rich body macros

- [Using rich body macros](https://developer.atlassian.com/platform/forge/using-rich-text-bodied-macros.md)

###### Create an LLM Web trigger application

- [Create an LLM Web trigger application](https://developer.atlassian.com/platform/forge/create-an-llm-webtrigger-app.md)

###### Create an Agentic LLM Web trigger application

- [Create an Agentic LLM Web trigger application](https://developer.atlassian.com/platform/forge/create-an-agentic-llm-webtrigger-app.md)

###### Handling long-running LLM processes with Forge Realtime

- [Handling long-running LLM processes with Forge Realtime](https://developer.atlassian.com/platform/forge/llm-long-running-process-with-forge-realtime.md)

###### Bitbucket

- [Extend Bitbucket Cloud](https://developer.atlassian.com/platform/forge/extend-bitbucket-cloud.md)
- [Build a hello world app in Bitbucket](https://developer.atlassian.com/platform/forge/build-a-hello-world-app-in-bitbucket.md)
- [Automate Bitbucket with triggers](https://developer.atlassian.com/platform/forge/automate-bitbucket-using-triggers.md)
- [Build a pull request title validator with custom merge checks](https://developer.atlassian.com/platform/forge/build-a-pull-request-title-validator-with-custom-merge-checks.md)
- [Orchestrate your builds using Dynamic Pipelines](https://developer.atlassian.com/platform/forge/orchestrate-your-builds-using-dynamic-pipelines.md)

###### Confluence

- [Build a hello world app in Confluence](https://developer.atlassian.com/platform/forge/build-a-hello-world-app-in-confluence.md)
- [Create a question generator app in multiple languages using i18n](https://developer.atlassian.com/platform/forge/create-a-question-generator-app-in-multiple-languages-using-i18n.md)
- [Create a quiz app using UI Kit](https://developer.atlassian.com/platform/forge/create-a-quiz-app-using-ui-kit.md)
- [Add configuration to a macro with UI Kit](https://developer.atlassian.com/platform/forge/add-configuration-to-a-macro-with-ui-kit.md)
- [Create a logo designer app using the Frame component](https://developer.atlassian.com/platform/forge/ui-kit/components/frame-tutorial.md)
- [Use space settings and content byline to implement space news](https://developer.atlassian.com/platform/forge/space-news.md)
- [Use content actions to count page macros](https://developer.atlassian.com/platform/forge/macros-in-the-page.md)
- [Build a Custom UI app](https://developer.atlassian.com/platform/forge/build-a-custom-ui-app-in-confluence.md)
- [Build a dashboard app with the Confluence full page module](https://developer.atlassian.com/platform/forge/build-a-dashboard-app-with-the-confluence-full-page-module.md)
- [Build a Confluence keyword extractor with OpenAI](https://developer.atlassian.com/platform/forge/build-confluence-keyword-extractor-with-openai.md)
- [Use highlighted text in a Confluence app](https://developer.atlassian.com/platform/forge/create-confluence-contextmenu-module.md)
- [Create a GIPHY app using UI kit on Confluence](https://developer.atlassian.com/platform/forge/create-a-giphy-app-using-the-ui-kit.md)

###### External integrations

- [Build a feedback app with integrations](https://developer.atlassian.com/platform/forge/build-a-feedback-integration-app.md)

###### Jira

- [Build a hello world app in Jira](https://developer.atlassian.com/platform/forge/build-a-hello-world-app-in-jira.md)
- [Automate Jira with triggers](https://developer.atlassian.com/platform/forge/automate-jira-using-triggers.md)
- [Build a Jira comments summarizer app with OpenAI](https://developer.atlassian.com/platform/forge/build-jira-comments-summarizer-with-openai.md)
- [Use a workflow validator to check issue assignments](https://developer.atlassian.com/platform/forge/check-jira-issues-assigned-using-workflow-validator.md)
- [Build a Custom UI app](https://developer.atlassian.com/platform/forge/build-a-custom-ui-app-in-jira.md)
- [Build a dashboard app with the Jira full page module](https://developer.atlassian.com/platform/forge/build-a-dashboard-app-with-the-jira-full-page-module.md)
- [Build a Jira UI modifications app](https://developer.atlassian.com/platform/forge/build-a-jira-uim-app.md)

###### Jira Service Management

- [Build a hello world app in Jira Service Management](https://developer.atlassian.com/platform/forge/build-a-hello-world-app-in-jira-service-management.md)
- [Import third party data into Assets](https://developer.atlassian.com/platform/forge/assets-import-app.md)
- [Use Async Events API to queue jobs to import objects into Assets](https://developer.atlassian.com/platform/forge/queue-events-with-async-events-api-to-import-assets.md)
- [Build a Custom UI app](https://developer.atlassian.com/platform/forge/build-a-custom-ui-app-in-jira-service-management.md)

###### Rovo

- [Extend Atlassian apps with a Forge Rovo agent](https://developer.atlassian.com/platform/forge/extend-atlassian-products-with-a-forge-rovo-agent.md)
- [Build a Rovo Agent app](https://developer.atlassian.com/platform/forge/build-a-hello-world-rovo-agent.md)
- [Build a Q&A Rovo Agent for Confluence](https://developer.atlassian.com/platform/forge/build-a-q-and-a-rovo-agent-for-confluence.md)
- [Build a Jira issue analyst Rovo Agent](https://developer.atlassian.com/platform/forge/build-a-jira-issue-analyst-rovo-agent.md)
- [Integrate remote agents with Jira](https://developer.atlassian.com/platform/forge/remote-agents-in-jira.md)

###### Teamwork Graph

- [Call the Teamwork Graph API](https://developer.atlassian.com/platform/forge/call-the-teamwork-graph-api.md)
- [Build a Teamwork Graph connector](https://developer.atlassian.com/platform/forge/build-a-teamwork-graph-connector.md)
- [Build an app with Teamwork Graph Smart Links](https://developer.atlassian.com/platform/forge/build-a-smart-link-app.md)

##### Atlassian developer glossary

- [Atlassian developer glossary](https://developer.atlassian.com/platform/forge/glossary.md)

### Plan & design

#### App architecture

- [Events and triggers](https://developer.atlassian.com/platform/forge/events.md)
- [Storage](https://developer.atlassian.com/platform/forge/storage.md)
- [Hosted storage data lifecycle](https://developer.atlassian.com/platform/forge/storage-reference/hosted-storage-data-lifecycle.md)
- [Manifest](https://developer.atlassian.com/platform/forge/manifest.md)
- [App compatibility](https://developer.atlassian.com/platform/forge/app-compatibility.md)
- [Modules](https://developer.atlassian.com/platform/forge/modules.md)
- [App security](https://developer.atlassian.com/platform/forge/security.md)
- [Optimise Forge platform costs](https://developer.atlassian.com/platform/forge/optimise-forge-costs.md)

#### User interface

- [Overview](https://developer.atlassian.com/platform/forge/user-interface.md)
- [Build with UI Kit](https://developer.atlassian.com/platform/forge/ui-kit.md)
- [Extend UI with custom options](https://developer.atlassian.com/platform/forge/extend-ui-with-custom-options.md)
- [Design tokens and theming](https://developer.atlassian.com/platform/forge/design-tokens-and-theming.md)
- [Guidelines for action components](https://developer.atlassian.com/platform/forge/action-components-guidelines.md)
- [Jira full-page modules](https://developer.atlassian.com/platform/forge/jira-full-page-modules.md)
- [Internationalization](https://developer.atlassian.com/platform/forge/internationalization.md)
- [Understanding the UI modifications module](https://developer.atlassian.com/platform/forge/understanding-ui-modifications.md)

#### Legal & privacy

- [Forge terms of use](https://developer.atlassian.com/platform/forge/developer-terms.md)
- [Forge service level agreement](https://developer.atlassian.com/platform/forge/forge-service-level-agreement.md)
- [Shared responsibility model](https://developer.atlassian.com/platform/forge/shared-responsibility-model.md)
- [Analytics tool policy for Forge apps](https://developer.atlassian.com/platform/forge/analytics-tool-policy.md)
- [Forge privacy and security FAQ](https://developer.atlassian.com/platform/forge/faq-privacy-security.md)
- [User privacy guide](https://developer.atlassian.com/platform/forge/user-privacy-guidelines.md)
- [Forge Data Processing Addendum](https://developer.atlassian.com/platform/forge/about-the-forge-data-processing-addendum.md)
- [Logging data](https://developer.atlassian.com/platform/forge/logging-guidelines.md)

#### App distribution

##### Promote an app from staging to production

- [Promote an app from staging to production](https://developer.atlassian.com/platform/forge/staging-and-production-apps.md)

##### Distribute via console

- [Distribute via console](https://developer.atlassian.com/platform/forge/distribute-your-apps.md)

##### Licensing

- [Overview](https://developer.atlassian.com/platform/forge/licensing-overview.md)
- [Adopt user-based billing](https://developer.atlassian.com/platform/forge/adopt-user-based-billing.md)

#### Programs

- [Overview](https://developer.atlassian.com/platform/forge/overview-programs.md)
- [Runs on Atlassian](https://developer.atlassian.com/platform/forge/runs-on-atlassian.md)

#### Reference architecture

- [Work item picker custom field in Jira](https://developer.atlassian.com/platform/forge/work-item-picker-custom-field-in-jira.md)
- [In-app notifications from events](https://developer.atlassian.com/platform/forge/in-app-notifications-from-events.md)
- [Manage the 1,000 value limit in custom JQL functions](https://developer.atlassian.com/platform/forge/working-around-jql-1000-limit.md)

### Build

#### Development life cycle

##### Environment configuration

- [Environment configuration](https://developer.atlassian.com/platform/forge/environments-and-versions.md)

##### Forge MCP Server

- [Forge MCP Server](https://developer.atlassian.com/platform/forge/ai-development-toolkit/forge-mcp.md)

##### Contributors

- [Overview](https://developer.atlassian.com/platform/forge/contributors.md)
- [Managing contributors](https://developer.atlassian.com/platform/forge/manage-app-contributors.md)

##### App versions

- [App versions](https://developer.atlassian.com/platform/forge/versions.md)

##### Testing and debugging

- [Overview](https://developer.atlassian.com/platform/forge/debugging.md)
- [Debug using IntelliJ](https://developer.atlassian.com/platform/forge/debug-functions-using-intellij.md)
- [Debug using VS Code](https://developer.atlassian.com/platform/forge/debug-functions-using-vscode.md)
- [Tunneling](https://developer.atlassian.com/platform/forge/tunneling.md)

#### App capabilities

##### Containerized services (EAP)

- [Containerized services (EAP)](https://developer.atlassian.com/platform/forge/containers-reference/index-TOC.md)

##### Compute

###### Functions

- [Invoke functions](https://developer.atlassian.com/platform/forge/function-reference/index.md)
- [Call an Atlassian app REST API](https://developer.atlassian.com/platform/forge/apis-reference/product-rest-api-reference.md)
- [Call an Atlassian app GraphQL API](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestgraph.md)
- [Verify user permissions for Atlassian app APIs](https://developer.atlassian.com/platform/forge/runtime-reference/authorize-api.md)
- [Call an external REST API](https://developer.atlassian.com/platform/forge/runtime-reference/external-fetch-api.md)
- [Check user account status](https://developer.atlassian.com/platform/forge/runtime-reference/authorize-api.md)

###### Web triggers

- [Work with web triggers](https://developer.atlassian.com/platform/forge/runtime-reference/web-trigger.md)

###### Queues

- [Use async app event queues](https://developer.atlassian.com/platform/forge/runtime-reference/async-events-api.md)

###### Events

- [Platform and Atlassian app events](https://developer.atlassian.com/platform/forge/events.md)

###### App REST APIs

- [Overview](https://developer.atlassian.com/platform/forge/app-rest-apis.md)
- [Expose Forge app REST APIs](https://developer.atlassian.com/platform/forge/expose-forge-app-rest-apis.md)
- [Access REST APIs exposed by a Forge app](https://developer.atlassian.com/platform/forge/access-rest-apis-exposed-by-a-forge-app.md)

###### Reference

- [Reference](https://developer.atlassian.com/platform/forge/function-reference/index.md)

##### Storage

- [Key value store](https://developer.atlassian.com/platform/forge/storage-reference/kvs.md)
- [Entity store](https://developer.atlassian.com/platform/forge/storage-reference/entities.md)
- [SQL](https://developer.atlassian.com/platform/forge/storage-reference/sql.md)
- [Reference](https://developer.atlassian.com/platform/forge/storage-reference/index.md)
- [Hosted storage data lifecycle](https://developer.atlassian.com/platform/forge/storage-reference/hosted-storage-data-lifecycle.md)

##### Realtime (Preview)

- [Overview](https://developer.atlassian.com/platform/forge/realtime/index.md)
- [Authorizing realtime channels](https://developer.atlassian.com/platform/forge/realtime/authorizing-realtime-channels.md)

##### Remotes

###### Overview

- [Overview](https://developer.atlassian.com/platform/forge/remote/index.md)

###### Forge Remote essentials

- [Forge Remote essentials](https://developer.atlassian.com/platform/forge/remote/essentials.md)

###### Send events to a remote

- [Send events to a remote](https://developer.atlassian.com/platform/forge/remote/sending-product-events.md)

###### Schedule triggers to invoke a remote

- [Schedule triggers to invoke a remote](https://developer.atlassian.com/platform/forge/remote/scheduled-triggers.md)

###### Call Forge storage from a remote

- [Using REST API (recommended)](https://developer.atlassian.com/platform/forge/remote/accessing-storage.md)
- [Using GraphQL](https://developer.atlassian.com/platform/forge/remote/accessing-storage-graphql.md)

###### Call Atlassian app APIs from a remote

- [Call Atlassian app APIs from a remote](https://developer.atlassian.com/platform/forge/remote/calling-product-apis.md)

###### Call from a Forge frontend

- [Call from a Forge frontend](https://developer.atlassian.com/platform/forge/remote/calling-from-frontend.md)

###### Call from a Forge function

- [Call from a Forge function](https://developer.atlassian.com/platform/forge/remote/calling-from-function.md)

###### Bitbucket git operations from a remote

- [Bitbucket git operations from a remote](https://developer.atlassian.com/platform/forge/remote/bitbucket-git-operations.md)

###### Remote observability

- [Remote observability](https://developer.atlassian.com/platform/forge/remote/observability.md)

###### Set up remotes for data residency realm pinning

- [Set up remotes for data residency realm pinning](https://developer.atlassian.com/platform/forge/remote/remote-realm-pinning.md)

###### Support data residency realm migrations for Forge Remotes

- [Support data residency realm migrations for Forge Remotes](https://developer.atlassian.com/platform/forge/remote/remote-realm-migration.md)

##### User interface

- [UI Kit](https://developer.atlassian.com/platform/forge/ui-kit.md)
- [Frontend bridge](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/bridge.md)
- [Display conditions](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/index.md)
- [Reference](https://developer.atlassian.com/platform/forge/ui-kit/overview.md)

##### Observability

- [Overview](https://developer.atlassian.com/platform/forge/remote/observability.md)
- [App observability in third-party tools](https://developer.atlassian.com/platform/forge/app-observability-in-third-party-tools.md)

#### Trust and security

##### Data residency

- [Data residency](https://developer.atlassian.com/platform/forge/data-residency.md)

##### Tenant data isolation

- [Tenant data isolation](https://developer.atlassian.com/platform/forge/tenant-data-isolation.md)

##### Configuring app security

###### Unlicensed user app access

- [Unlicensed user app access](https://developer.atlassian.com/platform/forge/access-to-forge-apps-for-unlicensed-users.md)

###### Scopes to call an Atlassian REST API

- [Scopes to call an Atlassian REST API](https://developer.atlassian.com/platform/forge/add-scopes-to-call-an-atlassian-rest-api.md)

###### Runtime egress permissions

- [Runtime egress permissions](https://developer.atlassian.com/platform/forge/runtime-egress-permissions.md)

###### Content security and egress controls

- [Content security and egress controls](https://developer.atlassian.com/platform/forge/add-content-security-and-egress-controls.md)

###### App context security

- [App context security](https://developer.atlassian.com/platform/forge/app-context-security.md)

###### External authentication overview

- [Configuring OAuth 2.0 providers](https://developer.atlassian.com/platform/forge/use-an-external-oauth-2.0-api-with-fetch.md)
- [Rotating an OAuth 2.0 client ID and secret](https://developer.atlassian.com/platform/forge/rotating-an-oauth-2.0-client-id-and-secret.md)
- [Common issues with external authentication](https://developer.atlassian.com/platform/forge/common-issues-with-external-authentication.md)

##### Runs on Atlassian apps

- [Runs on Atlassian apps](https://developer.atlassian.com/platform/forge/runs-on-atlassian-apps.md)

##### Forge compliance

- [Compliance with SOC 2 and ISO 27001](https://developer.atlassian.com/platform/forge/forge-soc2-iso27001.md)
- [ISO 27001 responsibilities for Forge Marketplace Partners](https://developer.atlassian.com/platform/forge/iso-27001-responsibilities.md)

#### Enterprise development

- [Using Forge CLI on a corporate network](https://developer.atlassian.com/platform/forge/enterprise/use-forge-cli-on-corporate-network.md)
- [Use Forge CLI via a development container](https://developer.atlassian.com/platform/forge/enterprise/use-forge-cli-via-a-development-container.md)

#### Forge releases and deprecation policy

- [Forge releases (includes enrolling in EAP)](https://developer.atlassian.com/platform/forge/whats-coming.md)
- [Forge deprecation policy](https://developer.atlassian.com/platform/forge/deprecation-policy.md)

### Manage

#### Overview

- [Overview](https://developer.atlassian.com/platform/forge/manage-your-apps.md)

#### Developer spaces

- [Overview of Developer Spaces](https://developer.atlassian.com/platform/forge/developer-space/developer-spaces-introduction.md)
- [Create a Developer Space](https://developer.atlassian.com/platform/forge/developer-space/create-developer-space.md)
- [Work with apps in a Developer Spaces](https://developer.atlassian.com/platform/forge/developer-space/developer-space-apps.md)
- [Manage roles in Developer Spaces](https://developer.atlassian.com/platform/forge/developer-space/developer-space-roles.md)
- [Manage Developer Space settings](https://developer.atlassian.com/platform/forge/developer-space/manage-developer-space.md)
- [Billing and payments in Developer Spaces](https://developer.atlassian.com/platform/forge/developer-space/billing-for-developer-spaces.md)
- [Publish a Developer Space to the Atlassian Marketplace](https://developer.atlassian.com/platform/forge/developer-space/publish-developer-space.md)

#### Observability

##### Manage app alerts

- [Overview](https://developer.atlassian.com/platform/forge/alerts.md)
- [Create alert rules](https://developer.atlassian.com/platform/forge/create-alert-rules.md)
- [Manage alert rules](https://developer.atlassian.com/platform/forge/manage-alert-rules.md)
- [View open and closed alerts](https://developer.atlassian.com/platform/forge/view-open-and-closed-alerts.md)
- [Usage alerts](https://developer.atlassian.com/platform/forge/usage-alerts.md)

##### Monitor app metrics

- [Overview](https://developer.atlassian.com/platform/forge/monitor-app-metrics.md)
- [Monitor invocation metrics](https://developer.atlassian.com/platform/forge/monitor-invocation-metrics.md)
- [Monitor API metrics](https://developer.atlassian.com/platform/forge/monitor-api-metrics.md)
- [Monitor custom metrics](https://developer.atlassian.com/platform/forge/monitor-custom-metrics.md)
- [Monitor SQL](https://developer.atlassian.com/platform/forge/monitor-sql-metrics.md)
- [Monitor usage metrics and costs](https://developer.atlassian.com/platform/forge/monitor-usage-metrics.md)
- [Export app metrics](https://developer.atlassian.com/platform/forge/export-app-metrics.md)
- [Export app resource usage](https://developer.atlassian.com/platform/forge/developer-space/export-app-resource-usage.md)

##### Monitor app logs

- [Overview](https://developer.atlassian.com/platform/forge/monitor-app-logs.md)
- [View app logs](https://developer.atlassian.com/platform/forge/view-app-logs.md)
- [Export app logs](https://developer.atlassian.com/platform/forge/export-app-logs.md)
- [Access app logs](https://developer.atlassian.com/platform/forge/access-app-logs.md)

##### View app installations

- [View app installations](https://developer.atlassian.com/platform/forge/view-app-installations.md)

##### View app storage

- [View app storage](https://developer.atlassian.com/platform/forge/view-app-storage.md)

#### Access

##### Manage app contributors

- [Manage app contributors](https://developer.atlassian.com/platform/forge/manage-app-contributors.md)

##### Manage environments

###### Forge environments

- [Forge environments](https://developer.atlassian.com/platform/forge/environments-and-versions.md)

###### Configuring the manifest

- [Configuring the manifest](https://developer.atlassian.com/platform/forge/manifest-reference/index.md)

###### Rolling releases (EAP)

- [Overview](https://developer.atlassian.com/platform/forge/rolling-releases.md)
- [Tutorial](https://developer.atlassian.com/platform/forge/rolling-releases-tutorial.md)

#### Distribution

- [Distribute via console](https://developer.atlassian.com/platform/forge/distribute-your-apps.md)
- [CLI installation](https://developer.atlassian.com/platform/forge/cli-reference/install.md)

#### Feature flags

##### Overview

- [Overview](https://developer.atlassian.com/platform/forge/feature-flags/overview.md)

##### Tutorials

- [Your first feature flag](https://developer.atlassian.com/platform/forge/feature-flags/featureflags-quickstart.md)
- [Page bookmark Confluence app](https://developer.atlassian.com/platform/forge/feature-flags/page-bookmark-feature-flag.md)
- [Dark mode switcher Confluence app](https://developer.atlassian.com/platform/forge/feature-flags/dark-mode-feature-flag.md)

##### How-to guides

- [Roll out to a percentage of users](https://developer.atlassian.com/platform/forge/feature-flags/how-to-percentage-rollouts.md)
- [Target specific users or organizations](https://developer.atlassian.com/platform/forge/feature-flags/how-to-target-users.md)
- [Use environment-specific flags](https://developer.atlassian.com/platform/forge/feature-flags/how-to-environment-specific.md)

##### Reference

- [Server-side SDK](https://developer.atlassian.com/platform/forge/feature-flags/feature-flags-sdk.md)
- [Client SDK](https://developer.atlassian.com/platform/forge/feature-flags/feature-flags-client-sdk.md)
- [Limitations and constraints](https://developer.atlassian.com/platform/forge/feature-flags/limitations.md)

##### Explanation

- [Core concepts](https://developer.atlassian.com/platform/forge/feature-flags/concepts.md)
- [Client SDK vs server-side SDK](https://developer.atlassian.com/platform/forge/feature-flags/client-vs-server-sdk.md)

## Reference

- [Reference](https://developer.atlassian.com/platform/forge/manifest-reference/index.md)

### Containers (EAP)

#### Forge Containers overview

- [Forge Containers overview](https://developer.atlassian.com/platform/forge/containers-reference/index.md)

#### Roadmap

- [Roadmap](https://developer.atlassian.com/platform/forge/containers-reference/roadmap.md)

#### Pricing (coming soon)

- [Pricing (coming soon)](https://developer.atlassian.com/platform/forge/containers-reference/pricing.md)

#### Reference

- [Reference](https://developer.atlassian.com/platform/forge/containers-reference/reference.md)
- [Glossary](https://developer.atlassian.com/platform/forge/containers-reference/ref-glossary.md)
- [Manifest](https://developer.atlassian.com/platform/forge/containers-reference/ref-manifest.md)
- [CLI tools](https://developer.atlassian.com/platform/forge/containers-reference/ref-cli.md)
- [API contract](https://developer.atlassian.com/platform/forge/containers-reference/ref-api.md)
- [Logging format](https://developer.atlassian.com/platform/forge/containers-reference/ref-logging.md)

#### Managing a service

- [Managing a service](https://developer.atlassian.com/platform/forge/containers-reference/managing-service.md)

#### Integrating a service

- [Integrating a service](https://developer.atlassian.com/platform/forge/containers-reference/integrating-service.md)
- [Event invocations](https://developer.atlassian.com/platform/forge/containers-reference/int-event.md)
- [Frontend/backend invocations](https://developer.atlassian.com/platform/forge/containers-reference/int-invokeservice.md)
- [Call APIs from an installation](https://developer.atlassian.com/platform/forge/containers-reference/int-installbased.md)
- [Web trigger invocations](https://developer.atlassian.com/platform/forge/containers-reference/int-webtrigger.md)

#### Testing a service locally

- [Testing a service locally](https://developer.atlassian.com/platform/forge/containers-reference/test-service-locally.md)
- [Hot reloading](https://developer.atlassian.com/platform/forge/containers-reference/test-service-locally-hot-reloading.md)
- [Get help](https://developer.atlassian.com/platform/forge/get-help.md)
```

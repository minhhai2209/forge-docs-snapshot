# Install the Forge AI Plugin

The Forge AI Plugin bundles Forge-focused skills and MCP-backed tooling so your AI coding agent can scaffold apps, review them before deploy, debug production issues, and stay current on Forge APIs and the Atlassian Design System.

## What's included

The plugin provides the following [skills](/platform/forge/ai-development-toolkit/forge-developer-skills/) and [MCP servers](/platform/forge/ai-development-toolkit/forge-mcp/):

### Skills

| Skill | What it does | Sample capabilities |
| --- | --- | --- |
| `forge-app-builder` | Guides scaffolding through production: `forge create`, developer spaces and templates, deploy and install, module selection, cross-product scopes, and common CLI or permission issues. | Forge CLI, environments, cross-product scopes |
| `forge-app-review` | Supports pre-deploy review and audits: security, architecture, cost and invocation efficiency, performance, and trigger or scheduling waste. | Audit before release, reduce invocations, find misconfigurations |
| `skills/forge-debugger` | Supports systematic troubleshooting: deploy errors, resolver failures, blank or missing UI, scopes and permissions, and apps that stopped working in Jira or Confluence. | Logs, blank panels, resolver errors, missing app in UI |

### MCP servers

| MCP server | What it does | Sample capabilities |
| --- | --- | --- |
| **Forge MCP Server** | Gives your agent access to up-to-date Forge documentation, template registries, module configuration, manifest syntax, and UI Kit/backend API guides. | Template lookup, manifest syntax, UI Kit guides, backend API reference |
| **ADS MCP Server** | Provides [Atlassian Design System](https://atlassian.design/design-system) lookup for Custom UI apps: component discovery, token reference, and icon search via the `@atlaskit` library. | Component discovery, token reference, icon lookup (Custom UI only) |

## Prerequisites

Before you install, make sure you have:

## Install the plugin

Run the appropriate command to install the Forge Skills Plugin on your chosen agent:

Claude Code

Cursor

Gemini CLI

GitHub Copilot CLI

Rovo Dev

```
```
1
2
```



```
/plugin install forge-skills@atlassian-forge-skills
```
```

## Verify the installation

After installing, run three quick checks to confirm everything is working.

### 1. Verify the skill layer

Ask your agent:

```
```
1
2
```



```
Build me a Jira issue panel that shows customer support tickets.
```
```

You should get a structured Forge workflow — developer space discovery, template selection, `forge create`, code customization, and deployment — not just generic code snippets.

You can also confirm the other skills:

* **Review:** "Review my Forge app for security and unnecessary trigger invocations before I deploy."
* **Debug:** "My Forge issue panel is blank after deploy — help me trace it."

### 2. Verify the Forge MCP Server

Ask your agent:

```
```
1
2
```



```
What Forge templates are available for Confluence macros?
```
```

You should get a response backed by live Forge documentation, not generic training data.

### 3. Verify the ADS MCP Server (Custom UI only)

Ask your agent:

```
```
1
2
```



```
What Atlaskit components should I use for a data table?
```
```

You should get a response backed by the [Atlassian Design System](https://atlassian.design/design-system), with specific component names and import paths.

## Learn more

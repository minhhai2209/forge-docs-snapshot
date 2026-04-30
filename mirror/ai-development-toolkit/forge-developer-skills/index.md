# Install Forge skills

*Forge skills* add Forge-specific capabilities to your AI coding agent. You can install all skills at once or pick individual skills based on what you need. These are the same skills packaged with the [Forge AI Plugin](/platform/forge/ai-development-toolkit/forge-ai-plugin/).

## Available skills

| Skill | What it does |
| --- | --- |
| `forge-app-builder` | Guides scaffolding through production: `forge create`, developer spaces and templates, deploy and install, module selection, cross-product scopes, and common CLI or permission issues. |
| `forge-app-review` | Supports pre-deploy review and audits: security, architecture, cost and invocation efficiency, performance, and trigger or scheduling waste. |
| `forge-debugger` | Supports systematic troubleshooting: deploy errors, resolver failures, blank or missing UI, scopes and permissions, and apps that stopped working in Jira or Confluence. |

## Install all skills

To install all Forge developer skills at once:

```
1
npx skills add atlassian/forge-skills
```

## Install an individual skill

Use the `--skill` flag to install a specific skill:

```
1
npx skills add atlassian/forge-skills --skill forge-app-builder
```

## Prompts to try

Once your skills are installed, try prompts like these:

**Forge App Builder:**

```
```
1
2
```



```
Create a Jira issue panel that shows related support tickets from an external API.
```
```

```
```
1
2
```



```
Build a Confluence macro that embeds an interactive chart with bar, line, and pie options.
```
```

```
```
1
2
```



```
What scopes do I need for a Confluence app that also reads Jira data?
```
```

**Forge App Review:**

```
```
1
2
```



```
Review my Forge app for security and unnecessary trigger invocations before I deploy.
```
```

```
```
1
2
```



```
Audit my app's architecture for cost efficiency.
```
```

**Forge Debugger:**

```
```
1
2
```



```
My Forge issue panel is blank after deploy — help me trace it.
```
```

```
```
1
2
```



```
My app stopped appearing in Jira after a recent deploy. What could have gone wrong?
```
```

## Learn more

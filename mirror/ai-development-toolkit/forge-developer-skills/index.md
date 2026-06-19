# Install Forge skills

*Forge skills* add Forge-specific capabilities to your AI coding agent. You can install all skills at once or pick individual skills based on what you need. These are the same skills packaged with the [Forge AI Plugin](/platform/forge/ai-development-toolkit/forge-ai-plugin/).

## Available skills

| Skill | What it does |
| --- | --- |
| `forge-app-builder` | Guides scaffolding through production: `forge create`, developer spaces and templates, deploy and install, module selection, cross-product scopes, and common CLI or permission issues. |
| `forge-app-review` | Performs a lightweight release-readiness review across manifest and module wiring, architecture, runtime compatibility, dependency posture, tests, deploy readiness, and obvious security, cost, or reliability signals. |
| `forge-cost-optimizer` | Helps reduce Forge platform consumption across invocations, storage, logs, memory, triggers, API calls, and frontend or backend boundaries. |
| `forge-debugger` | Supports systematic troubleshooting: deploy errors, resolver failures, blank or missing UI, scopes and permissions, and apps that stopped working in Jira or Confluence. |
| `forge-connector` | Guides building `graph:connector` apps that ingest external data into Atlassian's Teamwork Graph so it can appear in Rovo Search and Rovo Chat. |
| `forge-security-review` | Performs white-box Forge app security audits with rule-driven checks for authorization, injection, tenant isolation, secrets handling, egress and remotes, web triggers, and static analysis workflows. |

## Install all skills

To install all Forge developer skills at once:

```
```
1
2
```



```
npx skills add atlassian/forge-skills
```
```

## Install an individual skill

Use the `--skill` flag to install a specific skill:

```
```
1
2
```



```
npx skills add atlassian/forge-skills --skill forge-app-builder
```
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
Review my Forge app before release and tell me whether it is ready to ship.
```
```

```
```
1
2
```



```
Check my manifest, resolver wiring, dependencies, and tests before I deploy.
```
```

**Forge Cost Optimizer:**

```
```
1
2
```



```
Audit my Forge app for unnecessary invocations, storage writes, logs, and memory usage.
```
```

```
```
1
2
```



```
Optimize this app's scheduled triggers and resolver calls to reduce Forge platform consumption.
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

**Forge Connector:**

```
```
1
2
```



```
Build a Forge connector that ingests external project data into Rovo Search.
```
```

```
```
1
2
```



```
Where should I start if I want to surface ServiceNow knowledge articles in Rovo Chat?
```
```

**Forge Security Review:**

```
```
1
2
```



```
Run a white-box security review on this Forge app and include CVSS-scored findings.
```
```

```
```
1
2
```



```
Review this Forge web trigger for authentication, authorization, and tenant isolation issues.
```
```

## Learn more

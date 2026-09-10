# Rovo Skill (EAP)

Forge’s EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.

To join the EAP for Forge Rovo Skills, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18258).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

The `rovo:skill` module packages reusable instructions that help Rovo Agents complete specialized tasks. A skill consists of a `SKILL.md` instruction file, optional supporting files, and optional [action](/platform/forge/manifest-reference/modules/rovo-action/) dependencies from the same Forge app.

Forge validates and bundles each skill when you deploy the app. During the EAP, you can deploy apps that use `rovo:skill` only to development environments.

## Manifest structure

```
1modules {}
2└─ rovo:skill []
3   ├─ key (string) [Mandatory]
4   ├─ source {} [Mandatory]
5   │  └─ dir (string) [Mandatory]
6   └─ dependencies {} [Optional]
7      └─ tools [] [Mandatory if dependencies is specified]
8         └─ action (string)
9
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `source` | `object` | Yes | Identifies the directory that contains the skill. |
| `source.dir` | `string` | Yes | A relative path from the directory containing `manifest.yml` to the skill directory. The directory must exist, contain a `SKILL.md` file, and be unique among the app's `rovo:skill` modules. |
| `dependencies` | `object` | No | Declares the Forge tools that the skill can use. |
| `dependencies.tools` | `string[]` | Yes, if `dependencies` is specified | A list of [action](/platform/forge/manifest-reference/modules/rovo-action/) module keys from the same app. Each referenced action must exist in the manifest. Duplicate keys aren't allowed. |

## Skill directory

Each skill has its own directory. At minimum, the directory must contain a `SKILL.md` file:

```
```
1
2
3
4
5
```



```
skills/
└─ jira-issue-analyst/
   ├─ SKILL.md
   └─ references/ [Optional]
```
```

The directory can contain supporting reference documents. Refer to supporting files from `SKILL.md` using paths relative to the skill directory, for example `references/issue-fields.md`.

Executable scripts in a skill directory aren't supported during the EAP.

### `SKILL.md` format

The `SKILL.md` file follows the [Agent Skills specification](https://agentskills.io/specification). It must contain YAML frontmatter followed by Markdown instructions:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
```



```
---
name: jira-issue-analyst
description: Retrieve and summarize Jira issues for a project or sprint when users need an issue analysis.
allowed-tools: get-project-issues
---

# Jira issue analysis

Use `get-project-issues` to retrieve the issues for the project or sprint requested by the user.

Summarize the result by status and priority. Highlight blocked work and issues without an assignee.
```
```

The `name` must match the name of the directory that contains `SKILL.md`. In this example, the directory is `skills/jira-issue-analyst`.

The following frontmatter fields are supported:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | Yes | The skill name. Must be 1–64 characters, contain only lowercase letters, numbers, and single hyphens, and match the parent directory name. It must not start or end with a hyphen. |
| `description` | `string` | Yes | Describes what the skill does and when an Agent should use it. Must be 1–1,024 characters. Use at least 50 characters to give the Agent enough information to discover the skill reliably. |
| `compatibility` | `string` | No | Describes environment or product requirements. Must be 1–500 characters when specified. |
| `metadata` | `object` | No | Additional metadata as string key-value pairs. |
| `license` | `string` | No | The license that applies to the skill, or a reference to a bundled license file. |
| `allowed-tools` | `string` | No | A space-separated list of tool keys. If specified, it must include every action listed in `dependencies.tools`. |

Write the Markdown body as instructions for the Agent. Explain when and how to use every action in `dependencies.tools`, how to interpret its results, and how to handle expected errors or edge cases. Keep the Markdown body of `SKILL.md` to 500 lines or fewer. Forge CLI warns when the body exceeds this length. Move detailed material into focused files under `references`.

## Manifest example

The following example shows only the relevant modules. A complete manifest also requires an `app` section that defines the app ID and runtime, and a `permissions` section that declares the scopes required by the actions.

It defines a skill backed by an action and makes that skill available to a Forge Rovo Agent:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
```



```
modules:
  function:
    - key: get-project-issues-function
      handler: src/index.getProjectIssues

  action:
    - key: get-project-issues
      name: Get project issues
      function: get-project-issues-function
      actionVerb: GET
      description: Retrieve Jira issues for a project
      inputs:
        projectKey:
          title: Project key
          type: string
          required: true
          description: The key of the Jira project to retrieve issues from

  rovo:skill:
    - key: jira-issue-analyst
      source:
        dir: skills/jira-issue-analyst
      dependencies:
        tools:
          - get-project-issues

  rovo:agent:
    - key: issue-analyst-agent
      name: Issue analyst
      description: An Agent that analyzes work in a Jira project
      prompt: Help users understand the status of work in their Jira projects.
      skills:
        - jira-issue-analyst
```
```

Declare the OAuth scopes required by the actions in the app's `permissions.scopes`. The `rovo:skill` module doesn't introduce additional scopes or a separate consent step.

## Use a skill with a Forge Rovo Agent

To make a skill available to a [Forge Rovo Agent](/platform/forge/manifest-reference/modules/rovo-agent/), add the `rovo:skill` module key to the Agent's `skills` property. A Forge Rovo Agent can access only the skills declared in its `skills` property.

At runtime, the Agent selects a skill based on its description and the user's request. Explicit invocation by name isn't supported during the EAP.

## Limits and restrictions

* A skill directory must not exceed 100 MB uncompressed.
* Tool dependencies must be `action` modules declared by the same app.

## EAP limitations

* Apps that declare `rovo:skill` can be deployed only to a development environment.
* Skill-to-skill dependencies aren't supported.
* Executable skill sources, including scripts, aren't supported.

# Rovo Agent

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

The `rovo:agent` module defines an Agent. Agents are configurable AI teammates that integrate into Jira and Confluence workflows. You can define an Agent's behaviour using a prompt and an action, so the Agent can fetch data and perform operations.

## Data access

Unlike Agents built using an Atlassian app user interface (UI), app-based Agents only have access to the data in the workspace that the app is installed in. For instance, if there is a Confluence page located at yourtenant.atlassian.net that describes your team's CI/CD process, an app-based Agent that is installed in Jira at yourtenant.atlassian.net will not have automatic access to it.

To enable your Agent to access data from multiple Atlassian apps, configure your app to support multiple Atlassian apps. See [App compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility--preview-).

## Manifest structure

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
modules {}
└─ rovo:agent []
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ description (string) [Optional]
   ├─ icon (string) [Optional]
   ├─ prompt (string) [Mandatory]
   ├─ conversationStarters [] [Optional]
   │  └─ conversationStarter (string)
   ├─ actions [] [Optional]
   │  └─ action (string)
   └─ followUpPrompt (string) [Optional]

resources []
└─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

In this structure:

* The `rovo:agent` array includes properties such as `key`, `name`, `description`, `icon`, `prompt`, `conversationStarters`, `actions`, and `followUpPrompt`.
* The `conversationStarters` array and `actions` array are represented with generic entries `conversationStarter` and `action`, respectively.
* The `resources` array includes properties `key` and `path`.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | The name of your Agent. Must not exceed 30 characters. |
| `description` | `string` |  | The description of your Agent. This is used to describe what your Agent can do to users. |
| `icon` | `string` |  | The icon displayed as the Agent’s avatar.  The `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic avatar will be displayed. |
| `prompt` | `string` | Yes | This is the custom LLM prompt where you describe how your Agent will behave.  You can specify the `prompt` as a string or provide it as a relative path to a declared resource. See, the [prompt as resource example](/platform/forge/manifest-reference/modules/rovo-agent/#prompt-as-a-resource). |
| `conversationStarters` | `string[]` |  | Conversation starters that will be suggested to the user when they engage with your Agent. |
| `actions` | `actions` |  | A list of the actions that the Agent can invoke. |
| `followUpPrompt` | `string` |  | A prompt that will be used to generate follow up suggestions once the user’s original query has been answered. |

## Manifest example

Here is an example manifest file for creating an Agent that assists with managing project risks:

```
```
1
2
```



```
modules:
  rovo:agent: 
    - key: risk-agent
      name: "My Risk Register Assistant"
      description: A Rovo Agent that helps you manage your project risks
      icon: resource:example-resource;icons/risk-agent.svg
      prompt: |
        You are a helpful assistant that helps users manage their project risks. 
        You can retrieve risks from the risk register, create new risks and update existing ones.
      conversationStarters:
        - Fetch my active project risks
        - Fetch my highest priority risks
        - Create a new risk
      actions:
        - fetch-all-risks
        - fetch-risk-by-priority
        - create-risk
        - update-risk
resources:
  - key: example-resource
    path: static/hello-world/build
```
```

### prompt as a resource

```
```
1
2
```



```
modules:
  rovo:agent: 
    - key: risk-agent
      name: "My Risk Register Assistant"
      description: A Rovo Agent that helps you manage your project risks
      icon: resource:example-resource;icons/risk-agent.svg
      prompt: resource:agent-resource;prompts/agent-prompt.txt
      conversationStarters:
        - Fetch my active project risks
        - Fetch my highest priority risks
        - Create a new risk
      actions:
        - fetch-all-risks
        - fetch-risk-by-priority
        - create-risk
        - update-risk
resources:
  - key: example-resource
    path: static/hello-world/build
  - key: agent-resource
    path: resource/agent
```
```

Here `agent:prompt` refers to following string resource: `resource/agent/prompts/agent-prompt.txt`

```
```
1
2
```



```
You are a helpful assistant that helps users manage their project risks. 
You can retrieve risks from the risk register, create new risks and update existing ones.
```
```

## Agent interaction points

### Programmatic access via Forge bridge

Using the [Forge bridge rovo API](/platform/forge/apis-reference/ui-api-bridge/rovo/), you can initiate a conversation in the Rovo chat sidebar with your Forge Rovo agent.

### Chat side panel (Confluence and Jira)

Accessed by clicking the **Chat** button in the top navigation bar

![Example of a chat button](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-chat-side.png?_v=1.5800.1739)

Accessed using the /ai command in the editor

![Example of a chat button](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-ai-toolbar.png?_v=1.5800.1739)

Accessed using the /ai command in the Jira issues editor

![Example of a chat button](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-ai-toolbar-jira.png?_v=1.5800.1739)

### Automation (Confluence and Jira)

You can add Agents to Automation rules. This will invoke the Agent to act asynchronously in response to Atlassian app events or schedules.
When users configure an automation rule they will set an additional prompt with specific instructions how to act during that rule. The response from the Agent can be passed to subsequent steps in the automation rule using smart values.

![Example of a chat button](https://dac-static.atlassian.com/platform/forge/images/rovo/automations.png?_v=1.5800.1739)

## Writing effective prompts

When creating prompts for an Agent, it is essential to define the Agent's purpose, personality, output format, capabilities, and other relevant aspects. The structure of your prompts should align with the specific tasks you intend to delegate to the Agent and the nature of the actions you aim to develop.

For crafting a compelling prompt, it is advisable to incorporate the following key components:

### Define the role of your Agent

Roles play a crucial role in shaping the language, tone, style, and personality of your Agent.

**Example**:

```
```
1
2
```



```
You are an expert project manager tasked with managing risks for a project.
```
```

### Outline what your Agent can assist with

Outline the various jobs that the Agent can assist users with. The list does not need to be comprehensive.

```
```
1
2
```



```
You can help with the following jobs:

A. Reviewing high priority risks
B. Generating executive reports on project risks
C. Updating the risk register with new risks
D. Evaluating the impact of risks on project objectives
```
```

### Format and structure your prompt

Add logic/structure to longer prompts using delimiters. This improves instruction quality and readability.

```
```
1
2
```



```
I'll separate the instructions for each job with a. '---' on a new line, followed by the job title.
---
A. Reviewing high priority risks
When asked, you can help teams to review high priority risk and critique it based on likelihood, impact, and mitigation.
To do this, follow these steps:

--- 
B. Generating executive reports on project risks
To do this, follow these steps:
```
```

### Define when actions should be invoked

Instruct your Agent on how to execute more complex jobs by defining the actions it should take.

```
```
1
2
```



```
Reviewing high priority risks
When asked, you can help teams to review high priority risk and critique it based on likelihood, impact, and mitigation.

To do this, follow these steps:
1. Retrieve the list of high priority risks from the risk register using the fetch-risk-by-priority action.
2. Critique each risk based on likelihood, impact, and mitigation.
3. Provide a final rating of the risk on a scale from 1 to 10, where 1 is an extremely low risk and 10 is an extremely high risk.
```
```

### Define to format of output

Define how your Agent will structure its responses when performing certain jobs.

```
```
1
2
```



```
* Use emoji to highlight what the rating score for each risk. Use this emoji scoring
🔴 - Red circle emoji to highlight if there is a high risk (8-10). 
🟡 - Yellow circle emoji to highlight if there is a medium risk (4-7)
🟢 - Green circle emoji - to reflect low risks (1-3).
```
```

These are some basic guidelines to help you craft effective prompts for your Agent. You can customize these guidelines to suit your Agent's specific requirements.

## Tutorial

# rovo (Preview)

The Forge bridge `rovo` API is now available as a Preview capability. Preview capabilities are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview capabilities are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The Forge bridge `rovo` API enables your app to programmatically open the Rovo chat sidebar and initiate conversations with specific agents. Use this to provide contextual AI assistance by launching Rovo agents with pre-filled prompts based on user actions or data within your Forge app.

The `rovo` APIs are currently supported in:

* All Jira modules
* All Confluence modules
* The following Jira Service Management modules: `jiraServiceManagement:organizationPanel` and `jiraServiceManagement:queuePage`

## open

The `open` method allows you to open the Rovo chat sidebar and create a new conversation with the default or a specified Rovo agent.

### Function signature

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
function open(
  openRovoPayload?:
    | ForgeAgentPayload
    | AtlassianAgentPayload
    | DefaultAgentPayload,
): Promise<void>;

type ForgeAgentPayload = {
  type: "forge";
  agentName: string;
  agentKey: string;
  prompt?: string;
};

type AtlassianAgentPayload = {
  type: "atlassian";
  agentName: string;
  prompt?: string;
};

type DefaultAgentPayload = {
  type: "default";
  prompt?: string;
};
```

### Arguments

#### OpenRovoPayload

* **type**: The type of the Rovo agent.
* **agentName**: The name of the Rovo agent.
* **agentKey**: The key of the Forge Rovo agent module.
* **prompt**: An optional prompt to send to the new conversation.

Non-Forge custom agents are currently not supported for this method.
You can only open Forge agents that are created in the same app
from where the method is called.

### Examples

#### Forge agent

```
```
1
2
```



```
import { rovo } from "@forge/bridge";
...
await rovo.open({
  type: "forge",
  agentName:"My agent",
  agentKey: "my-agent-key",
  prompt:"Optional prompt"
});
```
```

#### Non-Forge agent

```
```
1
2
```



```
import { rovo } from "@forge/bridge";
...
await rovo.open({
  type: "atlassian",
  agentName:"My agent",
  prompt:"Optional prompt"
});
```
```

#### Default agent

```
```
1
2
```



```
import { rovo } from "@forge/bridge";
...
await rovo.open({
  type: "default",
  prompt:"Optional prompt"
});
```
```

## isEnabled

The `isEnabled` method returns a boolean value indicating whether Rovo is enabled in the current tenant.

### Example

```
```
1
2
```



```
import { rovo } from "@forge/bridge";
...
const isEnabled = await rovo.isEnabled();
if (isEnabled) {
  await rovo.open({
    type: "forge",
    agentName: "My agent",
    agentKey: "my-agent-key",
    prompt: "Optional prompt"
  });
}
```
```

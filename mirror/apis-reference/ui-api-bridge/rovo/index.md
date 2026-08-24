# rovo

The Forge bridge `rovo` API enables your app to programmatically open the Rovo chat sidebar and initiate conversations with specific agents. Use this to provide contextual AI assistance by launching Rovo agents with pre-filled prompts based on user actions or data within your Forge app.

The `rovo` APIs are currently supported in:

* All Jira modules
* All Confluence modules
* The following Jira Service Management modules: `jiraServiceManagement:organizationPanel` and `jiraServiceManagement:queuePage`

## open

The `open` method allows you to open the Rovo chat sidebar and create a new conversation with the default or a specified Rovo agent.

### Function signature

```
1function open(
2  openRovoPayload?:
3    | ForgeAgentPayload
4    | AtlassianAgentPayload
5    | DefaultAgentPayload,
6): Promise<void>;
7
8type ForgeAgentPayload = {
9  type: "forge";
10  agentName: string;
11  agentKey: string;
12  prompt?: string;
13};
14
15type AtlassianAgentPayload = {
16  type: "atlassian";
17  agentName: string;
18  prompt?: string;
19};
20
21type DefaultAgentPayload = {
22  type: "default";
23  prompt?: string;
24};
25
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
3
4
5
6
7
8
9
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
3
4
5
6
7
8
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
3
4
5
6
7
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

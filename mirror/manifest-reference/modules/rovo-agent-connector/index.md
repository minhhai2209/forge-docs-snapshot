# Rovo Agent Connector (EAP)

Rovo Agent Connector is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production. [Sign up here](https://go.atlassian.com/signup-forge-agent-connector) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The `rovo:agentConnector` module allows you to integrate remote AI agents hosted on external infrastructure into Jira. Once a remote agent is registered, users can interact with them in a similar manner to other users and Rovo agents: assigning them work items, @mentioning them in comments, and chatting with them via the Rovo Chat panel.

Use this module to integrate Jira with AI agents residing outside of the Atlassian platform (such as GitHub Copilot, Cursor Background Agents, or Box AI Agents).

## Requirement: Agent2Agent protocol server

Remote agents must implement an Agent2Agent (A2A) protocol server to communicate with Jira. The [A2A protocol](https://google.github.io/A2A/) is an open standard that enables AI agents to communicate with each other, regardless of the underlying framework or vendor.

For more information, see [Getting Started](https://github.com/a2aproject/A2A#getting-started).

Jira communicates with remote agents via the [JSON-RPC 2.0](https://www.jsonrpc.org/specification) protocol. Your remote service must expose an endpoint that accepts JSON-RPC requests from Jira and returns responses according to the A2A protocol specification.

## EAP limitations

During the EAP, apps using Rovo Agent Connector:

* Can't be deployed to the `production` and `staging` [environments](/platform/forge/environments-and-versions/).
* Can't be distributed or listed on the Atlassian Marketplace.

## Timeouts

| Transport Type | Timeout |
| --- | --- |
| `streaming=false` (sync invocation) | 55s |
| `streaming=true` (SSE stream) | 900s (15min) |

Note that in case of timeouts during the streaming requests, the product (ie, Jira) will attempt to reconnect automatically to the remote agent.

## Manifest structure

```
```
1
2
```



```
modules {}
└─ rovo:agentConnector []
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ description (string) [Optional]
   ├─ icon (string) [Optional]
   ├─ conversationStarters [] [Optional]
   │  └─ conversationStarter (string)
   ├─ productContexts [] [Mandatory]
   │  └─ product (string)
   └─ protocols [] [Mandatory]
      └─ agent2Agent
         └─ jsonRpcTransport
            ├─ streaming (boolean)
            └─ endpoint (string)

remotes []
└─ key (string) [Mandatory]
└─ baseUrl (string) [Mandatory]

resources []
└─ key (string) [Mandatory]
└─ path (string) [Mandatory]

permissions []
└─ scopes []
  └─ scope (string) [Mandatory]
```
```

In this structure:

* The `rovo:agentConnector` module defines a remote agent with metadata and communication protocols.
* The `endpoint` property references a separately defined [`endpoint` module](/platform/forge/manifest-reference/endpoint/), which specifies the route Jira uses to communicate with your remote agent via JSON-RPC.
* The `remotes` configuration identifies the domain of your remote service and enables authentication tokens to be passed to your service.
* The `resources` module provides static assets like the agent icon.
* The `productContexts` property specifies which Atlassian products the agent operates in. Only `jira` is supported during the EAP.
* The `permissions.scopes` array declares the OAuth scopes your app requires. The `read:jira-work` scope is required for the agent to function correctly.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | The name of your Agent. Must not exceed 30 characters. |
| `description` | `string` |  | The description of your Agent. This is used to describe what your Agent can do to users. |
| `icon` | `string` |  | The icon displayed as the Agent’s avatar.  The `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic avatar will be displayed. |
| `conversationStarters` | `string[]` |  | Conversation starters that will be suggested to the user when they engage with your Agent. |
| `productContexts` | `string[]` | Yes | The Atlassian apps within which the agent should operate.  Only `jira` can be used during the EAP. |
| `protocols` | `object` | Yes | Defines the protocols and transport mechanisms your remote agent uses to communicate with Jira.  See [A2A Protocols](#a2a-protocols) for more configuration details |

### A2A Protocols

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `agent2Agent` | `object` | Yes | Configures communication using the Agent2Agent (A2A) protocol. Currently, only `jsonRpcTransport` is supported. |
| `agent2Agent` `.jsonRpcTransport` | `object` | Yes | Enables Agent2Agent protocol over JSON-RPC 2.0 transport.  See [Transport properties](#transport-properties) for more configuration details |

### Transport properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `endpoint` | `string` | Yes | The key of the endpoint that should be invoked for JSON-RPC communication with your remote agent. |
| `streaming` | `boolean` |  | Whether responses from the remote agent are streamed back to Jira incrementally using [Server-Sent Events (SSE)](https://a2a-protocol.org/latest/topics/streaming-and-async/#streaming-with-server-sent-events-sse). Defaults to `false`. |

The `rovo:agentConnector` module works together with other manifest configurations to enable remote agent integration:

## Manifest example

The following example manifest file defines an `rovo:agentConnector` that connects to your remotely hosted agent:

```
```
1
2
```



```
modules:
  rovo:agentConnector:
    - key: your-awesome-agent
      name: Your Awesome Agent
      description: An awesome agent that you built
      icon: resource:agent-resources;icons/your-agent.svg
      productContexts:
        - jira
      protocols:
        agent2Agent:
          jsonRpcTransport:
            endpoint: a2a-json-rpc-endpoint
            streaming: true
  endpoint:
    - key: a2a-json-rpc-endpoint
      remote: agent-remote
      route:
        path: /a2a/json-rpc
remotes:
  - key: agent-remote
    baseUrl: https://youragent.com
    operations:
      - fetch
      - compute
      - other
resources:
  - key: agent-resources
    path: static/hello-world/build
permissions:
  scopes:
    - read:jira-work
```
```

## Tutorials and example apps

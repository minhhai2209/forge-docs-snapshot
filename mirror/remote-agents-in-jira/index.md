# Integrate remote agents with Jira (EAP)

Remote agents in Jira are available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production. [Sign up here](https://go.atlassian.com/signup-forge-agent-connector) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This guide is intended for developers seeking to integrate **AI agents running on external infrastructure** (referred to in this guide as *Remote Agents*) into Jira. For patterns to enable [Rovo agents](https://www.atlassian.com/software/rovo/features) running on Atlassian's AI agent platform to interact with external APIs or MCP servers, see the following:

* If your product has a published MCP server, users can register it with a [custom Rovo agent](https://support.atlassian.com/rovo/docs/create-and-edit-agents/) created in Atlassian Studio.
* If your product has a public API, you can develop a custom Rovo agent and actions that interact with your APIs using [the Forge platform](/platform/forge/manifest-reference/modules/rovo-index/) and publish it on Marketplace.

This guide is intended for developers building deep integrations between Jira and a Remote Agent that resides outside of the Atlassian platform — e.g. GitHub Copilot, Cursor Agents, OpenAI Codex, or Anthropic Claude.

## What can remote agents do?

Remote agents can be assigned work items, @mentioned in comments, and chatted with via the Rovo Chat panel. Typically a remote agent works with the user who assigned them work, providing updates and completed work artifacts that the user reviews and approves before posting them to the work item.

After following this guide, you will have an agent that can:

* be assigned work items, @mentioned in comments, or chatted to by a human user
* surface updates in Jira as it executes on a task
* elicit further context and requirements from the user, if required
* fetch further context programmatically from the [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
* be installed into any Jira Cloud site, and (optionally) published on the Atlassian Marketplace

## Terminology

The following terms describe key integration concepts used throughout this guide:

**Remote Agent** or **Agent** — The AI agent (hosted by you) that you are aiming to integrate with Jira.

**Remote Service** — The web application (also hosted by you) that is capable of sending and receiving requests to and from Jira Cloud and is capable of passing messages to your remote agent.

This guide assumes you are operating a typical multi-tenant SaaS-style web application, and is not suitable for "on-premise" web applications deployed behind customer firewalls.

**Forge app** — A middleware application built on [Forge](/platform/forge/) (Atlassian's cloud developer platform) that is used to register your agent with Atlassian, make it installable in Jira, and — optionally — distributable via the [Atlassian Marketplace](https://marketplace.atlassian.com). This Forge app is built and maintained by you, but is deployed to Atlassian's platform.

**Jira tenant** or **Jira site** — Jira is a multi-tenant web application hosted on Atlassian infrastructure. Each tenant is accessible under a different base URL, typically `${customer-subdomain}.atlassian.net`, though the domain and TLD may vary. If listing on the Atlassian Marketplace, your remote agent must be ready to handle installations and tasks from multiple Jira tenants.

![Simplified integration architecture showing a Jira site, a Forge app acting as middleware, and the remote service hosting the agent](https://dac-static.atlassian.com/platform/forge/images/remote-agents/architecture.png?_v=1.5800.2167)

*Simplified integration architecture*

## Prerequisites

We recommend completing the [Jira "Hello World" Forge](/platform/forge/build-a-hello-world-app-in-jira/) tutorial before beginning implementation.

This typically takes less than 60 minutes, and will get you set up with a free Atlassian cloud account and development Jira site, as well as the Forge developer toolchain and your first Jira app deployed into a development environment.

## About this guide

The remainder of this guide covers everything you need to know about extending your remote service to integrate with Jira. It is broken into four parts:

* [**1. Agent installation and lifecycle**](#1--agent-installation-and-lifecycle) — covers how to package your agent as a Forge app that is installable in Jira Cloud sites and (optionally) discoverable on the Atlassian Marketplace
* [**2. Handling Jira tasks**](#2--handling-jira-tasks) — covers task handling protocols for accepting, processing, and completing tasks initiated by users in Jira, including optional streaming support
* [**3. Agent configuration**](#3--agent-configuration) — covers how to surface configuration experiences in Jira for administrators and end-users to link accounts and customise agent behaviour
* [**4. Technical appendices**](#4--technical-appendices) — covers the JSON-RPC methods you'll need to implement, request and response schemas, Forge module references, and authentication protocols

We recommend reading through the first three sections in order, referring to the technical appendices as necessary.

## 1. Agent installation and lifecycle

To integrate your remote agent with Jira, you will need to create and deploy a [Forge app](/platform/forge/) to act as middleware between Jira and the remote service you will use to invoke your agent. This app will contain several modules:

* an [`agentConnector`](/platform/forge/manifest-reference/modules/rovo-agent-connector/) module, with metadata describing your remote agent
* a [remote](/platform/forge/manifest-reference/remotes/) and [endpoints](/platform/forge/manifest-reference/endpoint/), identifying the domain and routes that Jira should use to communicate with your remote agent
* an installation [trigger](/platform/forge/manifest-reference/modules/trigger/) module, allowing your remote service to receive events when users install or upgrade your agent in Jira
* (optional) UI modules for surfacing configuration and other end-user experiences in Jira — covered in depth in the [Agent configuration](#3--agent-configuration) section below

The [Forge Manifest Reference](#forge-manifest-reference) shows an example of how these are represented in a Forge manifest.

## Agent installation

Agent installation has a number of discrete steps:

1. The remote agent is installed by a customer administrator via the [Atlassian Marketplace](https://marketplace.atlassian.com/) or via a [direct distribution](/platform/forge/distribute-your-apps/#start-sharing-your-app) URL that you have provided them.
2. When the app is installed, your remote service will receive an [installation event](/platform/forge/events-reference/life-cycle/#life-cycle-events) sent as a webhook to the endpoint nominated in your Forge app manifest. Your agent must verify the webhook using JWKS, as described in [Authenticating requests from Jira to your agent](#authenticating-requests-from-jira-to-your-agent).

Always verify events sent as webhooks using JWKS before processing them. Failing to verify webhooks could allow malicious actors to spoof events.

3. After receiving and verifying an installation event, your remote service may optionally call the Jira REST API to retrieve additional information about the Jira tenant.
4. Your remote service then persists the Jira installation information in its data store. See [Recommended schema for jiraInstallations table](#recommended-schema-for-jirainstallations-table) for recommended properties to store.
   ![Installation flow diagram](https://dac-static.atlassian.com/platform/forge/images/remote-agents/installation-flow.png?_v=1.5800.2167)
5. Your agent may also initiate a post-installation configuration flow that the administrator will be directed to after installing your agent. Most remote agents will need to implement this in order to map the customer's tenant in the remote service to their tenant in Jira. This flow is covered in the [Agent configuration](#3--agent-configuration) section below.

After configuration is complete, your agent is ready to [handle tasks](#2--handling-jira-tasks).

## Handling upgrades

If you evolve your agent with new capabilities in the future that require additional scopes, you will also receive [upgrade events](/platform/forge/events-reference/life-cycle/#upgrade) as customers upgrade their installations to new versions that you have released.

## Uninstallation

Forge supports a [`preUninstall` trigger module](/platform/forge/events-reference/life-cycle/#pre-uninstallation) that fires when an uninstall action is initiated via the UI or CLI. You can use this to clean up any state your remote service holds for the Jira installation — for example, deleting the installation record from your `jiraInstallations` table.

The pre-uninstall invocation has a timeout of 55 seconds, during which the uninstallation process is paused. Your cleanup logic must complete within that window — once uninstallation completes, Jira API calls from the app may no longer work.

## 2. Handling Jira tasks

**A note on the Agent2Agent protocol**

Jira's Remote Agent task handling uses concepts from the [A2A (Agent2Agent) protocol](https://a2a-protocol.org/latest/). If you're familiar with this protocol or have already implemented A2A it will speed up development of a Remote Agent. However you *do not* need a full A2A implementation in order to integrate a Remote Agent with Jira.

Once your remote agent has been installed, users can begin delegating tasks to it from Jira. Interactions between Jira and your agent happen via [JSON-RPC](https://www.jsonrpc.org/specification). In a typical agent interaction, Jira will make two types of requests to your agent:

1. `message` requests, indicating either:
   * a user has asked your agent to perform a new task; or
   * a user has provided some additional context about an existing task
2. `task` requests, used to fetch updates from your agent about specific tasks

Schemas and examples for these methods are provided in the [JSON RPC Method Reference](#json-rpc-method-reference).

It is the agent's responsibility to keep track of tasks they have been asked to perform, and share the current state of these tasks when requested by Jira. If needed, your agent may also fetch additional context or work items using the Jira REST API, as described in [Authenticating requests from your agent to the Jira REST API](#authenticating-requests-from-your-agent-to-the-jira-rest-api).

## Polling for task updates

All message and task passing is handled by Jira invoking the remote agent over JSON RPC:

* Jira will send your agent a `message` whenever a user invokes your agent
* Jira will poll the `task` endpoint for updates to any task that is currently in an "active" status (`submitted`, `working`, `input-required`, `auth-required`, or `unknown`)

There is currently no mechanism for the remote agent to "push" updates to Jira. We may implement support for SSE or push notifications in the future.

## Task privacy

Conversations between users and agents (including any additional input from the user or status updates on tasks) are kept private to the user, and not automatically replicated on to the work item. Once a task is complete, the user has the option of sharing the outcome of the task via a comment on the work item.

## Task lifecycle

During its lifecycle, a `task` will start in the `submitted` state and then transition through a number of states until it reaches a terminal state (`rejected`, `completed`, `canceled`, or `failed`).

![Task lifecycle state diagram](https://dac-static.atlassian.com/platform/forge/images/remote-agents/task-lifecycle.png?_v=1.5800.2167)

The directional arrows on the diagram are important. Once a task has entered a terminal state — `rejected`, `completed`, `canceled`, or `failed` — it **can not be restarted**. Subsequent messages from the user for the same context should be handled by creating a new task. See the ["single active task per context" rule](#the-single-active-task-per-context-rule) for more details.

The supported task states are:

| State | Type | Description |
| --- | --- | --- |
| `submitted` | active | The task has been submitted and is awaiting execution. |
| `rejected` | terminated | The task was rejected by the agent and was not started. |
| `working` | active | The agent is actively working on the task. |
| `input-required` | active | The task is paused and waiting for input from the user. |
| `auth-required` | active | The agent requires the user to authenticate with a service in order to proceed with the task. |
| `completed` | terminated | The task has been successfully completed. |
| `canceled` | terminated | The task has been canceled by the user. |
| `failed` | terminated | The task failed due to an error during execution. |
| `unknown` | active\* | The task is in an unknown or indeterminate state. This state is supported for compatibility with the A2A protocol but generally results in a poor user experience, so should be avoided where possible. Jira will initially continue to poll tasks in the `unknown` state, but will eventually assume that it has failed. |

Jira will periodically poll the remote agent for updates on any `task` currently in an **active** state (except for `input-required`, which indicates the agent is waiting for user input). The agent must respond to these requests with a `task` object containing a `state` from the table above, and an explanatory `message` which will be displayed to the user in Jira.

## Agent contexts

An agent "context" is a series of messages and tasks between user and agent, triggered by assigning or @mentioning the agent. Each context corresponds to a single Rovo "chat" session where users will provide follow-up context to the agent, and will typically map on to the concept of an agent "conversation" or "session" in the agent's own domain model.

There are a few rules that govern agent context and task lifecycle in Jira:

* Whenever a user assigns a work item to a remote agent, or @mentions the agent in a comment, Jira will send the agent a `message` without a `contextId`. It is the agent's responsibility to create and return a new `contextId` attached to the `message` and/or `task` objects sent in the response.
* Jira will then pass back the same `contextId` in any follow-up messages from the user providing more context on this task.
* If a user assigns or @mentions the remote agent on the same work item *again*, Jira will again send your agent a message without a `contextId`. Your agent should create a new `contextId` and `task` to represent this request, and continue working on them in parallel. If your agent has a concept of a "chat session", these should (ideally) be modeled as separate sessions relating to the same work item.
* However, if a user sends a new message to the remote agent in an ongoing chat session with that agent, Jira will send your agent a new `message` with the `contextId` corresponding to that chat. Your agent should update an existing active task or create a new task within the same context when this happens. See the ["single active task per context" rule](#the-single-active-task-per-context-rule).
* Contexts are **always** private to a single user and agent. Messages from different users about the same work item should each have a separate context.

![Cardinality of remote agent task-related objects](https://dac-static.atlassian.com/platform/forge/images/remote-agents/context-cardinality.png?_v=1.5800.2167)

*Cardinality of remote agent task-related objects.*

## The "single active task per context" rule

Each agent can potentially have multiple contexts for the same user on the same work item. However, each context must have only a single active `task` at a time. Specifically:

* An agent must only ever have a single `task` in an active status for a given context, and must only return a single `task` in response to a `message`. Returning multiple tasks in response to a `message` will result in undefined behaviour.
* Therefore if your agent receives a new `message` in relation to a `task` it is already working on, it should attempt to incorporate that `message` into the context it is using to process the task (if possible).
* Your agent may have multiple active tasks for the same user and work item, provided they are in different contexts.

![A context may have multiple tasks, but only the newest may be in an active state](https://dac-static.atlassian.com/platform/forge/images/remote-agents/single-active-task.png?_v=1.5800.2167)

*A context may have multiple tasks, but only the newest may be in an active state.*

## Assignment flow

A typical assignment flow has up to four stages:

1. **Initial assignment:** A user assigns a work item to an agent for the first time. This results in a `message` being sent to the remote agent using the [SendMessage](#sendmessage) method. The message contains a `text` part informing the agent that they have been assigned to a work item, and a `data` part containing context information about the work item. Your agent must immediately create a new `task` in response, and a new `contextId` to associate with it.
2. **Task execution:** The agent then works on the task until it reaches a [terminal state](#task-lifecycle). During this time, Jira will poll the agent for status updates on the task using the [GetTask](#gettask) method. When polled, the agent should return the current `status` of the task, including an explanatory `message` that will be displayed to the user. If your agent needs more information, it can enter the `input-required` state with a message prompting the user to provide more context via chat.
3. **Task completion:** Once the task is complete, the agent should return a `task` object in the `completed` state on the next poll from Jira, with an accompanying `message` object describing the outcome of the task. This message will then be presented to the user, with the option to draft a comment sharing the outcome of the task on the work item.
4. **Follow-up:** The agent will remain assigned to the work item after the initial task has been completed. If the user @mentions or reassigns the agent to the same work item again, Jira will send a new `message` object to the agent with no `contextId`. The agent must create and return a new task in a [new context](#agent-contexts) representing this request.

The following diagrams show the user experience and flow for a typical assignment interaction:

## Initial assignment

![Assignment flow diagram](https://dac-static.atlassian.com/platform/forge/images/remote-agents/assign-flow.png?_v=1.5800.2167)

![User assigns remote agent to work item](https://dac-static.atlassian.com/platform/forge/images/remote-agents/assign-1.png?_v=1.5800.2167)

*User assigns remote agent to work item*

![Agent's task status displayed in the Jira UI](https://dac-static.atlassian.com/platform/forge/images/remote-agents/assign-2.png?_v=1.5800.2167)

*Agent's task status displayed in the Jira UI*

## Task execution

![Task execution flow diagram](https://dac-static.atlassian.com/platform/forge/images/remote-agents/exec-flow.png?_v=1.5800.2167)

![Agent requests input from user](https://dac-static.atlassian.com/platform/forge/images/remote-agents/exec-1.png?_v=1.5800.2167)

*Agent requests input from user*

![User selects "Refine in Chat" and provides further input to the Agent](https://dac-static.atlassian.com/platform/forge/images/remote-agents/exec-2.png?_v=1.5800.2167)

*User selects "Refine in Chat" and provides further input to the Agent*

## Task completion

![Task completion flow diagram](https://dac-static.atlassian.com/platform/forge/images/remote-agents/complete-flow.png?_v=1.5800.2167)

![Agent returns task in "completed" status with prompt to draft a comment](https://dac-static.atlassian.com/platform/forge/images/remote-agents/complete-1.png?_v=1.5800.2167)

*Agent returns task in "completed" status — final task message is displayed in the Jira UI with prompt to draft a comment*

![User selects "Draft comment" and modifies content to their tastes](https://dac-static.atlassian.com/platform/forge/images/remote-agents/complete-2.png?_v=1.5800.2167)

*User selects "Draft comment" and modifies content to their tastes*

![User posts comment on work item](https://dac-static.atlassian.com/platform/forge/images/remote-agents/complete-3.png?_v=1.5800.2167)

*User posts comment on work item*

After the task has reached a terminal state, Jira will cease polling for new updates for that task.

A task cannot be restarted after it reaches a terminal state. If the user reassigns the agent to the work item at a future date (or @mentions the agent again on a work item that the agent has already created a task for) a new `message` will be sent to the agent without a `contextId`.

## @mention flow

The @mention flow is almost identical to the [assignment flow](#assignment-flow) described above, with the exception that the initial `message` sent to the remote agent is slightly different:

* the `text` part will indicate that the agent has been @mentioned in a comment by a user
* the `data` part will contain the id and body (in markdown) of the comment

There are two other important things to note:

* a user @mentioning your agent in a comment will *not* automatically assign the work item to your agent
* each comment @mentioning your agent will result in a separate context being created

## Chat flow

We are also considering implementing support for users to initiate a chat session with your agent outside of a work item context. Stay tuned for updates!

## Retrying tasks

If a task terminates in the `rejected`, `canceled`, or `failed` state, the user will be able to ask the agent to retry the task via chat. In the near future, we will also support a "Retry" button in the agent panel to retry the task.

In both situations, your agent will be sent a new `message` object with the same `contextId` as the terminated task. Your agent must create and return a new `task` object in response to this request: you **must not** re-use the existing `task`.

## Task cancellation

A user may also request cancellation of a `task` that is currently in a non-terminal state. Jira will send a cancellation request to your remote service using [CancelTask](#canceltask). Your agent should attempt to cancel the task if possible, or return an error if the task is not in a cancellable state.

If a task is successfully canceled, Jira will stop polling for updates for that task. If a user attempts to retry the task, you must create a new task object (with a new `taskId`) to track this work — the canceled task must not be re-used.

## Fetching additional context via REST

In addition to prompting the user, remote agents can also fetch additional context using the method described in [Authenticating requests from your agent to the Jira REST API](#authenticating-requests-from-your-agent-to-the-jira-rest-api). You may wish to fetch additional context such as attachments, additional work item fields, or linked work items.

You must authenticate *as* the user (i.e. using the `appUserToken` passed to your agent in the `x-forge-oauth-user` header) when requesting additional context in this manner. This ensures your agent only considers data that the user has access to when working on the work item. See [Authorization & tenancy considerations](#authorization--tenancy-considerations) for details on safely handling this data.

## Streaming (optional)

By default, Jira uses polling to receive task updates from your agent — Jira periodically calls your agent's `GetTask` endpoint to check on progress. This works well for most use cases, but if your agent produces incremental output (for example, streaming text as it generates a response), you can opt in to **streaming** using [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events). This allows Jira to display real-time progress to the user as your agent works.

Implementing streaming is optional. Agents that do not implement it will continue to work via polling.

### Declaring streaming support in your Forge manifest

To advertise streaming support, add `streaming: true` to your `agent2Agent` protocol block in the Forge manifest (see the [`rovo:agentConnector` module reference](/platform/forge/manifest-reference/modules/rovo-agent-connector/) for the full manifest schema):

```
```
1
2
```



```
protocols:
  agent2Agent:
    jsonRpcTransport:
      endpoint: a2a-json-rpc-endpoint
      streaming: true
```
```

Once declared, Jira will send `SendStreamingMessage` requests to your agent instead of `SendMessage` requests, and will expect your agent to respond with an SSE stream.

### Implementing `SendStreamingMessage`

The `SendStreamingMessage` method uses the same request body shape as [`SendMessage`](#sendmessage). The difference is in the response: instead of returning a single JSON object, your agent must respond with an SSE stream.

Your agent must respond with:

* HTTP status `200 OK`
* `Content-Type: text/event-stream`
* An open HTTP connection that streams events as they occur

Each event in the stream must be formatted as a standard SSE `data:` field containing a JSON-RPC 2.0 response object. The `result` field of each response must be a `StreamResponse` object containing **exactly one** of:

| Field | Type | Description |
| --- | --- | --- |
| `task` | `Task` | The initial task object, returned as the first event in the stream |
| `statusUpdate` | `TaskStatusUpdateEvent` | A status change for the task (e.g. `working` → `completed`) |
| `artifactUpdate` | `TaskArtifactUpdateEvent` | An incremental chunk of an artifact being generated by the agent |
| `message` | `Message` | A direct message response (for simple interactions that don't require task tracking) |

**Stream lifecycle:**

1. The first event in the stream must be either a `Task` object (for work that will be tracked as a task) or a `Message` object (for simple one-shot responses).
2. If a `Task` is returned first, subsequent events may be `TaskStatusUpdateEvent` or `TaskArtifactUpdateEvent` objects as the agent progresses.
3. The stream must close when the task reaches a terminal state (`completed`, `failed`, `canceled`, or `rejected`), or when a `Message` is returned.

Example SSE stream for a task that completes successfully:

```
```
1
2
```



```
data: {
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "task": {
      "id": "task-123",
      "contextId": "ctx-456",
      "status": { "state": "working" },
      "kind": "task"
    }
  }
}

data: {
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "statusUpdate": {
      "taskId": "task-123",
      "contextId": "ctx-456",
      "status": { "state": "working" },
      "message": {
        "role": "agent",
        "parts": [{ "kind": "text", "text": "Analysing the issue..." }]
      },
      "kind": "status-update",
      "final": false
    }
  }
}

data: {
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "statusUpdate": {
      "taskId": "task-123",
      "contextId": "ctx-456",
      "status": { "state": "completed" },
      "message": {
        "role": "agent",
        "parts": [{ "kind": "text", "text": "Done! I've drafted a fix." }]
      },
      "kind": "status-update",
      "final": true
    }
  }
}
```
```

### Resubscribing to a stream

If Jira's connection to your agent drops while a task is still in progress, Jira may attempt to resubscribe using the `SubscribeToTask` method (see [SubscribeToTask](#subscribetotask) in the appendices). Your agent should respond with the current task state as the first event, followed by any subsequent updates.

### Authentication for streaming requests

Streaming requests are authenticated in the same way as non-streaming requests — Jira will include a Forge Invocation Token (FIT) in the `Authorization` header when opening the SSE connection. See [Authenticating requests from Jira to your agent](#authenticating-requests-from-jira-to-your-agent).

## Authorization & tenancy considerations

Aligning the context passed to your agent with Jira's permissions and tenancy model is **critical** for ensuring customer data is safeguarded. Please read this section carefully and ensure your remote agent conforms to these requirements.

You must ensure that your agent *only* reasons about data that the user who assigned them to a work item has access to. This ensures that a user cannot escalate their own permissions when working with your agent.

**Recommended method**

The simplest and most reliable way to implement this is to ensure that **both** of the following are true:

* your agent does not retain memory or otherwise share state across contexts; **and**
* additional context is *only* fetched by the following methods:
  * soliciting further context from the assigning user by using the `input-required` state; and/or
  * fetching data from the REST API by [authenticating as the user](#authenticating-requests-from-your-agent-to-the-jira-rest-api)

**Advanced method**

If your agent must retain memory or otherwise cache customer data across contexts, you must ensure your agent's context scheme **respects individual user permissions**. Specifically:

* agent memory **must** be specific to the context user — it is not safe to have shared memory for a Jira tenant / installation
* you **must not** pass data to an agent working on a task without first checking that the assigning user has permission to view that data

Correct authorization logic in external systems that handle customer data is a strict [Atlassian cloud security requirement](https://developer.atlassian.com/platform/marketplace/security-requirements/#forge-apps-that-egress-data). Failure to implement this correctly may result in a security incident, and your app being delisted from the Atlassian Marketplace.

## 3. Agent configuration

Forge apps can surface various configuration experiences within Jira. These can be used to perform post-installation configuration steps required before the agent can action tasks, and also allow administrators or end-users to customise agent behaviour when working within certain contexts.

Configuration experiences in Jira are implemented as UI modules using one of Forge's [UI technologies](/platform/forge/user-interface/). We recommend using [UI Kit](/platform/forge/user-interface/#build-with-ui-kit) for most agent configuration experiences.

## Mapping tenants

Most remote agents will need to implement a post-installation configuration flow in order to map the customer's Jira tenant to the customer's tenant in the remote service. For example, a customer named "Acme" will need to be able to associate their Jira site `acme.atlassian.net` with the "Acme" organisation registered in your remote service. The installation trigger webhook will identify which Jira site your agent has been installed into, but this will typically not be sufficient to uniquely identify the customer in your domain model.

A tenant mapping experience is typically implemented as an [admin page](/platform/forge/manifest-reference/modules/jira-admin-page/) where Jira administrators can configure your agent. To automatically drop the user into your configuration experience after app installation, set the [`useAsConfig`](/platform/forge/manifest-reference/modules/jira-admin-page/#configure-page) property on your admin page module to `true`.

A typical tenant mapping flow works as follows:

1. After app installation, the Jira administrator is redirected to the admin page registered by your Forge app.
2. The admin page uses the [`invokeRemote()`](/platform/forge/apis-reference/ui-api-bridge/invokeRemote/) bridge method to make a request (signed with a Forge Invocation Token) to your remote service, passing a signed `installationId` in the request body.
3. Your remote service then:
   1. authenticates the user's session
   2. looks up the `jiraInstallation` using the provided `installationId`
   3. confirms with the user whether to bind their tenant in your remote service to the specified Jira site
   4. stores the mapping between the customer's Jira site and their tenant in your domain model

You must [sign the installationId](#signing-parameters-for-tenant-or-account-mapping) passed during the tenant mapping redirect to prevent the user from tampering with the value.

Note that users will be able to interact with your agent as soon as it has been installed — possibly even before an administrator has completed the post-installation configuration step. If your agent receives a message from a Jira tenant that has not yet been configured, it should respond with a task in the `auth-required` state, with a message directing the user to ask an admin to complete the configuration. See [JSON RPC Method Reference](#json-rpc-method-reference) for details on the `auth-required` state.

## Mapping accounts

Additionally, some agents may need to map individual user accounts from Jira to the account domain model in their remote service. This is typically required if your agent is required to act on behalf of a given user, as opposed to an agent acting independently on behalf of an organisation.

Account mapping flows can be implemented in a similar manner to [tenant mapping](#mapping-tenants), but the flow is initiated from a [Jira personal settings page module](/platform/forge/manifest-reference/modules/jira-personal-settings-page/) instead of an admin page module, so that each end-user can map their own account.

Similar to tenant mapping, you must [sign the accountId](#signing-parameters-for-tenant-or-account-mapping) passed during account mapping to prevent tampering.

If your agent requires a user to map their accounts before executing a task, you should set the task status to `auth-required` with a message directing the user to the personal settings page registered by your app. See [Generating a link to a settings page](#generating-a-link-to-a-settings-page) for details on generating a link to this page to provide to the user.

## Storing other configuration information

Your admin and personal settings pages may also allow users to configure other settings for tuning agent behaviour. You can use the [`invokeRemote()` bridge method](/platform/forge/apis-reference/ui-api-bridge/invokeRemote/) to send these settings to your remote service using a request securely signed with a FIT.

## 4. Technical appendices

## Forge manifest reference

Example Forge `manifest.yml` for a remote agent. See the [`rovo:agentConnector` module reference](/platform/forge/manifest-reference/modules/rovo-agent-connector/) and the [Manifest reference](/platform/forge/manifest-reference/) for full details.

```
```
1
2
```



```
app:
  id: 324888fb-c374-44d3-aff5-2daa24721084
  name: your-awesome-app

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

  trigger:
    - key: installed-trigger
      endpoint: installed-endpoint
      events:
        - avi:forge:installed:app

  jira:adminPage:
    - key: configuration-page
      resource: config-page
      title: Awesome Agent Configuration
      render: native
      resolver:
        endpoint: config-endpoint
      useAsConfig: true

  endpoint:
    - key: a2a-json-rpc-endpoint
      remote: agent-remote
      route: /a2a/json-rpc
    - key: installed-endpoint
      remote: agent-remote
      route: /atlassian/installed
    - key: config-endpoint
      remote: agent-remote
      route: /atlassian/config

remotes:
  - key: agent-remote
    baseUrl: https://youragent.com
    operations:
      - compute
      - storage
    auth:
      appSystemToken:
        enabled: true
      appUserToken:
        enabled: true

resources:
  - key: agent-resources
    path: static/agent

permissions:
  scopes:
    - read:app-system-token
    - read:app-user-token
    - read:jira-work
```
```

## Installation trigger event reference

| Property | Description |
| --- | --- |
| `app` | Metadata about the Forge app being installed |
| `app.id` | The Forge app's ID (a UUID) |
| `app.name` | The Forge app's name |
| `app.ownerAccountId` | ID of the Atlassian Account who created the Forge app |
| `app.version` | The Forge app version |
| `context` | An **Atlassian Resource Identifier** (ARI) identifying the site that the app has been installed into. The format is: `ari:cloud:jira::site/${cloudId}`. The cloud ID is a permanent identifier for the site that will not change under normal circumstances. |
| `environment` | Metadata about the Forge app [environment](/platform/forge/environments-and-versions/) being installed |
| `environment.id` | The environment's ID (a UUID) |
| `eventType` | The name of the event. A single trigger module can consume multiple [events](/platform/forge/events-reference/), if desired. |
| `id` | The ID of the installation record for the app into this site (a UUID). This is referred to as an `installationId` in some other contexts. The installation ID will cycle if the app is uninstalled and then reinstalled. |
| `installerAccountId` | Atlassian Account ID of the user who is installing the Forge app |

Example:

```
```
1
2
```



```
{
  "app": {
    "id": "b9c0e1ec-3d22-4560-a650-34ff4155692c",
    "name": "agent-forge-app",
    "ownerAccountId": "557058:6ea56496-8c9b-4e0a-bc03-7412dedb3304",
    "version": "5.2.0"
  },
  "context": "ari:cloud:jira::site/02cfe711-47c9-46f3-ae22-9af9259c75be", // "cloudId" of Jira site being installed into
  "environment": {
    "id": "f11e5c8c-4f17-4547-b236-dc0ffbfff13b" // ID of Forge app environment being installed
  },
  "eventType": "avi:forge:installed:app", // event name
  "id": "4e874af6-799e-4236-b172-23e57f9e549e", // "installationId" of the installation record for your app into this site
  "installerAccountId": "557058:6ea56496-8c9b-4e0a-bc03-7412dedb3304" // account ID of the user installing the app
}
```
```

## Recommended schema for `jiraInstallations` table

Though not shown in the table below, you will likely also need to store a mapping from the Jira installation to a "tenant" in your own tenancy model.

| Name | Type | Description |
| --- | --- | --- |
| `cloudId` | string | The unique identifier of the Jira site, needed to make API requests to Jira. This is the **context** property from the installation webhook payload. |
| `installationId` | string | The unique identifier for the installation record of your app into this Jira site. If your app is uninstalled and then reinstalled, a new installationId is generated. This is the **id** property from the installation webhook payload. |
| `installerAccountId` | string | The Atlassian account ID of the user who installed your app. Storing this is optional, but may be useful for audit purposes. This is the **installerAccountId** property from the installation webhook payload. |
| `baseUrl` | string | The base URL of the Jira site (e.g. `my-site.atlassian.net`). Storing this is optional, but is useful for rendering links and displaying a human-recognisable name for the site. This is **not included** in the installation payload, but can be fetched after installation using the method described in [Fetching the Jira base URL](#fetching-the-jira-base-url). |

## Fetching the Jira base URL

You can fetch the base URL of a Jira site by calling the [Server info](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-server-info/#api-rest-api-3-serverinfo-get) API, which does not require authentication. You can call the REST API of a Jira site by passing the site's `cloudId` to Atlassian's API gateway:

```
```
1
2
```



```
https://api.atlassian.com/ex/jira/${cloudId}/rest/api/3/serverInfo
```
```

The API will return a set of metadata about the Jira site. The site's base URL is included in the `baseUrl` property.

You can also retrieve a Jira site's `cloudId` by accessing the following resource:

```
```
1
2
```



```
https://${subdomain}.atlassian.net/_edge/tenant_info
```
```

## Signing parameters for tenant or account mapping

When performing a browser redirect between a Jira configuration screen and a companion configuration screen in your remote service for the purposes of tenant or account mapping, you will often need to pass one or more identifiers in the query string or body of the request. If left unprotected, a malicious end-user may tamper with these identifiers to forge illegitimate mappings to other customers' accounts.

To prevent this from happening, we **strongly recommend** *signing* or *encrypting* these parameters to ensure they have not been tampered with.

One way to achieve this is to embed secure parameters (e.g. `installationId` or `accountId`) in a [JSON Web Token](https://auth0.com/docs/secure/tokens/json-web-tokens), then sign it with an HMAC generated using a secret shared between your Forge app and your remote service. The most common way to maintain a shared secret in Forge is to use an [encrypted environment variable](/platform/forge/cli-reference/variables-set/).

## Generating a link to a settings page

Jira page modules are accessible via special paths served within the customer's Jira site.

You can construct a link to a specific configuration page by inserting the relevant identifiers into one of the schemas described below:

| Module | Schema |
| --- | --- |
| `jira:adminPage` with `useAsConfig: true` | `{baseUrl}/jira/settings/apps/configure/{appId}/{envId}` |
| `jira:adminPage` without `useAsConfig` | `{baseUrl}/jira/settings/apps/{appId}/{envId}` |
| `jira:personalSettingsPage` | `{baseUrl}/jira/settings/personal/apps/{appId}/{envId}` |
| `jira:projectSettingsPage` | `{baseUrl}/jira/x/projects/{projectKey}/settings/apps/{appId}/{envId}` |

Where:

* `baseUrl` — base URL of the Jira site, e.g. `https://example.atlassian.net`
* `appId` — the UUID portion of your Forge app ID. For example, if the `id` property of your `app` in your manifest is `ari:cloud:ecosystem::app/cfff4a94-a7db-4c31-b842-292d00df6cce`, the `appId` in the URL should be `cfff4a94-a7db-4c31-b842-292d00df6cce`
* `envId` — ID of the Forge app [environment](/platform/forge/environments-and-versions/) installed into the site
* `projectKey` — the key of the Jira project being configured

## Authenticating requests from Jira to your agent

Requests to your agent from Jira will have a Forge Invocation Token (FIT) passed in the `Authorization` header. Your remote agent **must verify the FIT on all incoming requests** using JWKS, as described in [Verifying remote requests](/platform/forge/remote/essentials/#verifying-remote-requests).

## Authenticating requests from your agent to the Jira REST API

If your agent needs to make requests back to Jira's REST API, you can request for access tokens to be sent to your remote service by setting the `auth.appSystemToken.enabled` and/or the `auth.appUserToken.enabled` property on the [remote entry in your manifest](/platform/forge/manifest-reference/remotes/#remotes).

If set, every request from Jira to your agent will contain one or both of the following headers:

| Manifest property | Header | Value | When is it sent? |
| --- | --- | --- | --- |
| `remotes.auth.appSystemToken.enabled: true` | `x-forge-oauth-system` | An access token that can be used to authenticate as your app's dedicated system user. Requests made using this token will be attributed to "App Name" in audit logs and the UI. | All requests to your remote service |
| `remotes.auth.appUserToken.enabled: true` | `x-forge-oauth-user` | An access token that can be used to authenticate as the user who interacted with your agent from Jira. Requests made using this token will be attributed to the user in audit logs and the UI. | `message` and `task` requests |

Your agent can then make requests to Jira's APIs using these tokens as described in [Calling Atlassian app APIs from a remote](/platform/forge/remote/calling-product-apis/).

Both app user and app system tokens currently have a [4 hour TTL](https://developer.atlassian.com/changelog/#CHANGE-2160).

## Which token should I use?

If your app is accessing resources on behalf of the user (such as fetching additional context for processing a task), you should use the `appUserToken` when making requests, as it will respect the user's configured permissions in Jira. The app's system user *may* have access to resources that the end user does not, so requesting resources using the `appSystemToken` may result in privilege escalation.

You should typically only make requests with the `appSystemToken` if you are:

* fetching configuration information after installation (such as field names or work item schemes)
* creating, updating, or deleting a domain object in Jira and you wish for this action to be attributed to your app user rather than a real user

See [Authorization & tenancy considerations](#authorization--tenancy-considerations) for more details.

## Scopes

The tokens described above are bound by the [scopes defined in your Forge manifest](/platform/forge/manifest-reference/permissions/#scopes), so you will need to add any scopes required by the APIs you intend to call. Customers will be presented with these scopes and will need to consent to their use when they install your app.

Each time you add new scopes to your app's manifest, you will need to redeploy your app. Your customer will then need to upgrade their app installation and consent to the new scopes before you will be able to make requests to the corresponding APIs. Your remote service will receive an [upgrade event](#handling-upgrades) for each customer that has upgraded. If your agent cannot process a given task until the user has upgraded, it should respond with a task in the `auth-required` state.

## JSON RPC method reference

The following method schemas and conventions are based on a subset of the [A2A specification](https://a2a-protocol.org/latest/specification/). Only the properties used in the schemas and examples below are currently used by Jira.

Your remote service must implement the following JSON RPC methods, accessible at the endpoint specified by the `jsonRpcTransport` property in your Forge manifest.

All messages and rich text fields are formatted in markdown.

## `SendMessage`

Jira will call the `SendMessage` method when:

* a user creates a new context (by @mentioning or assigning your agent on a work item)
* a user sends a message in the Rovo chat panel attached to an existing context (e.g. when providing more information in response to an `input-required` task status)

### Initial message schema

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": $requestId,
  "method": "message/send",
  "params": {
    "message": {
      "kind": "message",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": $message
        }, {
          "kind": "data",
          "data": $data
        }
      ],
      "messageId": $messageId
    }
  }
}
```
```

### Agent assigned to work item — example

**Request:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "03fbd406-dc47-472d-9c5c-03b6f2716fce",
  "method": "message/send",
  "params": {
    "message": {
      "kind": "message",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "A user has assigned you to a work item."
        }, {
          "kind": "data",
          "data": {
            "userAccountId": "22222",
            "agentAccountId": "11111",
            "issue": {
              "id": "21930",
              "fields": {
                "summary": "QA checkout flow updates",
                "description": "Perform a comprehensive QA review..."
              }
            }
          }
        }
      ],
      "messageId": "a198b5e2-342b-4159-b9e0-c063ba627a4c"
    }
  }
}
```
```

**Response:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "03fbd406-dc47-472d-9c5c-03b6f2716fce",
  "result": {
    "id": "909aef32-059d-46d7-ade3-38fa4d2c5162",
    "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
    "status": {
      "state": "working",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [{
          "kind": "text",
          "text": "Cursor is reviewing AW26-11."
        }],
        "messageId": "0fca37e8-80c3-43d3-bcf5-cb4be26f4df8",
        "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162",
        "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c"
      },
      "timestamp": "2025-01-01T12:00:00Z"
    },
    "kind": "task"
  }
}
```
```

**Request:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "03fbd406-dc47-472d-9c5c-03b6f2716fce",
  "method": "message/send",
  "params": {
    "message": {
      "kind": "message",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "A user has mentioned you in a comment."
        }, {
          "kind": "data",
          "data": {
            "userAccountId": "22222",
            "agentAccountId": "11111",
            "issue": {
              "id": "21930",
              "fields": {
                "summary": "QA checkout flow updates",
                "description": "Perform a comprehensive QA review..."
              }
            },
            "comment": {
              "id": "91283",
              "body": "QA is showing that when a customer enters a valid discount code at checkout, it's not being reflected in the order summary or total. [@Cursor](~11111) can you analyze and suggest a fix?"
            }
          }
        }
      ],
      "messageId": "a198b5e2-342b-4159-b9e0-c063ba627a4c"
    }
  }
}
```
```

**Response:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "03fbd406-dc47-472d-9c5c-03b6f2716fce",
  "result": {
    "id": "909aef32-059d-46d7-ade3-38fa4d2c5162",
    "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
    "status": {
      "state": "working",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [{
          "kind": "text",
          "text": "Cursor is reviewing your comment."
        }],
        "messageId": "0fca37e8-80c3-43d3-bcf5-cb4be26f4df8",
        "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162",
        "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c"
      },
      "timestamp": "2025-01-01T12:00:00Z"
    },
    "kind": "task"
  }
}
```
```

### User provides more context in response to `input-required` — example

**Request:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "2561267b-a71a-42f6-bbb1-fbcb30359b41",
  "method": "message/send",
  "params": {
    "message": {
      "kind": "message",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "A user has sent a message in the chat."
        }, {
          "kind": "data",
          "data": {
            "userAccountId": "22222",
            "agentAccountId": "11111",
            "issue": {
              "id": "21930"
            },
            "chat": {
              "message": "The test credentials are username: testuser@example.com, password: Test1234!"
            }
          }
        }
      ],
      "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
      "messageId": "d2c9e3f1-5a6b-7c8d-9e0f-1a2b3c4d5e6f"
    }
  }
}
```
```

**Response:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "2561267b-a71a-42f6-bbb1-fbcb30359b41",
  "result": {
    "id": "909aef32-059d-46d7-ade3-38fa4d2c5162",
    "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
    "status": {
      "state": "working",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [{
          "kind": "text",
          "text": "Thanks! Resuming QA review with the provided credentials."
        }],
        "messageId": "e3d4c5b6-a7b8-9c0d-1e2f-3a4b5c6d7e8f",
        "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162",
        "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c"
      },
      "timestamp": "2025-01-01T12:05:00Z"
    },
    "kind": "task"
  }
}
```
```

## `GetTask`

Jira will call `GetTask` to poll for updates on tasks that are in an active state.

### Get task schema

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": $requestId,
  "method": "tasks/get",
  "params": {
    "taskId": $taskId
  }
}
```
```

**Request:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
  "method": "tasks/get",
  "params": {
    "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162"
  }
}
```
```

**Response (task in progress):**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
  "result": {
    "id": "909aef32-059d-46d7-ade3-38fa4d2c5162",
    "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
    "status": {
      "state": "working",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [{
          "kind": "text",
          "text": "Cursor is running through the checkout flow test cases."
        }],
        "messageId": "f4e5d6c7-b8a9-0b1c-2d3e-4f5a6b7c8d9e",
        "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162",
        "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c"
      },
      "timestamp": "2025-01-01T12:10:00Z"
    },
    "kind": "task"
  }
}
```
```

**Response (task completed):**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
  "result": {
    "id": "909aef32-059d-46d7-ade3-38fa4d2c5162",
    "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
    "status": {
      "state": "completed",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [{
          "kind": "text",
          "text": "## QA Review Complete\n\nAll 12 checkout flow test cases passed. The discount code issue (AW26SAVE) has been reproduced and a root cause identified in `checkout/discountService.ts:142`. A fix has been drafted in PR #847."
        }],
        "messageId": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162",
        "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c"
      },
      "timestamp": "2025-01-01T12:30:00Z"
    },
    "kind": "task"
  }
}
```
```

## `SendStreamingMessage`

`SendStreamingMessage` is used when your agent has declared `streaming: true` in its Forge manifest. It is invoked by Jira under the same circumstances as [`SendMessage`](#sendmessage), but your agent must respond with a Server-Sent Events (SSE) stream rather than a single JSON response.

The request body is identical to `SendMessage`. See [Streaming (optional)](#streaming-optional) for full details on implementing the SSE response.

## `SubscribeToTask`

`SubscribeToTask` allows Jira to re-establish a streaming connection to an in-progress task if the original SSE connection was dropped. Your agent must respond with an SSE stream beginning with the current task state, followed by any subsequent updates.

### Subscribe to task schema

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `jsonrpc` | string | Yes | Must be `"2.0"` |
| `method` | string | Yes | Must be `"tasks/resubscribe"` |
| `id` | string or number | Yes | Request identifier |
| `params` | object | Yes |  |
| `params.id` | string | Yes | The `taskId` to resubscribe to |

Your agent must return an SSE stream (same format as `SendStreamingMessage`), starting with the current `Task` object, followed by any pending `TaskStatusUpdateEvent` or `TaskArtifactUpdateEvent` events. If the task is already in a terminal state, return the task and close the stream immediately.

## `CancelTask`

Jira will call `CancelTask` when a user presses the cancel button on the agent panel for an active task.

### Cancel task schema

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": $requestId,
  "method": "tasks/cancel",
  "params": {
    "taskId": $taskId
  }
}
```
```

**Request:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "f1a032e3-9d46-4464-a50e-70cf12ff86bd",
  "method": "tasks/cancel",
  "params": {
    "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162"
  }
}
```
```

**Response:**

```
```
1
2
```



```
{
  "jsonrpc": "2.0",
  "id": "f1a032e3-9d46-4464-a50e-70cf12ff86bd",
  "result": {
    "id": "909aef32-059d-46d7-ade3-38fa4d2c5162",
    "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c",
    "status": {
      "state": "canceled",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [{
          "kind": "text",
          "text": "Cursor canceled the task at the user's request."
        }],
        "messageId": "a199fa50-a320-4c6b-b610-ef2664c43f4e",
        "taskId": "909aef32-059d-46d7-ade3-38fa4d2c5162",
        "contextId": "4bdcf71e-0441-4564-95a3-f1c50594b60c"
      },
      "timestamp": "2025-01-01T12:00:00Z"
    },
    "kind": "task"
  }
}
```
```

## Error codes

| A2A Error Type | JSON-RPC Code | Notes |
| --- | --- | --- |
| `TaskNotFoundError` | `-32001` | Only for `GetTask` |
| `TaskNotCancelableError` | `-32002` | Only for `CancelTask` |
| `UnsupportedOperationError` | `-32004` | Only for `CancelTask` |

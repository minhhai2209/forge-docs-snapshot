# Read Jira issues with a Rovo MCP tool

Rovo MCP is available through Forge's Early Access Program (EAP). The EAP allows all Forge developers for testing and feedback. APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production use.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

This tutorial builds on [Build a Rovo MCP hello world app](/platform/forge/build-a-hello-world-rovo-mcp/).
Instead of logging a message, your tool reads real product data: it takes a Jira issue key, fetches the
issue with the Jira REST API, and returns the issue's summary and status to the agent.

At the end of this tutorial, you'll have a Forge app whose [Rovo MCP](/platform/forge/manifest-reference/modules/rovo-mcp/)
module exposes a tool that a custom agent in Rovo Studio can call to look up a Jira issue.

## Before you begin

To expose tools to Rovo, you must have [Rovo activated](https://support.atlassian.com/organization-administration/docs/activate-or-deactivate-rovo-on-your-site/).

Complete [Getting started](/platform/forge/getting-started/) before working through
this tutorial.

Install `@forge/cli` version `13.3.0` or higher.

To install:

`npm install -g @forge/cli@latest` or

`npm install -g @forge/cli@^13.3.0`

You also need a Jira site with at least one issue to read, and its issue key, for example *PROJ-123*.

## Create your app

1. Create your app by running:
2. Enter a name for your app. For example *rovo-mcp-issue-reader*.
3. Select the *Show All* category.
4. Select the *blank* template.
5. Change to the app subdirectory to see the app files.

   ```
   ```
   1
   2
   ```



   ```
   cd rovo-mcp-issue-reader
   ```
   ```
6. Add the `rovo:mcp` module to your app by running:
7. Select the *Rovo* product.
8. Select the `rovo:mcp` module.
9. Follow the prompts to enter a module key and MCP name. These can be updated later. This tutorial
   uses the module key *issue-reader-mcp* and the MCP name *Issue reader MCP*.

`forge module add` adds a `rovo:mcp` module with a default `Log a message` action, and creates a starter
function file named after your module key (`src/issue-reader-mcp.js`). The next steps replace that default
action with one that reads a Jira issue.

The `src/index.js` file and the `my-function` module are left over from the blank template and aren't used
by the MCP module. The next steps remove them.

To read a Jira issue, your function calls the Jira REST API. Install the `@forge/api` package, which
provides the product REST API clients:

```
```
1
2
```



```
npm install @forge/api
```
```

### manifest.yml

Open your `manifest.yml` file and update it to match the following. This defines a single `get-issue`
tool with an `issueKey` input, and adds the `read:jira-work` scope so your app can read Jira issues.
Remember to keep your own app ID.

For a detailed understanding of the manifest structure, refer to the
[Rovo MCP module](/platform/forge/manifest-reference/modules/rovo-mcp/#manifest-structure).

```
```
1
2
```



```
modules:
  rovo:mcp:
    - key: issue-reader-mcp
      name: Issue reader MCP
      tools:
        - get-issue
  action:
    - key: get-issue
      name: Get a Jira issue
      function: resolver
      actionVerb: GET
      description: >
        Fetches a Jira issue's summary and status by its issue key.
      inputs:
        issueKey:
          title: Issue key
          type: string
          required: true
          description: The Jira issue key, for example PROJ-123.
  function:
    - key: resolver
      handler: issue-reader-mcp.getIssue
permissions:
  scopes:
    - read:jira-work
app:
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64
  id: <your app id>
```
```

`actionVerb: GET` marks this action as read-only. The `read:jira-work` scope must match the API call your
function makes; if you later call a write API, add the matching write scope and reinstall your app.

### src/issue-reader-mcp.js

Replace the contents of `src/issue-reader-mcp.js` with the following. The `getIssue` function reads the
`issueKey` from the payload, requests the issue from Jira as the current user, and returns a short summary
string:

```
```
1
2
```



```
import api, { route } from '@forge/api';

export async function getIssue(payload) {
  const { issueKey } = payload;

  // asUser() runs the request as the person invoking the tool, so it can only
  // read issues that user is already allowed to see.
  const response = await api
    .asUser()
    .requestJira(route`/rest/api/3/issue/${issueKey}?fields=summary,status`);

  if (!response.ok) {
    return `Could not fetch issue ${issueKey} (status ${response.status}).`;
  }

  const issue = await response.json();
  const summary = issue.fields.summary;
  const status = issue.fields.status.name;

  // The return value passes back to the agent, which relays it to the user.
  return `${issueKey}: "${summary}" — status: ${status}`;
}
```
```

Using `asUser()` keeps the tool safe: it respects the invoking user's own Jira permissions, so the agent
can't read anything the user couldn't read themselves.

You can also delete the unused `src/index.js` file left over from the blank template.

## Install your app

To use your app, it must be installed onto an Atlassian site. The
`forge deploy` command builds, compiles, and deploys your code; it'll also report any compilation errors.
The `forge install` command then installs the deployed app onto an Atlassian site with the
required API access.

You must run the `forge deploy` command before `forge install` because an installation
links your deployed app to an Atlassian site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select *Jira* using the arrow keys and press the enter key.
     
   This tool reads Jira issues, so it must be installed on Jira.
4. Confirm the `read:jira-work` scope when prompted.
5. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready to use on the
specified site.

Whenever you add or change a scope, you must run `forge deploy` and then `forge install` again to apply it.

With your app installed, your tool is available to custom agents in Rovo Studio.

1. In Jira, access Rovo by selecting **Ask Rovo** on the top menu.
2. In the Rovo side panel, select the agent selector and go to **Create agent**.

   ![example of the Rovo agent selector](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-agent-selector.png?_v=1.5800.2253)
3. Select **skip to manual step** to open the agent configuration.

   ![example of the create agent configuration screen](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-create-agent.png?_v=1.5800.2253)
4. In the agent configuration, find the **Tools** section and select **Add tools**.
5. Scroll down to the **Connected apps** section, select your app, then select the **Get a Jira issue** tool exposed by your MCP module, and select **Add**.

   ![example of adding the Get a Jira issue tool exposed by your app](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-issue-reader-add-tools.png?_v=1.5800.2253)
6. Your tool now appears under the agent's **Tools** section. Give your agent a name, for example *Issue lookup agent*, then select **Publish**.

   ![example of the agent with the Get a Jira issue tool added](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-issue-reader-agent-with-tool.png?_v=1.5800.2253)
7. Use the agent selector to find and select your published agent.

   ![example of selecting your published agent](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-select-agent.png?_v=1.5800.2253)
8. Chat with the agent and invoke your tool. Ask the agent to summarize an issue, for example, *Summarize KAN-3*, using a real issue key from your site.

The agent calls your `get-issue` tool to fetch the issue's summary and status, then presents a summary. Rovo can enrich the reply with other issue details it has access to, such as the reporter and description. You should see a reply like:

```
```
1
2
```



```
The Jira issue KAN-3: "Rovo MCP test issue - issue reader tool" is a Task in the
"My Kanban Space" (KAN) project. Here is a summary of its details:

- Status: To Do
- Reporter: Chris Ganta
- Created: 30 July 2026
- Description: A test case for verifying the "Get a Jira issue" tool.
```
```

![example of the agent replying with the Jira issue summary and status](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-issue-reader-reply.png?_v=1.5800.2253)

The value your function returns is what the agent shows the user, so returning more detail makes the tool
more useful. For example, add the assignee to the response.

1. Request the `assignee` field alongside `summary` and `status`:

   ```
   ```
   1
   2
   ```



   ```
   const response = await api
     .asUser()
     .requestJira(route`/rest/api/3/issue/${issueKey}?fields=summary,status,assignee`);
   ```
   ```
2. Include the assignee in the returned string:

   ```
   ```
   1
   2
   ```



   ```
   const assignee = issue.fields.assignee?.displayName ?? 'Unassigned';
   return `${issueKey}: "${summary}" — status: ${status}, assignee: ${assignee}`;
   ```
   ```
3. Deploy your app:

   You didn't change any scopes, so you don't need to reinstall.
4. Ask the agent to look up an issue again. The reply now includes the assignee.

## Next steps

* Add more tools to the same `rovo:mcp` module to expose a small toolkit. The tool `name`, `description`,
  and `inputs` are what the agent reads to decide when to call each tool, so write them clearly.
* Use the `context` object on the payload to act on the user's current issue without asking for a key. See
  [Build a Rovo MCP hello world app](/platform/forge/build-a-hello-world-rovo-mcp/#change-the-behavior-of-your-tool).

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).

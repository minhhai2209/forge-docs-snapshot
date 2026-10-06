# Build a Rovo MCP hello world app

Rovo MCP is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

Atlassian releases preview features so partners and developers can study, test, and integrate them before General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#forge-preview).

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

This tutorial walks through creating a Forge app that adds a
[Rovo MCP](/platform/forge/manifest-reference/modules/rovo-mcp/) module.
You will also create an [action](/platform/forge/manifest-reference/modules/rovo-action/),
which the MCP module exposes as a tool that custom agents in Rovo Studio can invoke with input from
the user's chat.

At the end of this tutorial, you’ll have created a Forge app that exposes a tool that can take
a user's prompt and log a simple hello world message inside a Forge function.

## Before you begin

To expose tools to Rovo, you must have [Rovo activated](https://support.atlassian.com/organization-administration/docs/activate-or-deactivate-rovo-on-your-site/).

Complete [Getting started](/platform/forge/getting-started/) before working through
this tutorial.

Install `@forge/cli` version `13.3.0` or higher.

To install:

`npm install -g @forge/cli@latest` or

`npm install -g @forge/cli@^13.3.0`

## Create your app

1. Create your app by running:
2. Enter a name for your app. For example *hello-world-rovo-mcp*.
3. Select the *Show All* category.
4. Select the *blank* template.
5. Change to the app subdirectory to see the app files.

   ```
   ```
   1
   2
   ```



   ```
   cd hello-world-rovo-mcp
   ```
   ```
6. Add the `rovo:mcp` module to your app by running:
7. Select the *Rovo* product.
8. Select the `rovo:mcp` module.
9. Follow the prompts to enter a module key and MCP name. These can be updated later. This tutorial
   uses the module key *hello-world-mcp* and the MCP name *Hello world MCP*.

Running `forge module add` updates your `manifest.yml` and generates a starter function file for the
module. It adds a `rovo:mcp` module with a default `Log a message` action (exposed as a tool) and
creates `src/hello-world-mcp.js` with a `messageLogger` function that backs the action.

Your app now has the following structure:

```
```
1
2
3
4
5
6
```



```
├── manifest.yml
├── package.json
└── src
    ├── hello-world-mcp.js
    └── index.js
```
```

The `src/index.js` file and the `my-function` module are left over from the blank template and aren't
used by the MCP module. The next steps remove them so the app only contains what the tool needs.

### manifest.yml

Open your `manifest.yml` file and remove the leftover `my-function` entry from the `function` list so
your manifest matches the following (your app ID is already filled in):

For a detailed understanding of the manifest structure, refer to the
[Rovo MCP module](/platform/forge/manifest-reference/modules/rovo-mcp/#manifest-structure).

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
```



```
modules:
  rovo:mcp:
    - key: hello-world-mcp
      name: Hello world MCP
      tools:
        - hello-world-mcp-logger
  action:
    - key: hello-world-mcp-logger
      name: Log a message
      function: resolver
      actionVerb: GET
      description: >
        When a user asks to log a message, this action logs the message to the
        Forge logs.
      inputs:
        message:
          title: Message
          type: string
          required: true
          description: The message that the user has requested be logged to Forge logs
  function:
    - key: resolver
      handler: hello-world-mcp.messageLogger
app:
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64
  id: <your app id>
```
```

### src/hello-world-mcp.js

`forge module add` creates `src/hello-world-mcp.js` with a starter `messageLogger` function that logs the
user-provided message to the console. The `hello-world-mcp-logger` action in the manifest invokes this
function to log messages as requested by the user.

Update the function to also return a confirmation message. An action's return value passes back to the
agent, so returning a value lets the agent confirm the result to the user:

```
```
1
2
3
4
5
```



```
export function messageLogger(payload) {
  console.log(`Logging message: ${payload.message}`);
  return `Logged message: ${payload.message}`;
}
```
```

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
3. Select *Confluence* using the arrow keys and press the enter key.
     
   This tutorial uses Confluence, but your Forge app isn't tied to a specific Atlassian app. To
   install it on Jira or another Atlassian app, select that app here instead.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

Running the `forge install` command only installs your app onto the selected site.
To install on additional sites, repeat these steps, selecting another site each time.
You must run `forge deploy` before running `forge install` in any of the Forge environments.

With your app installed, your tool is available to custom agents in Rovo Studio.

1. Access Rovo by selecting **Ask Rovo** on the top menu within the Atlassian app where you have installed your Forge app.
2. In the Rovo side panel, select the agent selector and go to **Create agent**.
   ![example of the Rovo agent selector](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-agent-selector.png?_v=1.5800.2363)
3. Select **skip to manual step** to open the agent configuration.
   ![example of the create agent configuration screen](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-create-agent.png?_v=1.5800.2363)
4. In the agent configuration, find the **Tools** section and select **Add tools**.
5. Scroll down to the **Connected apps** section, select your app, then select the **Log a message** tool exposed by your MCP module, and select **Add**.
   ![example of adding the tool exposed by your app](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-add-tools.png?_v=1.5800.2363)
6. Your tool now appears under the agent's **Tools** section. Give your agent a name, for example
   *Hello world logger agent*, then select **Publish**.
   ![example of the agent with the tool added](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-agent-with-tool.png?_v=1.5800.2363)
7. Use the agent selector to find and select your published agent.
   ![example of selecting your published agent](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-select-agent.png?_v=1.5800.2363)
8. Chat with the agent and invoke your tool. Ask the agent to log a message for you, for example,
   *Log the message "hello world"*.
     
   The agent now calls your tool, which logs the message to the Forge logs via your Forge function.
9. Check the logs to confirm your tool ran. Go to the [developer console](https://developer.atlassian.com/console/myapps/),
   select your app, and navigate to **Logs**.

You should see a Forge log with your message:

![example of your tool creating a Forge log](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-log.png?_v=1.5800.2363)

The Forge function in the `src/hello-world-mcp.js` file shapes the behavior of the tool:

```
```
1
2
3
4
5
```



```
export function messageLogger(payload) {
  console.log(`Logging message: ${payload.message}`);
  return `Logged message: ${payload.message}`;
}
```
```

1. Add a `console.log` line to inspect the payload object. Your function now looks like this:

   ```
   ```
   1
   2
   3
   4
   5
   6
   ```



   ```
   export function messageLogger(payload) {
     console.log(`Logging message: ${payload.message}`);
     console.log(`Payload: ${JSON.stringify(payload)}`);
     return `Logged message: ${payload.message}`;
   }
   ```
   ```
2. The payload returns an additional context object, which can contain identifiers relevant to
   the user’s current context. Because you installed this app on Confluence, the context includes a
   `confluence` key. If you installed on a different Atlassian app, you'd see that app's key instead
   (for example, `jira`). The following shows the structure of the `context` property on the payload:

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
   ```



   ```
   {
     "context": {
       "confluence": {
         "url": "https://mysite.atlassian.com/wiki/spaces/~61df1116125b12007152148f/pages/10092545/Mypage",
         "resourceType": "page",
         "contentId": "10092545",
         "spaceKey": "~61df1116125b12007152148f",
         "spaceId": "33248"
       },
       "cloudId": "13c6457e-69c5-4ad4-880a-dbdd77ef39f2",
       "moduleKey": "hello-world-mcp-logger"
     }
   }
   ```
   ```

   These can be useful for checking the identifiers passed in via action inputs, which the LLM
   can sometimes get wrong.
3. Now update the function to log an extra message detailing whether the user is on a Confluence page,
   blog post, or another resource type.

   Update your `messageLogger` function as follows:

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
   export function messageLogger(payload) {
     console.log(`Logging message: ${payload.message}`);
     console.log(`Payload: ${JSON.stringify(payload)}`);

     const message = `The user is on a Confluence ${payload.context?.confluence?.resourceType}`;
     console.log(message);
     return message;
   }
   ```
   ```
4. Deploy your app:
5. Test your tool again by asking the agent to log a message.
6. Check the logs to verify your tool ran. Go to the
   [developer console](https://developer.atlassian.com/console/myapps/), select your app, and navigate to **Logs**.

   You should see Forge logs with your messages.

## Connect to a third-party AI client (Preview)

You can now connect Rovo MCP tools to third-party AI clients. This capability is available under Forge's Early Access Program (EAP).
It is experimental, unsupported, not recommended for use in production environments, and subject to change without notice.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

In addition to custom agents in Rovo Studio, you can connect your tool to any third-party, MCP-compatible
AI client. The steps below show this flow using Claude Code as an example client; exact steps and
screens vary depending on the client you use.

1. External MCP exposure is disabled by default. In [Atlassian Administration](https://admin.atlassian.com/),
   go to **Apps > Sites > *your site* > Connected apps**, select your Forge app (the one with a `rovo:mcp`
   module), and open its app details. Under **Tools**, turn on the tools you want to expose to external
   clients. For full instructions, see
   [Configure tools for an external MCP server](https://support.atlassian.com/organization-administration/docs/configure-tools-for-an-external-mcp-server/).

   ![example of enabling tools for a Forge app with a rovo:mcp module in Atlassian Administration](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-3p-client-admin-toggle.png?_v=1.5800.2363)
2. Open your `manifest.yml` and copy the UUID portion of your `app.id`. That's the `<appId>` in
   `ari:cloud:ecosystem::app/<appId>`.
3. Construct your app's MCP endpoint URL: `https://mcp.atlassian.com/forge/<appId>`.
4. Add the URL as a remote MCP server in your AI client. The steps below use Claude Code;
   other clients vary, so check your client's docs.

   ```
   ```
   1
   2
   ```



   ```
   claude mcp add --transport http hello-world-mcp https://mcp.atlassian.com/forge/<appId>
   ```
   ```

   Then run `/mcp` in a Claude Code session to connect and complete OAuth.
5. When you connect, your client opens a browser window with an OAuth consent screen. Select the site
   where you installed your app, sign in with your Atlassian account, and approve access for the client.
6. Once connected, your client lists the **Log a message** tool exposed by your MCP module. Chat with
   your AI client and ask it to invoke the tool, for example, *Log the message "hello world"*.
7. Check the logs to confirm your tool ran, the same way as in [Use your Rovo MCP tool](#use-your-rovo-mcp-tool).

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).

# Build a Rovo MCP hello world app

Rovo MCP is available through Forge's Early Access Program (EAP). The EAP allows all Forge developers for testing and feedback. APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production use.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

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
   ![example of the Rovo agent selector](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-agent-selector.png?_v=1.5800.2255)
3. Select **skip to manual step** to open the agent configuration.
   ![example of the create agent configuration screen](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-create-agent.png?_v=1.5800.2255)
4. In the agent configuration, find the **Tools** section and select **Add tools**.
5. Scroll down to the **Connected apps** section, select your app, then select the **Log a message** tool exposed by your MCP module, and select **Add**.
   ![example of adding the tool exposed by your app](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-add-tools.png?_v=1.5800.2255)
6. Your tool now appears under the agent's **Tools** section. Give your agent a name, for example
   *Hello world logger agent*, then select **Publish**.
   ![example of the agent with the tool added](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-agent-with-tool.png?_v=1.5800.2255)
7. Use the agent selector to find and select your published agent.
   ![example of selecting your published agent](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-select-agent.png?_v=1.5800.2255)
8. Chat with the agent and invoke your tool. Ask the agent to log a message for you, for example,
   *Log the message "hello world"*.
     
   The agent now calls your tool, which logs the message to the Forge logs via your Forge function.
9. Check the logs to confirm your tool ran. Go to the [developer console](https://developer.atlassian.com/console/myapps/),
   select your app, and navigate to **Logs**.

You should see a Forge log with your message:

![example of your tool creating a Forge log](https://dac-static.atlassian.com/platform/forge/images/rovo/rovo-mcp-log.png?_v=1.5800.2255)

The Forge function in the `src/hello-world-mcp.js` file shapes the behavior of the tool:

```
```
1
2
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

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).

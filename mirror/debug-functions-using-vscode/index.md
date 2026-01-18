# Debug functions using VS Code

Interactive debuggers are useful tools that help identify and fix
issues or bugs within your code. You can execute your code line by
line, examining the values of variables and the program's state at
each step.

This tutorial demonstrates the use of the interactive debugger in VSCode to debug your
back-end code in Forge [functions](/platform/forge/manifest-reference/modules/function/)
and [resolvers](/platform/forge/runtime-reference/forge-resolver/) (for apps running on
the [NodeJS runtime](/platform/forge/runtime-reference/)).

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge
development. If this is your first time using Forge, see
[Getting started](/platform/forge/getting-started/) first.

The debugging procedure in this tutorial is only supported on the [NodeJS runtime](/platform/forge/runtime-reference/). If your app uses the [legacy runtime](/platform/forge/runtime-reference/legacy-runtime-reference/), we strongly recommend that you [migrate to the NodeJS runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).

In addition, you’ll also need to install version `9.2.0` (or higher) of the [Forge CLI](/platform/forge/cli-reference/).

## Create a launch configuration file

To get started, you need to create a launch configuration file in your
Forge project. Detailed VS Code instructions are available
[here](https://code.visualstudio.com/docs/editor/debugging).

1. Open your Forge app project in VS Code, then open the
   **Run and Debug** view from the activity sidebar.

   ![Image of the Run and Debug icon view from the activity sidebar](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/run-and-debug-ui.png?_v=1.5800.1771)
2. Click on **create a launch.json file**.

   ![Image of where to create a launch.json file in Run and Debug icon view](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/create-launch-file.png?_v=1.5800.1771)
3. Select **Node.js** as your debug environment. This will create a `launch.json` file in a `.vscode` folder in your base directory.

   ![Image of selecting Node.js as debug environment](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/select-node-environment.png?_v=1.5800.1771)
4. Replace the contents of the launch.json with the following example:

   You can change the `port` to whichever port you'd prefer to use but you must include `"sourceMaps": true`.

   ```
   ```
   1
   2
   ```



   ```
   {
       // Use IntelliSense to learn about possible attributes.
       // Hover to view descriptions of existing attributes.
       // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Attach Forge App Debugger",
               "port": 9229,
               "request": "attach",
               "type": "node",
               "sourceMaps": true
           }
       ]
   }
   ```
   ```

## Start debugging

Start debugging your Forge app by starting the [Forge tunnel](/platform/forge/tunneling/) using the additional debug options.

1. Replace the `index.handler` with the function/s you want to debug and make sure the port number matches the one you specified in your `launch.json` file.

   For example:

   ```
   ```
   1
   2
   ```



   ```
   forge tunnel --debug --debugFunctionHandlers index.handler --debugStartingPort 9229
   ```
   ```

   When you run the tunnel with the debug option, Forge will generate the bundle codes under `.forge` folder. You should add `.forge` to the git ignore list.
2. You should see a message saying the debugger is listening on the port specified and the tunnel is listening for requests:

   ```
   ```
   1
   2
   ```



   ```
   ✔ Resources bundled.

   Listening for requests...

   Debugger listening on ws://0.0.0.0:9229/8d29c246-2186-4e20-9851-4aa609a3b890
   For help, see: https://nodejs.org/en/docs/inspector
   ```
   ```
3. Click on the play button in the **Run and Debug** panel to start debugging.

   ![Image of play icon in Run and Debug panel](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/play-run-debug.png?_v=1.5800.1771)

## Add a breakpoint

1. Add a breakpoint to a line of code where you want the execution to pause. This will allow you to check things like variables and application state.

   ![Image of adding a breakpoint on a line of code](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/add-breakpoint-line.png?_v=1.5800.1771)
2. Refresh the page where your Forge app is rendered so that the function is invoked. It will now pause at the breakpoint.

   ![Image of adding a breakpoint on a line of code](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/breakpoint-pause.png?_v=1.5800.1771)
3. Here you can check the values of different variables like the `context` object:

   ![Image of checking context object for values at breakpoint](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/context-check-values.png?_v=1.5800.1771)
4. Continue stepping through the function when ready.

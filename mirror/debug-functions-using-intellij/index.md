# Debug functions using IntelliJ

Interactive debuggers are useful tools that help identify and fix
issues or bugs within your code. You can execute your code line by
line, examining the values of variables and the program's state at
each step.

This tutorial demonstrates the use of the interactive debugger in IntelliJ to debug your
back-end code in Forge [functions](/platform/forge/manifest-reference/modules/function/)
and [resolvers](/platform/forge/runtime-reference/forge-resolver/) (for apps running on
the [NodeJS runtime](/platform/forge/runtime-reference/)).

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge
development. If this is your first time using Forge, see
[Getting started](/platform/forge/getting-started/) first.

The debugging procedure in this tutorial is only supported on the [NodeJS runtime](/platform/forge/runtime-reference/). If your app uses the [legacy runtime](/platform/forge/runtime-reference/legacy-runtime-reference/), we strongly recommend that you [migrate to the NodeJS runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).

In addition, you’ll also need to install version `9.2.0` (or higher) of the [Forge CLI](/platform/forge/cli-reference/).

## Set up a new configuration

1. Start the [Forge tunnel](/platform/forge/tunneling/) using the additional debug options. For example:

   ```
   1
   forge tunnel --debug --debugFunctionHandlers index.handler --debugStartingPort 9229
   ```

   Replace `index.handler` with the function/s you want to debug.
2. If you’re successful you should see a message saying the debugger is listening on the port specified and the tunnel is listening for requests.

   ```
   1
   2
   3
   4
   5
   6
   ✔ Resources bundled.

   Listening for requests...

   Debugger listening on ws://0.0.0.0:9229/8d29c246-2186-4e20-9851-4aa609a3b890
   For help, see: https://nodejs.org/en/docs/inspector
   ```
3. With your Forge app open in ItelliJ click on **Current File** and **Edit Configurations**.

   ![Image of edit configuration in IntelliJ](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/edit-configuration.png?_v=1.5800.1808)
4. Click on **Add new run configuration** and **Attach to Node.JS/Chrome**.
5. Give the configuration a new name (for example, *Forge Debugger*), and make sure the port matches the port from your CLI command (for example, *9229*).

   ![Image of configuration pop up panel](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/config-debug-panel.png?_v=1.5800.1808)
6. Click **OK**.

## Add a breakpoint and start debugging

1. Add a breakpoint to your code by clicking on a line number.
2. Run the debugger by clicking the bug icon in the top right of the screen.

   ![Image of running bug icon to debug](https://dac-static.atlassian.com/platform/forge/images/debug-functions-tutorial/debug-forge-bug-icon.png?_v=1.5800.1808)
3. Refresh your Forge app in the web browser and the code will stop executing at the breakpoint. Here you can check the value of your variables and step through your code.

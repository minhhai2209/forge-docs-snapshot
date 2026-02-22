# Profile NodeJS app performance with the Forge tunnel debugger

Profiling app code is an essential method to analyze and optimize the code. This tutorial demonstrates how to perform CPU or memory profiling on NodeJS app code with VS Code via Forge tunnel.

To familiarise yourself with debugging and profiling, see:

For a step-by-step guide on completing this tutorial, check out this video:

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development and have completed [Debug Forge functions using VS Code](/platform/forge/debug-functions-using-vscode/). If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first. In addition, you’ll also need to install version `9.2.0` (or higher) of the Forge CLI.

## Set up and trigger debugging

Let’s apply what we have learned from [Debug Forge functions using VS Code](/platform/forge/debug-functions-using-vscode/) to do performance profiling on a Forge app code.

1. Run tunnel with the debugger option. Replace the `index.runFirstMacro` with the function handler you want to debug.

   ```
   ```
   1
   2
   ```



   ```
   forge tunnel --debug --debugFunctionHandlers index.runFirstMacro
   ```
   ```
2. Open VS Code and run debugging to attach the debugger. Put a breakpoint where you want to start profiling.
3. Trigger app code function by, for example, refreshing a Confluence page or accessing a Jira issue.

## Configure profiling

1. Start profiling by clicking on the **Call Stack** view. Hover over the session you want to debug, and select the **Take Performance Profile** icon (see screenshot for reference).

   ![Take performance icon in the VS Code call stack view](https://dac-static.atlassian.com/platform/forge/images/call-stack-vscode.png?_v=1.5800.1869)
2. Select the profiling you want to conduct. It can be a CPU profile, heap profile, or heap snapshot. See [Types of profiles](https://code.visualstudio.com/docs/nodejs/profiling#_types-of-profiles) for more details.

   ![VS Code dropdown of different profile types](https://dac-static.atlassian.com/platform/forge/images/profiling-vscode.png?_v=1.5800.1869)
3. If you select **CPU Profile** or **Heap Profile**, you will need to select how long the profiling is:

   ![VS Code dropdown of how long to run CPU or Heap profile](https://dac-static.atlassian.com/platform/forge/images/profiling-duration-vscode.png?_v=1.5800.1869)

## View profiling results

1. Examine the profiling result. Once the profiling is completed, it will be generated at the top-level of the app code directly as the last 2 files in the screenshot.

   ![VS Code generates profile results](https://dac-static.atlassian.com/platform/forge/images/view-profiling-vscode.png?_v=1.5800.1869)

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).

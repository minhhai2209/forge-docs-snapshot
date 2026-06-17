# tunnel

## Description

start a tunnel to connect your local code with the app running in the
development environment

## Usage

```
1
Usage: forge tunnel [options]
```

## Options

```
1
2
3
4
5
6
7
--verbose                                              enable verbose mode
-e, --environment [environment]                        specify the environment (see your default environment by running forge settings list)
-d, --debug                                            enable debugger mode
-f,--debugFunctionHandlers <debugFunctionHandlers...>  list of function handlers declared on manifest to debug, separated by space. This option must be specified if debug mode is enabled.  It is only used for Node runtime debugger
-p,--debugStartingPort [debugStartingPort]             starting port to use for debugging, multiple handlers will get subsequent ports. It is only used for Node runtime debugger (default: "9229")
-n, --no-verify                                        disable pre-tunnel checks
-h, --help                                             display help for command
```

For CLI versions `10.1.0` and beyond, tunnels running on Cloudflare do not require additional setup.

## Further information

* [Debug functions using IntelliJ](/platform/forge/debug-functions-using-intellij): This tutorial demonstrates debugging back-end Forge functions in Node.js with IntelliJ's debugger.
* [Debug functions using VSCode](/platform/forge/debug-functions-using-vscode): This tutorial demonstrates debugging back-end Forge functions in Node.js with VS Code's debugger.
* [Tunneling](/platform/forge/tunneling/): This guide explains how to debug in real-time between the local environment and the Forge platform.

# tunnel

## Description

start a tunnel to connect your local code with the app running in the
development environment

## Usage

```
1Usage: forge tunnel [options]
2
```

## Options

```
1--verbose                                              enable verbose mode
2-e, --environment [environment]                        specify the environment (see your default environment by running forge settings list)
3-d, --debug                                            enable debugger mode
4-f,--debugFunctionHandlers <debugFunctionHandlers...>  list of function handlers declared on manifest to debug, separated by space. This option must be specified if debug mode is enabled.  It is only used for Node runtime debugger
5-p,--debugStartingPort [debugStartingPort]             starting port to use for debugging, multiple handlers will get subsequent ports. It is only used for Node runtime debugger (default: "9229")
6-h,--debugHost [debugHost]                             host to bind the Node runtime debuggers to, default is 127.0.0.1 (default: "127.0.0.1")
7-n, --no-verify                                        disable pre-tunnel checks
8--help                                                 display help for command
9
```

For CLI versions `10.1.0` and beyond, tunnels running on Cloudflare do not require additional setup.

## Further information

* [Debug functions using IntelliJ](/platform/forge/debug-functions-using-intellij): This tutorial demonstrates debugging back-end Forge functions in Node.js with IntelliJ's debugger.
* [Debug functions using VSCode](/platform/forge/debug-functions-using-vscode): This tutorial demonstrates debugging back-end Forge functions in Node.js with VS Code's debugger.
* [Tunneling](/platform/forge/tunneling/): This guide explains how to debug in real-time between the local environment and the Forge platform.

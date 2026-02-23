# Debugging

Debugging is the process of finding and fixing problems in your code. This page describes how to
debug Forge apps, including:

* How to diagnose problems using debugging features of the Forge platform, such as logging and
  tunneling.
* How to identify different types of problems, such as UI kit errors.

This information will also help you when [monitoring apps](/platform/forge/monitor-your-apps/)
that are already installed on a user's site.

## Invoking functions

To invoke a function that you want to debug, such as a scheduled trigger or Atlassian app trigger for
an unusual event, consider configuring a [web trigger](/platform/forge/web-triggers/) for the
function. See the [Add scheduled trigger](/platform/forge/add-scheduled-trigger/) guide as an example.

## Diagnosing problems

Forge provides a number of features to help you diagnose problems with your app, such as tunneling
and logging. The following section describes these features and how to use them.

If you plan to share your app with other users,
make sure your logs don't contain any sensitive or inappropriate content. For more information,
see our [Logging guidelines for app developers](/platform/forge/logging-guidelines/).

### Logging

Logging messages to the console is a common process for debugging code. Forge supports logging via
the `forge logs` CLI command, which shows the logs for your deployed app.

The `forge logs` command works like this:

1. Insert `console.log()` statements into your app’s code. For example, you may want to inspect
   values of variables as the code executes.
   Tip: If you want to pretty print a JSON object, use a statement like `console.log(JSON.stringify(jsonObject, null, 2))`.
2. Deploy and run your app.
3. In the CLI, run `forge logs`.

The output of your logging statements will be shown in the CLI. For example:

```
```
1
2
```



```
INFO  2020-01-22T06:36:33.843Z f93rfad-1234-d920-a98r-9aendas93 Number of comments on this page: 2
```
```

Each logging statement has the following structure:

* Logging level, for example, `INFO`, `WARN`, `ERROR`, etc.
* Timestamp in UTC format in "verbose mode”, that is, a longer format.
* Invocation ID
* Logging message

Only `console.log` statements from backend Forge functions are available in logs. Logging from your frontend (UI Kit JSX files and Custom UI pages) can only be accessed using your browser's developer console.

#### Options for the forge logs command

You can use a number of options with the `forge logs` command to modify the data returned:

`forge logs --verbose`: Adding the `verbose` option shows log statements with their attached metadata.
Nested JSON objects are shown as a string. For example:

```
```
1
2
```



```
INFO  2020-01-22T06:36:33.843Z 194b0adb-7362-4f0d-8fc9-6ee950bea769 Number of comments on this page: 2
    App version: 1001000
    Function name: main
```
```

`forge logs --grouped`: Adding the `grouped` option shows log statements grouped by Invocation ID.
For example:

```
```
1
2
```



```
invocation: 194b0adb-7362-4f0d-8fc9-6ee950bea769
INFO  06:36:33.843Z Number of comments on this page: 2

invocation: b3d763d0-2ebd-40fe-88a4-79e8170f8c48
INFO  01:09:26.988Z Number of comments on this page: 0
```
```

`forge logs --verbose --grouped`: Adding both the `verbose` and `grouped` options shows log statements
grouped by Invocation ID with the attached metadata. For example:

```
```
1
2
```



```
┌─────────────────────────────────────────────────────┐
│ App version    1001000                              │
│ Invocation ID  194b0adb-7362-4f0d-8fc9-6ee950bea769 │
│ Function name  main                                 │
└─────────────────────────────────────────────────────┘

INFO  2020-01-22T06:36:33.843Z 194b0adb-7362-4f0d-8fc9-6ee950bea769 Number of comments on this page: 2
    App version: 1001000
    Function name: main

┌─────────────────────────────────────────────────────┐
│ App version    6                                    │
│ Invocation ID  b3d763d0-2ebd-40fe-88a4-79e8170f8c48 │
│ Function name  main                                 │
└─────────────────────────────────────────────────────┘

INFO  2020-02-21T01:09:26.988Z b3d763d0-2ebd-40fe-88a4-79e8170f8c48 Number of comments on this page: 0
    App version: 6
    Function name: main
```
```

#### Platform limits affecting logging

Forge limits the amount of data you can log per invocation. Be mindful of
these limits when debugging your app:

| Resource | Limit | Description |
| --- | --- | --- |
| Log lines per invocation | 100 per runtime minute (rounded up) | Maximum number of log entries for an invocation. The limit is calculated based on the function timeout, specified by `timeoutSeconds`, rounded up per minute.  * A function without a timeout declared is limited to 100 log lines. * A function with `timeoutSeconds: 90` (a minute and a half) is limited to 200 log lines. |
| Log size per invocation | 200 KB | Maximum size of all log line data generated per invocation. |
| Log file size per download | 100 MB | Maximum file size of filtered logs per download. |
| Log lines per download | 96,000 | Maximum number of log entries per download. |

See [Platform quotas and limits](/platform/forge/platform-quotas-and-limits/#invocation-limits) for a complete list of related limits.

## Identifying problems

Forge has error handling for common app issues, such as not implementing UI kit components in the
correct order. This helps you identify bugs, which you can investigate using tools such as logging.
The following section describes the types of errors that are captured and where to view them.

### General coding errors

**JSX errors:** Returned for general JSX compile-time errors. For example, syntax errors. These
errors are shown in the Forge CLI during deployment or while tunneling. A stack trace is also shown.
For example:

```
```
1
2
```



```
✕ Deploying hello-world-app to development...
ℹ Packaging app files
Error: Bundling failed: ./src/index.jsx
Module build failed (from /usr/local/lib/node_modules/@forge/cli/node_modules/babel-loader/lib/index.js):
SyntaxError: /Users/alui/src/forge/hello-world-app/src/index.jsx: Unexpected token (19:6)
  17 |     <Fragment>
  18 |       <Text>Number of comments on this page: {comments.length}</Text>
> 19 |       <Image
     |       ^
  20 |         src="https://media.giphy.com/media/jUwpNzg9IcyrK/source.gif"
  21 |         alt="homer"
  22 |       />
    at Object.raise (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:7017:17)
    at Object.unexpected (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:8395:16)
    at Object.jsxParseIdentifier (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:3894:12)
    at Object.jsxParseNamespacedName (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:3904:23)
    at Object.jsxParseAttribute (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:3988:22)
    at Object.jsxParseOpeningElementAfterName (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:4009:28)
    at Object.jsxParseOpeningElementAfterName (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:6459:18)
    at Object.jsxParseOpeningElementAt (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:4002:17)
    at Object.jsxParseElementAt (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:4034:33)
    at Object.jsxParseElementAt (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:4050:32)
    at Object.jsxParseElement (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:4108:17)
    at Object.parseExprAtom (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:4115:19)
    at Object.parseExprSubscripts (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:9259:23)
    at Object.parseMaybeUnary (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:9239:21)
    at Object.parseMaybeUnary (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:6269:20)
    at Object.parseExprOps (/usr/local/lib/node_modules/@forge/cli/node_modules/@babel/parser/lib/index.js:9109:23)
```
```

**Runtime errors:** Returned for general runtime errors. For example, calling a method that does not
exist or is not a method. These errors are shown in the app UI. A stack trace is included with the
error message. For example:
![Runtime error example](https://dac-static.atlassian.com/platform/forge/images/error-runtime.png?_v=1.5800.1875)

## Related pages

* [Getting started](/platform/forge/getting-started/): The getting started tutorials demonstrate how
  `forge logs` and `forge tunnel` are used in building an example app in Jira and Confluence.
* [UI kit components](/platform/forge/ui-kit-components/): This reference page describes the available
  UI kit components.
* [Debug functions using IntelliJ](/platform/forge/debug-functions-using-intellij): This tutorial demonstrates debugging back-end Forge functions in Node.js with IntelliJ's debugger.
* [Debug functions using VSCode](/platform/forge/debug-functions-using-vscode): This tutorial demonstrates debugging back-end Forge functions in Node.js with VS Code's debugger.

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).

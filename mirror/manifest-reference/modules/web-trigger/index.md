# Web trigger

The `webtrigger` module invokes a function as the result of an HTTP request.

Within your app, you can programatically obtain the URL to call the web trigger using the
[web trigger runtime API](/platform/forge/runtime-reference/web-trigger-api).

To manually obtain a web trigger URL for development purposes, perform the following steps:

1. Get the web trigger URL by running:

   1. Select the installation for the corresponding site, Atlassian app, and Forge environment.
   2. Select the web trigger function that you want the URL for. The options come from the manifest.

   You'll be provided with a URL that you can use to invoke the web trigger. See
   [webtrigger](/platform/forge/cli-reference/webtrigger/) for more information about
   the `forge webtrigger` command.

   By default, the URLs provided by `forge webtrigger` have no built-in authentication. As such, anyone can use the URL (and, by extension, invoke its related function) without providing an authentication token. You should keep these URLs secure.

   Alternatively, you can also implement authentication inside the trigger itself. For example, you can add a check for an `Authorization` header in the request and validate any provided token.

You can also schedule a web trigger to repeatedly invoke a function on a specific interval. See
[Scheduled trigger](/platform/forge/manifest-reference/modules/scheduled-trigger/) for more information.

## Web trigger types

Generally, web triggers can be categorized into two types, web triggers that can egress data and web triggers that cannot egress data.
These types of web triggers are called `dynamic` and `static` respectively and can be configured in the manifest under your
web trigger module. See [Response](#response) for more information.

Web triggers are considered `dynamic` by default, unless configured otherwise. It is important to note that only `static` web triggers are eligible for the [Runs on Atlassian](/platform/forge/runs-on-atlassian) program.

When adding a web trigger to your app, ensure that you consider your use case and whether you need the ability to egress data from the web trigger
or not to avoid unnecessary restrictions when it comes to your apps' egress capabilities. Wherever possible, it is recommended to use `static` web triggers.

## App versions

When adding a web trigger to your app, or updating an existing web trigger, consider the following:

1. If adding a new web trigger function that is `dynamic` and your app currently does not have other `dynamic`, this is considered as egress and will become a major version update for you app.
2. If adding a new web trigger that is `static`, this is considered as a minor version update for your app.
3. If updating an existing `static` web trigger to be `dynamic`, this is considered as a major version update for your app.

Read more about app versioning in [App Versions](/platform/forge/versions/#app-versions).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `response` | [Response](#response) | No | Allows for the configuration of the response type for the webtrigger. |

Since web-triggers are publicly available URLs, Atlassian user information is not attached to invocations. This means that `asUser` API calls will not work in webtrigger functions.

### Response

Inside the `response` object, you can configure the response type and definitions for the webtrigger.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | `static | dynamic` | Yes | When set to `static`, the web trigger will only be able to egress data as configured in [Outputs](#outputs). Static web triggers are eligible for the Runs on Atlassian program. Dynamic web triggers allow developers to return any data from their function and are not eligible for the Runs on Atlassian program. |
| `outputs` | `Array` of [Outputs](#outputs) | Yes (only when `type: static`) | An array of objects that contains the configured response definitions that a web trigger function can choose to use. |

#### Outputs

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A unique identifier to use in your web trigger response object to indicate which configured static response to map to. |
| `statusCode` | `number` | Yes | The `status` code that your web trigger URL will use in its response. |
| `contentType` | `string` | No | The `content-type` that your web trigger URL will use in its response. |
| `body` | `string` | No | The `body` that your web trigger URL will use in its response. |

The web trigger function's response requires a `statusCode` field. This is why for `type: static` web triggers, configured `outputs` are required to have both a `key` and `statusCode`.
For information about web trigger request and response, see
[Web trigger events](/platform/forge/events-reference/web-trigger/#web-trigger-events).

### Examples

#### Static web trigger

Below is a configured `no-egress-web-trigger` web trigger function that can return one of the defined responses under `outputs`.

```
```
1
2
```



```
modules:
  webtrigger:
    - key: no-egress-web-trigger
      function: no-egress-function
      response:
        type: static
        outputs:
          - key: status-ok
            statusCode: 200
            contentType: application/json
            body: '{"body": "Allowed static response"}'
          - key: status-error
            statusCode: 403
            contentType: text/plain
            body: 'Error: Forbidden'
```
```

The function response uses `outputKey` to return the configured response under `outputs`, matching on `key`.

```
```
1
2
```



```
// no-egress-function.js
export async function noEgressFunction() {
  return {
    outputKey: "status-ok"
  };
}
```
```

#### Dynamic web trigger

Below is a configured web trigger function that can return any data from the function.

```
```
1
2
```



```
modules:
  webtrigger:
    - key: egress-web-trigger
      function: egress-function
      response: # Dynamic web triggers do not need to define a response field and are dynamic by default.
        type: dynamic
```
```

When using a dynamic web trigger, the function can return any data.

Despite being `type: dynamic`, the web trigger function response still requires a `statusCode` field.
For information about web trigger request and response, see
[Web trigger events](/platform/forge/events-reference/web-trigger/#web-trigger-events).

```
```
1
2
```



```
// egress-function.js
export async function egressFunction() {
  const response = await fetch("https://api.example.com/data");
  const data = await response.json(); 
  return {
    statusCode: 200,
    contentType: "application/json",
    body: JSON.stringify(data)
  };
}
```
```

### Example web trigger URL

```
```
1
2
```



```
https://4a6d16a1-bf25-4ddb-9a1a-3a781c11af3d.hello.atlassian-dev.net/x1/XUBR5WnG2Hk2V52APDdGaRSDm
```
```

Explore these tutorials and examples to enhance your understanding of web triggers.

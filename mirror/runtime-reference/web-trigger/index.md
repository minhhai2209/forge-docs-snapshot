# Web triggers

Web triggers are incoming HTTPS calls that invoke a function, such as from a third-party webhook implementation. Web
triggers are configured in the app's manifest and the URL to call is created through the Forge CLI.

The request is serialized to JSON and passed to the function in the format described below. The function that is
invoked is responsible for parsing the JSON data.

The HTTP response is formed from the JSON format described below. If the function result is not compatible with the
JSON format, then an error response with status code `500` is sent.

See the [web trigger module](/platform/forge/manifest-reference/modules/web-trigger) for more details about the types of web triggers and how to configure them in the app manifest.

Invocations from users, webtriggers, or scheduled triggers are subject to Forge's [invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Basic usage

### Handler

Your handler should be defined as a [function](/platform/forge/runtime-reference/).

```
1
2
3
4
5
6
7
export const trigger = (payload, context) => {
  return {
    statusCode: 200,
    headers: {},
    body: "Hello, world!",
  };
};
```

### Manifest definition

A [web trigger module](/platform/forge/manifest-reference/modules/web-trigger/) should be declared in the [app manifest](/platform/forge/manifest-reference/).

```
```
1
2
```



```
modules:
  webtrigger:
    - key: example
      function: my-function
      response:
        type: dynamic
  function:
    - key: my-function
      handler: index.trigger
```
```

#### Types of web triggers

There are two types of web triggers, `static` and `dynamic`, that you can specify in your manifest. Read more about these types of web triggers and their usage in [Web trigger module](/platform/forge/manifest-reference/modules/web-trigger).

## Authentication

Web trigger URLs are not authenticated by the Forge platform. This is an intentional design
choice to maximize compatibility with external tools and services.

External applications and services use a variety of security schemes for authenticating outbound
webhooks (such as HMAC signatures, bearer tokens, or basic authentication). Imposing a specific
authentication scheme on Forge web triggers requires modifying the calling client to
support it, which isn't always possible with proprietary or third-party software. In those
cases, you'd need to build and host middleware to broker requests between the external tool
and the Forge platform, resulting in a more complex and less secure system overall.

Instead, you can implement your own authentication logic directly inside the web trigger handler
function to match the security scheme used by the calling service. This keeps the authentication
logic running on the Forge platform, rather than pushing it out into external middleware.

## Generating a URL

There are two ways to generate a webtrigger URL. If you are an administrator of an installation, you can run `forge webtrigger create` via the CLI [webtrigger command](/platform/forge/cli-reference/webtrigger/). Alternatively, you can programatically generate webtrigger URLs via the [SDK](/platform/forge/runtime-reference/web-trigger-api/).

## Request

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `body` | `string` |  | HTTP request body. |
| `headers` | `object` |  | HTTP headers sent by the caller.  **Format**`nameOfTheHeader: array of strings`  **Example**`"Content-Type”: ["application/json”]` |
| `method` | `string` | Yes | HTTP method used by the client. For example, GET, POST, PUT, or DELETE. |
| `path` | `string` | Yes | Path of request sent by the caller. |
| `userPath` | `string` | Yes | Additional path segments provided by the caller after the web trigger ID. For example, if the full URL path is `/x1/{id}/hello/world`, then `userPath` would be `/hello/world`. If no additional path segments are provided, this will be an empty string. Always starts with / when path segments are present. |
| `queryParameters` | `{ [key: string]: string[] }` |  | Parsed values from the query string on the request URL. |
| `*` | `any` |  | Additional properties are provided to support forward compatibility. |

### Example

#### Request with path parameters

The following example shows a request to `/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world?apples=green,red&grapes=green`, where `/hello/world` are path parameters provided by the caller:

```
```
1
2
```



```
{
  "method": "POST",
  "headers": {
    "Accept": ["*/*"],
    "accept-encoding": ["gzip, deflate"],
    "content-length": ["71"],
    "Connection": ["keep-alive"],
    "Host": ["localhost:8080"],
    "Cache-Control": ["no-cache"],
    "Content-Type": ["text/plain"]
  },
  "body": "{\n\t\"hello\": 1,\n\t\"test\": [\"foo\", \"bar\"],\n\t\"foo\": {\n\t\t\"bar\": \"hello\"\n\t}\n}",
  "path": "/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world",
  "userPath": "/hello/world",
  "queryParameters": {
    "apples": ["red", "green"],
    "grapes": ["green"]
  }
}
```
```

In this example:

* The full URL path is: `/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world`
* The `path` field contains: `/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world` (request sent by the caller)
* The `userPath` field contains: `/hello/world` (path parameters provided by the caller)

#### Request without path parameters

The following example shows a request to `/x1/XUBR5WnG2Hk2V52APDdGaRSDm?apples=green,red&grapes=green` with no additional path segments:

```
```
1
2
```



```
{
  "method": "POST",
  "headers": {
    "Accept": ["*/*"],
    "accept-encoding": ["gzip, deflate"],
    "content-length": ["71"],
    "Connection": ["keep-alive"],
    "Host": ["localhost:8080"],
    "Cache-Control": ["no-cache"],
    "Content-Type": ["text/plain"]
  },
  "body": "{\n\t\"hello\": 1,\n\t\"test\": [\"foo\", \"bar\"],\n\t\"foo\": {\n\t\t\"bar\": \"hello\"\n\t}\n}",
  "path": "/x1/XUBR5WnG2Hk2V52APDdGaRSDm",
  "userPath": "",
  "queryParameters": {
    "apples": ["red", "green"],
    "grapes": ["green"]
  }
}
```
```

When no path parameters are provided, `userPath` is an empty string `""`.

## Response

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `body` | `string` |  | HTTP response body sent back to the caller. |
| `headers` | `object` |  | HTTP headers sent by the caller.  **Format**`nameOfTheHeader: array of strings`  **Example**`"Content-Type": ["application/json"]` |
| `statusCode` | `integer` | Yes | HTTP status code returned to the caller. |
| `statusText` | `string` |  | Text returned to communicate status. The text provides context to the status code. |
| `*` | `any` |  | Additional properties are provided to support forward compatibility. |

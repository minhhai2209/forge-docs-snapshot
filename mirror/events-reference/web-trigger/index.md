# Web trigger events

Web triggers are incoming HTTPS calls that invoke a function, such as from a third-party webhook implementation. Web
triggers are configured in the app’s manifest and the URL to call is created through the Forge CLI.

The request is serialized to JSON and passed to the function in the format described below. The function that is
invoked is responsible for parsing the JSON data.

The HTTP response is formed from the JSON format described below. If the function result is not compatible with the
JSON format, then an error response with status code 500 is sent.

Webtrigger request and response sizes (including body, headers, query parameters, and all other metadata) are subject to the function request and response payload sizes documented in the Platform quotas and limits page under [Invocation Limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

[Learn more about web triggers](/platform/forge/manifest-reference/modules/web-trigger).

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
    "Postman-Token": ["5249865e-4106-447d-aa17-52df5e57c2b9"],
    "accept-encoding": ["gzip, deflate"],
    "User-Agent": ["PostmanRuntime/7.13.0"],
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
    "Postman-Token": ["5249865e-4106-447d-aa17-52df5e57c2b9"],
    "accept-encoding": ["gzip, deflate"],
    "User-Agent": ["PostmanRuntime/7.13.0"],
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

# Call a containerised service from a web trigger event (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

You can configure [web triggers](/platform/forge/manifest-reference/modules/web-trigger) to invoke your app's container
service endpoint. To enable this, use the web trigger module's `endpoint` property to specify which container service
endpoint to invoke. This endpoint property must match the key of a container service's
[endpoint module](/platform/forge/containers-reference/ref-manifest/).

When a web trigger URL is called, the HTTP request is forwarded directly to the specified container service endpoint,
including the method, headers, body, query parameters, and any user path segments appended to the route.

For details on generating web trigger URLs, see the [CLI reference](/platform/forge/cli-reference/webtrigger/) or the
[web trigger runtime API](/platform/forge/runtime-reference/web-trigger-api/) documentation. For request and response payload size
limits, see [Invocation Limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Request

An HTTP request is made to the container endpoint route with the appropriate HTTP method, path, headers, and query parameters.

### Example

The app below defines a container service `java-service`, which has an endpoint route `/webtrigger/http`.

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
services:
  - key: java-service
    containers:
      - key: java-service
        health:
          type: http
          route:
            path: /health
        resources:
          cpu: "1"
          memory: "2Gi"

modules:
  webtrigger:
    - key: http-webtrigger
      endpoint: webtrigger-http
  endpoint:
    - key: webtrigger-http
      service: java-service
      route:
        path: /webtrigger/http
app:
  runtime:
    name: nodejs22.x
  id: ari:cloud:ecosystem::app/${APP_ID}

environment:
  variables:
    - key: TAG
      default: latest
    - key: APP_ID
      default: FORGE_REGISTER_ME
```

#### Request with path parameters

A request to web-trigger `http-webtrigger` with user path `/hello/world`, query parameter `apples=green,red&grapes=green`

```
```
1
2
```



```
curl -X POST -H "my-header: my-header-value" https://${APP_ID}/x1/{triggerId}/hello/world?apples=green,red&grapes=green
```
```

will invoke container endpoint as

```
```
1
2
```



```
curl -X POST -H "my-header: my-header-value" https://{ContainerServiceBaseUrl}/webtrigger/http/hello/world?apples=green,red&grapes=green
```
```

In this example:

* Container service endpoint route: `/webtrigger/http` (as defined in the manifest)
* The `userPath` from request: `/hello/world` (path parameters provided by the caller)
* The `queryParameters` from request: `apples=green,red&grapes=green`
* Method: `POST`
* Headers: `"my-header: my-header-value"` as provided in request

Note that `userPath` values from the request are appended to the endpoint route, so it is recommended to avoid using nested routes in your manifest.

For example, the app manifest below defines two endpoints with nested routes that both include `/webtrigger/http`. If a caller invokes the `http-webtrigger` URL with the userPath `/secure`, the resulting route `/webtrigger/http/secure` will conflict with `http-webtrigger-secure` endpoints. Depending on your container service implementation, this could cause the wrong endpoint to be invoked.

```
```
1
2
```



```
modules:
  webtrigger:
    - key: http-webtrigger
      endpoint: webtrigger-http
    - key: http-webtrigger-secure
      endpoint: webtrigger-http-secure
  endpoint:
    - key: webtrigger-http
      service: java-service
      route:
        path: /webtrigger/http
    - key: webtrigger-http-secure
      service: java-service
      route:
        path: /webtrigger/http/secure
```
```

Instead, you can use a flat path for endpoints and avoid nested paths. For this example, the following manifest will work perfectly.

```
```
1
2
```



```
modules:
  webtrigger:
    - key: http-webtrigger
      endpoint: webtrigger-http
    - key: http-webtrigger-secure
      endpoint: webtrigger-http-secure
  endpoint:
    - key: webtrigger-http
      service: java-service
      route:
        path: /webtrigger/http
    - key: webtrigger-http-secure
      service: java-service
      route:
        path: /webtrigger/secure-http
```
```

#### Request without path parameters

A request to web-trigger `http-webtrigger` without user path and query parameters `apples=green,red&grapes=green`

```
```
1
2
```



```
curl -X POST -H "my-header: my-header-value" https://${APP_ID}/x1/{triggerId}?apples=green,red&grapes=green
```
```

will invoke container endpoint as

```
```
1
2
```



```
curl -X POST -H "my-header: my-header-value" https://{ContainerServiceBaseUrl}/webtrigger/http?apples=green,red&grapes=green
```
```

In this example:

* Container service endpoint route is: `/webtrigger/http` as defined in the manifest
* The `queryParameters` value from request: `apples=green,red&grapes=green`
* Method: `POST`
* Headers: `"my-header: my-header-value"` as provided in request

## Response

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `body` | `string` |  | HTTP response body sent back to the caller. |
| `headers` | `object` |  | HTTP headers sent by the caller.  **Format**`nameOfTheHeader: array of strings`  **Example**`"Content-Type": ["application/json"]` |
| `statusCode` | `integer` | Yes | HTTP status code returned to the caller. |
| `statusText` | `string` |  | Text returned to communicate status. The text provides context to the status code. |
| `*` | `any` |  | Additional properties are provided to support forward compatibility. |

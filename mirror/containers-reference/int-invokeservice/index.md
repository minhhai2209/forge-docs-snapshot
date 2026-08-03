# Call a containerised service directly from the frontend or backend (Preview)

Forge Container services is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#forge-preview).

Use the `invokeService` method to invoke a container service's functionality directly from the frontend or backend.

## Frontend invocation

When making an invocation from the frontend, the `invokeService` method must use a container service’s [endpoint](/platform/forge/containers-reference/ref-manifest/). The service endpoint must also be defined as an endpoint module. See [Define endpoints](/platform/forge/containers-reference/integrating-service/#define-endpoints) for details.

To use the `invokeService` method, import it from `@forge/bridge`:

```
1
import { invokeService } from '@forge/bridge'
```

This method is only enabled on [UI Kit](/platform/forge/ui-kit/) and [Custom UI](/platform/forge/custom-ui/).

### Function signature

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
interface InvokeServiceInput {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  headers?: Record<string, string>;
  body?: unknown;
}

function invokeService(
  input: InvokeServiceInput
): Promise<{ [key: string]: any } | void>;
```

### Arguments

* **path**: The path that will be appended to the base URL of the service.
* **method**: The HTTP method for the request.
* **headers**: Optional custom [headers](/platform/forge/remote/essentials#request-headers) that you can add to your request.
* **body**: The body of your request (must be in JSON format).

### Returns

A `Promise` that resolves with the data returned from the invoked endpoint:

* The `content-type` header must be `application/json`.
* For successful responses, headers will be available in the `headers` properties.
* For successful responses (1XX, 2XX, 3XX), where the `content-type` is JSON, the `Promise` will resolve.
* For successful responses (1XX, 2XX, 3XX), where the `content-type` is not JSON, the `Promise` will reject and a corresponding error message will be returned.
* For 4XX or 5XX code responses, regardless of the `content-type` returned, the `Promise` will resolve with a response in the following format:

```
```
1
2
```



```
{
  "headers": {
    "Content-Type": "application/json",
    "X-Custom-Header": "value1,value2"
  },
  "error": "", // always a string, containing the body, so could be escaped JSON
  "status": 4xx/5xx
}
```
```

## Backend invocation

You can also use `invokeService` to call a container service directly from a backend function. You won’t need a pre-defined endpoint for this. To do this, you’ll need to import `invokeService` from `@forge/api` first:

```
```
1
2
```



```
import { invokeService } from '@forge/api';
```
```

### Function signature

```
```
1
2
```



```
interface RequestInit {
  body?: ArrayBuffer | string | URLSearchParams;
  headers?: Record<string, string>;
  method?: string;
  redirect?: RequestRedirect;
  signal?: AbortSignal;
}

type InvokeEndpointOptions = {
  path: string;
};

interface APIResponse {
  json: () => Promise<any>;
  text: () => Promise<string>;
  arrayBuffer: () => Promise<ArrayBuffer>;

  ok: boolean;
  status: number;
  statusText: string;
  headers: Headers;
}

export async function invokeService(
  serviceKey: string,
  options: RequestInit & InvokeEndpointOptions
): Promise<APIResponse>
```
```

Refer to [this invocation](https://bitbucket.org/atlassian/forge-containers-app/src/main/src/panel.js) in our reference app for an example implementation.

### Required Arguments

* `serviceKey`**:** Key of the service entry in the `manifest.yml` file.
* `path`**:** **Must be a non-empty string**. This `path` value determines which endpoint will be called.
  * For example, `/invoke-service?hello=world`

### Returns

`Promise<APIResponse>`

# invokeRemote

The `invokeRemote` bridge method enables apps to integrate with [remote backends](/platform/forge/remote)
hosted outside the Atlassian platform.

Requests are validated and hydrated with required authentication (e.g. OAuth tokens if configured) before being proxied from Forge to the remote server. The HTTP response is validated before being returned to the frontend.

To use the `invokeRemote` bridge method, you need to define an [endpoint](/platform/forge/manifest-reference/endpoint)
for your back end in the `manifest.yml` file.

Invocations from users, webtriggers, or scheduled triggers are subject to Forge's [invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Function signature

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
interface InvokeRemoteInput {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  headers?: Record<string, string>;
  body?: unknown;
}

function invokeRemote(
  input: InvokeRemoteInput
): Promise<{ [key: string]: any } | void>;
```

## Arguments

* **path**: The path that will be appended to the `baseUrl` of the [remote](/platform/forge/manifest-reference/remotes).
* **method**: The HTTP method for the request.
* **headers**: Optional custom [headers](/platform/forge/remote/essentials#request-headers) that you can add to your request.
* **body**: The body of your request.

## Returns

A `Promise` that resolves with the data returned from the invoked endpoint:

* The `content-type` header must be `application/json`.
* The HTTP status code from the response will not be available in the `Promise`.
* For successful responses, headers will be available in the `headers` properties.
* For non-JSON or non-2xx status code responses, the `Promise` will reject and a corresponding error message will be returned.

Further information about the Forge Remote invocation contract can be found [here](/platform/forge/forge-remote-invocation-contract).

## Example

Making a `POST` request to a remote endpoint:

```
```
1
2
```



```
import { invokeRemote } from "@forge/bridge";

const res = await invokeRemote({
  path: `/tasks/`,
  method: 'POST',
  headers: {
    x-header-key: 'x-header-value',
  },
  body: {
    department: 'Ecosystem',
    team: 'Forge',
    description: 'Write docs'
  }
});

console.log(`Created task: ${JSON.stringify(res.task)}`);
```
```

Making a `GET` request to a remote endpoint:

```
```
1
2
```



```
import { invokeRemote } from "@forge/bridge";

const res = await invokeRemote({
  path: `/tasks/?team=Forge`,
  method: 'GET'
});

console.log(`Tasks: ${JSON.stringify(res.body[0])}`);
```
```

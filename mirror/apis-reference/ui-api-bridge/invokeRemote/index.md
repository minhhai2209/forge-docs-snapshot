# invokeRemote

The `invokeRemote` bridge method enables apps to integrate with a single [remote backend](/platform/forge/remote) hosted outside the Atlassian platform.

Requests are validated and hydrated with required authentication (e.g. OAuth tokens if configured) before being proxied from Forge to the remote server. The HTTP response is validated before being returned to the frontend.

To use the `invokeRemote` bridge method, you need to define an [endpoint](/platform/forge/manifest-reference/endpoint) for your back end in the `manifest.yml` file. For example:

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
modules:
  jira:issuePanel:
    - key: my-jira-issue-panel
      resolver:
        endpoint: my-remote-endpoint
      # ... other resolver properties
  endpoint:
    - key: my-remote-endpoint
      remote: my-remote
remotes:
  - key: my-remote
    baseUrl: https://my-remote.com
```

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
11
12
interface InvokeRemoteInput {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  headers?: Record<string, string>;
  body?: unknown;
}

function invokeRemote(input: InvokeRemoteInput): Promise<{
    headers: Record<string, string[]>;
    status: number;
    body?: Record<string, any>;
}>;
```

## Arguments

* **path**: The path that will be appended to the `baseUrl` of the [remote](/platform/forge/manifest-reference/remotes) following the relative path resolution rules of the [URL Standard](https://developer.mozilla.org/en-US/docs/Web/API/URL/URL).
* **method**: The HTTP method for the request.
* **headers**: Optional custom [headers](/platform/forge/remote/essentials#request-headers) that you can add to your request.
* **body**: Optional body of your request. If you are sending a `body`, you must send a valid JSON `object` as it will get transformed with `JSON.stringify(body)` before being sent to the remote.

## Returns

### Successful responses

To resolve the `Promise` successfully, the remote must respond with:

| Status code | Body required? | `content-type` header required? |
| --- | --- | --- |
| 2xx | No | No |
| Non-2xx (except 401, see below) | Yes | No, but if set, it must be set to `application/json` |

### Error responses

Possible error scenarios which cause the `Promise` to reject:

| Description | Error message |
| --- | --- |
| 401 returned from the remote.  This status code is reserved for the Forge platform to identify Forge Invocation Token validation errors. | `Remote could not verify the Forge Invocation Token` |
| Non-2xx with `content-type` header set but not equal to `application/json` | `Invalid response from remote` |
| Body value is not valid JSON and cannot be parsed.  This same error will occur if the status is non-2xx without a body. | `Invalid response from remote` |
| Network error (e.g. server unreachable) | `Invalid response from remote` |
| Timeout | `Remote invocation timed out after X seconds` |
| Other unhandled error | `An unexpected error happened` |

See the [Forge Remote invocation contract](/platform/forge/forge-remote-invocation-contract) for further details.

## Example

Making a `POST` request to a remote endpoint:

```
```
1
2
```



```
import { invokeRemote } from '@forge/bridge';

const res = await invokeRemote({
  path: `/tasks/`,
  method: 'POST',
  headers: {
    'x-header-key': 'x-header-value',
  },
  body: {
    department: 'Ecosystem',
    team: 'Forge',
    description: 'Write docs'
  }
});

console.log(`Created task: ${JSON.stringify(res.body.task)}`);
```
```

Making a `GET` request to a remote endpoint:

```
```
1
2
```



```
import { invokeRemote } from '@forge/bridge';

const res = await invokeRemote({
  path: `/tasks/?team=Forge`,
  method: 'GET'
});

console.log(`Tasks: ${JSON.stringify(res.body.tasks[0])}`);
```
```

# Invoke Remote API

The `invokeRemote` method enables apps to integrate with [remote backends](/platform/forge/remote)
from within Forge [functions](/platform/forge/manifest-reference/modules/function).

To use the `invokeRemote` method, you need to define a [remote](/platform/forge/manifest-reference/remotes)
for your backend in the `manifest.yml` file.

You must include `compute` in the remote definition's `operations` array,
to allow backend functions to invoke the remote.

## Function signature

```
1import { RequestInit, Response } from 'undici';
2
3type InvokeRemoteOptions = {
4  path: string;
5};
6
7type APIResponse = Pick<Response, 'json' | 'text' | 'arrayBuffer' | 'ok' | 'status' | 'statusText' | 'headers'>
8
9export async function invokeRemote(
10  remoteKey: string,
11  options: RequestInit & InvokeRemoteOptions
12): Promise<APIResponse>;
13
```

## Arguments

* **remoteKey**: Key of the remote entry in the `manifest.yml` file.
* **path**: **Must be a non-empty string** (like `'/'`). The path that will be appended to the `baseUrl` of the [remote](/platform/forge/manifest-reference/remotes).
* The rest in `options` are as in [Undici's options](https://undici.nodejs.org/#/docs/api/Dispatcher?id=parameter-requestoptions).

## Returns

`Promise<Response>`, see [Undici ResponseData](https://undici.nodejs.org/#/docs/api/Dispatcher?id=parameter-responsedata).

## Example

Making a `POST` request to a remote endpoint:

```
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
```



```
import { invokeRemote } from '@forge/api';

const res = await invokeRemote('my-remote-key', {
  path: `/tasks/`,
  method: 'POST',
  headers: {
    'x-header-key': 'x-header-value'
  },
  body: JSON.stringify({
    department: 'Ecosystem',
    team: 'Forge',
    description: 'Write docs'
  })
});

if (!res.ok) {
  throw new Error(`invokeRemote failed: ${res.status}`);
}

const json = await res.json();
console.log(`Created task: ${JSON.stringify(json.task)}`);
```
```

Making a `GET` request to a remote endpoint:

```
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
```



```
import { invokeRemote } from '@forge/api';

const res = await invokeRemote('my-remote-key', {
  path: `/tasks/?team=Forge`,
  method: 'GET'
});

if (!res.ok) {
  throw new Error(`invokeRemote failed: ${res.status}`);
}

const json = await res.json();
console.log(`Tasks: ${JSON.stringify(json)}`);
```
```

## Context and security

No context will automatically be passed to `invokeRemote` when called from a backend Forge function,
unlike the context shown on [Forge Remote essentials](/platform/forge/remote/essentials/),
which is only provided to frontend invocations of `invokeRemote`.

Context should only be pulled from the FCT token in your backend function,
otherwise it could be untrusted user input.

Because the context will be passed to the backend through `GET` params or `POST` body,
it is possible for a frontend user to spoof these parameters and make a call directly to the backend with altered values.

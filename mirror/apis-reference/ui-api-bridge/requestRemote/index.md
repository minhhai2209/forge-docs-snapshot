# requestRemote

The `requestRemote` bridge method allows Forge apps to make direct requests to remote backends from UI Kit and Custom UI applications. This method is optimized for latency-sensitive requests that affect user experience and don't require OAuth tokens. The method returns a standard WHATWG fetch Response object.

Unlike `invokeRemote`, requests made with `requestRemote` are not treated as official invocations and are not proxied through the Forge platform. This means `requestRemote` will not include OAuth tokens, even if configured for the remote, and will not be reflected in invocation metrics in the Developer console.

Similar to `invokeRemote`, requests include a Forge Invocation Token (FIT) as a bearer token in the authorization header. The FIT is a JWT that contains key information about the invocation context, signed into the claims.

**Keeping your remote app secure**
Your remote backend must validate the FIT to confirm the request originates from Atlassian. You must also verify the contextual claims to ensure the operations performed by your service suit the request context. See [Verifying Remote Requests](/platform/forge/remote/essentials/#verifying-remote-requests) for more details on how to validate the FIT.

You may choose to use `requestRemote` over `invokeRemote` for latency sensitive applications, which directly impacts user experience and you don't need OAuth tokens for Atlassian API calls.

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
type RequestRemoteOptions = {
  path: string;
};

function requestRemote(
  remoteKey: string,
  options?: RequestRemoteOptions & RequestInit,
): Promise<Response>
```

## Arguments

* **remoteKey**: Key of the remote entry in the `manifest.yml` file.
* **options**:
  * **path**: URL path appended to the remote's baseUrl. Example: if baseUrl is `https://api.example.com` and path is `/users/123`, the final URL becomes `https://api.example.com/users/123`
  * Supports all standard [RequestInit](https://fetch.spec.whatwg.org/#requestinit) properties like `method`, `headers` and `body`, but does not support `signal`

### FormData support

requestRemote accepts [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) as the request body. If you send files as part of the form, please note that you can send **only one file, and it must be named `file`**.

```
```
1
2
```



```
// Create a Blob with some text content
const content = 'This is the content of the file.';
const blob = new Blob([content], { type: 'text/plain' });

// Create a File object from the Blob
const file = new File([blob], 'testfile.txt', { type: 'text/plain' });
const formData = new FormData();
// NOTE: The file must be named 'file'
formData.append('file', file);
```
```

## Returns

## Example

Making a `POST` request to a remote endpoint:

```
```
1
2
```



```
import { requestRemote } from '@forge/bridge';

const response = await requestRemote('my-remote-key', {
  path: `/tasks/?team=Forge`,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'custom-header': 'custom-value'
  },
  body: JSON.stringify({
    taskName: 'My cool Forge task'
  })
});

if (!response.ok) {
  throw new Error(`request failed with the following status code: ${response.status}`);
}
```
```

Making a `GET` request to a remote endpoint

```
```
1
2
```



```
import { requestRemote } from '@forge/bridge';

const response = await requestRemote('my-remote-key', {
  path: `/tasks/?team=Forge`,
  method: 'GET',
  headers: {
    'custom-header': 'custom-value'
  },
});

if (!response.ok) {
  throw new Error(`request failed with the following status code: ${response.status}`);
}
```
```

Making a `POST` request to a remote endpoint with `FormData` as the body

```
```
1
2
```



```
import { requestRemote } from '@forge/bridge';

// Construct FormData object
const formData = new FormData();
formData.append('username', 'user-1');
formData.append('userId', '1');

const response = await requestRemote('my-remote-key', {
  path: '/post',
  method: 'POST',
  headers: {
    'custom-header': 'custom-value'
  },
  body: formData
});

if (!response.ok) {
  throw new Error(`request failed with the following status code: ${response.status}`);
}
```
```

## Limitations

* **FIT claims**: The FIT sent in the authorization header does not include the `app.license` field in the claims. We intend to add these, please follow the [Forge changelog](/platform/forge/changelog/) for updates.
* **Streaming**: Response body streaming is not supported. The entire response must be received before processing.
* **OAuth tokens**: Unlike `invokeRemote`, OAuth tokens are not included in requests. If you require them to be delivered on invocation, please use `invokeRemote` instead.
* **Metrics**: Requests are not tracked in the Developer Console's invocation metrics.
* **FIT refresh**: FIT tokens are cached but may expire. The API handles renewal automatically, but be prepared for occasional additional latency on the first request and longer user sessions.

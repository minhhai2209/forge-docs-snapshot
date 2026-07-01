# Installation Details API

You can retrieve details for a single Forge app installation through the Installation Details REST API. The response includes the installed app version, the installation's context (workspace) ARIs, and the OAuth scopes and external egress allowlists granted to the installation.

You can only retrieve details for an installation that your OAuth token is scoped to. The `installationId` in the request path must match the installation that the token was issued for, otherwise the request is rejected.

No OAuth 2.0 scopes are required.

## requestAtlassian

The Forge SDK code examples on this page use the `requestAtlassian` method, which is available on the object returned by `asApp`, exported from the `@forge/api` package.
This method uses the app's credentials, determined by the scopes defined in the app's manifest.

## Get installation details

Send a `GET` request to `/forge/installation/v1/{appId}/{envId}/installation/{installationId}` to retrieve details for the given installation.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `appId` | `string (UUID)` | Yes | The app's ID. |
| `envId` | `string (UUID)` | Yes | The environment's ID. |
| `installationId` | `string (UUID)` | Yes | The installation's ID. This must match the installation that the OAuth token was issued for. |

### Code examples

```
```
1
2
```



```
import { asApp } from '@forge/api';

const appId = '35559c21-6120-406b-b7cd-d87f468f6d32';
const envId = '3aaa01b0-02cc-1d00-3eee-1f01e001d1c0';
const installationId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';

try {
  const response = await asApp().requestAtlassian(
    `/forge/installation/v1/${appId}/${envId}/installation/${installationId}`,
    {
      method: 'GET'
    }
  );

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const body = await response.json();
  console.log(`Response: ${response.status}`, body);
} catch (error) {
  console.error('Failed to retrieve installation details', error);
}
```
```

### Responses

#### 200: OK

Details were successfully retrieved for the installation.

##### Response schema

| Property | Type | Description |
| --- | --- | --- |
| `version` | `string` | The app version installed. |
| `installationContext` | `object` | The primary installation context. See [Installation context object](#installation-context-object) below. |
| `secondaryInstallationContexts` | `array` | Additional installation contexts the installation can act in. Each item is an [installation context object](#installation-context-object). |
| `permissions` | `object` | The OAuth scopes and external egress allowlists granted to the installation. See [Permissions object](#permissions-object) below. |
| `isSandbox` | `boolean` | Whether the installation context is a sandbox. Omitted when the app is installed in a non-site based context. |

**Installation context object** (`installationContext` and each item in `secondaryInstallationContexts`):

| Property | Type | Description |
| --- | --- | --- |
| `id` | `string` | The context (workspace) ARI. |

**Permissions object** (`permissions`):

| Property | Type | Description |
| --- | --- | --- |
| `scopes` | `array` | OAuth scopes granted to the installation. |
| `external` | `object` | External resource allowlists, grouped by Forge external permission category. See [External permissions object](#external-permissions-object) below. |

**External permissions object** (`permissions.external`):

The egress allowlists are derived from the app's manifest. For more information, see [Add content security and egress controls](/platform/forge/add-content-security-and-egress-controls/#define-the-external-domains-in-the-manifest-file).

| Property | Type | Description |
| --- | --- | --- |
| `fetch.backend` | `array` | Backend fetch egress allowlist. |
| `fetch.client` | `array` | Client-side fetch egress allowlist. |
| `images` | `array` | Image egress allowlist. |
| `media` | `array` | Media (audio/video) egress allowlist. |
| `styles` | `array` | Stylesheet egress allowlist. |
| `scripts` | `array` | Script egress allowlist. |
| `frames` | `array` | Frame (iframe) egress allowlist. |
| `fonts` | `array` | Font egress allowlist. |

##### Example

```
```
1
2
```



```
{
  "version": "12.0.3",
  "installationContext": {
    "id": "ari:cloud:confluence::site/a12bc345-678d-9e1f-ab10-1bcd112131e4"
  },
  "secondaryInstallationContexts": [
    {
      "id": "ari:cloud:jira::site/b23cd456-789e-1f20-bc21-2cde223242f5"
    }
  ],
  "permissions": {
    "scopes": ["read:jira-user", "storage:app"],
    "external": {
      "fetch": {
        "backend": ["https://api.example.com"],
        "client": ["https://cdn.example.com"]
      },
      "images": ["https://images.example.com"],
      "media": ["https://media.example.com"],
      "styles": ["https://styles.example.com"],
      "scripts": ["https://scripts.example.com"],
      "frames": ["https://frames.example.com"],
      "fonts": ["https://fonts.example.com"]
    }
  },
  "isSandbox": false
}
```
```

#### 4XX Error codes

401: Unauthorized

404: Not Found

429: Too Many Requests

OAuth authentication failed, or the `installationId` in the request path does not match the installation that the OAuth token was issued for.

##### Example

```
```
1
2
```



```
{
  "type": "AuthorizationError",
  "code": 401,
  "message": "Authorization failed"
}
```
```

#### 500: Internal Server Error

The service encountered an unexpected problem.

```
```
1
2
```



```
{
  "type": "InternalError",
  "code": 500,
  "message": "An internal error occurred"
}
```
```

## Remote compatibility

You can call the Installation Details REST API from a remote backend. For more information, see [Calling Atlassian app APIs from a remote](/platform/forge/remote/calling-product-apis/), and the API endpoint is `https://api.atlassian.com/forge/installation/v1/{appId}/{envId}/installation/{installationId}`.

## Rate limit

| Scope | Limit |
| --- | --- |
| Per `installationId` | 1 request per 5 minutes |
| Per `appId` | 10 requests per minute |

Because all installations of an app share the per-`appId` limit, your app may hit a `429 Too Many Requests` response even if it hasn't reached the per-installation limit. When this happens, wait for the number of seconds specified in the `Retry-After` response header before retrying.

We recommend caching installation details and using a much lower frequency than the hard limit. If you receive a `429` response, retry with exponential back-off and jitter.

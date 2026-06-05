# Customer-managed egress and remotes API (Preview)

[Customer-managed egress and remotes](/platform/forge/customer-managed-egress-and-remotes/) is now available as a Forge Preview feature.

Preview features are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more information, see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Once the manifest of an app has been configured, the app can interact with customer‑managed egress and remotes using the async Forge functions in the `permissions` module in `@forge/bridge`.

Egress-related calls will fail if `permissions.external.configurable.enabled` is not set to `true`, and setting a remote will not work unless the remote has the `configured` property defined in the manifest.

## Set egress

When `permissions.egress.set` is called, an admin will see a confirmation modal describing the egress that will be added. If they approve, the group is saved and the Promise resolves. If they reject, the Promise rejects. This requires the user to be an administrator. This promise can be caught in the Forge app code and relevant errors can be shown to the user and handled as appropriate.

When this is called an admin will see a confirmation modal describing the egress that will be added. If they approve, the group is saved and the Promise resolves. If they reject, the Promise rejects. This requires the user to be an administrator otherwise the Promise will reject. This Promise can be caught in the Forge app code and relevant errors can be shown to the user and handled as appropriate.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the egress group |
| `description` | `string` | Yes | The description of the egress group being created. This appears in the admin modal to provide context to the reviewing admin |
| `configured` | `array` | Yes | An array of objects containing information about the egress being configured. The object consists of two fields:  * `domain` which contains the URL that will be egressed to. This may be a wildcard `*` for permissive egress. * `type` which contains an array of strings specifying which type of egress is allowed for this domain. These strings map to [these permission types](/platform/forge/manifest-reference/permissions/#fetch) and are defined in the [@forge/egress](https://www.npmjs.com/package/@forge/egress) package. |

### Responses

| Code | Description |
| --- | --- |
| 201 | Success |
| 400 | Malformed request, validation failures, or max egress limit exceeded |
| 403 | Authorization/permission issues, feature not enabled for app, or rate limit exceeded |
| 422 | Business logic violations (duplicate keys/domains, invalid URLs) |
| 5XX | Unexpected server errors |

### Example

```
```
1
2
```



```
import { permissions } from "@forge/bridge";
import { EgressType } from "@forge/egress";

async function configureEgress() {
  await permissions.egress.set({
    egresses: [
      {
        key: "example-egress",
        description: "Access to example.com",
        configured: [
          {
            domain: "https://api.example.com",
            type: [EgressType.Image],
          },
        ],
      },
    ],
  });
}
```
```

## Get egress

When `permissions.egress.get` is called, any previously configured egress groups will be returned. This call does not require a user to be an administrator.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `keys` | `string[]` | No | If provided, will return any egress groups that match the keys. If undefined, all egress groups will be returned. |
| `pageSize` | `number` | No | Number of egress groups to return in a single page. If undefined, will default to returning all available egress groups. |
| `nextPageToken` | `string` | No | Token to fetch the next page of values when paginating with `pageSize`. |

### Responses

| Code | Description |
| --- | --- |
| 200 | Success. Returns any configured egress groups. |
| 400 | Invalid query parameters (pageSize out of range, invalid types) |
| 401 | Authentication failures (missing/invalid OAuth claims, system account issues) |
| 403 | Authorization failures (insufficient permissions, feature not enabled, rate limit) |
| 429 | Rate limit exceeded |
| 5XX | Server/dependency errors |

### Example

```
```
1
2
```



```
import { permissions } from "@forge/bridge";

async function getEgress() {
  const getAllEgressGroups = await permissions.egress.get({});
  const getSomeEgressGroups = await permissions.egress.get({
    keys: ["my-egress-group-1", "my-egress-group-2"],
  });
}
```
```

## Delete domain from egress group

Use `permissions.egress.deleteDomain` to delete a single domain from a previously defined egress group. This is useful when you want to keep the group but remove one domain/type entry. This requires the user to be an administrator.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the egress group |
| `domain` | `string` | Yes | The domain to delete from the group |
| `type` | `string` | Yes | The egress type to delete from the group. This is required because a group may have multiple egress types set for the same domain. |

### Response

| Code | Description |
| --- | --- |
| 204 | Success (No Content). The domain/type combination was deleted, or didn't exist. |
| 400 | Invalid request body (missing fields, wrong types, invalid enum value) |
| 403 | Authorization failures (insufficient permissions, feature not enabled, rate limit) |
| 429 | Rate limit exceeded |
| 5XX | Server/dependency errors |

### Example

```
```
1
2
```



```
import { permissions } from "@forge/bridge";

async function deleteEgress() {
  await permissions.egress.deleteDomain({
    key: "my-egress-group",
    domain: "http://www.example.com",
    type: "FRAMES",
  });
}
```
```

## Delete group

Use `permissions.egress.deleteGroup` to delete an entire egress group and all of its defined domains. This requires the user to be an administrator.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the egress group |

### Response

| Code | Description |
| --- | --- |
| 204 | Success (No Content). The egress group was deleted, or didn't exist. |
| 400 | Invalid or missing key query parameter |
| 403 | Authorization failures (insufficient permissions, feature not enabled, rate limit) |
| 429 | Rate limit exceeded |
| 5XX | Server/dependency errors |

### Example

```
```
1
2
```



```
import { permissions } from "@forge/bridge";

async function deleteEgress() {
  await permissions.egress.deleteGroup({
    key: "my-egress-group",
  });
}
```
```

## Set remote endpoint

Use `permissions.remote.set` to set or update the endpoint of a customer-managed remote. This requires the user to be an administrator.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `remotes` | `array` | Yes | An array of objects representing remotes, it must contain:  * key: The key of the remote to be updated. The remote must exist in the manifest and be `configurable`. * endpoint: Absolute URL for the remote, or `null` to reset it. If a `baseUrl` is defined in the manifest, resetting to `null` will restore the manifest value. If no `baseUrl` is defined, resetting to `null` will unset the endpoint. |

### Response

| Code | Description |
| --- | --- |
| 201 | Success |
| 400 | Invalid request body, max remotes exceeded |
| 403 | Authorization failures, rate limit |
| 422 | Duplicate keys, invalid endpoints, pattern mismatch |
| 429 | Rate limit exceeded |
| 5XX | Server/dependency errors |

### Example

```
```
1
2
```



```
import { permissions } from "@forge/bridge";

async function setRemote() {
  await permissions.remote.set({
    remotes: [
      {
        key: "my-remote",
        configured: {
          endpoint: "https://example.com",
        },
      },
    ],
  });
}
```
```

## Get remote endpoint

Use `permissions.remote.get` to get previously configured remotes for an installation. You can fetch specific remotes or all remotes. This does not require the user to be an administrator.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `keys` | `string[]` | No | If provided, will return any remotes that match the keys. If undefined, all remotes will be returned. |
| `pageSize` | `number` | No | Number of remotes to return in a single page. If undefined, will default to returning all available remotes. |
| `nextPageToken` | `string` | No | Token to fetch the next page of values when paginating with `pageSize`. |

### Response

| Code | Description |
| --- | --- |
| 200 | Success |
| 400 | Invalid query parameters (pageSize out of range, keys exceeds pageSize, invalid types) |
| 401 | OAuth authentication failures |
| 403 | Authorization failures, rate limit |
| 429 | Rate limit exceeded |
| 5XX | Server/dependency errors |

### Example

```
```
1
2
```



```
import { permissions } from "@forge/bridge";

async function getRemotes() {
  const getAllRemotes = await permissions.remote.get({});
  const getSomeRemotes = await permissions.remote.get({
    keys: ["my-remote", "my-remote-2"],
  });
}
```
```

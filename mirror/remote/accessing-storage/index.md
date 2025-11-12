# Accessing Forge storage from a remote via REST API

You can configure a remote back end to store data on Forge’s
[Key-Value Store (KVS)](/platform/forge/rest/api-group-key-value-store/) or
[Custom Entity Store](/platform/forge/rest/api-group-custom-entity-store/) via REST API.

## Prerequisites

In order to communicate with Forge’s back end via REST API from remote, you’ll need to configure your app to call a remote backend (from a Custom UI or UI Kit 2 frontend). To do this, you’ll need to configure the following properties in your `manifest.yml` file:

| Property | Setting | Description |
| --- | --- | --- |
| `endpoint.auth.appSystemToken` | Set to `true` | This setting ensures that requests to your remote contain an `x-forge-oauth-system header`. This header contains a token (valid for at least 55 minutes) that you can use to call this REST API. See [Endpoint](/platform/forge/manifest-reference/endpoint/) for reference. |
| permissions.scopes | Must contain:  * storage:app * read:app-system-token | Forge requires these scopes to allow access to this REST API from remotes. See [Forge scopes](/platform/forge/manifest-reference/scopes-forge/) for reference. |

### Additional prerequisites for Custom Entities

Before you can start storing data in the Custom Entity Store, you’ll need to *define* your entities first. See
[Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) and
[Custom entities](/platform/forge/runtime-reference/custom-entities/) for detailed information on how to do this.

## Authentication

Requests to this API must be authenticated via a bearer token that is passed to your app via the `x-forge-oauth-system` header. Your app must supply this token in the `Authorization: Bearer {bearerToken}` header of the request. You can not use standard OAuth 2.0 3LO tokens to call this API.

## Requests

All requests should be sent in JSON format to the base URL `https://api.atlassian.com/forge/storage/kvs`, followed by the desired operation defined in the API. The following Node.js example uses the
`fetch` function from the `node-fetch` module to request data from the REST API:

```
```
1
2
```



```
'use strict'
import fetch from 'node-fetch';
const apiBaseUrl = 'https://api.atlassian.com/forge/storage/kvs';
export async function fetchFromStorage(token, apiBaseUrl) {
  const headers = {
     'Accept': 'application/json',
     'Authorization': `Bearer ${token}`,
     'Content-Type': 'application/json'
  }
  return await fetch(`${apiBaseUrl}/v1/get`, { method: "POST", headers });
}
```
```

## Quota and limit handling

Forge hosted storage capabilities are subject to limits, usage, and syntax constraints. These include limits to the number of operations, key lengths, and object depth. Any request that exceeds a quota or limit will return a
`429` status with an error code of `RATE_LIMIT_EXCEEDED`.

See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and
[Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for details about relevant constraints.

## Error handling

In conjunction with proper HTTP status codes, non-2xx responses will have the following schema:

```
```
1
2
```



```
{
  code: string; // "INVALID_KEY_FORMAT"
  message: string; // "Invalid key format"
}
```
```

Each `400 Bad Request` response will be accompanied by an *error code* containing more information. The following tables lists all possible error codes, what they mean, and what you can do to address each one:

| Error code | Description |
| --- | --- |
| KEY\_TOO\_SHORT | The provided key needs to be more than one character. |
| KEY\_TOO\_LONG | The provided key has exceeded the maximum 500 characters. |
| INVALID\_KEY | The provided key does not match the regex: `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` |
| NOT\_FOUND | The specified key does not exist. |

| Error code | Description |
| --- | --- |
| MAX\_SIZE | The provided value has exceeded the maximum size limit. |
| MAX\_DEPTH | The provided value has exceeded the maximum object depth (32) limit. |

| Error code | Description |
| --- | --- |
| ENTITY\_TYPE\_TOO\_SHORT | The provided key needs to be more than 3 characters. |
| ENTITY\_TYPE\_TOO\_LARGE | The provided key has exceeded the maximum 60 characters. |
| INVALID\_ENTITY\_TYPE | The provided key does not match the regex: `/^(?![\.\-])(?!.*\.{2})[a-z0-9:\-.]*(?<![.])$/`. |
| INVALID\_ENTITY\_VALUE | Entity values must match one of the types defined in [Custom Entities](/platform/forge/runtime-reference/custom-entities/#values). |
| INVALID\_ENTITY\_ATTRIBUTE | The specified attribute name is a reserved value and cannot be utilized. |
| INVALID\_ENTITY\_INDEX | The custom entity index provided is invalid. The index name is a reserved value and cannot be utilized. |

| Error code | Description |
| --- | --- |
| INVALID\_FILTER\_CONDITION | The specified condition is not supported for filters. |
| INVALID\_FILTER\_VALUES | The specified number of values are not supported by the given condition. |
| LIST\_QUERY\_LIMIT\_EXCEEDED | Limit for list query should be below 100. |
| QUERY\_WHERE\_INVALID | KVS queries should contain only a single "where" clause. |
| QUERY\_WHERE\_FIELD\_INVALID | The specified field is not supported for filters. |

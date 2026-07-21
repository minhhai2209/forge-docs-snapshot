# License API

You can retrieve license information for your Forge app through the License REST API. You can also query the license of other apps, provided both caller and queried apps belong to the same developer space and share the same environment (`environmentType` and `environmentKey`).

No OAuth 2.0 scopes are required.

To query your own app's license status, make sure `licensing.enabled` is set to `true` in your [app manifest](/platform/forge/manifest-reference/#app).
For an overview of billing models, see [Billing models](/platform/forge/licensing-overview/).

## requestAtlassian

The Forge SDK code examples on this page use the `requestAtlassian` module, which is available from the `@forge/api` package.
This package module uses the app's credentials, determined by the scopes defined in the app's manifest.

## Get app licenses

Send a `GET` request to `/forge/app/v1/license` to retrieve license information for one or more apps on the current site.

If `appId` is not provided, the request falls back to the calling app (self-query). For explicit `appId` queries, all apps must share the same developer space as the caller and match the caller environment (`environmentType` + `environmentKey`).

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `appId` | `string (UUID)` | No | The target app ID(s) to query. Repeat the query parameter to request multiple apps (maximum 10). If omitted, queries the calling app's own license. |

### Code examples

Forge

Forge (multiple apps)

Node.js

```
```
1
2
```



```
import { asApp } from '@forge/api';

// Self-query: retrieve the calling app's own license
const response = await asApp().requestAtlassian(`/forge/app/v1/license`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'GET'
});
const body = await response.json();
console.log(`Response: ${response.status}`, body);
```
```

### Responses

#### 200: OK

License information was successfully retrieved for the requested app(s). The `results` array contains one entry per requested app — each entry is either a successful license payload or an error payload for that app.

##### Response schema

| Property | Type | Description |
| --- | --- | --- |
| `results` | `array` | Per-app results for the query. Each item is either a `LicenseQueryResult` or a `LicenseQueryError`. |

**LicenseQueryResult** (success per app):

| Property | Type | Description |
| --- | --- | --- |
| `appId` | `string (UUID)` | The app ID for this result. |
| `data` | `object` | License information for the queried app. When no license exists, an empty object is returned. See [License record properties](#license-record-properties) below. |

**LicenseQueryError** (error per app):

| Property | Type | Description |
| --- | --- | --- |
| `appId` | `string (UUID)` | The app ID for this error result. |
| `error.type` | `string` | The error type. |
| `error.message` | `string` | A description of the error for this specific app. |

**License record properties** (`data`):

| Property | Type | Description |
| --- | --- | --- |
| `active` | `boolean` | Whether the license is currently active. |
| `type` | `string | null` | Type of license. Currently `"commercial"` or `null`. |
| `isEvaluation` | `boolean` | Whether the license is a trial/evaluation license. |
| `trialEndDate` | `string (date-time)` | The date and time when the trial period ends, if applicable. |
| `subscriptionEndDate` | `string (date-time)` | The date and time when the subscription ends, if applicable. |
| `billingPeriod` | `string` | The billing period for the license (for example, `"MONTHLY"` or `"ANNUAL"`). |
| `supportEntitlementNumber` | `string | null` | The support entitlement number associated with the license. |
| `ccpEntitlementId` | `string` | The CCP entitlement ID associated with the license. |
| `ccpEntitlementSlug` | `string` | The CCP entitlement slug associated with the license. |
| `capabilitySet` | `string` | The capability set granted by this license. |

##### Example

```
```
1
2
```



```
{
  "results": [
    {
      "appId": "35559c21-6120-406b-b7cd-d87f468f6d32",
      "data": {
        "active": true,
        "type": "commercial",
        "isEvaluation": false,
        "trialEndDate": null,
        "subscriptionEndDate": "2027-01-01T00:00:00.000Z",
        "billingPeriod": "ANNUAL",
        "supportEntitlementNumber": "SEN-12345678",
        "ccpEntitlementId": "ent-abc123",
        "ccpEntitlementSlug": "my-app-commercial",
        "capabilitySet": "capabilityAdvanced"
      }
    },
    {
      "appId": "11259c21-6120-406b-b7cd-d87f468f6d99",
      "error": {
        "type": "NOT_FOUND",
        "message": "No license found for this app on the current site"
      }
    }
  ]
}
```
```

#### 4XX Error codes

400: Bad Request

403: Forbidden

429: Too Many Requests

The request contains invalid query parameters.

##### Example

```
```
1
2
```



```
{
  "code": 400,
  "message": "Invalid appId format"
}
```
```

#### 500: Internal Server Error

The License service encountered an unexpected problem.

```
```
1
2
```



```
{
  "code": 500,
  "message": "An internal error occurred"
}
```
```

## Remote compatibility

You can call the License REST API from a remote backend. For more information, see [Calling Atlassian app APIs from a remote](/platform/forge/remote/calling-product-apis/), and the API endpoint is `https://api.atlassian.com/forge/app/v1/license`.

## Rate limit

| Scope | Limit |
| --- | --- |
| Per caller `installationId` | 1 request per 5 minutes |
| Per tenant | 10 requests per minute |

Because all apps on the same tenant share the per-tenant limit, your app may hit a `429 Too Many Requests` response even if it hasn't reached the per-installation limit. When this happens, wait for the number of seconds specified in the `Retry-After` response header before retrying.

We recommend caching license data and using a much lower frequency than the hard limit — for example, **once per hour per `installationId`**. If you receive a `429` response, retry with exponential back-off and jitter.

# Dynamic Modules API (EAP)

Forge Dynamic Modules is now available as part of Forge’s Early Access Program (EAP).
To start testing this, sign up [here](https://ecosystem.atlassian.net/servicedesk/customer/portal/3595).

EAP features and APIs are unsupported, and subject to change without notice. Apps that use dynamic modules should not be deployed to `production` environments.

All dynamic modules created during EAP will not be carried over to Preview. For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

You can manage [Dynamic Modules](/platform/forge/apis-reference/dynamic-modules/) through its REST API.
This API checks every request for OAuth authorisation to determine if it has permissions to access the
target installation.

No OAuth 2.0 scopes are required.

## Remote compatibility

You can configure a remote backend to call the Dynamic Module REST API. See
[Calling Atlassian app APIs from a remote](/platform/forge/remote/calling-product-apis/).

[Remote](/platform/forge/remote/) backends can only use `asApp` calls for dynamic module operations; `asUser` calls are not allowed. This means your remote backend will only be able to call the Dynamic Modules API as a generic bot user.

## requestAtlassian

The Forge SDK code examples on this page use the `requestAtlassian` module, which is available from the `@forge/api` package.
This package module uses the app's credentials, determined by the scopes defined in the app's manifest.

## Register a dynamic module

Send a `POST` request to `/forge/installation/v1/dynamic/module` to register a dynamic module for the current app installation.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the target dynamic module on the installation |
| `type` | `string` | Yes | The dynamic module being created (for example, use `trigger` to specify the [Trigger](/platform/forge/manifest-reference/modules/trigger/) module) |
| `data` | `map` | Yes | The dynamic module's structure, but in JSON format (the `payload`s in the [Code examples](#post-example) use the [Trigger](/platform/forge/manifest-reference/modules/trigger/) module). The `key` property will be automatically copied into this payload so does not need to be provided again. |

### Code examples

```
```
1
2
```



```
import { requestAtlassian } from "@forge/api";
const payload = {
  key: "unique-module-key",
  type: "trigger",
  data: {
    events: [
      "avi:jira:updated:issue"
    ],
    "endpoint": "some-endpoint"
  }
}
const response = await requestAtlassian(`/forge/installation/v1/dynamic/module/`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'POST',
  body: JSON.stringify(payload),
});
const body = await response.text(); 
console.log(`Response: ${response.status} ${body}`);
```
```

### Responses

#### 201: OK

The dynamic module was successfully registered on the installation.

#### 4XX Error codes

401: Unauthorized

422: Unprocessable

429: Too Many Requests

The request does not have permissions to access the target installation.

##### Example

```
```
1
2
```



```
{
  "message": "Authorization failed"
}
```
```

#### 500: Internal Server Error

The Dynamic Module service encountered an unexpected problem.

```
```
1
2
```



```
{
  "message": "An internal error occurred"
}
```
```

## Update a registered module

Send a `PUT` request to `/forge/installation/v1/dynamic/module/<key>` to update a dynamic module registered on the installation
(identified by the module's `key`).

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the target dynamic module on the installation |
| `dynamicModuleRequest` | `map` | Yes | Payload that defines the updated dynamic module |

The `dynamicModuleRequest` property requires the same properties as the [registration request](#register-a-dynamic-module), as in:

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the target dynamic module on the installation |
| `type` | `string` | Yes | The dynamic module being created (for example, use `trigger` to specify the [Trigger](/platform/forge/manifest-reference/modules/trigger/) module) |
| `data` | `map` | Yes | The dynamic module's structure, but in JSON format (the `payload`s in the [Code examples](#put-example) use the [Trigger](/platform/forge/manifest-reference/modules/trigger/) module). The `key` property will be automatically copied into this payload so does not need to be provided again. |

### Code examples

```
```
1
2
```



```
import { requestAtlassian } from "@forge/api";
const key = "unique-module-key";
const payload = {
  key: "unique-module-key",
  type: "trigger",
  data: {
    events: [
      "avi:jira:updated:issue"
    ],
    "endpoint": "some-endpoint"
  }
}
const response = await requestAtlassian(`/forge/installation/v1/dynamic/module/${key}`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'PUT',
  body: JSON.stringify(payload)
});
const body = await response.text(); 
console.log(`Response: ${response.status} ${body}`);
```
```

### Responses

#### 200: OK

The taget dynamic module was successfully updated. The response will contain the payload of the updated dynamic module.

##### Example

```
```
1
2
```



```
{
  "key": "unique-module-key",
  "type": "trigger",
  "data": {
    "key": "unique-module-key",
    "events": [
      "avi:jira:updated:issue"
    ],
    "endpoint": "some-endpoint"
  }
}
```
```

#### 4XX Error codes

400: Bad Request

401: Unauthorized

404: Not Found

422: Unprocessable

429: Too Many Requests

The specified key does not match the key specified in the `dynamicModuleRequest` map.

##### Example

```
```
1
2
```



```
{
  "message": "Key cannot be modified during update"
}
```
```

#### 500: Internal Server Error

The Dynamic Module service encountered an unexpected problem.

```
```
1
2
```



```
{
  "message": "An internal error occurred"
}
```
```

## List registered modules

Send a `GET` request to `/forge/installation/v1/dynamic/module/` to retrieve a *paginated list* of dynamic modules currently registered on the app installation.

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `nextPageToken` | `string` | No | Pagination cursor for fetching subsequent dynamic modules. This field is only present in a response if a *strict subset* of dynamic modules was previously fetched from this installation. |
| `limit` | `integer` | No | Maximum number of dynamic modules to return |

### Code examples

```
```
1
2
```



```
import { requestAtlassian } from "@forge/api";
const params = new URLSearchParams({
  limit: '10',
  nextPageToken: '<PAGINATION-TOKEN>'
}).toString();
const response = await requestAtlassian(`/forge/installation/v1/dynamic/module/?${params}`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'GET'
});
const body = await response.text(); 
console.log(`Response: ${response.status} ${body}`);
```
```

### Responses

#### 200: OK

Dynamic modules were successfully fetched.

##### Example

```
```
1
2
```



```
{
  "key": "a-dynamic-module",
  "type": "trigger",
  "data": {
    "key": "a-dynamic-module",
    "function": "jira-updated-issue-handler",
    "events": [
      "avi:jira:updated:issue"
    ]
  }
},
{
  "key": "another-dynamic-module",
  "type": "trigger",
  "data": {
    "filter": {
      "expression": "event.issue.fields?.issuetype.name == 'Bug'",
      "onError": "RECEIVE_AND_LOG"
    },
    "key": "another-dynamic-module",
    "endpoint": "some-endpoint",
    "events": [
      "avi:jira:updated:issue"
    ]
  }
}
```
```

#### 4XX Error codes

401: Unauthorized

422: Unprocessable

429: Too Many Requests

The request does not have permissions to access the target installation.

##### Example

```
```
1
2
```



```
{
  "message": "Authorization failed"
}
```
```

#### 500: Internal Server Error

The Dynamic Module service encountered an unexpected problem.

```
```
1
2
```



```
{
  "message": "An internal error occurred"
}
```
```

## Retrieve a registered module

Send a `GET` request to `/forge/installation/v1/dynamic/module/<key>` to retrieve a registered dynamic module on the installation
(identified by the module's `key`).

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the target dynamic module on the installation |

### Code examples

```
```
1
2
```



```
import { requestAtlassian } from "@forge/api";
const key = '<YOUR-MODULE-KEY>';
const response = await requestAtlassian(`/forge/installation/v1/dynamic/module/${key}`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'GET'
});
const body = await response.text(); 
console.log(`Response: ${response.status} ${body}`);
```
```

### Responses

#### 200: OK

The specified dynamic module was successfully fetched.

##### Example

```
```
1
2
```



```
{
  "key": "a-dynamic-module",
  "type": "trigger",
  "data": {
    "key": "a-dynamic-module",
    "events": [
      "avi:confluence:viewed:page"
    ],
    "function": "confluence-viewed-handler"
  }
}
```
```

#### 4XX Error codes

401: Unauthorized

404: Not Found

429: Too Many Requests

The request does not have permissions to access the target installation.

##### Example

```
```
1
2
```



```
{
  "message": "Authorization failed"
}
```
```

#### 500: Internal Server Error

The Dynamic Module service encountered an unexpected problem.

```
```
1
2
```



```
{
  "message": "An internal error occurred"
}
```
```

## Delete a registered module

Send a `DELETE` request to `forge/installation/v1/dynamic/module/<key>` to delete a registered dynamic module on the installation
(identified by the module's `key`).

### Request

| Property | Type | Required? | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The unique key of the target dynamic module on the installation |

### Code examples

```
```
1
2
```



```
import { requestAtlassian } from "@forge/api";
const moduleKey = '<YOUR-MODULE-KEY>';
const response = await requestAtlassian(`/forge/installation/v1/dynamic/module/${moduleKey}`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'DELETE'
});
console.log(`Response: ${response.status}`);
```
```

### Responses

#### 204: No Content

No content will be returned if the target dynamic module was successfully deleted.

#### 4XX Error codes

401: Unauthorized

404: Not Found

429: Too Many Requests

The request does not have permissions to access the target installation.

##### Example

```
```
1
2
```



```
{
  "message": "Authorization failed"
}
```
```

#### 500: Internal Server Error

The Dynamic Module service encountered an unexpected problem.

```
```
1
2
```



```
{
  "message": "An internal error occurred"
}
```
```

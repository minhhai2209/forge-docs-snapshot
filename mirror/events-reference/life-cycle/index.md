# Life cycle events

Forge apps can subscribe to their own life cycle events for:

Events are passed to your app via the `event` parameter.

```
1
2
3
4
export async function handleEvent(event, context) {
  console.log(`Event received: ${JSON.stringify(event)}`);
  console.log(`Context: ${JSON.stringify(context)}`);
}
```

### Arguments

* **event:** a payload detailing the event. See the documentation for an event for a detailed description of its payload.
* **context:** additional information about the context the event occurred in. Please refer to [Context Schema](/platform/forge/function-reference/arguments/#context-schema) for more details.

## Installation

An event with the name `avi:forge:installed:app` is sent when an app has been installed on a site.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| id | `string` | The ID of the installation. |
| installerAccountId? | `string` | [Optional] The ID of the user who installed the Forge app.     In Jira and Confluence apps, use the Get user operation of [Jira](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-get) or [Confluence](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-users/#api-wiki-rest-api-user-get) REST APIs to retrieve user information.     In Bitbucket apps, use [requestGraph](/platform/forge/apis-reference/fetch-api-product.requestgraph/) and [user query](/platform/atlassian-graphql-api/graphql/#identity_user) to retrieve user information. |
| app | `App` | An object describing the Forge app. |
| environment? | `Environment` | [Optional] An object containing the Forge app's environment id. |

### Type reference

```
```
1
2
```



```
interface App {
  id: string;
  version: string;
  name?: string;
  ownerAccountId?: string;
}

interface Environment {
  id: string;
}
```
```

### Example

This is an example payload.

```
```
1
2
```



```
{
  "id": "fff8e466-31f4-4c73-a337-c3309dd930dc",
  "installerAccountId": "4ad9aa0c52dc1b420a791d12",
  "app": { 
    "id": "406d303d-0393-4ec4-ad7c-1435be94583a", 
    "version": "9.0.0",
    "ownerAccountId": "3bc8aa0c52dc1b310a791d34",
    "name": "My App Name",
  },
  "environment": {
    "id": "23863033-1de4-4ebf-b30d-c906264a1e92"
  },
}
```
```

### Making API requests during installation

During app installation, the Atlassian account used by your app to authenticate with Atlassian APIs is granted various permissions and group memberships for the site it is being installed into. This process is eventually consistent, and the `installed` event may be sent before the app is granted the permissions needed to call certain APIs using `.asApp()`. For large sites, it may take a very long time (minutes) for your app user to be fully granted the requisite permissions.

As such, we recommend coding defensively when using `.asApp()` in an `installed` trigger. If you receive an unexpected authorisation error when calling an Atlassian API (typically a 401 or 403 HTTP status code), you should use Forge's [retry handling](/platform/forge/events-reference/product_events/#1--retry-for-app-level-errors) to reattempt the request after a delay.

Here is a simple `installed` trigger that uses an exponential back-off strategy to retry if an authorisation error is encountered:

```
```
1
2
```



```
import { InvocationError, InvocationErrorCode } from "@forge/events";

export async function handleInstalledEvent(event, context) {
  // When making an API call as the app in an `avi:forge:installed:app` event handler ... 
  const response = await api.asApp().requestJira(/* ... */);

  // ... a 401 or 403 may mean that the app's Atlassian account isn't yet fully initialised ...
  if (response.status === 401 || response.status === 403) {
    // ... so we retry after a delay
    const retryCount = event.retryContext?.retryCount || 1; // Forge will retry up to 4 times
    const retryDelay = Math.pow(5, retryCount); // Exponential backoff up to 5^4 seconds ~= 10 minutes
    console.log(`Auth error during initialisation, retrying in ${retryDelay} seconds.`);
    
    return new InvocationError({
      retryAfter: retryDelay,
      retryReason: InvocationErrorCode.FUNCTION_RETRY_REQUEST
    });
  }
}
```
```

## Upgrade

An event with the name `avi:forge:upgraded:app` is sent when an installed app on a site has been upgraded to a new major version. This event is not sent for minor or patch version upgrades.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| id | `string` | The ID of the installation. |
| upgraderAccountId? | `string` | [Optional] The ID of the user who upgraded the Forge app.     In Jira and Confluence apps, use the Get user operation of [Jira](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-get) or [Confluence](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-users/#api-wiki-rest-api-user-get) REST APIs to retrieve user information.     In Bitbucket apps, use [requestGraph](/platform/forge/apis-reference/fetch-api-product.requestgraph) and [user query](/platform/atlassian-graphql-api/graphql/#identity_user) to retrieve user information. |
| app | `App` | An object describing the Forge app. |
| environment? | `Environment` | [Optional] An object containing the Forge app's environment id. |

### Type reference

```
```
1
2
```



```
interface App {
  id: string;
  version: string;
  name?: string;
  ownerAccountId?: string;
}

interface Environment {
  id: string;
}
```
```

### Example

This is an example payload.

```
```
1
2
```



```
{
  "id": "fff8e466-31f4-4c73-a337-c3309dd930dc",
  "upgraderAccountId": "4ad9aa0c52dc1b420a791d12",
  "app": { 
    "id": "406d303d-0393-4ec4-ad7c-1435be94583a", 
    "version": "9.0.0",
    "ownerAccountId": "3bc8aa0c52dc1b310a791d34",
    "name": "My App Name",
  },
  "environment": {
    "id": "23863033-1de4-4ebf-b30d-c906264a1e92"
  },
}
```
```

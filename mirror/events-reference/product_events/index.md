# Atlassian app events

## Atlassian app events

Atlassian app events are generated when users perform actions in Atlassian apps. Apps can subscribe
to a list of Atlassian app events using a [trigger](/platform/forge/manifest-reference/modules/trigger)
in the manifest.

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

Forge apps can receive Atlassian app events from both public and restricted Jira projects and Confluence spaces.

When handling events, you can make API calls using either:

* `asApp()` - The app will have access to all data it has permissions for, regardless of restrictions
* `asUser(accountId)` - The app will have access only to the data that the specified user can access. This requires:
  * Retrieving the user's accountId from the event payload (e.g., `event.atlassianId`)
  * Declaring `allowImpersonation: true` for the required scopes in your manifest

See [Jira authentication](/platform/forge/apis-reference/fetch-api-product.requestjira/) for details on offline user impersonation.

### Arguments

* **event:** a payload detailing the event. See the documentation for an event for a detailed description of its payload.
* **context:** additional information about the context the event occurred in. Please refer to [Context Schema](/platform/forge/function-reference/arguments/#context-schema) for more details.

## Retry Atlassian app events

There are two types of retry events:

1. Retry app level errors
2. Retry platform level errors

Install the latest Forge events package by running:
`npm i @forge/events`

### 1. Retry for app level errors

You can request a retry for an Atlassian app event trigger by returning an `InvocationError` object. This is defined in the `@forge/events` package

You can only retry an event for a maximum of **four** times.

Additional options can be included in the `InvocationError` via a `RetryOptions` object, allowing you to provide more information about what went wrong and configure the retry.

**Event payload schema**

```
```
1
2
```



```
RetryOptions {
  retryAfter: number // retry trigger after in seconds
  retryReason: InvocationErrorCode // reason why the error occurred
  retryData: any // additional data to assist retry logic
}

enum InvocationErrorCode {
  // There was a rate limit upstream that caused the Application to fail.
  FUNCTION_UPSTREAM_RATE_LIMITED = "FUNCTION_UPSTREAM_RATE_LIMITED",
  // Some application level error occurred and a retry is warranted
  FUNCTION_RETRY_REQUEST = "FUNCTION_RETRY_REQUEST"
}
```
```

**retryAfter limitation**

The maximum `retryAfter` value is `900` seconds (15 minutes). Any `retryAfter` values exceeding this limit are lowered to `900` seconds.

**retryData limitation**

The maximum `retryData` size is 4KB. This will be enforced from `Nov 13, 2025`.

Because of the bug ([ECO-734](https://jira.atlassian.com/browse/ECO-734)), `retryData` should be of an object type, otherwise it is not sent on retry.

**retryReason values**

| Value | Description |
| --- | --- |
| FUNCTION\_UPSTREAM\_RATE\_LIMITED | Rate limit upstream that caused the app to fail |
| FUNCTION\_RETRY\_REQUEST | Unclassified error occurred during the app that the developer would like to retry |

**Example for requesting a retry**

In the following sample code, the app calls an upstream Jira API and is rate limited. A retry is requested with a timeout that is equal to the backoff time provided by the Jira API and the retry reason is `FUNCTION_UPSTREAM_RATE_LIMITED` as there was an upstream dependency that was rate limited.

```
```
1
2
```



```
import {InvocationError, InvocationErrorCode} from '@forge/events'
import {asApp, route} from '@forge/api'

export async function run(event, context) {
  const userName = 'john';
  const response = await asApp().requestJira(route`/rest/api/3/user/search?query=${userName}`, {
    headers: {
      'Accept': 'application/json'
    }
  });

  if(response.headers.has('Retry-After')){
    return new InvocationError({

      // The App can request the retry to happen after a certain time period elapses

      retryAfter: parseInt(response.headers.get('Retry-After')),

      // The App should provide a reason as to why they are retrying.

      // This reason will be feedback to the event payload on the retry

      // and is to help the developer discern the initial failure reason.

      retryReason: InvocationErrorCode.FUNCTION_UPSTREAM_RATE_LIMITED,
      retryData: {
        userName: userName
      }
    });
  }
}
```
```

**Example for handling a retry**

In the following sample code the app checks whether or not the `retryContext` field
exists in the event payload. If it exists, it means that the app is currently handling
a retry and the app can handle the retry accordingly. The app can request another retry
if another retryable error occurs, but note that the event can only be retried up to **4** times.

**Properties**

There will be one extra object `retryContext` in the event payload for a retry. This object contains three properties:

* `retryCount`: number of times (max 4) the app requested for retry
* `retryReason:` reason why the error occurred
* `retryData`: additional data to assist retry logic

`retryReason` and `retryData` will be populated with the same values as were given when requesting the retry with `InvocationError`.

```
```
1
2
```



```
import { RetryOptions, InvocationError, InvocationErrorCode } from "@forge/events"

export async function onIssueCreated(event, context) {
  try {
    // retryContext will be populated if this is a retry
    if (event.retryContext) {
      const { retryCount, retryReason, retryData } = event.retryContext;
      handleRetry(retryCount, retryReason, retryData, event);
    }
    else {
      handleEvent(event);
    }
  } catch(error) {
    // If the event is retryable, the App can request for another retry
    // although, note that the maximum number of retries is 4 
    if (e instanceof RetryableException) {
      const retryOptions: RetryOptions = {
        retryAfter: calculateBackOffTime(event.retryContext),
        retryReason: InvocationErrorCode.FUNCTION_RETRY_REQUEST,
        retryData: getRetryData(e, event)
      }
      return new InvocationError(retryOptions);
    }
  }
}
```
```

### 2. Retry for platform level errors

Platform level errors cannot be captured by the app. Examples include timeouts and Out of memory(OOM) errors. If a platform error occurs, the Forge platform will automatically retry the event on behalf of you.

**retryReason values**

| Value | Description |
| --- | --- |
| FUNCTION\_OUT\_OF\_MEMORY | The function ran out of memory (allocated by Forge Platform/Lambda) in the previous attempt |
| FUNCTION\_TIME\_OUT | The function timed out during the previous attempt |
| FUNCTION\_PLATFORM\_RATE\_LIMITED | An infrastructure Quota/Rate Limit occurred during the previous attempt at running the function |
| FUNCTION\_PLATFORM\_UNKNOWN\_ERROR | An undefined error occurred during the previous attempt at running the function |

## Filter out Atlassian app events

Forge apps subscribed to a list of [Atlassian app events](/platform/forge/events-reference/product_events) can now declare
an `expression` property in the [filter](/platform/forge/manifest-reference/modules/trigger/#filter-reference) property
in each of the [trigger](/platform/forge/manifest-reference/modules/trigger) module definitions in
the [manifest](/platform/forge/manifest-reference) to specify which events they should receive.

### Expressions language

You can build event filtering expressions using the following subset of
the [Jira expressions language](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/):

Expressions used in event filtering support only the
following [expressions types](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference):

### Filtering out events with expressions

The content of the event payload is accessible under the `event` variable that is
a [Map](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#map) type. Please refer to
the event payload documentation to understand the exact structure of the `event` variable for each event type.

Note that type references defined for events on the mentioned paged are not translated to types in expressions
language. This means that you should treat the type reference values as one of the supported expression types.

The expression has to evaluate to the
[`Boolean` type](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference/#boolean)
to filter out events. If the expression evaluates to `true`, the event will be delivered to the app. If the expression
evaluates to `false`, the event will be filtered out and dropped. Any other evaluation outcome will be considered
an error and result in the event being filtered out. This includes scenarios like performing mathematical operations
on non-compatible types or accessing object properties that aren’t defined in the event payload.

You can use the [Expressions playground](/platform/forge/events-reference/expressions-playground/) to test your
event filtering expressions against the provided payload.

A log will be shown in the [developer console](https://developer.atlassian.com/console/myapps) in case of such errors.
Note that those messages will not be logged in the [Forge CLI](/platform/forge/cli-reference) while [tunneling](/platform/forge/tunneling);
they're visible only in the [app logs](/platform/forge/view-app-logs).

### Error handling

You can specify what should happen when an error occurs while evaluating the expression using the
[`onError` property](/platform/forge/manifest-reference/modules/trigger/#filter-reference).

You can also use the
[runtime error handling](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#runtime-error-handling),
available in expressions to return a custom error message that will be shown in logs.

```
```
1
2
```



```
modules:
  trigger:
    events:
      filter:
        # actual expression to evaluate: "event.issue.fields?.issueType.name == 'Bug'"
        expression: |
          try {
            return event.issue.fields?.issueType.name == 'Bug';
          } catch (e) {
            throw `Unexpected error: "${e.location}" - ${e.message}.`;
          }
        # log error message in case of failure and receive event
        onError: RECEIVE_AND_LOG
```
```

### Restrictions

Some restrictions apply to expressions. While the limits are high enough not to interfere with any intended usage,
it's important to realize that they do exist.

Expressions have to use the
correct [syntax and semantics](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#syntax-and-semantics)
and contain at most 10,000 characters.

While in the [Jira expressions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/) the restrictions
are based on the number of
the [expensive operations](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#expensive-operations),
in expressions used in event filtering, restrictions are based on the approximate number of all operations performed
during the evaluation. Expressions may execute up to 50,000 steps, where a step is any of the high-level operations,
such as arithmetic, accessing a property, accessing a variable, or calling a function.

To verify the complexity of the expression, the [Forge CLI](/platform/forge/cli-reference) will analyze the expression
before the [app deployment](/platform/forge/cli-reference/deploy). If the analysis shows the expression is too complex,
the deployment will fail.

The error will contain information about the estimated complexity to help with the simplification process. An example
analysis will look similar to the following example: `N*M*L*K + 5*N*M*L + 10*N*M + 15*N + 20`, where:

* `N`, `M`, `L`, and `K` are the inferred variables used in the expression
* `N*M*L*K`, `5*N*M*L`, `10*N*M`, `15*N` are the estimated number of operations performed per each variable combination
* `20` is the constant number of all other operations performed during the evaluation

The restrictions for the analysis are based on the following limits:

* up to 3 inferred variables allowed
* up to 3 variable combinations allowed
* up to 3 variables in a single variable combination allowed
* up to 10,000 as a constant number of all other operations allowed

### Limitations

Currently, expressions used in event filtering don't support the
following [Jira expressions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/)
features:

### Example

To filter out all the Jira issue events where the issue type is a bug, we should check it this data is available in
the event payload of the [Jira issue events](/platform/forge/events-reference/jira/#issue-events).

By looking at the type reference of the [Jira issue event](/platform/forge/events-reference/jira/#type-reference),
we can see that the `issue` object has a `fields` object that may contain the `issueType` object.

```
```
1
2
```



```
interface Issue {
  id: string;
  key: string;
  fields: {
    issueType?: any;
    // (... other fields ...)
  };
}

// (other types...)
```
```

By looking at
the [example of the payload](https://developer.atlassian.com/platform/forge/events-reference/jira/#example), the data
for issue type is available under the `issue.fields.issueType.name` path.

```
```
1
2
```



```
{
  "issue": {
    "fields": {
      "issuetype": {
        "self": "https://example.atlassian.net/rest/api/2/issuetype/10001",
        "id": "10001",
        "description": "Functionality or a feature expressed as a user goal.",
        "iconUrl": "https://example.atlassian.net/secure/viewavatar?size=medium&avatarId=10315&avatarType=issuetype",
        "name": "Story",
        "subtask": false,
        "avatarId": 10315
      },
      (...
      other
      issue
      fields
      ...)
    }
  },
  (...
  other
  fields
  ...)
}
```
```

Since the event payload is available in the `event` variable as
a [Map](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#map) type, we have to use
`event.issue.fields?.issueType.name == 'Bug'` as the expression.

The [trigger](/platform/forge/manifest-reference/modules/trigger) module definition in
the [manifest](/platform/forge/manifest-reference) should look like this:

```
```
1
2
```



```
modules:
  trigger:
    - key: jira-issue-trigger-filtering-by-expression-for-bug-issue-type
      function: main
      events:
        - avi:jira:created:issue
        - avi:jira:updated:issue
        - avi:jira:deleted:issue
        - avi:jira:assigned:issue
        - avi:jira:viewed:issue
        - avi:jira:mentioned:issue
      filter:
        expression: "event.issue.fields?.issueType.name == 'Bug'"
  function:
    - key: main
      handler: index.run
```
```

After the app is deployed, events whose payload have `Bug` as the issue type will be delivered and trigger the `main`
function. For other and undefined issue types, events will be filtered out.

## OAuth 2.0 scopes

When using Atlassian app events, your Forge app must have permission from the site admin to access
the data it provides within the event payload. The OAuth scope required is documented under
each Atlassian app event. Note, running the `forge lint` command picks up these required scopes.

See [Permissions](/platform/forge/manifest-reference/permissions/)
for detailed information about each scope.
See [Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api)
to add new scopes to your app.

## Known issues

* Atlassian app events larger than 200 kB are not delivered. This limit may change without notice.

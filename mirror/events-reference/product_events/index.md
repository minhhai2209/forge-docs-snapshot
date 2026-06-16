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
import { RetryOptions, InvocationError, InvocationErrorCode } from '@forge/events'

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
    if (error instanceof RetryableException) {
      const retryOptions: RetryOptions = {
        retryAfter: calculateBackOffTime(event.retryContext),
        retryReason: InvocationErrorCode.FUNCTION_RETRY_REQUEST,
        retryData: getRetryData(error, event)
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

## Filtering by entity properties

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge apps can also filter events based on [entity properties](/cloud/jira/platform/jira-entity-properties/) and
enrich event payloads with selected entity property values.

### Manifest syntax

Use the `filter.expression` field to filter events by entity property values, and the
`payload.include.propertyPaths` field to include entity property values in the delivered event payload.

```
```
1
2
```



```
modules:
  trigger:
    - key: issue-updated-trigger
      function: main
      events:
        - avi:jira:updated:issue
      filter:
        expression: |
          event.runtime.project.properties['myapp'].status == 'active'
          && event.runtime.issue.properties['myapp'].type == 'bug'
      payload:
        include:
          propertyPaths: ["project.properties['myapp'].status", "issue.properties['myapp'].type"]
```
```

#### Key points about the syntax

1. **Filter expressions**: Entity property paths in filter expressions must be prefixed with `event.runtime.`
   (for example, `event.runtime.issue.properties['key'].field`). Sub-paths can use dot notation (`.field`) or
   bracket notation (`['field']`). For example, `event.runtime.issue.properties['myapp']['type']` is equivalent
   to `event.runtime.issue.properties['myapp'].type`.
2. **Payload enrichment**: Paths in the `payload.include.propertyPaths` section do **not** use the
   `event.runtime` prefix — they use the entity directly (for example, `issue.properties['key'].field`).
3. **Independence**: Filtering and enrichment are independent — a property used in a filter expression is
   **not** automatically included in the payload. You must explicitly add it to `propertyPaths` if you also
   want it in the delivered payload.
4. **Unresolvable properties**: A property that cannot be resolved at runtime will have its value set to
   `null`. Your manifest will pass validation even if entity property paths are wrong, but things may fail
   at runtime.
5. **Nested object resolution**: Paths must resolve to a **primitive value or an array of primitives**. If a
   path resolves to a nested object, the value will be `null`. You must provide the full path to the specific
   value you need.

   For example, given an entity property with key `some-property`:

   ```
   ```
   1
   2
   ```



   ```
   {
       "x": {
           "y": {
               "z": true
           }
       }
   }
   ```
   ```

   * `event.runtime.issue.properties['some-property'].x` → `null` (resolves to an object)
   * `event.runtime.issue.properties['some-property'].x.y.z` → `true` (resolves to a primitive value)
   * `event.runtime.issue.properties['some-property']['x.y.z']` → `true` (bracket notation equivalent)
   * Paths that resolve to an **array of primitives** support expression operations under parentheses. For
     example:

     ```
     ```
     1
     2
     ```



     ```
     filter:
       expression: (event.runtime.issue.properties['some-array-property'].strings).length > 0
     ```
     ```
6. **Root-level property access**: If the entity property value itself is a primitive (string, number,
   boolean), you can access it directly without a sub-path. For example,
   `event.runtime.project.properties['myPropertyKey']` works when the stored value is a primitive.

### Delivered payload shape

When `payload.include.propertyPaths` is configured, the resolved values are delivered on the `event`
object inside your trigger function under the top-level `payloadIncludeProperties` field. Each path you
declared in `payload.include.propertyPaths` appears as a key (a string), with the resolved value as the
corresponding value.

For example, given the manifest from the [Manifest syntax](#manifest-syntax) section above, your function
receives an event that contains:

```
```
1
2
```



```
{
  "payloadIncludeProperties": {
    "project.properties['myapp'].status": "active",
    "issue.properties['myapp'].type": "bug"
  }
}
```
```

You can access these values in your function like this:

```
```
1
2
```



```
export async function main(event, context) {
  // Entity property values resolved at event time
  const projectStatus = event.payloadIncludeProperties["project.properties['myapp'].status"]; // e.g. 'active'
  const issueType     = event.payloadIncludeProperties["issue.properties['myapp'].type"];     // e.g. 'bug'
}
```
```

If a path cannot be resolved (for example, the property doesn't exist on that entity), the value will be absent.

### Supported entities

Entity property filtering and enrichment currently supports properties on three Jira entity types:

| Entity | Expression path example |
| --- | --- |
| **Issue** | `event.runtime.issue.properties['key'].path` |
| **Project** | `event.runtime.project.properties['key'].path` |
| **User** | `event.runtime.user.properties['key'].path` |

### Supported events

Entity property filtering and enrichment is supported for the following Jira Forge events:

* `avi:jira:created:issue`
* `avi:jira:updated:issue`
* `avi:jira:deleted:issue`
* `avi:jira:commented:issue`
* `avi:jira:deleted:comment`
* `avi:jira:created:worklog`
* `avi:jira:updated:worklog`
* `avi:jira:deleted:worklog`
* `avi:jira:created:issuelink`
* `avi:jira:deleted:issuelink`
* `avi:jira:created:attachment`
* `avi:jira:deleted:attachment`
* `avi:jira:assigned:issue`

For `issuelink` events, filtering is based on the **source** issue or project properties.

### Limits and constraints

| Constraint | Limit |
| --- | --- |
| **Distinct entity property paths** across all `trigger` modules in a single app manifest, combined across filter expressions **and** `payload.include.propertyPaths` (deduplicated — the same path counts only once) | **5 paths total** |
| **Data freshness** | Filters are evaluated against recently stored entity property values that could be up to **a few seconds older** than the event generation time |
| **Processing overhead** | Triggers using runtime entity property filtering or enrichment involve additional processing time compared to triggers that do not use them |

#### Example of path counting

```
```
1
2
```



```
modules:
  trigger:
    # Trigger 1 — uses 2 paths in filter, 1 additional in payload = 3 paths
    - key: trigger-1
      function: main
      events:
        - avi:jira:updated:issue
      filter:
        expression: |
          event.runtime.project.properties['config'].status == 'active'    # Path 1
          && event.runtime.issue.properties['meta'].type == 'bug'          # Path 2
      payload:
        include:
          propertyPaths:
            - "project.properties['config'].status"   # Same as Path 1 — not counted again
            - "issue.properties['flags'].priority"    # Path 3

    # Trigger 2 — uses 1 additional path = 4 paths total
    - key: trigger-2
      function: main
      events:
        - avi:jira:updated:issue
      filter:
        expression: |
          event.runtime.user.properties['prefs'].role == 'admin'           # Path 4
  function:
    - key: main
      handler: index.run
```
```

In this example, **4 out of 5** allowed paths are used.

## Detect and filter self-generated events

When your app makes an API call that triggers an event your app is also subscribed to, the resulting
event is considered *self-generated*. Filtering out these events is important to prevent infinite
loops.

For example, if your app updates a Confluence page in response to a `page updated` event,
that update triggers another `page updated` event. Without filtering, your app would process its
own update, trigger yet another event, and repeat indefinitely.

To filter out self-generated events, set the
[`ignoreSelf` filter in your manifest](/platform/forge/manifest-reference/modules/trigger/#filter-reference).
This automatically discards self-generated events before your function is invoked:

```
```
1
2
```



```
modules:
  trigger:
    - key: my-trigger
      function: main
      events:
        - avi:confluence:updated:page
      filter:
        ignoreSelf: true
  function:
    - key: main
      handler: index.run
```
```

If you don't use the `ignoreSelf` filter, self-generated events will still be delivered to your
app with a `selfGenerated` property set to `true` in the event payload.

## Skip invocations for unlicensed apps

Set `filter.appIsLicensed` to `true` to skip trigger invocations for sites where the app does not have an active license. See the [filter reference](/platform/forge/manifest-reference/modules/trigger/#filter-reference) for more details.

```
```
1
2
```



```
modules:
  trigger:
    - key: my-trigger
      function: main
      events:
        - avi:jira:commented:issue
      filter:
        appIsLicensed: true
  function:
    - key: main
      handler: index.run
```
```

If you don't set `filter.appIsLicensed`, trigger functions will be invoked regardless of the app's license status on the site.

## OAuth 2.0 scopes

When using Atlassian app events, your Forge app must have permission from the site admin to access
the data it provides within the event payload. The OAuth scope required is documented under
each Atlassian app event. Note, running the `forge lint` command picks up these required scopes.

See [Permissions](/platform/forge/manifest-reference/permissions/)
for detailed information about each scope.
See [Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api)
to add new scopes to your app.

## Known issues

Atlassian app events larger than 200 kB are not delivered. This limit may change without notice.

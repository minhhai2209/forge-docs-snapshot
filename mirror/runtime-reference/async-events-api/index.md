# Async events API

This API enables Forge apps to push events and execute them asynchronously in the background.

One use case for async events is an app with a function that requires more than the Forge function maximum
of 25 seconds to run, such as an AI client or import function. The app can use the async events API to
send events to a consumer function with a longer maximum runtime that allows more processing before timeout.

## Get started

To import the Forge events package and instantiate the queue in your app, run:

```
1
2
3
import { Queue } from '@forge/events';

const queue = new Queue({ key: 'queue-name' });
```

`Queue` is generic and accepts an optional body type parameter. Pass your own type to constrain
the events the queue accepts, so `Queue.push()` only allows events whose `body` matches that type:

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
import { Queue } from '@forge/events';

interface IssueEventBody {
    issueKey: string;
}

const queue = new Queue<IssueEventBody>({ key: 'queue-name' });

await queue.push({ body: { issueKey: 'ABC-123' } }); // Allowed
// await queue.push({ body: { foo: 'bar' } });        // Type error
```

Use the same type for the [consumer function](/platform/forge/runtime-reference/async-events-api/#consumer-function)
that processes these events to type the event end to end.

## Push API

Pushes events to the queue to be processed later. The events processing can be delayed up to 15 minutes
using the `delayInSeconds` setting. A maximum of 50 events can be pushed per request, up to a maximum
combined payload of 200 KB.

### Method signature

```
```
1
2
```



```
export type Body = Record<string, unknown>;
export interface Concurrency {
    key: string;
    limit: number;
}
export interface PushEvent {
    body: Body;
    delayInSeconds?: number;
    concurrency?: Concurrency;
}
export interface PushResult {
  jobId: string;
}

const result: PushResult = await queue.push(PushEvent | PushEvent[]);
```
```

### Example

To push event(s) to the queue:

```
```
1
2
```



```
// Push a single event
await queue.push({ body: { hello: 'world' } });

// Push multiple events
await queue.push([
    { body: { greeting: 'hello' } },
    { body: { farewell: 'goodbye' } }
]);

// Delay the processing of the event by 5 seconds
await queue.push({
    body: { hello: 'world' },
    delayInSeconds: 5
});
```
```

## Event consumer

An event consumer is a standalone exported function that processes events from a queue. Unlike
[resolver functions](/platform/forge/runtime-reference/forge-resolver/), consumer functions do not use the
`Resolver` class. Instead, the consumer module in the manifest points directly to a
[`function`](/platform/forge/manifest-reference/modules/function/) module.

### Manifest configuration

To create an event consumer module in the app manifest, use:

```
```
1
2
```



```
modules:
  consumer:
    - key: queue-consumer
      # Name of the queue for which this consumer will be invoked
      queue: queue-name
      # Function to be called with payload
      function: consumer-function
  function:
    - key: consumer-function
      handler: consumer.handler
      timeoutSeconds: 600
```
```

The `handler` value follows the format `file.function`, where `consumer.handler` refers to the
`handler` function exported from `src/consumer.js` (or `src/consumer.ts`). You can use any file
name and function name, as long as they match the `handler` value in the manifest.

The optional `timeoutSeconds` parameter of the [`function`](/platform/forge/manifest-reference/modules/function/) module specifies the maximum runtime for an async event consumer function, enabling it to run longer than the default of 55 seconds.
You can specify up to 900 seconds (15 minutes).

### Consumer function

To define the function for the consumer module, export an async function from the file specified
in the manifest `handler` property:

```
```
1
2
```



```
import { AsyncEvent } from '@forge/events';

export async function handler(event: AsyncEvent, context) {
    // Access the event body
    const data = event.body;
    // Process the event
}
```
```

The `AsyncEvent` type from `@forge/events` provides type safety for the `event` parameter. By
default, `event.body` is typed as `Record<string, unknown>`. `AsyncEvent` is generic and accepts
an optional body type parameter, so you can pass your own type to get a fully typed `body`. Use the
same type you passed to the [`Queue`](/platform/forge/runtime-reference/async-events-api/#get-started)
to type the event from push to consumption:

```
```
1
2
```



```
import { AsyncEvent } from '@forge/events';

interface IssueEventBody {
    issueKey: string;
}

export async function handler(event: AsyncEvent<IssueEventBody>, context) {
    // event.body is typed as IssueEventBody
    const { issueKey } = event.body;
    // Process the event
}
```
```

If you are using JavaScript instead of TypeScript, you can omit the import and type annotation:

```
```
1
2
```



```
export async function handler(event, context) {
    // Access the event body
    const data = event.body;
    // Process the event
}
```
```

### AsyncEvent properties

The `event` parameter passed to the consumer function is an `AsyncEvent` object with the following
properties:

| Property | Type | Description |
| --- | --- | --- |
| `body` | `Record<string, unknown>` | The event payload, as provided in the `body` field of the [PushEvent](/platform/forge/runtime-reference/async-events-api/#push-api). |
| `jobId` | `string` | The unique identifier for the job that this event belongs to. Use this to [track progress](/platform/forge/runtime-reference/async-events-api/#tracking-progress-of-events) or [cancel the job](/platform/forge/runtime-reference/async-events-api/#cancel-a-job-in-progress). |
| `retryContext` | [RetryContext](/platform/forge/runtime-reference/async-events-api/#retry-context) | undefined | Contains retry metadata when the event is being retried. This property is only populated on retries, so check that it exists before accessing it. See [Retries](/platform/forge/runtime-reference/async-events-api/#retries). |

## Tracking progress of events

When you push events to the queue, a new job is created. This job's `id` is returned from the push API. To get the job's stats using the `id`, use:

```
```
1
2
```



```
// Get the job ID
const { jobId } = await queue.push([
    { body: { event: 'event1' } },
    { body: { event: 'event2' } }
]);

// Get the JobProgress object
const jobProgress = queue.getJob(jobId);

// Get stats of a particular job
const { success, inProgress, failed } = await jobProgress.getStats();
```
```

## Cancel a job in progress

You can cancel a job that's in progress using its `JobProgress` instance. When a job is canceled, any events from that job that have not yet started processing, including retries, will not be processed. This does not affect function invocations that are already being executed at the time of cancellation.

```
```
1
2
```



```
import { Queue, AsyncEvent } from '@forge/events';

const queue = new Queue({ key: 'queue-name' });

export async function handler(event: AsyncEvent, context) {
  const jobProgress = queue.getJob(event.jobId);

  try {
    // process the event
  } catch (error) {
    // You can cancel the job when an error happens
    await jobProgress.cancel();
  }
}
```
```

## Controlling processing concurrency

You can control the concurrency of event processing by setting the `concurrency` field of the `PushEvent` argument to `Queue.push()`.
This limits the number of events that can be processed concurrently.

Concurrency counters are implicitly scoped to an app installation, but not to a specific queue,
so a specific key can be used to control concurrency across multiple queues.

```
```
1
2
```



```
await queue.push({
    body: { ... },
    concurrency: {
        key: 'my-key',
        limit: 1
    }
});
```
```

If the `concurrency` field is not provided then there is no concurrency control. Event processing will be unbounded and limited only by the general per-installation [invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

We recommend setting `limit` to a fixed value for all events with the same concurrency `key`.
This ensures that the concurrency limit is consistent across all events, which helps avoid unexpected behavior.

## Delivery guarantees

Async Events that are successfully enqueued are guaranteed to be delivered **at least once** within a defined **retention window**.

### Retention window

The Retention window is a duration of the Async Event's lifetime.
It begins when the Async Event is successfully enqueued and lasts for **24 hours**.

#### Extending retention window

Retention window is extended due to:

* **processing overhead** caused by performance degradation of the Forge platform,
* **retries** triggered by [platform level errors](/platform/forge/runtime-reference/async-events-api/#platform-level-errors).

Retention window can be extended by another **72 hours**, to a total of 96 hours.

#### Exceeding retention window

If the retention window is exceeded due to [app level errors](/platform/forge/runtime-reference/async-events-api/#app-level-errors), the Async Event is dropped.

If the retention window is exceeded due to [platform level errors](/platform/forge/runtime-reference/async-events-api/#platform-level-errors), the Async Event is not dropped but will no longer be retried automatically.
Atlassian may intervene manually, which could include raising an incident or filing a public bug.

## Retries

Async Events are automatically retried within the [retention window](/platform/forge/runtime-reference/async-events-api/#retention-window) until they are successfully delivered.
Retries use exponential backoff, with intervals reaching up to approximately 15 minutes between attempts.

An event is considered successfully delivered if the invocation does **not** result in a [retry request](/platform/forge/runtime-reference/async-events-api/#retry-request),
[app level errors](/platform/forge/runtime-reference/async-events-api/#app-level-errors), or [platform level errors](/platform/forge/runtime-reference/async-events-api/#platform-level-errors).

### Retry context

The retried Async Event delivered to the app includes a `RetryContext` object.

```
```
1
2
```



```
interface RetryContext {
  retryCount: number;
  retryReason: string;
  retryData: any;
  retentionWindow?: RetentionWindow;
}

interface RetentionWindow {
  startTime: string;
  remainingTimeMs: number;
}
```
```

#### RetryContext reference

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `retryCount` | number | true | The number of retry attempts for this event. [Platform-level errors](/platform/forge/runtime-reference/async-events-api/#platform-level-errors) do not increment this. |
| `retryReason` | string | true | The reason for the retry, which may include [app-level error](/platform/forge/runtime-reference/async-events-api/#app-level-errors) or [platform-level error](/platform/forge/runtime-reference/async-events-api/#platform-level-errors) information. |
| `retryData` | any | true | Additional data to assist the [app's retry request](/platform/forge/runtime-reference/async-events-api/#retry-request). |
| `retentionWindow` | RetentionWindow | false | Information about the Async Event's retention window. |

#### RetentionWindow reference

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `startTime` | string | true | Retention window start time in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format. Retention window starts when the Async Event is successfully enqueued. |
| `remainingTimeMs` | number | true | Remaining time in milliseconds before the retention window [expires](/platform/forge/runtime-reference/async-events-api/#exceeding-retention-window), including any [extensions](/platform/forge/runtime-reference/async-events-api/#extending-retention-window). |

#### Example for reading the `retryContext`

The `retryContext` property is only populated when the event is being retried, so check that it
exists before reading it. Otherwise, destructuring it on a first delivery throws a `TypeError`.

```
```
1
2
```



```
import { AsyncEvent } from '@forge/events';

export async function handler(event: AsyncEvent) {
    // retryContext is only present on retries
    if (event.retryContext) {
        const {
            retryCount,
            retryData,
            retryReason,
            retentionWindow: {
                startTime,
                remainingTimeMs
            }
        } = event.retryContext;
        //...
    }
}
```
```

### App level errors

App-level errors occur when event processing fails due to issues in the Forge app’s code or setup, such as:

* runtime error,
* function time out,
* function out of memory,
* remote endpoint network error,
* insufficient permissions,
* reaching invocation limits.

### Platform level errors

Platform-level errors are failures caused by internal issues within the Forge platform, such as

* internal server errors,
* internal platform rate limiting.

### Retry request

You can request a retry of an Async Event by returning an `InvocationError` object. This is defined in the `@forge/events` package.

You can request Async Event retries for as long as the retention window is not exceeded.

Additional options can be included in the `InvocationError` via the `RetryOptions` object, allowing you to provide more information about what went wrong and configure the retry.

#### RetryOptions

```
```
1
2
```



```
interface RetryOptions {
  retryAfter: number;
  retryReason: InvocationErrorCode;
  retryData?: any;
}
```
```

#### RetryOptions reference

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `retryAfter` | number | true | The initial delay before the Async Event retry processing starts. The maximum `retryAfter` value is `900` seconds (15 minutes). Any `retryAfter` values exceeding this limit are lowered to `900` seconds. |
| `retryReason` | InvocationErrorCode | true | The reason for the Async Event retry. By default, `FUNCTION_RETRY_REQUEST` is used. |
| `retryData` | any | false | Additional data to assist the app's retry request. The maximum `retryData` size is 4KB. |

#### InvocationErrorCode values

| Value | Description |
| --- | --- |
| FUNCTION\_RETRY\_REQUEST | Unclassified error occurred during the app that the developer would like to retry. |
| FUNCTION\_UPSTREAM\_RATE\_LIMITED | Rate limit upstream that caused the app to fail. |

#### Example for requesting a retry

In the following sample code, the app calls an external API and is rate limited. A retry is requested with a timeout that is equal to the backoff time provided by the external API and the retry reason is `FUNCTION_UPSTREAM_RATE_LIMITED` as there was an upstream dependency that was rate limited.

```
```
1
2
```



```
import { AsyncEvent, InvocationError, InvocationErrorCode } from '@forge/events';

export async function handler(event: AsyncEvent) {
  const userName = event.body.userName;
  const response = await callExternalApi(userName);

  if (response.headers.has('Retry-After')) {
    return new InvocationError({
      retryAfter: parseInt(response.headers.get('Retry-After')),
      retryReason: InvocationErrorCode.FUNCTION_UPSTREAM_RATE_LIMITED,
      retryData: {
        userName: userName
      }
    });
  }
}
```
```

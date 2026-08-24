# Upgrade to @forge/events major version 2

## Event publishing

Breaking changes

The signature of `Queue.push()` has changed, with the parameter type `PushEvent` now containing `body` and `delayInSeconds`. The event `body` must be an `object`.

**`@forge/events` 1.x**

```
1type Payload = string | number | boolean | { [key: string]: Payload };
2type PushSettings = { delayInSeconds: number };
3
4await queue.push(Payload | Payload[], PushSettings);
5
```

**`@forge/events` 2.0.0**

```
1export type Body = Record<string, unknown>;
2export interface PushEvent {
3    body: Body;
4    delayInSeconds?: number;
5}
6
7const result: PushResult = await queue.push(PushEvent | PushEvent[]);
8
```

### Event consumption

Breaking changes

[Forge resolvers](/platform/forge/runtime-reference/forge-resolver/) are no longer used. The [Consumer](/platform/forge/manifest-reference/modules/consumer/) module instead requires a [Function](/platform/forge/function-reference/index/).

Consumer functions are invoked with an `AsyncEvent`, which contains the fields of `PushEvent` as well as invocation-specific fields, including `jobId` and `retryContext`. `jobId` is no longer available via context. `retryContext` is no longer added to the event body.

**`@forge/events` 1.x**

```
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
11
12
13
14
```



```
modules:
  consumer:
    - key: queue-consumer
      # Name of the queue for which this consumer will be invoked
      queue: queue-name
      resolver:
        function: consumer-function
        # resolver function to be called with payload
        method: event-listener
  function:
    - key: consumer-function
      handler: consumer.handler
      timeoutSeconds: 600
```
```

```
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
```



```
import Resolver from '@forge/resolver';
const resolver = new Resolver();

resolver.define('event-listener', async ({ payload, context }) => {
    // process the event
});

export const handler = resolver.getDefinitions();
```
```

**`@forge/events` 2.0.0**

```
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
11
12
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

```
```
1
2
3
4
5
6
```



```
import { AsyncEvent } from '@forge/events';

export async function handler(event: AsyncEvent, context) {
    // Process the event
}
```
```

### Job progress tracking

Breaking changes

`JobProgress.getStats()` now returns a `JobStats` object containing `success`, `inProgress` and `failed`, instead of an `APIResponse`.

**`@forge/events` 1.x**

```
```
1
2
3
4
5
```



```
const jobId = await queue.push([{ event: 'event1' }, { event: 'event2' }]);
const jobProgress = queue.getJob(jobId);
const response = await jobProgress.getStats();
const { success, inProgress, failed } = await response.json();
```
```

**`@forge/events` 2.0.0**

```
```
1
2
3
4
5
6
7
```



```
const { jobId } = await queue.push([
    { body: { event: 'event1' } },
    { body: { event: 'event2' } }
]);
const jobProgress = queue.getJob(jobId);
const { success, inProgress, failed } = await jobProgress.getStats();
```
```

### Job cancellation

Breaking changes

`JobProgress.cancel()` no longer returns an `APIResponse`.

### Retries

No breaking changes

Retries are now based on the [retention window](/platform/forge/runtime-reference/async-events-api/#retention-window) instead of the maximum retry count.
[Retention window](/platform/forge/runtime-reference/async-events-api/#retention-window) `startTime` and `remainingTimeMs` are now added to the `RetryContext` in the `AsyncEvent`.

**`@forge/events` 1.x**

Async Events were retried **4 times**.

```
```
1
2
3
4
5
6
```



```
interface RetryContext {
  retryCount: number;
  retryReason: InvocationErrorCode;
  retryData: any;
}
```
```

```
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
11
12
13
```



```
import Resolver from '@forge/resolver';
const resolver = new Resolver();

resolver.define('event-listener', async ({ payload, context }) => {
        const {
            retryCount,
            retryData,
            retryReason
        } = payload.retryContext;
});

export const handler = resolver.getDefinitions();
```
```

Known issues:

* [ECO-734](https://jira.atlassian.com/browse/ECO-734): Retry context is not sent when retrying Async Events with non-`object` payload

**`@forge/events` 2.0.0**

Async Events are retried until the [retention window is exceeded](/platform/forge/runtime-reference/async-events-api/#exceeding-retention-window).

```
```
1
2
3
4
5
6
7
```



```
interface RetryContext {
  retryCount: number;
  retryReason: string;
  retryData: any;
  retentionWindow?: RetentionWindow;
}
```
```

```
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
11
12
13
14
15
```



```
import {AsyncEvent} from '@forge/events';

export async function handler(event: AsyncEvent) {
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
```
```

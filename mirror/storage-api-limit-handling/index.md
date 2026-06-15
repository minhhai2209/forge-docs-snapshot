# Queue app interactions with storage API

The [Async event APIs](/platform/forge/runtime-reference/async-events-api/) can queue your app's interaction with the storage API.
Doing this can help prevent your app from exceeding Forge's [storage API operation limits per installation](/platform/forge/platform-quotas-and-limits/#storage-api-operation-limits-per-installation).

On this page, we provide an example that shows how to queue `kvs.set` calls. This example's strategy uses *exponential backoff* with *jitter retry* to minimize retry collisions.

## Before you begin

This guide documents the use of [Async event APIs](/platform/forge/runtime-reference/async-events-api/). Review these APIs for more detailed information about each endpoint.

## Step 1: Create an event consumer

Start by creating an [event consumer](/platform/forge/runtime-reference/async-events-api/#event-consumer) in the app manifest. The following snippet features a consumer with a queue for receiving batch calls, named `storage-async-queue`.

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
modules:
  # Async events
  consumer:
    - key: queue-consumer
      # Name of the queue for which this consumer will be invoked
      queue: storage-async-queue
      # Function to be called with payload
      function: consumer-function
  function:
    - key: consumer-function
      handler: index.handler
```

## Step 2: Push events to the queue

Next, create a new Queue object mapped to the `storage-async-queue` queue we defined earlier in the manifest. Instead of calling `kvs.set` directly inside the Atlassian app event handler, we will push the events to the queue.

By calling `kvs.set` inside the consumer function, we can leverage the [retry mechanism](/platform/forge/runtime-reference/async-events-api/#retries). Should the call to `kvs.set` hit the operation limit and return an error, we can catch the error and trigger the request to be retried by returning an `InvocationError`:

```
```
1
2
```



```
import {InvocationError, InvocationErrorCode, Queue} from "@forge/events";

const storageAsyncQueue = new Queue({ key: 'storage-async-queue' });

// Product event handling
export async function onIssueCreated(event, context) {

  // A batch job that created 1000+ of issues will call
  // kvs.set 1000+ times and hit the operation limits.
  // This pushes it to the queue instead to let onIssueCreated handle it.

  const body = {
    "issueKey": event.issue.key
  }

  await storageAsyncQueue.push({ body, delayInSeconds: 0.5 });

  return true;
}
```
```

Async events are automatically retried within the [retention window](/platform/forge/runtime-reference/async-events-api/#retention-window) (24 hours, extendable up to 96 hours), with a maximum of **four** retries. Retries use exponential backoff. See [Retries](/platform/forge/runtime-reference/async-events-api/#retries) for details.

## Step 3: Create the handler for the event consumer

Last, create the handler function that calls the storage API for the event consumer `queue-consumer`. This function configures how the batch calls queued (in `storage-async-queue`) are processed:

```
```
1
2
```



```
import { InvocationError, InvocationErrorCode } from '@forge/events';
import { storage as kvs } from '@forge/api';

// Async event handler
export async function handler(event, context) {
  let retryDelay = 0;

  // If `event.retryContext` exists, this event is a retry event
  if (event.retryContext) {
    const baseDelay = 20;
    const randomJitter = Math.random() * 100;
    
    // Exponential backoff with jitter
    retryDelay = (baseDelay * (2 ** event.retryContext.retryCount)) + randomJitter;
  }  

  // Store issue key by calling a Storage API
  try {
    await kvs.set('most-recent-issue-created', event.body.issueKey);
  } catch (error) {
    // Return an InvocationError to trigger a retry
    return new InvocationError({
      retryAfter: retryDelay,
      retryReason: InvocationErrorCode.FUNCTION_RETRY_REQUEST,
      retryData: {
        issueKey: event.body.issueKey
      }
    });
  }
}
```
```

## Reference implementation

Refer to the following sample for the complete contents of this guide's `index.js` file:

```
```
1
2
```



```
import { InvocationError, InvocationErrorCode, Queue } from '@forge/events';
import { storage as kvs } from '@forge/api';

const storageAsyncQueue = new Queue({ key: 'storage-async-queue' });

// Product event handling
export async function onIssueCreated(event, context) {

  // A batch job that created 1000+ of issues will call
  // kvs.set 1000+ times and hit the operation limits.
  // This pushes it to the queue instead to let onIssueCreated handle it.

  const body = {
    "issueKey": event.issue.key
  }

  await storageAsyncQueue.push({ body, delayInSeconds: 0.5 });

  return true;
}

// Async event handler
export async function handler(event, context) {
  let retryDelay = 0;

  // If `event.retryContext` exists, this event is a retry event
  if (event.retryContext) {
    const baseDelay = 20;
    const randomJitter = Math.random() * 100;
    
    // Exponential backoff with jitter
    retryDelay = (baseDelay * (2 ** event.retryContext.retryCount)) + randomJitter;
  }  

  // Store issue key by calling a Storage API
  try {
    await kvs.set('most-recent-issue-created', event.body.issueKey);
  } catch (error) {
    // Return an InvocationError to trigger a retry
    return new InvocationError({
      retryAfter: retryDelay,
      retryReason: InvocationErrorCode.FUNCTION_RETRY_REQUEST,
      retryData: {
        issueKey: event.body.issueKey
      }
    });
  }
}
```
```

# realtime (Preview)

Forge Realtime is now available as Preview capability. Preview capabilities are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview capabilities are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge Realtime allows Forge apps to subscribe and publish to realtime channels. Unlike the existing [Events API](/platform/forge/apis-reference/ui-api-bridge/events/), realtime events are broadcast beyond the current window. This means that it can be used for scenarios where live updates need to propagate to multiple users.

Realtime events can also be published from [resolvers](/platform/forge/runtime-reference/forge-resolver/), eliminating the need for the frontend to poll the resolver for live updates. However, resolvers cannot subscribe to channels.

## subscribe

The `subscribe()` function allows you to subscribe to a channel and call a provided callback function when any event is published to the channel. This includes events published from both the frontend and from resolvers.

Subscriptions created with the `subscribe()` function are scoped to channels for the current module context by default. This means that a subscription in a module, for example `jira:issuePanel`, will only receive messages that are published from the *same module in the same Jira issue*. It will not receive messages from a `jira:issueContext` on that issue, or the `jira:issuePanel` on a different issue, even if they share the same channel name.

See the [in-depth guide](/platform/forge/realtime/authorizing-realtime-channels/) on how to authorize channels for more detail.

### Function signature

```
```
1
2
```



```
const subscribe = (
  channel: string,
  callback: (payload?: string) => any,
  options?: SubscriptionOptions
): Promise<Subscription>

interface SubscriptionOptions {
  replaySeconds?: number;
  token?: string;
  contextOverrides?: ProductContext[];
}
```
```

```
```
1
2
```



```
export enum Jira {
  Board = 'board',
  Issue = 'issue',
  Project = 'project'
}

export enum Confluence {
  Content = 'content',
  Space = 'space'
}

export enum Bitbucket {
  PullRequest = 'pullRequest',
  Repository = 'repository'
}

type ProductContext = Jira | Confluence | Bitbucket;
```
```

### Arguments

* **channel**: A string identifier representing the name of the channel to subscribe to.
  This string should exactly match the `channel` parameter in the corresponding `publish()` function.
* **callback**: A function, which takes a string or JSON `payload`, that is called when an event is received on the channel.
* **options**: An object containing configuration options.
  * **replaySeconds**: A timespan in seconds to receive previous events from a channel when initially subscribing.
  * **token**: A token returned from the [signRealtimeToken](/platform/forge/runtime-reference/realtime-events-api/) method that is used to restrict a channel's scope. The subscription will only receive events that have been published with a token containing the same channel context claims. This is in addition to the existing Atlassian app context scope of the channel.
  * **contextOverrides**: An array of context properties to include in the channel context. This will override the existing Atlassian app context scope of the channel.

### Returns

* **Subscription**: A `Subscription` which contains the `unsubscribe()` function.

### Example

```
```
1
2
```



```
import { realtime } from '@forge/bridge';
import { Button } from '@forge/react';

const App = () => {
  return (
    <Button onClick={() => {
      const onEvent = (payload: string | Record<string, unknown>) => {
        console.log('Received event with payload: ', payload);
      };
      const subscription = realtime.subscribe('my-test-channel', onEvent);
    }}>
      Subscribe
    </Button>
  );
};
```
```

## subscribeGlobal

The `subscribeGlobal()` function allows you to subscribe to a global channel and call a provided callback function when any event is published to the channel. This includes events published from both the frontend and from resolvers.

Global channels are not secured by the Atlassian app context that the user has permissions for.

If an app is publishing messages to a global channel with `publishGlobal()`, then any user with access to the app installation can subscribe to that channel with `subscribeGlobal()` and receive its messages if they know the channel name. This is the case even if the message originates from a page that the user does not have permissions for, like a restricted Jira issue or Confluence page.

It is your responsibility to ensure you are scoping your channels appropriately, and only using global channels if absolutely necessary. Using channel tokens to enforce Atlassian app permissions is also encouraged when using global channels.

### Function signature

```
```
1
2
```



```
const subscribeGlobal = (
  channel: string,
  callback: (payload?: string | Record<string, unknown>) => any,
  options?: SubscriptionOptions
): Promise<Subscription>

interface SubscriptionOptions {
  replaySeconds?: number;
  token?: string;
  contextOverrides?: ProductContext[];
}
```
```

```
```
1
2
```



```
export enum Jira {
  Board = 'board',
  Issue = 'issue',
  Project = 'project'
}

export enum Confluence {
  Content = 'content',
  Space = 'space'
}

export enum Bitbucket {
  PullRequest = 'pullRequest',
  Repository = 'repository'
}

type ProductContext = Jira | Confluence | Bitbucket;
```
```

### Arguments

* **channel**: A string identifier representing the name of the channel to subscribe to.
  This string should exactly match the `channel` parameter in the corresponding `publishGlobal()` function.
* **callback**: A function, which takes a string or JSON `payload`, that is called when an event is received on the channel.
* **options**: An object containing configuration options.
  * **replaySeconds**: A timespan in seconds to receive previous events from a channel when initially subscribing.
  * **token**: A token returned from the [signRealtimeToken](/platform/forge/runtime-reference/realtime-events-api/) method that is used to restrict a channel's scope. The subscription will only receive events that have been published with a token containing the same channel context claims.
  * **contextOverrides**: An array of context properties to include in the channel context. This will override the existing Atlassian app context scope of the channel.

### Returns

* **Subscription**: A `Subscription` which contains the `unsubscribe()` function.

### Example

```
```
1
2
```



```
import { realtime } from '@forge/bridge';
import { Button } from '@forge/react';

const App = () => {
  return (
    <Button onClick={() => {
      const onEvent = (payload: string | Record<string, unknown>) => {
        console.log('Received event with payload: ', payload);
      };
      const subscription = realtime.subscribeGlobal('my-test-channel', onEvent);
    }}>
      Subscribe
    </Button>
  );
};
```
```

## unsubscribe

The `unsubscribe()` function for a channel can be accessed through the `Subscription` object that was returned from the `subscribe()` function for that channel.

Calling `Subscription.unsubscribe()` will remove the channel subscription for the specific `Subscription` instance and will not globally remove all subscriptions from that channel.

### Type signature

```
```
1
2
```



```
type Subscription = {
  unsubscribe: () => void;
};
```
```

### Example

```
```
1
2
```



```
import { useEffect } from 'react';
import { realtime } from '@forge/bridge';

const App = () => {
  useEffect(() => {
    const onEvent = (payload: string | Record<string, unknown>) => {
      console.log('Received event with payload: ', payload);
    };

    const subscription = realtime.subscribe('my-test-channel', onEvent);
    const globalSubscription = realtime.subscribeGlobal(
      'my-test-global-channel',
      onEvent
    );
    
    return () => {
      subscription.then(s => s.unsubscribe());
      globalSubscription.then(s => s.unsubscribe());
    }
  }, []);
  return (
    <div>My App</div>
  );
};
```
```

## publish

The `publish()` function will publish an event to the channel with the given payload. If you have subscribed to the channel with the `subscribe()` function, your callback will be invoked with the event. The payload must be a string, so make sure to stringify any objects before passing them as arguments.

### Function signature

```
```
1
2
```



```
const publish = (
    channel: string,
    payload: string | Record<string, unknown>,
    options?: PublishOptions
): Promise<PublishResult>

interface PublishOptions {
  token?: string;
  contextOverrides?: ProductContext[];
}

interface PublishResult {
  eventId: string | null;
  eventTimestamp: string | null;
  errors?: string[];
}
```
```

```
```
1
2
```



```
export enum Jira {
  Board = 'board',
  Issue = 'issue',
  Project = 'project'
}

export enum Confluence {
  Content = 'content',
  Space = 'space'
}

export enum Bitbucket {
  PullRequest = 'pullRequest',
  Repository = 'repository'
}

type ProductContext = Jira | Confluence | Bitbucket;
```
```

### Arguments

* **channel**: A string identifier representing the name of the channel to subscribe to.
  This string should exactly match the `channel` parameter in the corresponding `subscribe()` function.
* **payload**: The event payload as a string or serializable object.
* **options**: An object containing configuration options.
  * **token**: A token returned from the [signRealtimeToken](/platform/forge/runtime-reference/realtime-events-api/) method that is used to restrict a channel's scope. The published event will only be received by subscriptions that have been created with a token containing the same channel context claims.
  * **contextOverrides**: An array of context properties to include in the channel context. This will override the existing Atlassian app context scope of the channel.

### Returns

* **PublishResult**: A `PublishResult` which contains information about the published event.
  * **eventId**: The ID of the published event as a string. The value will be null if the event failed to publish or if there are no existing subscriptions for that channel.
  * **eventTimestamp**: The timestamp of the published event, in epoch milliseconds.
  * **errors**: A list of error messages if the event failed to publish.

### Example

```
```
1
2
```



```
import { useEffect } from 'react';
import { realtime } from '@forge/bridge';
import { Button } from '@forge/react';

const App = () => {
  useEffect(() => {
    const onEvent = (payload: string | Record<string, unknown>) => {
      console.log('Received event with payload: ', payload);
    };
    const subscription = realtime.subscribe('my-test-channel', onEvent);
    return () => {
      subscription.then(s => s.unsubscribe());
    }
  }, []);

  return (
    <Button onClick={() => realtime.publish('my-test-channel', 'Here is an event payload!')}>
      Publish event
    </Button>
  );
};
```
```

## publishGlobal

The `publishGlobal()` function will publish an event to the channel with the given payload. If you have subscribed to the channel with the `subscribeGlobal()` function, your callback will be invoked with the event. The payload must be a string, so make sure to stringify any objects before passing them as arguments.

### Function signature

```
```
1
2
```



```
const publishGlobal = (
    channel: string,
    payload: string | Record<string, unknown>,
    options?: PublishOptions
): Promise<PublishResult>

interface PublishOptions {
  token?: string;
  contextOverrides?: ProductContext[];
}

interface PublishResult {
  eventId: string | null;
  eventTimestamp: string | null;
}
```
```

```
```
1
2
```



```
export enum Jira {
  Board = 'board',
  Issue = 'issue',
  Project = 'project'
}

export enum Confluence {
  Content = 'content',
  Space = 'space'
}

export enum Bitbucket {
  PullRequest = 'pullRequest',
  Repository = 'repository'
}

type ProductContext = Jira | Confluence | Bitbucket;
```
```

### Arguments

* **channel**: A string identifier representing the name of the channel to subscribe to.
  This string should exactly match the `channel` parameter in the corresponding `subscribe()` function.
* **payload**: The event payload as a string or serializable object.
* **options**: An object containing configuration options.
  * **token**: A token returned from the [signRealtimeToken](/platform/forge/runtime-reference/realtime-events-api/) method that is used to restrict a channel's scope. The published event will only be received by subscriptions that have been created with a token containing the same channel context claims.
  * **contextOverrides**: An array of context properties to include in the channel context. This will override the existing Atlassian app context scope of the channel.

### Returns

* **PublishResult**: A `PublishResult` which contains information about the published event.
  * **eventId**: The ID of the published event as a string. The value will be null if the event failed to publish or if there are no existing subscriptions for that channel.
  * **eventTimestamp**: The timestamp of the published event, in epoch milliseconds.
  * **errors**: A list of error messages if the event failed to publish.

### Example

```
```
1
2
```



```
import { useEffect } from 'react';
import { realtime } from '@forge/bridge';
import { Button } from '@forge/react';

const App = () => {
  useEffect(() => {
    const onEvent = (payload: string | Record<string, unknown>) => {
      console.log('Received event with payload: ', payload);
    };
    const subscription = realtime.subscribeGlobal('my-test-channel', onEvent);
    return () => {
      subscription.then(s => s.unsubscribe());
    }
  }, []);

  return (
    <Button onClick={() => realtime.publishGlobal('my-test-channel', 'Here is an event payload!')}>
      Publish global event
    </Button>
  );
};
```
```

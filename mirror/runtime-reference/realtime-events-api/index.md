# Realtime events API (Preview)

Forge Realtime is now available as a a Preview capability. Preview capabilities are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview capabilities are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

This API enables Forge apps to publish events to realtime channels. This is suited for scenarios where live updates are sent beyond the current page or to multiple users. Unlike the existing [Async events API](https://developer.atlassian.com/platform/forge/runtime-reference/async-events-api/), realtime events are emitted via WebSocket connections rather than on the window object.

**Forge functions can only publish events at this time**. You will need to set up the frontend of your app to first subscribe to events using the respective realtime `@forge/bridge` [API](/platform/forge/apis-reference/ui-api-bridge/realtime) before receiving the published events.

## Get started

To publish an event, first import the Realtime publish API into your Forge resolver file:

```
1
import { publish } from '@forge/realtime';
```

Alternatively, to publish an event to a globally scoped channel, import the global publish API:

```
1
import { publishGlobal } from '@forge/realtime';
```

## Publish API

Publishes events if there is an existing subscription for the same channel context. The resulting `eventId` and `eventTimestamp` will be null if there are no existing subscribers.

### Method signature

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

const publishGlobal = (
    channel: string,
    payload: string | Record<string, unknown>,
    options?: PublishOptions
): Promise<PublishResult>

enum Jira {
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

type ProductContext = Jira | Conflunece | Bitbucket;

interface PublishOptions {
  token?: string;
  contextOverrides?: ProductContext[];
}

interface PublishResult {
  eventId: string | null;
  eventTimestamp: string | null;
  errors: any;
}
```
```

### Arguments

* **channel**: A string identifier representing the name of the channel to subscribe to. This string should exactly match the channel parameter in the corresponding subscribe() function.
* **payload**: The event payload as a string or serializable object.
* **options**: An object containing configuration options.
  * **token**: A token returned from the `signRealtimeToken` method that is used to restrict a channel's scope. The published event will only be received by subscriptions that have been created with a token containing the same channel context claims.
  * **contextOverrides**: An array of context properties to include in the channel context. This will override the existing Atlassian app context scope of the channel.

### Returns

### Example

```
```
1
2
```



```
import Resolver from '@forge/resolver';
import { publish } from '@forge/realtime';

const resolver = new Resolver();

resolver.define("publishRealtimeEvent", ({ payload, context }) => {
  const channel = 'my-example-channel';
  const payload = { foo: 'foo', bar: 'bar' };
  publish(channel, payload);
  return {
    example: `Published event with payload: ${JSON.stringify(payload)}`
  };
});

export const handler = resolver.getDefinitions();
```
```

## Choosing between publish and publishGlobal

Subscriptions created with the `subscribe()` function are scoped to channels for the current module context by default. This means that a subscription in a module, for example `jira:issuePanel`, will only receive messages that are published from the *same module in the same Jira issue*. It will not receive messages from a `jira:issueContext` on that issue, or the `jira:issuePanel` on a different issue, even if they share the same channel name.

See the [in-depth guide](/platform/forge/realtime/authorizing-realtime-channels/) on how to authorize channels for more detail.

Although the APIs for `publish` and `publishGlobal` are identical, the `publishGlobal` API does not enforce full permission scopes according to the Atlassian app and extension contexts your app is installed in. Events in global channels are sent across modules and Atlassian app contexts. This means that any users with access to your app may receive events from a private Jira issue or Confluence page that they do not have access to.

As a result, events sent by the `publish` API can only be received by subscriptions created using the `subscribe` @forge/bridge API, and `publishGlobal` events can only be received by subscriptions created using the `subscribeGlobal` bridge API.

## Using the `token` argument to secure channel context

The `token` argument allows for more fine-grained control over the permissions scopes of your realtime events. See [Authorizing Realtime channels](/platform/forge/realtime/authorizing-realtime-channels/) for more information on how to manage authorization within your app.

## Realtime token API

To obtained a signed realtime token, import the `signRealtimeToken` function into your resolver:

```
```
1
2
```



```
import { publishGlobal, signRealtimeToken } from '@forge/realtime';
```
```

### Method signature

```
```
1
2
```



```
const signRealtimeToken = (
    channel: string,
    claims: object
): Promise<TokenResult>

interface TokenResult = {
    token: string | null;
    expiresAt: number | null;
    errors?: any;
}
```
```

### Arguments

* **channel**: A string identifier representing the name of the channel to sign the token against. This string should exactly match the channel parameter in the corresponding subscribe() or publish() function.
* **claims**: An object containing token claims. This can take any shape, but for events to be communicated on the same channel the claims object must match exactly between the publisher and subscriber.

### Returns

* **TokenResult**: A `TokenResult` which contains the signed token result.
  * **token**: The signed token. This is the value to be used in the `token` argument in your `publish()`, `publishGlobal()`, `subscribe()` or `subscribeGlobal()` calls
  * **expiresAt**: The timestamp of when the token expires, in Epoch time.
  * **errors**: A list of error messages if the event failed to publish.

### Example

```
```
1
2
```



```
import Resolver from '@forge/resolver';
import { publish, signRealtimeToken } from '@forge/realtime';

const resolver = new Resolver();
const TOKEN_EXPIRY_BUFFER = 5000; // 5 seconds

resolver.define('publishEvent', ({ payload, context }) => {
  const customClaims = {
    allowedUsers: ['accountId-1', 'accountId-2'],
  };
  
  const { token, expiresAt } = signRealtimeToken('my-test-channel', customClaims);

  // expiresAt is an epoch timestamp expressed in seconds (in accordance with the JWT 
  // standard for the exp field), so it needs to be converted to milliseconds before 
  // comparing against a Date timestamp.
  if (Date.now() - TOKEN_EXPIRY_BUFFER < expiresAt * 1000) {
     return publish('my-test-channel', 'This is an event payload', { token }); 
  }
});

export const handler = resolver.getDefinitions();
```
```

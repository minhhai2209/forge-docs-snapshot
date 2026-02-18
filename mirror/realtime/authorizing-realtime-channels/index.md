# Authorizing Realtime channels

Forge Realtime is now available as Preview capability. Preview capabilities are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview capabilities are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge Realtime offers multiple options for restricting a channel's scope based on the Atlassian app context permissions or your own custom-defined permissions.
Realtime channels are always restricted to an app installation at a minimum; however, it is important that you use the appropriate level of authorization within your
app to prevent unprivileged users from gaining access to your channels in privileged contexts.

## Atlassian app context permissions

### Default channel context

The default context for a channel will be the Atlassian app context of the module. This means that a subscription in a module, for example `jira:issuePanel`, will only receive messages that are published *from the same module in the same Jira issue*. It will not receive messages from a `jira:issueContext` on that issue, or the `jira:issuePanel` on a different issue, even if they share the same channel name.

We recommend using the default `publish()` and `subscribe()` methods if you don't need to send messages between Atlassian app contexts.

![Atlassian app context as default channel context](https://dac-static.atlassian.com/platform/forge/images/realtime/realtime-atlassian-app-context-publish.png?_v=1.5800.1858)

#### Example

**Frontend**

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

    return () => {
      subscription.then(s => s.unsubscribe());
    };
  }, []);

  return (
    <Button onClick={() => realtime.publish('my-test-channel', 'Here is an event payload!')}>
      Publish event
    </Button>
  );
};
```
```

### Using context overrides

If the entire Atlassian app context is too restrictive for your channel scope, you can customize it with context overrides.
You can do this by providing the `contextOverrides` property in the `options` parameter of the subscribe and publish methods.
It takes a list of allowlisted Atlassian app context properties, such as `Jira.Project`, and only includes those properties in the channel context.

This will allow you to create channels that exist across different modules or pages while still enforcing the
user's product permissions for the context properties you provide.

Providing `contextOverrides` will completely override the default channel context. If it's provided as an empty array,
then the channel will *not* be secured by any Atlassian app context values, and will be equivalent to a [global channel](/platform/forge/realtime/authorizing-realtime-channels/#using-global-channels).

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

export type ProductContext = Jira | Confluence | Bitbucket;

export interface SubscriptionOptions {
  replaySeconds?: number;
  token?: string;
  contextOverrides?: ProductContext[];
}

export interface PublishOptions {
  token?: string;
  contextOverrides?: ProductContext[];
}
```
```

#### Example

The example below establishes a channel that is scoped to the current Jira project. Messages can be published
between different issues and boards in the project.

**Frontend**

```
```
1
2
```



```
import { useEffect } from 'react';
import { realtime } from '@forge/bridge';
import { Jira } from '@forge/bridge/realtime';

const App = () => {
  useEffect(() => {
    const subscription = realtime.subscribe(
      'my-test-channel',
      (payload) => console.log(payload),
      { contextOverrides: [Jira.Project] }
    );
  }, []);

  return (
    <Button onClick={() => realtime.publish(
      'my-test-channel',
      'Here is an event payload!',
      { contextOverrides: [Jira.Project] }
    )}>
      Publish event
    </Button>
  );
};
```
```

The properties in `contextOverrides` must match exactly in the `subscribe()` and `publish()` calls in order for messages to be received.

`contextOverrides` does not allow for a subscriber with a broader context to receive messages from a publisher with a more specific context. For example,
a subscriber with overrides `[Jira.Project]` will not receive messages from a publisher with overrides `[Jira.Project, Jira.Issue]`, even
though they have overlapping properties.

![Atlassian app context with overrides as channel context](https://dac-static.atlassian.com/platform/forge/images/realtime/realtime-context-overrides-publish.png?_v=1.5800.1858)

#### Limitations

When using `contextOverrides`, keep in mind these limitations:

* `contextOverrides` is only supported for functions invoked from the app frontend. This is **not** currently available for async events and web triggers.
* Similarly, publishing to non-global channels is only supported for functions invoked from the app frontend. Use global channels and the [`realtimeToken`](/platform/forge/realtime/authorizing-realtime-channels/#custom-channel-context-with-realtime-tokens) to apply additional restrictions.

### Using global channels

Global channels can be used to send messages across different Atlassian app contexts within an app installation, and should only be used when
the above two options are not suitable. Some examples of when you should use a global channel are if a channel needs to send messages between
different Jira projects, or when publishing messages from a Forge function that isn't associated with a UI context, for example functions for
[Atlassian app events](/platform/forge/events-reference/product_events/) or [lifecycle events](/platform/forge/events-reference/life-cycle/).

Global channels are not secured by the Atlassian app context that the user has permissions for.

If an app is publishing messages to a global channel with `publishGlobal()`, then any user with access to the app installation can subscribe to that channel with `subscribeGlobal()` and receive its messages if they know the channel name. This is the case even if the message originates from a page that the user does not have permissions for, like a restricted Jira issue or Confluence page.

It is your responsibility to ensure you are scoping your channels appropriately, and only using global channels if absolutely necessary. Using channel tokens to enforce Atlassian app permissions is also encouraged when using global channels.

![Global channels with no channel context](https://dac-static.atlassian.com/platform/forge/images/realtime/realtime-global-publish.png?_v=1.5800.1858)

#### Example

**Frontend**

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

    const subscription = realtime.subscribeGlobal('my-global-channel', onEvent);

    return () => {
      subscription.then(s => s.unsubscribe());
    };
  }, []);

  return (
    <Button
      onClick={() => realtime.publishGlobal('my-global-channel', 'Here is an event payload!')}
    >
      Publish event
    </Button>
  );
};
```
```

## Custom channel context with Realtime tokens

In addition to the Atlassian app context, you can also include your own set of custom claims to secure a channel by signing your own Realtime token
with the `signRealtimeToken` method from `@forge/realtime`. The claims can contain any serializable data, but it is your responsibility to validate the claims before signing them into the token. Note that the `@forge/realtime` package can only be used in a [resolver](/platform/forge/runtime-reference/forge-resolver/) and cannot be used on the frontend.

The custom claims will be added on top of the Atlassian app context that already exists for your channel. If using the `subscribe` and `publish` methods,
the channel is secured by the Atlassian app context (or a subset if `contextOverrides` is provided) and your token's claims. If using the `subscribeGlobal`
and `publishGlobal` methods, the channel is only secured by the token.

![Atlassian app context with Realtime token as channel context](https://dac-static.atlassian.com/platform/forge/images/realtime/realtime-token-publish.png?_v=1.5800.1858)

#### Example

**Resolver**

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

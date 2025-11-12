# App events (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge apps can publish custom backend events. Other apps installed on the same site can listen to those events.

## Publishing events

### Manifest declaration

Apps must declare their intent to publish events by using the [event](/platform/forge/manifest-reference/modules/event/) module:

```
1
2
3
4
5
modules:
  event:
    - key: event-key
      name: Event name
      allowedRecipients: ['*']
```

#### Restricting the list of recipients

By default, only the publishing app is allowed to receive the app event.

The list of allowed recipients can be controlled by the `allowedRecipients` property.

* To allow *anyone* to receive the event, add the special `*` wildcard character to the list of values.
* You can also allow only a given set of apps by providing app ARI identifiers

For example, the following declaration allows only two specified apps to receive the event:

```
```
1
2
```



```
modules:
  event:
    - key: event-key
      name: Event name
      allowedRecipients:
        - ari:cloud:ecosystem::app/23c6fcd5-2836-4a8e-b2b8-83b2e71238e1
        - ari:cloud:ecosystem::app/1623e379-f942-4517-9a20-830c24b54ec1
```
```

### Publishing with the runtime API

The app can publish the event using the runtime API.

To import the App events API, run:

```
```
1
2
```



```
import { appEvents } from '@forge/events';
```
```

The `appEvents` object has one function to publish events, called `publish`.
The function accepts a list of maximum 10 events, each event defined by its key (the key of the `event` module in the manifest).

To publish the event declared in the [Manifest declaration](#manifest-declaration) section, run:

```
```
1
2
```



```
const result = await appEvents.publish({'key': 'event-key'});
```
```

The result of this operation can be either a success or a failure.
The success can be partial; inspect the `failedEvents` field of the successful response to see which events failed publishing after all.

Here is a simple template for inspecting what happened and acting accordingly:

```
```
1
2
```



```
const result = await appEvents.publish({'key': 'my-custom-event'});
if (result.type === 'success') {
  // the event was published successfully
  if (result?.failedEvents?.length) {
      // but it was a partial success and some events failed to be published after all
      const eventsThatFailedPublishing = result.failedEvents;
  }
} else {
  // publishing failed
  const errorMessage = result.errorMessge;
  const errorType = result.errorType;
}
```
```

## Listening to events

App events can be subscribed to with the [trigger](/platform/forge/manifest-reference/modules/trigger/) module.

To subscribe to an app event, use the following AVI (Atlassian eVent Identifier):

```
```
1
2
```



```
avi:cloud:ecosystem::event/{app-id}/{module-key}
```
```

* `app-id` is the UUID of the app that publishes the event
* `module-key` is the key of the [event](/platform/forge/manifest-reference/modules/event/) module from the publishing app

For example, to subscribe to the event defined in the [Manifest declaration](#manifest-declaration) section, put this in the manifest:

```
```
1
2
```



```
modules:
  trigger:
    - key: my-trigger
      function: trigger
      events:
        - avi:cloud:ecosystem::event/d9022ad7-c220-4836-b1d1-7f9f2c633d3a/event-key
  function:
    - key: trigger
      handler: index.trigger
```
```

(Assuming the ID of the publishing app is `d9022ad7-c220-4836-b1d1-7f9f2c633d3a`.)

### Trigger function

The app is now ready to process events with the declared trigger [function](/platform/forge/function-reference/index/).
Here is a handy template for such a function:

```
```
1
2
```



```
export async function trigger(event, context) {
    console.log('context: ' + JSON.stringify(context, null, 2));
    console.log('event: ' + JSON.stringify(event, null, 2));

    return true;
}
```
```

### Event payload

The payload for app events (the `event` argument of the [trigger function](#trigger-function)) looks like this:

```
```
1
2
```



```
{
    "workspaceId": "ari:cloud:jira::site/3a1faf64-2f01-4d06-9ee3-fb11b0734e77",
    "eventType": "avi:cloud:ecosystem::event/d9022ad7-c220-4836-b1d1-7f9f2c633d3a/event-key",
    "name": "Event name",
    "environmentId": "0856b0e2-6fbe-449c-b515-d555cdce37ca",
    "environmentType": "DEVELOPMENT",
    "environmentKey": "default",
    "context": {
        "cloudId": "3a1faf64-2f01-4d06-9ee3-fb11b0734e77",
        "moduleKey": "my-trigger",
        "userAccess": {
            "enabled": false
        }
    },
    "contextToken": "<token>"
}
```
```

Where the properties specific to app events are:

* `workspaceId`: the workspace scope of the event exchange
* `name`: the name of the event
* `environmentId`, `environmentType`, `environmentKey`: information about the environment the publishing app is installed to

## Limitations

Below is a list of features that are missing in the current [preview](/platform/forge/whats-coming/#preview) version of App events.
Follow the [changelog](/platform/forge/changelog/) for any future updates.

* Events can be exchanged only within the scope of the same Atlassian app
* Publishing apps can't add any custom payload to the event

# Event

The `event` module defines a custom backend event type.

To publish the event, call this in your [function](/platform/forge/function-reference/index/):

```
1
2
import { appEvents } from '@forge/events';
const result = await appEvents.publish({'key': 'module-key'});
```

Apps can subscribe to the event with the [trigger](../trigger/) module,
referring to it by the following AVI (Atlassian eVent Identifier):

```
1
avi:cloud:ecosystem::event/{app-id}/{module-key}
```

where:

* `app-id` is the UUID of your app
* `module-key` is the key of the event module

---

For more details, see [App events](/platform/forge/events-reference/app-events/).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The key of the event. Part of the event AVI, and used in the publishing API to identify the event.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | A human-readable name of the event. |
| `allowedRecipients` | `Array<string>` | Yes | A list of apps allowed to receive the event.     * The publishing app can always receive its own event * To allow \_anyone\_ to receive the event, add the special `\*` wildcard character to the list * Use full app ARIs to specify allowed receiving apps (`ari:cloud:ecosystem::app/[uuid]`) |

#### Example

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
      allowedRecipients: ['*']
```
```

# events

The `events` API allows you to subscribe, unsubscribe, and emit events. This will allow
different Custom UI extensions *within the same app* to communicate with each other.

## on

The `on()` function allows you to subscribe to an event and invoke a provided `callback`
function when the event is triggered.

### Function signature

```
1
2
3
4
const on = (
    event: string,
    callback: (payload?: any) => Promise<any>
): Promise<Subscription>
```

### Arguments

* **event**: A string identifier representing the name of the event to listen to.
  This string should exactly match the `event` parameter in the corresponding `emit()` function.
* **callback**: A function, which takes a `payload`, that is called when the event is triggered.

### Returns

* **Subscription**: A `Subscription` which contains the `unsubscribe()` function.

### Example

```
1
2
3
4
5
6
7
import { events } from "@forge/bridge";

function eventHandler(payload?: any) {
  console.log("Payload: ", payload);
}

events.on("EVENT_NAME", eventHandler);
```

## unsubscribe

The `unsubscribe()` function for an event can be accessed through the `Subscription` object
that was returned from the `on()` function for that event.

Calling `Subscription.unsubscribe()` will remove the event listener for the specific `Subscription`
instance and will not globally unsubscribe from the event.

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
import { events } from "@forge/bridge";

// Subscribe to the event.
// If the event is fired, both eventHandler1 and eventHandler2 will be called.
const subscription1 = events.on("EVENT_NAME", eventHandler1);
const subscription2 = events.on("EVENT_NAME", eventHandler2);

// Unsubscribe from the event.
// Only subscription1 will be unsubscribed. If the event is fired again, eventHandler1 will not be called but eventHandler2 will.
subscription1.then((subscription) => subscription.unsubscribe());
```
```

## emit

The `emit()` function will trigger a specific `event` with the provided `payload` and returns
`Promise<void>`. If you have subscribed to this `event` with the `on()` function, your callback
will be invoked.

### Function signature

```
```
1
2
```



```
const emit = (event: string, payload?: any): Promise<void>;
```
```

The event payload supports the following types:

* `string`
* `number`
* `boolean`
* `blob`
* `null`
* objects or arrays of the above types

### Example

In this example, the `emit()` and `on()` functions are defined in two separate resource files.
These resources are then defined in the manifest file to be loaded as two different Custom UI modules.
These separate Custom UI modules can communicate with each other by using the `events` API .
To learn more about defining Custom UI modules, see [Custom UI](/platform/forge/custom-ui/).

**`on.js`**

```
```
1
2
```



```
import { events } from "@forge/bridge";

function eventHandler(payload?: any) {
  if (payload) {
    console.log(`Payload: ${payload}`);
  }
}

events.on("EVENT_NAME", eventHandler);
```
```

**`emit.js`**

```
```
1
2
```



```
import { events } from "@forge/bridge";

const payload = "PAYLOAD";

events.emit("EVENT_NAME", payload);
```
```

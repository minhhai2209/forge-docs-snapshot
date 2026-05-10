# Consumer

The `consumer` module defines the function for the queue to process the `async events`.
For more information about this feature, see [async events](/platform/forge/runtime-reference/async-events-api/).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `queue` | `string` | Yes | The name of the queue for which the consumer processes the events asynchronously. |
| `function` | `string` | Yes (when using `@forge/events` v2+) | A reference to the function module that will be invoked when events are pushed to the queue of this consumer module. Use this property when using `@forge/events` version 2 or later. |
| `resolver` | `object` | Yes (when using `@forge/events` v1.x) | **Deprecated.** Used with `@forge/events` version 1.x. Specifies the resolver function and method to invoke when events are pushed to the queue. Replaced by the `function` property in `@forge/events` v2+.  Contains the following properties:   * `function` (`string`, required): A reference to the function module that handles the event. * `method` (`string`, required): The name of the resolver method defined using `resolver.define()` that is called when an event is received. |
| `crossVersion` | `boolean` | No | When set to `true`, this property ensures that async events are processed even if the application version changes before the event processing begins.  Note that event processing begins after the `delayInSeconds` duration specified in the [Push API](/platform/forge/runtime-reference/async-events-api/#push-api).  This is a temporary property, and will be removed after `21 November 2025`. See [changelog](/platform/forge/changelog/#CHANGE-2526) for more details. |

## Example

The following examples show the two supported syntaxes for the `consumer` module.

**`@forge/events` v2+ (recommended)**

```
```
1
2
```



```
modules:
  consumer:
    - key: my-queue-consumer
      queue: my-queue
      function: myQueueFunction
  function:
    - key: myQueueFunction
      handler: index.handler
```
```

**`@forge/events` v1.x (deprecated)**

```
```
1
2
```



```
modules:
  consumer:
    - key: my-queue-consumer
      queue: my-queue
      resolver:
        function: myQueueFunction
        method: my-queue-listener
  function:
    - key: myQueueFunction
      handler: index.handler
```
```

See [Upgrade to @forge/events major version 2](/platform/forge/runtime-reference/async-events-api-version-2-upgrade/) for details on migrating from v1.x to v2+.

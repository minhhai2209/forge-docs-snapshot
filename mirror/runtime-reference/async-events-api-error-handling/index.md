# Async events API Reference

|  |  |
| --- | --- |
| `PartialSuccessError` | Some pushed events were not recorded for later processing. Each event can have a different reason for failure. To get error details for failed events, inspect the error's `failedEvents` property [here](#tip-menu-code). |
| `RateLimitError` | The total number of events pushed per minute exceeds the defined limits. To overcome this, retry adding events after a minute. |
| `TooManyEventsError` | More than 50 events were pushed to the queue in a single request. See [Async events limits](/platform/forge/limits-async-events/) for more details about this limit. |
| `PayloadTooBigError` | The combined payload of events pushed in a single request exceeded 200 KB. See [Async events limits](/platform/forge/limits-async-events/) for more details about this limit. |
| *Invalid event shape* | A pushed event is not an object (`Event must be an object.`), or it has no `body` object (`Event body must be an object.`). See [Event shape](/platform/forge/runtime-reference/async-events-api/#event-shape) for the structure `Queue.push()` expects. |
| `InvalidPushSettingsError` | The `delayInSeconds` setting of a pushed event is outside the supported range of 0 to 900 seconds. |
| `InvalidQueueNameError` | The queue name is invalid. A valid queue name is alphanumeric string, and can start with `_`. |
| `InvocationLimitReachedError` | An event resolver can push more events to the queue, creating a cycle. This error means an event pushed another event into the queue more than 1000 times. To avoid this, process more events in parallel. See [Async events limits](/platform/forge/limits-async-events/) for more details about this limit. |

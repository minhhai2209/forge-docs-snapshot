# Async events limits

|  |  |  |
| --- | --- | --- |
| Event per request | 50 | Maximum number of events pushed in a single request. |
| Event per minute | 500 | Maximum number of events pushed in one minute. |
| Payload size | 200 KB | Maximum combined payload size of events in single request. |
| Retry data size | 4 KB | Maximum size of `retryData`.  This will be enforced from `Nov 13, 2025`. See [CHANGE-2508](/platform/forge/changelog/#CHANGE-2508) for more details. |
| Payload size for long running functions | 100 KB | Maximum size of an *individual* event.  This limit only applies to functions specifying a timeout greater than 55 seconds. |
| Retry data size for long running functions | 4 KB | Maximum size of `retryData`.  This limit only applies to functions specifying a timeout greater than 55 seconds. |
| Cyclic invocation limit | 1000 | An event resolver can push more events to the queue, which may trigger further event handlers in a chain. This limit applies to the total number of **async event push requests** that can be made across all handlers originating from a single initial function invocation, including requests made by downstream handlers. Each push request can contain up to 50 events. For example, a function that calls push 1000 times in a loop, or a chain where each handler calls push once for 1000 hops, both reach this limit. |

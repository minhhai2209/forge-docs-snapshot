# frontendCustomMetrics

The `frontendCustomMetrics` bridge API lets you emit custom metrics from your app's frontend (browser-side) code using [@forge/bridge](https://www.npmjs.com/package/@forge/bridge). The Forge platform automatically attaches your app's identity and context, so no tokens or resolver functions are required.

Before emitting a metric, you must first [register it](/platform/forge/monitor-custom-metrics/#register-a-custom-metric) in the developer console.

Frontend custom metrics work even for apps with no resolver.

`counter` is currently the only supported metric type. Other metric types (such as gauge or histogram) aren't available. Additional metric types may be added in future releases.

## counter

Returns a `Counter` object for the named metric. Use it to increment the metric value when a tracked event occurs.

### Function signature

```
1
frontendCustomMetrics.counter(name: string): Counter
```

The `Counter` interface is exported from `@forge/bridge`:

```
1
2
3
4
interface Counter {
  incr: () => Promise<void>;
  incrBy: (value: number) => Promise<void>;
}
```

### Arguments

| Argument | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | The name of the registered custom metric. Must exactly match the name registered in the developer console. The name is validated on the client: it must be 1–50 characters, start and end with an alphanumeric character, contain only letters, numbers, dots (`.`), and hyphens (`-`), and must not contain consecutive dots or hyphens. An invalid name throws a `BridgeAPIError`. |

### Returns

A `Counter` object with the following methods. Both methods are asynchronous and return a `Promise<void>`:

| Method | Description |
| --- | --- |
| `incr()` | Increments the counter by 1. |
| `incrBy(value: number)` | Increments the counter by the specified `value`. The value must be a positive number; passing `0` or a negative number throws a `BridgeAPIError` synchronously, before any metric is emitted. |

If you call `counter()` with a name that isn't registered in the developer console, no error is thrown — the metric is silently dropped and never counted. Make sure the name exactly matches a metric [registered](/platform/forge/monitor-custom-metrics/#register-a-custom-metric) in the developer console.

### Example

```
```
1
2
```



```
import { frontendCustomMetrics } from '@forge/bridge';

const onButtonClick = () => {
  const counter = frontendCustomMetrics.counter('jira-actions-success');

  counter.incr();       // Increment by 1
  counter.incrBy(5);    // Increment by a specific value
};
```
```

## Rate limits

There are no frontend-specific rate limits for custom metrics at this time. General [Forge platform quotas and limits](/platform/forge/platform-quotas-and-limits/) still apply.

# Scheduled trigger

The `scheduledTrigger` module repeatedly invokes a function on a scheduled interval. Each trigger
is scheduled to start shortly after it is created, about 5 minutes after app deployment.
It then runs based on the configured interval `fiveMinute`, `hour`, `day`, or `week`.

The optional `timeoutSeconds` parameter of the [function](/platform/forge/manifest-reference/modules/function/#properties) module specifies the maximum runtime for a scheduled trigger function, enabling it to run longer than the default of 55 seconds.
You can specify up to 900 seconds (15 minutes). See [Platform quotas and limits](/platform/forge/platform-quotas-and-limits/#invocation-limits) for a complete list of related limits.

Every time any changes are made to any scheduled triggers `module`, all scheduled triggers will be
recreated and their start times reset.

Scheduled triggers run without a user context, which means the `principal` field of the
`context` argument doesn't represent a user. If a function invoked from a scheduled trigger
returns a value, it is ignored. If the function throws an error, nothing will happen,
and the function invocation will not be retried. The function will be invoked the next time the
schedule is due.

Apps can declare up to five scheduled triggers in the `manifest.yml` file.

Not all invocations for a single scheduled trigger will happen at once. To better improve overall performance,
invocations will be distributed in batches evenly across the interval specified on any given `module`. Distribution is done
by installations, so not all installations of an app will have their triggers invoked together. This is however a
consistent distribution, meaning that if an hourly trigger invokes at 1:10 for a particular installation, and
at 1:20 for another, those installations will invoke again at 2:10 and 2:20 respectively.

There is a small chance of duplicated invocations, such scenarios should be handled in the apps code by
the app developer.

For step-by-step instructions on how to use this module type, see the following tutorials:

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `endpoint` | `string` | Yes (if no `function` is specified). | A reference to the `endpoint` [specifying the remote back end](/platform/forge/manifest-reference/endpoint/) that resolves your event (if you are using [Forge Remote).](/platform/forge/forge-remote-overview) |
| `interval` | `'fiveMinute'`, `'hour'`, `'day'`, `'week'` | Yes | The interval at which to invoke the function. |

### Example

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: example-scheduled-trigger
      function: my-scheduled-function
      interval: hour # Runs hourly
  function:
    - key: my-scheduled-function
      handler: index.trigger
      timeoutSeconds: 60 #Optional. Maximum time (in seconds) this function can run when triggered by a schedule or as an async event consumer. Range: 1–900 seconds.
```
```

Handler function in `index.js`

```
```
1
2
```



```
// index.js

export const trigger = ({ context }) => {
  console.log("Scheduled trigger invoked");
  console.log(context);
  // Add your business logic here
};
```
```

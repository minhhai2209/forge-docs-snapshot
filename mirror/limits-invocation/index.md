# Invocation limits

|  |  |  |
| --- | --- | --- |
| Runtime seconds  (also includes UI modules invoked by Forge Remote) | 25 | Maximum runtime permitted before the app is stopped. |
| Runtime seconds  (events invoked by Forge Remote) | 5 | Maximum runtime permitted before the app is stopped. This applies to remote back ends receiving events from the Atlassian platform. |
| Runtime seconds (async events and scheduled trigger module) | 900 | This applies to function modules that are only referenced by consumer or scheduled trigger modules. Default timeout is 55 seconds. Use [timeoutSeconds](/platform/forge/manifest-reference/modules/function/) to extend it. |
| Runtime seconds  (web-triggers) | 55 | Maximum runtime permitted before the app is stopped. |
| Single outbound request timeout (async events) | 180 | Maximum time a single outbound request can take before being terminated. Outbound requests refer to fetch requests, including both Atlassian app REST API and external API requests. This limit can only be reached using [long-running functions](/platform/forge/use-a-long-running-function/). |
| Log lines per invocation | 100 per runtime minute (rounded up) | Maximum number of log entries for an invocation. The limit is calculated based on the function timeout, specified by `timeoutSeconds`, rounded up per minute.  * A function without a timeout declared is limited to 100 log lines. * A function with `timeoutSeconds: 90` (a minute and a half) is limited to 200 log lines. |
| Log size per invocation | 200 KB | Maximum size of all log line data generated per invocation. |
| Log file size per download | 100 MB | Maximum file size of filtered logs per download. |
| Log lines per download | 96,000 | Maximum number of log entries per download. |
| Egress requests | 100 per runtime minute (rounded up) | Number of network requests per invocation, excluding those made using `requestJira` or `requestConfluence`. The limit is calculated based on the function timeout, specified by `timeoutSeconds`, rounded up per minute.  * A function without a timeout declared is limited to 100 requests. * A function with `timeoutSeconds: 90` (a minute and a half) is limited to 200 requests. |
| Egress requests | 50,000 requests per minute, per app for egress calls | The maximum number of requests per minute that an app can make for egress calls, excluding those made using `requestJira` or `requestConfluence`. |
| Network requests | 3,000,000 requests per minute, per app and 100,000 requests per minute, per app, per tenant | The maximum number of requests per minute that an app can make for network calls, including those made using `requestJira` or `requestConfluence`. |
| Memory | 1,024MB | Available memory per invocation. Default memory limit is 512MB. To change it, use the `memoryMB` setting of the `runtime` [property](/platform/forge/manifest-reference/#runtime). |
| Front-end invocation request payload size | 500KB | The maximum request payload size for a front-end invocation (for example, `invoke` and `invokeRemote` via `@forge/bridge`). |
| Front-end invocation response payload size | 5MB | The maximum response payload size from a front-end invocation (for example, `invoke` and `invokeRemote` via `@forge/bridge`). |

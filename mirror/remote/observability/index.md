# Remote observability

Options for error metrics, logs, and tracing are available for Forge Remote.

## Metrics

Metrics on remote invocations and errors encountered are available in the [developer console](/console/myapps/).

The `Remote` error type shows the count of remote invocation errors.

![Developer console invocation errors graph showing remote invocation errors](https://dac-static.atlassian.com/platform/forge/images/remote-dev-console-invocation-errors.png?_v=1.5800.1869)

## Logs

Remote invocations are included in the Forge logs in the [developer console](/console/myapps/) and the [CLI](/platform/forge/cli-reference/logs/).

![Developer console showing remote invocation logs](https://dac-static.atlassian.com/platform/forge/images/remote-dev-console-invocation-logs.png?_v=1.5800.1869)

# Exporting app logs

[Use the App logs API](/platform/forge/export-app-logs/) to export app logs to observability tools, including Splunk, Datadog, Dynatrace, New Relic, and more.

## Tracing

To help with diagnosing issues Atlassian will provide the following trace headers as part of each request as well as part of the invocation body. If you provide this `traceId` in any support correspondence with Atlassian this should help speed up the resolution of any issues.

You can also optionally join this trace on the remote endpoint side and propagate these values onto any Atlassian app and platform APIs you need to call.

| Header | Explanation |
| --- | --- |
| `x-b3-traceid` | The TraceId is 64 or 128-bit in length and indicates the overall ID of the trace. Every span in a trace shares this ID. |
| `x-b3-spanid` | The SpanId is 64-bit in length and indicates the position of the current operation in the trace tree. The value should not be interpreted: it may or may not be derived from the value of the TraceId. |

# App observability in third-party tools

App observability provides data that can help understand app performance at any given time, as well as
provide access to accurate information about where and why an app may be failing or needing improvement.

You can view and monitor
[invocation metrics](/platform/forge/monitor-invocation-metrics/),
[API metrics](/platform/forge/monitor-api-metrics/), and
[app logs](/platform/forge/monitor-app-logs/) in the
[developer console](/console/myapps).

You can also choose to export metrics and logs to several observability tools of your choice,
including [SignalFX](https://www.splunk.com/) and [Datadog](https://www.datadoghq.com/).
Such tools offer capabilities, like grouping and filtering metrics by different attributes
and integrating logs with incident response tools.

## OpenTelemetry framework

[OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) is an
[observability](https://opentelemetry.io/docs/concepts/observability-primer/#what-is-observability)
framework and toolkit designed to create and manage telemetry data, such as
[traces](https://opentelemetry.io/docs/concepts/signals/traces/),
[metrics](https://opentelemetry.io/docs/concepts/signals/metrics/), and
[logs](https://opentelemetry.io/docs/concepts/signals/logs/).
OpenTelemetry uses a standard format for how observability data is collected and sent to tools
and services.

The [OpenTelemetry Protocol](https://opentelemetry.io/docs/specs/otlp/) (OTLP) specification
describes the encoding, transport, and delivery mechanism of telemetry data between telemetry
sources and intermediate nodes, such as collectors and telemetry backends.

The [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) (OTEL) offers a
vendor-agnostic implementation of how to receive, process, and export telemetry data. It removes
the need to run, operate, and maintain multiple agents or collectors. This works with improved
scalability and supports open source observability data formats, such as Jaeger, Prometheus,
Fluent Bit, and more, sending to one or more open source or commercial backends.

App metrics show you how your Forge app is currently performing across all sites on which your app
is installed.

You can use the **App metrics API** to export app metrics to several observability tools.
The App metrics API is an [Atlassian GraphQL](/platform/atlassian-graphql-api/graphql/)
metrics API that provides metrics in the
[OTLP protobuf JSON](https://protobuf.dev/programming-guides/proto3/#json) format, which is
the format used in the
[OpenTelemetry framework](/platform/forge/app-metrics-in-third-party-tools/#opentelemetry-framework).

You can only use the [OpenTelemetry framework](#opentelemetry-framework)
when using the App metrics API to export metrics to observability tools.

### Authentication with the Atlassian GraphQL Gateway

You must first
[authenticate with the Atlassian GraphQL Gateway (AGG)](/platform/atlassian-graphql-api/graphql/#authentication)
to consume the API and export app metrics to a tool of your choice.

The Atlassian account making the request must be the same account that owns the Forge app.

To get started using basic authentication:

1. Go to <https://id.atlassian.com/manage/api-tokens>.
2. Select **Create API token**.
3. Enter a label to describe your API token. For example, *export-metrics-api-token*.
4. Select **Create**.
5. Select **Copy to clipboard** and close the dialog.
6. Include the token and your email in the header of your GraphQL request.
7. Pass the `X-ExperimentalAPI` header. This is because the API is still in the experimental phase
   and is subject to change.
8. Provide a custom `User-Agent` header. This helps differentiate traffic coming from
   the developer console and your own export service. We recommend using this value:
   `ForgeMetricsExportServer/1.0.0`

Now you're ready to start [exporting your Forge app metrics](/platform/forge/export-app-metrics/).

App logs help in tracking down and troubleshooting issues that app users may be experiencing.
Forge app owners and
[app contributors](/platform/forge/manage-app-contributors/) can view app logs.

You can use the **App logs API** to export app logs to observability tools. The App logs API
is a REST API that provides logs in the [OTLP log data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
([example](https://github.com/open-telemetry/opentelemetry-proto/blob/v1.1.0/examples/logs.json)), which is the format used in the
[OpenTelemetry framework](/platform/forge/app-metrics-in-third-party-tools/#opentelemetry-framework).

While we recommend using the [OpenTelemetry framework](#opentelemetry-framework)
when exporting logs to observability tools, you can choose to use libraries specific to
your tool of choice.

### Authentication with the Atlassian Gateway

You must first authenticate with the Atlassian Gateway to consume the API and export app logs
to a tool of your choice. For this you need to generate the API tokens to access the App logs API.

Only the owner of the Forge app or an app contributor that has access to logs can make the request.
It is recommended to use a non human account (bot account), instead of an admin account, which has access to the app logs.

To generate the API tokens:

1. Go to <https://id.atlassian.com/manage/api-tokens>.
2. Select **Create API token**.
3. Enter a label to describe your API token. For example, *export-logs-api-token*.
4. Select **Create**.
5. Select **Copy to clipboard** and close the dialog.
6. Use this token as a Basic Authorization when making request to the API.

Now you're ready to start [exporting your Forge app logs](/platform/forge/export-app-logs/).

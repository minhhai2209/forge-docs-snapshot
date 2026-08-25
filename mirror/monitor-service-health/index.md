# Monitor container metrics (Preview)

Forge Container services is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#forge-preview).

Service Health monitoring provides real-time visibility into the health and performance of your
[Forge Container](/platform/forge/containers-reference/) services. You can view these metrics in the
developer console to monitor resource usage and service availability.

Service Health metrics are available only for apps that use
[Forge Container services](/platform/forge/containers-reference/). These metrics are not available for
standard Forge function-based apps.

## View Service Health metrics

To view Service Health metrics for your container services:

1. Access the [developer console](/console/myapps).
2. Select the Forge app that uses Forge Container services.
3. Select **Metrics** in the left menu.
4. Select **Service Health** in the left menu.

The Service Health page displays a table of your container services with the following information:

| Column | Description |
| --- | --- |
| **Service Instance** | The name of the container service. |
| **Status** | Indicates whether the service is receiving production traffic. Possible values are `Available` and `Unavailable`. |
| **Region** | The region where the service is deployed. |
| **Instances** | The number of currently running instances out of the maximum configured instances. |
| **Avg. CPU** | The average CPU usage across all container instances within the service, shown as a percentage. |
| **Avg. Memory** | The average memory usage across all container instances within the service, shown as a percentage. |
| **Deployed at** | The date and time the service was last deployed. |
| **Action** | Link to view the logs for the service. |

The Service Health page shows the current state of your services at the time the page loads. The page
does not update automatically. To see the latest metrics, use the **Refresh** button or reload the page.

## Filter metrics

Use the filters at the top of the Service Health page to narrow the displayed data:

* **Environment**: Select a single environment to view metrics for. Only one environment can be
  selected at a time.
* **Region**: Select one or more regions to filter by. By default, all regions are selected. Use
  **Select all** and **Clear selections** to manage your selections. Clearing all selections defaults
  back to showing all regions.
* **Reset to default**: Resets the environment filter to `production` and the region filter to all
  regions.

The service table supports pagination with **Previous** and **Next** controls. The default page size
is 10 services.

## Available metrics

The following Service Health metrics are available for Forge Container services:

| Metric | Type | Description |
| --- | --- | --- |
| `container_cpu_usage_percentage` | Gauge | Container CPU usage as a percentage of the container's CPU limit. |
| `container_memory_usage_percentage` | Gauge | Container memory working-set usage as a percentage of the container's memory limit. Working set is the memory used for out-of-memory (OOM) decisions. |
| `service_instance_count` | Gauge | The number of running instances for a container service in a given region. |
| `container_uptime_seconds` | Gauge | The number of seconds a container has been running since it last started. |
| `container_status_restarts_total` | Cumulative Counter | The total number of times a container has restarted. This counter resets to zero when the pod is replaced. |

## Export container metrics

You can export Service Health metrics using the
[App metrics API](/platform/forge/export-app-metrics/). To export container metrics,
include the following values in the `query.filters.metrics` array of your API request:

* `CONTAINER_CPU_USAGE_PERCENTAGE`
* `CONTAINER_MEMORY_USAGE_PERCENTAGE`
* `SERVICE_INSTANCE_COUNT`
* `CONTAINER_UPTIME_SECONDS`
* `CONTAINER_STATUS_RESTARTS_TOTAL`

For details on setting up metrics export, see
[Export app metrics](/platform/forge/export-app-metrics/).

The following tags and dimensions are available with container metrics when using the App metrics API:

| Tag | Description | Applicable metrics |
| --- | --- | --- |
| `appId` | The unique identifier for the Forge app. | All container metrics |
| `environmentId` | The environment UUID. | All container metrics |
| `serviceKey` | The service key as defined in the manifest. | All container metrics |
| `region` | The region where the service instance is running. | All container metrics |
| `cluster_uid` | The cluster where the service instance is running. | All container metrics |
| `container` | The container name. | `container_cpu_usage_percentage`, `container_memory_usage_percentage`, `container_uptime_seconds`, `container_status_restarts_total` |
| `pod` | The pod identifier for the container instance. | `container_cpu_usage_percentage`, `container_memory_usage_percentage`, `container_uptime_seconds`, `container_status_restarts_total` |

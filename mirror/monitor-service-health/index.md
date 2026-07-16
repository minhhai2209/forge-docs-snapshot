# Monitor container metrics (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Service Health monitoring provides real-time visibility into the health and performance of your
[Forge Container](/platform/forge/containers-reference/) services. You can view these metrics in the
developer console to monitor resource usage and service availability.

Service Health metrics are available only for apps that use
[Forge Containers](/platform/forge/containers-reference/). These metrics are not available for
standard Forge function-based apps.

## View Service Health metrics

To view Service Health metrics for your container services:

1. Access the [developer console](/console/myapps).
2. Select the Forge app that uses Forge Containers.
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

## Export container metrics

You can export Service Health metrics using the
[App metrics API](/platform/forge/export-app-metrics/). To export container metrics,
include the following values in the `query.filters.metrics` array of your API request:

* `CONTAINER_CPU_USAGE_PERCENTAGE`
* `CONTAINER_MEMORY_USAGE_PERCENTAGE`
* `SERVICE_INSTANCE_COUNT`

For details on setting up metrics export, see
[Export app metrics](/platform/forge/export-app-metrics/).

The following tags and dimensions are available with container metrics when using the App metrics API:

| Tag | Description | Applicable metrics |
| --- | --- | --- |
| `appId` | The unique identifier for the Forge app. | All container metrics |
| `environmentId` | The environment UUID. | All container metrics |
| `serviceKey` | The service key as defined in the manifest. | All container metrics |
| `region` | The region where the service instance is running. | All container metrics |
| `container` | The container name. | `container_cpu_usage_percentage`, `container_memory_usage_percentage` |
| `pod` | The pod identifier for the container instance. | `container_cpu_usage_percentage`, `container_memory_usage_percentage` |

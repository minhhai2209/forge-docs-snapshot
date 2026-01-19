# Monitor invocation metrics

Invocation metrics are indicators of the outcome of a Forge app function invocation. When monitoring
invocation metrics for your app, we recommend using [filters](#filters) to refine the results.

To view invocation metrics:

1. Access the [developer console](/console/myapps).
2. Select the Forge app that you want to view metrics for.
3. Select **Metrics** in the left menu.
4. Select **Invocation** in the left menu.

The image below shows invocation metrics, as well as all sites that your Forge app is currently
installed on, and where there has been at least one invocation in the [selected time period](#filters).
If there hasn't been any invocation, the charts won't show any data.

![Metrics screen](https://dac-static.atlassian.com/platform/forge/images/metrics-screen.svg?_v=1.5800.1779)

## Invocation metrics

The following metrics are available for all `function` invocations.

* **Invocation success rate**: The percentage of successful vs. failed invocations,
  across all functions. An invocation is considered successful if the function doesn’t fail
  with an invocation error.
* **Invocation count**: The total number of invocations, regardless of success or failure.
* **Invocation errors**: The number of invocations that failed with an error. They are grouped
  into the following error types:
  * **Out of memory**: The function has exhausted the
    [available memory](/platform/forge/platform-quotas-and-limits/#invocation-limits).
  * **Timeout**: The function has not been successful within a
    [time limit](/platform/forge/platform-quotas-and-limits/#invocation-limits).
  * **Deprecated Runtime**: The function is using a [deprecated runtime](https://developer.atlassian.com/platform/forge/changelog/#CHANGE-789).
    We recommend that all apps [upgrade to the current Node.js runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).
    If needed, you can [backport](/platform/forge/versions/#backporting) minor version updates to older major versions of your app.
  * **Unhandled exception**: The function threw an uncaught exception. This category may
    include exceeding other platform limits such as
    [network requests](/platform/forge/platform-quotas-and-limits/#invocation-limits).
    To learn more about why the exception was thrown, view your app logs
    by selecting **Logs** in the left hand menu. For more information, see
    [View app logs](/platform/forge/view-app-logs/).
* **Invocation time**: The time it takes for each [function](/platform/forge/manifest-reference/modules/function/)
  under the handler field in the app `manifest.yml` file to successfully complete an invocation.
  The chart shows the distribution of invocation time as a histogram across different time buckets.
  The time is measured from inside the AWS lambda, and doesn't include cold start, but it includes
  the time it took for the lambda initialization phase to complete.

Each metric is displayed as both a chart and a value. The value, displayed at the top of the screen, represents the overall or total value for that metric and includes any applied filters.

This doesn’t include code executing in a Custom UI iframe, but includes functions invoked by `@forge/bridge`.

## Invocation errors

To learn more about your app's invocation errors, select the chart title, or select
the **More actions (**⋯**)** menu on the chart and **View details**.

The following screen appears, showing site-specific information about your app's invocation errors.

![Invocation errors detailed view](https://dac-static.atlassian.com/platform/forge/images/invocation-errors-detailed-view.svg?_v=1.5800.1779)

In this view, you can search, filter, and sort the data to identify errors across specific sites
and installations. You can also group the chart by version and error type, by selecting
the **Group chart by** dropdown above the chart.

* Metrics are shown according to the selected time range.
* The data displayed in the chart will be filtered according to the sites selected in the table.
* By default, the table is sorted by error count, but you can sort by any column.

## Invocation time

To learn more about your app's invocation time, select the chart title, or select
the **More actions (⋯)** menu on the chart and **View details**.

The following screen appears, showing function-specific information about your app's invocation time.

![Invocation time detailed view](https://dac-static.atlassian.com/platform/forge/images/invocation-time-detailed-view.svg?_v=1.5800.1779)

In this view, you can search, filter, and group the data to see invocation time across
specific functions, environments, and time periods.

You can also see a summary of the following percentiles involving the invocation time of the Forge
app:

* **P50 - Median**
  * Indicates the value of the response time that's faster or equal to 50% of the app's speed
    of function invocations.
  * This is the typical performance of your app's speed of function invocations and is not skewed
    by extreme values.
* **P90 - 90th percentile**
  * Indicates the value of the response time that's faster or equal to 90% of the app's speed
    of function invocations.
  * If the P90 value is 170 ms, this means that the response times of 90% of the requests your
    app receives is less than or equal to 170 ms.
  * This helps give an understanding of what the slowest 10% of users may be experiencing with
    their response times.
* **P95 - 95th percentile**
  * Indicates the value of the response time that's faster or equal to 95% of the app's speed
    of function invocations.
  * If the P95 value is 170 ms, this means that the response times of 95% of the requests your
    app receives is less than or equal to 170 ms.
  * This helps give an understanding of what the slowest 5% of users may be experiencing with
    their response times.

To group the chart by function or version, select the **Group chart by** dropdown above the chart.
Note, this will only reflect in the chart data, not in the table data.

* Metrics are shown according to the selected time range and the selected deployment environment.
* By default, the table is sorted in descending order of invocation time, meaning functions
  with the longest invocation time will appear at the top. However, you can sort by any column.

## Filters

Use these filters to refine your metrics:

* **Environment**: Narrows down the metrics for a specific app environment
  for your app.
* **Date**: Narrows down the metrics based on your chosen time interval. Choose from a range of
  predefined values, such as the **Last 24 hours**, or choose a more specific time interval using
  the **Custom** option.
* **Sites**: Narrows down the metrics based on the sites that your app is
  installed onto, for example, `<your-site>.atlassian.net`. You can select multiple sites.
* **Atlassian app**: Narrows down the metrics to show data from a specific Atlassian app if your Forge app supports multiple Atlassian apps.

Each metric can also be grouped by [app version](/platform/forge/environments-and-versions/#versions)
or [function](/platform/forge/manifest-reference/modules/function/), by selecting
the **Group by** dropdown next to a chart.

* Metrics are only shown for sites with at least one invocation in the past 14 days.
* All dates are in Coordinated Universal Time (UTC).
* Each chart's data resolution depends on the time interval you've selected. For example
  'Last 24 hours' shows data at a 30-minute resolution, and 'Last hour' shows data at a
  1-minute resolution.
* Metrics may not always be accurate because undelivered metrics data isn’t back-filled
  and data sampling might be used for some metrics.

You can bookmark the URL on your browser to access metrics based on specific filtering
criteria for quick access.

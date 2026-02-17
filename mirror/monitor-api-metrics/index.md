# Monitor API metrics

API metrics help identify issues with and optimize the performance of APIs being used by apps.
This helps ensure apps are delivering expected results. When monitoring API metrics, we recommend
using [filters](#filters) to refine the results.

To view API metrics:

1. Access the [developer console](/console/myapps).
2. Select the Forge app that you want to view metrics for.
3. Select **Metrics** in the left menu.
4. Select **API** in the left menu.

The image below shows API metrics, as well as all sites that your Forge app is currently
installed on, and where there has been at least one invocation in the [selected time period](#filters).
If there hasn't been any invocation or if the app isn't using any APIs, the charts won't show any data.

![Metrics screen](https://dac-static.atlassian.com/platform/forge/images/api-metrics-screen.svg?_v=1.5800.1853)

To view API metrics on the developer console, make sure to redeploy your app with the
[latest version of Forge CLI](/platform/forge/cli-reference/#upgrading)
by running `forge deploy` in your terminal.

## API metrics

The following metrics are available for monitoring in the developer console:

## API status codes

HTTP response status codes are indicators of whether or not a specific HTTP request has been
successfully completed. When monitoring API performance, you can scan the volume of the
most frequent responses for each status code. The data resolution of each chart depends on the
[time interval](#filters) you've selected.

You can see a summary of the following status codes in the developer console:

| Status code | Description |
| --- | --- |
| **2xx - Success** | * Indicates client requests that are successfully received, understood, and processed by the server. * The chart shows the total volume of successful API responses against the selected time interval. |
| **3xx - Redirection** | * Indicates that the client must take additional action to complete the request. * These are often used when the requested resource has moved to a different location. |
| **4xx - Client errors** | * Indicates that there's an issue with the client's request, such as invalid credentials or a mistyped URL that's resulting in a non-existing page. These issues must be fixed on the client's side before retrying the request. * The chart shows a breakdown of the volume of the most frequent client error responses against the selected time interval. * Use the [detailed view](#further-analysis-of-api-status-codes) to perform a more in-depth analysis of specific error scenarios. To access this view, click **More details**. |
| **5xx - Server errors** | * Indicates that the server is experiencing errors or is unable to fulfill a valid request. These issues must be fixed on the server's side before retrying the request. * The chart shows a breakdown of the volume of the most frequent server error responses against the selected time interval. * Use the [detailed view](#further-analysis-of-api-status-codes) to perform a more in-depth analysis of specific error scenarios. To access this view, click **More details**. |

### Further analysis of API status codes

Both **4xx - Client errors** and **5xx - Server errors** status codes have detailed views,
which provide a more granular perspective of the errors occurring in the APIs your app
is using.

You can navigate to the [request URL](#request-urls) and [site](#sites) tabs to facilitate
efficient debugging and issue resolution. Use the tabs in conjunction to understand the current
status of your app's APIs, narrow down troubleshooting efforts efficiently, and optimize
the API performance of your app.

#### Request URLs

Use the **Request URL** tab to narrow down on API errors based on distinct URLs. This helps identify
which API is generating a high number of errors. You can also use [filters](#filters) to
further refine the results.

The image below provides a detailed view of the API metrics status code, with the request URL tab
selected. It shows a chart and a table that displays the URLs invoked within the
[selected time period](#filters).

![API status code detailed view request url tab](https://dac-static.atlassian.com/platform/forge/images/api-status-codes-req.svg?_v=1.5800.1853)

The chart visually shows a breakdown of the volume of the most frequent client error responses against
the selected time interval. This lets you quickly spot problematic APIs.

The table below the chart displays the exact number of errors each problematic API returns.
This provides insights into the extent of the problem each API is causing, as well as shows you
the APIs causing the most issues. You can sort the values in the table by ascending or descending
order by clicking the column headers.

Some request URLs may return an `unknown` value. This could be due to one of the following reasons:

* The site may be running on an older version of your app. If this happens, we recommend that you
  encourage your users to upgrade to the latest version of your app. Site admins may need to provide
  consent if a major version upgrade of their app is required.
* There may be issues matching the request URL with OpenAPI spec definitions of Atlassian apps.
  If this happens, we recommend checking if your app is using the correct request URL.

#### Sites

Use the **Sites** tab to narror down on API errors based on the sites where the errors are occurring.
This is particularly useful when you've identified a problematic request URL and you need to determine
whether the URL is causing issues across all sites or just a select few. You can also
use [filters](#filters) to further refine the results.

The image below highlights the API metrics status code, with the site tab selected. It provides
information about the distribution of errors across different sites.

![API status code detailed view sites tab](https://dac-static.atlassian.com/platform/forge/images/api-status-codes-sites.svg?_v=1.5800.1853)

The chart visually shows a breakdown of the error distribution across different sites.

The table below the chart provides a granular breakdown of errors by site. This lets you see at a glance
which sites are experiencing the most issues with the problematic URL. This helps narrow down
debugging efforts, so you can ensure the smooth operation of your app's APIs across all sites.
You can sort the error values in ascending or descending order by clicking the column headers.

## API response time

API response time is the total amount of time that it takes for an API to receive a request, process
the request, and send a response back to the client. Response time starts as soon as the client
initiates the request and ends as soon as the client receives a response from the server.

Percentiles are often used when measuring API response time. Percentiles provide a different view of
your API performance data. Data is sorted in a descending order and is measured at specific percentage
points.

When monitoring API response time, you can see a summary of the following percentiles involving
the response times of all HTTP requests being processed by your Forge app:

| Percentile | Description |
| --- | --- |
| **P50 - Median** | * Indicates the value of the response time that's faster or equal to 50% of all API responses. * This is the typical performance of your API and is not skewed by extreme values. |
| **P95 - 95th percentile** | * Indicates the value of the response time that's faster or equal to 95% of all API responses. * If the P95 value is 170 ms, this means that the API response times of 95% of the requests your app receives is less than or equal to 170 ms. * This helps give an understanding of what the slowest 5% of users may be experiencing with their response times. |
| **P99 - 99th percentile** | * Indicates the value of the response time that's faster or equal to 99% of all API responses. * If the P99 value is 170 ms, this means that the API response times of 99% of the requests your app receives is less than or equal to 170 ms. * This helps give an understanding of what the slowest 1% of users may be experiencing with their response times. |

You can also scan the latency of the 50th percentile, 95th percentile, and 99th percentile response
times of HTTP requests in the API response time chart. The data resolution of the chart depends on the
[time interval](#filters) you've selected.

### Further analysis of API response time

The detailed view of the API response time chart offers a more granular perspective of the overall
API performance of your app. This information makes it easy to identify and address any URLs tha
may be contributing to slower response times. You can also use [filters](#filters) to further refine the results.

The image below provides an in-depth look at the API response time chart, focusing on response times
for different percentile brackets.

![API response time detailed view screen](https://dac-static.atlassian.com/platform/forge/images/api-response-time-detailed.svg?_v=1.5800.1853)

The chart visually shows response times for the percentile brackets, **P50 - Median**, **P95 - 95th percentile**,
and **P99 - 99th percentile**. This information helps in assessing the speed at which your API
responds to requests, as well as in identifying significant delays that need your attention.

The table below the chart displays various request URLs and their corresponding response times. This
lets you quickly identify which URLs may be causing slower response times and address such issues
accordingly.

## Filters

Use these filters to refine your metrics:

* **Environment**: Narrows down the metrics for a specific app environment
  for your app.
* **Date**: Narrows down the metrics based on your chosen time interval. Choose from a range of
  predefined values, such as the **Last 24 hours**, or choose a more specific time interval using
  the **Custom** option.
* **Sites**: Narrows down the metrics based on the sites that your app is installed onto, for example,
  `<your-site>.atlassian.net`. You can select multiple sites. Note, this filter doesn't appear when
  you're on the **Site tab** of the [detailed views of API status codes](#further-analysis-of-api-status-codes).
* **Atlassian app**: Narrows down the metrics to show data from a specific Atlassian app if your Forge app supports multiple Atlassian apps.
* **API source**: Narrows down the metrics based on the origin of the APIs being used. Choose from
  **Atlassian app APIs**, **non-Atlassian APIs**, or **All APIs**.

Your filter selections persist across different API metrics. If you switch from one API metric
page to another, your chosen filters will remain active. This also applies to switching from detailed
views to the main API metrics page, as well as switching between tabs.

* Metrics are only shown for sites with at least one invocation in the past 14 days.
* All dates are in Coordinated Universal Time (UTC).
* Each chart's data resolution depends on the time interval you've selected. For example
  'Last 24 hours' shows data at a 30-minute resolution, and 'Last hour' shows data at a
  1-minute resolution.
* Metrics may not always be accurate because undelivered metrics data isn’t back-filled and
  data sampling might be used for some metrics.

You can also bookmark the URL on your browser to access metrics based on specific filtering criteria
for quick access. This is useful for repeated checks of the same metrics, saving time and effort in
reapplying preferred filters.

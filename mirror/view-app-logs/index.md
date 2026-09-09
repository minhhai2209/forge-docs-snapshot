# View app logs

Frontend logs are available as part of [Forge's Early Access Program (EAP)](/platform/forge/whats-coming/#eap). To get started, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/38/group/136/create/20612).

This feature is supported for both UI Kit and Custom UI across all environments, including production. It captures **console.error**, **uncaught exceptions**, and **unhandled promise rejections**.

App logs give you the information you need in order to [debug](/platform/forge/debugging/)
your apps. Logs are enabled by default when a user installs your app, and are displayed in the
developer console. If you need to view app logs for a site where the user has disabled log access,
you can ask them to [re-enable access](/platform/forge/access-app-logs/#re-enable-log-access).

For **Isolated Cloud (IC)**, customers don't have the option to enable or disable log sharing access to developers in [Admin Hub](https://admin.atlassian.com), and app developers can't access IC logs in the developer console. IC customers can still download the app logs from Admin Hub and share them with the developer. This is the only way for developers to get access to logs of an IC customer.

For **Atlassian Government Cloud (AGC) or FedRAMP**, customers can enable or disable log sharing access to developers in [Admin Hub](https://admin.atlassian.com), with sharing enabled by default. For more information, see [Access app logs](/platform/forge/access-app-logs/).

## View app logs

To view app logs:

1. Access the [developer console](/console/myapps).
2. In the left menu, select **Logs**.

The screen shows logs for all sites that users have granted you access to.

![A list of logs and the associated filters](https://dac-static.atlassian.com/platform/forge/images/logs-screen-new.png?_v=1.5800.2324)

A maximum of 20 log events are displayed by default. To view more log events, select **Load more logs**
at the bottom of the page.

## Log table

The table contains a list of your logs.

* **Level**: Displays the log level. This can be chosen by your app, by
  [inserting log statements](/platform/forge/debugging/) such as `console.log`, `console.warn`
  in your app's code. Unhandled errors are assigned the `Error` level, and include both app errors and
  platform errors.
* **Date/Time(UTC)**: Displays the time that the log was created in UTC.
* **Details**: Shows a concatenated preview of the log message. Select anywhere in a
  row to expand it and view the entire log message. See [Log messages](#log-messages) for more details.

Logs are shown for a single invocation. To see logs for another invocation, select
**Load logs for another invocation**.

## Log attributes

Expanding a row in the log table lets you view all log details, including the attributes
from the state of the app.

* **Invocation ID**: A unique identifier for the specific app invocation that generated the log lines.
* **Trace ID**: A request identifier that can be used to track log lines across different
  Forge invocations and remote API calls.
* **Module**: The name of the module where this log line was generated.
* **Function**: The name of the function where this log line was generated.
* **Version**: The [version](/platform/forge/environments-and-versions/#versions)
  of the app that's installed on the site.
* **Site**: The name of the site where the app was invoked from.
* **Environment**: The specific [environment](/platform/forge/environments-and-versions)
  (development, staging, or production) where the app is currently running in.
* **Atlassian app**: The Atlassian app onto which the Forge app is installed.
* **License**: The license status (active/inactive/trial) of your app installation if app is enabled for licensing
* **Edition**: The app edition value (standard/advanced) of your installation if app is enabled for editions

### Frontend log attributes ([EAP](https://ecosystem.atlassian.net/servicedesk/customer/portal/38/group/136/create/20612))

These attributes appear when you expand a frontend log.
See [Frontend log limits](/platform/forge/debugging/#frontend-log-limits) for how Forge truncates oversized frontend log data.

* **Log source**: Where the frontend log came from. One of `console` (`console.error`),
  `uncaught exception` (an uncaught `ErrorEvent`), or `unhandled rejection`
  (an unhandled promise rejection).
* **Error type**: The JavaScript error name, such as `TypeError` or `RangeError`.
  For `console.error` calls with no `Error` object, this is `unknown`.
* **Render type**: Whether the log was emitted from a **UI Kit** or **Custom UI** frontend.
* **Extension type**: The Forge module that rendered the frontend, for example
  `confluence:globalPage`.
* **Installation ID**: A unique identifier for the app installation on the site that
  produced the log.
* **Browser name**: The browser that ran the frontend, parsed from the user agent
  (for example, Chrome).
* **Browser version**: The browser version parsed from the user agent.
* **Operating system**: The operating system parsed from the user agent
  (for example, Mac OS X).
* **User agent**: The full browser user agent string captured by the Forge frontend host.

## Search for logs

You can search for logs using invocation ID, trace ID, log messages, and modules. This helps
narrow down log search results.

To search for logs:

1. In the search box above, enter the attributes of the logs you're searching for.
2. Press **Enter** or select the search icon.

To clear your search results, select the **X** button in the search box.

To efficiently narrow your search results, use the **Add to search** button next to the log details
you want to filter by, such as `Invocation ID`, `Trace ID`, `Function`, and `Site`. This incorporates
those values into your search, enabling you to filter results more quickly.

## Filters

You can use filters to further refine your logs.

* **Site**: Narrows down the logs based on the site that your app is installed
  onto, for example, `https://your-domain.atlassian.net`. You can select a maximum of 50 sites.
* **Environment**: Narrows down the logs for a specific app environment for your Forge app.
* **Time range**: Narrows down the logs for a specific time range that you set. Choose from
  a range of predefined values, such as the **Last 24 hours**, or choose a more specific time interval
  using the **Custom** option.
* **Container**: Narrows down the logs for a specific [container](/platform/forge/containers-reference/ref-manifest/#containers). This option only appears for apps that use [Forge Container services](/platform/forge/containers-reference/).
* **Log level**: Narrows down the logs based on the log level type that you set.
* **Atlassian app**: Narrows down the metrics to show data from a specific Atlassian app if your Forge app supports multiple Atlassian apps.
* **More filters**:
  * **Version**: Narrows down the logs based on the major version chosen.
  * **License**: Narrow down the logs based on the license status (active/inactive/trial) of your app installation if app is enabled for licensing.
  * **Edition**: Narrow down the logs based on the app edition value (standard/advanced) of your installation if app is enabled for editions.

* You can't filter by Atlassian app. For example, you can't narrow down logs just for Jira
  instances on a particular site.
* Logs are only available for the past 30 days and all dates are in UTC.
* To clear your filters, select `Reset to default`.

## Download app logs

You can download app logs, based on the [filters](#filters) you've chosen.

To download app logs:

1. Use [filters](#filters) to further refine your logs as necessary.
2. Select the **Download** button.
3. In the menu that appears, select one of the following format options:

   * **Logs as .csv**, where data values are separated by commas, allowing for data transfer with little
     or no reformatting needed.
   * **Logs as .log**, which is a zipped file that contains a `.log` file, making it easier
     for systems to consume downloaded files programmatically.

* The maximum file size when downloading logs is 100 MB.
* Each downloaded log file has a maximum of 96,000 log lines.
* To handle these limits, we recommend using [filters](#filters) before downloading logs.

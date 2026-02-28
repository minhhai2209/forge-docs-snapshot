# Monitor custom metrics

Forge Custom Metrics is now available as part of Forge Early Access Program (EAP). To start testing this feature, sign up using this
[form](https://ecosystem.atlassian.net/servicedesk/customer/portal/38/group/136/create/18658).

Forge Custom Metrics is an experimental feature offered to selected users for testing and feedback purposes. This
feature is unsupported and subject to change without notice

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

# Monitor custom metrics (EAP)

Custom metrics allow you to track specific events, actions, and measurements within your Forge app. This enables you to monitor business-specific KPIs and instrument critical paths within your app code.

Only users with [admin role](/platform/forge/contributors/#roles-and-permissions) can register, edit, and delete custom metrics.

To view custom metrics:

1. Access the [developer console](/console/myapps).
2. Select the Forge app that you want to view metrics for.
3. Select **Metrics** in the left menu.
4. Select **Custom** in the left menu.

## EAP limitation

* You can register up to 10 custom metrics per app.
* Only counter-type metrics are supported.
* You can view metrics only for non-production environments.

## Register a custom metric

To start using custom metrics for your app, you need to register them in the developer console.

To register a custom metric:

1. Select **Custom** in the left menu under Metrics.
2. Click **Register metric**.
3. Enter a name and description for your metric. For example, `jira-actions-success`.
4. Select **Register**.

![Custom metrics registration](https://dac-static.atlassian.com/platform/forge/images/custom-metrics-registration.png?_v=1.5800.1881)

After a custom metric is registered, it may take up to 15 minutes before the metric is ingested into the system.

## Instrument a custom metric

Before proceeding further, ensure you have [registered](#register-a-custom-metric) the custom metric for your app already.

1. Install the [Forge metrics package](https://www.npmjs.com/package/@forge/metrics) by running this command in your terminal:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/metrics
   ```
   ```
2. Use the metrics package installed above in your app code:

   ```
   ```
   1
   2
   ```



   ```
   import { internalMetrics } from '@forge/metrics';
   ```
   ```
3. Implement the custom metrics logic in your code. For example:

   ```
   ```
   1
   2
   ```



   ```
   export const run = async (payload, context) => {
     const counter = internalMetrics.counter('jira-actions-success'); // Name should exactly match as registered in developer console

     const jiraIssues = await fetch(...);
     counter.incr(); // Increment by 1
     // Or increment by a specific value
     counter.incrBy(value);
     for (const issue of jiraIssues) {
       ....
     }
   };
   ```
   ```

   The metric name in your app code must match the metric name registered in the developer console.
4. Deploy your app using the Forge CLI by running:
5. View the instrumented custom metric in the developer console.

   ![View custom metrics](https://dac-static.atlassian.com/platform/forge/images/view-custom-metrics.png?_v=1.5800.1881)

## Delete a custom metric

Once deleted, custom metric ingestion will be stopped immediately. However, you will still have access to historical data up to 14 days in the past.

To delete a custom metric:

1. Click the **options menu** next to the metric you want to delete.
2. Select **Delete** in the menu.
3. Select **Delete** in the confirmation dialog to confirm.

![Custom metrics unregistration](https://dac-static.atlassian.com/platform/forge/images/custom-metrics-unregistration.png?_v=1.5800.1881)

### Filters

Use these filters to refine your metrics:

* **Environment**: Narrows down the metrics for a specific app environment
  for your app.
* **Date**: Narrows down the metrics based on your chosen time interval. Choose from a range of
  predefined values, such as the **Last 24 hours**, or choose a more specific time interval using
  the **Custom** option.
* **Sites**: Narrows down the metrics based on the sites that your app is installed onto, for example,
  `<your-site>.atlassian.net`. You can select multiple sites.
* **Major App Versions**: Narrows down the metrics based on the major version of your app.
* **Function names**: Narrows down the metrics based on the function name from where the custom metric is emitted.

* Metrics are only shown for sites with at least one invocation in the past 14 days.
* All dates are in Coordinated Universal Time (UTC).
* Each chart's data resolution depends on the time interval you've selected. For example
  'Last 24 hours' shows data at a 30-minute resolution, and 'Last hour' shows data at a
  1-minute resolution.
* Metrics may not always be accurate because undelivered metrics data isn't back-filled and data sampling might be used for some metrics.

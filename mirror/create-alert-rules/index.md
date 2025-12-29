# Create alert rules

Only app admins have the permissions to to create alert rules. A maximum of five alert rules can be
created per app.

By creating alert rules, you and your team can proactively monitor your app's performance. This page
provides a step-by-step guide on how to create an alert rule for your app, ensuring you stay
informed about potential issues.

## Best practices

Follow these best practices to create useful alert rules:

* **Focus on critical metrics**: Create at least one alert rule based on the invocation success rate
  metric to ensure that customers have low downtime and your app is reliable.
* **Categorize alerts**: Use different severity levels, including `Minor`, `Major`, and `Critical`, to
  prioritize responses.
* **Avoid overly sensitive thresholds**: Set realistic and meaningful thresholds to avoid triggering
  too many alerts. You can also consider configuring the alert tolerance of your alert rules to control sensitivity.
* **Base thresholds on historical data**: Use past performance data to establish baseline metrics
  and determine appropriate thresholds.
* **Reduce alert noise**: Avoid creating multiple alerts for the same condition.
  [Disable alert rules](/platform/forge/manage-alert-rules/#disable-and-enable-alert-rules) during
  ongoing incidents or planned maintenance to prevent redundant alerts.
* **Assign relevant ownership**: Ensure each alert has responders who are responsible for taking action.
* **Seek continuous improvement**: Periodically review and adjust alert rules based on new insights,
  system performance changes, or team feedback.
* **Include documentation**: Ensure alerts provide enough context and guidance on the required
  actions by including a link to documentation in the provided field when creating the alert rule.

To begin creating an alert rule:

1. Access the [developer console](/console/myapps).
2. Select the app for which you want to create an alert rule.
3. In the side navigation panel, select **Alerts** and then select **Alert rules**.
4. Select the **Create alert rule** button in the top right-hand corner. This will open a screen
   that breaks down the process of creating an alert rule into four steps:

## Step 1: Select alert source

In this step, you will select the metric and filters that define the source of the alert.

![Create alert rule - select alert source screen](https://dac-static.atlassian.com/platform/forge/images/alerts/new_alert-alert_source.svg?_v=1.5800.1739)

### Select source metric

Select the metric you want to monitor. The alert will be based on the production data of the selected
metric. The available metrics are:

* **Invocation count**: The total number of invocations, regardless of success or failure.
* **Invocation errors**: The number of invocations that failed with an error. Errors can be due to
  out of memory issues, timeouts, or unhandled exceptions.
* **Invocation success rate**: The percentage of successful vs. failed invocations.

### Add source filters (optional)

For more specific alerts, you can add filters to refine the source. You can filter by:

* **Error type** (only for invocation errors): The specific types of errors that will trigger the
  alert.
* **Function**: The specific functions within your app.
* **Site**: The specific sites that will be monitored. A maximum of 25 sites can be selected.
* **Major version**: The major app versions that will be monitored. Selecting a major version
  includes all its minor versions.

Note that you can only select error types, functions, sites, and major versions that have had invocations
within the past 14 days.

## Step 2: Configure conditions

In this step, you will define the conditions that will trigger the alert. This
includes selecting the time period over which data is collected, setting the severity levels and
thresholds, and configuring advanced tolerance settings as needed.

Use the chart to visualize how your selected configuration settings would have correlated
with alerts based on historical data. Adjust the time period, thresholds, and alert tolerance based on
the chart and estimation banner to find the right balance between staying informed and managing alert
volume.

![Create alert rule - configure conditions screen](https://dac-static.atlassian.com/platform/forge/images/alerts/new_alert-conditions.svg?_v=1.5800.1739)

### Select time period

Select the time period during which data will be collected and evaluated. Data is aggregated over
contiguous fixed intervals.

The available options include 5 m, 10 m, 15 m, 30 m, 1 h, 2 h, 3 h, 6 h, 12 h, and 1 day.

### Define trigger conditions

Specify the severity levels of the alert and the conditions that trigger each severity.
These conditions have three main properties:

1. **Severity**: The level of impact or urgency of an alert, which assists in effectively prioritizing the response.

   * **Minor**: A low-impact issue or warning that you should be aware of. It may not be causing a
     problem yet, but it's important to monitor.
   * **Major**: A significant issue that requires attention. It suggests that something is wrong or not
     functioning as expected, requiring proactive resolution.
   * **Critical**: A severe situation that necessitates an immediate response.
2. **When**: The trigger logic for the alert.

   * Above
   * Below
   * Above or equal to
   * Below or equal to
3. **Threshold value**: The numeric value that the metric must reach to trigger the alert. For invocation
   errors and invocation count, this is an integer. For invocation success rate, this is a percentage
   and the value must be between 0 and 100.

You can add several conditions to create an alert with multiple severities. This allows you to
differentiate between varying levels of business impact and also to detect issues early.
For instance, a `Minor` alert could serve as an early warning, prompting preventive measures before
the issue escalates to a `Critical` level.

### Select alert tolerance (optional)

To help reduce alert noise from temporary spikes or dips in data, you can define the alert tolerance
as an optional advanced configuration. Alert tolerance specifies how many consecutive time
periods the threshold must be breached before the alert is triggered.

For example, if you set the alert tolerance to `3`, the threshold must be breached for three
consecutive time periods before the alert is triggered.

If alert tolerance is not configured, it defaults to `1`. This means that the threshold must only be
breached for one time period before the alert is triggered.

## Step 3: Add responders

In this step, you will specify who should be notified when the alert is triggered. Responders will
be notified by email when the alert is opened, when the alert changes severities, and when the alert
is closed.

![Create alert rule - add responders screen](https://dac-static.atlassian.com/platform/forge/images/alerts/new_alert-responders.svg?_v=1.5800.1739)

### Add responders

From the list of contributors associated with the app, choose the individuals who should receive
email notifications when the alert is triggered. You can select multiple responders to ensure that
all relevant team members are notified.

Once you’ve added the responders, you’re ready to finalize the alert rule in the next step.

## Step 4: Specify alert details

In this final step, you will provide additional details about the alert to help your team
identify and manage it effectively.

![Create alert rule - specify alert details screen](https://dac-static.atlassian.com/platform/forge/images/alerts/new_alert-alert_details.svg?_v=1.5800.1739)

### Enter alert name

Enter a clear and descriptive name for the alert. This name should help you quickly identify the
alert in the developer console and in notifications.

### Add description (optional)

Provide a brief description of the alert. Include relevant details, such as what the alert
monitors and why it’s important. This will help your team understand the alert’s purpose at a glance.

### Add documentation (optional)

If available, enter a URL that links to related documentation or a runbook. This could be a guide
to troubleshoot the alert or additional context on how to resolve the issue. Providing a documentation
link can make it easier for the team to take action when the alert is triggered.

You can review the alert rule configuration by using the **Back** and **Next** buttons. Once you've completed
all the steps, select **Create alert rule** to save the alert rule.

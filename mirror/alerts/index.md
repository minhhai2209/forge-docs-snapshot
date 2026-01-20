# Alerts

Alerts notify you about app performance issues so that you can quickly address problems
and maintain optimal performance for your users. [App admins](/platform/forge/contributors/#roles-and-permissions)
can create alert rules based on specific metrics with customizable filters, conditions, and responders to focus
on issues that matter most. Alerts can be configured based on the following
[invocation metrics](/platform/forge/monitor-invocation-metrics/#invocation-metrics):

* **Invocation count**: The total number of invocations, regardless of success or failure.
* **Invocation errors**: The number of invocations that failed with an error. Errors can be due to
  out of memory issues, timeouts, or unhandled exceptions.
* **Invocation success rate**: The percentage of successful vs. failed invocations.

Apps don’t come with alert rules by default. To receive alerts, app admins must first create alert
rules.

Note that alert rules are created on a per-app basis. If you have multiple apps, you must create
alert rules for each app. Each app can have a maximum of five alert rules.

## Permissions

Only app admins can [create](/platform/forge/create-alert-rules/)
and [manage alert rules](/platform/forge/manage-alert-rules/). All other contributors can be added
as responders to an alert rule, view alert rules that have been created, and [view open and closed alerts](/platform/forge/view-open-and-closed-alerts/).

## Alert rules

App admins can create **alert rules** with conditions that, when met, will trigger an **alert**. When
creating alert rules, app admins can customize the following attributes:

| Attribute | Description | Required |
| --- | --- | --- |
| Source metric | The specific data point or performance indicator being monitored. Alerts are based on the production data of the selected metric. Alerts can be configured based on invocation count, invocation errors, and invocation success rate. | Yes |
| Source filters | Optional filters that can be added to further refine the alert source. Available filters are error type (for invocation errors only), functions, sites, and major versions. | No |
| Time period | The time period during which data is collected. Data is aggregated over contiguous fixed intervals. | Yes |
| Trigger conditions | The conditions that, when met, will trigger the alert. Up to three different severity levels (`Minor`, `Major`, and `Critical`) can be configured per alert rule. | Yes |
| Alert tolerance | An advanced configuration option that defines the number of time periods the threshold must be consecutively breached to trigger the alert. If not defined, it will default to `1`. | No |
| Responders | The contributors who will receive email notifications when the alert is triggered. At least one responder is required per alert. | Yes |
| Alert name | The name given to the alert. | Yes |
| Alert description | Further descriptive details associated with the alert. | No |
| Documentation | A link to documentation to help guide the team in handling the alert. | No |

## Alert lifecycle

![Alert lifecycle diagram](https://dac-static.atlassian.com/platform/forge/images/alerts/alert-lifecycle.svg?_v=1.5800.1783)

Each time an alert is opened, a unique alert ID is generated. Throughout an alert’s lifecycle, it
may change severities. For example, if the situation worsens, the severity may escalate from `Major`
to `Critical`. Conversely, if the situation improves, the severity may downgrade from `Major` to
`Minor`. An alert remains open until the metric being monitored is no longer breaching any thresholds.
It’s only at this point that the alert is closed.

Responders get a notification when an alert is opened, when an alert changes severity, and when an
alert is closed. If an alert stays open, responders will be notified about the alert every
24 hours. Notifications are sent via email to the responders selected when the alert rule is created.

## Recommendations

By creating alert rules, you can stay ahead of issues, reduce downtime, and ensure your app is
running smoothly, all of which contribute to a better overall experience for your users. We
recommend creating at least one alert rule based on the invocation success rate metric to ensure
that your app is reliable and your users have low downtime.

Here are some scenarios where [creating an alert rule](/platform/forge/create-alert-rules) would be beneficial:

* **Performance**: To ensure that your app maintains a certain level of performance,
  such as invocation success rate, you can create an alert rule to notify you if the performance degrades.
* **Error detection**: If your app throws errors, you can create an alert rule to notify you when
  the number of invocation errors exceeds a certain threshold, indicating a potential problem that
  needs immediate attention.
* **Unusual traffic spikes**: You can create an alert rule on the invocation count metric to
  detect unusual spikes in traffic that could indicate a potential issue.

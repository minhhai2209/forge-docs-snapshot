# View open and closed alerts

All contributors can view open and closed alerts in the developer console. Contributors who are
added as responders to an alert rule will receive email notifications when an alert opens, when an
alert’s severity changes, and when an alert closes.

## Alert lifecycle

The typical lifecycle of an alert is as follows:

![Alert lifecycle diagram](https://dac-static.atlassian.com/platform/forge/images/alerts/alert-lifecycle.svg?_v=1.5800.1790)

|  |  |
| --- | --- |
| **Metric breaches threshold** | The monitored metric breaches the target threshold. |
| **Alert is opened** | The alert is opened, a unique alert ID is generated, and the responders receive an email. The alert appears on the Open alerts screen in the developer console. |
| **Alert severity changes** | The conditions of the alert might change while the alert is open, causing the severity to escalate or de-escalate. Responders receive an email each time a severity change occurs. |
| **Metric stops breaching lowest severity threshold** | The alert remains open until the monitored metric stops breaching the lowest severity threshold. |
| **Alert is closed** | The alert is closed and the responders receive an email. The alert appears on the Closed alerts screen in the developer console. |

## Alert emails

Responders receive emails when an alert is opened, when its severity level changes, and when it is
closed. An alert email includes the following details:

* **Alert rule:** The alert rule name to identify what triggered the alert.
* **Status:** The current status of the the alert. An alert's status can be `OPEN` or `CLOSED`.
* **Alert ID:** The unique ID that's generated when an alert is opened.
* **Severity:** The current severity of the alert, which can be `Minor`, `Major` or `Critical`.
* **Timestamp**: The time and date at which the alert was triggered.

You can easily access the alert details in the developer console from within the alert email by
clicking **Go to alert**. Additionally, you can use **View Logs** to go directly to the logs screen
to debug your app.

## Open alerts

When the conditions defined in an alert rule are met, the alert will be opened and a unique alert
ID is generated. This open alert will then appear in the open alert screen until the monitored
metric is no longer breaching any thresholds.

To view open alerts for an app in the developer console:

1. Access the [developer console](/console/myapps).
2. Select the app that the alert rule is related to.
3. In the side navigation panel, select **Alerts** and then select **Open alerts**. This screen shows
   all alerts that are currently open.

![Open alerts screen](https://dac-static.atlassian.com/platform/forge/images/alerts/alerts_open-alerts.svg?_v=1.5800.1790)

4. For a more detailed view of a specific open alert, including the alert activity, metrics chart,
   and alert rule details, select the specific alert.

![Open alert more details screen](https://dac-static.atlassian.com/platform/forge/images/alerts/alerts_open-alert-details.svg?_v=1.5800.1790)

## Closed alerts

Once the thresholds are no longer being breached, the alert is closed and it is moved to the closed
alerts screen. The metrics chart for a closed alert is available for 14 days and the details about a
closed alert are available for 60 days.

To view closed alerts for an app in the developer console:

1. Access the [developer console](/console/myapps).
2. Select the app that the alert rule is related to.
3. In the side navigation panel, select **Alerts** and then select **Closed alerts**. This screen shows
   alerts that have been recently closed.

![Closed alerts screen](https://dac-static.atlassian.com/platform/forge/images/alerts/alerts_closed-alerts.svg?_v=1.5800.1790)

4. For a more detailed view of a specific closed alert, including the alert activity from when
   the alert was open, metrics chart, and alert rule details, select the specific alert.

![Closed alert more details screen](https://dac-static.atlassian.com/platform/forge/images/alerts/alerts_closed-alert-details.svg?_v=1.5800.1790)

# Usage alerts

To help you proactively manage your apps, the Forge platform sends email alerts when
your app's resource usage crosses specific thresholds. These alerts give you early
warning as your app approaches its resource limits, so you can investigate, optimize,
or upgrade before hitting a hard limit.

These emails are sent so that you can monitor your app's resource consumption and
optimize your app to reduce costs if needed. For more information on how usage is
measured and billed, see [Forge platform pricing](/platform/forge/forge-platform-pricing/).

## Prerequisites

Before usage alerts can be delivered, the following requirements must be met:

* The app must be assigned to a [developer space](/platform/forge/developer-space/developer-spaces-introduction/) and any required consent steps must be completed. This connects the app to a transaction account and billing account.
* All [app contributors](/platform/forge/manage-app-contributors/#manage-app-contributors)
  and [billing admins](/platform/forge/developer-space/developer-space-roles/#special-roles--billing-and-marketplace-admins)
  of the developer space will automatically receive usage alert emails.

If someone is not an app contributor and wants to receive usage alerts, they
will need to be manually added as a billing admin in the billing console.

## When email alerts are sent

Email alerts are triggered when your app's resource usage crosses the following
thresholds:

| Threshold | What it means |
| --- | --- |
| **50%** | Your app has used half of its allocated resources. |
| **75%** | Your app is using a significant portion of its resources; monitor more closely. |
| **90%** | Your app is nearing its resource limit; you should consider taking action soon. |
| **100%** | Your app has reached its full resource allocation and may be subject to limits or other enforcement depending on your plan and configuration. |

You may receive multiple alerts over time as usage crosses each threshold (50%, 75%,
90%, 100%).

## What's in the alert email

Each resource usage alert email includes the following information:

* **Which app** the alert is about
* The **resource usage level** that triggered the alert (50%, 75%, 90%, or 100%)
* The **current usage** and **allocated limit** for context

The exact wording and layout of these emails may evolve over time, but they will
always indicate which threshold has been reached.

## Email sender address and authenticity

For security and trust, it's important that you can easily recognize genuine
platform emails about resource usage.

All resource usage alert emails are sent from the following Atlassian-controlled
sender address: **`noreply@po.atlassian.net`**. Use this address to verify the
authenticity of the message before clicking any links or taking action.

To make sure you receive these alerts:

* Add the sender address to your **allowlist or safe senders** in your email system.
* Check with your IT or security team if your organization uses strict email filtering.

## Monitor your usage

To track your app's resource usage and take proactive action, you can:

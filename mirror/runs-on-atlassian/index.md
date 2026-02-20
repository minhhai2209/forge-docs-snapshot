# Runs on Atlassian

The **Runs on Atlassian** program helps customers identify Forge apps that can benefit
enterprise customers with strict data privacy requirements. The **Runs on Atlassian** badge
is automatically applied to eligible apps on the Atlassian Marketplace.

Runs on Atlassian addresses the following requirements from customers:

1. Apps exclusively use Atlassian-hosted compute and storage.
2. Apps support data residency that matches data residency provided by the host Atlassian app.
3. Customers can control external data egress (for example, analytics and logs) via admin controls.

The Forge CLI provides a programmatic way to verify the above requirements.

While controls that limit external data egress are in place, these controls do not prevent misuse of access granted to the app during installation or abuse of the app runtime. The boundaries of tenant safety and data handling are defined in the [Shared responsibility model](/platform/forge/shared-responsibility-model/#tenant-safety).

![Runs on Atlassian page on app listing page](https://dac-static.atlassian.com/platform/forge/images/app-listing.svg?_v=1.5800.1869)

## Eligibility requirements

Eligibility for the Runs on Atlassian badge is automatically detected and applied on apps
that meet the qualifications. Partners do not need to apply or opt in to receive the badge.

To determine whether your Forge apps meet the requirements for Runs on Atlassian, start by checking
your [manifest file](/platform/forge/manifest/) for egress permissions. You can also use the
[Forge CLI](/platform/forge/cli-reference/eligibility/) to check the eligibility of an app.

Your app must not egress data, with the exception of egress for analytics purposes. If your app
sends data for analytics and does not send
[in-scope End-User Data](/platform/forge/data-residency/#in-scope-end-user-data), then it is eligible
for Runs on Atlassian.

Apps use analytics data to identify trends and insights, which can be used to improve
app performance. These trends and insights can fall under different categories, such as
web analytics and Atlassian app analytics. In the context of Runs on Atlassian,
you must not mark tools that don't capture analytics data as *analytics egress*.

We enforce a policy in order to prevent abuse. Refer to [Analytics tools policy for Forge apps](/platform/forge/analytics-tool-policy) for more information.

The [Cloud Fortified](/platform/marketplace/cloud-fortified-apps-program/) and
[Cloud Security Participant](/platform/marketplace/marketplace-security-bug-bounty-program/)
badges remain important signals on the investments partners have made in ensuring their apps adhere to
advanced trust practices. Depending on eligibility, an app can have a combination of these badges.

## Ready to dive right in?

Here are some things you can do to start making your apps eligible for Runs on Atlassian.

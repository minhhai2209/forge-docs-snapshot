# Analytics tool policy for Forge apps

This policy only applies to
[egress permissions](/platform/forge/manifest-reference/permissions/#egress-permissions)
configured under the **analytics** `category` in your Forge app manifest.

The policy is not limited to apps that meet the
[Runs on Atlassian](/platform/forge/runs-on-atlassian) criteria. Partners can still continue using
tools of choice, but these tools should be declared as general egress and *not* under the
**analytics** `category`.

To protect user privacy and data security, Atlassian enforces strict criteria for analytics tools
used by apps when configuring
[egress permissions](/platform/forge/manifest-reference/permissions/#egress-permissions)
under the *analytics* `category`.

This policy ensures that only recognized and legitimate analytics tools with proper
documentation are permitted.

This page outlines the enforced allowlist, as well as the process for requesting approval of analytics tools.

## Analytics criteria

These analytics criteria apply to **all tools** capturing data through
[analytics egress permissions](/platform/forge/manifest-reference/permissions/#egress-permissions)
in your Forge app manifest, regardless of whether your app is eligible
for the [Runs on Atlassian](/platform/forge/runs-on-atlassian) program.

Analytics tools must adhere to the following criteria:

* **Not** support self-hosted deployment (cloud-only).
* Have a **public website**, comprehensive documentation, and an accessible privacy policy.
* Have a **recognized fixed domain name** that is easily associated with the company or provider,
  for example, `subdomain.acme.com`.

Atlassian reserves the right to update these criteria as business needs arise.

### Policy rationale

Analytics tools are essential for understanding product usage and improving user experience.
Some customers acknowledge this and are comfortable with apps sharing data
with remote tools for analytics purposes, especially in the case of Runs on Atlassian apps.

This policy ensures that developers use the analytics category with recognized and legitimate
tools, maintaining transparency for customers regarding their apps' purposes for data egress while
providing flexibility for various analytics use cases.

As of 28 August 2025, apps declaring domains not matching the [criteria](#analytics-criteria) for analytics tools will be blocked from deployment.

As we explore various long-term solutions, we commit to provide at least four weeks' notice before making any further changes to the policy. We will announce any changes in a separate
changelog.

### Ineligible categories

| Category | Reasoning | Example | Recommended alternative |
| --- | --- | --- | --- |
| `Self-hosted tools` | Atlassian cannot guarantee that a self-hosted analytics URL is not being utilized for functional app egress. | Umani, Plausible | Use a cloud analytics vendor that meets the analytics criteria. |

## List of pre-approved domains

The `analytics` egress category is only allowed for the following pre-approved domains:

| Domain | Description |
| --- | --- |
| `*.google-analytics.com` | [Google Analytics](https://marketingplatform.google.com/about/analytics/) |
| `cdn.mxpnl.com`, `*.cdn.mxpnl.com`, `*.mixpanel.com` | [Mixpanel](https://mixpanel.com/) |
| `*.posthog.com` | [PostHog](https://posthog.com/) |
| `*.journy.io` | [Journy](https://www.journy.io/use-cases) |
| `*.amplitude.com` | [Amplitude](https://amplitude.com/docs/apis/analytics) |
| `static.cloudflareinsights.com` | [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/) |
| `*.cdn.usefathom.com` | [Fathom Analytics](https://usefathom.com/) |
| `*.events.usermaven.com`, `*.um.contentstudio.io` | [Usermaven](https://usermaven.com/docs) |
| `*.beamanalytics.b-cdn.net` | [Beam Analytics](https://beamanalytics.io/) |
| `*.microanalytics.io` | [Microanalytics](https://microanalytics.io/) |
| `*.scripts.withcabin.com` | [WithCabin](https://withcabin.com/) |
| `*.scripts.simpleanalyticscdn.com` | [Simple Analytics](https://docs.simpleanalytics.com/) |
| `*.userpilot.io` | [UserPilot](https://docs.userpilot.com/) |
| `in.accoil.com` | [Accoil](https://developer.accoil.com/) |
| `*.plausible.io` | [Plausible](https://plausible.io/) |
| `*.googleapis.com`, `*.googleapis.com`, `*.googletagmanager.com` | [Google Tag Manager](https://tagmanager.google.com/#/home) |
| `*.ingest.sentry.io`, `*.ingest.us.sentry.io`, `*.sentry-cdn.com` | [Sentry](https://sentry.io/) |
| `*.hotjar.io`, `*.hotjar.com` | [HotJar](https://www.hotjar.com/) |
| `*.cdn.segment.com`, `cdn.segment.com`, `*.api.segment.io` | [Segment](https://segment.com/) |
| `*.applicationinsights.azure.com` | [Azure Application Insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview) |
| `*.monitor.azure.com` | [Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview) |
| `*.launchdarkly.com` | [LaunchDarkly](https://launchdarkly.com/) |
| `*.statsigapi.net`, `statsigapi.net`, `*.featureassets.org`, `featureassets.org`, `*.prodregistryv2.org`, `prodregistryv2.org` | [Statsig](https://statsig.com/) |
| `*.newrelic.com` | [New Relic](https://newrelic.com/) |

Using the `analytics` category on a domain that isn't on this list will prevent your app from deploying.
This policy ensures that the `analytics` egress category is used transparently and only for legitimate
analytics purposes, maintaining user trust regardless of your app's participation in trust programs
like [Runs on Atlassian](/platform/forge/runs-on-atlassian).

## Requesting approval for additional domains

If you need to use an analytics tool that's not on the pre-approved list, raise a support request
[here](https://ecosystem.atlassian.net/servicedesk/customer/portal/34/group/3534/create/4180).

Atlassian will review your request and the information provided at its sole discretion. If
Atlassian approves your request, the tool will be added to the allowlist and published on
the developer documentation. If not, you will be advised to select an approved alternative.

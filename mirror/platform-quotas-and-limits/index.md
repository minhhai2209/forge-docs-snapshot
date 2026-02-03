# Platform limits and usage

Forge has transitioned to a consumption-based pricing model (effective January 1, 2026). This means developers only pay for what they use while still benefiting from a generous free usage allowance. Platform limits remain in place to maintain fair use, predictable performance, and overall platform reliability.

If your app consistently exceeds the limits, we will contact you. You can also contact us if you think your app needs higher limits. Learn more about exceeding Forge limits.

In addition to platform quotas and limits, Forge apps may also be affected by Atlassian app-specific rate limits, such as when making REST API calls to [Jira](/cloud/jira/platform/rate-limiting/) or [Confluence](/cloud/confluence/rate-limiting/).

## Quotas

Quotas were originally introduced to prevent abuse of the Forge platform by placing strict upper limits on usage. With the introduction of the new [consumption-based pricing model](/platform/forge/forge-platform-pricing/), quotas are no longer necessary. The pricing model now ensures fairness by charging for usage beyond free allowances, while still protecting platform reliability. This approach makes the rules clearer, more predictable, and directly tied to cost.

**Fair usage:** While we have removed most hard limits in favor of consumption pricing, strictly abusive or unstable usage patterns are not permitted. Atlassian reserves the right to contact you, throttle, or suspend apps that jeopardize the stability of the Forge platform or degrade performance for other users.

## Platform limits

The Forge platform enforces specific limits that don't scale with your app's usage. Review these constraints to optimize your app, prevent resource exhaustion, and understand the necessary tuning for your specific use case.

### Exceeding limits and suspended apps

Explains the consequences of exceeding platform limits, including billing for overages and potential app suspension. This section also details the monitoring tools available to help detect issues and prevent abuse or non-payment suspensions.

For more information, see [Exceeding limits and suspended apps](/platform/forge/exceeding-limits-and-suspended-apps/).

### Invocation limits

Details the maximum invocation counts and execution duration for functions. This section outlines how these limits affect responsiveness, compares short- versus long-running functions, and defines how usage is calculated against free and paid allowances.

For more information, see [Invocation limits](/platform/forge/limits-invocation/).

### Resource limits

Specifies the maximum number and size of static resource bundles for Custom UI and UI Kit apps. This covers limits on file counts per bundle, individual bundle sizes, and the total number of allowed bundles per app.

For more information, see [Resource limits](/platform/forge/limits-resource/).

### KVS and Custom Entity Store limits

Outlines operational limits for storage APIs, including read/write frequencies, key lengths, value sizes, and transaction depths. These installation-level limits are enforced to ensure fair use and reliable performance.

For more information, see [KVS and Custom Entity Store limits](/platform/forge/limits-kvs-ce/).

### Forge SQL limits

Defines constraints for Forge SQL databases, including total storage capacity, table counts, request rates, row sizes, and query execution times. These limits are designed to maintain stable performance and predictable costs.

For more information, see [Forge SQL limits](/platform/forge/limits-sql/).

### Forge Object Store

Describes installation-specific limits for throughput and object sizes, which help ensure fair use and reliable performance.

For more information, see [Forge Object Store](/platform/forge/limits-object-store/).

### Forge LLMs

Details limits for Forge LLMs such as context window size and requests per minute, helping ensure fair use and predictable costs.

For more information, see [Forge LLM limits](/platform/forge/limits-llm/).

### Web Trigger

Sets rate limits for Web trigger operations (get, create, delete) per minute, app, environment, and context. Exceeding these thresholds results in temporary request denials until usage normalizes.

For more information, see [Web Trigger limits](/platform/forge/limits-web-trigger/).

### Async events limits

Establishes boundaries for background event processing, including events per request, events per minute, payload sizes, and cyclic invocation depth. These limits ensure reliability and prevent platform overload.

For more information, see [Async events limits](/platform/forge/limits-async-events/).

### App and developer limits

Lists restrictions on app metadata (names, descriptions), module counts, resources, environments, and alert configurations. It also covers the maximum number of apps allowed per developer account to ensure fair resource distribution.

For more information, see [App and developer limits](/platform/forge/limits-app-developer/).

### Scheduled trigger limits

Covers limits on scheduled triggers, including how many triggers an app can define and how often they can run. Scheduled triggers share the same invocation limits as other Forge functions.

For more information, see [Scheduled trigger limits](/platform/forge/limits-scheduled-trigger/).

## Monitoring and managing costs

You can track your usage and forecast costs using:

## Migration note

We’ve reorganized this content for clarity. Quotas have been retired, and platform limits are now documented per category. If you’ve bookmarked the old quotas page, use this overview to find the updated guidance.

# Forge platform pricing

Forge uses a consumption-based pricing model, offering most capabilities for free within generous monthly usage limits. This page is the source of truth for current Forge pricing and will be updated as needed.

## Pricing model summary

* **Free Usage Allowance**: Each Forge app includes a generous monthly usage allowance at no cost.
* **Paid Usage (Overage)**: If your usage exceeds the free allowance, charges will apply monthly, billed in arrears.
* **Billing Start Date**: No billing will occur before January 1, 2026.

## Billable capabilities and pricing

| Capability | Unit | Free usage allowance (monthly) | Overage price per unit ($USD) |
| --- | --- | --- | --- |
| Forge Functions: Duration | $/GB-seconds | 100,000 GB-seconds | 0.000025 |
| Key-Value Store: Reads | $/GB | 0.1 GB | 0.055 |
| Key-Value Store: Writes | $/GB | 0.1 GB | 1.090 |
| Logs: Writes | $/GB | 1 GB | 1.005 |
| SQL: Compute duration | $/hr | 1 hr | 0.143 |
| SQL: Compute requests | $/1M-requests | 100,000 requests | 1.929 |
| SQL: Data stored | $/GB-hours | 730 GB-hours | 0.00076850 |

### Example: Calculating your monthly bill

Suppose your Forge app uses the following in a single month:

* **Compute functions:** 150,000 GB-seconds
* **Key-Value Store Reads:** 0.15 GB

Here’s how your monthly charge would be calculated:

1. **Compute functions (Forge Functions: Duration)**

   * Free usage allowance: **100,000 GB-seconds**
   * Your usage: **150,000 GB-seconds**
   * Overage: 150,000 – 100,000 = **50,000 GB-seconds**
   * Overage price: $0.000025 per GB-second
   * **Charge:** 50,000 × $0.000025 = **$1.25**
2. **Key-Value Store Reads**

   * Free usage allowance: **0.1 GB**
   * Your usage: **0.15 GB**
   * Overage: 0.15 – 0.1 = **0.05 GB**
   * Overage price: $0.055 per GB
   * **Charge:** 0.05 × $0.055 = **$0.00275**

**Total monthly charge:**  
$1.25 (compute) + $0.00275 (KVS reads) = **$1.25275**

This example shows how charges are only applied to usage above the free monthly allowance for each capability, and how multiple capabilities can contribute to your total bill.

## Estimate and monitor your costs

Use the [Forge cost estimator](https://developer.atlassian.com/forge-cost-estimator) to preview potential monthly charges based on your app's projected usage. You can monitor usage for your Forge apps in the [Developer console](/platform/forge/monitor-usage-metrics/). This helps you:

* Understand how much of your free usage allowance is being used
* Forecast potential charges once billing begins
* Identify performance or cost optimization opportunities

To view your app’s resource usage and costs:

1. Access the [developer console](https://developer.atlassian.com/console/myapps).
2. Select the Forge app that you want to view metrics for.
3. Select **Usage and costs** in the left menu and then select the resource you want to view (for example, Functions).
4. To see a detailed breakdown of usage, select View Details for the specific resource you're interested in. You can use the date filter to customize the view, with the default setting showing data for the current calendar month.

## FAQs

**When does billing start?**  
Billing starts on January 1, 2026. Before this date, any Forge usage up to platform quotas and limits is free.

**What do I need to do before billing begins?**  
Once pricing takes effect, you’ll need to provide billing details to continue using Forge. Instructions will be shared in the Developer Console. To avoid service interruptions, ensure you add a payment method.

**How does the free usage allowance work?**  
The free usage allowance is **per app, per month**. Each app receives its own quota for each billable capability. Usage above these thresholds will be billed monthly in arrears.

**Can I keep using Forge for free?**  
Yes, if your app remains within the monthly free usage allowance, you won’t be charged.

**How does billing work for multiple apps or organizations?**  
Billing is consolidated into a single monthly invoice for all apps managed by an individual, partner, or customer. Each app benefits from its own free usage allowance, which is not shared across other apps.

**Which Forge capabilities will be charged for?**  
At launch, the following capabilities will be charged above the free threshold:

* Compute Functions (Forge Functions: Duration)
* KVS Storage: Data Read and Data Written
* SQL: Compute (duration and request) and Data Stored
* Logs: Data Written

Other capabilities not listed here, such as using Connect on Forge modules or remote capabilities, will remain free.

**What makes Forge a valuable choice for building on the cloud?**  
Forge pricing reflects not just raw compute/storage, but also value-added features like data residency, customer compliance features like BRIE and BYOK, support for regulated environments like Atlassian Government Cloud, and integrated billing/discovery.

**Will there be differences in pricing for public vs. private apps?**  
No, the same thresholds and pricing apply to both public Marketplace apps and private/internal apps. However, to create a sustainable business, pricing has to be calibrated to current market conditions, and there are many variables that can change over time. These include pricing for the services Atlassian consumes to deliver Forge. We will always endeavour to price competitively and will review pricing periodically (much like Atlassian does for its flagship apps). Changes to pricing and or the introduction of new capabilities will be announced at least 3 months in advance.

**What support and SLAs are available for paid usage?**  
Apps exceeding the free tier will be eligible for enhanced support and SLAs, including 99.90% uptime for Compute, KVS, and SQL. Service credits are available if uptime falls below thresholds. More details will be provided before pricing takes effect.

**Why is Forge introducing pricing?**  
Introducing pricing for Forge creates a sustainable economic model that enables continued investment in the platform. This approach ensures we can deliver new capabilities and features that help partners grow and strengthen their businesses.

**Where can I find more information or get help?**  
Atlassian will continue to update partners via official communications and provide detailed documentation and support as the pricing model rolls out.

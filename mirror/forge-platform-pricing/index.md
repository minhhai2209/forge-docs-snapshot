# Forge platform pricing

Forge uses a consumption-based pricing model, offering most capabilities for free within generous monthly usage limits. This page is the source of truth for current Forge pricing and will be updated as needed.

## Pricing model summary

* **Free Usage Allowance**: Each Forge app includes a generous monthly usage allowance at no cost.
* **Paid Usage (Overage)**: If your usage exceeds the free allowance, charges will apply monthly, billed in arrears.
* **Billing schedule**: Invoices will be generated on the first day of each month, starting 1 February 2026, for usage in the previous month (for example, January 2026 usage will be invoiced on 1 February 2026). To help developers become familiar with the billing process, we will issue fully discounted (zero-dollar) invoices for December 2025 usage on 1 January 2026.
  Find more details about [Developer Space billing and payments](/platform/forge/developer-space/billing-for-developer-spaces/).

## Billable capabilities and pricing

| Capability | Unit | Free usage allowance (monthly) | Overage price per unit ($USD) |
| --- | --- | --- | --- |
| Forge Functions: Duration | $/GB-seconds | 200,000 GB-seconds | 0.000025 |
| Key-Value Store: Reads | $/GB | 0.1 GB | 0.055 |
| Key-Value Store: Writes | $/GB | 0.1 GB | 1.090 |
| Logs: Writes | $/GB | 1 GB | 1.005 |
| SQL: Compute duration | $/hr | 1 hr | 0.143 |
| SQL: Compute requests | $/1M-requests | 100,000 requests | 1.929 |
| SQL: Data stored | $/GB-hours | 730 GB-hours | 0.00076850 |
| Object Store: Requests | $/1k-requests | 5,000 requests | 0.001353 |
| LLM: Input | $/credits | 0 credits | 0.0000001 |
| LLM: Output | $/credits | 0 credits | 0.0000005 |
| Containers: Compute (starting August 1, 2026) | $/vCPU-hour | 0 vCPU-hours | 0.07177 |
| Containers: Memory (starting August 1, 2026) | $/GiB-hour | 0 GiB-hours | 0.00786 |

Empty KVS reads count as 1KB towards your usage, whereas non-empty reads are based on actual size. While we may consider a future update to apply this 1KB minimum to all reads under 1KB, the current policy applies only to empty reads. We will provide advance notice prior to adopting any changes.

### Example: Calculating your monthly bill

Suppose your Forge app uses the following in a single month:

* **Compute functions:** 250,000 GB-seconds
* **Key-Value Store Reads:** 0.15 GB
* **SQL:** Data stored: Your app adds 2.73 MB of data every hour and does not delete any data during the month.
* **LLM:** 2,000,000 input credits and 500,000 output credits

Here’s how your monthly charge would be calculated:

1. **Compute functions (Forge Functions: Duration)**

   * Free usage allowance: **200,000 GB-seconds**
   * Your usage: **250,000 GB-seconds**
   * Overage: 250,000 – 200,000 = **50,000 GB-seconds**
   * Overage price: $0.000025 per GB-second
   * **Charge:** 50,000 × $0.000025 = **$1.25**
2. **Key-Value Store Reads**

   * Free usage allowance: **0.1 GB**
   * Your usage: **0.15 GB**
   * Overage: 0.15 – 0.1 = **0.05 GB**
   * Overage price: $0.055 per GB
   * **Charge:** 0.05 × $0.055 = **$0.00275**
3. **SQL: Data stored**

   * Free usage allowance: **730 GB-hours (per month)**
   * Overage price: **$0.00076850 per GB-hour**
   * Your app adds 2.73 MB of new data every hour and does not delete any data.
   * At the end of the first hour, you have 2.73 MB stored. At the end of the second hour, you have 5.46 MB, and so on.
   * The total storage for each hour is summed across all hours in the month.
     **Total GB-hours for the month:**
     2.73 MB × (1 + 2 + 3 + ... + 720) = 2.73 MB × 720 × 721 / 2 ≈ 710,892 MB-hours
     Convert to GB-hours: 710,892 MB-hours ÷ 1,024 = 694.3 GB-hours
   * Free usage allowance: **730 GB-hours**
   * Overage: 694.3 – 730 = **0 GB-hours** (no overage, so no charge)

SQL storage is billed based on the total amount of data stored, measured hourly and summed over the month (GB-hours). You are not billed based on the amount of data read or written, but on the cumulative storage held each hour.

At the start of each new month, your SQL storage usage calculation continues from the amount of data stored at the end of the previous month. If you have not deleted any data, your hourly storage “snapshots” will begin at this higher baseline, and your total GB-hours for the new month will accumulate more quickly. To reduce future charges, consider deleting unneeded data before the next billing cycle begins.

4. **LLM: Input and Output**
   * Free usage allowance: **0 credits** (no free allowance)
   * **Input:**
     * Your usage: **2,000,000 credits**
     * Overage price: $0.0000001 per credit
     * **Charge:** 2,000,000 × $0.0000001 = **$0.20**
   * **Output:**
     * Your usage: **500,000 credits**
     * Overage price: $0.0000005 per credit
     * **Charge:** 500,000 × $0.0000005 = **$0.25**
   * **Total LLM charge:** $0.20 + $0.25 = **$0.45**

**Total monthly charge:**  
$1.25 (compute) + $0.00275 (KVS reads) + $0 (SQL data stored) + $0.45 (LLM) = **$1.70275**

This example shows how charges are only applied to usage above the free monthly allowance for each capability, and how multiple capabilities can contribute to your total bill.

## Billing for Rovo agents and actions

Forge consumption-based pricing covers the platform resources your app uses, such as compute, storage, and logs. If your Forge app includes a [Rovo agent](/platform/forge/manifest-reference/modules/rovo-agent/) or [Rovo action](/platform/forge/manifest-reference/modules/rovo-action/), Rovo usage is billed separately from Forge consumption-based pricing.

### How Rovo billing works for customers

Rovo billing is managed at the customer organization level, so Marketplace partners are not responsible for the AI usage costs of their Rovo agents. Every paid Jira, Confluence, or Jira Service Management subscription includes a pooled allowance of **Rovo credits** and **indexed objects**. The size of this allowance is determined by the customer's subscription tier and the number of licensed users in their organization.

Each agent request consumes credits from the customer's pool according to the rates defined in [Rovo usage limits](https://support.atlassian.com/rovo/docs/rovo-usage-limits/), regardless of whether the agent was built by Atlassian, created by the customer in Atlassian Studio, or distributed through a Marketplace Forge app.

If a customer exceeds their included credit quota and their organization has overage billing enabled, the additional charges are applied directly to the customer's Atlassian invoice. For more information about how customers are billed for Rovo usage, see [Rovo usage limits](https://support.atlassian.com/rovo/docs/rovo-usage-limits/) in Atlassian Support.

### What Forge developers are billed for

When a Rovo agent in your Forge app invokes a [Forge action](/platform/forge/manifest-reference/modules/rovo-action/), that action runs on the Forge platform like any other Forge function. The compute, storage, and log usage produced while executing your action counts towards your Forge platform pricing in the usual way, and any overage above the free usage allowance is billed to you according to the [pricing table](#billable-capabilities-and-pricing) above.

In short:

* **Rovo credits** (the cost of the AI interaction itself) are paid by the customer's organization from their pooled Rovo allowance.
* **Forge consumption-based pricing** (compute, storage, and logs used to execute your action) is paid by the developer of the Forge app, just like for any other Forge module.
* **Marketplace licensing** (for paid Marketplace apps) continues to be paid by the customer through Atlassian Marketplace.

Rovo credits, indexed objects, and the rules for Rovo overage billing are set by Atlassian and may change over time. The pricing model on this page covers only Forge platform resource usage. For the latest Rovo credit allowances and pricing, see [Rovo usage limits](https://support.atlassian.com/rovo/docs/rovo-usage-limits/).

## Estimate and monitor your costs

Use the [Forge cost estimator](https://developer.atlassian.com/forge-cost-estimator) to preview potential monthly charges based on your app's projected usage.

For practical techniques to keep your app within the free tier or minimise overage charges, see [Optimise Forge platform costs](/platform/forge/optimise-forge-costs/).

You can [monitor usage metrics and cost](https://developer.atlassian.com/platform/forge/monitor-usage-metrics/) for your Forge apps in the [Developer console](/platform/forge/monitor-usage-metrics/). This helps you:

* Understand how much of your free usage allowance is being used
* Forecast potential charges once billing begins
* Identify performance or cost optimization opportunities

To view your app’s resource usage and costs:

1. Access the [developer console](https://developer.atlassian.com/console/myapps).
2. Select the Forge app that you want to view metrics for.
3. Select **Usage and charges** in the left menu and then select the resource you want to view (for example, Functions).
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
* LLM: Input and Output (billed per credit, with no free usage allowance)
* Object Store: Requests

The following capabilities are also billable, but use different pricing models and provide no free usage allowance:

* [Forge Containers](/platform/forge/containers-reference/pricing/): uses a separate reservation-based pricing model.
* [Forge LLM](/platform/forge/runtime-reference/forge-llms-api-pricing/): tracked in credits, which correspond to model input and output tokens. Each model has a token-to-credit conversion ratio, and more powerful models use more credits per token.

Other capabilities not listed here, such as using Connect on Forge modules or remote capabilities, will remain free.

**How are functions that crash or run out of memory billed?**  
Forge measures the duration of each invocation to calculate its compute cost. In a small number of cases — for example, when a function runs out of memory or the runtime crashes — the function is stopped abruptly and a reliable execution time cannot be recorded. When this happens, you are charged for the **lower of**:

* the function's configured timeout (set via [`timeoutSeconds`](/platform/forge/manifest-reference/modules/function/)), or
* the measured execution time, including platform overhead.

To keep your compute costs predictable, set `timeoutSeconds` to the smallest value your function needs and avoid out-of-memory failures. See [Optimise Forge platform costs](/platform/forge/optimise-forge-costs/#right-size-timeouts-and-avoid-crashes) for guidance.

**Will I be charged for the Rovo credits used by a Rovo agent in my Forge app?**  
No. Rovo credits are paid by the customer's organization from their pooled Rovo allowance, not by the Forge app developer. As a developer, you are only billed for the Forge platform resources (compute, storage, and logs) used to execute any Forge actions your agent invokes. See [Billing for Rovo agents and actions](#billing-for-rovo-agents-and-actions) for details.

**What makes Forge a valuable choice for building on the cloud?**  
Forge pricing reflects not just raw compute/storage, but also value-added features like data residency, customer compliance features like BRIE and BYOK, support for regulated environments like Atlassian Government Cloud, and integrated billing/discovery.

**Will there be differences in pricing for public vs. private apps?**  
No, the same thresholds and pricing apply to both public Marketplace apps and private/internal apps. However, to create a sustainable business, pricing has to be calibrated to current market conditions, and there are many variables that can change over time. These include pricing for the services Atlassian consumes to deliver Forge. We will always endeavour to price competitively and will review pricing periodically (much like Atlassian does for its flagship apps). Changes to pricing and or the introduction of new capabilities will be announced at least 3 months in advance.

**Will I also be charged for usage in a non-production environment?**
Yes. Usage will be measured across all environments which include production, staging, development and all [custom development environments](https://developer.atlassian.com/platform/forge/environments-and-versions/#custom-environments).

**Will I be charged for usage on sandbox sites?**
Effective April 4, 2026, Forge usage on up to the first five sandboxes associated with each production site where your app is installed is now exempt from billing. Usage resulting from customers testing your app in sandboxes will no longer appear on your monthly Forge bill. For more details, refer to the [changelog announcement](https://developer.atlassian.com/platform/forge/changelog/#CHANGE-3135).

**What support and SLAs are available for paid usage?**  
Apps exceeding the free tier will be eligible for enhanced support and SLAs, including 99.90% uptime for Compute, KVS, and SQL. Service credits are available if uptime falls below thresholds. Find more details in the [Forge Service Level Agreement](https://developer.atlassian.com/platform/forge/forge-service-level-agreement/).

**Why is Forge introducing pricing?**  
Introducing pricing for Forge creates a sustainable economic model that enables continued investment in the platform. This approach ensures we can deliver new capabilities and features that help partners grow and strengthen their businesses.

**Where can I find more information or get help?**  
Atlassian will continue to update partners via official communications and provide detailed documentation and support as the pricing model rolls out.

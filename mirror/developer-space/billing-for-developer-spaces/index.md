# Understand billing and payments in Developer Spaces

A Developer Space is your team’s shared space for building, managing, and billing Forge apps. This page explains how billing works for a Developer Space, how to add a payment method, how automatic payments and invoices work, and what happens if you don’t add a payment method.

Read our docs for an [overview of Developer Spaces](/platform/forge/developer-space/developer-spaces-introduction/). For pricing details and free thresholds, visit [Forge platform pricing](/platform/forge/forge-platform-pricing/). To understand space-level roles and permissions, review [Developer Space roles](/platform/forge/developer-space/developer-space-roles/).

## How billing works for a Developer Space

Billing for Forge usage is managed at the **Developer Space** level:

* All apps in a Developer Space contribute to the same Forge usage bill.
* Usage is aggregated in a **billing (transaction) account** that’s linked to the space.
* Charges are calculated based on your monthly usage and any applicable free thresholds.
* Invoices are generated monthly and charged automatically when you have a valid payment method.

Key points:

* **One transaction account per Developer Space**: Each Developer Space is linked to a billing (transaction) account that lives in the Billing Console. Space admins can see the billing status from the Developer Space **Settings** page.
* **Monthly billing cycle and autopay**: Invoices are generated on the **first day of each month**, covering usage from the previous month.
  If you’ve added a valid payment method, an **automatic payment (autopay)**- is attempted on the first of each month for the total invoice amount.
* **Free usage threshold**: If your total usage for all apps in the space stays within the free threshold, your total monthly cost is $0. Learn [how the free threshold works and what’s included](/platform/forge/forge-platform-pricing/) in the Forge platform pricing.

## Add or update a payment method

To be charged for Forge usage above the free threshold, your billing account needs a valid payment method.

### Before you begin

You’ll need:

* Access to the **Developer Console**.
* The appropriate billing permissions (for example, you’re a **billing admin** for the transaction account linked to the Developer Space).

Billing administration is managed in the **Billing Console**. From a Developer Space, you’ll use shortcuts to open the relevant billing account.

To learn how to set up your Developer Space before configuring billing, read our docs on [how to create](/platform/forge/developer-space/create-developer-space/) and [manage Developer Spaces](/platform/forge/developer-space/manage-developer-space/).

#### Add a payment method from the Developer Console

1. In the Developer Console, open the **Developer Space** you want to manage.  
   If billing has not been set up, follow the prompts in the developer console to review terms if applicable and add the payment method.
2. You can also go to **Settings** for the space, and select **Go to Billing Console**. Next, in the billing account:  
   a. Go to the **Payment methods** section in the left navigation.  
   b. Select **Add payment method**.  
   c. Choose one of the supported options (for example, credit card, debit card, PayPal, or ACH, depending on your region).  
   d. Enter your billing details and save.

After you’ve successfully added a payment method:

* The payment method is used for **automatic monthly payments** for that billing account.
* You’ll see updated status for billing in the Developer Space **Settings** page.

## Access your billing account from a Developer Space

You can open the billing account that backs your Developer Space directly from the Developer Console.

From the Developer Console:

1. Open your **Developer Space**.
2. Go to **Settings**.
3. Use one of the following:

* In the **Billing account** section, select **Go to Billing Console** to open the billing account.
* If prompted after adding a card, select **Manage subscriptions** to open the billing account in a new tab.

In the billing account, you can review subscriptions, usage, invoices, and payment methods for the apps in that Developer Space.

## Navigate your billing account

The billing account (Billing Console) provides a left navigation to manage and review your charges.

| Left-hand nav sections | Description |
| --- | --- |
| Subscriptions | See all active subscriptions related to your Forge usage and related products. From here, you can open a subscription to see detailed usage and charges. |
| Billing profiles | Update your organization name, billing address, and (where applicable) shipping address used on invoices. |
| Payment methods | Add, update, or remove payment methods used for auto-payment. Only billing admins can change payment methods and billing profile details. Other roles may have read-only access, depending on your organization’s configuration. |
| Addresses | View or edit your billing address and sold-to address. |
| Billing permissions | Add another billing admin. |
| Invoices | Download invoices, review previous charges, and confirm whether an invoice has been paid. |

## View subscriptions and usage details

Once you’ve opened your billing account, you can drill into subscriptions and usage.

### View subscription details

1. In the billing account, go to the **Subscriptions** section in the left navigation.
2. Select the subscription associated with your Forge Developer Space.
3. On the subscription details page, you can see:

* A summary of the current plan or pricing model.
* The latest invoice amount and billing period.
* Links to **View usage** and **View invoices**.

### View daily usage charts

To see how your usage changes over time:

1. From the subscription details page, select **View usage**.
2. Use the filters and date range controls to:

* View **daily usage charts**.
* Break down usage by site or resource type (where supported).
* Understand peaks and trends in usage across the billing period.

Learn more about [usage metrics and charts](/platform/forge/monitor-usage-metrics/).

## Understand monthly invoices and autopay

Once a payment method and billing details are set up:

* On the **first day of each month**, the billing system:
  * Calculates your total usage for the previous month.
  * Generates an invoice for that billing period.
  * Attempts an automatic payment using your saved payment method.

What happens next depends on your usage and payment setup:

* If your total usage is within the free threshold, your total cost is $0 for that month.
* If your total usage exceeds the free threshold, you’ll see a non-zero invoice amount.
  The autopay charge uses your saved payment method. If the payment succeeds, the invoice is marked as paid.

Billing admins can download invoices and see payment status in the billing account.

## What happens if you don’t add a payment method?

You may choose not to add a payment method right away. The impact depends on whether your apps stay within the free threshold or exceed it.

**Scenario 1: Apps stay within the free threshold**
If the combined usage of all apps in your Developer Space stays within the free threshold:

1. **No payment is required.**
   Your total charge for that billing period is $0.
2. **Invoice behaviour**:

* If no **billing profile or addresses** are set, invoice generation may be skipped for that period.
* If you’ve added **billing and shipping address details**, but no **payment method**, a **$0 invoice** can still be generated and made available in the billing account.
  Billing admins can download and keep these $0 invoices for their records.

3. **No dunning or enforcement.**
   Because the apps are within the free threshold and there’s no outstanding balance:

* No dunning (payment collection) process is triggered.
* No enforcement actions are taken against your apps.

You can continue to use your apps in the Developer Space as long as your total usage remains within the free threshold.

**Scenario 2: Apps in the developer space exceed the free threshold (cost > $0)**. What happens then depends on your billing setup.

**When required billing details are missing**
If there’s **no valid payment method or required billing details** (for example, missing billing address) in the billing account:

1. **Invoice generation can fail.**
   The system attempts to generate an invoice, but if required billing information is missing, invoice creation or payment can fail.
2. **Dunning is triggered.**
   When invoice generation or payment fails, the billing system moves the apps into a **dunning state**:

* Dunning is a period where we repeatedly try to collect payment and notify you that there’s a problem with your billing details.
* The dunning period lasts for **21 days**.
* During this time, you’ll have **multiple opportunities (up to 5 retries)** to add or fix a payment method and resolve the issue.

3. **Notifications and retries.**
   Billing admins are notified about the failed payment or missing details. The system:

* Retries the payment several times.
* Prompts billing admins to update billing details and payment methods.

**After the dunning period**
If the issue is not resolved after the dunning period:

* **App enforcement actions** may apply to the apps in the Developer Space that generated the charges.
  For example, this can include restrictions or suspension that affect how the apps run for your customers.

To avoid dunning and enforcement:

## Keep billing healthy for your Developer Space

To reduce billing friction for your team and your customers:

* **Set up billing early**
  Add a payment method and billing details when you first create or start using a Developer Space, even if you expect to stay within free thresholds.
* Learn [how to monitor usage](/platform/forge/monitor-usage-metrics/), and utilise the **View usage charts** in your billing account to track how close you are to thresholds.
* **Review invoices and payment status**
  Make sure billing admins check new invoices and payment status each month, especially after significant increases in app adoption.
* **Keep billing admins up to date**
  Ensure the right people are assigned as billing admins in the Billing Console, and that contact details and email addresses are correct, so they receive billing and dunning notifications.

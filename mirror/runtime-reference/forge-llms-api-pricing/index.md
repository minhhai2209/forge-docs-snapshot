# Forge LLMs pricing

**No free usage allowance:** The Forge LLMs API does not include a free monthly usage quota. All token usage is billed.

Forge LLMs usage is charged to the developer of the Forge app and counted toward your Forge monthly bill.

## How billing works

Forge LLMs billing follows a three-step process:

1. **Token usage** — Your app consumes input and output tokens when calling an LLM model.
2. **Token-to-credit conversion** — Tokens are converted to credits using the model's conversion rate. More powerful models use more credits per token.
3. **Credit-to-cost calculation** — Credits are priced in USD to determine your final cost.

On your bill, you see two line items: input credits and output credits. You can also see a detailed breakdown of usage per model in the developer console.

## Credit conversion rates

The model names in this table correspond to the Claude variants listed in [Forge LLMs models](/platform/forge/runtime-reference/forge-llms-models/).

The following table shows how many credits each model consumes per 1 million tokens. The USD columns show the effective cost after applying the credit billing rates below.

| Model | Credits per 1M tokens | Effective cost per 1M input tokens ($USD) | Effective cost per 1M output tokens ($USD) |
| --- | --- | --- | --- |
| Opus 4.6 | 50 credits | $5 | $25 |
| Sonnet 4.5 | 30 credits | $3 | $15 |
| Haiku 4.5 | 10 credits | $1 | $5 |

## Credit billing rates

Credits are billed at the following rates:

* **Input credits:** $0.10 per credit
* **Output credits:** $0.50 per credit

## Worked example

Suppose your app consumes the following tokens in a given month:

* Opus 4.6: 0.5M input tokens and 0.2M output tokens
* Haiku 4.5: 5M input tokens and 1M output tokens

### Step 1: Convert tokens to credits

Multiply the token count (in millions) by the model's rate from the table:

* Opus 4.6: 0.5M input tokens × 50 credits per 1M tokens = **25 input credits**; 0.2M output tokens × 50 credits per 1M tokens = **10 output credits**
* Haiku 4.5: 5M input tokens × 10 credits per 1M tokens = **50 input credits**; 1M output tokens × 10 credits per 1M tokens = **10 output credits**

### Step 2: Sum the credits

* Total input credits: 25 + 50 = **75 input credits**
* Total output credits: 10 + 10 = **20 output credits**

### Step 3: Calculate the cost

Apply the credit billing rates:

* Input cost: 75 input credits × $0.10 per credit = $7.50
* Output cost: 20 output credits × $0.50 per credit = $10.00
* **Total monthly cost: $7.50 + $10.00 = $17.50**

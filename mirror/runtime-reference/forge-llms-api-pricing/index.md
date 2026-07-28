# Forge LLMs pricing (Preview)

Forge LLMs is now available as *preview* feature.

Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

**No free usage allowance:** The Forge LLMs API does not include a free monthly usage quota. All token usage is billed.

Forge LLM usage is charged to the developer of the Forge app and counted toward your Forge monthly bill.

Forge LLM usage is tracked in credits, which correspond to model input and output tokens. Each model has a token-to-credit conversion ratio, and more powerful models use more credits per token. On your bill you'll see two line items: input credits and output credits. You can also see a detailed breakdown of usage per model in the developer console.

## Model pricing per token usage

The model names in this table correspond to the Claude variants listed in [Forge LLMs models](/platform/forge/runtime-reference/forge-llms-models/).

| Model | Credits per 1M tokens | Price per 1M input tokens ($USD) | Price per 1M output tokens ($USD) |
| --- | --- | --- | --- |
| Opus 4.6 | 50 credits | $5 | $25 |
| Sonnet 4.5 | 30 credits | $3 | $15 |
| Haiku 4.5 | 10 credits | $1 | $5 |

## Billing in Forge LLM Credits

Forge LLM credits are priced at **$0.10 per 1M input credits** and **$0.50 per 1M output credits**.

## Worked example

For example, suppose your app consumes the following tokens in a given month:

* Opus 4.6: 0.5M input tokens and 0.2M output tokens
* Haiku 4.5: 5M input tokens and 1M output tokens

Converting the tokens to LLM credits for billing:

* Opus 4.6: (0.5 × 50) = 25M input credits + (0.2 × 50) = 10M output credits
* Haiku 4.5: (5 × 10) = 50M input credits + (1 × 10) = 10M output credits
* Total credits: 75M input credits + 20M output credits
* Total cost: Input (75 × $0.10) + Output (20 × $0.50) = $7.50 + $10.00 = **$17.50**

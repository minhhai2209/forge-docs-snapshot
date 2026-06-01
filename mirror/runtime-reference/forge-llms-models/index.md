# Forge LLMs models (Preview)

Forge LLMs is now available as *preview* feature.

Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge LLMs supports three Claude variants: Sonnet, Opus, and Haiku. You choose the model per request, allowing you to balance latency, capability, and cost for each use case.

## Supported models

You can use the `list` method from the [@forge/llm SDK](/platform/forge/runtime-reference/forge-llms-api/#forgelllm-sdk) to dynamically fetch the list of supported models and their current status.

You can use the `list` method from the [@forge/llm SDK](/platform/forge/runtime-reference/forge-llms-api-reference/) to dynamically fetch the list of supported models and their current status.
|:-----------------------------|:--------|:-------|:---------|:----|
| `claude-haiku-4-5-20251001` | Haiku | Claude | `ACTIVE` | |
| `claude-sonnet-4-20250514` | Sonnet | Claude | `ACTIVE` | |
| `claude-sonnet-4-5-20250929` | Sonnet | Claude | `ACTIVE` | |
| `claude-opus-4-1-20250805` | Opus | Claude | `ACTIVE` | |
| `claude-opus-4-5-20251101` | Opus | Claude | `ACTIVE` | |
| `claude-opus-4-6` | Opus | Claude | `ACTIVE` | |

AI models evolve quickly. Check the `status` and `EOL` fields regularly, and update your app before a model reaches end-of-life to avoid disruption. Initially only text input/output is supported; multimodal support may be considered later.

## Claude - Opus

* Most capable (best for complex, deep reasoning tasks)
* Slowest (higher latency due to depth)
* Highest cost

## Claude - Sonnet

* Balanced capability
* Moderate speed
* Moderate cost

## Claude - Haiku

* Fast and efficient (best for lightweight or high‑volume tasks)
* Lowest cost

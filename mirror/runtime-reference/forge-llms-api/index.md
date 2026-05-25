# Forge LLMs API (EAP)

[Forge LLMs](/platform/forge/runtime-reference/forge-llms-api/) is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production — [sign up here](https://go.atlassian.com/signup-forge-llms) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Forge LLMs lets your Forge app call Atlassian‑hosted large language models (LLMs) to add secure AI features without leaving the Atlassian platform. Apps using this API are badged as [**Runs on Atlassian**](/platform/forge/runs-on-atlassian/), indicating they leverage Atlassian’s security, compliance, and scalability. The API provides optimized, governed access to supported models so you can focus on creating innovative AI experiences while Atlassian handles model integration and infrastructure.

## Manifest reference for LLM module

See the [LLM module reference](/platform/forge/manifest-reference/modules/llm/) for details on the `llm` module for your
`manifest.yml`.

## Versioning

The `llm` module is required to enable Forge LLMs. When you add the `llm` module to an app's `manifest.yml`, it triggers a major version upgrade and requires administrators of existing installations to review and approve the update.

## EAP limitations

During the EAP, you are blocked from deploying your app to the `production` and `staging` environments. You cannot distribute your app or list it on the Atlassian Marketplace.

## Tutorials and example apps

## Node.js SDK

The [@forge/llm SDK](https://www.npmjs.com/package/@forge/llm?activeTab=readme) gives you a lightweight, purpose-built client for invoking Atlassian-hosted LLMs directly from Forge runtime functions.

Use `chat()` for structured multi-turn exchanges. Use `stream()` to incrementally receive LLM responses as smaller chunks. Provide 'tool' definitions so the model can call typed functions, and inspect returned usage to guide adaptive behaviour.

For runnable examples (tool wiring, retries, error handling), see the [Forge LLMs tutorials and example apps](#tutorials-and-example-apps) section above.

### Method signature

Please refer to the [request](/platform/forge/runtime-reference/forge-llms-api/#request) and the [response](/platform/forge/runtime-reference/forge-llms-api/#response) schemas.

```
```
1
2
```



```
list() => Promise<ModelListResponse>
chat(Prompt) => Promise<LlmResponse>
stream(Prompt) => Promise<StreamResponse>
```
```

### Example usage

#### Using chat

```
```
1
2
```



```
import { chat } from '@forge/llm';
try {
  const response = await chat({
    model: 'claude-3-7-sonnet-20250219',
    messages: [
      {
        role: 'user', content: 'Write a short poem about Forge LLMs.'
      }
    ],
  });

  console.log("#### LLM response:", JSON.stringify(response));
} catch (err) {
  console.error('#### LLM request failed:', { error:  err.context?.responseText });
  throw err;
}
```
```

#### Using stream

```
```
1
2
```



```
import { stream } from '@forge/llm';
try {
  const response = await stream({
    model: 'claude-3-7-sonnet-20250219',
    messages: [
      {
        role: 'user', content: 'Write a short poem about Forge LLMs.'
      }
    ],
  });

  for await (const chunk of response) {
    console.log("#### LLM response:", JSON.stringify(chunk));
  }

  response.close();

} catch (err) {
  console.error('#### LLM request failed:', { error:  err.context?.responseText });
  throw err;
}
```
```

### Module validation

The SDK requires the `llm` module to be defined in your `manifest.yml`. If the SDK is used without declaring this module, linting will fail with an error like:

```
```
1
2
```



```
Error: LLM package is used but 'llm' module is not defined in the manifest
```
```

The SDK can automatically fix your manifest. After linting, the manifest will include:

**Example of corrected manifest.yml:**

```
```
1
2
```



```
modules:
  llm:
    - key: llm-app
      model:
        - claude
```
```

Please refer to the [LLM module reference](/platform/forge/manifest-reference/modules/llm/) for details on how to define the module.

### Request and response schemas

Please consult the [@forge/llm](https://www.npmjs.com/package/@forge/llm?activeTab=readme) package for the most up-to-date request and response schema definitions.

#### Request

```
```
1
2
```



```
interface Prompt {
  model: string;
  messages: {
    role: "system" | "user" | "assistant" | "tool";
    content: string | { type: 'text'; text: string; }[];
  }[];
  max_completion_tokens?: number;
  temperature?: number;
  top_p?: number;
  tools?: {
    type: "function";
    function: {
      name: string;
      description: string;
      parameters: object;
    };
  }[];
  tool_choice?: "auto" | "none" | "required" | { type: "function"; function: { name: string } };
}
```
```

#### Response

```
```
1
2
```



```
interface LlmResponse {
  choices: {
    finish_reason: string;
    index?: number;
    message: {
      content: string | { type: "text"; text: string; }[];
      role: "assistant";
      tool_calls?: {
        id: string;
        type: "function";
        index: number;
        function: { name: string; arguments: object; };
      }[];
    };
  }[];
  usage?: { input_token?: number; output_token?: number; total_token?: number; };
}

interface StreamResponse extends AsyncIterable<LlmResponse> {
  close(): Promise<void> | undefined;
}

interface ModelListResponse {
  models: {
    model: string;
    status: "active" | "deprecated";
  }[];
}
```
```

### Important validation rules

The following request validation rules apply to specific models:

| Rule | Models |
| --- | --- |
| When adjusting sampling parameters, modify either `temperature` or `top_p`. Do not modify both at the same time. | `claude-haiku-4-5-20251001`, `claude-sonnet-4-5-20250929` |

## Model selection

We plan to launch with support for three Claude variants: Sonnet, Opus, and Haiku. You choose the model per request, allowing you to balance latency, capability, and cost for each use case.

### Supported models

You can use the `list` method from the SDK to dynamically fetch the list of supported models and their respective status.

| Model ID | Variants | Family | Status | EOL |
| --- | --- | --- | --- | --- |
| `claude-haiku-4-5-20251001` | Haiku | Claude | `ACTIVE` |  |
| `claude-sonnet-4-5-20250929` | Sonnet | Claude | `ACTIVE` |  |
| `claude-opus-4-6` | Opus | Claude | `ACTIVE` |  |

As AI models evolve quickly, check regularly for deprecated status and associated EOL dates so your apps do not break.

### Claude - Opus

* Most capable (best for complex, deep reasoning tasks)
* Slowest (higher latency due to depth)
* Highest cost

### Claude - Sonnet

* Balanced capability
* Moderate speed
* Moderate cost

### Claude - Haiku

* Fast and efficient (best for lightweight or high‑volume tasks)
* Lowest cost

AI models evolve quickly, so specific versions may change before launch. Initially only text input/output is supported; multimodal support may be considered later.

## Admin experience

Administrators will be informed (Marketplace listing and during installation) when an app uses Forge LLMs. Adding Forge LLMs—or a new model family—to an existing app triggers a major version upgrade requiring admin approval.

## Usage tracking

The Forge LLM API reports usage data per request (the number of input and output tokens consumed) in the API response.

During the EAP, usage tracking is limited to the data provided in the API response.

## Pricing (coming soon)

When LLMs graduate to Preview and General Availability, they will be a billable Forge capability. LLM usage is charged to the developer of the Forge app, and usage will be counted toward your Forge monthly bill. The Forge LLMs API does not include a free monthly usage quota.

Forge LLM usage is tracked in credits, which correspond to model input and output tokens. Each model has a token-to-credit conversion ratio, and more powerful models use more credits per token.

On your bill you'll see two line items: input credits and output credits. You can also see a detailed breakdown of usage per model in the developer console.

### Model pricing per token usage

| Model | Credits per 1M tokens | Price per 1M input tokens ($USD) | Price per 1M output tokens ($USD) |
| --- | --- | --- | --- |
| Opus 4.6 | 50 credits | $5 | $25 |
| Sonnet 4.5 | 30 credits | $3 | $15 |
| Haiku 4.5 | 10 credits | $1 | $5 |

### Billing in Forge LLM Credits

| Price per input credit ($USD) | Price per output credit ($USD) |
| --- | --- |
| $0.10 / 1M credits | $0.50 / 1M credits |

### Worked example

In a given month imagine your app consumes (in millions of tokens):

* Opus 4.6: 0.5M input tokens and 0.2M output tokens
* Haiku 4.5: 5M input tokens and 1M output tokens

Converting the tokens to LLM credits for billing:

* Opus 4.6: (0.5 × 50) = 25M input credits + (0.2 × 50) = 10M output credits
* Haiku 4.5: (5 × 10) = 50M input credits + (1 × 10) = 10M output credits
* Total credits: 75M input credits + 20M output credits
* Total cost: Input (75 × $0.10) + Output (20 × $0.50) = $7.50 + $10.00 = **$17.50**

## Responsible AI

Requests to Forge LLMs undergo the same moderation checks as Atlassian first‑party AI and Rovo features. High‑risk messages (per the Acceptable Use Policy) are blocked.

## Handling streaming errors

Streaming responses from LLMs increase the risk of delivering incomplete output to the user, particularly in cases of interruptions such as timeouts or network failures.

Instead of resubmitting the original prompt, a better way to recover is to prompt the LLM with prior context. For example, if chunked text responses have been accumulated into a variable `storedOutput`, you can use the following user prompt to recover:

```
```
1
2
```



```
`You were interrupted in your previous attempt.
Your original instruction was "${originalUserPrompt}".
Continue from the following interrupted output: ${storedOutput}`
```
```

We’ve observed that Claude Sonnet 4.5 typically responds in one of two ways:

* It successfully resumes text generation by continuing from the previously interrupted output.
* It explains that the previous output already fulfilled the original instruction, and why.

### Detecting when to retry

Platform interruptions can cause streaming to conclude before a complete response is delivered. In other words, not only can the LLM’s text output cut off prematurely, but the client can also fail to receive finalising streaming messages. One way to detect incomplete responses, and therefore attempt a retry, is to check whether a completion choice object with a `finish_reason` property is missing when the stream ends:

```
```
1
2
```



```
let isStreamComplete = false;
const checkIfFinishReasonExists = (chunk) =>
  !!chunk.choices.find(({ finish_reason }) => finish_reason !== undefined);

try {
  const response = await stream(myPrompt);

  for await (const chunk of response) {
    if (checkIfFinishReasonExists(chunk)) {
      isStreamComplete = true;
    }
  }
} catch (e) {
  // Exceptions are not thrown for finishing streams with incomplete responses.
} finally {
  response.close();
}

console.log(`Is the stream complete? ${isStreamComplete}`);
```
```

# Forge LLMs API

[Forge LLMs](/platform/forge/runtime-reference/forge-llms-api/) is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production — [sign up here](https://go.atlassian.com/signup-forge-llms) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Forge LLMs lets your Forge app call Atlassian‑hosted large language models (LLMs) to add secure AI features without leaving the Atlassian platform. Apps using this API are badged as [**Runs on Atlassian**](/platform/forge/runs-on-atlassian/), indicating they leverage Atlassian’s security, compliance, and scalability. The API provides optimized, governed access to supported models so you can focus on creating innovative AI experiences while Atlassian handles model integration and infrastructure.

## Manifest reference for LLM module

See the [LLM module reference](/platform/forge/manifest-reference/modules/llm/) for details on the `llm` module for your
`manifest.yml`.

**Important:**

The app retains its [**Runs on Atlassian**](/platform/forge/runs-on-atlassian) eligibility after the module is added.

## Versioning

The `llm` module is required to enable Forge LLMs. When you add the `llm` module to an app's `manifest.yml`, it triggers a major version upgrade and requires administrators of existing installations to review and approve the update.

## EAP limitations

During the EAP, you are blocked from deploying your app to the `production` environment and cannot list the app publicly on Marketplace.

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

| Model ID | Variants | Family | Status | EOL |
| --- | --- | --- | --- | --- |
| `claude-3-5-haiku-20241022` | Haiku | Claude | `ACTIVE` |  |
| `claude-haiku-4-5-20251001` | Haiku | Claude | `ACTIVE` |  |
| `claude-3-7-sonnet-20250219` | Sonnet | Claude | `ACTIVE` |  |
| `claude-sonnet-4-20250514` | Sonnet | Claude | `ACTIVE` |  |
| `claude-sonnet-4-5-20250929` | Sonnet | Claude | `ACTIVE` |  |
| `claude-opus-4-20250514` | Opus | Claude | `DEPRECATED` | February 2026 |
| `claude-opus-4-1-20250805` | Opus | Claude | `ACTIVE` |  |
| `claude-opus-4-5-20251101` | Opus | Claude | `ACTIVE` |  |

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

## Pricing

LLMs will become a paid Forge feature soon. Usage (token input/output volume) will appear in the developer console under usage and costs. Specific pricing will be published before preview.

## Responsible AI

Requests to Forge LLMs undergo the same moderation checks as Atlassian first‑party AI and Rovo features. High‑risk messages (per the Acceptable Use Policy) are blocked.

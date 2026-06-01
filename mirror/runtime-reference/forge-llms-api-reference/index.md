# Forge LLMs API reference (Preview)

Forge LLMs is now available as *preview* feature.

Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The [@forge/llm SDK](https://www.npmjs.com/package/@forge/llm?activeTab=readme) gives you a lightweight, purpose-built client for invoking Atlassian-hosted LLMs directly from Forge runtime functions.

Use `chat()` for structured multi-turn exchanges. Use `stream()` to incrementally receive LLM responses as smaller chunks. Provide 'tool' definitions so the model can call typed functions, and inspect returned usage to guide adaptive behaviour.

For runnable examples (tool wiring, retries, error handling), see the [Forge LLMs tutorials and example apps](/platform/forge/runtime-reference/forge-llms-api/#tutorials-and-example-apps) section.

## Module

The SDK requires the [`llm` module](/platform/forge/manifest-reference/modules/llm/) to be defined in your `manifest.yml`. If the SDK is used without declaring this module, linting will fail with an error like:

```
1
Error: LLM package is used but 'llm' module is not defined in the manifest
```

The SDK can automatically fix your manifest. After linting, the manifest will include:

**Example of corrected manifest.yml:**

```
1
2
3
4
5
modules:
  llm:
    - key: llm-app
      model:
        - claude
```

### Versioning

The `llm` module is required to enable Forge LLMs. When you add the `llm` module to an app's `manifest.yml`, it triggers a major version upgrade and requires administrators of existing installations to review and approve the update.

## Method signature

The SDK supports the following methods:

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

Both methods support a `chat` and a `stream` interface available for all supported models. See the [@forge/llm](https://www.npmjs.com/package/@forge/llm?activeTab=readme) package for the most up-to-date request and response schema definitions.

### Request schema

```
```
1
2
```



```
```javascript
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

### Response schema

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

### Example: Using chat

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

### Example: Using stream

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

## Validation rules

The following request validation rules apply to specific models:

| Rule | Models |
| --- | --- |
| When adjusting sampling parameters, modify either `temperature` or `top_p`. Do not modify both at the same time. | `claude-haiku-4-5-20251001`, `claude-sonnet-4-5-20250929` |

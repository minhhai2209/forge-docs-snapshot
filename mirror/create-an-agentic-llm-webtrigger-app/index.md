# Create an agentic LLM web trigger using Forge LLMs

[Forge LLMs](/platform/forge/runtime-reference/forge-llms-api/) is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production — [sign up here](https://go.atlassian.com/signup-forge-llms) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This tutorial demonstrates how enabling tool usage unlocks agentic capabilities in Forge apps, without relying on advanced frameworks like Langchain.

By following this guide, you will:

1. Integrate the Forge LLMs module with the Web trigger module for dynamic, user-driven interactions.
2. Implement agentic LLM behavior, allowing the LLM to call external functions (tools) as part of its reasoning process.
3. Build and test a practical example where the LLM can fetch live data (like weather) by invoking a tool.
4. Understand how to structure prompts, handle tool calls, and extend your app for more complex agentic workflows.

---

## 1. Prerequisites

Before you begin, ensure you have the following:

* A configured Forge development environment ([Getting Started Guide](https://developer.atlassian.com/platform/forge/getting-started/))
* Access to an Atlassian site for app installation (create one if needed)
* Forge CLI installed and authenticated
* **Quick Start**: This tutorial assumes you have completed [our first tutorial](https://developer.atlassian.com/platform/forge/create-an-llm-webtrigger-app/), where we have a working Forge LLMs Web trigger app as your starting point.

---

## 2. App setup

### 2.1 Complete our first tutorial

# Important

As mentioned in the **Prerequisites**, please complete [our first tutorial here](https://developer.atlassian.com/platform/forge/create-an-llm-webtrigger-app/).

* Ensure you have your Application ID correctly set in the `app.id` field, and not the `<your-unique-app-uuid>` placeholder.
* Register your app for the FORGE LLMs [Early Access Program (EAP)](https://go.atlassian.com/signup-forge-llms) before general availability.

**Overview**:
In this step, you'll extend your Forge LLMs app to support “agentic” behavior—enabling the LLM to call external functions (tools) as part of its reasoning process. This allows your app to dynamically execute code (such as fetching weather data) in response to user prompts, making your LLM integration far more powerful and interactive.

**To achieve this, your app will:**

1. **Send the initial prompt**: Pass the user’s prompt to the LLM, including the available tool(s) in the request.
2. **Inspect the LLM’s response**: Check if the LLM wants to use a tool (via a tool\_use message).
3. **Execute the tool and follow up**: If a tool is called, run it, then send the result back to the LLM in a follow-up prompt to get the final answer.
4. **Implement the tool function**: It's important to define the external function (e.g., get\_current\_weather) that the LLM can call.
5. **(Optional) Repeat as needed**: In more complex agentic flows, the LLM may call multiple tools before producing a final response.

Let's get started!

In `src/index.js`, update the app with

```
```
1
2
```



```
import { chat } from "@forge/llm";

exports.runSync = async (event, context) => {
  let finalResponse={};

  try {
    /* 1. Build and request the initial prompt. */
    const llmPrompt = JSON.parse(event.body);
    finalResponse = await chat(llmPrompt);

    /* 2. Handle tool_use: executed required "tool", and share the response with LLM */
    const firstChoice = finalResponse.choices[0];
    if (firstChoice?.message?.role === 'assistant' && !!firstChoice.message?.tool_calls) {
      const promptWithToolResult = await executeToolAndBuildToolUsePrompt(
              {
                toolUseAssistantChoice: firstChoice,
                initialPrompt: llmPrompt
              });

      /* Update finalResponse */
      finalResponse = await chat(promptWithToolResult);
    }

    return buildOutput(
            JSON.stringify({
              success: true,
              choices: finalResponse.choices,
            }),
            200,
            "OK"
    );
  } catch (err) {
    return buildOutput(
            JSON.stringify({
              success: false,
              error: err?.message || err,
              errorDetails: err.context?.responseText
            }),

            err.statusCode ?? 500,
            err.statusText ?? "Unknown Error"
    );
  }
};

/* 3. Execute the "tool" and build a new prompt */
async function executeToolAndBuildToolUsePrompt({ toolUseAssistantChoice, initialPrompt }) {
  const toolCall = toolUseAssistantChoice?.message.tool_calls?.[0];
  if (toolUseAssistantChoice.finish_reason !== 'tool_use' || !toolCall || toolCall.function?.name !== 'get_current_weather') return null;

  let args = {};
  try { args = typeof toolCall.function.arguments === 'string' ? JSON.parse(toolCall.function.arguments) : toolCall.function.arguments; } catch {}

  const result = await get_current_weather(args.location, args.unit);
  const requiredToolUseAssistantMessage = toolUseAssistantChoice.message; // Add proper validation when needed

  /* The prompt must include three types of messages:
   * 1. The original user and/or system messages from the initial prompt.
   * 2. The assistant's message indicating a tool should be used (`tool_use`).
   * 3. A tool message containing the function's result and context for the assistant.
   */
  return {
    messages: [
      ...initialPrompt.messages,
      requiredToolUseAssistantMessage,
      {
        role: "tool",
        content: [{ type: "text", text: JSON.stringify(result), tool_use: toolCall.id }],
        tool_call_id: toolCall.id,
        name: toolCall.function.name
      },
    ],
    model: initialPrompt.model,
  };
}

/* 4. A mock implementation of a weather tool */
async function get_current_weather(location, unit = 'celsius') {
  const temperature = Math.floor(Math.random() * 16) + 15; // 15°C to 30°C
  const conditions = ['clear skies', 'cloudy', 'rainy', 'sunny', 'windy', 'foggy'];
  const condition = conditions[Math.floor(Math.random() * conditions.length)];
  return { location, unit, temperature, condition };
}

const buildOutput = (body, statusCode, statusText) => ({
  body,
  headers: {
    'Content-Type': ['application/json'],
    'X-Request-Id': [`rnd-${Math.random()}`]
  },
  statusCode,
  statusText,
});
```
```

---

### 2.3 Deploy and install

```
```
1
2
```



```
forge deploy
# ✔ Deployed
forge install # OR 'forge install upgrade'
# ✔ Install in <Atlassian app> complete!
```
```

### 2.4 Test the web trigger endpoint

Get your Web trigger URL:

```
```
1
2
```



```
# ? Select an installation:  (Use the Enter key to select)
# ┌───────────────┬────────────────────┬────────────────┬───────────────┐
# │ Environment   │ Site               │ Atlassian apps │ Major Version │
# ├───────────────┼────────────────────┼────────────────┼───────────────┤
# │ ❯ environment │ <your-site>        │ <App>          │ 2 (Latest)    │
# └───────────────┴────────────────────┴────────────────┴───────────────┘
# ? Select a web trigger: llm-webtrigger-app-webtrigger-sync
# Copy your web trigger URL below to start using it:
# https://<WEBTRIGGER_URL>
```
```

#### Request example

Before we call the endpoint, let's create or update the `request.json` file with the following content:

```
```
1
2
```



```
{
  "model": "claude-3-5-haiku-20241022",
  "messages": [
    { "role": "user", "content": "What is the weather like in Melbourne?" },
    {
      "role": "system",
      "content": "Your role is to support our AI weather tool."
    }
  ],
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": { "type": "string", "description": "The city and state, e.g. Sydney, CA" },
          "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
        },
        "required": ["location"]
      }
    }
  }],
  "tool_choice": "auto"
}
```
```

We are providing `tools` block, with relevant tool's context such as description, name and parameters etc.

Now we call the Web trigger endpoint with initial prompt:

```
```
1
2
```



```
curl -X POST https://<WEBTRIGGER_URL> \
  -H "Content-Type: application/json" \
  -d @request.json | jq "."
```
```

#### Response example

```
```
1
2
```



```
{
  "success": true,
  "choices": [
    {
      "finish_reason": "end_turn",
      "message": {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "Currently in Melbourne, it's 22°C and rainy. I recommend bringing an umbrella or raincoat if you're heading out."
          }
        ]
      }
    }
  ]
}
```
```

---

### 2.5 Schema reference for 'chat'

**Prompt:**

```
```
1
2
```



```
{
  "messages": [
    {
      "role": "system | user | assistant | tool",
      "content": "string | ContentPart[]"
    }
  ],
  "temperature": number,
  "max_completion_tokens": number,
  "top_p": number,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "string",
        "description": "string",
        "parameters": "object"
      }
    }
  ],
  "tool_choice": "auto | none | required | { type: 'function', function: { name: string } }"
}
```
```

**Required:**

```
```
1
2
```



```
- messages: The conversation content, including system, user, assistant, or tool messages.
```
```

#### Optional:

```
```
1
2
```



```
- temperature: Controls randomness in responses; higher values produce more creative output.
- max_completion_tokens: Limits the maximum number of tokens in the generated response.
- top_p: Controls diversity via nucleus sampling; lower values make output more focused.
- tools: List of function tools available for the LLM to use during generation.
- tool_choice: Specifies which tool (if any) the LLM should use for the current prompt.
```
```

**Prompt Response:**

```
```
1
2
```



```
{
  "choices": [
    {
      "finish_reason": string, // "tool_use", "end_turn", "max_tokens", etc.
      "index": 0,
      "message": {
        "role": string, // "assistant"
        "content": string | ContentPart[],
        "tool_calls": [
          {
            "id": "<tool_call_id>",
            "type": "function",
            "index": number,
            "function": {
              "name": "<function_name>",
              "arguments": { /* function arguments */ }
            }
          }
        ]
      }
    }
  ]
}
```
```

---

## 3. Troubleshooting

* If you receive a `"status": 424` in your curl response, this usually means there is an error in your Web trigger function code.
  * Run `forge logs` to get more details and pinpoint the issue. You can use `forge logs -n 50` to see the last 50 log lines.
* Seeing `Error: Not logged in` during forge deploy or forge install? You need to authenticate your CLI by running `forge login`.
* If server errors are unclear, reach out to [Atlassian Developer Support](https://developer.atlassian.com/support/) with your app ID and error details.

### Tips

* Double-check that your prompt JSON is valid and matches the expected schema.
* Use `forge tunnel`, `curl` for real-time development and testing. This lets you see changes instantly without redeploying every time.
* Always run `forge lint` before deploying to catch manifest or code issues early.
* When updating scopes or permissions in `manifest.yml`, remember to redeploy and reinstall your app for changes to take effect.

## Conclusion

You have now built a Forge app that combines LLMs with agentic capabilities and dynamic Web triggers. This guide showed you how to let the LLM call external functions (tools), process their results, and deliver richer, more interactive responses. You are now equipped to extend your app with additional tools, customize agentic workflows, and integrate more Forge modules to unlock advanced AI-powered solutions.

## Source code

Please find the complete code for this tutorial in the [llm-agentic-webtrigger-app Bitbucket repository](https://bitbucket.org/atlassian/forge-llm-examples/src/main/llm-agentic-webtrigger-app/)

## Next steps

* Try customizing your prompt schema to suit your use case.
* Integrate with other Forge modules for more powerful workflows.

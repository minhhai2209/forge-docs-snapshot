# Create an LLM web trigger app using Forge LLMs

[Forge LLMs](/platform/forge/runtime-reference/forge-llms-api/) is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production — [sign up here](https://go.atlassian.com/signup-forge-llms) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This tutorial walks you through integrating the `llm` [module](/platform/forge/manifest-reference/modules/llm/) with the `webtrigger` module, enabling dynamic, user-driven LLM interactions in your Forge app.

By completing this guide, you’ll build a Forge app with a Web trigger endpoint using `@forge/llm`. The endpoint receives user input, forwards it to the LLM provider, and returns the generated response—all within the Forge platform.

If you're new to Web triggers, think of them as HTTP endpoints that let your Forge app interact with external systems or receive dynamic input from events or users. Please refer to the [Web trigger Module Documentation](https://developer.atlassian.com/platform/forge/manifest-reference/modules/web-trigger/) for more details.

---

## 1. Prerequisites

Before you begin, ensure you have the following:

* A configured Forge development environment ([Getting Started Guide](https://developer.atlassian.com/platform/forge/getting-started/))
* Access to an Atlassian site for app installation (create one if needed)
* Forge CLI installed and authenticated

---

## 2. App setup

### 2.1 Create a new Forge app

Use the Forge CLI to create your app. In this example, we’ll name it `llm-webtrigger-app`:

```
1
2
# First, authenticate with Forge if you haven’t already:
forge login
```

```
```
1
2
```



```
forge create
# ? Enter a name for your app: llm-webtrigger-app
# ? Select an Atlassian app or platform tool: Show All
# ? Select a category: Show All
# ? Select a template: webtrigger
```
```

Navigate to your app directory:

---

### 2.2 Configure the manifest with 'llm' module

Edit `manifest.yml` to include `llm` modules. Under the `llm` module, set the model to `claude`:

```
```
1
2
```



```
modules:
  # 'llm' module is required for LLM functionalities
  llm:
    - key: my-first-llm-app
      model:
        - claude
  # webtrigger module added automatically when you create a "webtrigger" app
  webtrigger:
    - key: llm-webtrigger-app-webtrigger-sync
      function: sync
      response:
        type: dynamic
  function:
    - key: sync
      handler: index.runSync
app:
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64
  id: ari:cloud:ecosystem::app/<your-unique-app-uuid>
```
```

# Important

* Ensure you have your Application ID correctly set in the `app.id` field, and not the `<your-unique-app-uuid>` placeholder.
* Register your app for the FORGE LLMs [Early Access Program (EAP)](https://go.atlassian.com/signup-forge-llms) before general availability.

---

### 2.3 Install dependencies

For a Node.js application, we have a new SDK to support this functionality.
Let's install the SDK for Forge LLMs:

Here we are using `yarn`, but you can also use `npm` if preferred.

Your `package.json` should include:

```
```
1
2
```



```
{
  "dependencies": {
    "@forge/llm": "^0.0.15"
  }
}
```
```

---

### 2.4 Implement the web trigger handler

The app structure should look like this:

```
```
1
2
```



```
.
├── AGENTS.md
├── manifest.yml
├── package.json
├── src
│  └── index.js
└── yarn.lock
└── node_modules
```
```

In `src/index.js`, implement the `runSync` function.
We also remove any boilerplate code from the Web trigger template.

**Key Steps:**

1. **Import the `@forge/llm`:** Load the `chat` function from `@forge/llm`.
2. **Parse Incoming Request:** Extract and parse the JSON body as the LLM prompt.
3. **Invoke LLM Chat:** Pass the prompt to the `chat` function to get a response.
4. **Return Success Response:** Format and return the LLM response with HTTP 200.
5. **Handle Errors:** Catch and format errors.

Example structure:

```
```
1
2
```



```
// 1. Install and import forge-llm-sdk
import { chat } from '@forge/llm'

exports.runSync = async (event, context) => {
  let finalResponse={};

  try {
    // 2. Parse the incoming JSON body as LLM prompt
    const llmPrompt = JSON.parse(event.body);

    // 3. Call the Forge LLMs SDK's chat function
    finalResponse = await chat(llmPrompt);

    // 4. Return the LLM response with status code 200
    console.log("#### LLM response:", JSON.stringify(finalResponse, null, 2 ));

    return buildOutput(
      JSON.stringify({
        success: true,
        choices: finalResponse.choices,
      }),
      200,
      "OK");

  } catch(err) {
    // 5. Handle errors
    console.error("Error during LLM chat:", err);
    return buildOutput({
        success: false,
        error: err?.message || err,
        errorDetails: err.context?.responseText
      },
      err.statusCode ?? 500,
      err.statusText ?? "Unknown Error"
    );
  }
};

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

**Chat function explanation:**
`chat` function simply takes a prompt object and returns a response object.
It supports various parameters to customize the LLM interaction, including tools and tool choice if needed.
The above example demonstrates a basic usage scenario.
Refer to the ['chat' Schema Reference](#2-7-schema-reference-for--chat-) for more details.

---

### 2.5 Deploy and install

Deploy your app:

```
```
1
2
```



```
forge deploy
# ✔ Deployed
```
```

**Tip:** If you encounter permission errors, ensure your Forge CLI is authenticated and your site allows app installations.

Install the app on your Atlassian site:

```
```
1
2
```



```
forge install
# ? Select an Atlassian app or platform tool: Jira
# ? Enter the site URL: <your-site-url>
# ? Do you want to continue? Yes
# ✔ Install in Jira complete!
```
```

---

### 2.6 Test the web trigger endpoint

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

Send a test prompt using `curl`:

First create a `request.json` file with the following content:

```
```
1
2
```



```
{
  "model": "claude-3-5-haiku-20241022",
  "messages": [
    {
      "role": "system",
      "content": "You are a meticulous problem-solver. Solve the following problem. Think step by step, showing each intermediate calculation and the rationale behind it. After reasoning, clearly state the final answer on a new line prefixed with 'Final answer:'."
    },
    {
      "role": "user",
      "content": "Problem: A shop sells pens at $2 each or 3 for $5. If I need 17 pens, what's the minimum cost? "
    }
  ]
}
```
```

Then execute the `curl` command:
We use `jq` to pretty-print the JSON response.

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
            "text": "Let's solve this step by step:\n\n1. Let's first look at the available pricing options:\n• Individual pen price: $2 per pen\n• Bulk pricing: 3 pens for $5\n\n2. To minimize cost, we want to use the bulk pricing as much as possible\n\n3. Calculate how many sets of 3 pens we can buy:\n• 17 ÷ 3 = 5 remainder 2\n• This means we can buy 5 sets of 3 pens (15 pens total)\n\n4. Calculate cost of bulk sets:\n• 5 sets × $5 per set = $25\n\n5. For the remaining 2 pens:\n• 2 pens at individual price of $2 each\n• 2 × $2 = $4\n\n6. Total minimum cost:\n• Bulk set cost + Individual pen cost\n• $25 + $4 = $29\n\nFinal answer: $29\n\nLet's verify:\n✓ 5 sets of 3 pens (15 pens): $25\n✓ 2 individual pens: $4\n✓ Total pens: 17\n✓ Total cost: $29"                                                                                                              
          }
        ]
      }
    }
  ]
}
```
```

---

### 2.7 Schema reference for 'chat'

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
      "finish_reason": "string",
      "message": {
        "role": "assistant",
        "content": "string | ContentPart[]"
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

You have now built a Forge app that leverages LLMs with dynamic Web triggers. By following this guide, you learned how to set up a Web trigger endpoint, send prompts to an LLM, and handle responses within the Forge platform. You are now ready to further customize your app, explore advanced LLM features, and integrate additional Forge modules to create more powerful and interactive solutions.

## Source code

Please find the complete code for this tutorial in the [llm-webtrigger-app Bitbucket repository](https://bitbucket.org/atlassian/forge-llm-examples/src/main/llm-webtrigger-app/)

## Next steps

* Try customizing your prompt schema to suit your use case.
* Discover advanced LLM features to add new capabilities to your app, [including support for "tools"](https://developer.atlassian.com/platform/forge/create-an-agentic-llm-webtrigger-app).
* Integrate with other Forge modules for more powerful workflows.

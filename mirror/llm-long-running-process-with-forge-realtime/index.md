# Handling long-running LLM processes with Forge Realtime

[Forge LLMs](/platform/forge/runtime-reference/forge-llms-api/) is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production — [sign up here](https://go.atlassian.com/signup-forge-llms) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

## Overview

When building Forge apps with large language models (LLMs), some prompts or agentic workflows may exceed the default [function timeout (55s)](/platform/forge/platform-quotas-and-limits/). To handle these, offload work to a queue consumer (up to 15 minutes) and stream results back to the user interface (UI) using [Realtime publish/subscribe](/platform/forge/realtime/). This pattern avoids storage-polling latency, reduces client/server round-trips, and keeps your macro responsive.

A queue consumer lets you run for longer (15 minutes) without blocking the initial invocation; Realtime keeps users informed the moment results (or errors) are available.

## Important security and technical requirements

**Important:** You **must** use tokens with unique custom claims to secure your Realtime channels. Both the subscriber (frontend) and publisher (consumer) must create tokens using the same unique signature (custom claims) that include identifying information (such as `channelName`, `accountId`, or other unique identifiers). This is essential to:

* Prevent unauthorized access to your channels
* Ensure channel isolation between different users and sessions
* Avoid cross-talk where one user receives another user's events

When using Realtime in async functions (such as queue consumers, triggers, or scheduled functions), you must use `subscribeGlobal()` and `publishGlobal()` because the context-based methods (`subscribe()` and `publish()`) are not supported in async execution contexts.

Read more about [securing Realtime channels with tokens](/platform/forge/runtime-reference/realtime-events-api/#using-the-token-argument-to-secure-channel-context).

---

## Prerequisites

Before you begin, you should be familiar with:

## Architecture

* **manifest.yml**: Declares modules for macro UI, resolver, queue consumer (extended timeout), LLM, and Realtime usage.
* **frontend/index.jsx**: Renders UI, subscribes to a Realtime channel, invokes the resolver, and displays results.
* **resolvers/index.js**: Pushes prompt payloads to the queue (fire-and-forget).
* **consumers/index.js**: Handles long-running LLM calls, then publishes results to the Realtime channel.

**Flow Sequence**

```
```
1
2
```



```
UI subscribes → resolver enqueues → consumer runs LLM → publishes → UI renders
```
```

The final project structure after completing the walkthrough:

```
```
1
2
```



```
  <project-directory>
  ├── manifest.yml
  ├── package-lock.json
  ├── package.json
  ├── README.md
  └── src
      ├── frontend
      │   └── index.jsx
      ├── consumers
      │   └── index.js
      ├── resolvers
      │   └── index.js
      ├── index.js
```
```

For the complete runnable example, see the [Source code](/platform/forge/llm-long-running-process-with-forge-realtime/#source-code) section below.

## Key implementation steps

### 1. Manifest configuration

Define modules in `manifest.yml` for the `llm`, queue `consumer` (extended timeout), `macro` UI, and `function` handlers (resolver and consumer).

```
```
1
2
```



```
modules:
  llm:
    - key: llm-with-realtime-app
      model: 
        - claude
  consumer:
    - key: llm-prompt-consumer
      queue: llm-prompt-consumer-queue
      function: consumer
  macro:
    - key: llm-with-forge-realtime-hello-world-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: llm-with-forge-realtime
  function:
    - key: resolver
      handler: index.resolverHandler
    - key: consumer
      handler: index.consumerHandler
      timeoutSeconds: 900 # 15 minutes (queue consumer max)
```
```

### 2. Dependencies

Ensure your `package.json` includes the necessary Forge SDK packages, for example:

```
```
1
2
```



```
{
  // ...
  "dependencies": {
    // ...
    "@forge/bridge": "5.8.0",
    "@forge/events": "^2.0.10",
    "@forge/llm": "^0.3.0",
    "@forge/realtime": "^0.3.0",
  }
}
```
```

### 3. Frontend: realtime subscription and prompt invocation

* Request a signed token from the resolver using custom claims (channel name, account ID).
* Subscribe to the channel using the token for secure communication, and achieving isolation.
* On submit, invoke the resolver to enqueue the prompt with the same custom claims.

```
```
1
2
```



```
//<project-directory>/src/frontend/index.jsx
import { invoke, realtime } from '@forge/bridge';

const CHANNEL_NAME = "my-llm-realtime-channel";

const [token, setToken] = useState(null);
const [customClaims, setCustomClaims] = useState({});
// ... other state variables like message, result, etc.

// Request token with custom claims
useEffect(() => {
  const fetchToken = async () => {
    const { token, customClaims } = await invoke('buildToken', { channelName: CHANNEL_NAME });
    setToken(token);
    setCustomClaims(customClaims);
  };
  fetchToken();
}, []);

// Subscribe with token
useEffect(() => {
  if (!token) return;
  let subscription;

  realtime.subscribeGlobal(
    CHANNEL_NAME,
    (payload) => setResult(payload),
    { token }
  ).then(sub => { subscription = sub; });

  return () => {
    if (subscription) subscription.unsubscribe();
  };
}, [token]);

const handleSubmit = () => {
  setResult(null);
  invoke("sendLLMPrompt", {
    customClaims,
    prompt: {
      model: 'claude-haiku-4-5-20251001',
      messages: [{ role: "user", content: message.trim() }]
    }
  });
};
```
```

### 4. Resolver: token signing and queue push

The resolver provides two functions:

* `buildToken`: **Critical security function** - Creates a signed token using custom claims (such as channel name and account ID) to secure Realtime communication and ensure channel isolation. This token must be created with the same custom claims that the consumer will use when publishing. See [Important security and technical requirements](#important-security-and-technical-requirements).
* `sendLLMPrompt`: Pushes the prompt payload to the queue for asynchronous processing.

```
```
1
2
```



```
//<project-directory>/src/resolvers/index.js
import Resolver from '@forge/resolver';
import { Queue } from '@forge/events';
import { signRealtimeToken } from '@forge/realtime';

const resolver = new Resolver();
const queue = new Queue({ key: "llm-prompt-consumer-queue" });

resolver.define('buildToken', async ({ payload, context }) => {
  const customClaims = {
    channelName: payload.channelName,
    accountId: context.accountId,
  };

  const { token } = await signRealtimeToken(payload.channelName, customClaims);
  return { token, customClaims };
});

resolver.define("sendLLMPrompt", async ({ payload }) => {
  await queue.push([{ body: payload }]);
});

export const handler = resolver.getDefinitions();
```
```

### 5. Consumer: LLM call and publish result

Handle the long-running process for the LLM app. The consumer must sign a token using the same custom claims as the subscriber, then publish the result to the Realtime channel.

```
```
1
2
```



```
//<project-directory>/src/consumers/index.js
import { publishGlobal, signRealtimeToken } from '@forge/realtime';
import { chat } from '@forge/llm';

export const handler = async (event) => {
  const { customClaims, prompt } = event.body;
  const channelName = customClaims.channelName;
  let result;
  
  try {
    const chatResult = await chat(prompt);
    result = { status: "done", ...chatResult };
  } catch (err) {
    result = {
      status: "error",
      error: err?.context?.responseText || "Unknown error occurred"
    };
  }

  // Sign token with same custom claims as subscriber
  const { token } = await signRealtimeToken(channelName, customClaims);

  await publishGlobal(
    channelName,
    result,
    { token }
  );
};
```
```

### 6. Export consumer and resolver handlers

Ensure you export the handlers for both the consumer and resolver functions.

```
```
1
2
```



```
// <project-directory>/index.js
import { handler as consumerHandler } from './consumers/index.js';
import { handler as resolverHandler } from './resolvers/index.js';
```
```

### Deploy and install

After completing the steps, deploy and then install the app into your site or environment.

```
```
1
2
```



```
forge deploy
forge install
```
```

When successful, your app will now handle long-running LLM prompts via the queue consumer and stream results back to the UI using Realtime.

## Source code

Find the complete code for this tutorial in the [llm-with-forge-realtime Bitbucket repository](https://bitbucket.org/atlassian/forge-llm-examples/src/main/llm-with-forge-realtime/)

## Why Use Realtime Over Polling?

* **Lower latency:** Results are pushed instantly when ready.
* **Simpler code:** No need to coordinate storage reads/writes or handle polling intervals.
* **Resource efficient:** No periodic client calls or extra backend invocations.

## Performance and scalability

* Optimize prompts for speed and cost.
* Choose models wisely (larger models = higher latency).
* Set UI timeouts and allow retries.
* Consider publishing partial progress for very long-running chains.

## Security and compliance

**Required security measures:**

* **Always use tokens:** Token-based security is mandatory for Realtime channels to prevent unauthorized access and ensure proper isolation.
* **Use unique custom claims:** Include identifiers like `accountId` or session-specific data in your custom claims.
* **Sign tokens on both sides:** Both the subscriber (frontend) and publisher (backend) must create tokens using the same custom claims.
* **Validate channel access:** Never rely on channel naming alone for security.

See [Important security and technical requirements](#important-security-and-technical-requirements) for implementation details.

## Troubleshooting

* **No events received:** Ensure channel names match exactly (case-sensitive) and that both subscriber and publisher use the same custom claims when signing tokens.
* **Context error in async functions:** If you see errors about missing context in queue consumers, triggers, or scheduled functions, ensure you're using `subscribeGlobal()` and `publishGlobal()` instead of `subscribe()` and `publish()`.
* **Debugging:** Use [Forge tunnel](/platform/forge/cli-reference/tunnel/) for logs.

## Conclusion

With an async function, a queue consumer, and Forge Realtime, your Forge LLMs app can run long-running prompts asynchronously and stream results to the UI, keeping it responsive and eliminating polling.

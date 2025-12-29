# Handling long-running LLM processes with Forge Realtime

[Forge LLMs](/platform/forge/runtime-reference/forge-llms-api/) is available through Forge's Early Access Program (EAP). EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production — [sign up here](https://go.atlassian.com/signup-forge-llms) to participate.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

## Overview

When building Forge apps with large language models (LLMs), some prompts or agentic workflows may exceed the default [function timeout (55s)](/platform/forge/platform-quotas-and-limits/). To handle these, offload work to a queue consumer (up to 15 minutes) and stream results back to the user interface (UI) using [Realtime publish/subscribe](/platform/forge/realtime/). This pattern avoids storage-polling latency, reduces client/server round-trips, and keeps your macro responsive.

A queue consumer lets you run for longer (15 minutes) without blocking the initial invocation; Realtime keeps users informed the moment results (or errors) are available.

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
    "@forge/llm": "^0.1.0",
    "@forge/realtime": "^0.3.0",
  }
}
```
```

### 3. Frontend: realtime subscription and prompt invocation

* Subscribe to a channel such as `my-llm-realtime-channel` and supply `contextOverrides` that match the product context, for example `Confluence`.
* On submit, invoke the resolver to enqueue the prompt.
* Use a unique channel name per session if you need isolation (see note below).

```
```
1
2
```



```
//<project-directory>/src/frontend/index.jsx
import { invoke, realtime } from '@forge/bridge';

const CHANNEL_NAME = "my-llm-realtime-channel"; // Consider scoping per user/session to avoid cross-talk.

const [message, setMessage] = useState("");
const [result, setResult] = useState(null);

useEffect(() => {
  const handleRealtimeEvent = (payload) => {
    setResult(payload);
  };

  let subscription;

  realtime.subscribe(
    CHANNEL_NAME,
    handleRealtimeEvent,
    // Important: match contextOverrides with publisher in consumer
    { contextOverrides: [Confluence] }
  ).then(sub => { subscription = sub; });

  return () => { if (subscription) subscription.unsubscribe(); };
}, []);

const handleSubmit = async () => {
  setResult(null);
  invoke("sendLLMPrompt", {
    promptConsumerPayload: {
      channelName: CHANNEL_NAME,
      model: 'claude-haiku-4-5-20251001',
      messages: [
        { role: "user", content: message.trim() }
      ]
    }
  }).then(() => { console.log("Prompt enqueued");});

  return (
    <>
      <Box>
        <TextArea value={message} onChange={(e) => setMessage(e.target.value)}/>
        <Button appearance="primary" onClick={handleSubmit} isDisabled={!message.trim()}>Submit</Button>
      </Box>
      <Box>
        <Text>Result: {result}</Text>
      </Box>
    </>
  );
};
```
```

Ensure the `contextOverrides` array is identical in both the Realtime subscription (frontend) and the consumer publish call; any mismatch blocks delivery (for example `[Confluence]` for Confluence, `[Jira]` for Jira). See the [Realtime documentation](/platform/forge/runtime-reference/realtime-events-api/#choosing-between-publish-and-publishglobal) for details.

### 4. Resolver: queue push

Push the prompt payload to the queue for asynchronous processing.

```
```
1
2
```



```
//<project-directory>/src/resolver/index.js
import { resolver, queue } from '@forge/queue';
const resolver = new Resolver();

resolver.define("sendLLMPrompt", async ({ payload }) => {
  await queue.push([{ body: payload.promptConsumerPayload }]);
});

export const handler = resolver.getDefinitions();
```
```

### 5. Consumer: LLM call and publish result

Handle the long-running process for the LLM app, and publish the result to the Realtime channel.

```
```
1
2
```



```
//<project-directory>/src/consumers/index.js
import { publish, Confluence } from '@forge/realtime';
import { chat } from '@forge/llm';

export const handler = async (event) => {
  const { body } = event;
  let result;
  
  try {
    const chatResult = await chat.completions.create({
      model: body.model,
      messages: body.messages
    });
    
    result = { status: "done", ...chatResult};
  } catch (err) {
    result = {
      status: "error",
      error: err?.context?.responseText || "Unknown error occurred"
    };
  }

  // Important: use same channel name and contextOverrides as frontend subscription
  await publish(
    body.channelName,
    result,
    {
      contextOverrides: [Confluence]
    }
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

## Channel naming and isolation

If multiple users might interact simultaneously, incorporate a unique suffix (for example, user account ID, issue ID) into the channel name to avoid unrelated events appearing in another user's UI.

You can also consider using token-based security for channels; see [Secure Realtime channels](/platform/forge/runtime-reference/realtime-events-api/#using-the-token-argument-to-secure-channel-context).

## Performance and scalability

* Optimize prompts for speed and cost.
* Choose models wisely (larger models = higher latency).
* Set UI timeouts and allow retries.
* Consider publishing partial progress for very long-running chains.

## Security and compliance

## Troubleshooting

* **No events received:** Ensure `contextOverrides` match on both publish and subscribe.
* **Wrong channel name:** Channel names must match exactly (case-sensitive).
* **Debugging:** Use [Forge tunnel](/platform/forge/cli-reference/tunnel/) for logs.

## Conclusion

With an async function, a queue consumer, and Forge Realtime, your Forge LLMs app can run long-running prompts asynchronously and stream results to the UI, keeping it responsive and eliminating polling.

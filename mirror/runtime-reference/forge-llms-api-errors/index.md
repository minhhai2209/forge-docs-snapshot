# Handling LLM API streaming errors

Streaming responses from LLMs increase the risk of delivering incomplete output to the user, particularly in cases of interruptions such as timeouts or network failures.

Instead of resubmitting the original prompt, a better way to recover is to prompt the LLM with prior context. For example, if chunked text responses have been accumulated into a variable `storedOutput`, you can use the following user prompt to recover:

```
1
2
3
`You were interrupted in your previous attempt.
Your original instruction was "${originalUserPrompt}".
Continue from the following interrupted output: ${storedOutput}`
```

We've observed that Claude Sonnet 4.5 typically responds in one of two ways:

* It successfully resumes text generation by continuing from the previously interrupted output.
* It explains that the previous output already fulfilled the original instruction, and why.

## Detecting when to retry

Platform interruptions can cause streaming to conclude before a complete response is delivered. In other words, not only can the LLM's text output cut off prematurely, but the client can also fail to receive finalising streaming messages. One way to detect incomplete responses, and therefore attempt a retry, is to check whether a completion choice object with a `finish_reason` property is missing when the stream ends:

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
let isStreamComplete = false;
let response;
const checkIfFinishReasonExists = (chunk) =>
  !!chunk.choices.find(({ finish_reason }) => finish_reason !== undefined);

try {
  response = await stream(myPrompt);

  for await (const chunk of response) {
    if (checkIfFinishReasonExists(chunk)) {
      isStreamComplete = true;
    }
  }
} catch (e) {
  // Exceptions are not thrown for finishing streams with incomplete responses.
} finally {
  response?.close();
}

console.log(`Is the stream complete? ${isStreamComplete}`);
```

# Scheduled triggers

Scheduled trigger events are `HTTPS GET` requests made by the Forge platform to an app function on a periodic basis that you specify.

Like web trigger functions, scheduled trigger functions are invoked by the Atlassian platform with two parameters, a request object and a context object.
However, the request object for a scheduled trigger function contains fewer properties than for a web trigger function.

When you handle a scheduled trigger, your function must return a response in the format expected by the platform, as described below.
If the response from your app does not follow that structure, the platform records an error with a status code of `424 Failed dependency`.

Read the [scheduled trigger module](/platform/forge/manifest-reference/modules/scheduled-trigger) to learn how to configure them in the manifest.

Invocations from users, webtriggers, or scheduled triggers are subject to Forge's [invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Basic usage

### Handler

Your handler should be defined as a [function](/platform/forge/runtime-reference/).

```
1
2
3
4
export const trigger = ({ context }) => {
  console.log(context);
  // Do something
}
```

### Manifest definition

A [scheduled trigger module](/platform/forge/manifest-reference/modules/scheduled-trigger/) should be declared in the [app manifest](/platform/forge/manifest-reference/).

```
1
2
3
4
5
6
7
8
modules:
  scheduledTrigger:
    - key: example
      function: my-function
      interval: hour # Runs hourly
  function:
    - key: my-function
      handler: index.trigger
```

## Parameters

### Request

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `context` | `object` | Yes | Properties identifying this scheduled trigger to Atlassian. |
| `context.cloudId` | `string` | Yes | The cloud ID. |
| `context.moduleKey` | `string` | Yes | The key identifying the module in the manifest that defines the scheduled trigger function and its frequency. |
| `contextToken` | `string` | Yes | An encoded token used by Atlassian to identify the scheduled trigger invocation. This value has no meaning to an app. |

#### Example

Your function receives a request object with the following structure:

```
```
1
2
```



```
{
  context: {
    cloudId: '4f6d9508-93c9-4c2e-abd7-916c34920012',
    moduleKey: 'my -scheduled-trigger-example'
  },
  contextToken: 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImZvcmdlL2NvbnRleHQtdG9rZW4vMTcyYWE2NDItNDY1OS00OWRlLTk0YTYtYjVhYTZjODdlYTliIn0.eyJjb250ZXh0Ijp7ImNsb3VkSWQiOiI0ZjJkMjUwOC05YWM5LTRiZGUtYWQ5Ny0uCCy7qpzzMjkwOTAiLCJtb2R1bGVLZXkiOiJoZWxlbi1zY2hlZHVsZWQtdHJpZ2dlci10cmlnZ2VyLWV4YW1wbGUifSwiYWNjb3VudElkIjoiNzEyMDIwOjQzYmVmMjU2LWQyMGUtNGU5YS1iMTI3LTE1OTM1YjUzZmU3MCIsImV4dGVuc2lvbklkIjoiYXJpOmNsb3VkOmVjb3N5c3RlbTo6ZXh0ZW5zaW9uLzA3ZDg4NWNlLWVkYjItNGQxMC04M2MzLTc5Y2NkODU3OTcyMy81OTcyMmM1OS05ZjY4LTRlMzItYTNkMi1mNDhjOWU4OWM4MDgvc3RhdGljL2hlbGVuLXNjaGVkdWxlZC10cmlnZ2VyLXRyaWdnZXItZXhhbXBsZSIsImNvbnRleHRJZHMiOlsiYXJpOmNsb3VkOmppcmE6OnNpdGUvNGYyZDI1MDgtOWFjOS00YmRlLWFkOTctOTE2YzM3MzI5MDkwIl0sImFwcElkIjoiMDdkODg1Y2UtZWRiMi00ZDEwLTgzYzMtNzljY2Q4NTc5NzIzIiwiYXBwVmVyc2lvbiI6IjIuMTIuMCIsImV4dGVuc2lvblR5cGUiOiJjb3JlOnNjaGVkdWxlZFRyaWdnZXIiLCJ1bmxpY2Vuc2VkIjpmYWxzZSwiaXNzIjoiZm9yZ2UvY29udGV4dC10b2tlbiIsImF1ZCI6ImZvcmdlIiwiaWF0IjoxNzA2MjU1MTgwLCJuYmYiOjE3MDYyNTUxODAsImV4cCI6MTcwNjI1NjA4MCwianRpIjoiYmQ0ZGMxNWY0ODhjYTdhOTRlOGY5NzBkNDZlNWZmNTg4OWRiNTM4YSJ9.Jaf5XHhzKseGx2qxNrAYRK1hKRdrXxMvdIbfmIGFqNh_P9MWVECyB59_1gPxbLhu_WbIwEM-sQxKtWlLLkMrgXNPbX2hraO6w7p6yOaLgitaPizSbAt6JCLYN5ulEpRMRjMAkG4xT-fKYuARBc_bd7WlP4Z8SZrqiZwkModWtHVsXD6OnsYpITJwP9nNoUIG_6WaBZelkyoCpomjj3zXRy5_b5MNI61rJrRGt_R3EZ9h2Xb5OwZ9OUve2SeelrcBBxJblg3tBQ9IFS_828Az6CELbCbf5h7Wz8aXvd3Q_Mrh3GpDHk4sP6bUsjkfhmtT9d292aEehl4BCZHFVQZieQ'
}
```
```

### Context

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `principal` | `Object` | Yes | The identity of the user invoking the function. Since no user is involved, this value is undefined. |
| `installContext` | `string` | Yes | The Atlassian Resource Identifier (ARI) identifying the cloud or Atlassian app context of the app installation. |

#### Example

Your function receives a request object with the following structure:

```
```
1
2
```



```
{
  principal: undefined,
  installContext: 'ari:cloud:jira::site/4f275028-9ac9-4a4e-ad97-91667d422097'
}
```
```

## Response

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `body` | `string` |  | HTTP response body sent back to the caller. |
| `headers` | `object` |  | HTTP headers sent by the caller.  **Format**`nameOfTheHeader: array of strings`  **Example**`"Content-Type: ["application/json"]` |
| `statusCode` | `integer` | Yes | HTTP status code returned to the caller. The platform recognizes a status code of `204` as success, and status codes in the 500 series as errors. |
| `statusText` | `string` |  | Text returned to communicate status. The text provides context to the status code. |

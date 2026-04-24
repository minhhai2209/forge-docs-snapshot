# Pre-uninstall trigger

The `preUninstall` module registers a function that runs when your app is uninstalled from an Atlassian app, giving it the opportunity to perform cleanup operations.

Pre-uninstall invocations are non-blocking. If the invocation fails, the uninstallation process will still continue.

Pre-uninstall functions run without a user context, which means the `principal` field of the
`context` argument doesn't represent a user. If a function invoked from a pre-uninstall function
returns a value, it is ignored. If the function throws an error, nothing will happen,
and the uninstallation process will continue.

The invocation will have a timeout of 55 seconds.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `endpoint` | `string` | Yes (if no `function` is specified). | A reference to the `endpoint` [specifying the remote back end](/platform/forge/manifest-reference/endpoint/) that resolves your event (if you are using [Forge Remote)](/platform/forge/forge-remote-overview). |

## Function arguments

When your trigger function is invoked, it receives two arguments:

```
1
2
3
export async function myTriggerFunction(payload, context) {
  // handle the payload
}
```

### Arguments

* **payload:** A payload detailing the invocation request.
* **context:** Additional information about the context the function invocation occurred in. Refer to [Context Schema](/platform/forge/function-reference/arguments/#context-schema) for complete details.

#### Payload

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `context` | `object` | Yes | Properties identifying this function to Atlassian. |
| `context.cloudId` | `string` | Yes | The cloud ID. |
| `context.moduleKey` | `string` | Yes | The key identifying the `preUninstall` module in the manifest. |
| `contextToken` | `string` | Yes | An encoded token used by Atlassian to identify the pre-uninstall trigger invocation. This value has no meaning to an app. |

#### Example

Your function receives a request object with the following structure:

```
```
1
2
```



```
{
  "context": {
    "cloudId": "4f6d9508-93c9-4c2e-abd7-916c34920012",
    "moduleKey": "example-pre-uninstall"
  },
  "contextToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImZvcmdlL2NvbnRleHQtdG9rZW4vMTcyYWE2NDItNDY1OS00OWRlLTk0YTYtYjVhYTZjODdlYTliIn0.eyJjb250ZXh0Ijp7ImNsb3VkSWQiOiI0ZjJkMjUwOC05YWM5LTRiZGUtYWQ5Ny0uCCy7qpzzMjkwOTAiLCJtb2R1bGVLZXkiOiJoZWxlbi1zY2hlZHVsZWQtdHJpZ2dlci10cmlnZ2VyLWV4YW1wbGUifSwiYWNjb3VudElkIjoiNzEyMDIwOjQzYmVmMjU2LWQyMGUtNGU5YS1iMTI3LTE1OTM1YjUzZmU3MCIsImV4dGVuc2lvbklkIjoiYXJpOmNsb3VkOmVjb3N5c3RlbTo6ZXh0ZW5zaW9uLzA3ZDg4NWNlLWVkYjItNGQxMC04M2MzLTc5Y2NkODU3OTcyMy81OTcyMmM1OS05ZjY4LTRlMzItYTNkMi1mNDhjOWU4OWM4MDgvc3RhdGljL2hlbGVuLXNjaGVkdWxlZC10cmlnZ2VyLXRyaWdnZXItZXhhbXBsZSIsImNvbnRleHRJZHMiOlsiYXJpOmNsb3VkOmppcmE6OnNpdGUvNGYyZDI1MDgtOWFjOS00YmRlLWFkOTctOTE2YzM3MzI5MDkwIl0sImFwcElkIjoiMDdkODg1Y2UtZWRiMi00ZDEwLTgzYzMtNzljY2Q4NTc5NzIzIiwiYXBwVmVyc2lvbiI6IjIuMTIuMCIsImV4dGVuc2lvblR5cGUiOiJjb3JlOnNjaGVkdWxlZFRyaWdnZXIiLCJ1bmxpY2Vuc2VkIjpmYWxzZSwiaXNzIjoiZm9yZ2UvY29udGV4dC10b2tlbiIsImF1ZCI6ImZvcmdlIiwiaWF0IjoxNzA2MjU1MTgwLCJuYmYiOjE3MDYyNTUxODAsImV4cCI6MTcwNjI1NjA4MCwianRpIjoiYmQ0ZGMxNWY0ODhjYTdhOTRlOGY5NzBkNDZlNWZmNTg4OWRiNTM4YSJ9.Jaf5XHhzKseGx2qxNrAYRK1hKRdrXxMvdIbfmIGFqNh_P9MWVECyB59_1gPxbLhu_WbIwEM-sQxKtWlLLkMrgXNPbX2hraO6w7p6yOaLgitaPizSbAt6JCLYN5ulEpRMRjMAkG4xT-fKYuARBc_bd7WlP4Z8SZrqiZwkModWtHVsXD6OnsYpITJwP9nNoUIG_6WaBZelkyoCpomjj3zXRy5_b5MNI61rJrRGt_R3EZ9h2Xb5OwZ9OUve2SeelrcBBxJblg3tBQ9IFS_828Az6CELbCbf5h7Wz8aXvd3Q_Mrh3GpDHk4sP6bUsjkfhmtT9d292aEehl4BCZHFVQZieQ"
}
```
```

#### Context object properties

The `context` object contains information about the environment and installation where the trigger was invoked:

| Property | Type | Description |
| --- | --- | --- |
| `principal` | `Principal | undefined` | The principal containing the Atlassian ID of the user that interacted with the component. |
| `installContext` | `string` | The ARI identifying the cloud or Atlassian app context of this component installation. |
| `workspaceId` | `string | undefined` | The ID of the workspace on which the extension is working. |
| `license` | `License | undefined` | Contains information about the license of the app. This field is only present for paid apps in the production environment.  `license` is `undefined` for free apps, apps in `DEVELOPMENT` and `STAGING` environments, and apps that are not listed on the Atlassian Marketplace. |
| `installation` | `Installation | undefined` | A summary of the app installation, including the installation ARI and the contexts where the app is installed. |

### Example

```
```
1
2
```



```
modules:
  preUninstall:
    - key: example-pre-uninstall
      function: my-pre-uninstall-function
  function:
    - key: my-pre-uninstall-function
      handler: index.trigger
```
```

Handler function in `index.js`

```
```
1
2
```



```
// index.js

export const trigger = (payload, context) => {
  console.log("Pre-uninstall invoked");
  console.log(payload);
};
```
```

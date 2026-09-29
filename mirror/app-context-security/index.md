# App context security

## UI Kit and Custom UI

For UI Kit, contextual information is available through the use of [Hooks](/platform/forge/ui-kit/hooks/hooks-reference/),
methods from the [Bridge](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) package,
and [Invoke](/platform/forge/apis-reference/ui-api-bridge/invoke/) method.
The same methods, Bridge and Invoke, are also applicable for accessing contextual information in Custom UI.

### Custom UI resolver

Context parameters in each resolver function are guaranteed to be secure, unalterable, and valid to be used for authorization.

### Custom UI bridge

You should not use the contextual information from the `getContext` API for authorization, as it is
able to be modified in the browser and is not guaranteed to be secure, unalterable, and valid to be used
for authorization.

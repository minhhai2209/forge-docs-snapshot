# App context security

When using Forge, your app may have access to contextual information that originates from various
sources. Since data originating from or passing through the browser can be altered or tampered with,
it's important to understand which parts of this contextual information are guaranteed to be
secure, unalterable, and thus valid to be used for authorization purposes.

When you use contextual information that is *not* guaranteed to be secure and unalterable, it is your
[responsibility](/platform/forge/shared-responsibility-model) to ensure that usage of this contextual
information does *not* allow a customer to have any sort of unauthorized access.
You may use the secure parts of the contextual information to determine and authorize access.
For example, you can use the `accountId` in the Custom UI resolver context payload to check a
user's access to some content.

## UI Kit and Custom UI

For UI Kit, the contextual information is available through the use of [Hooks](/platform/forge/ui-kit/hooks/hooks-reference/), methods from the [Bridge](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) package, and [Invoke](/platform/forge/apis-reference/ui-api-bridge/invoke/) method. The same methods, Bridge and Invoke, are also applicable for accessing contextual information in Custom UI.

### Custom UI resolver

Only `license`, `accountId`, `accountType`, and `installContext` from the context parameter in each resolver function are
guaranteed to be secure, unalterable, and valid to be used for authorization.

### Custom UI bridge

You should not use the contextual information from the `getContext` API for authorization, as it is
able to be modified in the browser and is not guaranteed to be secure, unalterable, and valid to be used
for authorization.

# Client SDK vs server-side SDK

Forge provides two SDKs for evaluating feature flags. This page explains the difference and helps you decide which to use.

## The short answer

|  | Client SDK (`@forge/bridge`) | Server-side SDK (`@forge/feature-flags`) |
| --- | --- | --- |
| **Where it runs** | Browser (Forge UI frontend) | Forge functions (resolvers, triggers) |
| **Initialization** | `new FeatureFlags()` from `@forge/bridge` | `new FeatureFlags()` from `@forge/feature-flags` |
| **User object** | Passed to `initialize(user, config)` | Passed to `checkFlag(user, flagId)` |
| **Config refresh** | On initialization | Polls every 60 seconds |
| **Use case** | Frontend feature gating without a resolver | Backend feature gating in resolvers and triggers |

## Why there are two SDKs

Forge apps have two distinct execution environments: the frontend (a browser-based UI) and the backend (Forge functions). These environments have different characteristics, so the SDKs are designed differently.

The server-side SDK runs in Forge functions. It initializes once per function invocation, downloads flag configuration, and then evaluates flags synchronously. It's designed for a multi-user context — you pass the user object to `checkFlag` each time, because different invocations may have different users.

The client SDK runs in the browser. It initializes once per app session, downloads flag configuration, and then evaluates flags synchronously. The user is set once at initialization time (it's always the current logged-in user).

## When to use the client SDK

Use the client SDK when:

* You want to gate UI elements (show/hide buttons, panels, sections) based on a flag
* You want to avoid the latency of a resolver round-trip just to evaluate a flag
* Your flag logic doesn't need server-side data to make the evaluation decision

```
```
1
2
```



```
// Client SDK: no resolver needed
import { view, FeatureFlags } from "@forge/bridge";

const featureFlags = new FeatureFlags();
const { accountId, cloudId, environmentType } = await view.getContext();

await featureFlags.initialize(
  { identifiers: { accountId }, attributes: { installContext: `ari:cloud:confluence::site/${cloudId}` } },
  { environment: environmentType.toLowerCase() }
);

const showNewUI = featureFlags.checkFlag("new-dashboard-ui", false);
```
```

## When to use the server-side SDK

Use the server-side SDK when:

* Your feature flag evaluation happens in a resolver, trigger, or scheduled job
* You need to combine the flag result with backend data (for example: only show the feature if the flag is enabled AND a database record exists)
* You're gating backend operations, not UI rendering

```
```
1
2
```



```
// Server-side SDK: in a resolver
import { FeatureFlags } from "@forge/feature-flags";

const featureFlags = new FeatureFlags();
await featureFlags.initialize({ environment: environmentType?.toLowerCase() || "development" });

const user = { identifiers: { accountId: context?.principal?.accountId } };
const isEnabled = featureFlags.checkFlag(user, "new-backend-logic", false);
```
```

## Can I use both?

Yes. A common pattern is to use the client SDK to gate the UI and the server-side SDK to gate the backend operation that the UI triggers. Both SDKs read from the same flag configuration, so if the flag is enabled, it's enabled in both.

In practice, you often only need one. If you're gating a UI element and the backend doesn't care about the flag state, use the client SDK. If you're gating backend behaviour and the UI reflects that, use the server-side SDK in your resolver and pass the result to the frontend via the resolver response.

## Architectural tradeoff

The client SDK evaluates flags in the browser, avoiding a resolver round-trip. Flag names and configuration are not exposed to end users — the SDK communicates with Atlassian's infrastructure internally and does not make flag details visible in browser dev tools.

The server-side SDK evaluates flags on Atlassian's infrastructure inside your resolver. Use it when you need flag evaluation tied to backend logic or when you're already making a resolver call for other reasons.

## Further reading

# Forge changelog

### What is changing?

We are removing support for anonymous (unauthenticated) users from the Forge Feature Flags Client SDK (`FeatureFlags` in `@forge/bridge`). Starting **December 1, 2026**, the Client SDK will no longer evaluate feature flags when no authenticated user is present.

Currently, the Client SDK can be initialized even without a logged-in user (i.e., when no `accountId` is available). After this change, `FeatureFlags.initialize()` will only function for authenticated users with a valid Atlassian account. If your app calls `initialize()` without an `accountId` in the user's `identifiers`, the SDK will not return evaluated flag values and will fallback to default values.

### Who is affected?

You are affected if your Forge app meets **both** of these conditions:

1. Uses the Feature Flags Client SDK (`FeatureFlags` from `@forge/bridge`)
2. Allows anonymous access (e.g., your app module has `unlicensedAccess` enabled and you serve users who are not logged in)

**If your app only serves logged-in users, no action is needed.**

### What should you do?

**Option A — Use a default value for anonymous users**

Before calling `initialize()`, check whether an `accountId` is available. If not, skip initialization and use a hardcoded default for your feature flag logic:

`1const { accountId } = await view.getContext();
2if (accountId) {
3 const featureFlags = new FeatureFlags();
4 await featureFlags.initialize(user, config);
5 const enabled = featureFlags.checkFlag("my-flag", false);
6} else {
7 // Anonymous user — use default behaviour
8 const enabled = false;
9}`

**Option B — Move flag logic to the server-side SDK**

If you need to control behaviour for anonymous users, use the <https://developer.atlassian.com/platform/forge/feature-flags/feature-flags-sdk/> in a resolver. The server SDK supports targeting by `installContext` (site-level), which does not require a user identity.

### Timeline

|  |  |
| --- | --- |
| Deprecation notice issued | Sep 2, 2026 |
| End of support (breaking change) | Dec 1, 2026 |

The deprecation period is **90 days**. During this time, the existing behaviour will continue to work, but you will see deprecation warnings in the developer console.

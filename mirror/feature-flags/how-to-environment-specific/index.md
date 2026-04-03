# Use environment-specific flags

Feature flags in Forge are configured independently per environment. A flag set to 100% in development has no effect on staging or production. This guide shows how to use that to safely test and promote flag changes across environments.

## How environment separation works

When you create a flag in Developer Console, it appears in three environments: **DEV**, **STAGING**, and **PROD**. Each has its own rollout configuration. You activate the flag in each environment separately.

In your code, the SDK environment is set from the Forge context:

```
1
2
3
4
const featureFlags = new FeatureFlags();
await featureFlags.initialize({
  environment: context?.environmentType?.toLowerCase() || "development"
});
```

`environmentType` is automatically provided by Forge and reflects where the app is running (`development`, `staging`, or `production`). You don't need to hardcode or configure this.

## Step 1: Deploy code with the flag check

Write your flag check using the context-based environment. Don't hardcode an environment string:

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
import { FeatureFlags } from "@forge/feature-flags";

resolver.define('getFeature', async ({ context }) => {
  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: context?.environmentType?.toLowerCase() || "development"
  });

  const user = {
    identifiers: {
      installContext: context?.installContext,
    }
  };

  const isEnabled = featureFlags.checkFlag(user, "new-feature", false);
  featureFlags.shutdown();
  return isEnabled;
});
```

Deploy to all environments:

```
```
1
2
```



```
forge deploy
forge deploy --environment staging
forge deploy --environment production
```
```

The flag defaults to `false` in all environments until you activate it.

## Step 2: Enable the flag in development first

In Developer Console:

1. Go to your app → **Manage** → **Feature flags** → select your flag
2. On the Setup page, check **DEV** only
3. Set **Pass** to `100%`, **Fail** to `0%`
4. Click **Save**

Your app in development now evaluates the flag as enabled. Staging and production are unaffected.

## Step 3: Test in staging

When you're satisfied with your development testing:

1. Check **STAGING** on the flag Setup page
2. Optionally set a lower percentage (e.g., `25%`) to test gradually
3. Click **Save**

Staging now evaluates the flag according to your staging configuration. Development and production remain unchanged.

When ready for production:

1. Check **PROD** on the flag Setup page
2. Start with a low percentage (e.g., `10%`) if you want a gradual rollout
3. Click **Save**

## Step 5: Disable in an environment quickly

If something goes wrong in production, set **Pass** to `0%` (or uncheck **PROD**) and save. The change propagates within 60 seconds for the server-side SDK.

## Use flags for debug-only behaviour

A common pattern is enabling debug logging or diagnostic output only in development:

```
```
1
2
```



```
const isDebugMode = featureFlags.checkFlag(user, "debug-mode", false);
if (isDebugMode) {
  console.log("Debug info:", { context, user });
}
```
```

Create this flag and only enable it in the **DEV** environment. It will never fire in staging or production, even if the code is deployed everywhere.

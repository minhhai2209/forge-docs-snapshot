# Roll out to a percentage of users

This guide shows you how to release a feature gradually — for example to 10% of sites first, then 50%, then 100% — using feature flags.

## Prerequisites

## Step 1: Choose your targeting unit

Before writing any code, decide what you're rolling out to: sites or users.

| Goal | ID type to use |
| --- | --- |
| Roll out to X% of Atlassian **sites** | `installContext` |
| Roll out to X% of **users** within each site | `accountId` |

Rolling out by site is simpler — all users in a site get the same experience. Rolling out by user allows finer control but means different users in the same site may see different behaviour.

## Step 2: Create the flag with the right ID type

When creating the flag in Developer Console:

1. Go to your app → **Manage** → **Feature flags** → **Create flag**
2. Set the **ID type** to match your choice:
   * `installContext` for site-level rollouts
   * `accountId` for user-level rollouts
3. Note the auto-generated **Flag ID** — you'll use this in code

## Step 3: Add the flag check to your resolver

### Rolling out by site (installContext)

```
```
1
2
```



```
import { FeatureFlags } from "@forge/feature-flags";

resolver.define('getFeature', async ({ context }) => {
  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: context?.environmentType?.toLowerCase() || "development"
  });

  const user = {
    identifiers: {
      installContext: context?.installContext,
    },
    attributes: {
      installContext: context?.installContext,
    }
  };

  const isEnabled = featureFlags.checkFlag(user, "my-feature-flag", false);
  featureFlags.shutdown();
  return isEnabled;
});
```
```

### Rolling out by user (accountId)

```
```
1
2
```



```
import { FeatureFlags } from "@forge/feature-flags";

resolver.define('getFeature', async ({ context }) => {
  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: context?.environmentType?.toLowerCase() || "development"
  });

  const user = {
    identifiers: {
      accountId: context?.principal?.accountId,
    },
    attributes: {
      accountId: context?.principal?.accountId,
    }
  };

  const isEnabled = featureFlags.checkFlag(user, "my-feature-flag", false);
  featureFlags.shutdown();
  return isEnabled;
});
```
```

## Step 4: Configure the rollout percentage in Developer Console

1. Go to your flag in Developer Console → **Setup**
2. Set **Pass** to your initial rollout percentage (for example, `10`)
3. Set **Fail** to the remainder (`90`)
4. Check the environments you want to activate this for
5. Click **Save**

The SDK randomly assigns each `installContext` or `accountId` to pass or fail based on these percentages. The assignment is consistent — the same site or user always gets the same result for a given percentage configuration.

## Step 5: Increase the rollout over time

To widen the rollout, update the percentage in Developer Console:

1. Go to your flag → **Setup**
2. Increase **Pass** (for example, from `10` to `50`)
3. Click **Save**

The change takes effect within 60 seconds for existing instances of the server-side SDK (its polling interval). The client SDK picks up the new configuration on next initialization.

Percentage updates are manual — there's no automated time-based progression. See [Limitations](/platform/forge/feature-flags/limitations) for details.

## Step 6: Complete the rollout

Once you're confident in the feature, set **Pass** to `100%` and **Fail** to `0%`. At this point, the flag is effectively permanent — you can clean it up:

1. Remove the `checkFlag` call from your code
2. Delete the flag from Developer Console
3. Deploy your updated code

# Feature flags server-side SDK

API reference for the `@forge/feature-flags` package.

The server-side SDK evaluates feature flags in Forge functions (resolvers, triggers, and other backend code). Evaluations are performed locally against a cached configuration — no network request per evaluation.

## Installation

```
1
npm install @forge/feature-flags@latest
```

Requires Forge CLI version 2.0.0 or later.

## `FeatureFlags`

### Constructor

Creates a new instance of the SDK client.

### `initialize(config)`

```
1
initialize(config: FeatureFlagConfig): Promise<void>
```

Downloads the latest flag configuration and prepares the SDK for evaluation. Must be called before using `checkFlag` or `getFeatureFlags`.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `config` | `FeatureFlagConfig` | Yes | SDK configuration |

**`FeatureFlagConfig`:**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `environment` | `'development' | 'staging' | 'production'` | — | Environment tier for flag evaluation |

After initialization, the SDK polls for configuration updates every 60 seconds.

### `checkFlag(user, flagName, defaultValue?)`

```
```
1
2
```



```
checkFlag(user: FeatureFlagUser, flagName: string, defaultValue?: boolean): boolean
```
```

Evaluates a single feature flag for the given user. Synchronous after initialization.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `user` | `FeatureFlagUser` | Yes | User context for flag evaluation |
| `flagName` | `string` | Yes | The ID of the feature flag to evaluate |
| `defaultValue` | `boolean` | No | Fallback value if the flag cannot be evaluated. Defaults to `false`. |

**Returns:** `boolean` — `true` if the flag is enabled for this user, `false` otherwise.

### `getFeatureFlags(user, flagNames)`

```
```
1
2
```



```
getFeatureFlags(user: FeatureFlagUser, flagNames: string[]): Record<string, boolean>
```
```

Evaluates multiple flags in a single call.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `user` | `FeatureFlagUser` | Yes | User context for flag evaluation |
| `flagNames` | `string[]` | Yes | Array of flag IDs to evaluate |

**Returns:** `Record<string, boolean>` — Map of flag ID to boolean result.

### `shutdown()`

Stops the polling interval and releases resources. Call this when the SDK instance is no longer needed.

## Interfaces

### `FeatureFlagUser`

```
```
1
2
```



```
interface FeatureFlagUser {
  attributes?: Record<string, string | number>;
  identifiers?: {
    installContext?: string;
    accountId?: string;
  };
}
```
```

**`identifiers`**: Used for percentage-based rollout targeting. Pass `installContext` for site-level rollouts or `accountId` for user-level rollouts. Always pass at least one identifier for a stable evaluation experience.

**`attributes`**: Key/value pairs evaluated against flag rules. Predefined attributes:

| Attribute | Type | Description | Example values |
| --- | --- | --- | --- |
| `installContext` | `string` | ARI identifying the app installation context | `ari:cloud:confluence::site/abc123` |
| `accountId` | `string` | Atlassian account ID of the current user | `5b10ac8d82e05b22cc7d4ef5` |
| `appVersion` | `string` | Version of the app | `1.2.3` |
| `license` | `string` | App license status. Only present for paid apps in production. | `ACTIVE`, `INACTIVE`, `TRIAL` |
| `capabilitySet` | `string` | App license capability tier | `capabilityStandard`, `capabilityAdvanced` |

Custom attributes are also supported.

## Usage example

```
```
1
2
```



```
import { getAppContext } from "@forge/api";
import { FeatureFlags } from "@forge/feature-flags";

export const handler = async (payload, context) => {
  const { appVersion, license: appLicense, environmentType } = getAppContext();

  // Resolve license value
  let licenseValue = "INACTIVE";
  if (appLicense?.trialEndDate && new Date(appLicense.trialEndDate) > new Date()) {
    licenseValue = "TRIAL";
  } else if (appLicense?.isActive) {
    licenseValue = "ACTIVE";
  }

  // Resolve capabilitySet value
  const capabilitySetValue = appLicense?.capabilitySet === "capabilityAdvanced"
    ? "capabilityAdvanced"
    : "capabilityStandard";

  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: environmentType?.toLowerCase() || "development"
  });

  const user = {
    identifiers: {
      accountId: context?.principal?.accountId,
    },
    attributes: {
      installContext: context?.installContext,
      accountId: context?.principal?.accountId,
      appVersion,
      license: licenseValue,
      capabilitySet: capabilitySetValue,
    }
  };

  const isEnabled = featureFlags.checkFlag(user, "new-feature", false);
  const flags = featureFlags.getFeatureFlags(user, ["feature-a", "feature-b"]);

  featureFlags.shutdown();
};
```
```

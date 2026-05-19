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

Downloads the latest flag configuration and prepares the SDK for evaluation. Must be called before using `checkFlag`, `getFlag`, or `getAllFlagIds`.

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

### `getFlag(user, flagId)`

```
```
1
2
```



```
getFlag(user: FeatureFlagUser, flagId: string): FlagEvaluationDetails | undefined
```
```

Gets the evaluation details for a specific feature flag. Useful for debugging purposes.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `user` | `FeatureFlagUser` | Yes | User context for flag evaluation |
| `flagId` | `string` | Yes | The ID of the feature flag to retrieve |

**Returns:** `FlagEvaluationDetails | undefined` — The flag's evaluation details, or `undefined` if the flag does not exist.

---

### `getAllFlagIds()`

```
```
1
2
```



```
getAllFlagIds(): string[]
```
```

Returns an array of all available flag IDs in the current configuration.

**Returns:** `string[]` — An array of flag ID strings.

---

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

### `FlagEvaluationDetails`

```
```
1
2
```



```
interface FlagEvaluationDetails {
  flagId: string;
  name: string;
  value: boolean;
  matchedRule: string | null;
  reason: 'override' | 'rule_match' | 'default' | 'disabled';
}
```
```

Returned by `getFlag()`. Contains the full evaluation result for a specific flag.

| Property | Type | Description |
| --- | --- | --- |
| `flagId` | `string` | The unique identifier of the flag |
| `name` | `string` | The human-readable name of the flag |
| `value` | `boolean` | The evaluated value of the flag for the given user |
| `matchedRule` | `string | null` | The ID of the rule that matched, or `null` if no rule matched |
| `reason` | `string` | Why the flag resolved to its value: `'override'` (user-specific override applied), `'rule_match'` (a targeting rule matched), `'default'` (no rule matched, default value used), or `'disabled'` (flag is disabled) |

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
  } else if (appLicense?.active) {
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

  // Get evaluation details for a specific flag (useful for debugging)
  const flagDetails = featureFlags.getFlag(user, "new-feature");
  if (flagDetails) {
    console.log(`Flag "${flagDetails.name}" evaluated to ${flagDetails.value} (reason: ${flagDetails.reason})`);
  }

  // Get all available flag IDs
  const allFlagIds = featureFlags.getAllFlagIds();
  console.log("Available flags:", allFlagIds);

  featureFlags.shutdown();
};
```
```

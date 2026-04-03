# Feature flags client SDK

API reference for the feature flags client in the `@forge/bridge` package.

The client SDK evaluates feature flags directly in your Forge UI app's frontend code. Unlike the [server-side SDK](/platform/forge/feature-flags/feature-flags-sdk), it runs in the browser and does not require a resolver round-trip for flag evaluation.

The client SDK is available from `@forge/bridge` version `5.15.0`.

## Installation

Check the latest version on npm: [@forge/bridge versions](https://www.npmjs.com/package/@forge/bridge?activeTab=versions).

## `FeatureFlags`

### Constructor

Creates a new instance of the client SDK.

### `initialize(user, config?)`

```
1
initialize(user: FeatureFlagUser, config?: ForgeFeatureFlagConfig): Promise<void>
```

Downloads flag configuration and prepares the SDK for evaluation. Must be called before using `checkFlag`.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `user` | `FeatureFlagUser` | Yes | User context for flag evaluation |
| `config` | `ForgeFeatureFlagConfig` | No | SDK configuration. Defaults to `development` environment. |

Call `initialize()` once at app startup, not on every render.

### `checkFlag(flagName, defaultValue?)`

```
```
1
2
```



```
checkFlag(flagName: string, defaultValue?: boolean): boolean
```
```

Evaluates a feature flag for the initialized user. Synchronous after initialization.

**Parameters:**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `flagName` | `string` | Yes | The ID of the feature flag to check |
| `defaultValue` | `boolean` | No | Fallback value if the flag cannot be evaluated. Defaults to `false`. |

**Returns:** `boolean` — `true` if the flag is enabled, `false` otherwise.

### `isInitialized()`

```
```
1
2
```



```
isInitialized(): boolean
```
```

**Returns:** `boolean` — `true` if the SDK has been initialized, `false` otherwise.

### `shutdown()`

Releases resources. Call this before re-initializing with an updated user context.

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

**`identifiers`**: Used for percentage-based rollout targeting. Supports `installContext` and `accountId`. Always pass at least one identifier for a stable evaluation experience.

**`attributes`**: Key/value pairs evaluated against flag rules. Predefined attributes include `installContext`, `appVersion`, `license`, and `capabilitySet`. Custom attributes are also supported.

### `ForgeFeatureFlagConfig`

```
```
1
2
```



```
interface ForgeFeatureFlagConfig {
  environment?: 'development' | 'staging' | 'production';
}
```
```

## Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `environment` | `'development' | 'staging' | 'production'` | `'development'` | Environment tier for flag evaluation |

Use `view.getContext()` from `@forge/bridge` to get the current environment:

```
```
1
2
```



```
const { environmentType } = await view.getContext();
const config = {
  environment: environmentType.toLowerCase(), // "development", "staging", or "production"
};
```
```

## Usage example

```
```
1
2
```



```
import { useEffect, useState } from "react";
import { view, FeatureFlags } from "@forge/bridge";

const App = () => {
  const [isFeatureEnabled, setIsFeatureEnabled] = useState(false);

  useEffect(() => {
    const initializeFeatureFlags = async () => {
      const { accountId, cloudId, environmentType } = await view.getContext();

      const user = {
        attributes: {
          installContext: `ari:cloud:confluence::site/${cloudId}`,
        },
        identifiers: {
          accountId: accountId,
        },
      };

      const config = {
        environment: environmentType.toLowerCase(),
      };

      const featureFlags = new FeatureFlags();
      await featureFlags.initialize(user, config);

      const enabled = featureFlags.checkFlag("is-feature-enabled");
      setIsFeatureEnabled(enabled);
    };

    initializeFeatureFlags();
  }, []);

  return (
    <>
      {isFeatureEnabled ? (
        <Text>Feature is enabled!</Text>
      ) : (
        <Text>Feature is not enabled.</Text>
      )}
    </>
  );
};
```
```

## Re-initializing with an updated user

To re-evaluate flags with a different user context, shut down the current instance first:

```
```
1
2
```



```
featureFlags.shutdown();

const updatedUser = {
  attributes: {
    installContext: `ari:cloud:confluence::site/${cloudId}`,
    issueId: "<JIRA_ISSUE_ID>",
  },
  identifiers: {
    accountId: accountId,
  },
};

await featureFlags.initialize(updatedUser, { environment: "production" });
```
```

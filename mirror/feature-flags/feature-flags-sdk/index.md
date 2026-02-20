# Feature flags SDK

Forge Feature Flags is now available as part of Forge Early Access Program (EAP). To start testing this feature, sign up using this
[form](https://ecosystem.atlassian.net/servicedesk/customer/portal/38/group/136/create/18725).

Forge Feature Flags is an experimental feature offered to selected users for testing and feedback purposes. This
feature is unsupported and subject to change without notice. Do not use Forge Feature Flags in apps that
handle sensitive information and customer data. The Feature flags EAP is fully functional in development, staging, and production environments.

**Note: Feature flags are not available in Atlassian Government Cloud or FedRAMP environments. See**, [Limitations](/platform/forge/feature-flags/limitations#atlassian-government-cloud).

The Feature flags SDK in Forge is the in-code tool that developers use to flag their features. The SDK runs in Forge functions (resolvers, triggers, and other backend code) and provides local evaluation of feature flags.

## SDK overview

The server-side SDK (`@forge/feature-flags`) is designed for Forge runtime and Forge resolvers.

**Key characteristics:**

* **Local evaluation**: Evaluations are done in real-time without a network request. Flag checks are effectively a dictionary lookup with some computation.
* **Polling for updates**: The SDK makes an upfront request for configuration files, then continually polls for changes every 60 seconds.
* **Multi-user support**: The SDK is designed to run against multiple users, and all SDK methods require a user object for evaluation.

## Getting started

### Prerequisites

### Installation

Install the server SDK using npm:

```
```
1
2
```



```
npm install @forge/feature-flags@latest
```
```

### Basic usage pattern

The SDK follows a simple pattern:

1. **[Initialize](#usage-example)**: Set up the SDK and download the latest flag configurations
2. **[Check a flag](#usage-example)**: Evaluate flags using the user object

After initialization, the SDK evaluates flags without a network request, typically in less than 1ms.

## Core concepts

### User object

The user object is the input you provide to the SDK for flag targeting. If you want to target on an attribute, you need to add it to your user object.

The interface for the User Object is:

```
```
1
2
```



```
interface FeatureFlagUser {
  custom?: Record<string, string | number>;
  attributes?: {
    installContext?: string;
    accountId?: string;
    appVersion?: string;
    license?: string;
    capabilitySet?: string;
  };
  identifiers?: {
    installContext?: string;
    accountId?: string;
  };
}
```
```

#### User object properties

**identifiers**: Dictionary containing key/value pairs for feature flag targeting, especially for percentage-based rollouts. Supports `installContext` and `accountId`.

**attributes**: Dictionary containing key/value pairs for feature flag targeting. Supports:

* `installContext`
* `appVersion`
* `license`
* `capabilitySet`

**custom**: Dictionary for custom targeting attributes not supported in the `attributes` field.

A user object with identifiers is required for `checkFlag`. Always pass the `accountId` or `installContext` if available to ensure a stable experience.

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
  // Get app context values
  const {
    appVersion,
    license: appLicense,
    environmentType,
  } = getAppContext();

  // Determine license value based on trialEndDate and isActive
  let licenseValue = "INACTIVE";
  const trialEndDate = appLicense?.trialEndDate;
  const isActive = appLicense?.isActive;

  if (trialEndDate) {
    const now = new Date();
    const trialEnd = new Date(trialEndDate);
    if (trialEnd > now) {
      licenseValue = "TRIAL";
    } else if (isActive) {
      licenseValue = "ACTIVE";
    }
  } else if (isActive) {
    licenseValue = "ACTIVE";
  }

  // Determine capabilitySet value (enum)
  let capabilitySetValue = "capabilityStandard";
  if (appLicense?.capabilitySet === "capabilityAdvanced") {
    capabilitySetValue = "capabilityAdvanced";
  }

  // Initialize the feature flags SDK
  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: environmentType?.toLowerCase() || "development" 
  });

  // Define a user with all possible attributes for feature flag rules
  const user = {
    identifiers: {
      accountId: context?.principal?.accountId,
    },
    attributes: { 
      installContext: context?.installContext,
      accountId: context?.principal?.accountId,
      appVersion: appVersion,
      license: licenseValue, // "ACTIVE", "INACTIVE", "TRIAL"
      capabilitySet: capabilitySetValue // "capabilityAdvanced", "capabilityStandard"
    }
  };

  // Check a feature flag (synchronous after initialization)
  const isEnabled = featureFlags.checkFlag(user, "new-feature");

  // Get multiple flags at once (synchronous)
  const flags = featureFlags.getFeatureFlags(user, ["feature-a", "feature-b"]);

  // Shutdown when done
  await featureFlags.shutdown();
}
```
```

## Best practices

### Error handling

The SDK is designed to be resilient and provide fallback behavior:

* **Initialization failures**: Default to safe fallback values (typically `false` for boolean flags)
* **Invalid flag names**: Return `false` for non-existent flags

```
```
1
2
```



```
// Example error handling
try {
  const isEnabled = featureFlags.checkFlag(user, "new-feature");
} catch (error) {
  console.warn("Feature flag evaluation failed:", error);
  // Use safe fallback
  const isEnabled = false;
}
```
```

## Troubleshooting

### Common issues

**SDK Initialization Fails**

* Ensure you're using the correct environment (`development`, `staging`, `production`)
* Verify your app has feature flag permissions enabled
* Check that you're in the EAP program

**Flags Always Return Default Values**

* Confirm the flag exists in the Developer Console
* Verify the flag is enabled for your environment
* Check that your user object contains required identifiers

**Performance Issues**

* The SDK polls every 60 seconds by default — this is normal
* Flag evaluations should be sub-1ms after initialization

## Next steps

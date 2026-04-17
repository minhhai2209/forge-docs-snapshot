# Target specific users or organizations

This guide shows you how to enable a feature flag for specific users (by account ID), specific organizations (by install context), or users with a specific license tier — rather than a random percentage.

## Prerequisites

* The server-side SDK is installed: `npm install @forge/feature-flags@latest`
* You have a flag created in [Developer Console](https://developer.atlassian.com/console)

## Target a specific organization (by installContext)

Use this approach to enable a feature for all users in a particular Atlassian site — for example, a specific enterprise customer.

### Step 1: Create the flag with installContext ID type

In Developer Console, create the flag with **ID type: installContext**.

### Step 2: Add the flag check

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
19
20
21
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

  const isEnabled = featureFlags.checkFlag(user, "enterprise-feature", false);
  featureFlags.shutdown();
  return isEnabled;
});
```

### Step 3: Target the organization in Developer Console

1. Go to your flag → **Rules**
2. Add a rule: `installContext` **equals** `<the ARI for that site>`
3. Set the rule result to **Pass**
4. Save

The `installContext` ARI looks like `ari:cloud:confluence::site/<site-id>`. To find it, go to the **Installations** page in Developer Console and click the **Copy Site ARI** icon next to the site name.

## Target specific users (by accountId)

Use this approach to enable a feature for named users — for example, your own team for internal testing, or a specific beta user.

### Step 1: Create the flag with accountId ID type

In Developer Console, create the flag with **ID type: accountId**.

### Step 2: Add the flag check

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

  const isEnabled = featureFlags.checkFlag(user, "beta-feature", false);
  featureFlags.shutdown();
  return isEnabled;
});
```
```

### Step 3: Target users in Developer Console

1. Go to your flag → **Rules**
2. Add a rule: `accountId` **is one of** — enter each account ID individually and press Enter to confirm before adding the next
3. Set the pass percentage (0–100%) based on your requirements
4. Save

## Target by license tier

Use the `license` attribute to enable features only for paid or trial users.

```
```
1
2
```



```
import { getAppContext } from "@forge/api";
import { FeatureFlags } from "@forge/feature-flags";

resolver.define('getFeature', async ({ context }) => {
  const { license: appLicense, environmentType } = getAppContext();

  // Determine the license value
  let licenseValue = "INACTIVE";
  if (appLicense?.trialEndDate && new Date(appLicense.trialEndDate) > new Date()) {
    licenseValue = "TRIAL";
  } else if (appLicense?.active) {
    licenseValue = "ACTIVE";
  }

  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: environmentType?.toLowerCase() || "development"
  });

  const user = {
    identifiers: {
      installContext: context?.installContext,
    },
    attributes: {
      installContext: context?.installContext,
      license: licenseValue, // "ACTIVE", "INACTIVE", or "TRIAL"
    }
  };

  const isEnabled = featureFlags.checkFlag(user, "premium-feature", false);
  featureFlags.shutdown();
  return isEnabled;
});
```
```

In Developer Console, add a rule: `license` **equals** `ACTIVE` → **Pass**.

The `license` attribute is only available for paid apps in production. In development and staging environments, `license` is `undefined`. See [Attributes](/platform/forge/feature-flags/feature-flags-sdk#attributes) for the full list of predefined attribute values.

## Target by capability tier

Use `capabilitySet` to differentiate between Standard and Advanced license tiers:

```
```
1
2
```



```
let capabilitySetValue = "capabilityStandard";
if (appLicense?.capabilitySet === "capabilityAdvanced") {
  capabilitySetValue = "capabilityAdvanced";
}

const user = {
  identifiers: { installContext: context?.installContext },
  attributes: {
    installContext: context?.installContext,
    capabilitySet: capabilitySetValue, // "capabilityStandard" or "capabilityAdvanced"
  }
};
```
```

In Developer Console, add a rule: `capabilitySet` **equals** `capabilityAdvanced` → **Pass**.

## Use custom attributes

If the predefined attributes don't meet your needs, pass any custom key/value pair in the `attributes` field:

```
```
1
2
```



```
const user = {
  identifiers: {
    installContext: context?.installContext,
  },
  attributes: {
    region: "EU",          // custom string attribute
    issueCount: 4,         // custom numeric attribute
  }
};
```
```

Configure matching rules in Developer Console under **Rules** using the attribute name you defined.

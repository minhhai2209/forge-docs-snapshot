# Feature flags quick start guide

Forge Feature Flags is now available as part of Forge Early Access Program (EAP). To start testing this feature, sign up using this
[form](https://ecosystem.atlassian.net/servicedesk/customer/portal/38/group/136/create/18725).

Forge Feature Flags is an experimental feature offered to selected users for testing and feedback purposes. This
feature is unsupported and subject to change without notice. Do not use Forge Feature Flags in apps that
handle sensitive information and customer data. The Feature flags EAP is fully functional in development, staging, and production environments.

**Note: Feature flags are not available in Atlassian Government Cloud or FedRAMP environments. See**, [Limitations](/platform/forge/feature-flags/limitations#atlassian-government-cloud).

Get started with feature flags in your Forge app. You'll create a simple toggle that controls a welcome message without redeploying your app.

**What you'll build:** A feature flag that shows/hides a premium welcome message

**Time:** 10 minutes

## Before you begin

You need:

**Install required packages:**

```
1
2
cd your-forge-app
npm install @forge/feature-flags@latest
```

## Step 1: Add feature flag code

Update your resolver code to include the feature flag SDK initialization and flag evaluation logic. Replace your `src/resolvers/index.js`:

```
```
1
2
```



```
//src/resolvers/index.js
import Resolver from '@forge/resolver';
import { FeatureFlags } from "@forge/feature-flags";

const resolver = new Resolver();

resolver.define('getFlagValue', async ({ payload, context }) => {
  const featureFlags = new FeatureFlags();
  await featureFlags.initialize({
    environment: context?.environmentType?.toLowerCase() || "development" 
  });

  const user = {
    identifiers: {
      installContext : context?.installContext
    },
    attributes: { 
      installContext : context?.installContext
    }
  }

  return featureFlags.checkFlag( user, payload?.flag, false);
});

export const handler = resolver.getDefinitions();
```
```

Update your frontend code to include feature flag logic. Replace your `src/frontend/index.jsx`:

```
```
1
2
```



```
// src/frontend/index.jsx
import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Text } from '@forge/react';
import { view } from '@forge/bridge';

const App = () => {
  const [showPremium, setShowPremium] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    invoke('getFlagValue', { flag: 'show_premium_welcome' })
      .then((value) => {
        setShowPremium(value)
        setLoading(false);
      })
      .catch(() => {
        console.error('Feature flag error:');
        setShowPremium(false);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <Text>Loading...</Text>;
  }

  return (
    <>
      <Text>Hello world!</Text>
      {showPremium && (
        <Text appearance="success">🎉 Welcome to Premium Features!</Text>
      )}
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

**What this code does:**

* Gets `installContext` from the context
* Initializes `FeatureFlags` with user context and environment in the resolver
* Checks the `show_premium_welcome` flag
* Shows premium message only when flag is enabled

## Step 2: Deploy your app

Deploy your app with the feature flag code:

```
```
1
2
```



```
forge deploy
forge install --upgrade
```
```

Your app is now deployed with feature flag code, but the flag doesn't exist yet (it will default to `false`).

## Step 3: Create the feature flag

Now create the feature flag in Developer Console:

1. Go to [Developer Console](https://developer.atlassian.com/console)
2. Select your app → **Manage** → **Feature flags**
3. Click **Create flag**
4. Configure:
   * **Name**: `show premium welcome`
   * **Description**: `Controls premium welcome message visibility`
   * **ID type**: `installContext`
5. Click **Confirm**

The Flag ID (`show_premium_welcome`) is automatically generated from the name you provide.

6. On the Setup page:
   * Set **Pass** to `100%` and **Fail** to `0%`
   * Ensure the **DEV** environment is checked
   * Click **Save**

## Step 4: Test your feature flag

1. **Refresh your app** - You should now see: "🎉 Welcome to Premium Features!"
2. **Test the toggle:**

   * Go to Developer Console → Feature flags → `show_premium_welcome`
   * Change **Pass** to `0%`, **Fail** to `100%`
   * **Save**
   * Refresh app - Premium message disappears
   * Change back to **Pass** `100%`, **Fail** `0%`
   * **Save**
   * Refresh app - Premium message returns!

## Next steps

Congratulations! You've successfully implemented your first feature flag. Here's what to explore next:

### Expand your implementation

* Create additional flags for different features
* Practice percentage rollouts (10%, 50%, etc.)
* Test environment-specific configurations

### Best practices to implement

* Use descriptive names: `new-dashboard-layout`, `checkout-v2`
* Include team/component: `team-dashboard-redesign`
* Test both enabled and disabled states
* Write unit tests that mock feature flag responses
* Use staging environment for validation

### Continue learning

---

**You're now ready to use feature flags in your Forge apps!** Start experimenting with different flag configurations and rollout strategies.

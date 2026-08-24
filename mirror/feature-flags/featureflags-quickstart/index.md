# Tutorial: Your first feature flag

In this tutorial, you'll add a feature flag to a Forge app, create the flag in Developer Console, and see it toggle a UI element on and off — without redeploying your app.

**What you'll build:** A flag that shows or hides a premium welcome message.

**What you'll learn:**

* How to add the server-side SDK to your resolver
* How to check a flag at runtime
* How to create a flag in Developer Console and activate it

**Time:** 10 minutes

## Before you begin

You need:

Install the server-side SDK:

```
1cd your-forge-app
2npm install @forge/feature-flags@latest
3
```

## Step 1: Add feature flag code

Update your resolver to initialize the SDK and check a flag. Replace your `src/resolvers/index.js`:

```
1// src/resolvers/index.js
2import Resolver from '@forge/resolver';
3import { FeatureFlags } from "@forge/feature-flags";
4
5const resolver = new Resolver();
6
7resolver.define('getFlagValue', async ({ payload, context }) => {
8  const featureFlags = new FeatureFlags();
9  await featureFlags.initialize({
10    environment: context?.environmentType?.toLowerCase() || "development"
11  });
12
13  const user = {
14    identifiers: {
15      installContext: context?.installContext
16    },
17    attributes: {
18      installContext: context?.installContext
19    }
20  };
21
22  return featureFlags.checkFlag(user, payload?.flag, false);
23});
24
25export const handler = resolver.getDefinitions();
26
```

Update your frontend to call the resolver and show the message. Replace your `src/frontend/index.jsx`:

```
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
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
```



```
// src/frontend/index.jsx
import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Text } from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const [showPremium, setShowPremium] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    invoke('getFlagValue', { flag: 'show_premium_welcome' })
      .then((value) => {
        setShowPremium(value);
        setLoading(false);
      })
      .catch(() => {
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
        <Text appearance="success">Welcome to Premium Features!</Text>
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

## Step 2: Deploy your app

```
```
1
2
3
```



```
forge deploy
forge install --upgrade
```
```

The app now contains feature flag code, but the flag doesn't exist yet — it defaults to `false`.

## Step 3: Create the feature flag

1. Go to [Developer Console](https://developer.atlassian.com/console)
2. Select your app → **Manage** → **Feature flags**
3. Click **Create flag**
4. Configure:
   * **Name**: `show premium welcome`
   * **Description**: `Controls premium welcome message visibility`
   * **ID type**: `installContext`
5. Click **Confirm**

The Flag ID (`show_premium_welcome`) is automatically generated from the name.

6. On the Setup page:
   * Set **Pass** to `100%` and **Fail** to `0%`
   * Ensure the **DEV** environment is checked
   * Click **Save**

## Step 4: Test your feature flag

1. **Refresh your app** — You should now see the "Welcome to Premium Features!" message.
2. **Toggle it off:**

   * Go to Developer Console → Feature flags → `show_premium_welcome`
   * Change **Pass** to `0%`, **Fail** to `100%` → **Save**
   * Refresh your app — the message disappears
3. **Toggle it back on:**

   * Change back to **Pass** `100%`, **Fail** `0%` → **Save**
   * Refresh — the message returns

You've just controlled a feature without redeploying your app.

## What you learned

* The server-side SDK (`@forge/feature-flags`) initializes in your resolver
* `checkFlag(user, flagId, defaultValue)` returns `true` or `false` based on your flag configuration
* Flags default to `false` when they don't exist yet — safe to deploy code before creating the flag
* You can change flag behavior instantly from Developer Console

## Next steps

# Tutorial: Dark mode switcher Confluence app with feature flags

This tutorial shows you how to build a dark mode toggle in a Confluence Forge app and control it with a feature flag. You'll use the client SDK to evaluate the flag directly in the frontend — no resolver needed.

By the end of this tutorial, you'll have a working Confluence macro that lets users switch between light and dark mode, with the ability to enable or disable the feature instantly without redeploying your app.

Feature flags are not available in Atlassian Government Cloud or FedRAMP environments. See [Limitations](/platform/forge/feature-flags/limitations#atlassian-government-cloud).

## Before you begin

This tutorial assumes you have experience with basic Forge development. If you're new to Forge, complete the [hello world tutorial](/platform/forge/build-a-hello-world-app-in-confluence/) first.

You need:

* Forge CLI installed and configured
* A Confluence Forge app already deployed (the hello world app is sufficient)
* Access to [Atlassian Developer Console](https://developer.atlassian.com/console)

Install the `@forge/bridge` package:

```
1
npm install @forge/bridge@latest
```

Feature flags in the client SDK require `@forge/bridge` version `5.15.0` or later.

## What you'll build

A Confluence macro that:

* Uses the client SDK (`@forge/bridge`) to check a feature flag in the browser
* Shows a dark/light mode toggle button when the flag is enabled
* Shows a disabled message when the flag is disabled
* Reflects flag changes in real time without a page reload (by re-initializing the client)

This demonstrates the client SDK pattern: flag evaluation happens entirely in the frontend, with no backend resolver involved.

## Step 1: Set up your app

If you already have a hello world Confluence app, you can use it. Otherwise, create a new one:

When prompted:

* **App name**: `dark-mode-switcher`
* **Template**: `confluence-macro`
* **Template category**: `UI Kit`

Your app structure:

```
```
1
2
```



```
dark-mode-switcher/
├── manifest.yml
├── package.json
└── src/
    ├── index.js
    ├── frontend/
    │   └── index.jsx
    └── resolvers/
        └── index.js
```
```

## Step 2: Create the feature flag

1. Go to [Atlassian Developer Console](https://developer.atlassian.com/console)
2. Select your app → **Manage** → **Feature flags**
3. Click **Create flag**
4. Configure:
   * **Name**: `Is Dark Mode Enabled`
   * **Description**: `Enable or disable dark mode in the Forge app`
   * **ID type**: `accountId` (targets individual users)
5. Click **Confirm**

The Flag ID (`is_dark_mode_enabled`) is generated automatically from the name. Note this ID exactly — you'll use it in your code.

### Configure the flag for development

On the **Setup** page after confirming:

1. Select `installContext` for the **Attribute key**
2. Add the install context values for the sites where you want to enable the feature
3. Set **Pass** to `100%` and **Fail** to `0%`
4. Check the **DEV** environment
5. Click **Save**

## Step 3: Update the manifest

Replace your `manifest.yml`:

```
```
1
2
```



```
# manifest.yml
modules:
  macro:
    - key: switch-dark-mode
      resource: main
      render: native
      resolver:
        function: resolver
      title: switch-dark-mode
      adfExport:
        function: export-key
  function:
    - key: resolver
      handler: index.handler
    - key: export-key
      handler: macroExport.exportFunction
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs22.x
    memoryMB: 256
    architecture: arm64
  id: ari:cloud:ecosystem::app/<your-app-id>
```
```

## Step 4: Implement the frontend

Replace your `src/frontend/index.jsx`:

```
```
1
2
```



```
// src/frontend/index.jsx
import React, { useEffect, useState } from "react";
import ForgeReconciler, { Box, Button, Text, Stack } from "@forge/react";
import { view, FeatureFlags } from "@forge/bridge";

const App = () => {
  const [refresh, setRefresh] = useState(false);
  const [isDarkModeEnabled, setIsDarkModeEnabled] = useState(null);
  const [darkUiActive, setDarkUiActive] = useState(false);

  const onRefresh = () => {
    setRefresh(true);
  };

  const onToggleDarkMode = () => {
    setDarkUiActive((prev) => !prev);
  };

  useEffect(() => {
    void view.theme.enable();
  }, []);

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

      const result = featureFlags.checkFlag("is_dark_mode_enabled");
      setIsDarkModeEnabled(result);

      if (!result) {
        setDarkUiActive(false);
      }
    };

    initializeFeatureFlags();
    setRefresh(false);
  }, [refresh]);

  if (isDarkModeEnabled === null) {
    return <Text>Loading…</Text>;
  }

  return (
    <Box
      padding="space.200"
      backgroundColor={darkUiActive ? "color.background.neutral.bold" : undefined}
    >
      <Stack space="space.200" alignInline="center">
        <Button onClick={onRefresh}>Refresh</Button>
        {isDarkModeEnabled ? (
          <Text color={darkUiActive ? "color.text.inverse" : "color.text"}>
            Dark mode feature is enabled
          </Text>
        ) : (
          <Text color={darkUiActive ? "color.text.inverse" : "color.text"}>
            Dark mode feature is disabled
          </Text>
        )}
        <Text color={darkUiActive ? "color.text.inverse" : "color.text"}>
          Dark mode UI is {darkUiActive ? "on" : "off"}
        </Text>
        {isDarkModeEnabled ? (
          <Button onClick={onToggleDarkMode}>
            {darkUiActive ? "Switch to light mode" : "Switch to dark mode"}
          </Button>
        ) : null}
      </Stack>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```
```

**How this works:**

* `view.theme.enable()` activates Forge's theme support for the component
* The `useEffect` with `[refresh]` dependency re-initializes the feature flag client each time the Refresh button is pressed, picking up any flag configuration changes without a full page reload
* `checkFlag("is_dark_mode_enabled")` returns `false` by default if the flag doesn't exist yet — safe to deploy before the flag is active
* When the flag is disabled, the toggle button is hidden and `darkUiActive` resets to `false`

## Step 5: Deploy your app

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

Select your Confluence site when prompted.

## Step 6: Add the macro to a Confluence page and test

1. Open Confluence and navigate to any page
2. Edit the page and type `/` to open the macro menu
3. Search for **switch-dark-mode** and insert it
4. Save the page

With the flag enabled (Pass: 100%), you see:

* "Dark mode feature is enabled"
* A **Switch to dark mode** button that toggles the background and text colors

### Test disabling the flag

1. Go to Developer Console → your app → **Manage** → **Feature flags** → `is_dark_mode_enabled`
2. Change **Pass** to `0%`, **Fail** to `100%` → **Save**
3. Click **Refresh** in the macro (or reload the page)
4. The toggle button disappears and the message reads "Dark mode feature is disabled"

### Re-enable the flag

1. Change **Pass** back to `100%`, **Fail** to `0%` → **Save**
2. Click **Refresh** — the toggle button reappears

## Next steps

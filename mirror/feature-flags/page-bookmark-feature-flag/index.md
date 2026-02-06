# Page bookmark Confluence app with Feature flags

Forge Feature Flags is now available as part of Forge Early Access Program (EAP). To start testing this feature, sign up using this
[form](https://ecosystem.atlassian.net/servicedesk/customer/portal/38/group/136/create/18725).

Forge Feature Flags is an experimental feature offered to selected users for testing and feedback purposes. This
feature is unsupported and subject to change without notice. Do not use Forge Feature Flags in apps that
handle sensitive information and customer data. The Feature flags EAP is fully functional in development, staging, and production environments.

**Note: Feature flags are not available in Atlassian Government Cloud or FedRAMP environments. See**, [Limitations](/platform/forge/feature-flags/limitations#atlassian-government-cloud).

This tutorial describes how to build a page bookmarking feature for Confluence using feature flags. You'll learn how to create a user-friendly bookmark button that allows users to save pages to their personal collection, with the entire feature controlled by a feature flag for safe rollout and testing.

By the end of this tutorial, you'll have a working Confluence macro that lets users bookmark pages, with the ability to enable or disable the feature instantly without redeployment.

## Before you begin

To complete this tutorial, you need:

## Scenario: Building a page bookmark feature

Let's walk through building a practical feature: a page bookmarking system that allows users to save their favorite Confluence pages. This demonstrates how feature flags enable you to:

* Roll out new features gradually to different user groups
* Test new features safely in development
* Disable features instantly if issues arise
* Control both frontend UI and backend storage independently

## Step 1: Set up your initial app

If you already have a hello world Confluence app, you can use it. Otherwise, create a new one:

When prompted:

* **App name**: `page-bookmark-app`
* **Template**: Select "confluence-macro"
* **Template category**: Select "UI Kit"

This tutorial uses **UI Kit** (Forge React components). UI Kit provides pre-built components like `Button`, `Text`, and more, making it easier to build consistent Confluence integrations.

Your app folder structure should look like this:

```
```
1
2
```



```
page-bookmark-app/
├── manifest.yml                
├── package.json                
├── node_modules/               
└── src/                        
    ├── index.js                
    ├── frontend/               
    │   └── index.jsx          
    └── resolvers/              
        └── index.js
```
```

### Initial frontend code

Your starting `src/frontend/index.jsx` should be a simple hello world:

```
```
1
2
```



```
// src/frontend/index.jsx
import React from 'react';
import ForgeReconciler, { Text } from '@forge/react';

const App = () => {
  return (
    <>
      <Text>Hello world!</Text>
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

## Step 2: Create the feature flag in Developer Console

Before implementing the bookmark feature, set up the feature flag that will control it.

### Navigate to feature flags

1. Go to [Atlassian Developer Console](https://developer.atlassian.com/console).
2. Select your app from **My apps**.
3. Navigate to **Manage** → **Feature flags**.

### Create the bookmark feature flag

1. Click **Create flag**.
2. Configure the flag:

   * **Name**: `enable page bookmarks`
   * **Description**: `Controls the page bookmarking feature - displays bookmark button and manages bookmark storage`
   * **ID type**: `installContext` (targets specific Confluence installations)
3. Click **Confirm**.

The Flag ID (`enable_page_bookmarks`) is automatically generated from the name and will be used in your code.

**Important:** Note down your **Flag ID** exactly as shown. You will need to use this exact ID in your resolver code in Step 3. The Flag ID must match exactly — if you used a different name, your Flag ID will be different (for example, "MyPageBookmark" becomes `mypagebookmark`).

### Configure flag rules for development

1. After clicking **Confirm**, you'll be on the **Setup** page.
2. Configure the rule:

   * Leave **Attribute key** as default.
   * Set **Pass** to `100%` and **Fail** to `0%`.
   * This enables the bookmark feature for all users.
3. Ensure the **DEV** environment is checked at the top of the rule card.
4. Click **Save** to apply your configuration.

## Step 3: Implement the bookmark feature with feature flags

Now that your feature flag is created, implement the bookmarking functionality in your app.

### Update manifest.yml

First, ensure your manifest has the necessary permissions:

```
```
1
2
```



```
# manifest.yml
modules:
  macro:
    - key: page-bookmark-hello-world-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: Page Bookmarks
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
permissions:
  scopes:
    - read:confluence-content.summary
    - storage:app
app:
  runtime:
    name: nodejs22.x
    memoryMB: 256
    architecture: arm64
  id: ari:cloud:ecosystem::app/<Replace with your App Id>
```
```

Key permissions:

* **`read:confluence-content.summary`**: Allows reading page information
* **`storage:app`**: Enables storing bookmark data

### Implement the frontend with feature flag

Replace your `src/frontend/index.jsx` with the bookmark feature controlled by a feature flag:

```
```
1
2
```



```
// src/frontend/index.jsx
import React, { useEffect, useState } from 'react';
import ForgeReconciler, { 
  Text, 
  Button, 
  useProductContext,
  Box,
  Stack,
  Lozenge
} from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const context = useProductContext();
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [showBookmarkFeature, setShowBookmarkFeature] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check bookmark status when feature is enabled
  useEffect(() => {
    // Wait for context to be available before checking feature flag
    if (!context) return;

    const pageId = context?.extension?.content?.id;
    if (pageId) {
      invoke('checkBookmark', { pageId }).then(({isEnabled, bookmark}) => {
        setIsBookmarked(bookmark);
        setShowBookmarkFeature(isEnabled);
        setLoading(false);
      });
    } else {
      setLoading(false);
      setShowBookmarkFeature(false);
    }
  }, [context]);

  // Handle bookmark toggle
  const toggleBookmark = async () => {
    const pageId = context?.extension?.content?.id;
    if (!pageId) return;

    const newStatus = await invoke('toggleBookmark', { pageId });
    setIsBookmarked(newStatus);
  };

  if (loading) {
    return (
      <Box padding="space.100">
        <Text appearance="subtle">Loading...</Text>
      </Box>
    );
  }

  // If feature flag is disabled, show educational message
  if (!showBookmarkFeature) {
    return (
      <Box padding="space.150">
        <Text appearance="subtle">
          The bookmark feature is controlled by a feature flag. Enable it in Developer Console to activate.
        </Text>
      </Box>
    );
  }

  // Feature flag is enabled - show fully functional bookmark UI
  return (
    <Box padding="space.150">
      <Stack space="space.150" alignInline="start">
        <Button 
          onClick={toggleBookmark}
          appearance={isBookmarked ? "primary" : "default"}
          iconBefore={isBookmarked ? "star-filled" : "star"}
        >
          {isBookmarked ? "Bookmarked" : "Bookmark"}
        </Button>
        {isBookmarked && (
          <Lozenge appearance="success" isBold>
            Saved
          </Lozenge>
        )}
      </Stack>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

**Key implementation details:**

1. **Feature flag initialization**: Uses `ForgeFeatureFlags` SDK to check if the bookmark feature is enabled
2. **User context**: Includes `accountId` and `installContext` for proper feature targeting
3. **Environment awareness**: Automatically detects and uses the correct environment
4. **Conditional rendering**: Shows educational message when feature flag is disabled, full UI when enabled
5. **Visual feedback**: Button changes appearance (default → primary) and displays "Saved" badge when bookmarked
6. **Graceful degradation**: If the feature flag check fails, the feature is hidden with a clear message

### Implement backend resolvers with feature flag

Create or update `src/resolvers/index.js` to handle bookmark operations:

```
```
1
2
```



```
// src/resolvers/index.js
import Resolver from '@forge/resolver';
import { storage, getAppContext } from '@forge/api';
import { ForgeFeatureFlags } from "@forge/feature-flags-node";

const resolver = new Resolver();

// Helper function to check if feature flag is enabled
async function isBookmarkFeatureEnabled(context) {
  try {
    const { environmentType } = getAppContext();
    
    const featureFlags = new ForgeFeatureFlags();
    await featureFlags.initialize({
      environment: environmentType?.toLowerCase() || "development" 
    });

    const user = {
      identifiers: {
        accountId: context?.accountId,
      },
      attributes: {
        installContext: context?.installContext
      }
    };

    // IMPORTANT: Replace "enable_page_bookmarks" with your Flag ID from Developer Console
    // if you used a different name when creating the flag
    return featureFlags.checkFlag(user, "enable_page_bookmarks");
  } catch (error) {
    console.error("Feature flag check failed:", error);
    return false;
  }
}

// Toggle bookmark for a page
resolver.define('toggleBookmark', async (req) => {
  const { context, payload } = req;
  const { pageId } = payload;
  const accountId = context.accountId;

  // Check feature flag before processing
  const isEnabled = await isBookmarkFeatureEnabled(context);
  if (!isEnabled) {
    console.log("Bookmark feature is disabled");
    return false;
  }

  // Get user's bookmarks from storage
  const storageKey = `bookmarks_${accountId}`;
  const bookmarks = await storage.get(storageKey) || [];

  // Toggle bookmark status
  if (bookmarks.includes(pageId)) {
    // Remove bookmark
    const updatedBookmarks = bookmarks.filter(id => id !== pageId);
    await storage.set(storageKey, updatedBookmarks);
    return false;
  } else {
    // Add bookmark
    await storage.set(storageKey, [...bookmarks, pageId]);
    return true;
  }
});

// Check if a page is bookmarked
resolver.define('checkBookmark', async (req) => {
  const { context, payload} = req;
  const { pageId } = payload;
  const accountId = context.accountId;

  // Check feature flag before processing
  const isEnabled = await isBookmarkFeatureEnabled(context);
  if (!isEnabled) {
    return {isEnabled, bookmark : false};
  }

  // Check if page is in user's bookmarks
  const storageKey = `bookmarks_${accountId}`;
  const bookmarks = await storage.get(storageKey) || [];
  return { isEnabled, bookmark : bookmarks.includes(pageId)};
});

export const handler = resolver.getDefinitions();
```
```

**Key backend features:**

1. **Backend feature flag check**: Validates the feature flag on every resolver call
2. **User-specific storage**: Each user has their own bookmark list stored as `bookmarks_${accountId}`
3. **Toggle logic**: Adds or removes page IDs from the bookmark array
4. **Security**: Feature flag acts as a circuit breaker - if disabled, no storage operations occur

### Update index.js

Ensure your `src/index.js` exports the resolver handler:

```
```
1
2
```



```
// src/index.js
export { handler } from './resolvers';
```
```

## Step 4: Deploy and install your app

Deploy and test your app:

1. **Deploy your app:**
2. **Install in development:**

   ```
   ```
   1
   2
   ```



   ```
   forge install --upgrade
   ```
   ```
3. When prompted, select your Confluence site.

## Step 5: Test your bookmark feature

### Add the macro to a page

1. **Open Confluence** and navigate to any page (or create a new one)
2. **Edit the page** (click the pencil/edit icon)
3. **Insert the macro**:
   * Type `/` to open the macro menu
   * Search for **"Page Bookmarks"** (your macro title)
   * Click to insert it
4. **Save the page**

### Test basic functionality

With the feature flag enabled (Pass: 100%), you should see:

1. **Bookmark button**: "Bookmark" with an empty star icon (grey default appearance)
2. **Green "Saved" badge**: Appears when you bookmark the page

**Test the bookmark:**

1. Click the "Bookmark" button → It changes to "Bookmarked" with a filled star icon and turns blue
2. Green "Saved" badge appears next to the button
3. Refresh the page → Bookmark status persists (button remains blue with "Bookmarked" text)
4. Click again → Bookmark is removed, button returns to grey "Bookmark" state

**Test on multiple pages:**

1. Navigate to a different Confluence page
2. Add the same macro
3. Each page should have independent bookmark status

### Test feature flag toggle

Now test the feature flag control:

#### Disable the feature

1. Go to [Developer Console](https://developer.atlassian.com/console)
2. Select your app → **Manage** → **Feature flags**
3. Click on `enable_page_bookmarks`
4. Change configuration:
5. **Save**

#### Verify the feature is hidden

1. Go back to your Confluence page
2. **Hard refresh**: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
3. You should **only see**: "The bookmark feature is controlled by a feature flag. Enable it in Developer Console to activate."
4. The bookmark button is **completely hidden**

#### Re-enable the feature

1. Go back to Developer Console
2. Change `enable_page_bookmarks`:
3. **Save**
4. Refresh Confluence page
5. Bookmark feature reappears!

## Next steps

Congratulations! You've successfully built a page bookmarking feature controlled by feature flags. Here's what to explore next:

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

**You're now ready to build feature-flagged apps in Confluence!** This bookmark feature demonstrates the power of feature flags for safe, controlled rollouts of new functionality.

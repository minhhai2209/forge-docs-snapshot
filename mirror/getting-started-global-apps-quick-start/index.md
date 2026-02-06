# Quick start: Build a global app

EXPERIMENTAL

**EXPERIMENTAL:** Global UI Kit components are currently in an experimental phase. The APIs and features are subject to change without notice and are not recommended for production use. Use these components for testing and feedback purposes only.

Global apps deliver a full-page experience inside Confluence or Jira using full page modules ([`confluence:fullPage`](/platform/forge/manifest-reference/modules/confluence-full-page/) or [`jira:fullPage`](/platform/forge/manifest-reference/modules/jira-full-page/)) and the [Global UI Kit component](/platform/forge/ui-kit/components/global/). Unlike embedded modules that live inside existing pages (such as issue panels or page macros), a global app gives you a full page with complete layout control, app-wide context, access from the Apps menu or URL, routing for multiple views, and custom navigation—suitable for custom dashboards, admin tools, or other full-page workflows.

This guide walks you through building your first global app: creating the app, building the frontend with header, sidebar and main content, and deploying to see it in action.

## Before you begin

Make sure you have the following:

* Latest `@forge/react`: 11.10.0 or later. To update, run `npm install @forge/react@latest --save` in your app directory.
* Latest `@forge/cli`: 12.13.1 or later. To update, run `npm install -g @forge/cli@latest` on the command line.
* Node.js version 20.x or 22.x (LTS release)
* A Jira or Confluence site where you can install and test your app
* Basic knowledge of React and JavaScript, plus understanding of Forge modules and resolvers

### Verify your setup

Check your Forge CLI version:

Update the CLI to the latest version:

```
```
1
2
```



```
npm install -g @forge/cli@latest
```
```

Ensure you have the latest version of UI Kit:

```
```
1
2
```



```
npm install @forge/react@latest --save
```
```

## Step 1: Create your app

1. Navigate to the directory where you want to create the app.
2. Create your app by running:
3. Select or create a Developer Space.
4. Enter a name for your app (for example, **my-global-app**).
5. Select **Confluence** or **Jira** as the product.
6. Select the **UI Kit** category.
7. Select the **confluence-full-page** or **jira-full-page** template.
8. Change to the app subdirectory:

This creates a new app with all the files you need to build a global app.

## Step 2: Review the manifest (optional)

The template created a `manifest.yml` file with everything you need. You can customize or add the following if you want:

* **`title`**: The app title that appears in the header and apps menu
* **`icon`**: The logo that appears in the header and apps menu
* **`routePrefix`**: URL path for your app (default: hello-world)

The manifest already includes:

* A full page module (`confluence:fullPage` or `jira:fullPage`)
* Frontend resource pointing to `src/frontend/index.jsx`
* Basic permissions for user context

You can skip this step and come back later if needed.

## Step 3: Build your app layout

Open `src/frontend/index.jsx` and replace the entire file with:

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Global, Text, Heading, Box } from '@forge/react';

const App = () => {
  return (
    <Global>
      <Global.Sidebar>
        <Global.LinkMenuItem label="Dashboard" href="" />
        <Global.LinkMenuItem label="Reports" href="reports" />
        <Global.LinkMenuItem label="Settings" href="settings" />
      </Global.Sidebar>
      
      <Global.Main>
        <Box padding="space.300">
          <Heading size="large">Welcome to your global app!</Heading>
          <Text>You now have a full-page app with header, sidebar, and main content area.</Text>
        </Box>
      </Global.Main>
    </Global>
  );
};

export default ForgeReconciler.render(<App />);
```
```

This creates a complete layout with:

* **Header**: Shows your app title and icon at the top
* **Sidebar**: Navigation menu on the left
* **Main content**: Your app's primary content area

## Step 4: Deploy and install

1. Deploy your app:

   ```
   ```
   1
   2
   ```



   ```
   forge deploy -e development
   ```
   ```
2. Install it to your site:

   ```
   ```
   1
   2
   ```



   ```
   # For Confluence
   forge install --site <your-site>.atlassian.net --product confluence -e development

   # For Jira
   forge install --site <your-site>.atlassian.net --product jira -e development
   ```
   ```

   Install the app in the product corresponding to the full page module you selected. If using `jira:fullPage`, install in Jira. If using `confluence:fullPage`, install in Confluence.
3. Get your app's URL by running:

   ```
   ```
   1
   2
   ```



   ```
   forge environments list
   ```
   ```

   Full page modules can be accessed using this URL format:

```
```
1
2
```



```
https://<your-site>.atlassian.net/forge-apps/a/<app-id>/e/<forge-environment-id>/r/<route-prefix>/<app-route>
```
```

**Where to find each value:**

* **`<your-site>`**: Your site name
* **`<app-id>`**: The UUID from your `app.id` in `manifest.yml` (if in ARI format like `ari:cloud:ecosystem::app/UUID`, use only the UUID section)
* **`<forge-environment-id>`**: The UUID of the environment that the app is installed on.
  Run `forge environments list` to find the UUID of the desired environment.
* **`<route-prefix>`**: Defined in your manifest under `routePrefix`
* **`<app-route>`**: Optional - if your app code contains routing, it will appear under the `<app-route>` section of the URL.

**Example:**

```
```
1
2
```



```
https://example.atlassian.net/forge-apps/a/21e590df-79e6-40dd-9ee4-ba2c7b678f26/e/9f699e8b-33f1-4fa7-bd48-c5fdc44fa4c2/r/ui-kit
```
```

## Step 5: View your app

Access your app in one of these ways:

1. **App switcher**: Click the app switcher icon and select your app name
2. **Direct URL**: Use the URL from the previous step

You should see your app with:

* A header showing your provided app title and logo
* A sidebar with Dashboard, Reports, and Settings menu items
* Main content area with a welcome message

For more information about accessing full page modules, see [Accessing Confluence full page module](/platform/forge/manifest-reference/modules/confluence-full-page/#accessing-confluence-full-page-module) or [Accessing Jira full page module](/platform/forge/manifest-reference/modules/jira-full-page/#accessing-jira-full-page-module).

## Next steps

Now that you have a basic global app running, you can:

**Add backend functionality:**

* Create resolvers to fetch data from Jira or Confluence APIs
* Use Forge Storage to persist app data
* Handle user interactions with backend logic

**Enhance your app:**

* Add routing to create multiple views
* Build forms and interactive components
* Integrate with third-party APIs
* Add authentication and permissions

**Learn by example:**

* Follow the [Chronicle tutorial](/platform/forge/chronicle-tutorial/) to build a complete work tracking app with CRUD operations, search, and API integrations

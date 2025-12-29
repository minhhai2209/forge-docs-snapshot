# Build a dashboard app with the Confluence full page module

The [Confluence full page module](/platform/forge/manifest-reference/modules/confluence-full-page) allows you to create fully customized app experiences that occupy the entire web page, providing ample space to deliver UI for a broader range of use cases, such as specialized content views or internal tools that reflect your own branding.

This tutorial will walk you through creating a Forge app for Confluence using the full page module that displays a dashboard with interactive charts and user information. You'll learn how to configure the manifest, build the frontend using either UI Kit or Custom UI, integrate with Confluence APIs, and deploy your app.

At the end of this tutorial, you'll have created an app using the full page module that displays:

* A monthly usage dashboard with an interactive bar chart
* Period selection buttons to toggle between Q1 and Q2 data
* Current user information fetched from the Confluence API

[Example app

Full source code for this tutorial, including UI Kit and Custom UI implementations.](https://bitbucket.org/atlassian/full-page-module-apps/src/main/Confluence-full-page-module-examples/)

## Before you begin

Make sure you have the following:

* The latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.
* If you are using UI Kit, make sure you have installed the latest version of UI Kit before you begin deploying your app.
  Navigate to the top-level directory of the app and run `npm install @forge/react@latest --save` on the command line.
* An existing Forge app. If you don't have one, create a new app using `forge create` and select the *confluence-global-page* template.

## Step 1: Configure the manifest

Update your `manifest.yml` to add the `confluence:fullPage` module. The key differences from `confluence:globalPage` are:

* Replace `confluence:globalPage` with `confluence:fullPage`
* Replace `route` with `routePrefix`
* `title` is optional for the full page module
* For UI Kit, ensure `render: native` is set

Your `manifest.yml` should look like the following:

```
```
1
2
```



```
modules:
  confluence:fullPage:
    - key: my-full-page-module
      resource: main
      render: native
      resolver:
        function: resolver
      routePrefix: ui-kit
      title: My full page module # Optional
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: "<your app id>"
  runtime:
    name: nodejs24.x
permissions:
  scopes:
    - read:confluence-user
```
```

## Step 2: Configure the app code

Add the following code into the frontend file of your app.

Place this code inside the file `src/frontend/index.jsx`.

```
```
1
2
```



```
import React, { useState, useEffect } from "react";
import ForgeReconciler, { Box, Stack, Heading, Text, BarChart, Button, Inline, Image, xcss } from "@forge/react";
import { requestConfluence } from "@forge/bridge";

const chartContainerStyle = xcss({
  maxWidth: "600px",
});

const App = () => {
  const [selectedPeriod, setSelectedPeriod] = useState("Q1");
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Dashboard usage data for different periods
  const q1Data = [
    { month: 'Jan', usage: 45 },
    { month: 'Feb', usage: 52 },
    { month: 'Mar', usage: 48 },
  ];

  const q2Data = [
    { month: 'Apr', usage: 61 },
    { month: 'May', usage: 55 },
    { month: 'Jun', usage: 67 },
  ];

  const chartData = selectedPeriod === "Q1" ? q1Data : q2Data;

  // Fetch current user information from Confluence API
  const fetchUserInfo = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await requestConfluence('/wiki/rest/api/user/current');
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API error: ${response.status} - ${errorText}`);
      }
      const data = await response.json();
      setUserInfo(data);
    } catch (err) {
      setError(`Failed to fetch user info: ${err.message}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserInfo();
  }, []);

  return (
    <Box padding="space.400">
      <Stack space="space.400">
        <Stack space="space.200">
          <Heading size="xlarge">Dashboard</Heading>
          <Text>Monthly usage overview</Text>
        </Stack>

        <Inline space="space.200">
          <Button 
            appearance={selectedPeriod === "Q1" ? "primary" : "default"}
            onClick={() => setSelectedPeriod("Q1")}
          >
            Q1
          </Button>
          <Button 
            appearance={selectedPeriod === "Q2" ? "primary" : "default"}
            onClick={() => setSelectedPeriod("Q2")}
          >
            Q2
          </Button>
        </Inline>

        <Stack space="space.300">
          <Box xcss={chartContainerStyle}>
            <BarChart
              data={chartData}
              xAccessor="month"
              yAccessor="usage"
            />
          </Box>

          <Box padding="space.200">
            <Stack space="space.100">
              <Text>Current period: {selectedPeriod}</Text>
              <Text>Total usage: {chartData.reduce((sum, item) => sum + item.usage, 0)}</Text>
            </Stack>
          </Box>
        </Stack>

        <Box padding="space.400">
          <Stack space="space.300">
            <Heading size="medium">Current User Information</Heading>
            {loading && <Text>Loading user info...</Text>}
            {error && <Text>{error}</Text>}
            {!loading && !error && userInfo && (
              <Box padding="space.300" xcss={xcss({
                borderWidth: "border.width",
                borderStyle: "solid",
                borderColor: "color.border",
                borderRadius: "border.radius.300",
              })}>
                <Stack space="space.200">
                  <Text>
                    <Text weight="bold">Name:</Text> {userInfo.displayName}
                  </Text>
                  {userInfo.email && (
                    <Text>
                      <Text weight="bold">Email:</Text> {userInfo.email}
                    </Text>
                  )}
                  {userInfo.accountId && (
                    <Text>
                      <Text weight="bold">Account ID:</Text> {userInfo.accountId}
                    </Text>
                  )}
                  {userInfo.profilePicture && (
                    <Box padding="space.200">
                      <Image 
                        src={userInfo.profilePicture.path} 
                        alt="Profile" 
                        width="48px"
                        height="48px"
                      />
                    </Box>
                  )}
                </Stack>
              </Box>
            )}
          </Stack>
        </Box>
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

**API permissions**: Both UI Kit and Custom UI examples use `requestConfluence` to fetch the current user's information. Make sure your `manifest.yml` includes the required scope:

```
```
1
2
```



```
permissions:
  scopes:
    - read:confluence-user
```
```

**Note**: When using `requestConfluence` from Custom UI or UI Kit, classic scopes (like `read:confluence-user`) are recommended over granular scopes for better compatibility.

You'll need to redeploy and reinstall your app with `forge install -upgrade` after adding scopes.

## Step 3: Deploy and install your app

If you are using UI Kit, make sure you have installed the latest version of UI Kit
before you begin deploying your app. Navigate to the top-level directory of the app
and run `npm install @forge/react@latest --save` on the command line.

If you are using Custom UI, each time you run the `forge deploy` command, make sure you navigate to `static/hello-world`
and run `npm run build` beforehand.

To use your app, it must be installed onto an Atlassian site. The
`forge deploy` command builds, compiles, and deploys your code; it'll also report any compilation errors.
The `forge install` command then installs the deployed app onto an Atlassian site with the
required API access.

You must run the `forge deploy` command before `forge install` because an installation
links your deployed app to an Atlassian site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

**Install/upgrade**: Run `forge install --upgrade` if you've changed permissions

**Installing to different environments**: To deploy your app to a different environment, use the `-e` flag to specify the environment.
For example, the following command will deploy to production environment: `forge deploy -e production`.

If you encounter errors during testing, check the browser console for detailed error messages and refer to the [Troubleshooting](#troubleshooting) section below.

## Step 4: Access the full page module

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

## Troubleshooting

| Issue | Solution |
| --- | --- |
| The route is displaying a blank screen instead of my app | 1. Open your browser's developer console (F12 or right-click → Inspect → Console tab). 2. Look for JavaScript errors that may be preventing the app from rendering. 3. Check that your frontend code is correctly deployed by verifying the latest deployment timestamp. 4. Ensure your app code matches the example in Step 2 and that all imports are correct. |
| The app is displaying the error: `You don't have sufficient permissions to load this app`. | 1. Ensure you are logged into an account that has access to the Confluence site. 2. Verify that the app is installed on your site by checking the site admin panel or running `forge install` again. 3. If you're not the site admin, ask your site administrator to grant you access to the app. 4. Check that you're accessing the correct site URL where the app is installed. |
| The app is displaying the error: `An error has occurred in loading this app`. | 1. Verify your route URL format matches: `https://<your-site>.atlassian.net/forge-apps/a/<app-id>/e/<forge-environment-id>/r/<route-prefix>/<app-route>`    * Check that `<app-id>` matches the UUID from your `app.id` in `manifest.yml` (extract just the UUID if it's in ARI format).    * Verify `<route-prefix>` matches the value defined in your manifest under `confluence:fullPage` → `routePrefix`.    * Ensure `<forge-environment-id>` is correct. Run `forge environments list` to find the UUID for the desired environment. 2. Verify your app is deployed and installed:    * Check deployment status: `forge deploy --non-interactive -e development`    * Verify installation: `forge install --non-interactive --site <your-site> --product confluence --environment development` 3. Ensure your app manifest includes the `confluence:fullPage` module with all required properties. 4. Check that you're accessing the app from the site where it's installed. |
| The command `forge deploy` is throwing an error for `confluence:fullPage`. | 1. Verify your manifest syntax is correct by running `forge lint`. 2. Ensure all mandatory properties are included for [confluence:fullPage](/platform/forge/manifest-reference/modules/confluence-full-page):    * `key`    * `resource`    * `routePrefix`    * `render` (for UI Kit) 3. Update your Forge CLI to the latest version: `npm install -g @forge/cli@latest` 4. Ensure you have at least Forge CLI version 12.7.1. Check your version with `forge version`. 5. Review the error message for specific details about missing or invalid properties. |
| I can't find my app's route URL | 1. Locate your `app-id`: Open `manifest.yml` and find the UUID in `app.id`. If it's in ARI format (`ari:cloud:ecosystem::app/UUID`), extract just the UUID part. 2. Find your `route-prefix`: Check the value under `confluence:fullPage` → `routePrefix` in your manifest. 3. Get your environment ID: Run `forge environments list` to find the environment ID for your deployment. 4. Construct the URL: `https://<your-site>.atlassian.net/forge-apps/a/<app-id>/e/<forge-environment-id>/r/<route-prefix>/`. |

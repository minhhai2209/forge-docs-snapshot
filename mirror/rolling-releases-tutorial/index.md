# Create an app supporting rolling releases

Forge rolling releases is available through Forge's Early Access Program (EAP). This feature is currently only available in Jira and Confluence.

EAP grants selected users early testing access for feedback. APIs and features in EAP are experimental, unsupported, and subject to change without notice. To participate in the rolling releases EAP, [sign up here](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18974).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/).

This tutorial walks you through onboarding your app to rolling releases, using the frontend and backend permissions SDK, and testing how your app behaves in a decoupled state.

By completing this guide, you will build an app for which you can upgrade only the code version in your test installation.

## Before you begin

Before you begin, ensure you have the following:

* A configured Forge development environment ([Getting Started Guide](/platform/forge/getting-started/))
* Access to an Atlassian site for app installation (create one if needed)
* You have been onboarded to the [EAP](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18974)
* Install the `next` version of CLI and authenticate

  ```
  1
  2
  3
  4
  5
  6
  7
  8
  # Install next (pre-release) version of CLI
  npm i -g @forge/cli@next

  # Ensure you are authenticated by running 
  forge whoami

  # If not authenticated then login to authenticate
  forge login
  ```

---

## Create a new Forge app

Use the Forge CLI to create your app. In this example, we'll name it `rolling-release-confluence`:

1. Authenticate with Forge if you haven't already:
2. Create your app:

   ```
   ```
   1
   2
   ```



   ```
   forge create
   # ? Enter a name for your app: rolling-release-confluence
   # ? Select an Atlassian app or platform tool: Confluence
   # ? Select a category: UI Kit
   # ? Select a template: confluence-macro
   ```
   ```
3. Raise a request to enable rolling releases for your test app.
4. Navigate to your app directory:

   ```
   ```
   1
   2
   ```



   ```
   cd rolling-release-confluence
   ```
   ```

## Enable rolling releases for the app

Update the permissions in the app manifest to add `enforcement: app-managed`.

1. In the app's top-level directory, open the `manifest.yml` file.
2. Add the `permissions` section with `enforcement: app-managed`:

Your `manifest.yml` file should look like the following:

```
```
1
2
```



```
modules:
  macro:
    - key: rolling-release-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: Hello World!
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64
permissions:
  # Enable rolling releases for the app
  enforcement: app-managed
```
```

The `enforcement: app-managed` setting enables rolling releases for your app, allowing you to decouple code updates from permission approvals.

## Display the installed app version

Update your app code to display the currently installed app version. This helps verify which version is running.

1. Open `src/frontend/index.jsx`.
2. Update the imports to include `view` from `@forge/bridge`:

   ```
   ```
   1
   2
   ```



   ```
   import { invoke, view } from '@forge/bridge';
   ```
   ```
3. Add state to store the context and a `useEffect` to fetch it:

   ```
   ```
   1
   2
   ```



   ```
   const [context, setContext] = useState({});

   useEffect(() => {
     const fetchContext = async () => {
       setContext(await view.getContext());
     };
     fetchContext();
   }, []);
   ```
   ```
4. Display the app version in the return statement:

Your complete `src/frontend/index.jsx` should look like this:

```
```
1
2
```



```
import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Text } from '@forge/react';
import { invoke, view } from '@forge/bridge';

const App = () => {
  const [data, setData] = useState(null);
  const [context, setContext] = useState({});

  useEffect(() => {
    invoke('getText', { example: 'my-invoke-variable' }).then(setData);
  }, []);

  useEffect(() => {
    const fetchContext = async () => {
      setContext(await view.getContext());
    };
    fetchContext();
  }, []);

  return (
    <>
      <Text>Hello world!</Text>
      <Text>Installed app version: {context.appVersion}</Text>
      <Text>{data ? data : 'Loading...'}</Text>
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

## Deploy and install the app

1. Deploy the app by running:
2. Install the app in your test instance:

   Follow the prompts to select your Confluence site.
3. View the app in Confluence by creating or editing a page and inserting your macro.

When viewing the app you should see the major version of the app installed (e.g., version 2.0.0).

## Add a new scope to the app

Now we'll add a permission scope to demonstrate rolling releases behavior.

1. Open `manifest.yml`.
2. Add a `scopes` section under `permissions` with the `read:space:confluence` scope:

```
```
1
2
```



```
permissions:
  enforcement: app-managed
  scopes:
    # added a new scope
    - read:space:confluence
```
```

## Call the Confluence API

Update your app to fetch and display Confluence spaces.

1. Open `src/frontend/index.jsx`.
2. Update your imports to include `CodeBlock` from `@forge/react` and `requestConfluence` from `@forge/bridge`:

   ```
   ```
   1
   2
   ```



   ```
   import ForgeReconciler, { Text, CodeBlock } from '@forge/react';
   import { invoke, view, requestConfluence } from '@forge/bridge';
   ```
   ```
3. Add a `ShowSpaces` component that fetches all spaces:

```
```
1
2
```



```
// Added Component to fetch all spaces and render them
const ShowSpaces = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [spaces, setSpaces] = useState([]);

  useEffect(() => {
    const fetchSpaces = async () => {
      try {
        setIsLoading(true);
        const response = await requestConfluence(`/wiki/api/v2/spaces`, {
          headers: {
            Accept: "application/json",
          },
        });
        const data = await response.json();
        setSpaces(data.results || []);
      } catch (error) {
        console.error('Failed to fetch spaces:', error);
        setSpaces([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSpaces();
  }, []);

  if (isLoading) {
    return <Text>Loading spaces...</Text>;
  }

  return <CodeBlock text={JSON.stringify(spaces, undefined, 2)} language="json" />;
};
```
```

4. Update the `App` component to include `ShowSpaces`:

```
```
1
2
```



```
return (
  <>
    <Text>Hello world!</Text>
    <Text>Installed app version: {context.appVersion}</Text>
    {/* Show all the spaces in the instance */}
    <ShowSpaces />
    <Text>{data ? data : 'Loading...'}</Text>
  </>
);
```
```

## Deploy the app

Deploy the app with the new scope:

At this point, your app is in a state where the latest version requires new permissions. App installations will invoke the older version until admins manually update the app and grant permissions.

Let's see how rolling releases will help us handle such upgrades.

## Check for app permissions

Use the `usePermissions` hook in the app frontend to gracefully handle missing permissions.

1. Open `src/frontend/index.jsx`.
2. Add `usePermissions` to your `@forge/react` imports:

   ```
   ```
   1
   2
   ```



   ```
   import ForgeReconciler, { Text, CodeBlock, usePermissions } from '@forge/react';
   ```
   ```
3. In the `App` component, add the `usePermissions` hook before the `useEffect` calls:

   ```
   ```
   1
   2
   ```



   ```
   // Check if read:space:confluence permission is granted
   const { hasPermission, isLoading: permissionsLoading } = usePermissions({
     scopes: ["read:space:confluence"],
   });
   ```
   ```
4. Update the return statement to conditionally render `ShowSpaces` based on permission status:

Your complete `src/frontend/index.jsx` should now look like this:

```
```
1
2
```



```
import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Text, CodeBlock, usePermissions } from '@forge/react';
import { invoke, view, requestConfluence } from '@forge/bridge';

// Added Component to fetch all spaces and render them
const ShowSpaces = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [spaces, setSpaces] = useState([]);

  useEffect(() => {
    const fetchSpaces = async () => {
      try {
        setIsLoading(true);
        const response = await requestConfluence(`/wiki/api/v2/spaces`, {
          headers: {
            Accept: "application/json",
          },
        });
        const data = await response.json();
        setSpaces(data.results || []);
      } catch (error) {
        console.error('Failed to fetch spaces:', error);
        setSpaces([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSpaces();
  }, []);

  if (isLoading) {
    return <Text>Loading spaces...</Text>;
  }

  return <CodeBlock text={JSON.stringify(spaces, undefined, 2)} language="json" />;
};

const App = () => {
  const [data, setData] = useState(null);
  const [context, setContext] = useState({});

  // Check if read:space:confluence permission is granted
  const { hasPermission, isLoading: permissionsLoading } = usePermissions({
    scopes: ["read:space:confluence"],
  });

  useEffect(() => {
    invoke('getText', { example: 'my-invoke-variable' }).then(setData);
  }, []);

  useEffect(() => {
    const fetchContext = async () => {
      setContext(await view.getContext());
    };
    fetchContext();
  }, []);

  return (
    <>
      {/* Update the text to signify a backwards compatible change that you wished to ship in older installations */}
      <Text>Hello new world!</Text>
      <Text>Installed app version: {context.appVersion}</Text>
      {permissionsLoading ? (
        <Text>Loading...</Text>
      ) : (
        /* Skip calling show spaces if permission is not granted */
        hasPermission && <ShowSpaces />
      )}
      <Text>{data ? data : "Loading..."}</Text>
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

We renamed `isLoading` to `permissionsLoading` to avoid naming conflicts with the `isLoading` state in the `ShowSpaces` component.

## Test code-only upgrade

Deploy the new version of the app:

To upgrade only the code version of the app in your installations, run the install command with the `code` upgrade flag:

```
```
1
2
```



```
forge install --upgrade code
```
```

This will upgrade only the code version of the app. The new `read:space:confluence` permission will **not** be approved.

Now when you view your app, you can see the new code version but fetching the spaces is skipped:

* The text changes from "Hello world!" to "Hello new world!"
* The app version shows the new version (e.g., 3.0.0)
* Spaces are **not** displayed because the permission is not granted

The app version received in context is the app **code version** (e.g., major version 3 in this case). To see the **permission version**, run:

The **Major version** in the table is the permission version for the installation. It should show as "Out-of-date" since the code version is newer.

This demonstrates rolling releases in action: your code updated without requiring admin approval for the new permission!

## Upgrade app permissions

To upgrade the permission version of the app on your test instance, run the forge install command with the upgrade flag:

```
```
1
2
```



```
forge install --upgrade
```
```

This will:

* Prompt for approval of the new `read:space:confluence` scope
* Upgrade the permission version to match the code version

After approval, refresh your app in Confluence and you should see:

* "Hello new world!" text
* The current app version
* A JSON list of all Confluence spaces (now that the permission is granted)

## Rollback to an older version

To help with testing, we've released a `--major-version` flag on the install command so that you can install an older version on your instance to test rolling releases.

You must uninstall the app before installing an older version.

1. Uninstall the app from the test instance:
2. Install the older version using the `--major-version` flag:

   ```
   ```
   1
   2
   ```



   ```
   forge install --major-version <major-version>
   ```
   ```

   For example, to install major version 2:

   ```
   ```
   1
   2
   ```



   ```
   forge install --major-version 2
   ```
   ```

After installing the older version, the app will revert to the previous code and permissions state.

## Next steps

Now that you've learned about rolling releases, consider:

* Adding more granular permission checks in your app using the [Permissions SDK](/platform/forge/runtime-reference/@forge/api/#usepermissions)
* Building apps that gracefully degrade functionality when permissions are missing
* Exploring [app versioning strategies](/platform/forge/environments-and-versions/) for your production apps

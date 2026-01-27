# Part 2: Call a Jira Service Management API

Using the `@forge/api` package, you'll learn how to make REST calls to an authenticated Jira Service Management endpoint.

## Make an API call

In this section, you'll modify your app to call the [Jira Service Management REST API](/cloud/jira/service-desk/rest/intro/#jira-cloud-platform-apis). Using the [requestJira](/platform/forge/apis-reference/ui-api-bridge/requestJira) function from the `@forge/bridge` package, you'll get the list of queues on a Jira Service Management queue page app in the form of an array and print the number of comments to the console.

The `@forge/bridge` package simplifies HTTP operations and contains other Forge APIs such as the
[Storage](/platform/forge/runtime-reference/storage-api/) and
[Properties](/platform/forge/runtime-reference/properties-api/) APIs.
For this tutorial, you'll also use the UI Kit hook
[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) to get context information about the Jira Service Management queues the app is on.

1. In the app's top-level directory make sure your tunnel is running:
2. Navigate to the `src/frontend` directory and open the `index.jsx` file. Import the `requestJira` from `@forge/bridge` package by adding the following to the top of the file:

   ```
   1
   import { requestJira } from '@forge/bridge';
   ```
3. Copy the following code to create a function that calls the Jira Service Management REST API by using the `requestJira` function:

   ```
   1
   2
   3
   4
   5
   const getJsmQueues = async (serviceDeskKey) => {
     const res = await requestJira(`/rest/servicedeskapi/servicedesk/${serviceDeskKey}/queue`);
     const data = await res.json();
     return data.values;
   };
   ```

   This function takes a `serviceDeskKey` to call the REST API with path `/rest/servicedeskapi/servicedesk/${serviceDeskKey}/queue`.

When you save the `index.jsx` file, the tunnel output in the terminal
will display a `permission-scope-required` error. To address this, you'll
need to add the required permissions first; this is covered later in the
[*Set required permissions*](#set-required-permissions) section.

4. We need to get the key of the service desk we are currently on, which is stored in the Atlassian app context.

   1. To get the current Atlassian app context, import the `useProductContext` hook from `@forge/react`:

      ```
      ```
      1
      2
      ```



      ```
      import ForgeReconciler, { Text, useProductContext } from '@forge/react';
      ```
      ```
   2. Modify the start of the `App` component so it automatically retrieves the context:

      ```
      ```
      1
      2
      ```



      ```
      const App = () => {
        const context = useProductContext();
      ```
      ```
5. Modify the start of the App function to add a `queues` variable to store the queues data:

   ```
   ```
   1
   2
   ```



   ```
   const App = () => {
     const context = useProductContext();

     // add these code to keep track of queues
     const [queues, setQueues] = React.useState();
     console.log(`Number of queues in your service desk project: ${queues?.length}`);
   ```
   ```
6. Add the following code inside `App`, below the `getJsmQueues` function, so it automatically runs when `context` finishes loading:

   ```
   ```
   1
   2
   ```



   ```
   React.useEffect(() => {
     if (context) {
       // extract the current service desk key from the context
       const serviceDeskKey = context.extension.project.key;

       getJsmQueues(serviceDeskKey).then(setQueues);
     }
   }, [context]);
   ```
   ```

   This code uses the service key to call `getJsmQueues`, then updates the data stored in `queues`

We recommend clearing the `src/frontend/index.jsx` file and replacing it with the provided code for error free results.

Your `index.jsx` file should look like the following:

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Text, useProductContext } from '@forge/react';
import { requestJira } from '@forge/bridge';

const App = () => {
  const context = useProductContext();

  // add these code to keep track of queues
  const [queues, setQueues] = React.useState();
  console.log(`Number of queues in your service desk project: ${queues?.length}`);

  const getJsmQueues = async (serviceDeskKey) => {
    const res = await requestJira(`/rest/servicedeskapi/servicedesk/${serviceDeskKey}/queue`);
    const data = await res.json();
    return data.values;
  };

  React.useEffect(() => {
    if (context) {
      // extract the current service desk key from the context
      const serviceDeskKey = context.extension.project.key;

      getJsmQueues(serviceDeskKey).then(setQueues);
    }
  }, [context]);

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

## Test your app

1. Create a new JSM service project, or open the one you created earlier.
2. Refresh the JSM queue page app.
3. Check the output of the app in your browser's developer console. The number of queues on the service desk displays as follows:

![The message displayed in the browser console](https://dac-static.atlassian.com/platform/forge/images/console-log-successful-jsm.png?_v=1.5800.1800)

## Set required permissions

Your app calls a remote resource; namely, the Jira Service Management REST API.
As such, you'll need to grant your app the right [permissions](/platform/forge/manifest-reference/permissions/). To do this, you'll need to add the required OAuth 2.0 scope to the app's manifest.

In the steps below, you'll do this by using the `forge lint` command. This command will automatically
add the required scope to your `manifest.yml` file (in this case, `read:jira-work`).

1. Run the following command:
2. Whenever you change permissions, you must upgrade the app's installation. Stop your tunnel process
   and run these commands to deploy and install your change:

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
3. Start the tunnel again:

## Enable usage analytics (optional)

If you haven't enabled usage analytics yet, we recommend you do so using following command:

```
```
1
2
```



```
forge settings set usage-analytics true
```
```

This command provides the consent required by Forge to collect data about your app's
deployments and installations (including error data). This, in turn, helps us monitor the
overall performance and reliability of Forge. The collected data also helps us
make better decisions on improving Forge's feature set and performance.

For information about how Atlassian collects and handles your data, read our
[Privacy Policy](https://www.atlassian.com/legal/privacy-policy).

## Next step

In the next tutorial, you'll learn how to make changes to your app's frontend using the
[UI Kit components](/platform/forge/ui-kit/components/) of Forge.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1800)](/platform/forge/build-a-hello-world-app-in-jira-service-management/)
[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1800)](/platform/forge/change-the-jira-service-management-frontend-with-the-ui-kit/)

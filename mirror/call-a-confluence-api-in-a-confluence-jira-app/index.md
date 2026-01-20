# Part 2: Call a Confluence API

This functionality is available through Forge's Early Access Program (EAP). To start building
Forge apps that are compatible with multiple Atlassian apps, you must be part of the EAP.
[Sign up to join the EAP](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18660).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. This functionality must not be used in customer
production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Using the `@forge/bridge` package, you'll learn how to make REST calls to an authenticated Confluence endpoint.

## Make an API call

In this section, you'll modify your app to call the Confluence REST API. Using the
[requestConfluence](/platform/forge/custom-ui-bridge/requestConfluence/) bridge method
from the `@forge/bridge` package, you'll get the comments on a Confluence page in an array and print the number of comments to the console.

The `@forge/bridge` package simplifies requests to Atlassian app REST APIs as well as other
javascript APIs to interact with Atlassian apps. For this tutorial, you'll also use the UI Kit hook
[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) to get context information about the Confluence page the app is on.

Modify your app’s code to call the Confluence REST API that gets the footer comments on a page. You’ll
use the returned array to count the number of footer comments and write it to the logs in your browser console.

1. In the app's top-level directory make sure your tunnel is running:
2. Go to the `src/frontend/index.jsx` file, replace it with the following code:

   ```
   ```
   1
   2
   ```



   ```
   // Import React and Forge UI Kit components/hooks
   import React from 'react';
   import ForgeReconciler, { Text, useProductContext } from '@forge/react';
   // Import the bridge method to call Confluence REST APIs
   import { requestConfluence } from '@forge/bridge';

   /**
   * Fetches footer comments for a given Confluence page.
   * @param {string} pageId - The ID of the Confluence page.
   * @returns {Promise<Array>} - Resolves to an array of comment objects.
   */
   const fetchCommentsForPage = async (pageId) => {
     // Call the Confluence REST API for footer comments
     const res = await requestConfluence(`/wiki/api/v2/pages/${pageId}/footer-comments`);
     const data = await res.json();
     return data.results;
   };

   const App = () => {
     // Get the current Atlassian app context (includes page info)
     const context = useProductContext();

     // State to store the array of footer comments
     const [comments, setComments] = React.useState();

     // Log the number of comments to the browser console for debugging
     console.log(`Number of comments on this page: ${comments?.length}`);

     // Fetch comments when the context is available (i.e., after loading)
     React.useEffect(() => {
       if (context) {
         // Extract the page ID from the context object
         const pageId = context.extension.content.id;
         // Fetch and store the comments
         fetchCommentsForPage(pageId).then(setComments);
       }
     }, [context]);

     // Render the UI: show the number of comments and a hello message
     return (
       <>
         <Text>Number of comments on this page: {comments?.length}</Text>
         <Text>Hello world!</Text>
       </>
     );
   };

   // Render the App component using ForgeReconciler
   ForgeReconciler.render(
     <React.StrictMode>
       <App />
     </React.StrictMode>
   );
   ```
   ```

   This code includes comments to help you quickly understand what each section does.

When you save the `index.jsx` file, the tunnel output in the terminal
will display a `permission-scope-required` error. To address this, you'll
need to add the required permissions first; this is covered later in the
[*Set required permissions*](#set-required-permissions) section.

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

## Test your app

1. Add a footer comment to the Confluence page that contains your macro. For example, a comment with *Hello from the comments*.
2. Refresh the Confluence page that contains your macro.
3. Check the developer console in your browser. The number of comments on the page displays as follows:

![The message displayed in the browser console](https://dac-static.atlassian.com/platform/forge/images/console-log-successful.png?_v=1.5800.1783)

The `requestConfluence` method inherits the Atlassian app permissions of the user that is interacting with the app. This can cause different API responses between different users in the same app.

## Set required permissions

Your app calls a remote resource; namely, the Confluence REST API.
As such, you'll need to grant your app the right [permissions](/platform/forge/manifest-reference/permissions/). To do this, you'll need to add the required OAuth 2.0 scope to the app's manifest.

You'll have to manually add the required scope permission into your `manifest.yml` file (in this case, `read:comment:confluence`):

1. At the bottom of the file, add the following code:

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     scopes:
       - read:comment:confluence
   ```
   ```
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

## Next step

In the next tutorial, you'll learn how to add support for Jira as an optional Atlassian app and make calls to the Jira REST API.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1783)](/platform/forge/build-an-app-compatible-with-confluence-and-jira/)
[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1783)](/platform/forge/add-support-for-jira-as-an-optional-atlassian-app)

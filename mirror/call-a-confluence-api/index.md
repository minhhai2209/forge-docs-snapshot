# Part 2: Call a Confluence API

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Dforge-call-a-confluence-api)

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
   1// Import React and Forge UI Kit components/hooks
   2import React from 'react';
   3import ForgeReconciler, { Text, useProductContext } from '@forge/react';
   4// Import the bridge method to call Confluence REST APIs
   5import { requestConfluence } from '@forge/bridge';
   6
   7/**
   8* Fetches footer comments for a given Confluence page.
   9* @param {string} pageId - The ID of the Confluence page.
   10* @returns {Promise<Array>} - Resolves to an array of comment objects.
   11*/
   12const fetchCommentsForPage = async (pageId) => {
   13  // Call the Confluence REST API for footer comments
   14  const res = await requestConfluence(`/wiki/api/v2/pages/${pageId}/footer-comments`);
   15  const data = await res.json();
   16  return data.results;
   17};
   18
   19const App = () => {
   20  // Get the current Atlassian app context (includes page info)
   21  const context = useProductContext();
   22
   23  // State to store the array of footer comments
   24  const [comments, setComments] = React.useState();
   25
   26  // Log the number of comments to the browser console for debugging
   27  console.log(`Number of comments on this page: ${comments?.length}`);
   28
   29  // Fetch comments when the context is available (i.e., after loading)
   30  React.useEffect(() => {
   31    if (context) {
   32      // Extract the page ID from the context object
   33      const pageId = context.extension.content.id;
   34      // Fetch and store the comments
   35      fetchCommentsForPage(pageId).then(setComments);
   36    }
   37  }, [context]);
   38
   39  // Render the UI: show the number of comments and a hello message
   40  return (
   41    <>
   42      <Text>Number of comments on this page: {comments?.length}</Text>
   43      <Text>Hello world!</Text>
   44    </>
   45  );
   46};
   47
   48// Render the App component using ForgeReconciler
   49ForgeReconciler.render(
   50  <React.StrictMode>
   51    <App />
   52  </React.StrictMode>
   53);
   54
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

![The message displayed in the browser console](https://dac-static.atlassian.com/platform/forge/images/console-log-successful.png?_v=1.5800.2303)

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
   3
   4
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
   3
   ```



   ```
   forge deploy
   forge install --upgrade
   ```
   ```
3. Start the tunnel again:

## Next step

In the next tutorial, you'll learn how to make changes to your app's frontend using the
[UI Kit components](/platform/forge/ui-kit/components/) of Forge.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.2303)](/platform/forge/build-a-hello-world-app-in-confluence/)
[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.2303)](/platform/forge/change-the-confluence-frontend-with-the-ui-kit)

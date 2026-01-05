# Part 3: Add support for Jira as an optional Atlassian app

This functionality is available through Forge's Early Access Program (EAP). To start building
Forge apps that are compatible with multiple Atlassian apps, you must be part of the EAP.
[Sign up to join the EAP](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18660).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. This functionality must not be used in customer
production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Now that you have set up your app with Confluence as the required Atlassian app, you can add support
for optional Atlassian apps to your app. In this case, we will be adding a Jira module and calling a Jira API.

## Add Jira as an optional Atlassian app to the manifest

To add support for optional Atlassian apps, you declare them in the `compatibility` section of
the `manifest.yml` file using `required: false`.
For this tutorial, we will be adding Jira:

```
1
2
3
4
5
6
7
app:
  id: '<app id>'
  compatibility:
    confluence:
      required: true
    jira:
      required: false
```

## Add a Jira module

Now, we will add a `jira:issuePanel` module to the manifest to
enable the app to display 'Hello world' on the Jira issue view page.

Copy the below code and paste it in the `modules` section of the `manifest.yml` file:

```
```
1
2
```



```
  jira:issuePanel:
    - key: hello-world-hello-world-issue-panel
      resource: main
      resolver:
        function: resolver
      render: native
      title: <your app name>
      icon: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
```
```

Your `manifest.yml` should now look like this:

```
```
1
2
```



```
modules:
  macro:
    - key: hello-world-app-hello-world
      resource: main
      render: native
      resolver:
        function: resolver
      title: Forge app for Mia
      description: Inserts hello world!
  jira:issuePanel:
    - key: hello-world-hello-world-issue-panel
      resource: main
      resolver:
        function: resolver
      render: native
      title: Forge app for Mia
      icon: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs24.x
  id: <your app id>
  compatibility:
    confluence:
      required: true
permissions:
  scopes:
    - read:comment:confluence
```
```

You can now run `forge deploy` to update the app with the new module.

## Make a Jira API call

In this section, you'll modify your app to call the Jira REST API. Using the [requestJira](/platform/forge/apis-reference/ui-api-bridge/requestJira) function from the `@forge/bridge` package, you'll get the comments on a Jira issue in the form of an array and print the number of comments to the console.

The `@forge/bridge` package simplifies HTTP operations and contains other Forge APIs such as the Storage and Properties APIs. For this tutorial, you'll also use the UI Kit hook
[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) to get context information about the Jira issue the app is on.

1. In the app's top-level directory make sure your tunnel is running:
2. Navigate to the `src/frontend` directory and open the `index.jsx` file. Import the `requestJira` from `@forge/bridge` package. Your imports from `@forge/bridge` should now look like:

   ```
   ```
   1
   2
   ```



   ```
   import { requestConfluence, requestJira } from '@forge/bridge';
   ```
   ```
3. Copy the following code to create a function that calls the Jira REST API by using the `requestJira` function:

   ```
   ```
   1
   2
   ```



   ```
   const fetchCommentsForIssue = async (issueIdOrKey) => {
     const res = await requestJira(`/rest/api/3/issue/${issueIdOrKey}/comment`);
     const data = await res.json();
     return data.comments;
   };
   ```
   ```

   This function takes an `issueIdOrKey` to call the REST API with path
   `/rest/api/3/issue/${issueIdOrKey}/comment`.

When you save the `index.jsx` file, the tunnel output in the terminal
will display a `permission-scope-required` error. To address this, you'll
need to add the required permissions first; this is covered later in the
[*Set required permissions*](#set-required-permissions) section.

4. We can get the `ID` of the issue we are currently on from the Atlassian app context which was previously added in [Part 2: Call a Confluence API](/platform/forge/call-a-xpa-confluence-api/).

   ```
   ```
   1
   2
   ```



   ```
   import ForgeReconciler, { Text, useProductContext } from '@forge/react';
   ```
   ```
5. Modify the `App` component to use `fetchCommentsForIssue` function, so it automatically runs when `context` finishes loading and updates the data stored in `comments`:

   ```
   ```
   1
   2
   ```



   ```
   React.useEffect(() => {
     if (context) {
       // extract page ID from the context
       const pageId = context.extension.content?.id;
       if (pageId) {
         fetchCommentsForPage(pageId).then(setComments);
       }
       // extract issue ID from the context
       const issueId = context.extension.issue?.id;
       if (issueId) {
         fetchCommentsForIssue(issueId).then(setComments);
       }
     }
   }, [context]);
   ```
   ```

This code checks if the context is being loaded onto a Confluence or Jira page. If a Jira issue is found, the issue ID
is passed to `fetchCommentsForIssue`, and then updates the data stored in `comments`.

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
import { requestConfluence, requestJira } from '@forge/bridge';

const fetchCommentsForPage = async (pageId) => {
  const res = await requestConfluence(`/wiki/api/v2/pages/${pageId}/footer-comments`);
  const data = await res.json();
  return data.results;
};

const fetchCommentsForIssue = async (issueIdOrKey) => {
  const res = await requestJira(`/rest/api/3/issue/${issueIdOrKey}/comment`);
  const data = await res.json();
  return data.comments;
};

const App = () => {
  const context = useProductContext();

  // add these code to keep track of comments
  const [comments, setComments] = React.useState();
  console.log(`Number of comments: ${comments?.length}`);

  React.useEffect(() => {
    if (context) {
      // extract page ID from the context
      const pageId = context.extension.content?.id;
      if (pageId) {
        fetchCommentsForPage(pageId).then(setComments);
      }

      // extract issue ID from the context
      const issueId = context.extension.issue?.id;
      if (issueId) {
        fetchCommentsForIssue(issueId).then(setComments);
      }
    }
  }, [context]);

  return (
    <>
      // This UI will be updated in the next part of this tutorial to display number of comments onto the screen
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

## Install your app onto Jira

You can now run the `forge deploy` and `forge install` commands to install your app onto Jira.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your ap by running the below command using `jira` as the Atlassian app with the `-p [Atlassian app]` flag:
3. When prompted, provide your site url.

Note that your app must always be installed into the required Atlassian app before you can
install it in other Atlassian apps.

## Test your app

1. Create a new Jira issue.
2. In the issue panel of that issue, select the Apps button and select your app from the list.

   ![Image of Cross-Context App in Jira](https://dac-static.atlassian.com/platform/forge/images/forge-getting-started-xpa-jira-initial-state.png?_v=1.5800.1742)
3. Add a comment to the Jira issue. For example, a comment with *Hello from the comments*.
4. Refresh the Jira issue view.
5. Check the output of the app in your browser's developer console. The number of comments on the issue displays as follows:

When you save the `index.jsx` file, the tunnel output in the developer console may display a `permission-scope-required` error. To address this, you'll need to add the required permissions first and this is covered in the next section.

## Set required permissions

Your app calls a remote resource; namely, the Jira REST API.
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

## Next step

In the next tutorial, you'll learn how to make changes to your app's frontend using the
[UI Kit components](/platform/forge/ui-kit/components/) of Forge.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1742)](/platform/forge/call-a-confluence-api-in-a-confluence-jira-app/)
[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1742)](/platform/forge/change-the-frontend-with-ui-kit-for-a-confluence-jira-app/)

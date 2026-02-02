# Use content actions to count the macros in a Confluence page

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Ddac-get-help%2Cforge-macros-in-the-page)

This tutorial describes how to create a Forge app that displays the number of macros in a Confluence
page. The app retrieves the body of the page, counts the number of macros, then displays the result
in a modal dialog. A user triggers the action from an entry in the more actions (...) menu.

The final app looks like the following:

![Confluence page showing a modal dialog with macros used in this page.](https://dac-static.atlassian.com/platform/forge/images/content-action-macro-count.gif?_v=1.5800.1808)

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development.
If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

To complete this tutorial, you need the following:

* The latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.

### Set up a cloud developer site

An Atlassian cloud developer site lets you install and test your app on
Atlassian apps including Confluence and Jira. If you don't have one yet, set it up now:

1. Go to <http://go.atlassian.com/cloud-dev> and
   create a site using the email address associated with your Atlassian account.
2. Once your site is ready, log in and complete the setup wizard.

You can install your app to multiple Atlassian sites. However, app
data won't be shared between separate Atlassian apps, sites,
or Forge environments.

The limits on the numbers of users you can create are as follows:

* Confluence: 5 users
* Jira Service Management: 1 agent
* Jira Software and Jira Work Management: 5 users

## Create your app

The app retrieves the body of the page, counts the number of macros, then displays the result in a
modal dialog.

1. Navigate to the directory where you want to create the app.
2. Create your app by running:
3. Enter a name for the app. For example, *macro-counter*.
4. Select the *UI kit* category, and then *Confluence* as the Atlassian app.
5. Select the *confluence-macro* template from the list.
6. Open the app directory to see the app files.

## Update the manifest

To register the functionality of your app, add `confluence:contentAction` and `function` modules to
the manifest. The `confluence:contentAction` module adds an entry to the more actions (...) menu,
with the value of `title`. The `function` module contains the logic to count and display the number
of macros.

1. In the app's top-level directory, open the `manifest.yml` file.
2. Replace the `macro` entry under `modules` with the following `confluence:contentAction`.

   ```
   ```
   1
   2
   ```



   ```
   confluence:contentAction:
     - key: macro-counter
       title: Macro count
       resource: main
       render: native
       resolver:
         function: resolver
   ```
   ```
3. Add the follow permissions to the end of `manifest.yml`

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     scopes:
       - 'read:page:confluence'
   ```
   ```

Your `manifest.yml` should look like the following, with your value for the app ID:

```
```
1
2
```



```
modules:
  confluence:contentAction:
    - key: macro-counter
      resource: main
      render: native
      resolver:
        function: resolver
      title: Macro Count
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
  id: '<your-app-id>'
permissions:
  scopes:
    - 'read:page:confluence'
```
```

## Build, deploy, and install

Build, deploy, and install the app to see it in your Confluence site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

## View the app

With the app installed, it's time to see the entry in the more actions (...) menu.

1. Navigate to your Confluence Cloud site, then open a page.
2. Select the more actions (...) menu.

You'll see the *Macro Count* entry from the app.

When you select the menu item you will see, the following modal.

![Confluence page showing a modal dialog with the default content from the macro count template](https://dac-static.atlassian.com/platform/forge/images/content-action-macro-count-initial.png?_v=1.5800.1808)

## Implement the front end

Add UI Kit components that render when a user views the app. You'll use a static value for the
number of macros in the page.

1. Start tunneling to view your local changes by running:
2. Open the `src/frontend/index.jsx` file.
3. Replace the contents of the file with:

   ```
   ```
   1
   2
   ```



   ```
   import React, {useEffect, useState} from 'react';
   // Import required components from UI Kit
   import ForgeReconciler, { Text, useProductContext } from '@forge/react';
   // Import required for calling resolver
   import { invoke } from '@forge/bridge';

   // You'll implement countMacros later 
   const countMacros = (data) => {
       return 10;
   };

   const App = () => {
       const [data, setData] = useState();
       const context = useProductContext();
       const pageId = context?.extension?.content?.id;

       useEffect(() => {
           if(pageId){
               // You'll implement getContent later
               invoke('getContent', { pageId }).then(setData);
           }
       }, [pageId]);

       const macroCount = countMacros(data);

       return (
           <Text>{`Number of macros on this page: ${macroCount}`}</Text>
       );
   };

   ForgeReconciler.render(
       <React.StrictMode>
           <App />
       </React.StrictMode>
   );
   ```
   ```
4. Refresh a Confluence page on your site, open the more actions (...) menu, and select **Macro Count**.

   A modal dialog displays with:

   ```
   ```
   1
   2
   ```



   ```
   Number of macros on this page: 10
   ```
   ```

In the code from this step:

* The import statement lists the components to use from the UI Kit. See [UI Kit components](/platform/forge/ui-kit/components/) to learn more about these components.
* `setData` awaits the asynchronous `getContent` function to complete. This function does not yet exist.
* See [UI Kit hooks](/platform/forge/ui-kit/hooks-reference/#useproductcontext) to learn more about `useProductContext`.
* The countMacros function returns the number of macros in the page. At this stage, the function always returns 10.

## Call the Confluence REST API

Turn the static app into a dynamic app by making an API call to Confluence to retrieve the contents
of the page.

1. In terminal, navigate to the app's top-level directory and install the runtime API package by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/api
   ```
   ```
2. Check the tunnel is still running. If it's not, start the tunnel again.
3. Open the `src/resolvers/index.js` file.
4. Get the contents of the page by replacing the `getContent` function with:

   ```
   ```
   1
   2
   ```



   ```
   import Resolver from '@forge/resolver';
   import api, { route } from '@forge/api';

   const resolver = new Resolver();

   resolver.define('getContent', async ({ payload }) => {
       const response = await api.asUser().requestConfluence(route`/wiki/api/v2/pages/${payload.pageId}?body-format=atlas_doc_format`);

       if (!response.ok) {
           const err = `Error while getContent with pageId ${payload.pageId}: ${response.status} ${response.statusText}`;
           console.error(err);
           throw new Error(err);
       }

       return await response.json();
   });

   export const handler = resolver.getDefinitions();
   ```
   ```
5. Count the number of macros by replacing the `countMacros` function with:

   ```
   ```
   1
   2
   ```



   ```
   const countMacros = (data) => {
       if (!data || !data.body || !data.body.atlas_doc_format || !data.body.atlas_doc_format.value) {
           return 0;
       }

       const { body: { atlas_doc_format: { value } } } = data;
       const { content: contentList } = JSON.parse(value);

       const macros = contentList.filter((content) => {
           return content.type = "extension";
       });

       return macros.length;
   };
   ```ƒ
   ```
   ```
6. Refresh the Confluence page, open the more actions (...) menu, and select **Macro count**.
   The modal dialog shows the number of macros in the page.

Edit the page to add macros (e.g. type /blog post) and select **Macro count** again to see the number update.

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work when you close
the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:

That’s it. You've built an app that retrieves the contents of a page, counts the number of macros,
then displays the result in a modal dialog.

## Next steps

Check out an example app, continue to one of the other tutorials, or read through the reference
pages to learn more.

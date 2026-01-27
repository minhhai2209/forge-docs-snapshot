# Use highlighted text in a Confluence Forge app

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Ddac-get-help%2Cforge-create-confluence-contextmenu-module)

This tutorial describes how to make a Forge app that uses highlighted text from a Confluence page.
You might use this technique in a dictionary app, a custom glossary, or any app that requires users
to highlight text on a page.

![Confluence context menu](https://dac-static.atlassian.com/platform/forge/images/context-menu.png?_v=1.5800.1800)

To create the app, you'll learn how to:

* Use the [confluence:contextMenu](https://developer.atlassian.com/platform/forge/manifest-reference/modules/confluence-context-menu/)
  module to add an item to the context menu dropdown, which appears when users highlight text on
  a published page.

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development.
If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

To complete this tutorial, you need the following:

* The latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.
* The latest version of UI Kit. To update your version, navigate to the app's top-level
  directory, and run `npm install @forge/ui@latest --save` on the command line.

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

Create an app starting from the macro template.

1. Navigate to the directory where you want to create the app.
2. Create an app by running:

   1. Enter a name for the app. For example, *show-selected-text*.
   2. Select the *UI Kit* category from the list.
   3. Select the *Confluence* app from the list.
   4. Select the *confluence-context-menu* template from the list.
3. Open the app directory to see the app files.

## Check the manifest

This app uses a `confluence:contextMenu` module. All apps that use this module appear in the dropdown
in the context menu.

1. In the app's top-level directory, open the `manifest.yml` file.

Your `manifest.yml` should look like the following, with your value for the app ID:

```
```
1
2
```



```
modules:
  confluence:contextMenu:
    - key: hello-world-context-menu
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
  id:
```
```

See [Manifest](/platform/forge/manifest-reference/) to learn more
about the manifest file.

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

With the app installed, you can see the new entry in the context menu.

1. Navigate to a page on your Confluence Cloud site.
2. Select any text on the page, and then hover over it. A menu should appear with the dropdown button on the right.
3. Click on the dropdwon button.

You'll see your app appear there.

## Implement the front end

Add UI elements that render when the app is called (when the user clicks on the menu item). You'll
use the [useProductContext](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-product-context/) UI Kit hook to get information about the selected text.

1. In terminal, navigate to the app's top-level directory and start tunneling to view your local changes
   by running:
2. Open the `src/frontend/index.jsx` file.
3. Replace the content of the file with:

   ```
   ```
   1
   2
   ```



   ```
   import React from 'react';
   import ForgeReconciler, { Text, Strong, useProductContext } from '@forge/react';

   const App = () => {
     const context = useProductContext();
     const selectedText = context?.extension.selectedText;

     return (
       <>
         <Text><Strong>Selected text</Strong></Text>
         <Text>{selectedText}</Text>
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
4. Open a Confluence page and select some text. When the menu appears, click the dropdown
   button and select your app.

   ![App displaying selected text](https://dac-static.atlassian.com/platform/forge/images/context-menu-highlighted-text.png?_v=1.5800.1800)

   In the code from this step:

   * The import statement lists the components and hooks that are used in the app.
     See [UI Kit components](/platform/forge/ui-kit/components/) and
     [UI Kit hooks](/platform/forge/ui-kit/hooks/hooks-reference/) for more information.
   * The `App` component renders app with selected text.
     * The const `selectedText` is retrieved from `useProductContext`.
     * The `Text` UI Kit component displays the selected text.

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work when you close
the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:

Now you know how to build a simple Forge app using the `confluence:contextMenu` module.

## Next steps

Review other documentation for more on how Forge works:

* See the [reference pages](/platform/forge/) for more information on what you
  can do with Forge.

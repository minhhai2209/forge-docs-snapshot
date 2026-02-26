# Part 3: Change the front end with UI Kit

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Dforge-change-the-confluence-frontend-with-the-ui-kit)

This section describes how to use tools in UI Kit, including [UI Kit components](/platform/forge/ui-kit/components/).
You'll use these components to build dynamic and interactive interfaces for your app's front end. When your app is complete, you'll learn how to continue monitoring the Forge environment using the `forge logs` command.

## Modify the user interface

The hello world app contains a `Text` component that displays 'Hello world!' on a Confluence page. In the UI kit,
this is represented by `<Text>Hello world!</Text>`.

When using multiple UI Kit components, you must wrap them in a fragment (`<>`) block because a function
can only return one top-level component. In the example below `<>` acts as a wrapper for
the other UI Kit components.

You’ll add a new component to display the number of comments on a page.

1. Start the tunnel by running:
2. Navigate to the `frontend` directory and open the `index.jsx` file.
3. Inside the `<>` tag, add the following before the first `Text` component:

   ```
   1
   2
   3
   <Text>
     Number of comments on this page: {comments?.length}
   </Text>
   ```
4. Refresh the Confluence page that contains your app.

Your `index.jsx` file should look like the following:

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Text, useProductContext } from '@forge/react';
import { requestConfluence } from '@forge/bridge';

const fetchCommentsForPage = async (pageId) => {
  const res = await requestConfluence(`/wiki/api/v2/pages/${pageId}/footer-comments`);
  const data = await res.json();
  return data.results;
};

const App = () => {
  const context = useProductContext();

  // add these code to keep track of comments
  const [comments, setComments] = React.useState();
  console.log(`Number of comments on this page: ${comments?.length}`);

  React.useEffect(() => {
    if (context) {
      // extract page ID from the context
      const pageId = context.extension.content.id;

      fetchCommentsForPage(pageId).then(setComments);
    }
  }, [context]);

  return (
    <>
      <Text>
        Number of comments on this page: {comments?.length}
      </Text>
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

Your app should display the number of comments on the page. You can add more top-level comments to
the page and refresh the page to see your app update. Your page should look like the following:

![The final app displays on a Confluence page](https://dac-static.atlassian.com/platform/forge/images/display-confluence-macro.png?_v=1.5800.1881)

## Specify the export view

When the page is exported to PDF, Word, or viewed in the page history, you can specify how the app should be displayed.
This is done by specifying an `adfExport` function, and referencing it in your app's `manifest.yml` file.

First let's write the function, which will return a representation of the macro in [Atlassian document format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/).

1. In your app's `src` directory, create a new file called `macroExport.js`, and open it.
2. To include the number of comments in the export view, fetch the comments on the page with the [@forge/api](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestconfluence/) package. First, install the required packages by running the following command from your app's top-level directory:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/api && npm install @atlaskit/adf-utils
   ```
   ```
3. Now, add the following to the top of your `macroExport.js` file:

   ```
   ```
   1
   2
   ```



   ```
   import api, { route } from '@forge/api';
   import { doc, p } from '@atlaskit/adf-utils/builders';
   ```
   ```
4. Next call the Confluence REST API to fetch the comments. Add the following function to the file:

   ```
   ```
   1
   2
   ```



   ```
   const fetchComments = async (pageId) => {
    const res = await api
      .asApp()
      .requestConfluence(route`/wiki/api/v2/pages/${pageId}/footer-comments`);
    const data = await res.json(); 
    return data.results;
   };
   ```
   ```
5. Now specify the actual export function, which returns [Atlassian document format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) (ADF).
   Here you can use the [adf-utils](https://atlaskit.atlassian.com/packages/editor/adf-utils) package to create the ADF. Add the following function to the file:

   ```
   ```
   1
   2
   ```



   ```
   export const exportFunction = async (payload) => {
     const pageId = payload.context.content.id;
     const comments = await fetchComments(pageId);

     return doc(
       p(`Number of comments on this page: ${comments.length}`),
       p(`Hello world! This is an export of type ${payload.exportType}.`)
     );
   }
   ```
   ```

   Notice that the function is consuming the `exportType` from the `payload` object.
   The valid `exportType` values are `pdf`, `word`, and `other`.

Your `macroExport.js` file should look like the following:

```
```
1
2
```



```
import api, {route} from '@forge/api';
import { doc, p } from '@atlaskit/adf-utils/builders';

const fetchComments = async (pageId) => {
  const res = await api
    .asApp()
    .requestConfluence(
      route`/wiki/api/v2/pages/${pageId}/footer-comments`);
  const data = await res.json();
  return data.results;
};

export const exportFunction = async (payload) => {
  const pageId = payload.context.content.id;
  const comments = await fetchComments(pageId);

  return doc(
    p(`Number of comments on this page: ${comments.length}`),
    p(`Hello world! This is an export of type ${payload.exportType}.`)
  );
}
```
```

## Reference the export function in the manifest

1. In the app’s top-level directory, open the `manifest.yml` file.
2. Under `macro`, add the following property:

   ```
   ```
   1
   2
   ```



   ```
   adfExport:
     function: export-key
   ```
   ```
3. Under `function`, add the following entry

   ```
   ```
   1
   2
   ```



   ```
   - key: export-key
      handler: macroExport.exportFunction
   ```
   ```

Once deployed, your macro should export as specified along with the rest of the Confluence page when exporting to pdf, word, or viewed in page history.

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work
when you close the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:
3. Refresh the page where your app is installed.

## View your app in the developer console

Once your app is deployed, it will appear in the [developer console](/console/myapps/).
From the console, you can [manage](/platform/forge/manage-your-apps/) and
[distribute](/platform/forge/distribute-your-apps/) your apps. You can also
[see how your app is performing](/platform/forge/view-app-metrics),
[view your app logs and installations](/platform/forge/view-app-logs-and-installations), and
[manage app alerts](/platform/forge/manage-app-alerts).

## Next steps

You now know enough to develop your own Forge apps. Learn more from our
[tutorials](/platform/forge/tutorials-and-guides/), [guides](/platform/forge/guides/),
[example apps](/platform/forge/example-apps/) or [reference pages](/platform/forge/manifest-reference/).

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1881)](/platform/forge/call-a-confluence-api/)

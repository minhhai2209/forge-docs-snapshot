# Part 2: Call a Jira API

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Ddac-get-help%2Cforge-call-a-jira-api)

Using the `@forge/bridge` package, you'll learn how to make REST calls to an authenticated Jira endpoint.

## Make an API call

In this section, you'll modify your app to call the Jira REST API. Using the [requestJira](/platform/forge/apis-reference/ui-api-bridge/requestJira) function from the `@forge/bridge` package, you'll get the comments on a Jira issue in the form of an array and print the number of comments to the console.

The `@forge/bridge` package simplifies HTTP operations and contains other Forge APIs such as the Storage and Properties APIs. For this tutorial, you'll also use the UI Kit hook
[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) to get context information about the Jira issue the app is on.

1. In the app's top-level directory make sure your tunnel is running:
2. Open the `src/frontend/index.jsx` and replace its contents with the following code:

   ```
   1
   2
   3
   4
   5
   6
   7
   8
   9
   10
   11
   12
   13
   14
   15
   16
   17
   18
   19
   20
   21
   22
   23
   24
   25
   26
   27
   28
   29
   30
   31
   32
   33
   34
   35
   36
   37
   38
   39
   40
   41
   42
   43
   import React from "react";
   // useProductContext hook retrieves current Atlassian app context
   import ForgeReconciler, { Text, useProductContext } from "@forge/react";
   // requestJira calls the Jira REST API
   import { requestJira } from "@forge/bridge";

   const App = () => {
     const context = useProductContext();

     // add the the 'comments' variable to store comments data
     const [comments, setComments] = React.useState();
     console.log(`Number of comments on this issue: ${comments?.length}`);

     // start of function that calls Jira REST API
     const fetchCommentsForIssue = async () => {
       // extract issue ID instead expecting one from function input
       const issueId = context?.extension.issue.id;
       // modify to take issueId variable
       const res = await requestJira(`/rest/api/3/issue/${issueId}/comment`);
       const data = await res.json();
       return data.comments;
     };

     React.useEffect(() => {
       if (context) {
         // extract issue ID from the context
         const issueId = context.extension.issue.id;
         // use the issue ID to call fetchCommentsForIssue(),
         // then updates data stored in 'comments'
         fetchCommentsForIssue().then(setComments);
       }
     }, [context]);

     // This UI will be updated in the next part of this tutorial
     // to display number of comments onto the screen
     return <Text>Hello world!</Text>;
   };

   ForgeReconciler.render(
     <React.StrictMode>
       <App />
     </React.StrictMode>
   );
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

## Test your app

1. Create a new Jira issue, or open the one you created earlier.
2. Add a comment to the Jira issue. For example, a comment with *Hello from the comments*.
3. Refresh the Jira issue view.
4. Check the output of the app in your browser's developer console. The number of comments on the issue displays as follows:

   ```
   ```
   1
   2
   ```



   ```
   Number of comments on this issue: 1
   ```
   ```

When you save the `index.jsx` file, the tunnel output in the developer console may display a `permission-scope-required` error. To address this, you'll need to add the required permissions first and this is covered in the next section.

## Next step

In the next tutorial, you'll learn how to make changes to your app's frontend using the
[UI Kit components](/platform/forge/ui-kit/components/) of Forge.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1801)](/platform/forge/build-a-hello-world-app-in-jira/)
[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1801)](/platform/forge/change-the-jira-frontend-with-the-ui-kit/)

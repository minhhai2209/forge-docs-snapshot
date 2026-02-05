# Part 3: Change the front end with UI Kit

This section describes how to use tools in UI Kit, including [UI Kit components](/platform/forge/ui-kit/components/).
You'll use these components to build dynamic and interactive interfaces for your app's front end. When your app is complete, you'll learn how to continue monitoring the Forge environment using the `forge logs` command.

## Modify the user interface

The hello world app contains a single Text component that displays 'Hello world!' in a Jira issue.
In the UI Kit, this is represented by `<Text>Hello world!</Text>`. You’ll update the component
to display the number of comments on an issue.

When using multiple UI Kit components, you must wrap them in a fragment (`<>`) block because
a function can only return one top-level component. In the example below `<>` acts as a wrapper
for the other UI Kit components.

1. In the app's top-level directory make sure your tunnel is running:
2. Open the `src/frontend/index.jsx`
3. Find the `<Text>Hello world!</Text>` line and following below it:

   ```
   1
   2
   3
   <Text>
     Number of comments on this issue: {comments?.length}
   </Text>
   ```

   Your `src/frontend/index.jsx` should look like this:

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
   44
   45
   46
   47
   48
   49
   50
   import React from 'react';
   // useProductContext hook retrieves current product context
   import ForgeReconciler, { Text, useProductContext } from '@forge/react';
   // requestJira calls the Jira REST API
   import { requestJira } from '@forge/bridge';

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

    return (
      <>
        // This UI will now render the value of `comments` variable
        <Text>Hello world!</Text>
        <Text>
          Number of comments on this issue: {comments?.length}
        </Text>
      </>
    );
   };

   ForgeReconciler.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
   );
   ```
4. Refresh the Jira issue view.

The app displays the number of comments in the issue panel. Add more comments and refresh the page to count them in your app. Your issue should look like the following:

![A Jira issue displaying the hello world forge app with comments counted](https://dac-static.atlassian.com/platform/forge/images/forge-getting-started-jira-final-state.png?_v=1.5800.1824)

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work
when you close the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:
3. Refresh the page where your app is installed.

## Check the logs

After you deploy your app, open your browser’s developer console to view app logs. Logs are created after the app loads, so you may need to refresh your page.

```
```
1
2
```



```
Number of comments on this issue: 1
```
```

Your logs are an important tool when debugging Forge apps. [Learn more about debugging](/platform/forge/debugging/).

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

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1824)](/platform/forge/call-a-jira-api/)

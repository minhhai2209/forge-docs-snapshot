# Part 4: Change the front end with UI Kit

This functionality is available through Forge's Early Access Program (EAP). To start building
Forge apps that are compatible with multiple Atlassian apps, you must be part of the EAP.
[Sign up to join the EAP](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18660).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. This functionality must not be used in customer
production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This section describes how to use tools in UI Kit, including [UI Kit components](/platform/forge/ui-kit/components/).
You'll use these components to build dynamic and interactive interfaces for your app's front end. When your app is complete, you'll learn how to continue monitoring the Forge environment using the `forge logs` command.

## Modify the user interface

Your hello world app contains a single Text component that displays 'Hello world!' in a Confluence page and Jira issue.
In UI Kit, this is represented by `<Text>Hello world!</Text>`. You’ll update the component
to display the number of comments posted.

When using multiple UI Kit components, you must wrap them in a fragment (`<>`) block because
a function can only return one top-level component. In the example below `<>` acts as a wrapper
for the other UI Kit components.

1. Start the tunnel by running:
2. Navigate to the `src/frontend` directory and open the `index.jsx` file.
3. Inside the `<>` tag, add the following after the first `Text` component:

   ```
   ```
   1
   2
   ```



   ```
   <Text>
     Number of comments: {comments?.length}
   </Text>
   ```
   ```
4. Refresh the Confluence page or the Jira issue view to see the changes.

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
      <Text>Hello world!</Text>
      <Text>
      Number of comments: {comments?.length}
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
```

In Confluence, your app should display the number of comments on the page. In Jira, your app should display the
number of comments in the issue panel. Add more comments and refresh the page to count them in your app.

Your Confluence page should look like the following:

![A Confluence page displaying the hello world forge app with comments counted](https://dac-static.atlassian.com/platform/forge/images/display-xpa-confluence-macro.png?_v=1.5800.1741)

Your Jira issue should look like the following:

![A Jira issue displaying the hello world forge app with comments counted](https://dac-static.atlassian.com/platform/forge/images/display-xpa-jira-issue-panel.png?_v=1.5800.1741)

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work
when you close the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:
3. Refresh the page where your app is installed.

## Check the logs

After you deploy your app, open your browser’s developer console to view app logs. Logs are created after the app loads, so you may need to refresh your page.

Your logs are an important tool when debugging Forge apps. [Learn more about debugging](/platform/forge/debugging/).

## View your app in the developer console

Once your app is deployed, it will appear in the [developer console](/console/myapps/).

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1741)](/platform/forge/add-support-for-jira-as-an-optional-atlassian-app/)

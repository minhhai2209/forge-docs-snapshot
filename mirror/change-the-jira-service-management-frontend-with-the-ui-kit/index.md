# Part 3: Change the front end with UI Kit

This section describes how to use tools in UI Kit, including [UI Kit components](/platform/forge/ui-kit/components/).
You'll use these components to build dynamic and interactive interfaces for your app's front end. When your app is complete, you'll learn how to continue monitoring the Forge environment using the `forge logs` command.

## Modify the user interface

The hello world app contains a single `Text` component that displays 'Hello world!' in a Jira Service Management QueuePage app. In the UI Kit,
this is represented by `<Text>Hello world!</Text>`.
You’ll update the component to display the number of queues on a service desk project.

When using multiple UI Kit components, you must wrap them in a fragment (`<>`) block because a function can only return one top-level component. In the example below `<>` acts as a wrapper for the other UI Kit components.

1. Start the tunnel by running:
2. Navigate to the `src` directory and open the `index.jsx` file.
3. Inside the `<>` tag, add the following code after the first `Text` component:

   ```
   1
   2
   3
   <Text> 
     Number of queues: {queues?.length} 
   </Text>
   ```
4. Refresh the Jira Service Management queues view.

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

     const getJsmQueues = async () => {
       // fetch Atlassian app context and extract service desk key
       const serviceDeskKey = context?.extension.project.key;

       // modify to take serviceDeskKey variable
       const res = await requestJira(`/rest/servicedeskapi/servicedesk/${serviceDeskKey}/queue`);
       const data = await res.json();
       return data.values;
     };

     React.useEffect(() => {
       if (context) {
         getJsmQueues().then(setQueues);
       }
     }, [context]);

     return (
       <>
         <Text>Hello world!</Text>
         <Text> 
           Number of queues: {queues?.length} 
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

   The app displays the number of queues in the queue page app in Jira Service Management. Add more queues and refresh the page to count them in your app. Your queue page app should look like the following:

   ![A Jira Service Management queue page app displaying the hello world with queues counted](https://dac-static.atlassian.com/platform/forge/images/forge-getting-started-jira-service-management-final-state.png?_v=1.5800.1837)

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work
when you close the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:
3. Refresh the page where your app is installed.

## Check the logs

After you deploy your app, open your browser’s developer console to view app logs. Logs are created after the app loads, so you may need to refresh your page.

You should have the following in your log:

```
```
1
2
```



```
Number of queues in your service desk project: 1
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

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1837)](/platform/forge/call-a-jira-service-management-api/)

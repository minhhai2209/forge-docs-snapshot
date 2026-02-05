# Part 3: Change the front end with UI Kit

This section describes how to use tools in UI Kit, including [UI Kit components](/platform/forge/ui-kit/components/).
You'll use these components to build dynamic and interactive interfaces for your app's front end. When your app is complete, you'll learn how to continue monitoring the Forge environment using the `forge logs` command.

## Modify the user interface

The hello world app renders two `Text` components in a Bitbucket repository panel.
The first `Text` component displays 'Hello world!'.
The second `Text` component displays the contents of the state variable `data` if it is defined,
otherwise it displays 'Loading...'. You’ll update the app to display the repository full name.

1. Start the tunnel by running:
2. Navigate to the `src/frontend` directory and open the `index.jsx` file.
3. After fetching the repository in the `useEffect` hook, store the repository in the `data` state variable.
4. Inside the `<></>` section, modify the second `Text` component:

   ```
   1
   <Text>{data ? `Repository full name: ${data.full_name}` : 'Loading...'}</Text>
   ```
5. Refresh the Bitbucket repository source page.

Your `src/frontend/index.jsx` file should look like the following:

```
```
1
2
```



```
import React, { useEffect, useState } from "react";
import ForgeReconciler, { Text } from "@forge/react";
import { invoke } from "@forge/bridge";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchRepoAndCommits = async () => {
      const repo = await invoke("fetchRepository");
      setData(repo)
      console.log(`Repository full name: ${repo.full_name}`);

      const commits = await invoke("fetchCommits", {
        commitsUrl: repo.links.commits.href,
      });
      console.log(`Number of commits: ${commits.values.length}`);
    };
    fetchRepoAndCommits();
  }, []);

  return (
    <>
      <Text>Hello world!</Text>
      <Text>{data ? `Repository full name: ${data.full_name}` : 'Loading...'}</Text>
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

You can view the completed app code in the [Bitbucket Forge Hello World repository](https://bitbucket.org/atlassian/bitbucket-forge-hello-world/src/main/).

## Close the tunnel and deploy the app

After confirming the app works locally, deploy the app so that it continues to work
when you close the tunnel.

1. Close your tunnel by pressing **Ctrl+C**.
2. Deploy your app by running:
3. Refresh the page where your app is installed.

## Check the logs

After you deploy your app, run the `forge logs` command to view app events. Logs are processed
after deployment, so you may need to wait a moment before running the command.

Check for new logs in your development environment by running:

Your logs should look something like the following:

```
```
1
2
```



```
INFO    2023-05-16T03:53:04.192Z 10bc425b-adee-47ff-b9e9-ea3c38ab22e2 Repository full name: workspace/repository
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

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1824)](/platform/forge/call-a-bitbucket-api/)

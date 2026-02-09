# Part 2: Call a Bitbucket API

This page introduces the [Forge Javascript APIs](/platform/forge/runtime-reference/).
Using the `@forge/api` and `@forge/bridge` package, you'll learn how to make REST calls to an authenticated Bitbucket endpoint
from the backend and frontend of your app.

## Make an API call using backend resolver function

In this section, you'll modify your app to call the Bitbucket REST API from your app's backend. Using the
[Atlassian app Fetch API](/platform/forge/runtime-reference/fetch-api/)
from the `@forge/api` package, you'll get the repository metadata and print the repository's full name to the console.

The `@forge/api` package simplifies HTTP operations and contains other Forge APIs such as the
[Storage](/platform/forge/runtime-reference/storage-api/) API.
For this tutorial, you’ll also use the context of a [Custom UI resolver](/platform/forge/runtime-reference/custom-ui-resolver/)
to get context information about the page the app is on.

1. In the app’s top-level directory, install the `@forge/api` package by running:
2. Restart your tunnel to use the new npm modules by running:

   Make sure your docker is running.
3. Navigate to the `src/resolvers` directory and open the `index.js` file. Import the `@forge/api`
   package by adding the following to the top of the file:

   ```
   1
   import api, { route } from "@forge/api";
   ```
4. In the same file, copy the following code to create a resolver function that calls
   the Bitbucket REST API by using the `@forge/api` package:

   ```
   ```
   1
   2
   ```



   ```
   resolver.define("fetchRepository", async ({ context }) => {
     const workspaceId = context.workspaceId;
     const repositoryId = context.extension.repository.uuid;

     console.log(`Fetching repository ${workspaceId}/${repositoryId}`)

     const res = await api
       .asApp()
       .requestBitbucket(
         route`/2.0/repositories/${workspaceId}/${repositoryId}`
       );

     return res.json();
   });
   ```
   ```

   This function makes calls to the REST API with path `/2.0/repositories/${workspaceId}/${repositoryId}`.
5. Navigate to the `src/frontend` directory and open the `index.jsx` file.
   Fetch the repository and log the output in the `App` function by replacing the
   `useEffect` Hook with the following code directly above the return statement:

   ```
   ```
   1
   2
   ```



   ```
   useEffect(() => {
     const fetchRepo = async () => {
       const repo = await invoke("fetchRepository");
       console.log(`Repository full name: ${repo.full_name}`);
     };
     fetchRepo();
   }, []);
   ```
   ```

Your `src/resolvers/index.js` file should look like the following:

```
```
1
2
```



```
import api, { route } from "@forge/api";
import Resolver from "@forge/resolver";

const resolver = new Resolver();

resolver.define("fetchRepository", async ({ context }) => {
  const workspaceId = context.workspaceId;
  const repositoryId = context.extension.repository.uuid;

  console.log(`Fetching repository ${workspaceId}/${repositoryId}`)

  const res = await api
    .asApp()
    .requestBitbucket(route`/2.0/repositories/${workspaceId}/${repositoryId}`);

  return res.json();
});

export const handler = resolver.getDefinitions();
```
```

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
    const fetchRepo = async () => {
      const repo = await invoke("fetchRepository");
      console.log(`Repository full name: ${repo.full_name}`);
    };
    fetchRepo();
  }, []);


  return (
    <>
      <Text>Hello world!</Text>
      <Text>{data ? data : "Loading..."}</Text>
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

## Set required permissions

Your app calls a remote resource; namely, the Bitbucket REST API.
As such, you'll need to grant your app the right [permissions](/platform/forge/manifest-reference/permissions/).
To do this, you'll need to add the required [Forge app scope](/cloud/bitbucket/rest/intro/#forge-app-and-api-token-scopes) to the app's manifest.

In the steps below, you'll do this by using the `forge lint` command. This command will automatically
add the required scope to your `manifest.yml` file (in this case, `read:repository:bitbucket`).

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

1. Open your browser's developer console.
2. Refresh the Bitbucket repository source page.
3. Check the output of the tunnel in the terminal. The resolver action should display as follows:

   ```
   ```
   1
   2
   ```



   ```
   invocation: 00000000000000004972bdc10ad9aad4 index.handler
   INFO    03:41:21.061  00000000000000004972bdc10ad9aad4  Fetching repository workspaceId/repositoryId
   ```
   ```
4. Check the output of the console. The repository’s full name should display as follows:

   ```
   ```
   1
   2
   ```



   ```
   Repository full name: workspace/repository
   ```
   ```

Logs can appear in your browser's developer console or tunnel in the terminal depending on where the `console.log` statements are placed.
See [Logging and debugging](https://developer.atlassian.com/platform/forge/debugging/).

## Follow API response links

API response links are absolute links. To follow them, you’ll need to use `routeFromAbsolute` when making the API call.
We’ll also try out `api.asUser()` instead of `api.asApp()` to make API requests in this section.

1. In `src/resolvers/index.js`, copy the following code to create a resolver function that calls the Bitbucket REST API
   by using the `routeFromAbsolute` method (don’t forget to add import of `routeFromAbsolute` from `@forge/api`):

   ```
   ```
   1
   2
   ```



   ```
   resolver.define("fetchCommits", async (req) => {
     const { payload } = req;
     const { commitsUrl } = payload;

     console.log("Fetching commits")

     const res = await api
       .asUser()
       .requestBitbucket(routeFromAbsolute(commitsUrl));

     return res.json();
   });
   ```
   ```

   Note we are using `api.asUser()` instead of `api.asApp()` this time.

The `.asUser()` function inherits the Atlassian app permissions of the user who has granted
access to the app. This can cause different API responses between different users in the same app.

1. In `src/frontend/index.jsx`, fetch the commits for the repository and log the output in the `App` function.
   To do this, add the following code in the `useEffect` hook in the `App` function directly after fetching the repository:

   ```
   ```
   1
   2
   ```



   ```
   const commits = await invoke("fetchCommits", {
     commitsUrl: repo.links.commits.href,
   });
   console.log(`Number of commits: ${commits.values.length}`);
   ```
   ```
2. Refresh the Bitbucket repository source page.
3. Since this is the first time the app is making API calls on behalf of the user (`asUser()`)
   rather than the app (`asApp()`), you'll need to authorize the app and grant it access to act on the user’s behalf.
   Follow the onscreen prompts to allow your app to access Atlassian apps on your behalf and
   refresh the repository source page again.
4. Check the output of the tunnel in the terminal. The resolver actions should display as follows:

   ```
   ```
   1
   2
   ```



   ```
   invocation: 00000000000000002f91025048f752ff index.handler
   INFO    03:44:09.506  00000000000000002f91025048f752ff  Fetching repository workspaceId/repositoryId

   invocation: 000000000000000081d88b18b30235ff index.handler
   INFO    03:44:11.764  000000000000000081d88b18b30235ff  Fetching commits
   ```
   ```
5. Check the output of the developer console in your browser.
   The repository’s full name and the number of commits should display as follows:

   ```
   ```
   1
   2
   ```



   ```
   Repository full name: workspace/repository
   Number of commits: 1
   ```
   ```

## Make an API call from frontend

In this section, you'll learn how to make Bitbucket API calls directly from the frontend of your app.

1. In `src/frontend/index.jsx`, add import of `view` and `requestBitbucket` from `@forge/bridge`:

   ```
   ```
   1
   2
   ```



   ```
   import { invoke, view, requestBitbucket } from "@forge/bridge";
   ```
   ```
2. In the same file, add the following code in the `useEffect` hook in the `App` function directly after
   fetching the commits. Using [requestBitbucket](/platform/forge/apis-reference/ui-api-bridge/requestBitbucket/) from the `@forge/bridge` package,
   this will make a Bitbucket API call as the current user to fetch a particular commit.

   ```
   ```
   1
   2
   ```



   ```
   if (commits.values) {
     const context = await view.getContext();
     const firstCommit = await requestBitbucket(`/2.0/repositories/${context.workspaceId}/${repo.uuid}/commit/${commits.values[0].hash}`);
     const firstCommitDate = (await firstCommit.json()).date;
     console.log(`First commit's date: ${firstCommitDate}`);
   }
   ```
   ```
3. Check the output of the developer console in your browser. If you had any commits in your repo,
   the first commit's date should be displayed similar to the below:

   ```
   ```
   1
   2
   ```



   ```
   Repository full name: workspace/repository
   Number of commits: 1
   First commit's date: 2024-04-19T07:02:29+00:00
   ```
   ```

Your `src/frontend/index.jsx` file should now look like the following:

```
```
1
2
```



```
import React, { useEffect, useState } from "react";
import ForgeReconciler, { Text } from "@forge/react";
import { invoke, view, requestBitbucket } from "@forge/bridge";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
   const fetchRepoAndCommits = async () => {
     const repo = await invoke("fetchRepository");
     setData(repo);
     console.log(`Repository full name: ${repo.full_name}`);
 
     const commits = await invoke("fetchCommits", {
       commitsUrl: repo.links.commits.href,
     });
     console.log(`Number of commits: ${commits.values.length}`);
 
     if (commits.values) {
       const context = await view.getContext();
       const firstCommit = await requestBitbucket(`/2.0/repositories/${context.workspaceId}/${repo.uuid}/commit/${commits.values[0].hash}`);
       const firstCommitDate = (await firstCommit.json()).date;
       console.log(`First commit's date: ${firstCommitDate}`);
     }
   };
   fetchRepoAndCommits();
  }, []);

  return (
    <>
      <Text>Hello world!</Text>
      <Text>
        {data ? `Repository full name: ${data.full_name}` : "Loading..."}
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

## Next step

In the next tutorial, you'll learn how to make changes to your app's frontend using the
[UI Kit components](/platform/forge/ui-kit/components/) of Forge.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1834)](/platform/forge/build-a-hello-world-app-in-bitbucket/)
[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1834)](/platform/forge/change-the-bitbucket-frontend-with-the-ui-kit)

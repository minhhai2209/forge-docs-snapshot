# Part 1: Build a pull request title validator with custom merge checks

This tutorial describes how to create a [custom merge check](/platform/forge/manifest-reference/modules/bitbucket-merge-check/)
app that can block a pull request merge when the title contains the word 'DRAFT'.
You can view the complete app code in the [Bitbucket pull request title validator repository](https://bitbucket.org/atlassian/forge-bitbucket-pull-request-title-validator/src/main/).

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development.
If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

### Set up a shared team workspace

For Bitbucket apps you need to join or create a [shared Bitbucket team workspace](https://confluence.atlassian.com/bbkb/difference-between-shared-and-personal-workspaces-1141477191.html) (as Forge apps are not supported on personal workspaces).
If you don't have a Bitbucket workspace, see the references below for related instructions:

1. [Creating a Bitbucket Cloud account](https://confluence.atlassian.com/bbkb/creating-a-bitbucket-cloud-account-1206558490.html).
2. [Join or create a workspace](https://support.atlassian.com/bitbucket-cloud/docs/create-your-workspace/).

A free Bitbucket team space can have up to 5 users.

## Create your app

Create an app based on the Bitbucket merge check template.

1. Navigate to the directory where you want to create the app. A new directory with the app's name will be created there.
2. Create your app by running:
3. Enter a name for the app. For example, *pr-title-validator*.
4. Select the *Triggers and Validators* category.
5. Select *Bitbucket* as the Atlassian app.
6. Select the *bitbucket-merge-check* template.
7. Change to the app subdirectory to see the app files

## Configure the app manifest

1. In the app's top-level directory, open the `manifest.yml` file.
2. Ensure the app has the `read:pullrequest:bitbucket` permission. This scope is required for the `bitbucket:mergeCheck` module.
   Additionally, the app will call the [Get a pull request API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/#api-repositories-workspace-repo-slug-pullrequests-pull-request-id-get) for which the `read:pullrequest:bitbucket` permission is required.

   ```
   ```
   1
   2
   ```



   ```
   permissions:
   scopes:
       - read:pullrequest:bitbucket
   ```
   ```
3. Change the `key` under `bitbucket:mergeCheck` to *check-pr-title*.
4. Change the `name` under `bitbucket:mergeCheck` to *Check pull request title*.
5. Change the `description` under `bitbucket:mergeCheck` to *Check pull request title does not contain 'DRAFT'*.
6. Update the `triggers` under `bitbucket:MergeCheck`, replacing the `on-code-pushed` trigger with `on-merge`.
   The check should be invoked when a user attempts to merge the pull request.

Your `manifest.yml` should look like the following:

```
```
1
2
```



```
permissions:
  scopes:
    - read:pullrequest:bitbucket
modules:
  bitbucket:mergeCheck:
    - key: check-pr-title
      function: main
      name: Check pull request title
      description: Check pull request title does not contain 'DRAFT'
      triggers:
        - on-merge
  function:
    - key: main
      handler: index.run
app:
  runtime:
    name: nodejs24.x
  id: '<your-app-id>'
```
```

See [Manifest](/platform/forge/manifest-reference/) to learn more about the manifest file.

## Implement the merge check

Your `manifest.yml` defines that when an `on-merge` event occurs, the `main` entry under `function` is invoked for the merge check.
The `main` function references the `run` function in your `src/index.js` file. Update the `run` function to implement the merge check.

1. In the app's top-level directory, install the `@forge/api` package API by running the following command:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/api
   ```
   ```
2. Open the `src/index.js` file.
3. Import the `@forge/api` package by adding the following to the top of the file:

   ```
   ```
   1
   2
   ```



   ```
   import api, { route } from "@forge/api";
   ```
   ```
4. In the `run` function, before you return the check result, make a request to [Get a pull request API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/#api-repositories-workspace-repo-slug-pullrequests-pull-request-id-get).
   Note, `await` expressions are only allowed within async functions, so you will need to change the function definition of `run` to be async.

   ```
   ```
   1
   2
   ```



   ```
   const workspaceUuid = event.workspace.uuid;
   const repoUuid = event.repository.uuid;
   const prId = event.pullrequest.id;

   const res = await api
     .asApp()
     .requestBitbucket(
       route`/2.0/repositories/${workspaceUuid}/${repoUuid}/pullrequests/${prId}`
     );
   const pr = await res.json();
   ```
   ```
5. Copy the following code to check whether the pull request title contains the word 'DRAFT'.

   ```
   ```
   1
   2
   ```



   ```
   const success = !pr.title.includes("DRAFT");
   const message = success
     ? "Pull request title does not contain 'DRAFT'"
     : "Pull request title contains 'DRAFT'";
   ```
   ```
6. Then, construct and return a check result object containing the outcome of the title checking logic, accompanied by a message.
   This check result object should be consistent with the [response payload](/platform/forge/manifest-reference/modules/bitbucket-merge-check/#response-payload) for a custom merge check.

   ```
   ```
   1
   2
   ```



   ```
   return { success, message };
   ```
   ```

Your `src/index.js` file should look something like this:

```
```
1
2
```



```
import api, { route } from "@forge/api";

export const run = async (event, context) => {
  const workspaceUuid = event.workspace.uuid;
  const repoUuid = event.repository.uuid;
  const prId = event.pullrequest.id;

  const res = await api
    .asApp()
    .requestBitbucket(
      route`/2.0/repositories/${workspaceUuid}/${repoUuid}/pullrequests/${prId}`
    );
  const pr = await res.json();

  const success = !pr.title.includes("DRAFT");
  const message = success
    ? "Pull request title does not contain 'DRAFT'"
    : "Pull request title contains 'DRAFT'";

  return { success, message };
};
```
```

## Install your app

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select *Bitbucket* using the arrow keys and press the enter key.
4. Enter the URL for your workspace. For example, <https://bitbucket.org/example-workspace/>.

Forge apps are not supported on personal workspaces. If you install an app to a personal workspace,
you will get an insufficient permissions error. See [set up a shared team workspace](/platform/forge/build-a-pull-request-title-validator-with-custom-merge-checks/#set-up-a-shared-team-workspace).

## Test your app

1. Enable the custom merge check feature in **Workspace settings → Workflow → Custom merge checks**

   ![Enable the custom merge check feature in your workspace settings](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-workspace-settings.png?_v=1.5800.1834)
2. Navigate to the repository within the workspace you want to enable the merge check for.
3. Navigate to the **Repository settings → Workflow → Custom merge checks** page.
4. Find your app in the list of merge check apps, and click the **Add Check** button.
5. Select the *Check pull request title* check from the **Name** dropdown.
6. Select the **Branch** you wish the check to be run against (for the sake of this tutorial, select `All branches`).
7. If you're on a [premium plan](https://www.atlassian.com/software/bitbucket/premium), tick the *Required* checkbox
   ![Enable the custom merge check in your repository settings](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-repository-settings.png?_v=1.5800.1834)
8. Create a pull request in your repository with the word ‘DRAFT' in the title and attempt to merge the pull request.
   The merge check should fail. If you configured the check as

   * **Required:** The merge will fail and the check failure will be visible on the merge checks card on the right side bar.

     ![Required custom merge check failure](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-required-failure.png?_v=1.5800.1834)
   * **Not required:** The merge will succeed, but the check failure will be visible on the merge checks card on the right side bar.

     ![Recommended custom merge check failure](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-recommended-failure.png?_v=1.5800.1834)
9. Create another pull request in your repository without the word ‘DRAFT' and merge the pull request. This time the merge check should pass.

   ![Custom merge check success](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-success.png?_v=1.5800.1834)

See [Set up custom merge checks](https://support.atlassian.com/bitbucket-cloud/docs/set-up-and-use-custom-merge-checks/) for more details.

## Next steps

Congratulations, you've built your first custom merge check. In this tutorial you covered:

* How to create a new forge app using the custom merge check template.
* How to add the required permissions for calling the Bitbucket Cloud API.
* How to call the Bitbucket API to retrieve the pull request for a particular custom merge check.
* How to run some simple validation on the state of that pull request, in order to decide if the pull request can be merged or not.
* And finally, how to return a check result to Bitbucket and control whether or not a pull request can be merged.

In the next tutorial, you'll learn how to make your custom merge check configurable
with [UI Kit](/platform/forge/ui-kit/get-started-with-ui/) and [Forge storage](/platform/forge/runtime-reference/storage-api/).

[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1834)](/platform/forge/extend-custom-merge-checks-with-ui-kit)

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).

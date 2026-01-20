# Part 2: Extend custom merge checks with UI Kit

This guide describes how to use [UI Kit](/platform/forge/ui-kit/get-started-with-ui/) and
[Forge storage](/platform/forge/runtime-reference/storage-api/) to extend a custom merge check app.

In Part 1, we made sure the title of a PR did not include the string "DRAFT".
Alternatively, you might have scenarios where you want to ensure the title does include some particular piece of text.
For example, you might have a process where every pull request needs to include a specific prefix from a list of options, or match a regex pattern.

In Part 2, we're going to modify the merge check we made in Part 1 such that it can prevent a pull request
from being merged if its title includes a specific substring set by a repository admin.
You can view the complete app code in the [Bitbucket pull request title validator repository](https://bitbucket.org/atlassian/forge-bitbucket-pull-request-title-validator/src/main/).

## Refactor the app

We will be adding more resources and functions to the app. Let's refactor it so that it is easier to extend.

1. Navigate to the app's top-level directory.
2. Create a `src/merge-checks` directory and move `src/index.js` to `src/merge-checks/index.js`.
3. Open `src/merge-checks/index.js` and rename `run` to `checkPullRequest`.
4. Create a `src/index.js` and export the `checkPullRequest` function.

   ```
   1
   2
   3
   import { checkPullRequest } from "./merge-checks";

   export { checkPullRequest };
   ```

Your app should have the following structure:

```
```
1
2
```



```
pr-title-validator
├── README.md
├── manifest.yml
├── package-lock.json
├── package.json
└── src
    ├── index.js
    └── merge-checks
        └── index.js
```
```

The `manifest.yml` file will also need to be updated to reflect the structural changes made to the app.

1. In the app's top-level directory, open the manifest.yml file.
2. Change the `function` under `bitbucket:mergeCheck` to *check-pull-request*.
3. Change the `description` under `bitbucket:mergeCheck` to *Check pull request title contains a configured substring*.
4. Change the `key` under `function` to *check-pull-request*.
5. Change the `handler` under `function` to *index.checkPullRequest*.

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
      function: check-pull-request
      name: Check pull request title
      description: Check pull request title contains a configured substring
      triggers:
        - on-merge
  function:
    - key: check-pull-request
      handler: index.checkPullRequest
app:
  runtime:
    name: nodejs24.x
  id: '<your-app-id>'
```
```

Test that the app is still behaving as expected after the refactor.

1. Deploy your app by running:

   You do not need to upgrade the app's installation as app permissions have not changed.
2. Test your app as described in [Part 1: View your app](/platform/forge/build-a-pull-request-title-validator-with-custom-merge-checks/#test-your-app)

## Store the configured substring

We need a way to store and retrieve the string we want to check for when validating the pull request title.
To do this, define [resolver](/platform/forge/runtime-reference/forge-resolver/#forge-resolver) methods for the frontend to call.
The resolver methods will interact with [Forge's storage API](/platform/forge/runtime-reference/storage-api/) for storing and retrieving the configured string.

1. In the app's top-level directory, install the `@forge/resolver` package by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/resolver
   ```
   ```
2. Create a `src/resolvers` directory and a `src/resolvers/index.js` file to contain the resolver functions that will interact with Forge storage.

   Your app should have the following structure:

   ```
   ```
   1
   2
   ```



   ```
   pr-title-validator
   ├── README.md
   ├── manifest.yml
   ├── package-lock.json
   ├── package.json
   └── src
       ├── index.js
       ├── merge-checks
       │   └── index.js
       └── resolvers
           └── index.js
   ```
   ```
3. Open `src/resolvers/index.js` and add helper methods to store and retrieve the configured pull request title.

   ```
   ```
   1
   2
   ```



   ```
   import Resolver from "@forge/resolver";
   import { kvs } from "@forge/kvs";

   const resolver = new Resolver();

   resolver.define("getTitleSubstring", async (request) => {
     const titleSubstring = await kvs.get("titleSubstring") || "";
     return titleSubstring;
   });

   resolver.define("updateTitleSubstring", async (request) => {
     await kvs.set("titleSubstring", request.payload.titleSubstring);
   });

   export const resolverHandler = resolver.getDefinitions();
   ```
   ```
4. Open `src/index.js` and export the `resolverHandler` from `src/resolvers/index.js`.

   ```
   ```
   1
   2
   ```



   ```
   import { resolverHandler } from "./resolvers";

   export { resolverHandler };
   ```
   ```

## Add a user interface

We render a form on the repository settings page for repository admins to configure
a string they expect to appear in the title of pull requests in the repository.
The UI will invoke our resolver methods from the earlier section using [Forge bridge APIs](/platform/forge/apis-reference/ui-api-bridge/bridge/).

1. In the app's top-level directory, install the `react`, `@forge/react` and `@forge/bridge` packages by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install react @forge/react @forge/bridge
   ```
   ```
2. Create a `src/frontend` directory and a `src/frontend/index.jsx` file to contain the frontend code.

   Your app should have the following structure:

   ```
   ```
   1
   2
   ```



   ```
   pr-title-validator
   ├── README.md
   ├── manifest.yml
   ├── package-lock.json
   ├── package.json
   └── src
       ├── index.js
       ├── frontend
       │   └── index.jsx
       ├── merge-checks
       │   └── index.js
       └── resolvers
           └── index.js
   ```
   ```
3. Open `src/frontend/index.js` and create a `TitleSubstringForm` component that will invoke the resolver method to store the substring when the form is submitted.

   ```
   ```
   1
   2
   ```



   ```
   import { invoke, showFlag } from "@forge/bridge";
   import {
     ErrorMessage,
     Form,
     FormFooter,
     Label,
     LoadingButton,
     RequiredAsterisk,
     Textfield,
     useForm,
   } from "@forge/react";

   const TitleSubstringForm = ({ defaultValues }) => {
     const { handleSubmit, register, getFieldId, formState } = useForm({
       defaultValues,
     });
     const { errors, isSubmitting } = formState;

     const onSubmit = async (data) => {
       if (data.titleSubstring) {
         await invoke("updateTitleSubstring", data);
         showFlag({
           id: "flag",
           title: "Changed title substring",
           type: "success",
           appearance: "success",
           description: `Set title substring to: ${data.titleSubstring}`,
           isAutoDismiss: true,
         });
       }
     };

     return (
       <Form onSubmit={handleSubmit(onSubmit)}>
         <Label labelFor={getFieldId("titleSubstring")}>
           Pull request title substring
           <RequiredAsterisk />
         </Label>
         <Textfield {...register("titleSubstring", { required: true })} />
         {errors.titleSubstring && (
           <ErrorMessage>This field is required</ErrorMessage>
         )}
         <FormFooter align="start">
           <LoadingButton type="submit" isLoading={isSubmitting}>
             Submit
           </LoadingButton>
         </FormFooter>
       </Form>
     );
   };
   ```
   ```
4. Add an `App` component that will invoke the resolver method to retrieve the stored substring
   and pass it as a `defaultValue` to the `TitleSubstringForm` component.

   ```
   ```
   1
   2
   ```



   ```
   import { useEffect, useState } from "react";
   import { Inline, Spinner, Text } from "@forge/react";

   const App = () => {
     const [titleSubstring, setTitleSubstring] = useState();

     useEffect(() => {
       invoke("getTitleSubstring").then((substring) => {
         setTitleSubstring(substring);
       });
     }, []);

     return (
       <>
         {titleSubstring === undefined ? (
           <Inline alignInline="center">
             <Spinner size="large" />
           </Inline>
         ) : (
           <>
             <Text>Configure the required string in pull request title</Text>
             <TitleSubstringForm defaultValues={{ titleSubstring }} />
           </>
         )}
       </>
     );
   };
   ```
   ```
5. Render the `App` component using the `ForgeReconciler`.

   ```
   ```
   1
   2
   ```



   ```
   import ForgeReconciler from "@forge/react";
   import React from "react";

   ForgeReconciler.render(
     <React.StrictMode>
       <App />
     </React.StrictMode>
   );
   ```
   ```

Your `src/frontend/index.jsx` should look something like this:

```
```
1
2
```



```
import { invoke, showFlag } from "@forge/bridge";
import ForgeReconciler, {
  ErrorMessage,
  Form,
  FormFooter,
  Inline,
  Label,
  LoadingButton,
  RequiredAsterisk,
  Spinner,
  Text,
  Textfield,
  useForm,
} from "@forge/react";
import React, { useEffect, useState } from "react";

const TitleSubstringForm = ({ defaultValues }) => {
  const { handleSubmit, register, getFieldId, formState } = useForm({
    defaultValues,
  });
  const { errors, isSubmitting } = formState;

  const onSubmit = async (data) => {
    if (data.titleSubstring) {
      await invoke("updateTitleSubstring", data);
      showFlag({
        id: "flag",
        title: "Changed title substring",
        type: "success",
        appearance: "success",
        description: `Set title substring to: ${data.titleSubstring}`,
        isAutoDismiss: true,
      });
    }
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Label labelFor={getFieldId("titleSubstring")}>
        Pull request title substring
        <RequiredAsterisk />
      </Label>
      <Textfield {...register("titleSubstring", { required: true })} />
      {errors.titleSubstring && (
        <ErrorMessage>This field is required</ErrorMessage>
      )}
      <FormFooter align="start">
        <LoadingButton type="submit" isLoading={isSubmitting}>
          Submit
        </LoadingButton>
      </FormFooter>
    </Form>
  );
};

const App = () => {
  const [titleSubstring, setTitleSubstring] = useState();

  useEffect(() => {
    invoke("getTitleSubstring").then((substring) => {
      setTitleSubstring(substring);
    });
  }, []);

  return (
    <>
      {titleSubstring === undefined ? (
        <Inline alignInline="center">
          <Spinner size="large" />
        </Inline>
      ) : (
        <>
          <Text>Configure the required string in pull request title</Text>
          <TitleSubstringForm defaultValues={{ titleSubstring }} />
        </>
      )}
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

## Update the merge check

Update the merge check to retrieve the stored substring and return a response payload
based on whether the pull request title contains the substring.

1. Open `src/merge-checks/index.js`.
2. Import `kvs` from `@forge/kvs` so that configured substring can be retrieved.

   ```
   ```
   1
   2
   ```



   ```
   import { kvs } from "@forge/kvs";
   ```
   ```
3. In the same file, before you call the Bitbucket REST API, retrieve the configured pull request title substring from Forge Storage.
   If the substring is not configured, return a failure response payload.

   ```
   ```
   1
   2
   ```



   ```
   const substring = await kvs.get("titleSubstring");

   if (!substring) {
     console.log("Title substring is not configured. Failing merge check.");
     return {
       success: false,
       message: "Title substring is not configured",
     };
   }
   ```
   ```
4. Modify the check criteria to be successful if the pull request contains the substring.

   ```
   ```
   1
   2
   ```



   ```
   const success = pr.title.includes(substring);
   const message = success
     ? `Pull request title contains ${substring}`
     : `Pull request title does not contain ${substring}`;
   ```
   ```

Your `src/merge-checks/index.js` should look like the following:

```
```
1
2
```



```
import api, { route } from "@forge/api";
import { kvs } from "@forge/kvs";

export const checkPullRequest = async (event, context) => {
  const workspaceUuid = event.workspace.uuid;
  const repoUuid = event.repository.uuid;
  const prId = event.pullrequest.id;

  const substring = await kvs.get("titleSubstring");

  if (!substring) {
    console.log("Title substring is not configured. Failing merge check.");
    return {
      success: false,
      message: "Title substring is not configured",
    };
  }

  const res = await api
    .asApp()
    .requestBitbucket(
      route`/2.0/repositories/${workspaceUuid}/${repoUuid}/pullrequests/${prId}`
    );
  const pr = await res.json();

  const success = pr.title.includes(substring);
  const message = success
    ? `Pull request title contains ${substring}`
    : `Pull request title does not contain ${substring}`;

  return { success, message };
};
```
```

## Update the app manifest

1. In the app's top-level directory, open the `manifest.yml` file.
2. Add the `storage:app` permission to the `scopes` under `permissions`. This scope is required for Forge Storage.
3. Add a `bitbucket:repoSettingsMenuPage` [module](/platform/forge/manifest-reference/modules/bitbucket-repository-settings-menu-page/) entry
   for the repository settings page we added.

   ```
   ```
   1
   2
   ```



   ```
   bitbucket:repoSettingsMenuPage:
     - key: settings-page
       resource: main
       render: native
       title: Check pull request title
       resolver:
         function: resolver
   ```
   ```
4. Add a new `function` module entry for the repository settings page resolver.

   ```
   ```
   1
   2
   ```



   ```
   function:
     - key: resolver
       handler: index.resolverHandler
   ```
   ```
5. Add a new `resources` entry for the repository settings page resource.

   ```
   ```
   1
   2
   ```



   ```
   resources:
     - key: main
       path: src/frontend/index.jsx
   ```
   ```

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
    - storage:app
modules:
  bitbucket:mergeCheck:
    - key: check-pr-title
      function: check-pull-request
      name: Check pull request title
      description: Check pull request title contains the string configured in settings
      triggers:
        - on-merge
  bitbucket:repoSettingsMenuPage:
    - key: settings-page
      resource: main
      render: native
      title: Check pull request title
      resolver:
        function: resolver
  function:
    - key: check-pull-request
      handler: index.checkPullRequest
    - key: resolver
      handler: index.resolverHandler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs24.x
  id: '<your-app-id>'
```
```

## Test the app

1. Deploy your app by running:
2. Upgrade the app's installation. This is necessary as the app's permissions have changed.

   ```
   ```
   1
   2
   ```



   ```
   forge install --upgrade
   ```
   ```
3. Navigate to your repository settings and open the "Check pull request title" menu item under the `FORGE APPS` section.

   ![Check pull request title repository settings page](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-configuration-page.png?_v=1.5800.1783)
4. Set the pull request title substring value. For example, *TICKET-*.
5. Ensure the merge check is enabled via the Repository settings → Custom merge checks page if it is not already enabled.
6. Create a pull request without the substring in the title.
7. Merge the pull request. The merge check should fail.
8. Create another pull request with the substring in the title.
9. Merge the pull request. This time the merge check should pass.

## Next Steps

Check out an example app, continue to one of the other tutorials, or read through the reference pages to learn more.

[![A button to go back a page](https://dac-static.atlassian.com/platform/forge/images/button-go-back.svg?_v=1.5800.1783)](/platform/forge/build-a-pull-request-title-validator-with-custom-merge-checks/)

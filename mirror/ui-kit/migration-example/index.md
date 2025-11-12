# Migrate an app from UI Kit 1 to UI Kit example

In this tutorial, we will be going through the steps of migrating a Jira issue translator app built with
UI Kit 1 to the latest version of [UI Kit](/platform/forge/ui-kit/). We will be migrating this sample [UI Kit 1 app](https://bitbucket.org/atlassian/forge-issue-translation/src/master/).

For a full list of changes between UI Kit 1 and UI Kit, see the [UI Kit 1 to UI Kit upgrade page](/platform/forge/ui-kit/upgrade-to-ui-kit-latest/).

## Before you begin

Make sure to do the following before you start migrating your app:

1. Have a UI Kit 1 app you would like to migrate ready or use our sample [UI Kit 1 app](https://bitbucket.org/atlassian/forge-issue-translation/src/master/) to follow along.
2. Update the Forge CLI to the latest version by running the following command:

   `npm install -g @forge/cli@latest`

## Install required packages

1. UI Kit requires a few new packages to be installed. Install the following packages from the root of the project by running the following command:

   `npm install @forge/react @forge/resolver @forge/bridge --save`

* `@forge/react` is a package that contains all UI Kit components.
* `@forge/resolver` is a package that allows you to define backend functions.
* `@forge/bridge` is a package that allows you to invoke Atlassian app specific capabilities and resolver functions from the frontend.
* `@forge/ui` can be uninstalled as it is no longer required.

## Structuring frontend (UI) and backend code for UI Kit

In UI Kit, frontend code will be invoked in a sandboxed environment on the client. Frontend code is any code that renders our UI or JavaScript code that can be executed in the browser. Sandboxing ensures that the frontend code runs securely and independently within the browser.

Backend code will be invoked from resolvers. This approach is used to manage data requests and responses, ensuring that backend logic is executed in response to specific queries or mutations. Resolvers are configured to trigger the appropriate backend functions when needed.

We will first create a separate directory for frontend code and migrate our frontend logic to there.

## Migrate the frontend code

1. Create the following directory and file: `src/frontend/index.js`.
2. Move all frontend code into this file. Any code using `@forge/api` is backend code and will need to be moved into a resolver in the next step.

From our sample app, this is what the initial `src/frontend/index.jsx` file will look like:

```
```
1
2
```



```
import React, { Fragment, useState } from "react";
import ForgeReconciler, { ButtonGroup, Button, Text } from "@forge/react";
import { invoke } from "@forge/bridge"; // will be used in `setLanguage` in the next step

const LANGUAGES = [
  ["🇯🇵 日本語", "ja"],
  ["🇰🇷 한국어", "ko"],
  ["🇬🇧 English", "en"],
];

const App = () => {
  const [translation, setTranslation] = useState(null);

  const setLanguage = async (countryCode) => {
    // will be implemented in the next step
  };

  return (
    <Fragment>
      <ButtonGroup>
        {LANGUAGES.map(([label, code]) => (
          <Button
            key={code}
            onClick={async () => {
              await setLanguage(code);
            }}
          >
            {label}
          </Button>
        ))}
      </ButtonGroup>
      {translation && (
        <Fragment>
          <Text>**{translation.summary}**</Text>
          <Text>{translation.description}</Text>
        </Fragment>
      )}
    </Fragment>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

Note the differences from the original UI Kit 1 code:

* `@forge/react` is the new library holding all UI Kit components.
* Usage of the `Fragment` component should be from the `react` library. The shorthand syntax `<></>`
  can also be used instead and doesn’t require an additional import.
* The root of your app needs to be passed into `ForgeReconciler.render`
* Several updates to component APIs have been made between UI Kit 1 and the latest version of UI Kit.
  The full list of changes can be found [here](/platform/forge/ui-kit/upgrade-to-ui-kit-latest/#changes-to-existing-components).
  In this example, we’ve had to:
  * Replace `ButtonSet` with `ButtonGroup`
  * Pass the text content in `Button` and `Text` as children of the component.

## Migrate the backend code

From the previous step, you’ll notice the `setLanguage` logic is missing. This is due to the usage of the
[@forge/api](/platform/forge/runtime-reference/) package. `@forge/api` can only be used in a
Forge resolver function, as it is a Node package and is incompatible with the frontend.
Forge resolvers are a series of backend functions for your app that can use backend packages. These resolvers can then be invoked from the frontend using `invoke` from `@forge/bridge`.

1. Create a new directory and file with the following folder structure `src/resolvers/index.js`.
2. Copy over the `setLanguage` function into the resolver.

```
```
1
2
```



```
import Resolver from "@forge/resolver";
import api, { route } from "@forge/api";

async function checkResponse(apiName, response) {
  if (!response.ok) {
    const message = `Error from ${apiName}: ${
      response.status
    } ${await response.text()}`;
    console.error(message);
    throw new Error(message);
  } else if (process.env.DEBUG_LOGGING) {
    console.debug(`Response from ${apiName}: ${await response.text()}`);
  }
}

const TRANSLATE_API =
  "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0";

const resolver = new Resolver();

resolver.define("setLanguage", async ({ context, payload }) => {
  const countryCode = payload.countryCode;
  const issueKey = context.extension.issue.key;

  // Fetch issue fields to translate from Jira
  const issueResponse = await api
    .asApp()
    .requestJira(
      route`/rest/api/2/issue/${issueKey}?fields=summary,description`
    );
  await checkResponse("Jira API", issueResponse);
  const { summary, description } = (await issueResponse.json()).fields;

  // Translate the fields using the Azure Cognitive Services Translation API
  const translateResponse = await api.fetch(
    `${TRANSLATE_API}&to=${countryCode}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
        // See README.md for details on generating a Translation API key
        "Ocp-Apim-Subscription-Key": process.env.TRANSLATE_API_KEY,
        "Ocp-Apim-Subscription-Region": process.env.TRANSLATE_API_LOCATION,
      },
      body: JSON.stringify([
        { Text: summary },
        { Text: description || "No description" },
      ]),
    }
  );
  await checkResponse("Translate API", translateResponse);
  const [summaryTranslation, descriptionTranslation] =
    await translateResponse.json();

  // Update the UI with the translations
  return {
    to: countryCode,
    summary: summaryTranslation.translations[0].text,
    description: descriptionTranslation.translations[0].text,
  };
});

export const handler = resolver.getDefinitions();
```
```

Important things to note:

* The first parameter of `resolver.define` is a string that will be used as a key to invoke this resolver.
* The second parameter is the callback function that will be executed when invoked from the frontend. It's parameters include the context object of an extension point
  and payload of the function invocation.

We'll also need to export this resolver so that it can be imported into our manifest file in the next section.

Add a new `src/index.js` file with the following contents:

```
```
1
2
```



```
export { handler } from "./resolvers";
```
```

Back in `src/frontend/index.jsx`, add the following to invoke your new resolver:

```
```
1
2
```



```
const setLanguage = async (countryCode) => {
  const resp = await invoke("setLanguage", { countryCode });
  setTranslation(resp);
};
```
```

## Update the manifest

We now need to wire up the frontend and backend and also update our app to use UI Kit. We can do this by updating our `manifest.yml` file.

1. Add the `render: native` property to your app so that it will now render using UI Kit instead of UI Kit 1.

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: translate
      render: native
      ...
```
```

2. Remove the `function` property in your app as this is no longer required for UI Kit.
3. Replace the existing UI Kit 1 `function`'s `key` and `handler` properties with a new `key` and `handler` that points to our new resolver.

```
```
1
2
```



```
function:
  - key: resolver
    handler: index.handler
```
```

4. Add a new `resources` property and set a unique `key` and `path` to our frontend file.

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

5. The full manifest file should look like this:

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: translate
      resource: main
      resolver:
        function: resolver
      render: native
      title: Translate
      icon: https://developer.atlassian.com/platform/forge/images/icons/issue-translation-icon.svg
      description: Translate issue fields into other languages
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: "ari:cloud:ecosystem::app/764f9c2d-fac3-493f-b9fe-aabda3c639a2"
  runtime:
    name: nodejs22.x
permissions:
  scopes:
    - "read:jira-work"
  external:
    fetch:
      backend:
        - "https://api.cognitive.microsofttranslator.com"
```
```

That's it! To test, set up Forge variables, then deploy and install the app in to your instance.

You can find the migrated sample app [here](https://bitbucket.org/atlassian/forge-ui-kit-2-translate/src/main/).

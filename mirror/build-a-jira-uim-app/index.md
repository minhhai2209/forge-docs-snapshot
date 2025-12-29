# Build a Jira UI modifications app

This tutorial walks you through creating your first **UI modifications (UIM)** app. You'll set up the manifest, write the app code, and configure UI modifications using the REST API so your app can customize Jira and Jira Service Management experiences.

This tutorial is based on the following example app:

[Jira UI modifications example app

This example Jira UIM app demonstrates how to configure the manifest, modify fields and tabs at runtime, and manage UI modifications via REST APIs.](https://bitbucket.org/atlassian/forge-ui-modifications-example)

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development. If this is your first time using Forge, see [Getting started](/platform/forge/getting-started) first.

You should also:

## Step 1: Configure the Forge manifest

You can build your Forge app by following our [Jira](/platform/forge/build-a-hello-world-app-in-jira/)
or [Jira Service Management Hello World app](/platform/forge/build-a-hello-world-app-in-jira-service-management/)
tutorials. To turn your app into a UIM app, update your `manifest.yml` file to include a `jira:uiModifications` module and a static resource:

```
1
2
3
4
5
6
7
8
modules:
  jira:uiModifications:
    - key: ui-modifications-app
      title: Example UI modifications app
      resource: uiModificationsApp
resources:
  - key: uiModificationsApp
    path: static/ui-modifications/dist
```

## Step 2: Add the UIM app code

UIM apps depend on the `@forge/jira-bridge` package, which exposes the [uiModifications API](/platform/forge/custom-ui-jira-bridge/uiModifications/) from version 0.6.0 onwards.

The UIM app code:

* Runs on the client side inside an invisible `iframe`.
* Is loaded from the static resource declared in the `jira:uiModifications` module.
* Applies all requested changes at once, after the initialization callback finishes.

In your static resource (for example, `static/ui-modifications/index.js`), add the following code:

```
```
1
2
```



```
// static/ui-modifications/index.js
import { uiModificationsApi } from '@forge/jira-bridge';

uiModificationsApi.onInit(
  ({ api }) => {
    const { getFieldById, getScreenTabs } = api;

    // Hiding the priority field
    const priority = getFieldById('priority');
    priority?.setVisible(false);

    // Changing the summary field label
    const summary = getFieldById('summary');
    summary?.setName('Modified summary label');

    // Changing the assignee field description
    const assignee = getFieldById('assignee');
    assignee?.setDescription('Description added by UI modifications');

    // Get value of labels field
    const labels = getFieldById('labels');
    const labelsData = labels?.getValue() || [];
    labels?.setDescription(
      `${labelsData.length} label(s) are currently selected`
    );

    // Hide the last screen tab
    const tabs = getScreenTabs();
    if (tabs.length > 0) {
      tabs.at(-1).setVisible(false);
    }
  },
  () => ['priority', 'summary', 'assignee', 'labels']
);
```
```

All changes requested during the `onInit` callback are applied together after the function completes.

## Step 3: Handle async operations

Sometimes your UIM app needs to perform async work before deciding which modifications to apply. For example, you may need to call a remote service or fetch configuration first.

To support this, `onInit` callbacks can return a `Promise`. Changes are postponed until the `Promise` resolves.

Here is a correct implementation using a `Promise`:

```
```
1
2
```



```
import { uiModificationsApi } from '@forge/jira-bridge';

// Imaginary import
import { shouldPriorityBeHidden } from '../my-services';

uiModificationsApi.onInit(
  ({ api }) => {
    const { getFieldById } = api;

    // Hiding the priority field
    const priority = getFieldById('priority');
    // Store the update Promise
    const priorityUpdate = shouldPriorityBeHidden().then((result) => {
      if (result === true) {
        priority?.setVisible(false);
      }
    });

    // Changing the assignee field description
    const assignee = getFieldById('assignee');
    assignee?.setDescription('Description added by UI modifications');

    // Return the promise. In this case even the assignee field description
    // is updated only after the priorityUpdate promise resolves.
    return priorityUpdate;
  },
  () => ['priority', 'assignee']
);
```
```

`async/await` syntax is also supported:

```
```
1
2
```



```
import { uiModificationsApi } from '@forge/jira-bridge';

// Imaginary import
import { shouldPriorityBeHidden } from '../my-services';

uiModificationsApi.onInit(
  async ({ api }) => {
    const { getFieldById } = api;

    // Hiding the priority field
    const priority = getFieldById('priority');
    const result = await shouldPriorityBeHidden();
    if (result === true) {
      priority?.setVisible(false);
    }

    // Changing the assignee field description
    const assignee = getFieldById('assignee');
    assignee?.setDescription('Description added by UI modifications');
  },
  () => ['priority', 'assignee']
);
```
```

## Step 4: Configure the UI modification

The UIM Forge module only renders when you configure it for a given context using the [UIM REST API](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/).

You can, for example, create an [AdminPage](/platform/forge/ui-kit-components/jira/admin-page/) that calls the REST API to create a UI modification. Apps can also include custom UIM data, which is passed to the UIM Forge module when it runs (for example, a list of rules a user has selected).

Jira

Jira Service Management

To configure a UI modification for a given `projectId` and `issueTypeId`:

```
```
1
2
```



```
import api, { route } from '@forge/api';

const createUiModification = async (projectId, issueTypeId) => {
  const result = await api.asApp().requestJira(route`/rest/api/3/uiModifications`, {
    method: "POST",
    body: JSON.stringify({
      name: 'demo-ui-modification',
      data: '["custom data", "for your app"]',
      contexts: [
        { projectId, issueTypeId, viewType: 'GIC' }, 
        { projectId, issueTypeId, viewType: 'IssueView' }
      ],
    }),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });
  console.log(`Created UI modification with status ${result.status}`);
  return result.status;
}
```
```

Custom UIM data is available as `uiModifications` within the `onInit` and `onChange` callbacks. It has the following shape:

```
```
1
2
```



```
uiModifications: Array<{
  id: string,
  data?: string,
}>
```
```

## Next steps

Now that you've built your first UIM app, you can:

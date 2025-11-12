# Jira dashboard gadget

The `jira:dashboardGadget` module creates a dashboard gadget that is displayed on the [Dashboards page](https://support.atlassian.com/jira-work-management/docs/what-is-a-jira-dashboard/).

This module can be used in Jira and Jira Service Management.

## Configuration

Dashboard Gadgets can be configured using their edit mode.

### Auto-refresh

Dashboard Gadgets can be refreshed manually by your users and automatically. The automatic refresh interval (in minutes) is configured by submitting a `refresh` field as part of an edit view (the API accepts positive integers for this field).

#### Custom UI and UI Kit

When using Custom UI and UI Kit to work with the Dashboard Gadget module, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit) as part of your edit view to provide a `refresh` field to the submit function:

```
1
await view.submit({ ...otherFieldsToSubmit, refresh: 15 });
```

##### Overriding default gadget refresh behavior

1. Set the `refreshable` property to `false` in the gadget's manifest file.
2. Write your own refresh logic by handling the `JIRA_DASHBOARD_GADGET_REFRESH` event using the `events.on()` function from the Forge bridge.
3. Optionally, apply the refresh logic only when the `origin` and `gadgetId` properties of the payload satisfy a condition.

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
import { events } from '@forge/bridge';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    const subscription = events.on('JIRA_DASHBOARD_GADGET_REFRESH', (payload) => {
      // the payload contains the following properties:
      // - payload.origin - either 'dashboard' or 'gadget' depending on which refresh button was clicked
      // - payload.gadgetId - the ID of the gadget initiating the refresh (only available if payload.origin === 'gadget')

      // you can obtain the ID of the currently rendered gadget using the view.getContext() function
    });

    return () => {
      subscription.then(({ unsubscribe }) => unsubscribe());
    };
  }, []);

  // render the gadget
}
```

> When the user clicks the refresh button of any Forge dashboard gadget that has overridden the default refresh
> behavior, the `JIRA_DASHBOARD_GADGET_REFRESH` event will be triggered and *all* Forge gadgets will receive it.
> You can limit the scope of the refresh logic based on the available payload, for example with `payload.origin === 'dashboard' || payload.gadgetId === thisGadgetId`.

## Conditional rendering

With Custom UI, you can define the same resource for viewing and editing your dashboard gadget.

First, define your manifest:

```
```
1
2
```



```
modules:
  jira:dashboardGadget:
    - key: hello-world-gadget
      title: Hello world!
      description: A hello world dashboard gadget.
      thumbnail: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
      resource: main # the resource used to view our dashboardGadget
      resolver:
        function: resolver
      edit:
        resource: main # the same resource, used to edit our dashboardGadget configuration
resources:
  - key: main
    path: static/hello-world/build
```
```

Then in your Custom UI, use the view API to determine whether to display the view mode or edit mode:

```
```
1
2
```



```
// App.jsx
import React, { useEffect, useState } from 'react';
import { view } from '@forge/bridge';
import View from './View';
import Edit from './Edit';

function App() {
  const [context, setContext] = useState();

  useEffect(() => {
    view.getContext().then(setContext);
  }, []);

  if (!context) {
    return 'Loading...';
  }

  return context.extension.entryPoint === 'edit' ? <Edit/> : <View/>;
}

export default App;
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` or `{ text: string, href: string }` | Yes | Can be:  * a plain string containing the gadget's title. * an `i18n object` to enable internationalization. * an object containing a `text` property containing the gadget's title and a `href` property containing a link that the user is sent to when they click the gadget’s title.   The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | A description of what the gadget does.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `thumbnail` | `string` | Yes | The absolute URL of the icon that's displayed next to the gadget's name and description in the list of gadgets that can be added to a dashboard. |
| `edit.resource` | `string` | If your editing experience uses [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that provides the editing experience for your dashboard gadget. See [Resources](/platform/forge/manifest-reference/resources) for more details. To submit the view, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit). |
| `edit.render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the editing experience uses UI Kit. |
| `refreshable` | `boolean` |  | Set the `refreshable` property of the dashboard item to `false` to override the native Jira refresh behavior. |
| `displayConditions` | `object` |  | An object that defines whether the gadget is displayed on the list of gadgets available to install. If a gadget is already added to the dashboard, users without the permission to use it will see an error message. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

| Property | Type | Description |
| --- | --- | --- |
| `gadgetConfiguration` | `object` | Object containing gadget configuration. |
| `dashboard.id` | `string` | ID of the dashboard. |
| `gadget.id` | `string` | ID of the gadget. |
| `type` | `string` | The type of the module. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

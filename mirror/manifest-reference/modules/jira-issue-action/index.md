# Jira issue action

The `jira:issueAction` module adds a menu item to the more actions (•••) menu on the issue view.
When the menu item is clicked, the module’s function renders a modal dialog.

This module can be used in Jira and Jira Service Management.
It works in the
[new issue view](https://support.atlassian.com/jira-core-cloud/docs/what-is-the-new-jira-issue-view/)
but not the old issue view.

![Example of an Issue action button](https://dac-static.atlassian.com/platform/forge/snippets/images/issue-action-location.png?_v=1.5800.1813)

This is an example of the triggered modal dialog:

![Example of an Issue action with the above sample code](https://dac-static.atlassian.com/platform/forge/snippets/images/issue-action-demo.png?_v=1.5800.1813)

## Manifest example

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
  jira:issueAction:
    - key: hello-world-issue-action
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'small'`, `'medium'`, `'large'`, `'xlarge'` or `'max'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |
| `title` | `string` or `i18n object` | Yes | The title of the issue action, which is displayed as a menu item.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension data

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `issue.id` | `string` | The id of the issue on which the module is rendered. |
| `issue.key` | `string` | The key of the issue on which the module is rendered. |
| `issue.type` | `string` | The type of the issue on which the module is rendered. |
| `issue.typeId` | `string` | The id of the type of the issue on which the module is rendered. |
| `project.id` | `string` | The id of the project where the module is rendered. |
| `project.key` | `string` | The key of the project where the module is rendered. |
| `project.type` | `string` | The type of the project where the module is rendered. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

#### Extension context

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |

#### Platform context

| Property | Type/value | Description |
| --- | --- | --- |
| `issueId` | `string` | The ID of the issue on which the module is rendered. |
| `issueKey` | `string` | The key of the issue on which the module is rendered. |
| `issueType` | `string` | The type of the issue on which the module is rendered. |
| `issueTypeId` | `string` | The ID of the type of the issue on which the module is rendered. |
| `projectId` | `string` | The ID of the project where the module is rendered. |
| `projectKey` | `string` | The key of the project where the module is rendered. |
| `projectType` | `string` | The type of the project where which the module is rendered. |

## Events

Apps can receive frontend events that will notify your app when an issue has been changed. These events are triggered when an issue is updated or commented on, and are only available for Jira issue view modules.

```
```
1
2
```



```
import { events } from "@forge/bridge";
events.on("JIRA_ISSUE_CHANGED", (data) => {
  console.log("JIRA_ISSUE_CHANGED (Forge)", data);
});
```
```

However, if you have multiple issue view modules in your app, you should use the Jira issue view background script module or its Connect counterpart. This will give you a central place for fetching issue details, thus reducing the number of network requests and improving the user experience. Fetching issue details separately for every module would introduce unnecessary overhead and degrade performance.

### Data shape

```
```
1
2
```



```
{
  "issueId": string,
  "projectId": string,
  "changes":[{
    "changeType": "updated" | "commented",
    "atlassianId": string
  }]
}
```
```

| Property | Description |
| --- | --- |
| `issueId` | ID of the issue the app is rendered on. |
| `projectId` | ID of the project the issue belongs to. |
| `changes` | List of issue changes  * `changeType` - type of the change   * `commented` - a comment has been added to the page   * `updated` - the issue has been updated * `atlassianId` - ID of the user who made the change |

### Limitations

* There is a delay between the moment the issue is modified and when the event is emitted. It might take up to a few seconds.
* When the issue is modified by the user who is currently viewing it, it will not be refreshed. This is because we assume the change was made by that same user and there is no need for an update.

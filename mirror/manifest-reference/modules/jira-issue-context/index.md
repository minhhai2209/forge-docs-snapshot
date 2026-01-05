# Jira issue context

The `jira:issueContext` module adds a collapsible panel under the other fields on the right side of the [issue view](https://support.atlassian.com/jira-work-management/docs/what-is-the-new-jira-issue-view/).
These panels give your users a quick way to get information related to the issue from your app.
Users can expand these panels to view app information or collapse them if they don’t need it.

![](https://dac-static.atlassian.com/platform/forge/images/jira-issue-context.png?_v=1.5800.1742)

This module can be used in Jira and Jira Service Management.
It works in the
[new issue view](https://support.atlassian.com/jira-core-cloud/docs/what-is-the-new-jira-issue-view/)
but not the old issue view.

## Manifest example

```
```
1
2
```



```
modules:
  jira:issueContext:
    - key: hello-world-issue-context
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World!
      description: A hello world issue context.
      label: Hello World!
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the issue context panel, which is displayed next to its label.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `label` | `string` or `i18n object` | Yes | The text shown on the button for the issue context panel.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The absolute URL of the icon that is displayed to the left of the label on the button for the issue context panel. |
| `status` | `object` |  | The badge, lozenge, or icon shown to the right of the `label`. If `status` is not specified, then nothing is shown. See [status properties](#status-properties). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `dynamicProperties` | `{ function: string }` |  | Contains a `function` property, which references the `function` module that returns changeable properties. See [Dynamic properties](#dynamic-properties) for more details. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

### Status properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | `'badge' | 'lozenge' | 'icon'` | Yes | The UI element used to display the status. |
| `value` | `object` | Yes | This property is an object representing the status value. See [status value properties](#status-value-properties). |

### Status value properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | The text to display in the status. If `type` is `'badge'`, this property is a number specified as a string (for example, `'3'`). |
| `url` | `string` |  | If `type` is `'icon'`, this value controls the URL of the icon to display in the status. |
| `type` | `'default' | 'inprogress' | 'moved' | 'new' | 'removed' | 'success'` |  | If `type` is `'lozenge'`, this value controls the appearance of the status. |

### Dynamic properties

To use dynamic properties, you must declare them in your app's `manifest.yml`. Your app must also implement a `dynamicProperties` handler function.

Jira will retrieve your app's dynamic properties on initial render, which happens when the issue context panel is first expanded. Your app will then render inside the issue context panel and execute its business logic.

When the issue context panel is collapsed, Jira will call your app's `dynamicProperties` handler function and update the status based on what the function returns.

The app's handler function is passed the `payload` argument. The `payload` object has the following structure:

```
```
1
2
```



```
interface Payload {
  // The cloudId for your site 
  cloudId: string;
  extension: {
    // The module type included in the manifest.yml file.
    type: "jira:issueContext";
    issue: {
      id: string,
      type: string,
      key: string,
      typeId: string
    },
    project: {
      id: string,
      type: string,
      key: string
    }
  };
}
```
```

The handler function should return (or resolve with) a plain JavaScript object with `status` as key.

This is an example of a handler function returning an object:

```
```
1
2
```



```
function handlerFunction(contextPayload) {
  return {
    "status": {
      "type": "lozenge",
      "value": {
        "label": "Dynamically set status",
        "type": "moved"
      }
    }
  };
}
```
```

When you use an `icon` in your dynamic properties, its source URL is subject to a permission check.

For an example of adding source URL permissions for your `icon` property, see [External Permissions](/platform/forge/manifest-reference/permissions/#images).

Bundled resources in the following formats are allowed by default:

* `resource:<resource key>;<relative path to resource>`
* `data:image` URIs

See [Icons](/platform/forge/custom-ui/#icons) for more information about bundling icons as a resource.

When the source URL does not have the appropriate permissions, the dynamic properties are not loaded. The default configuration is used instead.

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

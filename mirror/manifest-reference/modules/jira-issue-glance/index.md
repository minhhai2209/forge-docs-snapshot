# Jira issue glance

The `jira:issueGlance` module adds an issue glance to Jira, which is content that is shown/hidden in
an issue by clicking a button. The button for the issue glance is placed alongside fields
such as *Assignee* and *Labels*. Clicking the button opens the content provided by the Forge app, so
that it fills the right sidebar.

This module can be used in Jira and Jira Service Management.
It works in the
[new issue view](https://support.atlassian.com/jira-core-cloud/docs/what-is-the-new-jira-issue-view/)
but not the old issue view.

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
9
10
modules:
  jira:issueGlance:
    - key: hello-world-issue-glance
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World!
      description: A hello world issue glance.
      label: Hello World!
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the issue glance, which is displayed above its label.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `label` | `string` or `i18n object` | Yes | The text shown on the button for the issue glance.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed to the left of the `label` on the issue glance's button.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
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

Dynamic properties are used to dynamically update the `status` properties. If provided in the `manifest.yml` file,
Jira attempts to retrieve the dynamic properties on the initial render of the app. To do this, the `dynamicProperties`
handler function of the app is called. When the issue glance item is clicked, the app renders in the side panel,
where it can perform business logic updates. After the side panel is closed, the handler function
is called to retrieve updates, and then update the `status`.

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
    type: "jira:issueGlance";
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

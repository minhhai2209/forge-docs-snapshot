# Jira issue view background script

The `jira:issueViewBackgroundScript` module adds an invisible container to the
[Issue view page](https://support.atlassian.com/jira-work-management/docs/what-is-the-new-jira-issue-view/).

This makes it the perfect candidate for:

* distributing shared data
* making heavy calculations
* running code without UI elements

## Examples

Use the [events](/platform/forge/custom-ui-bridge/events/) API for communication between
an issue view background script and an issue panel. Because modules may be rendered in a different order, we recommend that you handle both scenarios.

Issue view background script:

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
import { events } from '@forge/bridge';

// Emit the data to an already rendered issue panel
events.emit('app.data-change', 'initial-data');

// Listen to data change requests from issue panels
events.on('app.request-data', (payload) => {
  events.emit('app.data-change', 'initial-or-changed-data');
});
```

Issue panel:

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
import { events } from '@forge/bridge';

// Request data in case the background script is already rendered
events.emit('app.request-data');

// Listen to data change
events.on('app.data-change', (payload) => {
  console.log('The data has changed:', payload)
});
```

### Manifest

```
```
1
2
```



```
modules:
  jira:issueViewBackgroundScript:
    - key: background-t-issue-view-background-script
      resource: issueBgScriptResource
      render: native
  jira:issuePanel:
    - key: issue-background-dashboard-background-script-panel
      title: issue-panel
      viewportSize: medium
      icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
      resource: panelResource
      render: native
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.   *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | Yes | A reference to the static `resources` entry that your context menu app wants to display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | Yes for [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |

## Extension context

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `issue.id` | `string` | The ID of the issue on which the module is rendered. |
| `issue.key` | `string` | The key of the issue on which the module is rendered. |
| `issue.type` | `string` | The type of the issue on which the module is rendered. |
| `issue.typeId` | `string` | The ID of the type of the issue on which the module is rendered. |
| `project.id` | `string` | The ID of the project where the module is rendered. |
| `project.key` | `string` | The key of the project where the module is rendered. |
| `project.type` | `string` | The type of the project where the module is rendered. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Events

Apps can receive frontend events, [emitted by the product](/platform/forge/events-reference/product_events/), that will notify your app when an issue has been changed. These events are triggered when an issue is updated or commented on, and is only available for Jira issue view modules.

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

* UI Kit 1 apps don’t have an event system in place and so aren’t supported.
* There is a delay between the moment the issue is modified and when the event is emitted. It might take up to a few seconds.
* We can’t guarantee that all issue change events will be received by Jira. Therefore, the issue view may sometimes remain stale.
* When the issue is modified by the user who is currently viewing it, it will not be refreshed. This is because we assume the change was made by that same user and there is no need for an update.

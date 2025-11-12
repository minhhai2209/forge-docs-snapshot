# Jira dashboard background script

The `jira:dashboardBackgroundScript` module adds an invisible container to the
[Dashboards page](https://support.atlassian.com/jira-work-management/docs/what-is-a-jira-dashboard/).

Unlike dashboard gadgets, the dashboard background script is not influenced by the dashboard page navigation changes.
This makes it the perfect candidate for:

* distributing shared data
* making heavy calculations
* other optimizations

## Examples

Use the [events](/platform/forge/custom-ui-bridge/events/) API for communication between
dashboard background scripts and dashboard gadgets. Because modules may be rendered in a different order, we recommend that you handle both scenarios.

Dashboard background script:

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

// Emit the data to already rendered dashboard gadgets
events.emit('app.data-change', 'initial-data');

// Listen to data change requests from dashboard gadgets
events.on('app.request-data', (payload) => {
  events.emit('app.data-change', 'initial-or-changed-data');
});
```

Dashboard gadget:

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

// Request the data in case the dashboard background script is already rendered
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
  jira:dashboardBackgroundScript:
    - key: dashboard-bg-script
      resource: dashBgScriptResource
      render: native
  jira:dashboardGadget:
    - key: dashboard-bg-script-gadget
      title: Hello world!
      description: Gadget that talks with background script.
      thumbnail: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
      resource: gadgetResource
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
| `location` | `string` | The full URL of the host page where this module is displayed. |

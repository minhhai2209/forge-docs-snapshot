# Dashboard background script

## Dashboard background script module

The dashboard background script module allows you to run background processes that can:

* Distribute shared data across dashboard widgets
* Perform heavy calculations
* Handle optimizations and data processing
* Communicate with dashboard widgets through events

Unlike dashboard widgets, the background script is not influenced by dashboard page navigation changes, making it perfect for persistent operations.

### Setup instructions

You can create a dashboard widget with background script app with the following steps:

1. Ensure your Jira development or test site is enrolled in the [Developer Canary Program](https://developer.atlassian.com/cloud/jira/platform/developer-canary-program/).
2. Run `forge create` and follow the prompts, selecting the templates under **Dashboards**.
3. Run `forge deploy` to deploy the app.
4. Run `forge install` and follow the prompts to install the app to **Jira**.
5. Once the app is installed, navigate to Jira and go to **Dashboards**.
6. Select **Add widget** and find your widget in the Atlassian Marketplace widget list.
7. Add your widget to the upgraded dashboard to see it in action.

## Examples

Use the [events](/platform/forge/custom-ui-bridge/events/) API for communication between dashboard background scripts and dashboard widgets.

### Basic background script

```
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
```



```
import { events } from "@forge/bridge";

// Emit data to already rendered dashboard widgets
events.emit("app.data-change", "initial-data");

// Listen to data change requests from dashboard widgets
events.on("app.request-data", (payload) => {
  events.emit("app.data-change", "initial-or-changed-data");
});
```
```

```
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
```



```
import { events } from "@forge/bridge";

// Request data in case the background script is already rendered
events.emit("app.request-data");

// Listen to data changes
events.on("app.data-change", (payload) => {
  console.log("The data has changed:", payload);
});
```
```

## Manifest

```
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
```



```
modules:
  dashboards:backgroundScript:
    - key: dashboard-bg-script
      resource: dashBgScriptResource
      render: native

resources:
  - key: dashBgScriptResource
    path: static/dashboard-bg-script/build
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. |
| `resource` | `string` | Yes | The key of a static resources entry that provides the background script implementation. |
| `render` | `'native'` | Yes | Indicates the background script uses native rendering. |

## Extension Data

The background script receives context information about the dashboard environment and can access various APIs for data processing and communication.

## Complete examples

For complete implementation examples, refer to the [Forge sample apps repository](https://developer.atlassian.com/platform/forge/example-apps/).

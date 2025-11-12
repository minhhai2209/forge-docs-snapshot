# Dashboard background script (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://developer.atlassian.com/platform/forge/eap-preview-ga/#early-access-program-eap).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

## Dashboard Background Script module (EAP)

The dashboard background script module allows you to run background processes that can:

* Distribute shared data across dashboard widgets
* Perform heavy calculations
* Handle optimizations and data processing
* Communicate with dashboard widgets through events

Unlike dashboard widgets, the background script is not influenced by dashboard page navigation changes, making it perfect for persistent operations.

### Setup Instructions

You can create a dashboard widget with background script app with the following steps:

1. Run `forge create` and follow the prompts, selecting the templates under **Dashboards (EAP)**.
2. Run `forge deploy` to deploy the app.
3. Run `forge install` and follow the prompts to install the app to **Jira** context (even though it is only available in Atlassian Home).
4. Once the app is installed, navigate to your Atlassian site and go to the Dashboards section in Atlassian Home.
5. Click "Add widget" and find your widget in the Marketplace widget list.
6. Add your widget to the dashboard to see it in action.

## Examples

Use the [events](/platform/forge/custom-ui-bridge/events/) API for communication between dashboard background scripts and dashboard widgets.

### Basic Background Script

```
```
1
2
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

For complete implementation examples, refer to the [Forge sample apps repository](https://developer.atlassian.com/platform/forge/example-apps/) once the EAP is fully available.

## UI Kit Background Script

When using UI Kit for your background script implementation, ensure you're using the latest version that supports the dashboard features.

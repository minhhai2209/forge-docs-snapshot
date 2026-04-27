# Jira Service Management portal request view action

The `jiraServiceManagement:portalRequestViewAction` module adds an option item to the request view action section that shows up request details page on Jira Service Management customer portal.
When the menu item is clicked, the module’s function renders a modal dialog.

This module can be used in Jira Service Management.

Unlicensed user access: This module supports interaction with customer accounts and unlicensed accounts. It does not support anonymous access. For information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users).

When adding this to your app, use it as a top-level component.

![Example of a Portal request view action button](https://dac-static.atlassian.com/platform/forge/snippets/images/portal-request-view-action-location.png?_v=1.5800.1997)

This is an example of the triggered modal dialog:

![Example of a Portal request view with the above sample code](https://dac-static.atlassian.com/platform/forge/snippets/images/portal-request-view-action-demo.png?_v=1.5800.1997)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'small'`, `'medium'`, `'large'` or `'xlarge'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |
| `title` | `string` or `i18n object` | Yes | The title of the issue action, which is displayed as a menu item. The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` | Yes | The URL of the icon that's displayed next to the title. A generic app icon is displayed if no icon is provided. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` and `customer`. This module does not support anonymous access. For more information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `portal.id` | `number` | The id of the service desk where the module is rendered. |
| `request.key` | `string` | The key of the request where the module is rendered. |
| `request.typeId` | `number` | The id of the request type where the module is rendered. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Dynamic module (EAP)

This module can also be declared as a dynamic module. However, this capability is currently only available
as part of Forge’s Early Access Program (EAP).

For more details, see [Dynamic Modules](/platform/forge/apis-reference/dynamic-modules/).

### Code examples

The following examples show Dynamic Module implementations specific to this module. For more detailed information about the API used in these examples
(including error handling information), see [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/).

#### Create a dynamic portal request view action module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const payload = {
  "key": "portal-request-view-action",
  "type": "jiraServiceManagement:portalRequestViewAction",
  "data": {
    "resource": "main",
    "render": "native",
    "title": "Dynamic Request Action",
    "icon": "https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg"
  }
}
const response = await asApp().requestAtlassian(`/forge/installation/v1/dynamic/module/`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'POST',
  body: JSON.stringify(payload),
});
const body = await response.text();
console.log(`Response: ${response.status} ${body}`);
```
```

#### Update a dynamic portal request view action module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const key = "portal-request-view-action";
const payload = {
  "key": "portal-request-view-action",
  "type": "jiraServiceManagement:portalRequestViewAction",
  "data": {
    "resource": "main",
    "render": "native",
    "title": "Dynamic Request Action",
    "icon": "https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg"
  }
}
const response = await asApp().requestAtlassian(`/forge/installation/v1/dynamic/module/${key}`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'PUT',
  body: JSON.stringify(payload)
});
const body = await response.text(); 
console.log(`Response: ${response.status} ${body}`);
```
```

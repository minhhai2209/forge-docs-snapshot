# Jira Service Management portal header

The `jiraServiceManagement:portalHeader` module adds a panel at the top of customer portal pages.
This module can be used in Jira Service Management.

![Example of a portal header](https://dac-static.atlassian.com/platform/forge/snippets/images/portal-header-screen-shot.png?_v=1.5800.2203)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'xsmall'`,`'small'`, `'medium'`, `'large'` or `'xlarge'` |  | The display size of `resource`. Remove this property to enable automatic resizing of the module. |
| `pages` | `help_center`,`portal`, `create_request`, `view_request`, `approvals`,`profile` or `my_requests` |  | Restrict the module to only be visible in specified customer portal pages. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed`, `customer`, and `anonymous`. For more information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `page` | `string` | The location of the page where the module is rendered. Values include `help_center`,`portal`, `create_request`, `view_request`, `approvals`,`profile` and `my_requests`. |
| `portal.id` | `number` | The id of the service desk, depending on the page where it is rendered. |
| `request.typeId` | `number` | The id of the request type, depending on the page where it is rendered. |
| `request.key` | `string` | The key of the request, depending on the page where it is rendered. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Dynamic module (Preview)

This module can also be declared as a dynamic module. However, this capability is currently
available as a Forge *preview* feature.

For more details, see [Dynamic Modules](/platform/forge/apis-reference/dynamic-modules/).

### Code examples

The following examples show Dynamic Module implementations specific to this module. For more detailed information about the API used in these examples
(including error handling information), see [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/).

```
```
1
2
```



```
import { asApp } from "@forge/api";
const payload = {
  "type": "jiraServiceManagement:portalHeader",
  "data": {
    "resource": "main",
    "render": "native",
    "viewportSize": "medium",
    "pages": ["portal", "view_request"]
  }
}
const response = await asApp().requestAtlassian(`/forge/installation/v2/dynamic/module/`, {
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

```
```
1
2
```



```
import { asApp } from "@forge/api";
const key = "portal-header";
const payload = {
  "type": "jiraServiceManagement:portalHeader",
  "data": {
    "resource": "main",
    "render": "native",
    "viewportSize": "medium",
    "pages": ["portal", "view_request"]
  }
}
const response = await asApp().requestAtlassian(`/forge/installation/v2/dynamic/module/${key}`, {
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

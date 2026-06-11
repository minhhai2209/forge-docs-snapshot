# Confluence content action

The `confluence:contentAction` module adds a menu item to the more actions (•••) menu for pages and
blogs. When the menu item is clicked, the module’s function renders a modal dialog.

On apps that use Custom UI, module content is displayed inside a [special Forge iframe](/platform/forge/custom-ui/iframe/) which has the [sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox) attribute configured. This means that HTML links (for example, `<a href="https://domain.tld/path">...</a>`) in this iframe won't be clickable. To make them clickable, use the [router.navigate](/platform/forge/custom-ui-bridge/router/#navigate) API from the `@forge/bridge` package.

![Example of a Content action button](https://dac-static.atlassian.com/platform/forge/snippets/images/content-action-location.png?_v=1.5800.2109)

![Example of a Content action with the above sample code](https://dac-static.atlassian.com/platform/forge/snippets/images/content-action-demo.png?_v=1.5800.2109)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'small'`, `'medium'`, `'large'`, `'xlarge'` or `'max'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |
| `title` | `string` or `i18n object` | Yes | The title of the content action, which is displayed as a menu item.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `keyboardShortcut` | `object` |  | The object that defines a keyboard shortcut to trigger this module. See [keyboard shortcuts](/platform/forge/manifest-reference/keyboard-shortcuts). |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` (Guests Users), and `anonymous`. For more information, see [Access to Forge apps for unlicensed Confluence users](/platform/forge/access-to-forge-apps-for-unlicensed-users/#confluence-forge-modules). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Dynamic module (Preview)

This module can also be declared as a dynamic module. However, this capability is currently
available as a Forge *preview* feature.

For more details, see [Dynamic Modules](/platform/forge/apis-reference/dynamic-modules/).

When you register a dynamic `confluence:contentAction` module, the `data` object uses the same properties as a static `confluence:contentAction` module in the manifest. The module `key` is provided as a top-level property in the Dynamic Modules API payload.

### Code examples

The following examples show Dynamic Module implementations specific to this module. For more detailed information about the API used in these examples
(including error handling information), see [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/).

#### Create a dynamic content action module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const payload = {
  "type": "confluence:contentAction",
  "data": {
    "resolver": {
      "function": "resolver"
    },
    "resource": "main",
    "render": "native",
    "title": "Dynamic content action"
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

#### Update a dynamic content action module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const key = "content-action-dynamic";
const payload = {
  "type": "confluence:contentAction",
  "data": {
    "resolver": {
      "function": "resolver"
    },
    "resource": "main",
    "render": "native",
    "title": "Updated dynamic content action"
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

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
|
| `content.id` | `string` | A string that represents the unique identifier of the `content` object. |
| `content.subtype` | `string` or `null` | A string that represents the subtype of the `content` object. `null` is returned if `subtype` does not apply. |
| `space.id` | `string` | A string that represents the unique identifier of the `space` object. |
| `space.key` | `string` | A string that represents the unique key of the `space` object. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

# Confluence space settings

The `confluence:spaceSettings` module adds a tab inside the integration settings of a Confluence space.
Clicking the tab shows the module's content.

When adding this to your app, use it as a top-level component.

On apps that use Custom UI, module content is displayed inside a [special Forge iframe](/platform/forge/custom-ui/iframe/) which has the [sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox) attribute configured. This means that HTML links (for example, `<a href="https://domain.tld/path">...</a>`) in this iframe won't be clickable. To make them clickable, use the [router.navigate](/platform/forge/custom-ui-bridge/router/#navigate) API from the `@forge/bridge` package.

![Example of the Space settings component](https://dac-static.atlassian.com/platform/forge/snippets/images/space-settings-demo.png?_v=1.5800.1790)

The page URL is constructed in the form of: `/spaces/:spaceKey/settings/apps/:appId/:envId/:route`. You can configure `:route` in the manifest.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the space settings, which is displayed as the title of the tab.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `route` | `string` | Yes | A string of text that makes the URL of the browser more readable. Inside an app, each space settings module must have a distinct `route`.  *Regex:* `^[0-9a-z-]+$` |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `keyboardShortcut` | `object` |  | The object that defines a keyboard shortcut to go to this page. See [keyboard shortcuts](/platform/forge/manifest-reference/keyboard-shortcuts). |

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
| `space.id` | `string` | A string that represents the unique identifier of the `space` object. |
| `space.key` | `string` | A string that represents the unique key of the `space` object. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

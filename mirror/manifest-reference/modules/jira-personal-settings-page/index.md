# Jira personal settings page

|  |  |  |  |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
|
| `resource` | `string` | Required if using [Custom UI](/platform/forge/custom-ui/) or the latest version of [UI Kit.](/platform/forge/ui-kit/) | A reference to the static `resources` entry that your context menu app wants to display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | Yes for [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the global page, which is displayed at the top of the page.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The URL of the icon that displays next to the title. Relative URL's aren't supported. A generic app icon is displayed if no URL is provided. |
| `viewportSize` | `'small'`, `'medium'`, `'large'`, `'xlarge'` or `'max'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |
| `layout` | UI Kit: Custom UI:  * `native` * `blank` * `basic (deprecated)`  (default: `native`) |  | The layout of the global page that defines whether a page is rendered with default controls (native), lays out the entire viewport with a margin on the left and breadcrumbs (basic for UI Kit), or is left blank allowing for full customization (blank for Custom UI). |
| `pages` | `Page[]` |  | The list of subpages to render on the sidebar.  Note that you can only specify `pages` or `sections` but not both. |
| `pages.title` | `string` or `i18n object` | Yes, if using `pages` | The title of the subpage, which is displayed on the sidebar.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `pages.icon` | `string` |  | The URL of the icon that's displayed next to the subpage title. A generic app icon is displayed if no icon is provided. |
| `pages.route` | `string` | Yes, if using `pages` | The unique identifier of the subpage. This identifier is appended to the global page URL. |
| `pages.displayConditions` | `object` |  | The object that defines whether the subpage is displayed in the navigation. The subpage is hidden when the conditions evaluate to false.  See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `sections` | `Section[]` |  | The list of sections to render on the sidebar.  Note that you can only specify `pages` or `sections` but not both. |
| `sections.header` | `string` or `i18n object` |  | The section header.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `sections.pages` | `Page[]` | Yes, if using `sections` | The list of subpages to render on the sidebar. |
| `sections.displayConditions` | `object` |  | The object that defines whether the section is displayed in the navigation. The section, and every subpage it contains, is hidden when the conditions evaluate to false.  The section is also hidden when all of the subpages it contains are hidden.  See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `displayConditions` | `object` |  | The object that defines whether a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

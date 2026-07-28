# Jira Service Management queue page

|  |  |  |  |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the project page, which is displayed at the top of the page. The title also appears as an item in the `Apps` section. You can find the `Apps` section in the left navigation of `Queues` in a service project.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `layout` | UI Kit: Custom UI:  * `native` * `blank` * `basic (deprecated)`  (default: `native`) |  | The layout of the service management queue page that defines whether a page is rendered with default controls (native), lays out the entire viewport with a margin on the left and breadcrumbs (basic for UI Kit), or is left blank allowing for full customization (blank for Custom UI). |

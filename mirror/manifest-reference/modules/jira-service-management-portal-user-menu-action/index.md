# Jira Service Management portal user menu action

|  |  |  |  |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'small'`, `'medium'`, `'large'` or `'xlarge'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |
| `title` | `string` or `i18n object` | Yes | The title of the issue action, which is displayed as a menu item.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` and `customer`. This module does not support anonymous access. For more information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

# Bitbucket project settings menu page

The `bitbucket:projectSettingsMenuPage` module adds an item in the `FORGE APPS` section of the left navigation of Bitbucket project settings menu. When you click the menu item, the content will render on a new Bitbucket page. You can use [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/) to create content for this page.

The page URL is constructed in the form of: `/{workspaceSlug}/projects/{projectKey}/settings/forge/{forgeAppId}/{forgeEnvironmentKey}/{forgeAppModuleKey}`

![Example of a project settings menu page](https://dac-static.atlassian.com/platform/forge/images/bitbucket-project-settings-menu-page.png?_v=1.5800.1790)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the page which is displayed.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `project` | `object` | The project where this page is displayed in. |
| `project.uuid` | `string` | The project [UUID](https://developer.atlassian.com/cloud/bitbucket/rest/intro#universally-unique-identifier) which will be wrapped in `{}`. |
| `project.key` | `string` | The project key. |
| `location` | `string` | The full URL of this page. |

Some Forge APIs (for example, storage API) do not support `{}`. You can use the `unwrapUUid` and
`wrapUuid` functions to convert a Bitbucket resource ID between a wrapped and unwrapped UUID. See
[unwrapUuid/wrapUuid helper functions](https://www.npmjs.com/package/@forge/bitbucket#unwrapuuidwrapuuid)
for more information.

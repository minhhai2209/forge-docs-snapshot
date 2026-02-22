# Bitbucket workspace global page

The `bitbucket:workspaceGlobalPage` module adds an item to the `Apps` section in the Bitbucket navigation bar.
The menu item will be visible in the navigation bar when viewing pages within a workspace context.
When you select the menu item, the content will render in a new page.
You can use the [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/) to create content for this page.

The page URL is constructed in the form of: `/{workspaceSlug}/workspace/forge/{forgeAppId}/{forgeEnvironmentKey}/{forgeAppModuleKey}`

![Example of a workspace global page](https://dac-static.atlassian.com/platform/forge/images/bitbucket-workspace-global-page.png?_v=1.5800.1869)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the page, which is displayed as a menu item.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Example

The snippet below defines a workspace global page using UI Kit. This adds "Hello World UI Kit" to the Apps section in the Bitbucket navigation bar.

```
```
1
2
```



```
modules:
  bitbucket:workspaceGlobalPage:
    - key: hello-world-workspace-global-page
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World UI Kit
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
```
```

The snippet below defines a workspace global page using Custom UI.

```
```
1
2
```



```
modules:
  bitbucket:workspaceGlobalPage:
    - key: hello-world-workspace-global-page
      resource: main
      resolver:
        function: resolver
      title: Hello World Custom UI
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: static/hello-world/build
```
```

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `workspace` | `object` | The workspace where this page is displayed. |
| `workspace.uuid` | `string` | The workspace [UUID](https://developer.atlassian.com/cloud/bitbucket/rest/intro#universally-unique-identifier) which will be wrapped in `{}`. |
| `location` | `string` | The full URL of this page. |

Some Forge APIs (for example, storage API) do not support `{}`. You can use the `unwrapUUid` and
`wrapUuid` functions to convert a Bitbucket resource ID between a wrapped and unwrapped UUID. See
[unwrapUuid/wrapUuid helper functions](https://www.npmjs.com/package/@forge/bitbucket#unwrapuuidwrapuuid)
for more information.

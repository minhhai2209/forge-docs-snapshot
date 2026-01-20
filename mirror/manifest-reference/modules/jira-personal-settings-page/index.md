# Jira personal settings page (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:personalSettingsPage` module adds an item to the user's profile menu in the main navigation. When the item is clicked, content is rendered on a new Jira page.

The page URL is constructed in the following format: `/jira/settings/personal/apps/{appId}/{envId}`

![Example of a personal settings page](https://dac-static.atlassian.com/platform/forge/snippets/images/personal-settings-page.png?_v=1.5800.1785)

## Subpages

By default, the `jira:personalSettingsPage` module registers a top-level page.
However, there is an option to register multiple pages using a `pages` or `sections` field.

Use `pages` to add individual pages to the sidebar and `sections` to group pages.

The sidebar will only change the global page URL, you will need to [handle routes inside your Custom UI app](/platform/forge/add-routing-to-a-full-page-app/) using [view.createHistory()](/platform/forge/custom-ui-bridge/view/#createhistory).

This feature works only with Custom UI.

## Manifest structure

```
```
1
2
```



```
modules {}
└─ jira:personalSettingsPage []
   ├─ key (string) [Mandatory]
   ├─ resource (string) [Mandatory]
   ├─ render (string) [Optional]
   ├─ resolver {} [Optional]
   ├─ title (string | i18n) [Mandatory]
   ├─ icon (string) [Optional]
   ├─ viewportSize (string) [Optional]
   ├─ displayCondition {} [Optional]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```
```

## Properties

| Property | Type | Required | Description |
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
| `sections` | `Section[]` |  | The list of sections to render on the sidebar.  Note that you can only specify `pages` or `sections` but not both. |
| `sections.header` | `string` or `i18n object` |  | The section header.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `sections.pages` | `Page[]` | Yes, if using `sections` | The list of subpages to render on the sidebar. |
| `displayConditions` | `object` |  | The object that defines whether a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension data

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Manifest example

```
```
1
2
```



```
modules:
  jira:personalSettingsPage:
    - key: hello-world-personal-settings-page-module
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World
      icon: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
      viewportSize: medium
```
```

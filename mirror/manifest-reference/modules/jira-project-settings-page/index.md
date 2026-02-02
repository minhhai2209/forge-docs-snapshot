# Jira project settings page

The `jira:projectSettingsPage` module adds an item to the project settings sidebar.

This module can be used in Jira and Jira Service Management.

The page URL is constructed in the following format: `/jira/software/projects/{projectKey}/settings/apps/{appId}/{envId}`

When adding this to your app, use it as a top-level component.

![Example of an project settings page](https://dac-static.atlassian.com/platform/forge/snippets/images/project-settings-page.jpg?_v=1.5800.1808)

## Subpages

By default, the `jira:projectSettingsPage` module registers a top-level page.
However, there is an option to register multiple pages using a `pages` or `sections` field.

Use `pages` to add individual pages to the sidebar and `sections` to group pages.

The sidebar will only change the project settings page URL, you will need to [handle routes inside your Custom UI app](/platform/forge/add-routing-to-a-full-page-app/) using [view.createHistory()](/platform/forge/custom-ui-bridge/view/#createhistory).

This feature works only with Custom UI.

![Example of a subpage](https://dac-static.atlassian.com/platform/forge/snippets/images/project-settings-subpage.jpg?_v=1.5800.1808)

## Manifest example

```
```
1
2
```



```
modules:
  jira:projectSettingsPage:
    - key: hello-world-project-settings-page
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the project settings page, which is displayed at the top of the page. The title also appears as an item in the `Project settings` section of the left navigation of Jira settings.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `layout` | UI Kit: Custom UI:  * `native` * `blank` * `basic (deprecated)`  (default: `native`) |  | The layout of the project settings page that defines whether a page is rendered with default controls (native) or lays out the entire viewport with margin on the left and breadcrumbs (basic for UI Kit) or taking the 100% of the page (blank for Custom UI). |
| `pages` | `Page[]` | You can only specify `pages` or `sections` but not both. | The list of subpages to render on the sidebar. |
| `sections` | `Section[]` | The list of sections to render on the sidebar. |
| `displayConditions` | `object` |  | The object that defines whether a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

### Page

#### Manifest example

```
```
1
2
```



```
modules:
  <module-name>:
    - key: hello-world-jira-module-page-example
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World
      pages:
        - title: page example
          route: page-example-1
          icon: https://example.com/icon.png
```
```

#### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | `string` or `i18n object` | Yes | The title of the subpage, which is displayed on the sidebar.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The URL of the icon that's displayed next to the subpage title. A generic app icon is displayed if no icon is provided. |
| `route` | `string` | Yes | The unique identifier of the subpage. This identifier is appended to the project settings page URL. |

### Section

#### Manifest example

```
```
1
2
```



```
modules:
  <module-name>:
    - key: hello-world-jira-module-section-example
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World
      sections:
        - header: example section
          pages:
            - title: page example
              route: page-example-1
              icon: https://example.com/icon.png
```
```

#### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `header` | `string` or `i18n object` |  | The section header.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `pages` | `Page[]` | Yes | The list of subpages to render on the sidebar. |

## Extension data

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `project.id` | `string` | The ID of the project where the module is rendered. |
| `project.key` | `string` | The key of the project where the module is rendered. |
| `project.type` | `string` | The type of the project where the module is rendered. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

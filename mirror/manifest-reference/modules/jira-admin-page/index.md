# Jira admin page

The `jira:adminPage` module adds an item in the Apps section of the left navigation of Jira admin
settings. When the item is clicked, content is rendered on a new Jira page.

This module can be used in Jira and Jira Service Management.

The page URL is constructed in the following format: `/jira/settings/apps/{appId}/{envId}`

When adding this to your app, use it as a top-level component.

![Example of an admin page](https://dac-static.atlassian.com/platform/forge/snippets/images/admin-page.jpg?_v=1.5800.1771)

To organize your Jira admin space and simplify the app management, create [Configure](#configure-page) and [Get started](#get-started-page) pages.

### Configure page

On the Configure page, you can store your app’s configure settings.

The page URL is constructed in the following format: `/jira/settings/apps/configure/{appId}/{envId}`

To create this page, use the `useAsConfig` property.

When it’s set to `true`, it creates a Configure button that leads to this page from the app's entry in **Manage Apps**.

![Example of a configure button in Manage Apps](https://dac-static.atlassian.com/platform/forge/snippets/images/configure-button-manage-apps.png?_v=1.5800.1771)

The `jira:adminPage` entry with the `useAsConfig` property won't be displayed on the sidebar.

Related: [Configuring apps](https://confluence.atlassian.com/upm/configuring-apps-273875766.html)

### Get started page

On the Get started page, you can provide information on how to start using your app.

The page URL is constructed in the following format: `/jira/settings/apps/get-started/{appId}/{envId}`

To create this page, use the `useAsGetStarted` property.

When it’s set to `true`, it creates a Get started button that leads to this page from the app's entry in **Manage Apps**.

![Example of a get started button in Manage Apps](https://dac-static.atlassian.com/platform/forge/snippets/images/get-started-button-manage-apps.png?_v=1.5800.1771)

The `jira:adminPage` entry with the `useAsGetStarted` property won’t be displayed on the sidebar.

Related: [Manage your apps](https://confluence.atlassian.com/upm/viewing-installed-apps-273875714.html)

## Subpages

By default, the `jira:adminPage` module registers a top-level page.
However, you can register multiple pages using the `pages` and `sections` properties.

Use `pages` to add individual pages to the sidebar and `sections` to group pages.

![Example of an admin page](https://dac-static.atlassian.com/platform/forge/snippets/images/subpages-admin.jpg?_v=1.5800.1771)

The sidebar will only change the admin page URL, you'll need to
[handle routes inside your Custom UI app](/platform/forge/add-routing-to-a-full-page-app/)
using [view.createHistory()](/platform/forge/custom-ui-bridge/view/#createhistory).

### Limitations

Subpages only work with Custom UI.

Subpages are not supported by the [Configure](#configure-page) and [Get started](#get-started-page) pages.

## Validation rules

Take into account the following validation rules when creating a `jira:adminPage` entry:

* the `jira:AdminPage` module can only have a single entry that doesn’t include either `useAsConfig` or `useAsGetStarted` properties.
* the `jira:AdminPage` module can only have a single entry that includes either `useAsConfig` or `useAsGetStarted` property.
* the `jira:AdminPage` entry that includes either `useAsConfig` or `useAsGetStarted` properties can’t include either `pages` or `sections`.

You'll see an error message if these aren't followed.

## Manifest example

The `jira:adminPage` module example containing both **Configure** and **Get Started** pages:

```
```
1
2
```



```
modules:
  jira:adminPage:
    - key: admin-page-example-hello-world-admin-page
      resource: main-admin-page
      title: Admin page example
      render: native
      resolver:
        function: resolver
    - key: admin-page-example-hello-world-configure-page
      resource: main-configure-page
      title: Configure page example
      render: native
      resolver:
        function: resolver
      useAsConfig: true
    - key: admin-page-example-hello-world-get-started-page
      resource: main-get-started-page
      title: Get started page example
      render: native
      resolver:
        function: resolver
      useAsGetStarted: true
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main-admin-page
    path: src/frontend/main-admin-page.jsx
  - key: main-configure-page
    path: src/frontend/main-configure-page.jsx
  - key: main-get-started-page
    path: src/frontend/main-get-started-page.jsx
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the admin page, which is displayed at the top of the page. The title also appears as an item in the Apps section of the left navigation of Jira admin settings.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `layout` | UI Kit: Custom UI:  * `native` * `blank` * `basic (deprecated)`  (default: `native`) |  | The layout of the admin page that defines whether a page is rendered with default controls (native), lays out the entire viewport with a margin on the left and breadcrumbs (basic for UI Kit), or is left blank allowing for full customization (blank for Custom UI). |
| `useAsConfig` | `boolean` |  | See the description [here](#configure-page). |
| `useAsGetStarted` | `boolean` |  | See the description [here](#get-started-page). |
| `pages` | `Page[]` | You can only specify `pages` or `sections` but not both. | The list of subpages to render on the sidebar. |
| `sections` | `Section[]` | The list of sections to render on the sidebar. |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |

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
| `route` | `string` | Yes | The unique identifier of the subpage. This identifier is appended to the admin page URL. |

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
| `location` | `string` | The full URL of the host page where this module is displayed. |

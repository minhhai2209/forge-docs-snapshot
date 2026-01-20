# Jira project page

The `jira:projectPage` module adds the app in the horizontal tab navigation in Jira.

For Jira Service Management, you can access the app within the Jira Service Management project in the left navigation.

The page URL is constructed in the form of: `/jira/{projectType}/projects/{projectKey}/apps/{appId}/{envId}`

This module can be used in Jira and Jira Service Management.

When adding this to your app, use it as a top-level component.

![Example of a project page](https://dac-static.atlassian.com/platform/forge/snippets/images/project-page.jpg?_v=1.5800.1783)

![Example of a project page - JSM](https://dac-static.atlassian.com/platform/forge/snippets/images/project-page-jsm.jpg?_v=1.5800.1783)

## Subpages

By default, the `jira:projectPage` module registers a top-level page.
However, you can create **multiple subpages** using either a `pages` or `sections` field to organize your app's functionality.

Use `pages` to add individual pages to the app and `sections` to group related pages together.

This configuration only changes the project page URL structure. You must [handle routes inside your Custom UI app](/platform/forge/add-routing-to-a-full-page-app/) using [view.createHistory()](/platform/forge/custom-ui-bridge/view/#createhistory) for proper navigation.

This subpage feature works only with Custom UI applications.

## Manifest example

```
```
1
2
```



```
modules:
  jira:projectPage:
    - key: hello-world-project-page
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World!
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the project page, which is displayed at the top of the page. The title also appears in the horizontal tab navigation in Jira.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `layout` | UI Kit: Custom UI:  * `native` * `blank` * `basic (deprecated)`  (default: `native`) |  | The layout of the project page that defines whether a page is rendered with default controls (native), lays out the entire viewport with a margin on the left and breadcrumbs (basic for UI Kit), or is left blank allowing for full customization (blank for Custom UI). |
| `pages` | `Page[]` | You can only specify `pages` or `sections` but not both. | The list of subpages to render in the app. |
| `sections` | `Section[]` | The list of sections to render in the app. |
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
| `route` | `string` | Yes | The unique identifier of the subpage. This identifier is appended to the project page URL. |

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
| `pages` | `Page[]` | Yes | The list of subpages to render within the app. |

## Extension data

### UI Kit and Custom UI

Your Jira project page can **access contextual project information** through extension data. Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit applications or the [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) bridge method in Custom UI applications.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `project.id` | `string` | The id of the project where the module is rendered. |
| `project.key` | `string` | The key of the project where the module is rendered. |
| `project.type` | `string` | The type of the project where the module is rendered. |
| `board.id` | `string` | The id of the board where the module is rendered.  Only for Jira Software |
| `board.type` | `"simple" | "scrum" | "kanban"` | The type of the board where the module is rendered.  Only for Jira Software |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Frequently asked questions

### How do I create a Jira project page?

Add the `jira:projectPage` module to your Forge app's manifest:

```
```
1
2
```



```
modules:
  jira:projectPage:
    - key: hello-world-project-page
      resource: main
      resolver:
        function: resolver
      render: native
      title: Hello World!
```
```

Using UI Kit with `render: native` ensures your page has the proper Jira look and feel. UI Kit offers a wide range of pre-built and customizable components that align with Atlassian's design standards.

### What's the difference between pages and sections in subpages?

* **Pages**: Individual subpages that appear directly in your app's navigation
* **Sections**: Groups of pages organized under section headers for better organization
* You can only use either `pages` OR `sections`, not both in the same module

### Can I use custom icons for my project page?

Yes, you can specify a custom icon using the `icon` property. Provide a URL to your icon image. If no icon is specified, a generic app icon will be displayed.

### What layout options are available for project pages?

The `layout` property supports:

* **UI Kit**: `native` (default) or `basic`
* **Custom UI**: `native` (default), `blank`, or `basic` (deprecated)
  The layout of the project page defines whether a page is rendered with default controls (native), lays out the entire viewport with a margin on the left and breadcrumbs (basic for UI Kit), or is left blank allowing for full customization (blank for Custom UI).

#### UI Kit Layouts

* `native`: Includes all default Jira project page controls and navigation elements
* `basic`: Provides a simplified layout with left margin, breadcrumbs, and minimal controls

#### Custom UI Layouts

* `native`: Includes standard Jira project page chrome and navigation
* `blank`: Provides a completely empty canvas for full viewport customization
* `basic`: (Deprecated) Similar to UI Kit's basic layout with left margin and breadcrumbs

### How do I handle routing in subpages?

For subpages to work properly, you need to:

1. Define `pages` or `sections` in your manifest
2. Implement routing in your Custom UI app using `view.createHistory()`

```
```
1
2
```



```
import { view } from "@forge/bridge";

const history = await view.createHistory();

// e.g. URL begins as http://example.atlassian.net/example/apps/abc/123

history.push("/page-1");
// this updates the URL to http://example.atlassian.net/example/apps/abc/123/page-1

history.push("/page-2");
// this updates the URL to http://example.atlassian.net/example/apps/abc/123/page-2

history.go(-2);
// this updates the URL to http://example.atlassian.net/example/apps/abc/123
```
```

3. Each page's `route` property becomes part of the URL path

### Can I restrict when my project page appears?

Yes, use the [displayConditions](/platform/forge/manifest-reference/display-conditions/) property to control when your module is visible. This allows you to show the page only in specific project types or under certain conditions.

### Is the project page module compatible with Jira Service Management?

Yes, the `jira:projectPage` module works in both Jira Software and Jira Service Management. In JSM, the page appears in the left navigation panel.

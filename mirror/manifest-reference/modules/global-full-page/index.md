# Global full page (Preview)

Isolated Cloud and Atlassian Government Cloud (AGC) are not yet supported but will be added in the near future.

The full page module allows you to create fully customised app experiences.
Full page modules occupy the entire web page, providing ample space to deliver UI for a broader range of use cases,
such as specialised content views or internal tools that reflect your own branding.

The `global:fullPage` module delivers an immersive full-page experience separate from Atlassian core app UIs.

To use the `global:fullPage` module:

1. Your app must declare a required Atlassian app through the [`compatibility`](/platform/forge/app-compatibility/#multiple-app-compatibility) property in your app manifest. At least one Atlassian app must have `required: true`.
2. Install your app in a site that has the required Atlassian app.

## Manifest structure

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
modules []
└─ global:fullPage {}
   ├─ key (string) [Mandatory]
   ├─ resource (string) [Mandatory]
   ├─ routePrefix (string) [Mandatory]
   ├─ render (string) [Mandatory for UI Kit only]
   ├─ resolver {} [Optional]
   ├─ title {} [Optional]
   └─ icon {} [Optional]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]

app {}
├─ id (string) [Required]
├─ runtime {} [Required]
└─ compatibility {} [Required]
```

## Example manifest

```
```
1
2
```



```
modules:
  global:fullPage:
    - key: my-app
      resource: main
      routePrefix: route-prefix
      render: native
      resolver:
        function: resolver
      title: My App
      icon: resource:icons;icon.svg
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
  - key: icons
    path: icons
app:
  runtime:
    name: nodejs22.x
    memoryMB: 256
    architecture: arm64
  compatibility:
    confluence:
      required: true
    jira:
      required: false
  id: ari:cloud:ecosystem::app/your-app-id
```
```

### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `routePrefix` | `string` | Yes | Unique route identifier for a module. This serves as the entry point for each module. Within an app, each full page module must have a distinct `routePrefix`.  *Regex:* `^[a-z0-9\\-]+$` |
| `title` | `string` | No | The title of the full page, which is displayed in the tab title. |
| `icon` | `string` | No | The icon to use as the favicon for the page.  For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |

## Compatibility

Your app must declare a required Atlassian app in the manifest:

```
```
1
2
```



```
app:
  compatibility:
    confluence:
      required: true
    jira:
      required: false
```
```

The required Atlassian app determines where your app is installed, how it is licensed, and who can access it.
Optional Atlassian apps let your app connect to additional Atlassian apps after installation; users choose whether
to enable these connections.

| Property | Description |
| --- | --- |
| `required: true` | The Atlassian app must be present for the app to be installed. Licensing is inherited from this Atlassian app. |
| `required: false` | The Atlassian app connection is optional. Users can link the app to this Atlassian app after installation. |

For more details on declaring compatibility, see [App compatibility](/platform/forge/app-compatibility/).

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Access your app

Full page modules can be accessed using this URL format:

```
```
1
2
```



```
{site-hostname}/apps/full-page/{installation-id}/{route-prefix}/{app-route}
```
```

**Where to find each value:**

* **`<site-hostname>`**: Your site name
* **`<installation-id>`**: The UUID of the app installation. Run `forge install list` to find the UUID of the desired installation.
* **`<route-prefix>`**: Defined in your manifest under `routePrefix`
* **`<app-route>`**: Optional — if your app code contains routing, it will appear under the `<app-route>` section of the URL.

**Example:**

```
```
1
2
```



```
https://example.atlassian.net/apps/full-page/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/route-prefix
```
```

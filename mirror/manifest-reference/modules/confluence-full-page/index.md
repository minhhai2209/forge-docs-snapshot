# Confluence full page (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The full page module allows you to create fully customised app experiences.
Full page modules occupy the entire web page, providing ample space to deliver UI for a broader range of use cases,
such as specialised content views or internal tools that reflect your own branding.

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
modules []
└─ confluence:fullPage {}
   ├─ key (string) [Mandatory]
   ├─ resource (string) [Mandatory]
   ├─ routePrefix (string) [Mandatory]
   ├─ render (string) [Mandatory for UI Kit only]
   ├─ resolver {} [Optional]
   ├─ title {} [Optional]
   ├─ icon {} [Optional]
   └─ unlicesedAccess (string[]) [Optional]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `routePrefix` | `string` | Yes | Unique route identifier for a module. This serves as the entry point for each module. Within an app, each full page module must have a distinct `routePrefix`.  *Regex:* `^[a-z0-9\\-]+$` |
| `title` | `string` or `i18n object` | No | The title of the full page, which is displayed in the tab title.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` | No | The icon to represent the app in the logo and app switcher dropdown.  For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` (Guests Users), and `anonymous`. For more information, see [Access to Forge apps for unlicensed Confluence users](/platform/forge/access-to-forge-apps-for-unlicensed-users/#confluence-forge-modules). |

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
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Accessing Confluence full page module

Full page modules can be accessed using this URL format:

```
```
1
2
```



```
https://<your-site>.atlassian.net/forge-apps/a/<app-id>/e/<forge-environment-id>/r/<route-prefix>/<app-route>
```
```

**Where to find each value:**

* **`<your-site>`**: Your site name
* **`<app-id>`**: The UUID from your `app.id` in `manifest.yml` (if in ARI format like `ari:cloud:ecosystem::app/UUID`, use only the UUID section)
* **`<forge-environment-id>`**: The UUID of the environment that the app is installed on.
  Run `forge environments list` to find the UUID of the desired environment.
* **`<route-prefix>`**: Defined in your manifest under `routePrefix`
* **`<app-route>`**: Optional - if your app code contains routing, it will appear under the `<app-route>` section of the URL.

**Example:**

```
```
1
2
```



```
https://example.atlassian.net/forge-apps/a/21e590df-79e6-40dd-9ee4-ba2c7b678f26/e/9f699e8b-33f1-4fa7-bd48-c5fdc44fa4c2/r/ui-kit
```
```

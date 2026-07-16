# global:ui module (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.

To join the EAP for `global:ui`, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/19016?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzgyMzUxNTgzNDkwIiwic291cmNlIjoiY29uZmx1ZW5jZSJ9).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The `global:ui` module gives your Forge app its own end-to-end experience within the Atlassian
platform. It provides a side navigation bar and a main content area that users access directly from
the Atlassian app switcher.

To use the `global:ui` module:

1. Your app must declare a required Atlassian app through the [`compatibility`](/platform/forge/app-compatibility/#multiple-app-compatibility)
   section of the manifest.
2. Your app must use the [`global:ui` UI Kit components](/platform/forge/global-ui/ui-kit-components/).

## Manifest structure

To use `global:ui`, the manifest has two key parts:

1. A `compatibility` section in `app` with at least one Atlassian app set to `required: true`.
2. A `global:ui` entry in the `modules` section that defines the module entry point.

```
```
1
2
```



```
modules []
└─ global:ui {}
   ├─ key (string) [Required]
   ├─ resource (string) [Required]
   ├─ render (string) [Required - must be native]
   ├─ resolver {} [Optional]
   ├─ title (string | i18n object) [Required]
   └─ icon (string) [Optional]

app {}
├─ id (string) [Required]
├─ runtime {} [Required]
└─ compatibility {} [Required]
```
```

## Example manifest

```
```
1
2
```



```
modules:
  global:ui:
    - key: my-app
      resource: main
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
permissions:
  content:
    styles:
      - "unsafe-inline"
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

## Properties

### `key`

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A unique key that identifies this module within the app. Must be unique across all modules in the manifest. |

### `resource`

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | Yes | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources/) for more details. |

### `render`

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `render` | `string` | Yes | The rendering method for the module. Must be set to `native`, which enables UI Kit rendering. Custom UI is not supported for `global:ui`. The platform enforces a UI chrome around the module and UI Kit is the public API that lets you control it. To embed custom web content in the main content area, use the [`Frame`](/platform/forge/ui-kit/components/frame/) component inside `<Main>`. |

### `resolver`

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `resolver` | `object` | No | An optional object that specifies a resolver for back-end data access. Set the `function` property if you are using a hosted `function` module for your resolver. Set the `endpoint` property if you are using [Forge Remote](/platform/forge/remote/remote-overview/) to integrate with a remote back end. |

### `title`

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | `string` or i18n object | Yes | The display name for your app. Shown in the Atlassian app switcher and in the top navigation bar. |

To provide localized titles, use an i18n object:

```
```
1
2
```



```
title:
  i18n:
    default: My App
    es: Mi aplicación
```
```

### `icon`

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `icon` | `string` | No | A reference to a local SVG resource for your app icon, in the format `resource:<resource-key>;<filename>`. Displayed at 24×24px in the sidenav header and 32×32px in the app switcher. Requires a corresponding entry in the `resources` section. |

The following example configures an icon:

```
```
1
2
```



```
modules:
  global:ui:
    - key: my-app
      icon: resource:icons;icon.svg
resources:
  - key: icons
    path: icons # directory containing icon.svg
```
```

## Compatibility

The `compatibility` section in your manifest declares which Atlassian apps your app connects to.
This section is required for `global:ui`, and one Atlassian app must be set to `required: true`.

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

## Access your app

Users access the `global:ui` module from the site-level app switcher. During the EAP, the app launches
on an existing site hostname using the following URL format:

```
```
1
2
```



```
{site-hostname}/apps/a/{app-id}/e/{env-id}
```
```

The URL format shown above is the current EAP format and may change
in a later phase. Avoid hard-coding URLs in your app.

## Add or remove the global:ui module

You can add or remove the `global:ui` module from your app without triggering a [major version](/platform/forge/versions/#major-version-upgrades).

Removing the `global:ui` module from a deployed app removes access to the app entirely. Make sure this
is intentional before you deploy.

# global:ui module (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.

To join the EAP for `global:ui`, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/19016?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzgyMzUxNTgzNDkwIiwic291cmNlIjoiY29uZmx1ZW5jZSJ9).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The `global:ui` module gives your Forge app its own end-to-end experience within the Atlassian
platform. It provides a side navigation bar and a main content area that users access directly from
the Atlassian app switcher.

To build this experience, you must use the [`global:ui` UI Kit components](/platform/forge/global-ui/ui-kit-components/).

## Manifest structure

To use `global:ui`, add a `global:ui` entry to the `modules` section of your manifest.

```
1modules []
2└─ global:ui {}
3   ├─ key (string) [Required]
4   ├─ resource (string) [Required]
5   ├─ render (string) [Required - must be native]
6   ├─ resolver {} [Optional]
7   ├─ title (string | i18n object) [Required]
8   ├─ icon (string) [Optional]
9   └─ emitsReadyEvent (boolean) [Optional]
10
```

## Example manifest

```
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
19
20
21
22
23
24
25
26
27
28
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
  id: ari:cloud:ecosystem::app/your-app-id
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A unique key that identifies this module within the app. Must be unique across all modules in the manifest. |
| `resource` | `string` | Yes | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources/) for more details. |
| `render` | `string` | Yes | The rendering method for the module. Must be set to `native`, which enables UI Kit rendering. Custom UI is not supported for `global:ui`. The platform enforces a UI chrome around the module and UI Kit is the public API that lets you control it. To embed custom web content in the main content area, use the [`Frame`](/platform/forge/ui-kit/components/frame/) component inside `<Main>`. |
| `resolver` | `object` | No | An optional object that specifies a resolver for back-end data access. Set the `function` property if you are using a hosted `function` module for your resolver. Set the `endpoint` property if you are using [Forge Remote](/platform/forge/remote/) to integrate with a remote back end. |
| `title` | `string` or i18n object | Yes | The display name for your app. Shown in the Atlassian app switcher and in the top navigation bar. |
| `icon` | `string` | No | A reference to a local SVG resource for your app icon, in the format `resource:<resource-key>;<filename>`. Displayed at 24×24px in the sidenav header and 32×32px in the app switcher. Requires a corresponding entry in the `resources` section. |
| `emitsReadyEvent` | `boolean` | No | Defaults to `false`. When `true`, the platform continues to show the initial loading screen with your app logo until your app code calls [`view.emitReadyEvent()`](/platform/forge/apis-reference/ui-api-bridge/view/#emitreadyevent). Use this when your app needs to load data or finish rendering before users see it. If your app doesn't call `view.emitReadyEvent()`, the loading screen is removed after a default timeout of 10 seconds. |

### i18n object

To provide localized titles, use an i18n object:

```
```
1
2
3
4
5
```



```
title:
  i18n:
    default: My App
    es: Mi aplicación
```
```

### Show the loading screen until your app is ready

The following example keeps the loading screen visible until the app calls `view.emitReadyEvent()`:

```
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
      emitsReadyEvent: true
  function:
    - key: resolver
      handler: index.handler
```
```

```
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
19
20
21
22
23
24
25
26
27
28
29
30
31
```



```
import React, { useEffect, useState } from "react";
import ForgeReconciler, { Text } from "@forge/react";
import { invoke, view } from "@forge/bridge";

const App = () => {
  const [summary, setSummary] = useState();

  useEffect(() => {
    const loadData = async () => {
      try {
        setSummary(await invoke("getSummary"));
      } catch (error) {
        console.error("Failed to load summary:", error);
      } finally {
        // Notify the platform even if loading fails, so the loading screen is removed.
        await view.emitReadyEvent();
      }
    };

    loadData();
  }, []);

  return <Text>{summary ?? "No summary available."}</Text>;
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```
```

### Icon example

The following example configures an icon:

```
```
1
2
3
4
5
6
7
8
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

## Access your app

Users access the `global:ui` module from the site-level app switcher. During the EAP, the app launches
on an existing site hostname using the following URL format:

```
```
1
2
```



```
{site-hostname}/apps/{installation-id}
```
```

The URL format shown above is the current EAP format and may change
in a later phase. Avoid hard-coding URLs in your app.

## Add or remove the global:ui module

You can add or remove the `global:ui` module from your app without triggering a [major version](/platform/forge/versions/#major-version-upgrades).

Removing the `global:ui` module from a deployed app removes access to the app entirely. Make sure this
is intentional before you deploy.

# global:ui UI Kit components (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials", as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.

To join the EAP for `global:ui`, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/19016?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzgyMzUxNTgzNDkwIiwic291cmNlIjoiY29uZmx1ZW5jZSJ9).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The global UI Kit components provide the navigation experience for your app. They deliver a complete
layout with a header, sidebar navigation, and main content area that integrates with the Atlassian
platform.

You can only use the `Global` component inside the [`global:ui` module](/platform/forge/global-ui/global-ui-module/).

These UI Kit components are exported from the `@forge/react/global` entry point.

## Import

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
import {
  Global,
  Sidebar,
  LinkMenuItem,
  FlyOutMenuItem,
  ExpandableMenuItem,
  ReorderableMenuItems,
  HelpLink,
  PersonalSettings,
  PersonalSettingsItem,
  CreateButton,
  CreateMenuItem,
  Main,
} from "@forge/react/global";
```

## Component hierarchy

The `Global` component is composed of sub-components that work together to create the full layout:

```
```
1
2
```



```
<Global>
├─ <HelpLink />
│
├─ <CreateButton />
│  └─ <CreateMenuItem />
│
├─ <PersonalSettings />
│  └─ <PersonalSettingsItem />
│
├─ <Sidebar />
│  ├─ <LinkMenuItem />
│  │
│  ├─ <ReorderableMenuItems />
│  │
│  ├─ <FlyOutMenuItem />
│  │  └─ <LinkMenuItem />
│  │
│  └─ <ExpandableMenuItem />
│     └─ <LinkMenuItem />
│
└─ <Main />
   └─ {Your app content}
```
```

Both `<Sidebar>` and `<Main>` must be present as direct children of `<Global>`.

## Layout areas

The component renders three layout areas:

1. **Header** — Rendered automatically by the platform. Includes your app branding, the search
   component, Rovo Chat, profile, and settings. You do not configure the header in code; it uses
   properties from your manifest.
2. **Sidebar** — The left navigation panel. You configure the menu items using `Sidebar`,
   `LinkMenuItem`, `ExpandableMenuItem`, and related components.
3. **Main content** — The central area for your app's primary content, wrapped in `<Main>`.

## Props

### `Global`

The root component that wraps the full layout.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeElement` | Yes | Accepts `HelpLink`, `CreateButton`, `PersonalSettings`, `Sidebar`, and `Main`. |

Renders the left navigation panel.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeElement` | Yes | Accepts `LinkMenuItem`, `ExpandableMenuItem`, `FlyOutMenuItem`, and `ReorderableMenuItems`. |

A clickable navigation link in the sidebar.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | The text displayed for the menu item. |
| `href` | `string` | Yes | The route this item navigates to. |

### `ExpandableMenuItem`

An expandable menu item that reveals nested links when selected.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | The text displayed for the expandable menu item. |
| `children` | `ForgeElement` | Yes | Accepts `LinkMenuItem`, `ExpandableMenuItem` (can be nested up to 3 levels), and `ReorderableMenuItems`. |

A sidebar item that opens a flyout containing nested menu items.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | The text displayed for the flyout menu item. |
| `children` | `ForgeElement` | Yes | Accepts nested sidebar menu items, such as `LinkMenuItem`. |

Groups sidebar menu items that users can reorder. Use this when your app supports a customizable
navigation order.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `items` | `{ id: string; label: string; href: string }[]` | Yes | An array of sidebar menu items that the user can reorder. Each item must include a unique `id`, a display `label`, and a navigation `href`. |
| `onReorder` | `(items: Item[]) => void` | Yes | A callback invoked after the user changes the item order. Receives the reordered items so the app can update local state or persist the new order. |
| `onError` | `(error: Error, currentItems: Item[], nextItems: Item[]) => void` | No | A callback invoked when reordering fails. Receives the error, the current items before the attempted reorder, and the next items from the attempted reorder. |

### `Main`

Wraps your app's main content area.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeElement` | Yes | Your app's main content. |

### `HelpLink`

Renders a help link in the app header. Use it to direct users to support, documentation, or other
help resources for your app.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `href` | `string` | Yes | The URL opened when the help link is selected. |

### `PersonalSettings`

Renders a personal settings menu in the app header. Use it to group user-specific settings and
account actions.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeElement` | Yes | Accepts `PersonalSettingsItem` components. |

### `PersonalSettingsItem`

Renders an item inside the personal settings menu.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | The text displayed for the settings item. |
| `onClick` | `() => void` | Yes | The handler called when the item is selected. |

### `CreateButton`

Renders a create button in the app header. Use it to expose one or more create actions for your app.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeElement` | Yes | Accepts `CreateMenuItem` components. |

Renders an item inside the create menu.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | The text displayed for the create action. |
| `onClick` | `() => void` | Yes | The handler called when the item is selected. |

The header is rendered automatically. You do not configure it in code. It uses the following
properties from your manifest:

| Manifest property | Description |
| --- | --- |
| `title` | Displayed in the header next to your app icon. Also appears in the Atlassian app switcher. |
| `icon` | A reference to a local SVG resource, in the format `resource:<resource-key>;<filename>`. Displayed as a 24×24px icon in the header. In smaller viewports, only the icon is shown. |

The header automatically includes:

* **App name and logo** — From your manifest `title` and `icon`. Selecting it navigates to the root
  route (`/`).
* **Search** — Lets users search content indexed by the platform. Search indexes content from any
  Atlassian app your app is linked to.
* **Settings** — A dropdown for app admins to access the manage apps console.
* **Rovo Chat** — Opens the Rovo AI chat sidebar.
* **Profile** — Opens the user's profile and account settings.

For details on configuring `title` and `icon`, see the [`global:ui` module reference](/platform/forge/global-ui/global-ui-module/).

## Requirements and limitations

* `<Sidebar>` and `<Main>` must both be present as direct children of `<Global>`.

## Usage example

The following example assembles a complete app layout with header actions, sidebar navigation,
and main content:

```
```
1
2
```



```
import React, { useState } from "react";
import ForgeReconciler, { Button, Text } from "@forge/react";
import {
  Global,
  Sidebar,
  LinkMenuItem,
  ExpandableMenuItem,
  HelpLink,
  PersonalSettings,
  PersonalSettingsItem,
  ReorderableMenuItems,
  CreateButton,
  CreateMenuItem,
  FlyOutMenuItem,
  Main,
} from "@forge/react/global";

const initialNotes = [
  { id: "1", label: "Document 1", href: "/notes/1" },
  { id: "2", label: "Document 2", href: "/notes/2" },
  { id: "3", label: "Document 3", href: "/notes/3" },
];

const App = () => {
  const [notes, setNotes] = useState(initialNotes);
  const [message, setMessage] = useState(
    "Select an action from the header or sidebar."
  );

  const handleCreateDocument = () => {
    setMessage("Create document selected.");
  };

  const handleCreateFolder = () => {
    setMessage("Create folder selected.");
  };

  return (
    <Global>
      <HelpLink href="https://support.atlassian.com/" />

      <CreateButton>
        <CreateMenuItem
          label="Create document"
          onClick={handleCreateDocument}
        />
        <CreateMenuItem label="Create folder" onClick={handleCreateFolder} />
      </CreateButton>

      <PersonalSettings>
        <PersonalSettingsItem
          label="Notification preferences"
          onClick={() => {}}
        />
        <PersonalSettingsItem label="Preferences" onClick={() => {}} />
      </PersonalSettings>

      <Sidebar>
        <LinkMenuItem label="Home" href="/" />
        <LinkMenuItem label="Recent" href="/recent" />

        <ExpandableMenuItem label="Projects">
          <LinkMenuItem label="Project Alpha" href="/projects/alpha" />
          <LinkMenuItem label="Project Beta" href="/projects/beta" />
        </ExpandableMenuItem>

        <FlyOutMenuItem label="Resources">
          <LinkMenuItem label="Documentation" href="/resources/docs" />
          <LinkMenuItem label="Templates" href="/resources/templates" />
        </FlyOutMenuItem>

        <ReorderableMenuItems
          items={notes}
          onReorder={(items) => {
            setNotes(items);
            setMessage("Sidebar order changed.");
          }}
          onError={(error, currentItems, nextItems) => {
            console.error("Failed to persist sidebar order:", error);
          }}
        />
      </Sidebar>

      <Main>
        <Text>{message}</Text>
        <Button onClick={() => setMessage("Main content action selected.")}>
          Run action
        </Button>
      </Main>
    </Global>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

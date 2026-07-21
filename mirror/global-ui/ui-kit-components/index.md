# global:ui UI Kit components (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
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
2. **Sidebar** — The left navigation panel. The platform renders a mandatory **For you** item at
   the top of the sidebar. This item navigates to the root route (`/`) of your app and acts as
   the app's home page. Below it, you configure additional menu items using `Sidebar`,
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
| `icon` | `string` | No | The name of an Atlassian Design System (ADS) icon glyph to display alongside the label. For example, `"chart-bar"` or `"settings"`. The platform controls the icon size and color. Always use with a visible `label`. |

#### Using icons

The `icon` prop accepts an ADS icon glyph name as a string. The platform renders the icon at the correct size and color for the sidebar context. Browse all available glyph names in the [ADS icon explorer](https://atlassian.design/components/icon/icon-explorer).

```
```
1
2
```



```
<LinkMenuItem label="Reports" href="/reports" icon="chart-bar" />
```
```

Use icons to help users identify destinations more quickly. Icons work alongside labels — they don't replace them.

##### Icon guidelines

Follow these guidelines when choosing icons for sidebar navigation:

1. **Use icons that represent destinations, not actions.** Choose icons for places your users navigate to, such as a dashboard, a reports area, or a settings section. Avoid icons that suggest transient actions like create, edit, or run — those belong in buttons and menus.
2. **Always pair icons with labels.** The `icon` prop should always appear alongside a `label`. Don't rely on an icon alone to communicate a destination — very few icons are universally understood, especially in a custom app context.
3. **Maintain a one-to-one relationship between icons and destinations.** Each icon should represent exactly one destination, and each destination should use exactly one icon. Duplicating an icon across two items, or swapping icons for the same item in different parts of the navigation, weakens recognition.
4. **Be mindful of Atlassian's existing navigation icons.** Some ADS icons are already associated with specific Atlassian products and navigation areas. Reusing them for unrelated destinations in your app can mislead users into thinking they are navigating to an Atlassian-native area.

##### Recommended icons to avoid in unrelated contexts

The following icons are used in Atlassian's own global navigation for specific primary objects and areas. We recommend avoiding them for destinations that are unrelated to the Atlassian product they represent.

| ADS glyph name | ADS icon | Meaning | Guidance |
| --- | --- | --- | --- |
| `"spaces"` | spaces icon | Spaces directory in Confluence | Avoid if your destination isn't related to Confluence Spaces. |
| `"project"` | project icon | Projects directory in Jira | Avoid if your destination isn't related to Jira Projects. |
| `"goal"` | goal icon | Goal object in the Goals app | Avoid if your destination isn't related to Atlassian Goals. |
| `"dashboard"` | dashboard icon | Dashboard object in the Home app | Avoid if your destination isn't related to Atlassian Dashboards. |
| `"teams"` | teams icon | Teams object in the Teams app | Avoid if your destination isn't related to Atlassian Teams. |
| `"person"` | person icon | "For you" landing page in Atlassian navigation | Avoid reusing this icon to prevent confusion with Atlassian's "For you" navigation item. |
| `"clock"` | clock icon | "Recent" flyout in Atlassian navigation | Avoid to prevent confusion with Atlassian's "Recent" navigation item. |
| `"star-starred"`, `"star-unstarred"` | star-starred icon star-unstarred icon | "Starred" flyout in Atlassian navigation | Avoid unless your destination represents starred or favourited content. |

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
| `items` | `{ id: string; label: string; href: string, icon: string }[]` | Yes | An array of sidebar menu items that the user can reorder. Each item must include a unique `id`, a display `label`, and a navigation `href`. An optional ADS `icon` glyph name from [ADS icon explorer](https://atlassian.design/components/icon/icon-explorer) can also be included to render the corresponding icon. |
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
* Custom UI is not supported for `global:ui`. The platform enforces a UI chrome around the module
  and UI Kit is the public API that lets you control it. To embed custom web content in the main
  content area, use the [`Frame`](/platform/forge/ui-kit/components/frame/) component inside `<Main>`.
* The sidebar always includes a platform-provided **For you** item as its first entry. This item
  navigates to the root route (`/`) of your app and cannot be removed or replaced. Use it as your
  app's home page.

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
    "Select an action from the header or sidebar.",
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
        <LinkMenuItem label="Reports" href="/reports" icon="chart-bar" />
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
  </React.StrictMode>,
);
```
```

## Using dispatch to update state

If using a [Frame](/platform/forge/ui-kit/components/frame/) component in the `Main` content area of your app, there may be scenarios where you want to update the app state from within the `Frame` resource. You can use the [dispatch](/platform/forge/ui-kit/components/frame/#props) prop to define a function that can be called inside the resource to dispatch updates to its parent.

The implementation of the function is up to you, although the most common pattern will be to use a reducer and its associated dispatch function. This is a pattern that will be familiar to developers who have used React’s [useReducer](https://react.dev/reference/react/useReducer) hook or React Redux for complex state management.

### Example

#### Main app

In the main app, the sidebar state is defined as a list of items that can be dynamically updated, with each item mapping to a `LinkMenuItem` component. The `reducer` is a pure function that updates the state based on a provided action, which it receives when `dispatch` is called.

```
```
1
2
```



```
import React, { useReducer } from "react";
import ForgeReconciler, { Frame } from "@forge/react";
import {
  Global,
  Sidebar,
  LinkMenuItem,
  LinkMenuItemProps,
  Main,
} from "@forge/react/global";

interface GlobalState {
  sidebar: LinkMenuItemProps[];
}

type AddSidebarItemAction = { type: 'ADD_SIDEBAR_ITEM', item: LinkMenuItemProps };
const initialState: GlobalState = {
  sidebar: [
    { id: "dashboard", label: "Dashboard", href: "/dashboard" },
    { id: "bugs", label: "Bugs", href: "/bugs" },
    {
      id: "reports",
      label: "Reports",
      type: "expandable",
      children: [
        { id: "weekly", label: "Weekly", href: "/reports/weekly" },
        { id: "monthly", label: "Monthly", href: "/reports/monthly" },
      ],
    },
  ]
};

const reducer = (state: GlobalState, action: Action) => {
  switch (action.type) {
    case "ADD_SIDEBAR_ITEM":
      return {
        ...state,
        sidebar: [...state.sidebar, action.item]
      };
    default:
      return state;
  }
};

const App = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <Global>
      <Sidebar>
        {state.sidebar.map((item) => (
          <LinkMenuItem key={item.id} {...item} />
        ))}
      </Sidebar>
      <Main>
        <Frame resource="my-resource" dispatch={dispatch} />
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

#### my-resource

Inside the resource, the dispatch function can be retrieved by calling [view.getFrameDispatch()](/platform/forge/apis-reference/ui-api-bridge/view/#getframedispatch). It can then be used to dispatch actions to the parent to trigger state updates. In this example, it adds a new `Settings` item to the sidebar menu.

```
```
1
2
```



```
import React, { useEffect, useState } from "react";
import { view } from "@forge/bridge";

const App = () => {
  const [dispatch, setDispatch] = useState(undefined);

  useEffect(() => {
    view
      .getFrameDispatch()
      // If using React to set the dispatch function in state to use, make sure to
      // wrap it in a callback. Otherwise React treats dispatch as a functional updater
      // and tries to execute it.
      .then((dispatch) => setDispatch(() => dispatch));
  }, []);

  if (!dispatch) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <button
        onClick={() =>
          dispatch({
            type: "ADD_SIDEBAR_ITEM",
            item: {
              id: "settings",
              label: "Settings",
              href: "/settings",
            },
          })
        }
      >
        Add Settings menu item
      </button>
    </div>
  );
};

export default App;
```
```

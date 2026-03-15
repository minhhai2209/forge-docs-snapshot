# Jira command palette item (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:command` module allows apps to add items to the [Jira command palette](https://support.atlassian.com/jira-software-cloud/docs/what-is-the-command-palette/). They can be used to navigate to app-defined pages (such as `jira:globalPage` modules) or open custom modals.

Command palette shortcuts are only fetched after the user opens the palette for the first time. This is to reduce the number of unnecessary requests to our internal services.

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
modules {}
└─ jira:command []
   ├─ key (string) [Mandatory]
   ├─ title (string | i18n) [Mandatory]
   ├─ shortcut (string) [Optional]
   ├─ icon (string) [Optional]
   ├─ keywords (string[]) [Optional]
   └─ target {} [Mandatory]
      ├─ page (string) [Optional]
      ├─ resource (string) [Optional]
      └─ render (string) [Optional]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `title` | `string` or `i18n object` | Yes | The title of the command, which is displayed in the command palette.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `shortcut` | `string` |  | A keyboard shortcut sequence that triggers the command without opening the command palette. The shortcut is a space-separated sequence of keys (for example, `e e` or `g t`).  If multiple shortcuts have the same sequence, there is no guarantee on which will be invoked. |
| `icon` | `string` |  | The icon displayed next to the command in the command palette. See [Available icons](#available-icons) for a list of supported values. |
| `keywords` | `string[]` |  | A list of keywords to help users find the command when searching in the command palette. These values are used for search matching only and are never displayed to the user. |
| `target` | `object` | Yes | Defines what happens when the command is invoked. See [Target object](#target-object) for details. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

### Target object

The `target` object defines the action that occurs when a user invokes the command. You can either navigate to a page or open a modal dialog.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `page` | `string` | Either `page` or `resource` | The key of a `jira:globalPage` module defined in the manifest. When the command is invoked, the user is redirected to this page. |
| `resource` | `string` | Either `page` or `resource` | The key of a static [resource](/platform/forge/manifest-reference/resources) entry. When the command is invoked, a modal dialog opens displaying the resource content. |
| `render` | `'native'` | Yes, if using [UI Kit](/platform/forge/ui-kit/components/) | Indicates the resource uses [UI Kit](/platform/forge/ui-kit/components/). Required when using UI Kit with `resource`. |

## Available icons

The following icons are available for use with the `icon` property:

* `add`
* `arrow-right`
* `copy`
* `open`
* `page`
* `edit`
* `user-avatar`
* `activity`
* `settings`
* `undo`
* `document`
* `notification-direct`
* `folder`

You can explore the look and feel of these icons in the [icon explorer](https://atlassian.design/components/icon/icon-explorer).

## Manifest example

```
```
1
2
```



```
modules:
  jira:command:
    - key: command-to-open-global-page
      title: Navigate to My App Global Page
      shortcut: e e
      icon: arrow-right
      target:
        page: global-page
    - key: command-to-open-modal
      title: Open my app's custom modal
      shortcut: e z
      target:
        resource: main-resource
        render: native
      keywords:
        - my search term
        - another search term
  jira:globalPage:
    - key: global-page
      resource: main-resource
      render: native
      title: My App Global Page

resources:
  - key: main-resource
    path: src/frontend/fui.jsx
```
```

In this example:

* The `command-to-open-global-page` command navigates to a global page when invoked via the shortcut `e e` or by selecting it from the command palette.
* The `command-to-open-modal` command opens a modal dialog displaying the content from `main-resource` when invoked via `e z` or selected from the palette. The `keywords` property helps users find this command by searching for "my search term" or "another search term".

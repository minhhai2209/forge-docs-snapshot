# Jira command palette item (Preview)

The `jira:command` module allows apps to add items to the [Jira command palette](https://support.atlassian.com/jira-software-cloud/docs/what-is-the-command-palette/). They can be used to navigate to app-defined pages (such as `jira:globalPage` modules) or open custom modals.

Command palette shortcuts are only fetched after the user opens the palette for the first time. This is to reduce the number of unnecessary requests to our internal services.

## Manifest example

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

#### Notes about the manifest

The file `src/frontend/fui.jsx`, in the Forge app code, implements the custom modal referenced by the `command-to-open-modal` module.

Note also that the `shortcut` property is optional. If present, it provides a quick way to navigate to the wanted destination with key presses. If not, manually opening the command palette and selecting the desired item will be required each time.

In case multiple shortcuts have the same sequence, there is no guarantee on which will be invoked.

Lastly, the `keywords` field is also optional. This field is only used to facilitate searching for items in the command palette; those values are never surfaced to the user.

#### Available icons

The available icons are:

* add
* arrow-right
* copy
* open
* page
* edit
* user-avatar
* activity
* settings
* undo
* document
* notification-direct
* folder

You can explore the look and feel of these icons in the [icon explorer](https://atlassian.design/components/icon/icon-explorer).

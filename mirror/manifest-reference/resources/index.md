# Resources

You can define your own user interface using [UI Kit](/platform/forge/ui-kit/overview/) or [Custom UI](/platform/forge/extend-ui-with-custom-options/).

For UI Kit apps, the Forge platform bundles and hosts your source files, enabling your app to render natively within Atlassian apps using React components from `@forge/react`. See the [UI Kit](/platform/forge/ui-kit/overview/) documentation for more details.

For Custom UI apps, the Forge platform hosts your static resources, enabling your app to display within an iframe. Custom UI apps inherit modern security features to ensure high trust between Atlassian, developers, and users. See the [Custom UI](/platform/forge/custom-ui/iframe/) documentation for more details.

## Properties

The `resources` section of your `manifest.yml` controls the configuration of assets that
you want to display in your app.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the resource, which other modules can refer to. Must be unique within the manifest and have a maximum of 23 characters.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `path` | `string` | Yes | For UI Kit, this is the relative path from your app's root directory to the source file containing your app (for example, `src/frontend/index.jsx`), or to the source directory when using the `entry` property.   For Custom UI, this is the relative path from your app's root directory to the directory containing your static resources, which must include an `index.html` entry point (or named entry files when using the `entry` property). |
| `entry` | `object` | No | An optional map of named entry points within this resource. Each key is an entry identifier and each value is a source filename (not a nested path) directly within the `path` directory — a source file for UI Kit (for example, `global.jsx`), or an `.html` file for Custom UI (for example, `global.html`). Nested paths such as `views/global.jsx` or `views/global.html` are not supported.  A maximum of **50 entries** are allowed per resource.  When `entry` is defined, modules reference a specific entry using the slash syntax: `resource: <resource-key>/<entry-key>`.  When `entry` is omitted, the resource behaves as it does today: a single entry point inferred from `path`. Existing apps require no changes. |

### Examples

#### Single entry point

Use this model when each resource maps to one view. Use the tabs to switch between UI Kit and Custom UI examples.

```
```
1
2
```



```
resources:
  - key: ui-resource
    path: src/frontend/index.jsx
```
```

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: hello-world-panel
      title: UI Kit App
      render: native
      resource: ui-resource
app:
  id: "<your app id>"
resources:
  - key: ui-resource
    path: src/frontend/index.jsx
```
```

To build a UI Kit app in Confluence and Jira, see the [step-by-step tutorial](/platform/forge/build-an-app-compatible-with-confluence-and-jira/).

#### Multiple entry points

Use `entry` to define multiple named entry points inside a single resource. This is useful when multiple modules share dependencies and you want to reduce bundle duplication. Use the tabs to switch between UI Kit and Custom UI examples.

This feature is supported for [Jira](/platform/forge/manifest-reference/modules/index-jira/) and [Confluence](/platform/forge/manifest-reference/modules/index-confluence/) modules. Other Atlassian apps will be supported in the future.

`entry` values are source files (`.jsx`, `.js`, and similar) relative to `path`. The Forge CLI bundles each entry and creates shared chunks for common dependencies.

```
```
1
2
```



```
modules:
  confluence:globalPage:
    - key: my-global-page
      resource: app/global  # <resource-key>/<entry-key>
      render: native
  confluence:globalSettings:
    - key: my-settings-page
      resource: app/settings
      render: native
resources:
  - key: app
    path: src/frontend/
    entry:
      global: global.jsx
      settings: settings.jsx
```
```

See the [UI Kit multi-entry example](https://bitbucket.org/atlassian/uikit-multi-entry-example/src/master/).

## Remote resources

To enable your app to access remote resources, you need to add egress permissions to whitelist those resources. For more information, see [Permissions](/platform/forge/manifest-reference/permissions/).

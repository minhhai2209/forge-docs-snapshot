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
| `path` | `string` | Yes | For UI Kit, this is the relative path from your app's root directory to the source file containing your app (for example, `src/frontend/index.jsx`).   For Custom UI, this is the relative path from your app's root directory to the directory containing your static resources, which must include an `index.html` entry point. |

### Example

```
1
2
3
resources: # list below the static resources entries for your UI Kit app
  - key: my-resource-1
    path: relative/path/to/resource/index.jsx
```

```
```
1
2
```



```
resources: # list below the static resources entries for your Custom UI app
  - key: my-resource-1
    path: relative/path/to/resource/one/directory
  - key: my-resource-2
    path: relative/path/to/resource/two/directory
```
```

A full example of a module using resources would look like:

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
      description: A Forge app with resources
      resource: my-resource-1 # link to the resources listed below
app:
  id: "<your app id>"
resources: # list below the resource entries for your app
  - key: my-resource-1
    path: relative/path/to/resource/index.jsx
```
```

See this [step-by-step tutorial](/platform/forge/build-an-app-compatible-with-confluence-and-jira/) to start building a UI Kit app in Confluence and Jira, or this [tutorial](/platform/forge/build-a-custom-ui-app-in-jira/) to start building a Custom UI app in Jira.

## Remote resources

To enable your app to access remote resources, you need to add egress permissions to whitelist those resources. For more information, see [Permissions](/platform/forge/manifest-reference/permissions/).

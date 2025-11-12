# Resources

You can define your own user interface using static resources, such as HTML, CSS, JavaScript, and images.
The Forge platform hosts your static resources, enabling your app
to display custom UI on Atlassian apps. Custom UI apps inherit modern security features to ensure
high trust between Atlassian, developers, and users.

UI Kit allows only images. However, in the case of Custom UI, there are no restrictions on loading any of the previously mentioned resources.

## Properties

The `resources` section of your `manifest.yml` controls the configuration of the static assets that
you want to display in your app.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the resource, which other modules can refer to. Must be unique within the manifest and have a maximum of 23 characters.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `path` | `string` | Yes | The relative path from the top-level directory of your app to the directory that contains the resources your app is using. |

### Example

```
1
2
3
4
5
resources: # list below the static resources entries for your app
  - key: my-resource-1
    path: relative/path/to/resource/one/directory
  - key: my-resource-2
    path: relative/path/to/resource/two/directory
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
      title: Custom UI App
      description: A Forge app with resources
      resource: my-resource-1 # link to the resources listed below
app:
  id: "<your app id>"
resources: # list below the resource entries for your app
  - key: my-resource-1
    path: relative/path/to/resource/one/directory
```
```

See the following [step-by-step tutorial](/platform/forge/build-a-custom-ui-app-in-jira/) to start building a Custom UI app in Jira.

## Permissions

To enable your app to access remote resources, you need to add egress permissions to whitelist those resources. For more information, see [Permissions](/platform/forge/manifest-reference/permissions/).

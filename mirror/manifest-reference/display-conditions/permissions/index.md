# Permissions

You can control when a module is shown based on its permission state. Use this feature on modules that support `displayConditions.permissions`.

## What it does

Permission-based display conditions let you show a module only when specific permissions are in effect. Each condition maps to a corresponding section in the [Permissions](/platform/forge/manifest-reference/permissions/) manifest reference.

| Type | Description |
| --- | --- |
| `scopes` | Shows the module only when the app has (or the user is in a context that implies) certain OAuth scopes. |
| `external.fetch.backend` | Shows the module only when the specified egress addresses are allowed (e.g. `*.example.com`, or an object with `address`). |
| `external.fetch.client` | Shows the module only when the specified egress addresses are allowed (e.g. `*.example.com`, or an object with `address`). |
| `external.fonts` | Shows the module only when the specified font sources are allowed. |
| `external.images` | Shows the module only when the specified image sources are allowed. |
| `external.scripts` | Shows the module only when the specified script sources are allowed. |
| `external.styles` | Shows the module only when the specified style sources are allowed. |
| `external.frames` | Shows the module only when the specified frame sources are allowed. |
| `external.media` | Shows the module only when the specified media sources are allowed. |

Values can be a string (for a single scope or address) or an array (for multiple values). For `backend` and `client`, you can also use an object with an `address` property, matching the [manifest permissions](/platform/forge/manifest-reference/permissions/#egress-permissions) format.

## Example

In the example below, two Jira issue panel modules use permission-based display conditions: one for a scope, and one for external fetch (backend and client).

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: panel-with-scope
      title: Panel with scope condition
      function: panel-func
      displayConditions:
        permissions:
          scopes: "read:jira-work"
    - key: panel-with-fetch-backend
      title: Panel with fetch backend condition
      function: panel-func
      displayConditions:
        permissions:
          external:
            fetch:
              backend: "*.example.com"
              client: "https://client.example.com"
```
```

## More information

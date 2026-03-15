# API route (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The Forge `apiRoute` module enables Forge apps to expose REST APIs that can be used to allow authorized external systems to securely invoke functions from an installed app.

For a conceptual overview of app REST APIs and a step‑by‑step guide to configuring `apiRoute`, see:

Currently, the `apiRoute` module is only available for Jira and Confluence apps.
This feature is currently not available for apps on Isolated Cloud.

## Manifest structure

```
```
1
2
```



```
modules {}
└─ apiRoute []
   ├─ key (string) [Mandatory]
   ├─ path (string) [Mandatory]
   ├─ operation (string) [Mandatory]
   ├─ function (string)  [Mandatory]
   └─ accept [] [Mandatory]
     └─ application/json (string) [Mandatory]
   └─ scopes [] [Mandatory]
     └─ <scope-1> (string) 
     └─ <scope-2> (string) 
     └─ ...
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | The name of the API route. |
| `path` | `string` | Yes | The developer-defined path that will appear in the final URL. |
| `method` | `string` | Yes | The HTTP method, such as `GET` or `PUT`. |
| `function` | `string` | Yes | A reference to the function key that the route is mapping to. |
| `accept` | `array<string>` | Yes | The payload types that can be accepted. Currently only `application/json` is supported. |
| `scopes` | `array<string>` | Yes | List of developer-defined scopes this API maps to. |

## Example

```
```
1
2
```



```
modules:
  apiRoute:
    - key: employee-api-1
      path: /getEmployeeName
      operation: GET
      function: handler1
      accept:
        - application/json 
      scopes:
        - read:employee:custom
    - key: employee-api-2
      path: /editEmployeeName
      operation: POST
      function: handler2
      accept:
        - application/json 
      scopes:
        - read:employee:custom
        - write:employee:custom
```
```

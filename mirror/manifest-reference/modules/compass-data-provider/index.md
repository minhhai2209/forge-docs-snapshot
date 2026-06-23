# Compass data provider

The `compass:dataProvider` module enables apps to send events and metrics to Compass whenever specific links are added to a component.

For a complete guide to this module, see [Create a data provider app for events and metrics](/cloud/compass/integrations/create-a-data-provider-app/).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `linkTypes` | `Array<enum>` | Yes | A list of Compass link types that your data provider function handles. The possible values are `chat-channel`, `dashboard`, `document`, `on-call`, `project`, `repository`, and `other-link`. |
| `domains` | `Array<string>` | Yes | A list of domains that your data provider function handles. You can specify both full domains (e.g. `'www.example.com'`) and subdomain wildcards (e.g. `'*.example.com'`). |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `callback` | `{ function: string }` |  | Optional reference to the function to be invoked after the above function finishes running. For example: `function: callback-function-key` |

## Required permissions

In order for your app to provide events data, add these [scopes](/platform/forge/manifest-reference/permissions/#compass) to your app manifest:

* `write:component:compass`
* `write:event:compass`

In order for your app to provide metrics data, add this [scope](/platform/forge/manifest-reference/permissions/#compass) to your manifest:

## Example manifest

```
```
1
2
```



```
modules:
  compass:dataProvider:
    key: data-provider
    function: data-provider-fn
    callback:
      function: data-provider-callback-fn
    linkTypes:
      - project
      - repository
    domains:
      - 'www.example.com'
      - '*.example.org'
  function:
    - key: data-provider-fn
      handler: index.dataProvider
    - key: data-provider-callback-fn
      handler: index.dataProviderCallback

permissions:
  scopes:
    - write:component:compass
    - write:event:compass
    - write:metric:compass
```
```

## Function payload

A JSON object is sent to the function that is invoked when a matching component link is added. The object contains one property:

| Property | Type | Description |
| --- | --- | --- |
| `url` | `string` | URL of the component link that was added. |

## Function response format

For details on the expected response format, see [Create a data provider app for events and metrics](/cloud/compass/integrations/create-a-data-provider-app/).

## Callback function payload

A JSON object is sent to the callback function that is invoked (if specified) when the above function finishes running. The object contains these properties:

| Property | Type | Description |
| --- | --- | --- |
| `success` | `boolean` | Whether the request was successful. |
| `url` | `string` | URL the request was performed on. |
| `errorMessage` | `string` | `undefined` | What went wrong, if an error did occur. |

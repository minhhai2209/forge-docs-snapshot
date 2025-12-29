# updateBylineProperties

The `updateBylineProperties` function allows you to programmatically update the `title`, `icon` and `tooltip` values for `confluence:contentBylineItem` Forge apps. This function is available in `@forge/confluence-bridge` version `3.1.0` and above.

This must be used in conjunction with the `contentPropertyKey` manifest parameter in the byline module. See the [contentPropertyKey documentation](content/platform/forge/manifest-reference/modules/confluence-content-byline-item/#content-properties-to-store-byline-properties) for more information.

While this function updates the byline properties, it does not update the values stored in the content key. You will need to make a separate call to the [content property API](/cloud/confluence/rest/v2/api-group-content-properties/#api-pages-page-id-properties-property-id-put) to persist these values.

This function must be called in an app outside of `confluence:contentBylineItem`, but rendered on the same page, like:

* `confluence:backgroundScript`
* `confluence:pageBanner`
* `macro`

## Function Parameter

The `updateBylineProperties` function accepts the following parameters:

| Name | Type | Description |
| --- | --- | --- |
| `propertyKey` | `string` | The key of the [content property](/cloud/confluence/rest/v2/api-group-content-properties/#api-group-content-properties) which stores the `title`, `icon`, and `tooltip` byline properties. This should match the byline module [contentPropertyKey](/platform/forge/manifest-reference/modules/confluence-content-byline-item/#properties) in the manifest. |
| `valueUpdate` | `{ title?: string, icon?: string, tooltip?: string }` | An object containing the updated values of the byline properties. If none is supplied, the app will fallback to using default byline properties. |

### Example

This example shows how to use `updateBylineProperties`:

```
```
1
2
```



```
import { updateBylineProperties } from '@forge/confluence-bridge';
import { requestConfluence } from '@forge/bridge';

// POST request to make contentProperty, e.g.
const bodyData = `{
  "key": "byline-property-unique-key"
}`;

const response = await requestConfluence(`/wiki/api/v2/pages/{page-id}/properties`, {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  body: bodyData
});

// PUT request to update contentProperty with new values
bodyData = `{
  "key": "byline-property-unique-key",
  "value": { "title": "Updated title", "icon": "updated-image.png", "tooltip": "Updated tooltip" },
  "version": {
    "number": 2,
    "message": "updated values"
  }
}`;

const response = await requestConfluence(`/wiki/api/v2/pages/{page-id}/properties/{property-id}`, {
  method: 'PUT',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  body: bodyData
});

// Calling updateBylineProperties to programmatically update the byline properties
const propertyKey = 'byline-property-unique-key'
const valueUpdate = {
    title: 'Updated title',
    icon: 'updated-image.png',
    tooltip: 'Updated tooltip'
};

await updateBylineProperties({ propertyKey, valueUpdate });
```
```

## Response Type

The `updateBylineProperties` function return type is `Promise`.

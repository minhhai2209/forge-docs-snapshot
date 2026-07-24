# Confluence content property

Defining a content property in Forge makes the data inside content properties available to CQL search so that apps can search for content they have set data on via CQL.

Content properties allow you to store key-value pairs against a piece of content, where the value must be well-formed JSON. When defined as part of a contentProperty module, values from these JSON objects can be extracted, indexed, and made available to CQL queries.

Content properties can be set against multiple Confluence content types via the [Content Properties REST APIs](../../../../../cloud/confluence/rest/v2/api-group-content-properties).

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
modules {}
└─ confluence:contentProperty []
   ├─ key (string) [Mandatory]
   ├─ propertyKey (string) [Mandatory]
   ├─ values [] [Mandatory]
     ├─ path (string) [Mandatory]
     ├─ type (string) [Mandatory]
     ├─ searchAlias (string) [Mandatory]
     ├─ uiSupport {} [optional]
       ├─ name (string) [Mandatory]
       ├─ valueType (string) [Mandatory]
       ├─ defaultOperator (string) [Optional]
       ├─ tooltip (string) [Optional]
```

The `propertyKey` and the `searchAlias` must both be globally unique. Prefixing both with a unique representation for your Forge app is the best way to ensure this.

If your app is a [Connect-on-Forge app](/platform/adopting-forge-from-connect/how-to-adopt/), then these properties must be unique in *both surfaces*. The `searchAlias` values here and the `alias` values in any Connect `confluenceContentProperties` module share the same namespace. Reusing the same alias on both (even for different `propertyKey` values) will break CQL search on every tenant that installs the app.

If you are migrating from Connect to Forge, remove the old `confluenceContentProperties` module in the same release that adds this one. For related information, learn more about [Communicating between Connect and Forge](/platform/adopting-forge-from-connect/extending-your-app/#communicating-between-connect-and-forge).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `propertyKey` | `string` | Yes | The key of the property from which the data is indexed. Only alphanumeric and underscore (\_) characters are allowed.  **Important:** Must be globally unique. Prefixing it with a unique representation for your Forge app is the best way to ensure this. |
| `values` | `Values` | Yes | The reference to values of JSON object which will be indexed and the types of referenced values. |
| `values[].path` | `string` |  | The objectName of the JSON data which should be indexed. The objectName is the key of a flattened JSON object with '.' as the path separator.  For instance, for JSON `{"label": {"color": "green", "text":"forge"}}` the valid objectName referencing the color is `label.color`.  Currently, specifying indexes for JSON arrays is not supported. |
| `values[].type` | `string` | Yes | The type of the referenced value:   * `number` - indexes as a number and allows for range ordering and searching on the field. * `text` - tokenizes the value before indexing and allows for searching for words. * `string` - indexed as is and allows searching for the exact phrase only. * `user` - indexes as a user and allows for user-based searching. The expected value is an Atlassian account ID string. * `date` - indexed as a date, optionally also including a time, and allows date or date/time range searching and ordering. The expected date format is `[YYYY]-[MM]-[DD]`. The expected date time format is `[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss][TZ]` where `[TZ]` is an offset from UTC of `+/-[hh]:[mm]` or `Z` for no offset. For example: `2021-05-15`, `2021-05-15T13:44:11+02:00`, `2021-05-15T13:44:11Z` |
| `values[].searchAlias` | `string` | Yes | A CQL field name alias for this content property. Only alphanumeric and underscore (\_) characters are allowed. By defining an alias you are exposing it to CQL and allow other macros and search features to easily use your content property in their search.  **Important:** Must be globally unique. Prefixing it with a unique representation for your Forge app is the best way to ensure this. |
| `values[].uiSupport` | `UI Support` |  | `uiSupport` can be used to define how your aliased field will be displayed in the CQL query builder. By defining `uiSupport`, your content property will appear in the CQL query builder for all macros and search features built on CQL. For example, your property will become usable in the [Page Properties macro](https://confluence.atlassian.com/doc/page-properties-report-macro-186089616.html) |
| `values[].uiSupport.name` | `string` |  | The name of this field as used by the [Page Properties Report macro](https://confluence.atlassian.com/doc/page-properties-report-macro-186089616.html) |
| `values[].uiSupport.valueType` | `string` |  | As well as providing a text field and allowing any entry, the UI support system provides a number of built-in components that can enrich the user experience. These provide extra user interface components to allow setting or picking their value in an intuitive way.  The type can be one of the following values:   * `space` - provides a space picker and stores the result space key as the result. * `label` - provides a label picker and stores the list of labels as the result. * `contentId` - provides a content picker and stores the content id as the result. * `contentType` - provides a content type picker. * `date` - provides a date picker * `string` - provides a free form text field |
| `values[].uiSupport.defaultOperator` | `string` |  | The CQL builder will use this operator when constructing the CQL string. A list of supported CQL operators can be found in the [CQL operators](https://developer.atlassian.com/cloud/confluence/cql-operators/) reference. |
| `values[].uiSupport.tooltip` | `string` |  | The tooltip of this field as used by the [Page Properties Report macro](https://confluence.atlassian.com/doc/page-properties-report-macro-186089616.html) |

## Dynamic module (Preview)

This module can also be declared as a dynamic module. However, this capability is currently
available as a Forge *preview* feature.

For more details, see [Dynamic Modules](/platform/forge/apis-reference/dynamic-modules/).

When you register a dynamic `confluence:contentProperty` module, the `data` object uses the same properties as a static `confluence:contentProperty` module in the manifest.

### Code examples

The following examples show Dynamic Module implementations specific to this module. For more detailed information about the API used in these examples
(including error handling information), see [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/).

#### Create a dynamic content property module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const payload = {
  "type": "confluence:contentProperty",
  "data": {
    "propertyKey": "myapp_metadata",
    "values": [
      {
        "type": "number",
        "path": "wordCount",
        "searchAlias": "myapp_wordcount"
      }
    ]
  }
}
const response = await asApp().requestAtlassian(`/forge/installation/v2/dynamic/module/`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'POST',
  body: JSON.stringify(payload),
});
const body = await response.text();
console.log(`Response: ${response.status} ${body}`);
```
```

#### Update a dynamic content property module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const key = "dynamic-content-property";
const payload = {
  "type": "confluence:contentProperty",
  "data": {
    "propertyKey": "myapp_metadata",
    "values": [
      {
        "type": "number",
        "path": "wordCount",
        "searchAlias": "myapp_wordcount"
      }
    ]
  }
}
const response = await asApp().requestAtlassian(`/forge/installation/v2/dynamic/module/${key}`, {
  headers: {
    'Content-Type': 'application/json'
  },
  method: 'PUT',
  body: JSON.stringify(payload)
});
const body = await response.text();
console.log(`Response: ${response.status} ${body}`);
```
```

## Example

This example uses a content property with the key of `myApp_extraMetaData`, which is defined like this:

```
```
1
2
```



```
{
   "wordCount": 500,
   "status": "pending",
   "reviewer": "<account-id>",
   "relatedContent": "10000"
}
```
```

Using the `confluence:contentProperty` module you request that fields of a content property are indexed.

```
```
1
2
```



```
modules:
  confluence:contentProperty:
    - key: "myApp-extraMetaData"
      propertyKey: myapp_metadata
      values:
        - path: wordCount
          type: number
          searchAlias: myapp_wordcount
        - path: status
          type: string
          searchAlias: myapp_status
          uiSupport:
            valueType: string
            name: Status
            defaultOperator: "="
            tooltip: "Status of the content."
        - path: reviewer
          type: string
          searchAlias: myapp_reviewer
        - path: relatedContent
          type: string
          searchAlias: myapp_relatedContent
          uiSupport:
            valueType: contentId
            name: Related Content
            defaultOperator: "="
            tooltip: "Related content ID."
```
```

Now, indexed data is available to search in CQL, as in this example:

```
```
1
2
```



```
myapp_wordcount=500
content.property[myapp_metadata].status=pending
myapp_reviewer="716720b3c7bea48869bbde5d"
myapp_relatedContent="10000"
```
```

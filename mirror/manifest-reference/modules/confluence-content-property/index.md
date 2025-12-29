# Confluence content property

Defining a content property in Forge makes the data inside content properties available to CQL search so that apps can search for content they have set data on via CQL.

Content properties allow you to store key-value pairs against a piece of content, where the value must be well formed JSON. When defined as part of a contentProperty modules, values from these JSON objects can be extracted, indexed and made available to CQL queries.

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

Both the propertyKey and the searchAlias must be globally unique. Prefixing it with a unique representation for your Forge app is the best way to ensure this.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `propertyKey` | `string` | Yes | The key of the property from which the data is indexed. Only alphanumeric and underscore (\_) characters are allowed.  **Important:** Must be globally unique. Prefixing it with a unique representation for your Forge app is the best way to ensure this. |
| `values` | `Values` | Yes | The reference to values of JSON object which will be indexed and the types of referenced values. |
| `values[].path` | `string` |  | The objectName of the JSON data which should be indexed. The objectName is the key of a flattened JSON object with '.' as the path separator.  For instance, for JSON `{"label": {"color": "green", "text":"forge"}}` the valid objectName referencing the color is `label.color`.  Currently, specifying indexes for JSON arrays is not supported. |
| `values[].type` | `string` | Yes | The type of the referenced value:   * `number` - indexes as a number and allows for range ordering and searching on the field. * `text` - tokenizes the value before indexing and allows for searching for words. * `string` - indexed as is and allows searching for the exact phrase only. * `user` - indexes as a user and allows for user-based searching. The expected value is an Atlassian account ID string. * `date` - indexed as a date, optionally also including a time, and allows date or date/time range searching and ordering. The expected date format is `[YYYY]-[MM]-[DD]`. The expected date time format is `[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss][TZ]` where `[TZ]` is an offset from UTC of `+/-[hh]:[mm] or` |
| `values[].searchAlias` | `string` | Yes | A CQL field name alias for this content property. Only alphanumeric and underscore (\_) characters are allowed. By defining an alias you are exposing it to CQL and allow other macros and search features to easily use your content property in their search.  **Important:** Must be globally unique. Prefixing it with a unique representation for your Forge app is the best way to ensure this. |
| `values[].uiSupport` | `UI Support` |  | uiSupport can be used to define how your aliased field will be displayed in the CQL query builder. By defining uiSupport, your content property will appear in the CQL query builder for all macros and search features built on CQL. For example, your property will become usable in the [Page Properties macro](https://confluence.atlassian.com/doc/page-properties-report-macro-186089616.html) |
| `values[].uiSupport.name` | `string` |  | The name of this field as used by the [Page Properties Report macro](https://confluence.atlassian.com/doc/page-properties-report-macro-186089616.html) |
| `values[].uiSupport.valueType` | `string` |  | As well as providing a text field and allowing any entry, the UI support system provides a number of build in components that can enrich the user experience. These provide extra user interface components to allow setting or picking their value in an intuitive way.  The type can be one of the following values:   * `space` - provides a space picker and stores the result space key as the result. * `label` - provides a label picker and stores the list of labels as the result. * `contentId` - provides a content picker and stores the content id as the result. * `contentType` - provides a content type picker. * `date` - provides a date picker * `string` - provides a free form text field |
| `values[].uiSupport.defaultOperator` | `string` |  | The CQL builder will use this operator when constructing the CQL string. A list of supported CQL operators can be found [here](https://developer.atlassian.com/cloud/confluence/cql-operators/) |
| `values[].uiSupport.tooltip` | `string` |  | The tooltip of this field as used by the [Page Properties Report macro](https://confluence.atlassian.com/doc/page-properties-report-macro-186089616.html) |

## Example

This example uses an content property with the key of `myApp_extraMetaData`, which is defined like this:

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

Using the `confluence:contentProperty` module you request that fields of an content property are indexed.

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

# Jira entity property set

The `jira:entityPropertySet` module lets you bundle multiple entity properties under a single module, with no limit on the number of properties.

See [Entity properties](/cloud/jira/platform/jira-entity-properties/) in the Jira Cloud platform guides for more information about Jira entity properties.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `properties` | [EntityProperty[]](#entity-property) | Yes | A list of entity properties to index. Each entry defines a single entity property with its type, key, and indexed values. |

## Entity property

Each entry in the `properties` array defines a single entity property to index.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `entityType` | `string` |  | The type of the entity. Allowed types are:  The default value is `issue` |
| `propertyKey` | `string` | Yes | The key of the entity property from which the data is indexed. |
| `values` | [PropertyValues[]](#property-values) | Yes | The list of fields in the JSON object to index with the type of each field. |

## Property values

Defines the fields of an entity property to be indexed by Jira. Each value is a reference to a field in the JSON object, along with its type.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | Yes | The path to the JSON data to index. The path is the key of a flattened JSON object with '.' as the delimiter.  For example, for the JSON `{"label": {"color": "red", "text":"connect"}}` the valid path referencing `color` is `label.color`.  The path may refer to an array type. In this case, the 'type' field should be the type of the elements in the array. |
| `type` | `string` | Yes | The type of the referenced value:   * `number`, which indexes as a number and allows for range ordering and searching on the field. * `text`, which tokenizes the value before indexing and allows for searching for words. * `string`, which is indexed as is and allows searching for the exact phrase only. * `user`, which indexes as a user and allows for user-based searching. The expected value is an Atlassian account ID string. * `date`, which is indexed as a date and allows date range searching and ordering.   The expected date format is `[YYYY]-[MM]-[DD]`.   The expected date time format is `[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss][TZ]`   where `[TZ]` is an offset from UTC of `+/-[hh]:[mm]` or `Z` for no offset.   For example: `2021-05-15`, `2021-05-15T13:44:11+02:00`, `2021-05-15T13:44:11Z` |
| `searchAlias` | `string` |  | The name used for this property in JQL. |

## Example

This example bundles multiple entity properties under a single `jira:entityPropertySet` module:

```
```
1
2
```



```
modules:
  jira:entityPropertySet:
    - key: my-properties
      properties:
        - propertyKey: stats
          entityType: issue
          values:
            - path: comments
              type: number
              searchAlias: commentCount
            - path: statusTransitions
              type: number
              searchAlias: transitionCount
            - path: lastCommenter
              type: user
              searchAlias: lastCommenter
        - propertyKey: metadata
          entityType: issue
          values:
            - path: category
              type: string
              searchAlias: metaCategory
            - path: lastUpdated
              type: date
              searchAlias: metaLastUpdated
```
```

### JQL syntax

Once indexed, you can query entity property data using:

* **Search alias** — Use the `searchAlias` value directly as the JQL field name. This is the recommended approach.
* **Full property path** — Use the format `issue.property['<propertyKey>'].<path>`.

```
```
1
2
```



```
commentCount = 5
issue.property['stats'].comments = 5
```
```

Both queries return the same results.

## Limitations

While `jira:entityPropertySet` removes the per-app limit on entity properties, there are platform-wide constraints to be aware of:

There is a platform-wide limit of **1,000 searchable entity properties per entity type** (e.g., `issue`), shared across all apps installed on the tenant. If your app registers a large number of properties, it reduces the available capacity for other apps on the same tenant. Plan your property usage accordingly.

* **Manifest file size**: The manifest YAML file must be under 256 KB. A manifest with ~1,000 entity properties is approximately 165 KB, well within this limit.

## Required permissions

This module requires the `read:jira-work` and `write:jira-work` scopes.

```
```
1
2
```



```
permissions:
  scopes:
    - read:jira-work
    - write:jira-work
```
```

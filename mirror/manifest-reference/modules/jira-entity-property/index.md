# Jira entity property

The `jira:entityProperty` module requests that fields of an entity property are indexed by Jira to make the fields available to query in JQL.

See [Entity properties](/cloud/jira/platform/jira-entity-properties/) in the Jira Cloud platform guides for more information about Jira entity properties.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `entityType` | `string` |  | The type of the entity. Allowed types are:  The default value is `issue` |
| `propertyKey` | `string` | Yes | The key of the entity property from which the data is indexed. |
| `values` | [PropertyValues](#property-values) | Yes | The list of fields in the JSON object to index with the type of each field. **The maximum number of elements to index is 30. This means that all your `jira:entityProperty` modules combined can't declare more than 30 values.** |

## Property values

Defines an entity property to be indexed by Jira. An entity property value is a reference to a JSON object, which also defines its type.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | Yes | The path to the JSON data to index. The path is the key of a flattened JSON object with '.' as the delimiter.  For example, for the JSON `{"label": {"color": "red", "text":"connect"}}` the valid path referencing `color` is `label.color`.  The path may refer to an array type. In this case, the 'type' field should be the type of the elements in the array. See the specification for indexing 'blockedIssues' in the [example](#example). |
| `type` | `string` | Yes | The type of the referenced value:   * `number`, which indexes as a number and allows for range ordering and searching on the field. * `text`, which tokenizes the value before indexing and allows for searching for words. * `string`, which is indexed as is and allows searching for the exact phrase only. * `user`, which indexes as a user and allows for user-based searching. The expected value is an Atlassian account ID string. * `date`, which is indexed as a date and allows date range searching and ordering.   The expected date format is `[YYYY]-[MM]-[DD]`.   The expected date time format is `[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss][TZ]`   where `[TZ]` is an offset from UTC of `+/-[hh]:[mm]` or `Z` for no offset.   For example: `2021-05-15`, `2021-05-15T13:44:11+02:00`, `2021-05-15T13:44:11Z` |
| `searchAlias` | `string` |  | The name used for this property in JQL. |

## Example

This example uses an issue entity property with the key of `stats`, which is defined like this:

```
```
1
2
```



```
{
   "comments": 5,
   "statusTransitions": 6,
   "lastCommenter": "<account-id>",
   "blockedIssues": ["10000", "10001"]
}
```
```

Using the `jira:entityProperty` module you request that fields of an entity property are indexed.

```
```
1
2
```



```
modules:
  jira:entityProperty:
    - key: "stats-property"
      entityType: "issue"
      propertyKey: stats
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
        - path: blockedIssues
          type: string
          searchAlias: blockedIssues
```
```

Now, indexed data is available to search in JQL, as in this example:

```
```
1
2
```



```
commentCount = 5
issue.property['stats'].comments = 5
lastCommenter = currentUser()
blockedIssues[0] = "10000"
```
```

Similarly, you can request indexing for other entity types, such as `user` and `project`.

```
```
1
2
```



```
modules:
  jira:entityProperty:
    - key: "user-property"
      entityType: "user"
      propertyKey: user-stats
      values:
        - path: comments
          type: number
          searchAlias: commentCount
    - key: "project-property"
      entityType: "project"
      propertyKey: project-stats
      values:
        - path: pages
          type: number
          searchAlias: pagesCount
```
```

In a JQL search, you access these properties using a prefix.

```
```
1
2
```



```
project.pagesCount = 5
project.property['project-stats'].pages = 5
assigne.commentCount = 10
reporter.property['user-stats'].comments = 10
```
```

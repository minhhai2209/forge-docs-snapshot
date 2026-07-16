# Jira entity property

The `jira:entityProperty` module requests that fields of an entity property are indexed by Jira to make the fields available to query in JQL.

If your app needs more than 100 indexable entity properties, use the [`jira:entityPropertySet`](/platform/forge/manifest-reference/modules/jira-entity-property-set/) module instead. It bundles multiple entity properties under a single module with no limit on the number of properties.

See [Entity properties](/cloud/jira/platform/jira-entity-properties/) in the Jira Cloud platform guides for more information about Jira entity properties.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `entityType` | `string` |  | The type of the entity. Allowed types are:  The default value is `issue` |
| `propertyKey` | `string` | Yes | The key of the entity property from which the data is indexed. |
| `values` | [PropertyValues](#property-values) | Yes | The list of fields in the JSON object to index with the type of each field. **The maximum number of elements to index is 100. This means that all your `jira:entityProperty` modules combined can't declare more than 100 values.**  If you need more than 100 indexable entity properties, use the [`jira:entityPropertySet`](/platform/forge/manifest-reference/modules/jira-entity-property-set/) module instead, which has no limit. |

## Property values

Defines an entity property to be indexed by Jira. An entity property value is a reference to a JSON object, which also defines its type.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | Yes | The path to the JSON data to index. The path is the key of a flattened JSON object with '.' as the delimiter.  For example, for the JSON `{"label": {"color": "red", "text":"connect"}}` the valid path referencing `color` is `label.color`.  The path may refer to an array type. In this case, the 'type' field should be the type of the elements in the array. See the specification for indexing 'blockedIssues' in the [example](#example). |
| `type` | `string` | Yes | The type of the referenced value:   * `number`, which indexes as a number and allows for range ordering and searching on the field. * `text`, which tokenizes the value before indexing and allows for searching for words. * `string`, which is indexed as is and allows searching for the exact phrase only. * `user`, which indexes as a user and allows for user-based searching. The expected value is an Atlassian account ID string. * `date`, which is indexed as a date and allows date range searching and ordering.   The expected date format is `[YYYY]-[MM]-[DD]`.   The expected date time format is `[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss][TZ]`   where `[TZ]` is an offset from UTC of `+/-[hh]:[mm]` or `Z` for no offset.   For example: `2021-05-15`, `2021-05-15T13:44:11+02:00`, `2021-05-15T13:44:11Z` |
| `searchAlias` | `string` |  | The name used for this property in JQL. |

## Dynamic module (Preview)

This module can also be declared as a dynamic module. However, this capability is currently
available as a Forge *preview* feature.

For more details, see [Dynamic Modules](/platform/forge/apis-reference/dynamic-modules/).

### Code examples

The following examples show Dynamic Module implementations specific to this module. For more detailed information about the API used in these examples
(including error handling information), see [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/).

#### Create a dynamic entity property module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const payload = {
  "type": "jira:entityProperty",
  "data": {
    "entityType": "issue",
    "propertyKey": "dynamic_property",
    "values": [
      {
        "type": "number",
        "path": "comments",
        "searchAlias": "commentCount"
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

#### Update a dynamic entity property module

```
```
1
2
```



```
import { asApp } from "@forge/api";
const key = "dynamic-entity-property";
const payload = {
  "type": "jira:entityProperty",
  "data": {
    "entityType": "issue",
    "propertyKey": "dynamic_property",
    "values": [
      {
        "type": "number",
        "path": "comments",
        "searchAlias": "commentCount"
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
   "blockedIssues": ["10000", "10001"],
   "summary": "Performance improvements for the dashboard",
   "category": "optimization",
   "lastUpdated": "2025-06-15T10:30:00Z"
}
```
```

Using the `jira:entityProperty` module, you request that fields of an entity property are indexed.

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
        - path: summary
          type: text
          searchAlias: statsSummary
        - path: category
          type: string
          searchAlias: statsCategory
        - path: lastUpdated
          type: date
          searchAlias: statsLastUpdated
```
```

### JQL syntax

Once indexed, you can query entity property data in JQL using two syntax forms:

* **Search alias** — Use the `searchAlias` value directly as the JQL field name. This is the recommended approach.
* **Full property path** — Use the format `issue.property['<propertyKey>'].<path>`. This works without a `searchAlias`.

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

Both queries above return the same results. The search alias form is shorter and easier to read.

### JQL examples by type

The JQL operators available for a field depend on the `type` you specified in the module definition.

#### `number` type

The `number` type supports exact match (`=`, `!=`), comparison (`>`, `>=`, `<`, `<=`), and ordering.

```
```
1
2
```



```
commentCount = 5
commentCount > 3
commentCount >= 1 AND commentCount <= 10
transitionCount != 0
ORDER BY commentCount ASC
```
```

#### `text` type

The `text` type tokenizes the value before indexing, which means you can search for individual words
using the `~` (contains) and `!~` (does not contain) operators.

```
```
1
2
```



```
statsSummary ~ "dashboard"
statsSummary ~ "performance improvements"
statsSummary !~ "bug"
```
```

The `text` type does not support exact match (`=`) or ordering. Use the `string` type if you need exact matching.

#### `string` type

The `string` type indexes the value as-is and supports exact match (`=`, `!=`) only.

```
```
1
2
```



```
statsCategory = "optimization"
statsCategory != "bug"
blockedIssues[0] = "10000"
```
```

To search for a value in an indexed array of strings, use the array index syntax (for example, `blockedIssues[0]`).

#### `date` type

The `date` type supports exact match, comparison, and ordering. Use the format `YYYY-MM-DD` or an ISO 8601
date-time with timezone offset.

```
```
1
2
```



```
statsLastUpdated > "2025-01-01"
statsLastUpdated >= "2025-06-01" AND statsLastUpdated < "2025-07-01"
statsLastUpdated > "2025-06-15T00:00:00Z"
ORDER BY statsLastUpdated DESC
```
```

#### `user` type

The `user` type accepts an Atlassian account ID and supports the `currentUser()` function.

```
```
1
2
```



```
lastCommenter = currentUser()
lastCommenter = "<account-id>"
lastCommenter != currentUser()
```
```

### User and project entity types

You can also request indexing for `user` and `project` entity types.

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

In a JQL search, you access `user` and `project` properties using a prefix that corresponds to a JQL user or
project field.

For **project** properties, use the `project` prefix:

```
```
1
2
```



```
project.pagesCount = 5
project.property['project-stats'].pages = 5
```
```

For **user** properties, use a user-based field as the prefix (for example, `assignee`, `reporter`, or `creator`):

```
```
1
2
```



```
assignee.commentCount = 10
reporter.property['user-stats'].comments = 10
```
```

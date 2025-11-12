# Defining Custom Entities

Custom entities are user-defined data structures for storing app data. Forge's storage API lets
you query data stored in these structures using a wide array of query conditions. These query conditions
make it possible to build advanced, complex queries to suit your app's operations.

Custom entities are keys with multiple typed or untyped `attributes`. You can define attributes with the following data types:

* `string`
* `integer`
* `float`
* `boolean`
* `any`

Custom entities are defined in your `manifest.yml` as part of the `storage` property. Each custom entity
also includes an `indexes` section where you define your query's filter patterns (more on this later). The `storage` property is a child of `app`, and uses the following syntax:

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
14
15
16
17
18
19
20
21
22
app:
  id: "ari:cloud:ecosystem::app/406d303d-0393-4ec4-ad7c-1435be94583a"
[...]
  storage:
    entities:
      - name: <custom entity name>
        attributes:
          <attribute1>: 
            type: <type>
          <attribute2>: 
            type: <type>
          <attributeN>: 
            type: <type>
        indexes: 
          - <attributeN>
          - <attributeN>
          - name: <by-any-name>
            partition: 
              - <attribute1>
              - <attribute2>
            range: 
              - <attributeN>
```

After declaring custom entities for your structure data, you can start building complex queries
for them. See [Querying the Custom Entity Store](/platform/forge/runtime-reference/storage-api-query-complex/)
for more details.

For information about storing data in custom entities, see
[Storing data in custom entities](/platform/forge/runtime-reference/storage-api-custom-entities) .

For a detailed tutorial on storing and querying structured data through custom entities,
see [Use custom entities to store structured data](/platform/forge/custom-entities-store-structured-data/).

## Limitations

Custom entities are subject to the following limitations:

| Category | Requirements | Limits |
| --- | --- | --- |
| Entity | Entity names:   * Must only consist of the following characters `a-z0-9:-_.` * Must follow the regex pattern `[_a-z0-9:-.]` * Cannot start with `-` or `_` * Must not begin or end with a `.` * Must not contain the sequence `..`   In addition, an app must not have duplicate entity names. | * An app can have a maximum of 20 entities * Each entity can have a maximum of 7 custom indexes and 50 attributes * Objects that can be stored as custom entities have a maximum depth of 31 and a maximum size of 240KiB (RAW) per object * Entity names cannot be shorter than 3 characters or longer than 60 characters in length |
| Attribute | Attribute names must follow the regex `[_A-Za-z][_0-9A-Za-z]*`. | Attribute names have a maximum length of 64 characters. |
| Index | Index names must contain only the following characters `a-zA-Z0-9:-_.`, and must adhere to the following requirements:   * Must not begin or end with a `.` * Must not contain the sequence `..` * Must not be empty   In addition, each index name within an entity must be unique. | * Each entity can have a maximum of 7 custom indexes * The size of combined values for all   [range](/platform/forge/runtime-reference/custom-entities/#index-types)   attributes on any defined index cannot exceed 900 bytes * The size of combined values for all   [partition](/platform/forge/runtime-reference/custom-entities/#index-types)   attributes on any defined index cannot exceed 1700 bytes * Index names cannot be shorter than 3 characters or longer than 50 characters in length. |
| Keys | A key should:   * Follow the regex pattern `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` * Contain at least 1 character * Not be empty * Not contain only blank space(s) | A key can contain a maximum of 500 characters. |

### Values

Stored entity values must adhere to the following limitations:

| Type | Requirements |
| --- | --- |
| `integer` | Must be a 32-bit signed integer, with the following value limits:  * Minimum value: -2,147,483,648 * Maximum value: 2,147,483,647 (inclusive) |
| `float` | The value must either be 0, or fall within the following range limits (both inclusive):  * Positive range: 1E-130 to 9.9999999999999999999999999999999999999E+125 * Negative range: -9.9999999999999999999999999999999999999E+125 to -1E-130   We provide 38 digits of precision as a base-10 digit. |
| `string` | * Must be a free-form, UTF-8 character sequence * Must contain at least one non-whitespace character * Must not be empty |
| `boolean` | Can only be `true` or `false` |  |
| `any` | The `any` type supports the following values:   * `string` * `integer` * `float` * `boolean` * `object` * `array` |

The [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) strictly enforces attribute types.
Attempting to store a value whose type doesn't
match its field will result in an error (for example, when you try to set a `string` value to an attribute with an `integer` type).

### Entity deletion

Once you've deployed your app, any entities or attributes included in your
manifest can no longer be deleted. If you do, Forge will return an error. We are working
on addressing this in a future update.

You can still add new attributes to an existing entity. Doing so will not
count as an entity deletion.

### Index deletion

You can delete indexes in
[development](/platform/forge/environments-and-versions/#default-environments)
and [custom environments](/platform/forge/environments-and-versions/#custom-environments). Indexes that have already been included in deployments to `staging` and `production` can no longer be
deleted in *any* environment.

## Indexes

While the `entities` property assigns multiple attributes to each key, `indexes` sets which attributes to create indexes for. Attributes with indexes are optimized for your queries; as such, you should create indexes based on the query patterns you intend to use.

### Key index

Forge automatically creates an index based on each entity's key. This will allow your queries to filter by key directly *without* having to declare an index or attribute for it.

The key index's name is `by-key`. This index does not count towards an entity's index limit.

### Custom indexes

You can create custom indexes based on any attributes, or combination of them. A custom index can be either *simple* or *named*.

A *simple* index specifies one attribute (which you can use to reference the index in your queries):

```
```
1
2
```



```
indexes:
  - <attribute>
```
```

A *named* index allows you to optimize for more complex query patterns. Named indexes use the following parameters:

| Parameter | Required? | Description |
| --- | --- | --- |
| ``` name ``` | Yes | Used to reference the index in your queries. |
| ``` range ``` | Yes | Optimizes your index for the use of query [conditions](/platform/forge/runtime-reference/storage-api-query-complex/#basic-methods). This parameter can only have one attribute. |
| ``` partition ``` | No | Optimizes your index for exact matches. This parameter can have multiple attributes. |

The `range` and `partition` parameters can be used together or alone; both accept all data types (except for `any`). If you use either or both, you must set a `name`.

The following snippet shows the basic syntax for a named index:

```
```
1
2
```



```
indexes:
  - name: <value>
    range: 
      - <attribute>
    partition: 
      - <attribute1>
      - <attribute2>
      - <attribute3>
```
```

You can set a maximum of 7 indexes per entity. See [Limitations](#limitations) for more
details.

### Deploying apps with indexes

If your app uses indexes, the `forge deploy` command will send an indexing request to Forge's hosted storage service. This storage service will then create or update indexes as necessary while your app's code is deployed. The indexing process's duration scales with your data set's size, from a minimum of 5 minutes for small data sets.

The indexing process is independent of the rest of the deployment. As such, the `forge deploy` command will normally complete while the indexing process is still ongoing. Until the indexing process completes, you won't be able to install your app on any sites.

To check the status of the indexing process on an environment (namely, `development` or `staging`), run:

```
```
1
2
```



```
forge storage entities indexes list -e <environment>
```
```

The indexing process is complete once all indexes have an `ACTIVE` status.

Indexes that have already been included in deployments to `staging` and `production` can no longer be
deleted in *any* environment.

Before deploying your app to production, make sure that you've removed any references to
deleted indexes. See [Entity and index deletion](#entity-and-index-deletion) for more details.

## Example entity

The following `manifest.yml` excerpt shows a custom entity named `employee` with several attributes and indexes:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/406d303d-0393-4ec4-ad7c-1435be94583a"

  storage:
    entities:
      - name: employee
        attributes:
          surname: 
            type: string
          age: 
            type: integer
          employmentyear: 
            type: integer
          gender: 
            type: string
          nationality: 
            type: string
        indexes:
          - surname
          - employmentyear
          - name: by-age
            range: 
              - age
          - name: by-age-per-gender
            partition: 
              - gender
            range: 
              - age
```
```

This entity also creates four indexes based on the following `employee` attributes:

* `surname`
* `employmentyear`
* `age` (further optimized for filtering according to different age ranges)
* `age` per `gender` (further optimized for filtering according to age ranges for each gender)

For examples of queries you can make against this example entity, see
[Example queries](/platform/forge/runtime-reference/storage-api-query-complex/#example-queries)
in the [Complex query](/platform/forge/runtime-reference/storage-api-query-complex/) page.

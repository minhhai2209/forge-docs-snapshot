# Querying the Custom Entity Store via the legacy package

This page explains how to build Custom Entity queries using the legacy `storage` module from the `@forge/api` package.
While we will continue supporting this module, all future Key-Value Store and Custom Entity Store capabilities will only be built on the new `@forge/kvs` package.

If your app is using the new `@forge/kvs` package, see [Querying the Custom Entity Store](/platform/forge/runtime-reference/storage-api-query-complex/) instead.

You can build complex queries against
data stored in the [Custom Entity Store](/platform/forge/runtime-reference/storage-api-custom-entities/)
using a wide variety of filters and conditions.

To start, import the Forge API package in your app, as follows:

```
1
import { storage } from '@forge/api';
```

Each installation of your app is subject to the API's quotas and limits. See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and [Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

## Scope requirement

Using Forge’s [persistent hosted storage](/platform/forge/runtime-reference/storage-api/#persistent) through `@forge/api` package requires the `storage:app` scope in your manifest file:

```
1
2
3
permissions:
  scopes:
    - storage:app
```

See [Permissions](/platform/forge/manifest-reference/permissions/#scopes) for more information about scopes.

Before you can store data in the Custom Entity Store, you'll need to declare your [custom entities](/platform/forge/runtime-reference/custom-entities/) and indexes first in your app's manifest file.
Custom entities are user-defined data structures for storing app data. Forge's storage API lets
you query data stored in these structures using a wide array of query conditions. These query conditions
make it possible to build advanced, complex queries to suit your app's operations.

For information about storing data to the Custom Entity Store, see [Storing data in custom entities](/platform/forge/runtime-reference/storage-api-custom-entities) .

For a detailed tutorial on storing and querying structured data through custom entities,
see [Use custom entities to store structured data](/platform/forge/custom-entities-store-structured-data/).

## Basic methods

All complex queries operate on a [custom entity's index](/platform/forge/runtime-reference/custom-entities/#indexes). Complex queries follow the same basic signature:

```
```
1
2
```



```
await storage
  .entity("<custom-entity>")
  .query()
  .index()
```
```

This structure contains all the *required* methods for a complex query. The `entity` method sets which custom entity to query, and `index` sets which of those entity's indexes to query. Each query can only target one index from one custom entity.

When using indexes that feature a `partition`, you must specify a value to match the parameter's attribute:

```
```
1
2
```



```
await storage
  .entity("<custom-entity>")
  .query()
  .index("<index-name>", {
    partition: ["<value>"]
  })
```
```

If your index's `partition` has multiple attributes, then you must set a value for each attribute. In addition, you must also set each value in the order they are declared in the index. For example, consider the following index:

```
```
1
2
```



```
indexes:
  - name: by-gender-and-age
    range: 
      - employmentyear
    partition: 
      - gender
      - age
```
```

An appropriate query for this would be:

```
```
1
2
```



```
await storage
  .entity("employee")
  .query()
  .index("by-gender-and-age", {
    partition: ["male", 20]
  })
  .where(WhereConditions.isGreaterThan(2003))
  .getMany()
```
```

This query will fetch employees who are:

* male
* 20 years old
* employed after 2003 (that is, `employmentyear` is higher than `2003`).

Every complex query returns up to 10 values by default. You can increase this to a maximum of 100 using [query.limit](#query-limit).

## where

While `index` lets you filter matches to an index's `partition`, `where` lets you filter against an index's `range`. To use the `where` filter:

```
```
1
2
```



```
import { WhereConditions } from '@forge/api';
```
```

### Method signature

```
```
1
2
```



```
.where(WhereConditions.<condition>("<value>"))
```
```

### Conditions

The `where` filtering method supports the following conditions:

* `beginsWith`
* `between`
* `equalsTo`
* `isGreaterThan`, `isLessThan`
* `isGreaterThanOrEqualTo`, `isLessThanOrEqualTo`

## andFilter / orFilter

You can only use the `index` and `where` methods once per query. The `andFilter` and
`orFilter` allow you add more conditions to a query.

### Method signature

To use either filtering method:

```
```
1
2
```



```
import { FilterConditions } from '@forge/api';
```
```

Each filtering method use the following signatures:

* `andFilter`: *all* conditions must be matched.

  ```
  ```
  1
  2
  ```



  ```
  .andFilter("<attribute>", FilterConditions.<condition>("<value>"))
  ```
  ```
* `orFilter`: only *one* condition must be matched.

  ```
  ```
  1
  2
  ```



  ```
  .orFilter("<attribute>", FilterConditions.<condition>("<value>"))
  ```
  ```

Within the same query, you can use multiple `andFilter` and `orFilter` methods. However, you cannot use *both* methods within the same query.

In addition, the `andFilter` and `orFilter` methods are *in-memory* filters. Using them can sometimes produce pages with no results, with cursor pointing to the next page where actual results exist.

### Conditions

Both filtering methods support the following conditions:

* `beginsWith`
* `between`
* `equalsTo`
* `isGreaterThan`, `isLessThan`
* `isGreaterThanOrEqualTo`, `isLessThanOrEqualTo`
* `exists`, `doesNotExist`
* `contains`, `doesNotContain`
* `notEqualsTo`

## sort

The `sort` method displays your results in either ascending (`ASC`) or descending (`DESC`) order:

```
```
1
2
```



```
.sort(SortOrder.<"ASC|DESC">)
```
```

By default, results are displayed in ascending order.

## query.limit

Returns a new `Query` with a limit on how many matching values get returned. The query
API returns up to 10 values by default, this can be increased to a maximum of 100.

### Method signature

```
```
1
2
```



```
query.limit(limit: number): Query
```
```

## query.cursor

Returns a new `Query` that will start after the provided
[cursor](/platform/forge/runtime-reference/storage-api/#cursors). Cursors enable your
app to fetch subsequent pages of results after completing an initial query.

Cursors are returned from the `getMany` query API.

### Method signature

```
```
1
2
```



```
query.cursor(after: string): Query;
```
```

## query.getMany

Execute the query and return a list of results up to the provided limit in length.
This method returns both the array of results and a cursor that's used to fetch subsequent
pages of results.

### Method signature

```
```
1
2
```



```
query.getMany(): Promise<ListResult>;

interface ListResult {
  results: Result[];
  nextCursor?: string;
}

export interface Result {
  key: string;
  value: object;
}
```
```

## query.getOne

Execute the query and get the first matching result, if any matches exist. If there
is no match, the result resolves to `undefined`.

### Method signature

```
```
1
2
```



```
query.getOne(): Promise<Result | undefined>;

export interface Result {
  key: string;
  value: object;
}
```
```

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

## Example queries

Using the [previous section's](#example-entity) example entity and its indexes, the following queries demonstrate the use of each method:

### Simple index

Targets the `surname` index of the `employee` entity.

```
```
1
2
```



```
await storage
  .entity("employee")
  .query()
  .index("surname")
  .getMany()
```
```

### Simple index with where condition

Targets the `by-age` index, which uses `age` as its `range`. From this, the `where` method will limit matches to employees above the age of 30. Results will be displayed in descending order.

```
```
1
2
```



```
await storage
  .entity("employee")
  .query().index("by-age")
  .where(WhereConditions.isGreaterThan(30))
  .sort(SortOrder.DESC)
  .getMany()
```
```

### Named index with partition

Targets the `by-age-per-gender` index, and will limit matches to female employees.

```
```
1
2
```



```
await storage
  .entity("employee")
  .query()
  .index("by-age-per-gender", {
    partition: ["female"]
  })
  .getMany()
```
```

### Named index with partition and filters

Using the `by-age-per-gender` index, limits matches only to female Australian employees above the age of 30 who were also hired after 2020.

```
```
1
2
```



```
await storage
  .entity("employee")
  .query()
  .index("by-age-per-gender", {
    partition: ["female"]
  })
  .where(WhereConditions.isGreaterThan(30))
  .andFilter("employmentyear", FilterConditions.isGreaterThan(2020))
  .andFilter("nationality", FilterConditions.equalsTo("Australian"))
  .getMany()
```
```

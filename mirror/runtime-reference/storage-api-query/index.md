# Querying key-value pairs

You can use the `kvs.query` method to query data stored through the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/)'s
basic methods:

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
import { kvs, WhereConditions } from '@forge/kvs';

await kvs.query()
  // Filter the response to only keys that start with the string 'value'
  .where('key', WhereConditions.beginsWith('value'))

  // Limit the result size to 10 values, up to a maximum of 20
  .limit(10)

  // Use the cursor provided (returned from a previous invocation)
  // Cursors shouldn't be persisted
  .cursor('...')

  // Get a list of results
  .getMany();
```

The `Query` object is immutable.

Each installation of your app is subject to the Storage API's quotas and limits.
See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and [Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

## Legacy version

Legacy versions of the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) were originally provided through the `storage` module of the `@forge/api` package. For now, we will continue supporting the legacy `storage` module.

However, as of [March 17, 2025](/platform/forge/changelog/#CHANGE-2399), no further feature updates will be provided through this module. Instead, all new KVS and Custom Entity Store feature updates will only be built on modules in the @forge/kvs package. For example,
[KVS transactions](/platform/forge/storage-reference/transactions/) and
[Custom Entity Store transactions](/platform/forge/storage-reference/transactions-entities/) are only available through `@forge/kvs`.

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact

## query.cursor

Returns a new `Query` that will start after the provided
[cursor](/platform/forge/runtime-reference/storage-api-basic/#cursors). Cursors enable your
app to fetch subsequent pages of results after completing an initial query.

Cursors are returned from the `getMany` query API.

When building a query, do not persist cursors, as they may not always be stable. See [Cursors](/platform/forge/runtime-reference/storage-api-basic/#cursors) for related information.

### Method signature

```
```
1
2
```



```
query().cursor(after: string): Query;
```
```

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
query().limit(limit: number): Query
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
query().getMany(): Promise<ListResult<T>>;

interface ListResult<T> {
  results: Result<T>[];
  nextCursor?: string;
}

export interface Result<T> {
  key: string;
  value: T;
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
query().getOne(): Promise<Result<T> | undefined>;

export interface Result<T> {
  key: string;
  value: T;
}
```
```

## query.where

Returns a new query with an additional predicate that returned values must match.
Filters are applied server side and have the following restrictions:

* Queries can only target the `key` field.
* There may only be a single `where` condition for a query.
* The only condition supported by the Key-value store is `beginsWith`.

If no conditions are supplied, the query iterates over all values.

### Method signature

```
```
1
2
```



```
query().where(field: 'key', condition: Predicate): Query
```
```

### beginsWith condition

You can use the condition `beginsWith` to filter results from the Key-value store. To use the condition import `WhereConditions` from the `@forge/kvs` package.

```
```
1
2
```



```
import { WhereConditions } from '@forge/kvs';
```
```

This condition lets you construct a predicate that filters fields starting with the specified string:

```
```
1
2
```



```
beginsWith(value: string): Predicate
```
```

The legacy `storage` module from the `@forge/api` package used the condition `startsWith` instead of `beginsWith`.

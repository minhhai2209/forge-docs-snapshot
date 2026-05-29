# Querying key-value pairs

You can use the `kvs.query` method to query data stored through the [Key-Value Store](/platform/forge/storage-reference/kvs/)'s
basic methods.

To request expiry metadata for results, pass the `EXPIRE_TIME` metadata field using `metadataFields`. When requested, the API returns an `expireTime` attribute in ISO-8601 format.

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
import { kvs, WhereConditions, MetadataField } from '@forge/kvs';

await kvs.query({ metadataFields: [MetadataField.EXPIRE_TIME] })
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

This returns a `ListResult` object containing the matching key-value pairs and the requested metadata:

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
{
  "results": [
    {
      "key": "value-1",
      "value": "stored data",
      "expireTime": "2026-01-15T16:12:19.000Z"
    },
    {
      "key": "value-2",
      "value": { "name": "another entry" },
      "expireTime": "2026-03-20T10:30:00.000Z"
    }
  ],
  "nextCursor": "eyJrZXkiOiJ2YWx1ZS0yIn0="
}
```

The `Query` object is immutable.

Each installation of your app is subject to the Storage API's quotas and limits.
See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and [Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

## Legacy version

Legacy versions of the [Key-Value Store](/platform/forge/storage-reference/kvs/) and [Custom Entity Store](/platform/forge/storage-reference/entities/) were originally provided through the `storage` module of the `@forge/api` package. For now, we will continue supporting the legacy `storage` module.

However, as of [March 17, 2025](/platform/forge/changelog/#CHANGE-2399), no further feature updates will be provided through this module. Instead, all new KVS and Custom Entity Store feature updates will only be built on modules in the @forge/kvs package. For example,
[KVS transactions](/platform/forge/storage-reference/kvs-transactions/) and
[Custom Entity Store transactions](/platform/forge/storage-reference/entities-transactions/) are only available through `@forge/kvs`.

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact.

## query.cursor

Returns a new `Query` that will start after the provided
[cursor](/platform/forge/storage-reference/kvs/#cursors). Cursors enable your
app to fetch subsequent pages of results after completing an initial query.

Cursors are returned from the `getMany` query API.

When building a query, do not persist cursors, as they may not always be stable. See [Cursors](/platform/forge/storage-reference/kvs/#cursors) for related information.

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

### Response

The response is a `ListResult` object containing:

| Property | Type | Description |
| --- | --- | --- |
| `results` | `Result<T>[]` | An array of key-value pairs matching the query. |
| `nextCursor` | `string` (optional) | A cursor for fetching the next page of results. If absent, there are no more results. |

Each `Result` object contains:

| Property | Type | Description |
| --- | --- | --- |
| `key` | `string` | The key of the stored entry. |
| `value` | `T` | The value of the stored entry. |

If `metadataFields` were requested in the query options, each result will also include the requested metadata attributes (such as `createdAt`, `updatedAt`, or `expireTime`).

### Example response

```
```
1
2
```



```
{
  "results": [
    { "key": "item-1", "value": { "name": "First item" } },
    { "key": "item-2", "value": { "name": "Second item" } }
  ],
  "nextCursor": "eyJrZXkiOiJpdGVtLTIifQ=="
}
```
```

When there are no more pages of results, `nextCursor` is omitted:

```
```
1
2
```



```
{
  "results": [
    { "key": "item-3", "value": { "name": "Third item" } }
  ]
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

### Response

The response is a single `Result` object, or `undefined` if no match is found.

| Property | Type | Description |
| --- | --- | --- |
| `key` | `string` | The key of the stored entry. |
| `value` | `T` | The value of the stored entry. |

If `metadataFields` were requested in the query options, the result will also include the requested metadata attributes (such as `createdAt`, `updatedAt`, or `expireTime`).

### Example response

When a match is found:

```
```
1
2
```



```
{ "key": "item-1", "value": { "name": "First item" } }
```
```

When no match is found, the result resolves to `undefined`.

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

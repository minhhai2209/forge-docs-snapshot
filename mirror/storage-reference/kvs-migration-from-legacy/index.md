# Migrating to @forge/kvs from legacy storage module

This page provides guidance on updating any functions that still use the `@forge/api` package's `storage` module to use the new `@forge/kvs` package instead.

Apps that call the KVS or Custom Entity Store from a remote previously did so via GraphQL. We strongly recommend that you migrate those integrations
to the REST API instead. See [Accessing Forge storage from a remote via REST API](/platform/forge/remote/accessing-storage/) for more detailed information.

## Why you should migrate

Legacy versions of the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) (KVS) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) were originally provided through the `storage` module of the `@forge/api` package. As of [March 17, 2025](/platform/forge/changelog/#CHANGE-2399), we stopped applying feature updates to this module.

Instead, all new KVS and Custom Entity Store feature updates are applied to the `@forge/kvs` package. For example, [KVS transactions](/platform/forge/storage-reference/transactions/) and [Custom Entity Store transactions](/platform/forge/storage-reference/transactions-entities/) are only available through `@forge/kvs`.

### Typing improvements

The `@forge/kvs` package provides better support for types through generics. This lets you indicate what data you’re working with for all KVS and Custom Entity Store operations.

## Error handling for keys

You’ll need to update any functions that rely on error handling for non-existent keys.

The legacy `storage` module of `@forge/api` returned an `UNDEFINED` error to any request that specified a key that doesn’t exist. The `@forge/kvs` will now return a `KEY_NOT_FOUND` error instead.

This applies to the following methods:

## Module changes

The `kvs` module of the `@forge/kvs` package provides access to all builders to perform CRUD operations to the KVS and Custom Entity Store.

### Replace startsWith filter with beginsWith

The `query.where` [operation]((/platform/forge/runtime-reference/storage-api-query/#query-where)) now uses the `beginsWith` filter instead of `startsWith`.

**Before**

```
```
1
2
```



```
await storage.query().
  where("key", startsWith("aa")).
  getMany();
```
```

**After**

```
```
1
2
```



```
await kvs.query().
  where("key", WhereConditions.beginsWith("aa")).
  getMany();
```
```

### Replace sortOrder with Sort

The `SortOrder` method is now simply the `sort` [method](/platform/forge/runtime-reference/storage-api-query-complex/#sort); all enum definitions are unchanged.

**Before**

```
```
1
2
```



```
export enum SortOrder { ASC = 'ASC', DESC = 'DESC' }
```
```

**After**

```
```
1
2
```



```
export enum Sort { ASC = 'ASC', DESC = 'DESC'}
```
```

## Filter changes

The `kvs` module introduces several changes to the way filters work in the Custom Entity Store.

### Filter builder

The `kvs` module provides a Custom Entity Store builder for composing `filter` conditions, ensuring better predictability. This builder also helps provide better support for [transactions](/platform/forge/storage-reference/transactions-entities/).

### Replace andFilter/orFilter with filter

The `andFilter` and `orFilter` methods have been replaced by a simpler `filters` [method](/platform/forge/runtime-reference/storage-api-query-complex/#filters):

```
```
1
2
```



```
const andFilterChain = new Filter<Employee>()
  .and('employmentYear', FilterConditions.equalTo(2025))
  .and(...);
const orFilterChain = new Filter<Employee>()
  .or('employmentYear', FilterConditions.equalTo(2025))
  .or(...);
await kvs
  .entity<Employee>('employee')
  .query()
  .index('by-age')
  .filters(filter) // add filterChain here
  .sort(Sort.DESC)
  .getMany();
```
```

### Rename conditional filters

Some [where](/platform/forge/runtime-reference/storage-api-query-complex/#conditions) methods have been renamed to match their corresponding [filters](/platform/forge/runtime-reference/storage-api-query-complex/#filters) conditions:

```
```
1
2
```



```
export const WhereConditions = {
  beginsWith,
  between,
  equalTo,
  greaterThan,
  greaterThanEqualTo,
  lessThan,
  lessThanEqualTo
};

export const FilterConditions = {
  beginsWith,
  between,
  contains,
  notContains,
  equalTo,
  notEqualTo,
  exists,
  notExists,
  greaterThan,
  greaterThanEqualTo,
  lessThan,
  lessThanEqualTo
};
```
```

## References

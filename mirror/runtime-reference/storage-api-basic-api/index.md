# Storing unencrypted key-value pairs

This page lists the Key-Value Store's basic methods for storing unencrypted data. Data stored through these
methods can be queried through the [kvs.query](#kvs.query) tool.

To store sensitive data in a more secure manner, you'll need to [encrypt your stored data](/platform/forge/runtime-reference/storage-api-secret)
instead. This data, however, can't be queried through the [kvs.query](#kvs.query) tool.

To start, import the Forge KVS package in your app, as follows:

```
1
import { kvs } from '@forge/kvs';
```

Each installation of your app is subject to the API's quotas and limits.
See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and
[Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

## Scope requirement

Using the `@forge/kvs` package requires the `storage:app` scope in your manifest file:

```
1
2
3
permissions:
  scopes:
    - storage:app
```

See [Permissions](/platform/forge/manifest-reference/permissions/#scopes) for more information about scopes.

## Legacy version

Legacy versions of the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) were originally provided through the `storage` module of the `@forge/api` package. For now, we will continue supporting the legacy `storage` module.

However, as of [March 17, 2025](/platform/forge/changelog/#CHANGE-2399), no further feature updates will be provided through this module. Instead, all new KVS and Custom Entity Store feature updates will only be built on modules in the @forge/kvs package. For example,
[KVS transactions](/platform/forge/storage-reference/transactions/) and
[Custom Entity Store transactions](/platform/forge/storage-reference/transactions-entities/) are only available through `@forge/kvs`.

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact.

## kvs.set

Stores a JSON value with a specified key.

You can learn more about limits and quotas [here](/platform/forge/platform-quotas-and-limits/#storage-limits).

You don't need to include any identifiers for apps or installations in your key.

Internally, Forge automatically prepends an identifier to every key, mapping it to
the right app and installation. This lets you use the full key length without risking
conflicts across apps or installations.

### kvs.set options

You can use `SetOptions` type to specify the following options to your write requests:

#### Time-to-live (TTL)

You can configure a *relative* time-to-live (TTL) when storing data. TTL applies an *expiry* to a value, starting from the time it
is written.

To set a TTL, provide the following option:

```
```
1
2
```



```
{
  "ttl": {
    "unit": "SECONDS" | "MINUTES" | "HOURS" | "DAYS";
    "value": number;
  }
}
```
```

When specifying a TTL, keep in mind the following:

* **Maximum TTL**: The maximum supported TTL is *1 year* from the time the expiry is set.
* **Expired data deletion is asynchronous**: Expired data is not removed immediately upon expiry. Deletion may take up to 48 hours.

  During this window, read operations may still return expired results. If your app requires strict expiry semantics, request `EXPIRE_TIME` metadata and ignore values where `expireTime` is in the past.
* **Expiry metadata is not returned by default**: Expiry time is returned as metadata *only* when explicitly requested.

  To receive the computed expiry timestamp, request the `EXPIRE_TIME` metadata field. When requested, the API returns an `expireTime` attribute in ISO-8601 format.

#### Change write conflict strategy

When writing data (using either [kvs.set](/platform/forge/runtime-reference/storage-api-basic-api/#kvs-set),
[kvs.setsecret](/platform/forge/runtime-reference/storage-api-secret/#kvs-setsecret), or
[kvs.entity().set](/platform/forge/runtime-reference/storage-api-custom-entities/#entity---set)), Forge resolves write conflicts
using a *last-write-wins* strategy by default.

You can control this behaviour through the `keyPolicy` option, which supports two properties:

* `FAIL_IF_EXISTS`: if the key already exists, don't overwrite it.
* `OVERRIDE`: always write data, regardless of whether it already exists or not. This is identical to the default strategy, which is last-write-wins.

Specify whether a write request should also return metadata. Use the following options for this:

* `returnValue`: when data overwrites are allowed (that is, the `keyPolicy: 'FAIL_IF_EXISTS'` [property](#write-conflict) is *not* set), specify whether the response should also return the value that was written (`LATEST`)
  or overwritten (`PREVIOUS`).
* `returnMetadataFields`: lets you specify what metadata to return. This option supports the following values:
  * `CREATED_AT`
  * `UPDATED_AT`
  * `EXPIRE_TIME`

### Method signature

```
```
1
2
```



```
type SetOptions = {
  ttl?: {
    value: number;
    unit: 'SECONDS' | 'MINUTES' | 'HOURS' | 'DAYS';
  };
  keyPolicy?: 'OVERRIDE' | 'FAIL_IF_EXISTS';
  // If returnValue is provided, keyPolicy must be 'OVERRIDE'
  returnValue?: 'PREVIOUS' | 'LATEST';
  // If returnMetadataFields is provided, keyPolicy must be 'OVERRIDE' and returnValue must be provided
  returnMetadataFields?: MetadataField[];
};

kvs.set(
  key: string,
  value: array | boolean | number | object | string,
  options?: SetOptions
): Promise<void>;
```
```

### Examples

Sets the key `example-key` to one of the supported value types.

```
```
1
2
```



```
// array
kvs.set('example-key', [ 'Hello', 'World' ]);

// boolean
kvs.set('example-key', true);

// number
kvs.set('example-key', 123);

// object
kvs.set('example-key', { hello: 'world' });

// string
kvs.set('example-key', 'Hello world');
```
```

#### Set a TTL

You can set a *relative* [time-to-live (TTL)](#ttl) for the value:

```
```
1
2
```



```
await kvs.set('example-key', { hello: 'world' }, {
  ttl: {
    unit: 'DAYS',
    value: 7,
  },
});
```
```

#### Change write conflict strategy

Use the `keyPolicy` [property](#write-conflict) to specify how to handle write conflicts:

```
```
1
2
```



```
// override the value if key already exists
await kvs.set('example-key', { hello: 'world' }, {
  keyPolicy: 'OVERRIDE',
});

// fail the set request if the key already exists
await kvs.set('example-key', { hello: 'world' }, {
  keyPolicy: 'FAIL_IF_EXISTS',
});
```
```

#### Return value when overwriting

Use `returnValue` to return the written or overwritten value with the `kvs.set()` request response. This only works if
`keyPolicy` is undefined or set to `OVERRIDE`.

```
```
1
2
```



```
// return the written value
await kvs.set('example-key', { hello: 'world' }, {
  returnValue: 'LATEST',
});

// returns the overwritten value
await kvs.set('example-key', { hello: 'world' }, {
  returnValue: 'PREVIOUS',
});
```
```

You can also request the key's relevant metadata by including `metadataFields` in the `options` parameter, similar to [kvs.get](#kvsget):

```
```
1
2
```



```
import { kvs, MetadataField } from '@forge/kvs';

await kvs.set('example-key', {
  returnValue: 'LATEST',
  metadataFields: [MetadataField.CREATED_AT, MetadataField.UPDATED_AT, MetadataField.EXPIRE_TIME]
});
```
```

This will return an object containing the `key`, `value`, and the requested metadata, for example:

```
```
1
2
```



```
{ 
  "key": "example-key", 
  "value": "example-value", 
  "createdAt": 1753750184233, 
  "updatedAt": 1753750200296,
  "expireTime": "2026-01-15T16:12:19.000Z"
}
```
```

## kvs.get

Gets a value by key. If the key doesn't exist, the API returns undefined.

This method also supports an optional `options` parameter that lets you request the following metadata for the key:

* `CREATED_AT`
* `UPDATED_AT`
* `EXPIRE_TIME`

The first two fields will return a Unix timestamp, however, `EXPIRE_TIME` will return a string in ISO-8601 format representing when the node expires.

### Method signature

```
```
1
2
```



```
export enum MetadataField {
  CREATED_AT = 'CREATED_AT',
  UPDATED_AT = 'UPDATED_AT',
  EXPIRE_TIME = 'EXPIRE_TIME'
}

export interface GetOptions {
  metadataFields?: MetadataField[];
}

kvs.get(key: string, options?: GetOptions): Promise<array | boolean | number | object | string>;
```
```

### Example

Gets the value associated with the key `example-key`.

```
```
1
2
```



```
// Read the value for key `example-key`
await kvs.get('example-key'); // returns 'Hello world'
```
```

You can also request the key's relevant metadata by including `metadataFields` in the `options` parameter:

```
```
1
2
```



```
import { kvs, MetadataField } from '@forge/kvs';                                                      

await kvs.get('example-key', {
  metadataFields: [MetadataField.CREATED_AT, MetadataField.UPDATED_AT, MetadataField.EXPIRE_TIME]
});
```
```

This will return an object containing the `key`, `value`, and the requested metadata, for example:

```
```
1
2
```



```
{ 
  "key": "example-key", 
  "value": "example-value", 
  "createdAt": 1753750184233, 
  "updatedAt": 1753750200296,
  "expireTime": "2026-01-15T16:12:19.000Z"
}
```
```

## kvs.delete

Deletes a value by key, this succeeds whether the key exists or not. Write conflicts are resolved
using a last-write-wins strategy.

While you can use the `kvs.delete` method to delete app storage when deleting an app,
we recommend you raise a ticket with the Atlassian Marketplace team to handle this for you. See
[Retiring your app](/platform/marketplace/knowledge-base/retiring-your-app/#paid-via-atlassian-cloud-apps-only)
for more details.

### Method signature

```
```
1
2
```



```
kvs.delete(key: string): Promise<void>;
```
```

### Example

Deletes the value associated with the key `example-key`, if it hasn't already been deleted.

```
```
1
2
```



```
// Delete the value with the key `example-key`
await kvs.delete('example-key');
```
```

## kvs.query

Builds a query which returns a set of entities matching the provided list of criteria.
See [Querying data](/platform/forge/runtime-reference/storage-api-query) for more information
on building and executing queries.

`kvs.query` does not return secret values set by `kvs.setSecret`.

### Method signature

```
```
1
2
```



```
export interface QueryOptions {
  metadataFields?: MetadataField[];
}

kvs.query(options?: QueryOptions): Query
```
```

### Examples

```
```
1
2
```



```
import { kvs, MetadataField, WhereConditions } from '@forge/kvs';

await kvs.query({ metadataFields: [MetadataField.CREATED_AT, MetadataField.UPDATED_AT, MetadataField.EXPIRE_TIME] })
  // Filter the response to only keys that start with the string 'value'
  .where('key', WhereConditions.beginsWith('example'))

  // Limit the result size to 10 values
  .limit(10)

  // Use the cursor provided (returned from a previous invocation)
  .cursor('...')

  // Get a list of results
  .getMany();
```
```

This will return a list of objects containing the `key`, `value`, and the requested metadata, for example:

```
```
1
2
```



```
{
  "nextCursor": "<nextCursor>",
  "results": [{ 
    "key": "example-key", 
    "value": "example-value", 
    "createdAt": 1753750184233, 
    "updatedAt": 1753750200296,
    "expireTime": "2026-01-15T16:12:19.000Z"
  }]
}
```
```

The legacy `storage` module from the `@forge/api` package use the condition `startsWith` instead of `beginsWith`.

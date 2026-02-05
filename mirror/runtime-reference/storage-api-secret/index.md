# Encrypting stored data

The Key-Value Store also lets you store key-value pairs in a secure, encrypted manner. Use the methods listed here to
store sensitive data. Data stored through these methods can't be queried through the [query](/platform/forge/runtime-reference/storage-api-query/)
method.

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

## kvs.setSecret

Similar to `kvs.set`, `kvs.setSecret` provides a way to store sensitive credentials.
Values set with `kvs.setSecret` can only be accessed with `kvs.getSecret`.

The same limitation is applied: persisted JSON values may be up to 128 KiB
in size and have a key of up to 500 bytes.

You do not need to identify your app or the active site/installation in your key,
as Forge will do this automatically.

### kvs.setSecret options

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

kvs.setSecret(
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
kvs.setSecret('example-key', [ 'Hello', 'World' ]);

// boolean
kvs.setSecret('example-key', true);

// number
kvs.setSecret('example-key', 123);

// object
kvs.setSecret('example-key', { hello: 'world' });

// string
kvs.setSecret('example-key', 'Hello world');
```
```

#### Set a TTL

You can also set a *relative* [time-to-live (TTL)](#ttl) for the secret value:

```
```
1
2
```



```
await kvs.setSecret('example-key', { hello: 'world' }, {
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
await kvs.setSecret('example-key', { hello: 'world' }, {
  keyPolicy: 'OVERRIDE',
});

// fail the set request if the key already exists
await kvs.setSecret('example-key', { hello: 'world' }, {
  keyPolicy: 'FAIL_IF_EXISTS',
});
```
```

#### Return value when overwriting

Use `returnValue` to return the written or overwritten value with the `kvs.setSecret()` request response. This only works if
`keyPolicy` is undefined or set to `OVERRIDE`.

```
```
1
2
```



```
// returns the latest value (i.e. the one just set)
await kvs.setSecret('example-key', { hello: 'world' }, {
  returnValue: 'LATEST',
});

// returns the previous value (i.e. the value overriden)
await kvs.setSecret('example-key', { hello: 'world' }, {
  returnValue: 'PREVIOUS',
});
```
```

You can also request the key's relevant metadata by including `metadataFields` in the `options` parameter, similar to [kvs.getSecret](#kvsgetsecret):

```
```
1
2
```



```
import { kvs, MetadataField } from '@forge/kvs';                                                      

await kvs.setSecret('example-key', {
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

## kvs.getSecret

Gets a value by key, which was stored using `kvs.setSecret`. If the key doesn't exist, the API returns undefined.

You can request the expiry time metadata for secret values using the `EXPIRE_TIME` metadata field.

When requested, the API returns an `expireTime` attribute in ISO-8601 format.

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

kvs.getSecret(key: string, options?: GetOptions): Promise<array | boolean | number | object | string>;
```
```

### Example

Gets the secret value associated with the key `example-key`.

```
```
1
2
```



```
// Read the value for key `example-key`
await kvs.getSecret('example-key');

// Request expiry metadata
await kvs.getSecret('example-key', {
  metadataFields: [MetadataField.EXPIRE_TIME]
});
```
```

## kvs.deleteSecret

Deletes a secret value by key, this succeeds whether the key exists or not. Write conflicts are resolved using a last-write-wins strategy.

### Method signature

```
```
1
2
```



```
kvs.deleteSecret(key: string): Promise<void>;
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
await kvs.deleteSecret('example-key');
```
```

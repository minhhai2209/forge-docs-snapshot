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

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact

## kvs.setSecret

Similar to `kvs.set`, `kvs.setSecret` provides a way to store sensitive credentials.
Values set with `kvs.setSecret` can only be accessed with `kvs.getSecret`.

The same limitation is applied: persisted JSON values may be up to 128 KiB
in size and have a key of up to 500 bytes.

You do not need to identify your app or the active site/installation in your key,
as Forge will do this automatically.

Write conflicts are resolved using a last-write-wins strategy.

### Method signature

```
```
1
2
```



```
kvs.setSecret(key: string, value: array | boolean | number | object | string ): Promise<void>;
```
```

### Example

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

## kvs.getSecret

Gets a value by key, which was stored using `kvs.setSecret`. If the key doesn't exist, the API returns undefined.

### Method signature

```
```
1
2
```



```
kvs.getSecret(key: string): Promise<array | boolean | number | object | string>;
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

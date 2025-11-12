# Executing KVS transactions

Transactions allow you to perform multiple operations in a single transaction, ensuring that all operations are either committed or rolled back together. This works with data stored through the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/)'s basic methods:

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
import { kvs } from '@forge/kvs';

await kvs.transact()
    // set first key with value
    .set('key1', 'value1')
    
    // delete second key
    .delete('key2')
    
    //set third key with value
    .set('key3', 'value3')
    
    //commit the transaction
    .execute();
```

Use transactions to execute multiple requests that must either succeed or fail together. If you want to
batch multiple requests where each one can succeed or fail independently, use
[batch operations](/platform/forge/storage-reference/batchops/)
instead.

This page discusses KVS transactions. For Custom Entity Store transactions, see [here](/platform/forge/storage-reference/transactions-entities/).

KVS and Custom Entity Store transactions are not available through the
legacy `storage` module of `@forge/api`.

## Limitations

Data stored through transactions is still subject to the limits defined in [Forge hosted storage key and object size limits](/platform/forge/platform-quotas-and-limits/#forge-hosted-storage-key-and-object-size-limits). Transactions are also subject to additional limits, namely:

| Category | Limit |
| --- | --- |
| Rate limit | Transactions are treated as a single **Write** operation, subject to the rate limits defined in [KVS and Custom Entity Store limits - Future Limits](/platform/forge/platform-quotas-and-limits/#future-limits). The transaction will fail if it exceeds these limits, returning a `TOO_MANY_REQUESTS` error. |
| Quota | The `transaction.set` operation is subject to the quota limits defined in [KVS and Custom Entity Store quotas](/platform/forge/platform-quotas-and-limits/#kvs-and-custom-entity-store-quotas). |
| Transaction operations | Each transaction can contain a maximum of 25 operations. |
| Unique keys | Each key can only be used once in a transaction. |
| Payload | Each transaction is limited to a payload size of 4MB. |

We are currently working on addressing a bug that is incorrectly limiting request payloads for Transactions and Batch operations
to 1MB instead of 4MB. See [FRGE-1916](https://ecosystem.atlassian.net/browse/FRGE-1916) for additional details.

## transact.set

Adds an operation to the transaction to set a JSON value with a specified key.

### Method signature

```
```
1
2
```



```
  transact.set(key: string, value: array | boolean | number | object | string): TransactionBuilder;
```
```

### Example

```
```
1
2
```



```
// array
kvs.transact().set('example-key', [ 'Hello', 'World' ])

// boolean
kvs.transact().set('example-key', true);

// number
kvs.transact().set('example-key', 123);

// object
kvs.transact().set('example-key', { hello: 'world' });

// string
kvs.transact().set('example-key', 'Hello world');
```
```

## transact.delete

Deletes a value by key, this succeeds whether the key exists or not.

### Method signature

```
```
1
2
```



```
  transact.delete(key: string): TransactionBuilder;
```
```

### Example

```
```
1
2
```



```
kvs.transact().delete('example-key');
```
```

# Executing Custom Entity Store transactions

Transactions allow you to perform multiple conditional operations in a single transaction, ensuring that all operations are either committed if all conditions are met or rolled back together. This works with data stored through the [Custom Entity Store](/platform/forge/runtime-reference/storage-api-custom-entities/).

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
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
import { kvs, Filter, Conditions } from '@forge/kvs';

// Pre define conditions for performing a transaction operation 
const conditions = new Filter().and('surname', FilterConditions.beginsWith('S'))

await kvs
   .transact()
   
   // set key with a value for employee entity
   .set('employee1', {
    surname:"Davis",
    age: 30,
    employmentyear: 2022,
    gender: "male",
    nationality: "Australian"
    }, { entityName: 'employee' })
   
   // conditionally set key with value with inline conditions
   .set('employee2', {
    surname:"Scott",
    age: 30,
    employmentyear: 2022,
    gender: "male",
    nationality: "Australian"
    }, {
     entityName: 'employee',
     conditions: new Filter().and('surname', FilterConditions.beginsWith('S'))
       .and('nationality', FilterConditions.beginsWith('A'))
   })
   
   // delete value for key
   .delete('employee3', { entityName: 'employee' })
   
    // delete value with premade conditions
   .delete('employee4', { entityName: 'employee', conditions }) 
   
   // check if key exists and meets conditions
   .check('employee5', filter, { entityName: 'author', conditions })
   
   // Commit the transaction
   .execute();
```

Use transactions to execute multiple requests that must either succeed or fail together. If you want to
batch multiple requests where each one can succeed or fail independently, use
[batch operations](/platform/forge/storage-reference/batchops-entities/)
instead.

This page discusses Custom Entity Store transactions. For Key-Value Store transactions, see [here](/platform/forge/storage-reference/transactions/).

KVS and Custom Entity Store transactions are not available through the
legacy `storage` module of `@forge/api`.

## Limitations

Data stored through transactions is still subject to [Custom entities limits](/platform/forge/platform-quotas-and-limits/#custom-entities-limits). Transactions are also subject to additional limits, namely:

| Category | Limit |
| --- | --- |
| Rate limit | Transactions are treated as a single **Write** operation, subject to the rate limits defined in [KVS and Custom Entity Store limits - Future Limits](/platform/forge/platform-quotas-and-limits/#future-limits). The transaction will fail if it exceeds these limits, returning a `TOO_MANY_REQUESTS` error. |
| Quota | The `transaction.set` operation is subject to the quota limits defined in [KVS and Custom Entity Store quotas](/platform/forge/platform-quotas-and-limits/#kvs-and-custom-entity-store-quotas). |
| Transaction operations | Each transaction can contain a maximum of 25 operations. |
| Unique keys | Each key can only be used once in a transaction. |
| Payload | Each transaction is limited to a payload size of 4MB. |

We are currently working on addressing a bug that is incorrectly limiting request payloads for Transactions and Batch operations
to 1MB instead of 4MB. See [FRGE-1916](https://ecosystem.atlassian.net/browse/FRGE-1916) for additional details.

## Conditions

You can specify conditions for each operation of a transaction. Each condition is checked and must be true; if any condition is not met, the entire transaction will fail.

You can specify conditions using the `Filter` class. This class provides an `and()` or `or()` method for adding conditions to the transaction. The conditions that are supported are the same as filters for [custom entity querying](/platform/forge/runtime-reference/storage-api-query-complex/#conditions-1).

### Method signature

To use either method:

```
```
1
2
```



```
import { Filter, FilterConditions } from '@forge/kvs';
```
```

Each filtering method use the following signatures:

* `and`: *all* conditions must be matched.

```
```
1
2
```



```
.and("<attribute>", FilterConditions.<condition>("<value>"))
```
```

* `or`: *any* condition must be matched.

```
```
1
2
```



```
.or("<attribute>", FilterConditions.<condition>("<value>"))
```
```

## transact.set

Adds an operation to the transaction to set a JSON value with a specified key for a custom entity. Conditions are optional.

### Method signature

```
```
1
2
```



```
  transact().set(key: string, value: object, options: { entityName: string, conditions?: Filter }): TransactionBuilder;
```
```

### Example

```
```
1
2
```



```
await kvs
   .transact()
   
   // set key with a value for employee entity
   .set('employee1', {
    surname:"Davis",
    age: 30,
    employmentyear: 2022,
    gender: "male",
    nationality: "Australian"
    }, { entityName: 'employee' })
   
   // conditionally update key with value for employee entity
   .set('employee2', {
    surname:"Scott",
    age: 30,
    employmentyear: 2022,
    gender: "male",
    nationality: "Australian"
    }, {
     entityName: 'employee',
     conditions: new Filter().and('lastName', FilterConditions.beginsWith('S'))
       .and('nationality', FilterConditions.beginsWith('A'))
   })
```
```

## transact.delete

Deletes a value by key for a custom entity, this succeeds whether the key exists or not. Conditions are optional.

### Method signature

```
```
1
2
```



```
  transact().delete(key: string, options: { entityName: string, conditions?: Filter }): TransactionBuilder;
```
```

### Example

```
```
1
2
```



```
await kvs.transact()
   // delete value for key in employee entity
   .delete('employee1', { entityName: 'employee' })
   
    // delete value for key in employee entity with condition
   .delete('employee2', { entityName: 'employee', conditions: new Filter().or('lastName', FilterConditions.beginsWith('S'))
       .or('lastName', FilterConditions.beginsWith('A')) })
```
```

## transact.check

Checks a key meets the specified conditions for a custom entity. Conditions are **mandatory**.

### Method signature

```
```
1
2
```



```
  transact().check(key: string, options: { entityName: string, conditions: Filter }): TransactionBuilder;
```
```

### Example

```
```
1
2
```



```
await kvs.transact()
    // Check value in key for employee entitiy meets conditions
    .check('employee1', { entityName: 'employee', conditions: new Filter().and('lastName', FilterConditions.beginsWith('S'))
```
```

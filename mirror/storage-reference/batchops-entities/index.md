# Executing batch operations

You can *batch* multiple `set` requests and execute them simultaneously using `kvs.batchSet`. This method will execute all batched requests
*in parallel*, and will successfully complete as many as possible.

There is no guaranteed order of completion. Batch operations will report which operations succeeded or failed.

By contrast,
[KVS transactions](/platform/forge/storage-reference/transactions/) and
[Custom Entity Store transactions](/platform/forge/storage-reference/transactions-entities/) will succeed or fail *all* operations
included in the transaction. That is, if any operation in the transaction cannot be completed, then all other operations will also fail.

Batch operations are not available through the legacy `storage` module of `@forge/api`.

## Limitations

Data stored through batch operations is still subject to the defined
[Forge hosted storage key and object size limits](/platform/forge/platform-quotas-and-limits/#key-and-object-size-limits).

In addition:

* You can send a maximum of 45 batch operations per minute.
* A single `kvs.batchSet` operation can be a payload of 4MB, similar to transactions.

We are currently working on addressing a bug that is incorrectly limiting request payloads for Transactions and Batch operations
to 1MB instead of 4MB. See [FRGE-1916](https://ecosystem.atlassian.net/browse/FRGE-1916) for additional details.

## Error handling

A batch operation will return an error and fail entirely if:

* It doesn't contain any `set` requests.
* There are multiple requests to set the same key or entity.

## kvs.batchSet

Execute multiple [kvs.set](/platform/forge/runtime-reference/storage-api-basic-api/#kvs-set) or
[kvs.entity().set](/platform/forge/runtime-reference/storage-api-custom-entities/#entity---set) requests
in one operation. You can execute a mix of both types of request in the same batch operation.

This method will return a `BatchResponse` that contain an array of
operatioons succeeded (`successfulKeys`) and failed (`failedKeys`).

### Method signature

```
```
1
2
```



```
kvs.batchSet(items: BatchSetItem[]): Promise<BatchResponse>;

// Definition of what needs to be stored
interface BatchSetItem {
  entityName?: string; // If not provided it becomes a KVS request
  key: string;
  value: string | number | boolean | Record<string, any> | any[];
}

interface BatchResponse {
  successfulKeys: BatchItemSuccess[];
  failedKeys: BatchItemError[];
}

interface BatchItemSuccess {
  key: string;
  entityName?: string;
}

interface BatchItemError {
  key: string;
  entityName?: string;
  error: {
    code: string;
    message: string;
  }
}
```
```

### Example

The following batch operation sets multiple entities across different data structures:

```
```
1
2
```



```
await kvs.batchSet([
  {
    key: 'employee1',
    value: {
      surname:"Davis",
      age: -1,
      employmentyear: 2022,
      gender: "male",
      nationality: "Australian"
     },
     entityName: "employee"
   }, 
   { 
    key: "untypedobject",
    value: {
      foo: "bar"
     },
   }
]);

/*
{
  "successfulKeys": [
    {"key": "untypedobject"},
    {"entityName": "employee", "key": "employee1"}
  ],
  "failedKeys": []
}

If some keys fail
{
  successfulKeys: [{"key": "untypedobject"}]
  failedKeys: [{
      "key": "employee1",
      "entityName": "employee",
      "error": {
        "code": "PROPERTY_VALUE_OUT_OF_BOUNDS",
        "message": "Property age value must be between: 1 and 100"}
    }]
}
*/
```
```

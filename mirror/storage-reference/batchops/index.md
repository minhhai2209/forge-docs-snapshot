# Executing batch operations

You can *batch* multiple `get`, `set` and `delete` requests and execute them simultaneously using `kvs.batchSet`, `kvs.batchGet` and `kvs.batchDelete` respectively. These methods execute all batched requests
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

* A single `kvs.batchSet` operation can be a payload of 4MB, similar to transactions.
* Each batch operation can contain a maximum of 25 keys.

## Error handling

A batch operation will return an error and fail entirely if:

* It doesn't contain any keys.
* There are multiple requests to set, delete, or get the same key or key plus entity.

## kvs.batchSet

Execute multiple [kvs.set](/platform/forge/runtime-reference/storage-api-basic-api/#kvs-set) or
[kvs.entity().set](/platform/forge/runtime-reference/storage-api-custom-entities/#entity---set) requests
in one operation. You can execute a mix of both types of request in the same batch operation.

This method will return a `BatchResult` that contains an array of
operations succeeded (`successfulKeys`) and failed (`failedKeys`).

You can also set a *relative* time-to-live (TTL) for all keys in your batched operation. See [Time-to-live](/platform/forge/runtime-reference/storage-api-basic-api/#ttl) for related details.

### Method signature

```
```
1
2
```



```
kvs.batchSet(items: BatchSetItem[]): Promise<BatchResult>;
```
```

### Type definitions

```
```
1
2
```



```
// Definition of what needs to be stored
interface BatchSetItem {
  entityName?: string; // If not provided it becomes a KVS request
  key: string;
  value: string | number | boolean | Record<string, any> | any[];
  options?: SetOptions;
}

type SetOptions = {
  ttl?: {
    unit: 'SECONDS' | 'MINUTES' | 'HOURS' | 'DAYS';
    value: number;
  };
};

interface BatchResult {
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
     entityName: "employee",
     options: {
       ttl: {
         unit: 'DAYS',
         value: 7,
       },
     },
   }, 
   { 
    key: "untypedobject",
    value: {
      foo: "bar"
     },
   }
]);
```
```

## kvs.batchGet

Execute multiple [kvs.get](/platform/forge/runtime-reference/storage-api-basic-api/#kvs-get) or
[kvs.entity().get](/platform/forge/runtime-reference/storage-api-custom-entities/#entity---get) requests
in one operation. You can execute a mix of both types of request in the same batch operation.

This method will return a `BatchGetResult` that contains an array of
operations succeeded (`successfulKeys`) and failed (`failedKeys`). Successful operations include the retrieved value and metadata.

### Method signature

```
```
1
2
```



```
kvs.batchGet(items: BatchGetItem[]): Promise<BatchGetResult<T>>;
```
```

### Type definitions

```
```
1
2
```



```
// Definition of what needs to be retrieved
export type BatchGetItem = {
  entityName?: string;
  key: string;
  options?: GetOptions;
};

export interface GetOptions {
  metadataFields?: MetadataField[];
}

export interface BatchGetResult<T> {
  successfulKeys: Array<BatchGetItemResult<T>>;
  failedKeys: BatchItemError[];
}

export interface BatchGetItemResult<T> {
  key: string;
  entityName?: string;
  value: T;
  createdAt?: number;
  updatedAt?: number;
  expireTime?: string;
}

export interface BatchItemError {
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

The following batch operation gets multiple entities across different data structures:

```
```
1
2
```



```
await kvs.batchGet([
  {
    key: 'employee1',
    entityName: "employee",
    options: {
      metadataFields: [MetadataField.CREATED_AT]
    }
  }, 
  { 
    key: "untypedobject",
  }
]);
```
```

## kvs.batchDelete

Execute multiple [kvs.delete](/platform/forge/runtime-reference/storage-api-basic-api/#kvs-delete) or
[kvs.entity().delete](/platform/forge/runtime-reference/storage-api-custom-entities/#entity---delete) requests
in one operation. You can execute a mix of both types of request in the same batch operation.

This method will return a `BatchResult` that contains an array of
operations succeeded (`successfulKeys`) and failed (`failedKeys`).

### Method signature

```
```
1
2
```



```
kvs.batchDelete(items: BatchDeleteItem[]): Promise<BatchResult>;
```
```

### Type definitions

```
```
1
2
```



```
// Definition of what needs to be deleted
interface BatchDeleteItem {
  entityName?: string; // If not provided it becomes a KVS request
  key: string;
}

interface BatchResult {
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

The following batch operation deletes multiple entities across different data structures:

```
```
1
2
```



```
await kvs.batchDelete([
  {
    key: 'employee1',
    entityName: "employee",
  }, 
  { 
    key: "untypedobject",
  }
]);
```
```

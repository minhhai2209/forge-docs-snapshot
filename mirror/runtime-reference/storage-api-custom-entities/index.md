# Storing data in custom entities

This page lists the basic methods you can use to store data in the [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/)
using your defined [custom entities](/platform/forge/runtime-reference/custom-entities/).

To start, import the Forge KVS package in your app, as follows:

```
1
import { kvs } from '@forge/kvs';
```

Each installation of your app is subject to the API's quotas and limits.
See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and
[Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

For a detailed tutorial on storing and querying structured data through custom entities,
see [Use custom entities to store structured data](/platform/forge/custom-entities-store-structured-data/).

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

This page lists different methods for managing data stored in custom entities. For related information:

For a detailed tutorial on storing and querying structured data through custom entities,
see [Use custom entities to store structured data](/platform/forge/custom-entities-store-structured-data/).

### Legacy version

Legacy versions of the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) were originally provided through the `storage` module of the `@forge/api` package. For now, we will continue supporting the legacy `storage` module.

However, as of [March 17, 2025](/platform/forge/changelog/#CHANGE-2399), no further feature updates will be provided through this module. Instead, all new KVS and Custom Entity Store feature updates will only be built on modules in the @forge/kvs package. For example,
[KVS transactions](/platform/forge/storage-reference/transactions/) and
[Custom Entity Store transactions](/platform/forge/storage-reference/transactions-entities/) are only available through `@forge/kvs`.

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact.

## Limitations

Stored entity values must adhere to the following type requirements:

| Type | Requirements |
| --- | --- |
| `integer` | Must be a 32-bit signed integer, with the following value limits:  * Minimum value: -2,147,483,648 * Maximum value: 2,147,483,647 (inclusive) |
| `float` | The value must either be 0, or fall within the following range limits (both inclusive):  * Positive range: 1E-130 to 9.9999999999999999999999999999999999999E+125 * Negative range: -9.9999999999999999999999999999999999999E+125 to -1E-130   We provide 38 digits of precision as a base-10 digit. |
| `string` | * Must be a free-form, UTF-8 character sequence * Must contain at least one non-whitespace character * Must not be empty |
| `boolean` | Can only be `true` or `false` |  |
| `any` | The `any` type supports the following values:   * `string` * `integer` * `float` * `boolean` * `object` * `array` |

The [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) strictly enforces attribute types.
Attempting to store a value whose type doesn't
match its field will result in an error (for example, when you try to set a `string` value to an attribute with an `integer` type).

## entity().set

Stores a JSON value with a specified key, for the selected entity. You can customise the key conflict and response behaviour using the Set Options available.

### entity().set options

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
    unit: 'SECONDS' | 'MINUTES' | 'HOURS' | 'DAYS';
    value: number;
  };
  keyPolicy?: 'OVERRIDE' | 'FAIL_IF_EXISTS';
  // If returnValue is provided, keyPolicy must be 'OVERRIDE'
  returnValue?: 'PREVIOUS' | 'LATEST';
  // If returnMetadataFields is provided, keyPolicy must be 'OVERRIDE' and returnValue must be provided
  returnMetadataFields?: MetadataField[];
};

kvs.entity(entityName: string).set(
  key: string,
  value: object,
  options?: SetOptions
): Promise<void>;
```
```

### Limitations

A key should:

* match the regex `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/`
* contain at least 1 character
* contain a maximum of 500 characters
* not be empty
* not contain only blank space(s)

### Examples

Sets the key `example-key` for an entity named `employee`.

```
```
1
2
```



```
kvs.entity('employee').set('example-key', {
    surname: "Davis",
    age: 30,
    employmentyear: 2022,
    gender: "male",
    nationality: "Australian"
});
```
```

#### Set a TTL

You can also set a *relative* [time-to-live (TTL)](#ttl) for the entity value:

```
```
1
2
```



```
await kvs.entity('employee').set('example-key', {
  surname: 'Davis',
  age: 30,
  employmentyear: 2022,
  gender: 'male',
  nationality: 'Australian'
}, {
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
await kvs.entity('employee').set('example-key', {
  surname: 'Davis',
  age: 30,
  employmentyear: 2022,
  gender: 'male',
  nationality: 'Australian'
}, {
  // override the value if key already exists
  keyPolicy: 'OVERRIDE',
});

await kvs.entity('employee').set('example-key', {
  surname: 'Davis',
  age: 30,
  employmentyear: 2022,
  gender: 'male',
  nationality: 'Australian'
}, {
  // fail the set request if key already exists
  keyPolicy: 'FAIL_IF_EXISTS',
});
```
```

#### Return value when overwriting

Use `returnValue` to return the written or overwritten value with the `entity().set` request response. This only works if
`keyPolicy` is undefined or set to `OVERRIDE`.

```
```
1
2
```



```
await kvs.entity('employee').set('example-key', {
  surname: 'Davis',
  age: 30,
  employmentyear: 2022,
  gender: 'male',
  nationality: 'Australian'
}, {
  // returns the latest value (i.e. the one just set)
  returnValue: 'LATEST',
});

await kvs.entity('employee').set('example-key', {
  surname: 'Davis',
  age: 30,
  employmentyear: 2022,
  gender: 'male',
  nationality: 'Australian'
}, {
  // returns the previous value (i.e. the value overriden)
  returnValue: 'PREVIOUS',
});
```
```

You can also request the key's relevant metadata by including `metadataFields` in the `options` parameter, similar to [entity().get](#entityget):

```
```
1
2
```



```
await kvs.entity('employee').set('example-key', {
  surname: 'Davis',
  age: 30,
  employmentyear: 2022,
  gender: 'male',
  nationality: 'Australian'
}, {
  returnValue: 'LATEST',
  metadataFields: [MetadataField.CREATED_AT, MetadataField.UPDATED_AT, MetadataField.EXPIRE_TIME]
});
```
```

## entity().get

Gets a custom entity value by key. If the key doesn't exist, the API returns `undefined`.

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

kvs.entity(entityName: string).get(key: string, options?: GetOptions): Promise<object>;
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
await kvs.entity('employee').get('example-key');
```
```

This will return all attributes related to the key:

```
```
1
2
```



```
{
  "surname": "Davis",
  "age": 30,
  "employmentyear": 2022,
  "gender": "male",
  "nationality": "Australian"
}
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

// Read the value for key `example-key`
await kvs.entity('employee').get('example-key', {
  metadataFields: [MetadataField.CREATED_AT, MetadataField.UPDATED_AT, MetadataField.EXPIRE_TIME]
});
```
```

This will return the key's attributes with the requested metadata:

```
```
1
2
```



```
{
  "key": "example-key",
  "value": {
    "surname": "Davis",
    "age": 30,
    "employmentyear": 2022,
    "gender": "male",
    "nationality": "Australian"
  },
  "createdAt": 1753750184233,
  "updatedAt": 1753750200296,
  "expireTime": "2026-01-15T16:12:19.000Z"
}
```
```

## entity().delete

Deletes a value by key, for the selected entity. This succeeds whether the key exists or not.

While you can use the `kvs.entity.delete` method to delete app data when deleting an app,
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
kvs.entity(entityName: string).delete(key: string): Promise<void>;
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
await kvs.entity('employee').delete('example-key');
```
```

## entity().query

Allows you to build complex queries against data in the Custom Entity Store. See
[Querying the Custom Entity Store](/platform/forge/runtime-reference/storage-api-query-complex/) for detailed information.

To return expiry metadata for results, pass the `EXPIRE_TIME` metadata field.

When requested, the API returns an `expireTime` attribute in ISO-8601 format.

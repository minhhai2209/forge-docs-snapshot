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

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact

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

Stores a JSON value with a specified key, for the selected entity.

### Method signature

```
```
1
2
```



```
kvs.entity(entityName: string).set(key: string, value: object): Promise<void>;
```
```

### Limitations

A key should:

* match the regex `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/`
* contain at least 1 character
* contain a maximum of 500 characters
* not be empty
* not contain only blank space(s)

### Example

Sets the key `example-key` for an entity named `employee`.

```
```
1
2
```



```
kvs.entity("employee").set('example-key', {
    surname:"Davis",
    age: 30,
    employmentyear: 2022,
    gender: "male",
    nationality: "Australian"
});
```
```

## entity().get

Gets a custom entity value by key. If the key doesn't exist, the API returns `undefined`.

### Method signature

```
```
1
2
```



```
kvs.entity(entityName: string).get(key: string): Promise<object>;
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
await kvs.entity("employee").get('example-key');
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

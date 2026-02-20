# Key-Value Store

The [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic-api/) provides simple storage for key/value pairs. Use this to persistently store data that you'd like to retrieve through the
[Query](/platform/forge/runtime-reference/storage-api-query/) tool.

For example:

```
1
2
3
4
5
6
7
import { kvs, WhereConditions } from '@forge/kvs';

await kvs.set('foo', 'bar');
await kvs.get('foo');
await kvs.query()
  .where('key', WhereConditions.beginsWith('fo'))
  .getMany();
```

To safeguard sensitive data in a more secure manner, the Key-Value Store allows for storing encrypted data via the [Secret store](/platform/forge/runtime-reference/storage-api-secret).

If you see examples using `startsWith` for key prefix matching, use `beginsWith` (from `WhereConditions.beginsWith()`) instead. The legacy `storage` module used `startsWith`; `@forge/kvs` uses `beginsWith`. See [Migrating to @forge/kvs from legacy storage](/platform/forge/storage-reference/kvs-migration-from-legacy/) for more migration details.

## Quotas and limits

Each installation of your app is subject to the storage quotas and limits. See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and [Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for more details.

## Platform pricing resources

Learn more about Forge’s pricing structure, allowances, and billing by visiting [Forge platform pricing](/platform/forge/forge-platform-pricing/).

Estimate your app’s monthly costs using the [cost estimator](https://developer.atlassian.com/forge-cost-estimator), which lets you model usage and see potential charges.

## Recommendations

When using the KVS and Custom Entity Store, we strongly recommend that you:

## Scope requirement

Using the `@forge/kvs` package requires the `storage:app` scope in your manifest file:

```
```
1
2
```



```
permissions:
  scopes:
    - storage:app
```
```

See [Permissions](/platform/forge/manifest-reference/permissions/#scopes) for more information about scopes.

## Data residency

The Atlassian cloud provides features that allow admins to control and verify where their Jira and Confluence data is hosted. These features support them in meeting company requirements or regulatory obligations relating to data residency.

Forge's [persistent storage options](/platform/forge/runtime-reference/storage-api/#persistent)
use this same cloud infrastructure to store data. This allows Forge to extend similar data residency
features to your app. All data stored on Forge persistent storage automatically inherit these features.

Specifically, if your app stores data on Forge persistent storage, an admin can control where that
data is stored.
For more details about how this works, see [Data residency](/platform/forge/data-residency/).

## Partitioning

Data in Forge hosted storage is namespaced. The namespace includes all metadata relevant to an app's current installation. As a result:

* Only your app can read and write your stored data.
* An app can only access its data for the same environment.
* Keys or table names only need to be unique for an individual installation of your app.
* Data stored by your Forge app for one Atlassian app is not accessible from other Atlassian apps.
  For example, data stored in Jira is not accessible from Confluence or vice versa.
* Your app cannot read stored data from different sites, Atlassian apps, and app environments.
* [Quotas and limits](/platform/forge/platform-quotas-and-limits/#storage-limits) are not
  shared between individual installations of your app.

## Security and durability

Data is transferred, encrypted, and stored on disk according to the [Atlassian cloud’s data encryption policies](https://www.atlassian.com/trust/security/security-practices#tenant-separation). Once stored, data will persist until deleted or updated by your app.

In addition, the Atlassian Cloud backs up all [persistent](/platform/forge/runtime-reference/storage-api/#persistent) storage for disaster recovery.

## Conflict resolution

By default, Forge writes to keys using `set` or `delete` use a *last write wins* conflict resolution strategy.
You can override this behaviour using the `keyPolicy` option.

Writes to individual keys are atomic. Values are either updated in full or not at all.

## Supported values

The app storage API is able to persist any JSON data type except `null`. For example:

* arrays
* booleans
* numbers
* objects
* strings

The JavaScript storage API serializes your objects using `JSON.stringify`, and as such removes functions and the value `undefined` from any object you attempt to serialize.

## Cursors

The Key-Value Store and Custom Entity Store use cursors for paginated data access. Queries (both through the [Query builder](/platform/forge/runtime-reference/storage-api-query/) and [Complex Query builder](/platform/forge/runtime-reference/storage-api-query-complex/)) return a cursor in the results. This cursor can be provided to subsequent queries to paginate over larger data sets than you would otherwise be able to fetch.

Cursors are derived from underlying storage identifiers, and hence are subject to change anytime there is any change in how these underlying storage identifiers are created. This means that cursors are not stable and should not be persisted.

You will have to use the same parameters as the initial query. See the example below.

```
```
1
2
```



```
// Inserts some dummy data
await kvs.set('account.1', 'account 1');
await kvs.set('account.2', 'account 2');
await kvs.set('account.3', 'account 3');
await kvs.set('account.4', 'account 4');
await kvs.set('account.5', 'account 5');
await kvs.set('user.1', 'user 1');
await kvs.set('user.2', 'user 2');
await kvs.set('user.3', 'user 3');
await kvs.set('user.4', 'user 4');

// Fetch up to 2 results, but will return "account.1" and "account.2" and a cursor to next page
const { nextCursor: firstCursor } = await kvs
    .query()
    .limit(2)
    .where('key', WhereConditions.beginsWith('account.'))
    .getMany();

// Fetch up to 2 results after the cursor, but will return "account.3" and "account.4" and a cursor to next page
const { nextCursor: secondCursor } = await kvs.query()
    .limit(2)
    .where('key', WhereConditions.beginsWith('account.'))
    .cursor(firstCursor)
    .getMany();

// Fetch up to 2 results, but will only return "account.5" and no cursor
const { nextCursor: undefinedCursor } = await kvs.query()
    .limit(2)
    .where('key', WhereConditions.beginsWith('account.'))
    .cursor(secondCursor)
    .getMany();
```
```

## Key ordering

Keys are lexicographically ordered; this means, for example, that the [Query builder](/platform/forge/runtime-reference/storage-api-query/) and [Complex Query builder](/platform/forge/runtime-reference/storage-api-query-complex/)) will return entities ordered by their key. This property can be used to group related entities or build ad-hoc indexes.

The Key-Value Store and Custom Entity Store don't support indexing of arbitrary attributes. However, it is possible to support this sort of access pattern if your keys are constructed in such a way as to support indexed reads.

Hierarchical keys can be constructed to allow for nested entities to be fetched in a single list operation such as the example below.

```
```
1
2
```



```
import { kvs, WhereConditions } from '@forge/kvs';

// Nested entities
await kvs.set('survey-responses#1#{UUID}', { });
await kvs.set('survey-responses#1#{UUID}', { });
await kvs.set('survey-responses#1#{UUID}', { });
await kvs.set('survey-responses#1#{UUID}', { });

const results = await kvs
  .query()
  .where('key', WhereConditions.beginsWith('survey-response#1#'))
  .limit(10)
  .getMany();
```
```

## Data consistency

The `kvs.query` [method](/platform/forge/runtime-reference/storage-api-query/) used by the Key-Value Store is eventually consistent. This means that the method returns data that may be slightly out of date.

The `kvs.get` [method](/platform/forge/runtime-reference/storage-api-basic-api/#storage-get), on the other hand, is strictly consistent. It will always return current data.

## Legacy version

Legacy versions of the [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/) were originally provided through the `storage` module of the `@forge/api` package. For now, we will continue supporting the legacy `storage` module.

However, as of [March 17, 2025](/platform/forge/changelog/#CHANGE-2399), no further feature updates will be provided through this module. Instead, all new KVS and Custom Entity Store feature updates will only be built on modules in the @forge/kvs package. For example,
[KVS transactions](/platform/forge/storage-reference/transactions/) and
[Custom Entity Store transactions](/platform/forge/storage-reference/transactions-entities/) are only available through `@forge/kvs`.

We strongly recommend using `@forge/kvs`. Migrating to this package will only change the interface to your app’s data; all data stored through the legacy module will remain intact.

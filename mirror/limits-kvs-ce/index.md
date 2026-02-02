# KVS and Custom Entity Store limits

When using the KVS and Custom Entity Store, we strongly recommend that you:

The Atlassian Cloud backs up the entire hosted storage for disaster recovery.
This includes content stored from the Forge storage API.

## Operation limits per installation

If an installation of your app exceeds these limits due to bulk processing
(for example, triggered by a bulk issue update in Jira), consider using
the [Async events API](/platform/forge/runtime-reference/async-events-api/)
to queue your app's interactions with the KVS and Custom Entity Store. See
[Queue app interactions with storage API](/platform/forge/storage-api-limit-handling/) for guidance. While the new limits are designed to fit the majority of apps, partners with data-heavy apps can reach out to Atlassian support and ask for extended limits.

The limits listed below apply to the [Key-Value Store or Custom Entity Store](/platform/forge/runtime-reference/storage-api/)
for *each installation* of your app.

| Parameter | Limit |
| --- | --- |
| Request rate (RPS) | 1000 |
| Read (10KB request per min)\* | 4000 |
| Write (10KB request per min)\* | 4000 |

\* Request sizes are rounded up to the nearest 10KB. Requests that are 10KB or smaller are counted as 1 request. For sizes between 10KB and 20KB, they are counted as 2 requests. For example, a request with a payload of 65KB will be rounded up to 70KB, resulting in a count of 7 requests.

The new limits, compared to the current rigid per-operation limits, allow apps to distribute their usage dynamically.

## Key and object size limits

The KVS and Custom Entity Store have the following limits on keys and values.

You don't need to include any identifiers for apps or installations in your key.

Internally, Forge automatically prepends an identifier to every key, mapping it to
the right app and installation. This lets you use the full key length without risking
conflicts across apps or installations.

| Resource | Limit | Description |
| --- | --- | --- |
| Key length | 500 | Maximum length of a key |
| Key format | `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` | Keys must match the regex |
| Value size | 240 KiB | Maximum size of a single persisted value (in RAW) |
| Object depth | 31 | Maximum object depth permitted |
| Reads | 12 MB/s per key | Maximum reads permitted per second for keys |
| Writes | 1 MB/s per key | Maximum writes permitted per second for keys |
| Query | 24 MB/s per index value | Maximum queries permitted per second for index values |

## Transaction limits

The KVS and Custom Entity Store also let you package multiple operations into one transaction. Transactions are subject to the following limits:

| Category | Limit |
| --- | --- |
| Rate limit | Transactions are treated as a single **Write** operation, subject to the rate limits defined in [KVS and Custom Entity Store limits - Future Limits](/platform/forge/platform-quotas-and-limits/#future-limits). The transaction will fail if it exceeds these limits, returning a `TOO_MANY_REQUESTS` error. |
| Quota | The `transaction.set` operation is subject to the quota limits defined in [KVS and Custom Entity Store quotas](/platform/forge/platform-quotas-and-limits/#kvs-and-custom-entity-store-quotas). |
| Transaction operations | Each transaction can contain a maximum of 25 operations. |
| Unique keys | Each key can only be used once in a transaction. |
| Payload | Each transaction is limited to a payload size of 4MB. |

## Custom Entity Store limits

Custom entities (used for [complex queries](/platform/forge/runtime-reference/storage-api-query-complex/)) are subject to the following additional limits:

| Category | Requirements | Limits |
| --- | --- | --- |
| Entity | Entity names:   * Must only consist of the following characters `a-z0-9:-_.` * Must follow the regex pattern `[_a-z0-9:-.]` * Cannot start with `-` or `_` * Must not begin or end with a `.` * Must not contain the sequence `..`   In addition, an app must not have duplicate entity names. | * An app can have a maximum of 20 entities * Each entity can have a maximum of 7 custom indexes and 50 attributes * Objects that can be stored as custom entities have a maximum depth of 31 and a maximum size of 240KiB (RAW) per object * Entity names cannot be shorter than 3 characters or longer than 60 characters in length |
| Attribute | Attribute names must follow the regex `[_A-Za-z][_0-9A-Za-z]*`. | Attribute names have a maximum length of 64 characters. |
| Index | Index names must contain only the following characters `a-zA-Z0-9:-_.`, and must adhere to the following requirements:   * Must not begin or end with a `.` * Must not contain the sequence `..` * Must not be empty   In addition, each index name within an entity must be unique. | * Each entity can have a maximum of 7 custom indexes * The size of combined values for all   [range](/platform/forge/runtime-reference/custom-entities/#index-types)   attributes on any defined index cannot exceed 900 bytes * The size of combined values for all   [partition](/platform/forge/runtime-reference/custom-entities/#index-types)   attributes on any defined index cannot exceed 1700 bytes * Index names cannot be shorter than 3 characters or longer than 50 characters in length. |
| Keys | A key should:   * Follow the regex pattern `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` * Contain at least 1 character * Not be empty * Not contain only blank space(s) | A key can contain a maximum of 500 characters. |

In addition, each [complex query](/platform/forge/runtime-reference/storage-api-query-complex/)
can only have a maximum of 100 conditions
(for example, `beginsWith`, `contains`, and `isGreaterThan`). This limit applies to conditions used in
[where](/platform/forge/runtime-reference/storage-api-query-complex/#where),
[andFilter](/platform/forge/runtime-reference/storage-api-query-complex/#andfilter---orfilter), and
[orFilter](/platform/forge/runtime-reference/storage-api-query-complex/#andfilter---orfilter) filters.

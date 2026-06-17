# Forge SQL query policy

Forge SQL inspects every query submitted by your app before it reaches the
database. Queries that contain restricted functions, statements, or syntax are
rejected with a [`SQL_POLICY_VIOLATION`](/platform/forge/storage-reference/sql-handling-errors/#error-codes)
error before they execute.

This policy helps Forge SQL:

* Provide stricter compliance with [standard ANSI SQL syntax](/platform/forge/storage-reference/sql/#implementation).
* Pre-emptively increase the security posture of Forge SQL against possible
  SQL-based exploits.
* Maintain stable, predictable performance for all Forge apps using SQL storage.

The query policy applies to all queries executed through the `@forge/sql`
package, including queries run via
[`sql.prepare`](/platform/forge/storage-reference/sql-api/#prepared-statements) and
[`sql.executeRaw`](/platform/forge/storage-reference/sql-api/#execute-statement).

## Trigger statements

The following terms automatically trigger an audit when detected in a query.
Queries that use these terms are not immediately blocked, but may be rejected
based on specific patterns:

* `COMPRESS(...)`
* `UNCOMPRESS(...)` or `DECOMPRESS(...)`
* `AES_ENCRYPT(...)` or `AES_DECRYPT(...)`
* `SHA2(...)`
* `SLEEP(...)`
* `BENCHMARK(...)`
* `ALTER USER ...`
* `LOCK TABLES ...`

During a triggered audit, the query is compared against patterns that indicate risks to Forge SQL security and stability. This can result in the query being rejected entirely (with an `SQL_POLICY_VIOLATION` error) or rate-limited.

## Trigger patterns

Forge SQL also restricts certain syntax patterns, only permitting a subset of their normal use cases.

When detected in a query, Forge SQL rejects the query with a
`SQL_POLICY_VIOLATION` error.

| Restricted pattern | Description |
| --- | --- |
| Optimizer hints | Only the following optimizer hints are permitted:  * `USE_INDEX` * `IGNORE_INDEX` * `FORCE_INDEX` * `ORDER_INDEX` * `NO_ORDER_INDEX` * `HASH_JOIN` * `MERGE_JOIN` * `INL_JOIN` * `INL_HASH_JOIN` * `INL_MERGE_JOIN` * `BKA` * `NO_BKA` * `BNL` * `NO_BNL` |
| `SET` statements | Only user-variable assignments such as `SET @var=...` are permitted. Other `SET` statements, including `SET autocommit`, `SET sql_mode`, `SET GLOBAL`, and `SET INSTANCE`, are not permitted. |
| `SHOW` statements | Only the following `SHOW` statements are permitted:  * `SHOW TABLES` * `SHOW COLUMNS` * `SHOW INDEXES` (also `SHOW KEYS`) |
| SQL-level `PREPARE` statements | `PREPARE`, `EXECUTE`, or `DEALLOCATE PREPARE` statements are not permitted. Use [`sql.prepare` to safely parameterize queries](/platform/forge/storage-reference/sql-api/#prepared-statements). |
| Multiple statements | Each call to the Forge SQL API must contain only one statement. More than one `;`-separated statement in a single request is not allowed. |
| Fully qualified cross-installation table names | References to objects in another app installation's schema (for example, `SELECT * FROM other_app_installation.users`) are not permitted. Only references to objects in your own app installation's schema are allowed.  References to the `INFORMATION_SCHEMA` and `MYSQL` system schemas are permitted. |
| `USE` statements | The `USE` statement (for example, `USE other_app_installation`) is not permitted. Forge SQL automatically scopes queries to your app installation's schema, so this statement is not required. |

## Parse errors

Queries that are empty or cannot be parsed are also rejected. Parse errors are
returned as
[`SQL_EXECUTION_ERROR`](/platform/forge/storage-reference/sql-handling-errors/#error-codes)
responses that mirror the native TiDB `ER_PARSE_ERROR` shape. See
[Parse errors](/platform/forge/storage-reference/sql-handling-errors/#parse-errors)
for the full response shape.

## Handling query policy violations

When a query is rejected, the response includes a `suggestion` field describing
the recommended action. See
[Error response shapes](/platform/forge/storage-reference/sql-handling-errors/#error-response-shapes)
for details and an example of handling a `SQL_POLICY_VIOLATION` error.

## Request an exemption or change

If your app has a use case that requires a restricted function or statement,
you can request an exemption or propose a change to the policy through
[Developer and Marketplace Support](https://ecosystem.atlassian.net/servicedesk/customer/portal/34/group/3534/create/4180).

Include the following information in your request:

* The `app.id` of your Forge app.
* The exact query (or queries) that you need to run.
* A description of the use case and why the restricted function or statement
  is required.
* Any alternative approaches you have evaluated.

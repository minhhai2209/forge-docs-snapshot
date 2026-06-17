# Forge changelog

Forge SQL now inspects every query submitted by your app before it reaches the database. Queries that contain restricted functions, statements, or syntax are rejected with a new **SQL\_POLICY\_VIOLATION** error code *before* execution.

We’ve implemented this new policy to enforce the following:

* Stricter compliance with standard ANSI SQL syntax.
* Pre-emptive protection against SQL-based resource exhaustion and exploits.
* Stable, predictable performance across all Forge apps using SQL storage.

**New error code: SQL\_POLICY\_VIOLATION**

If your app submits a query that uses a restricted function or pattern, the `@forge/sql` package will return an error with a `code`, `message`, and `suggestion` field to help you resolve the violation.

**Restricted functions and statements**

The following are now monitored and may trigger rejection:

* **Functions:** `SLEEP()`, `BENCHMARK()`, `COMPRESS()`, `UNCOMPRESS()`, `AES_ENCRYPT()`, `AES_DECRYPT()`, `SHA2()`
* **Statements:** `ALTER USER`, `LOCK TABLES`, `USE <table>`
* **Patterns:** Unsupported optimizer hints, `SET GLOBAL`/`SET INSTANCE`, most `SHOW` statements, SQL-level `PREPARE`/`EXECUTE`/`DEALLOCATE PREPARE`, and multi-statement queries.

A subset of `SET`, `SHOW`, `USE` and optimizer hints remain permitted. See the [SQL query policy documentation](https://developer.atlassian.com/platform/forge/storage-reference/sql-query-policy/ "https://developer.atlassian.com/platform/forge/storage-reference/sql-query-policy/") for the full allowlist.

**What you need to do**

* **Review your queries:** If your app uses any restricted functions or syntax patterns, those queries will now be rejected at runtime.
* **Update error handling:** Check for `errorCodes.SQL_POLICY_VIOLATION` alongside existing error codes to handle rejections gracefully.

If your app requires a restricted function for a valid use case, request an exemption through the [Developer Support portal](https://ecosystem.atlassian.net/servicedesk/customer/portal/34/group/3534/create/4180 "https://ecosystem.atlassian.net/servicedesk/customer/portal/34/group/3534/create/4180") with your `app.id`, the query, and the use case.

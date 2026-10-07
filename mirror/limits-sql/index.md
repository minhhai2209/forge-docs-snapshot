# Forge SQL limits

Forge SQL offers a multi-tenant SQL solution offering tenant isolation and stable query performance. To do so, we add a few constraints over and above TiDB's limitations:

* Foreign keys are not supported. You can still perform `JOIN` operations, but `DELETE` operations will not be cascaded.
* Each SQL statement can only contain a single query.

The following limits also apply:

### Per-install limits

The following limits are applied to your app's Forge SQL usage on a per-install basis:

| Resource | Limit |
| --- | --- |
| Total stored data | 1 GiB (`production` installs) |
| 256 MiB (`staging` installs) |
| 128 MiB (`development` or custom environment installs) |
| Number of tables | 200 |
| DML Requests per second (RPS) | 150 |
| DDL Requests per minute (RPM) | 25 |
| Size per row | 6Mib |
| Total query execution time for all current invocations | 62.5 seconds (within each minute) |

App databases provisioned and managed via Forge SQL are backed up periodically.

### Query and response limits

The following limits apply to each query sent and response received by your app's Forge SQL database functions:

| Resource | Limit |
| --- | --- |
| Memory usage per query | 16 MiB |
| Query time per minute (s/minute) | 62.5 seconds |
| Request size | 1 MiB |
| Response size | 4 MiB |
| Per-connection timeout for `SELECT` queries | 5 seconds |
| Per-connection timeout for `INSERT`, `UPDATE`, and `DELETE` queries | 10 seconds |
| Per-connection query timeout for [DDL queries](/platform/forge/storage-reference/sql-api-schema/#manage-database-schemas) | 20 seconds |

### Versioning

If you add Forge SQL to an existing app, admins of that app's current installations must review and consent before updating.

As such, adding Forge SQL to an existing app will require a [major version upgrade](/platform/forge/versions/#major-version-upgrades). This will be triggered through the `sql`
[module](/platform/forge/manifest-reference/modules/sql/)
(which is required to enable the feature on an app).

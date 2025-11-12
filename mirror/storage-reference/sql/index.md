# Forge SQL

Forge SQL is a hosted storage capability that will let you use an SQL database for your app. With this capability, Forge will provision and host your app’s database (and, by extension, host your customer’s app data) on Atlassian infrastructure.

Forge SQL provisions a single database instance per installation. That is, each instance will be associated to a specific installation of your app. As a result, each app installation will have its own dedicated database instance; this instance will store only data specific to its corresponding installation.

## Implementation

Forge SQL is based on a MYSQL-compliant, distributed SQL database. We've configured
Forge SQL to comply with standard ANSI-compliant SQL. To allow for optimal data
portability outcomes, we strongly encourage you use standard ANSI SQL syntax when
interacting with the database.

Forge SQL is currently based on a
[self-hosted TiDB](https://docs.pingcap.com/tidb/stable/dev-guide-overview) implementation, and we impose limitations on how the database can be used to support Forge use cases.

We recommend that you avoid designing applications with TiDb-specific functionality.

## Platform pricing resources

Learn more about Forge’s pricing structure, allowances, and billing by visiting [Forge platform pricing](/platform/forge/forge-platform-pricing/).

Estimate your app’s monthly costs using the [cost estimator](https://developer.atlassian.com/forge-cost-estimator), which lets you model usage and see potential charges.

## Limitations

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
| Per-connection query timeoutfor [DDL queries](/platform/forge/storage-reference/sql-api-schema/#manage-your-database-schema) | 20 seconds |

### SOC2 and ISO compliance

Forge SQL has not yet undergone external assessment for SOC 2 or ISO certification. As we continue development on Forge SQL, we will aim to include it in our standard audit certification reporting cycle.

### Versioning

If you add Forge SQL to an existing app, admins of that app's current installations must review and consent before updating.

As such, adding Forge SQL to an existing app will require a [major version upgrade](/platform/forge/versions/#major-version-upgrades). This will be triggered through the `sql` module (which is required to enable Forge SQL on an app).

## Schema management

Forge SQL provisions databases for each individual installation, thereby isolating each customer’s data. This helps secure each database and optimise its performance, at least in relation to each customer’s stored data.

With this implementation, your app’s database schema needs to be applied as soon as the app is installed. As such, schema management with Forge SQL is split into two phases:

* **Queueing**: Queue Data Definition Language (DDL) operations to create the database objects that make up your schema. You can use a special Forge SQL SDK for this, which will let you define each operation (and the order they should be run). To update your app’s schema, simply add DDL operations as needed.
* **Execution**: Using a [scheduled trigger](/platform/forge/function-reference/scheduled-trigger/), Forge SQL can execute your queued DDL operations when the app is installed or whenever you update the schema. Forge SQL can track which DDL operations need to be executed on which specific installations, and which ones need to be re-run (in case of errors).

During the execution phase, Forge SQL will also take care of migrating data between older and newer schema versions.

[Manage database schema

Learn more about defining and updating your app’s SQL database schema.](/platform/forge/storage-reference/sql-api-schema/)

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

## Monitoring

Forge SQL provides reliability and latency metrics to help you understand your app’s database interactions. It also provides some observability into the health of each provisioned database, as well as their respective schemas.

To view these metrics:

1. Access the [developer console](https://developer.atlassian.com/console/myapps).
2. Select **SQL** in the left menu (under **STORAGE**).

From there, you can choose between the following observability options:

* **Monitor**: tracks your app’s reliability and performance. You can do this across all installations, or filter information by any combination of site, environment, or time frame. See
* **Manage**: provides insights on database schemas for individual installations.

See [Monitor SQL](/platform/forge/monitor-sql-metrics/) for detailed information.

## Recommendations

* Ensure that each change to your SQL database is backwards compatible to all schema versions that are currently in use. Every DDL operation you define should introduce schema changes that won’t block data migrations from previous versions.
* Likewise, each SQL database change should be compatible to all versions of your app currently installed on a customer site. This means, for example, that every SQL query used by previous versions of your app should also work in the latest version of your SQL database.
* Avoid destructive changes to your SQL database, as these risk breaking compatibility between database schema versions.
* Avoid using `AUTO_INCREMENT` fields in your tables, as this could cause
  [*hotspot* issues](https://docs.pingcap.com/tidb/stable/auto-increment/#auto_increment) when used on databases with very large datasets. We recommend either of the following strategies instead:
  * Use `AUTO_RANDOM(S,R)` to limit the size of the integer between `-(2^53)+1` and `(2^53)-1`. This will ensure that the BIGINT column can be represented accurately within Forge SQL's JSON response payload. We also recommend that you review [TiDB documentation](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues/#handle-auto-increment-primary-key-hotspot-tables-using-auto_random) for information on auto-incrementing primary key hotspot tables.
  * Store UUIDs as `BINARY(16)` type (see [TiDB documentation](https://docs.pingcap.com/tidb/stable/uuid/#overview-of-uuids)).

## Migration

If you are planning to migrate your app from an existing remote SQL database, we recommend that you consult our [Forge SQL migration guide](/platform/forge/storage-reference/sql-migration-guide/) for guidance and tips.

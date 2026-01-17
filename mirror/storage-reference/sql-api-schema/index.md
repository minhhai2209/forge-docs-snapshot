# Manage your database schema

Use *Data Definition Language (DDL)* to create and update database objects (such as tables and indexes) in your provisioned SQL database. Forge SQL supports MySQL-compatible DDL operations like `CREATE`, `ALTER`, and `DROP` (for more details, see
[SQL Statement Overview](https://docs.pingcap.com/tidb/stable/sql-statement-overview) in the TiDB documentation).

You can create as many DDL operations as needed. Forge SQL can use `scheduledTrigger` to execute each operation on each provisioned SQL database in the sequence you specify.

You can also update your app’s database schema by adding new DDL operations over time. Forge SQL can:

1. Track which operations have already been executed on any installation of your app.
2. Track failed DDL operations, and re-run them later.
3. Migrate data between old and new database schemas.

## Before you begin

The `sql` package provides the necessary methods for interacting with Forge SQL. To start using Forge SQL’s capabilities, you’ll need to install it in your project:

```
```
1
2
```



```
npm install @forge/sql
```
```

You can use the `migrationRunner` SDK to execute DDL operations. To import it:

```
```
1
2
```



```
import migrationRunner from `@forge/sql` ;
```
```

When using the `migrationRunner` SDK, your app should only have one `migrationRunner` invocation.

## Define schema updates

Use DDL operations to create and update each database object in your schema. Use the `migrationRunner.enqueue` method to queue these operations in the order they should be executed. This method accepts a list of ordered DDL operations, with each one defined as a key/value pair consisting of:

* a unique `operationName`
* a pre-defined DDL function

### Example

The following snippet defines two DDL operations, `CREATE_USERS_TABLE` and `CREATE_BOOKS_TABLE`, both of which create tables for our provisioned database.

```
```
1
2
```



```
import { migrationRunner } from '@forge/sql';

export const CREATE_USERS_TABLE = `CREATE TABLE IF NOT EXISTS Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
)`;

export const CREATE_BOOKS_TABLE = `CREATE TABLE IF NOT EXISTS Books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    published_date DATE
)`;
```
```

To invoke both DDL operations through `migrationRunner.enqueue`, assign an `operationName` to each one (`v001_create_users_table` and `v002_create_books_table`):

```
```
1
2
```



```
const createDBobjects = migrationRunner
  .enqueue('v001_create_users_table', CREATE_USERS_TABLE)
  .enqueue('v002_create_books_table', CREATE_BOOKS_TABLE)
```
```

Next, wrap `createDBobjects` in a single database object creation function (`runMigration`). This will let you map its key to a scheduled trigger, which Forge will use to execute it (this is covered in the [next section](#executeddl)):

```
```
1
2
```



```
export const runMigration = async () => {
  try {
    await applyMigrations();
  };

export const applyMigrations = async () => {
  const successfulMigrations = await createDBobjects.run();
  console.log('Migrations applied:', successfulMigrations);
};
```
```

[Creating database objects

Our example app uses DDL operations to define each database object, then orders them in the sequence they should be executed. This sequence is then wrapped in a single database object creation function.](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts)

## Orchestrate schema updates

Database object creation (that is, your DDL operations) needs to be executed as part of the app installation process. One way to orchestrate this is through *scheduled triggers*. Doing so assigns the entire lifecycle of creating your database objects to Forge SQL.

Map your database object creation function to a
[scheduled trigger](/platform/forge/function-reference/scheduled-trigger/) module in your manifest. Forge will use the trigger to execute your `migrationRunner` invocation according to your defined `interval` (we recommend `hourly` or `daily`).

### Example

The following declaration triggers the `runMigration` function from the
[previous example](#migrationrunnerexample):

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: my-db-schema
      function: runMigration
      interval: hour 
  function:
    - key: runMigration
      handler: index.trigger
```
```

Here, Forge will execute `runMigration` within the *hour* after app installation. As such, it is possible for customers to have your app already installed, without the database schema applied yet.

Forge SQL will check each app installation hourly if there are any failed or pending DDL functions (tracking them based on their `operationName`). Forge SQL will run pending DDL functions and re-run failed ones.

[Orchestrate DDL operations

In our sample app, the database object creation function is mapped to a scheduled trigger. This lets Forge manage the lifecycle of your database object creation (and database schema migration later on, if needed).](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/manifest.yml#lines-13)

## Log schema updates

The `migrationRunner.list` method lists all the DDL operations you queued (through `migrationRunner.enqueue`), along with the status of each one. Use it to generate *logs* for your database object creation function; this will allow you to track its progress for each app installation.

Use your [app logs](/platform/forge/view-app-logs/#view-app-logs) in the Developer Console to view these generated logs. From there, you can filter for errors against your database object creation function.

### Example

The following snippet expands on our [earlier example](#migrationrunnerexample) by adding a `migrationRunner.list` invocation to create logs for the `runMigration` function:

```
```
1
2
```



```
export const applyMigrations = async () => {
  await createDBobjects.run();

  console.log('Migrations checkpoint [after running migrations]:');
  await migrationRunner
    .list()
    .then((migration) => migration.map((y) => console.log(`${y.name} migrated at ${y.migratedAt.toUTCString()}`)));
  };
```
```

[Generate logs

Our sample app’s database object creation function generates logs for each operation. These logs let you track the progress of each schema application (and update) for every app installation.](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts#lines-48)

## Monitoring

You can inspect each installation's SQL database schema through the developer console.
The developer console can display:

* The size of your database.
* Which schema updates have already been applied.
* The database objects present in the current schema.
* The contents of each table within your database (this is only available for your
  [cloud developer site](/platform/forge/build-a-hello-world-app-in-jira/#set-up-a-cloud-developer-site)'s
  development, custom, or staging environment).

See [Monitoring SQL](/platform/forge/monitor-sql-metrics/) for more information.

### Hidden fields

The **Table data** tab within the **Schema viewer** won't display fields with the following database data types:

* `BLOB`
* `MEDIUMBLOB`
* `LONGBLOB`
* `BINARY`
* `VARBINARY`
* `CLOB`
* `TEXT`
* `IMAGE`
* `XML`
* `JSON`

These field are hidden to prevent the display of possibly large data payloads. These fields won't be included in the records
provided through the **Download** button either.

## Recommendations

* Ensure that each change to your SQL database is backwards compatible to all schema versions that are currently in use. Every DDL operation you define should introduce schema changes that won’t block data migrations from previous versions.
* Likewise, each SQL database change should be compatible to all versions of your app currently installed on a customer site. This means, for example, that every SQL query used by previous versions of your app should also work in the latest version of your SQL database.
* Avoid destructive changes to your SQL database, as these risk breaking compatibility between database schema versions.
* Avoid using `AUTO_INCREMENT` fields in your tables, as this could cause
  [*hotspot* issues](https://docs.pingcap.com/tidb/stable/auto-increment/#auto_increment) when used on databases with very large datasets. We recommend either of the following strategies instead:
  * Use `AUTO_RANDOM(S,R)` to limit the size of the integer between `-(2^53)+1` and `(2^53)-1`. This will ensure that the BIGINT column can be represented accurately within Forge SQL's JSON response payload. We also recommend that you review [TiDB documentation](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues/#handle-auto-increment-primary-key-hotspot-tables-using-auto_random) for information on auto-incrementing primary key hotspot tables.
  * Store UUIDs as `BINARY(16)` type (see [TiDB documentation](https://docs.pingcap.com/tidb/stable/uuid/#overview-of-uuids)).

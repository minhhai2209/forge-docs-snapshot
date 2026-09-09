# Manage database schemas

Use *Data Definition Language (DDL)* to create and update database objects (such as tables and indexes) in your provisioned SQL database. Forge SQL supports MySQL-compatible DDL operations like `CREATE`, `ALTER`, and `DROP` (for more details, see
[SQL Statement Overview](https://docs.pingcap.com/tidb/stable/sql-statement-overview) in the TiDB documentation).

You can create as many DDL operations as needed. Forge SQL can use an [async event consumer](#orchestrate-with-an-async-event-consumer-recommended) (recommended) or a [scheduled trigger](#orchestrate-with-a-scheduled-trigger) to execute each operation on each provisioned SQL database in the sequence you specify.

You can also update your app’s database schema by adding new DDL operations over time. Forge SQL can:

1. Track which operations have already been executed on any installation of your app.
2. Track failed DDL operations, and re-run them later.
3. Migrate data between old and new database schemas.

## Before you begin

The `sql` package provides the necessary methods for interacting with Forge SQL. To start using Forge SQL’s capabilities, you’ll need to install it in your project:

```
1npm install @forge/sql
2
```

You can use the `migrationRunner` SDK to execute DDL operations. To import it:

```
```
1
2
```



```
import migrationRunner from '@forge/sql';
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
3
4
5
6
7
8
9
10
11
12
13
14
15
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
3
4
```



```
const createDBobjects = migrationRunner
  .enqueue('v001_create_users_table', CREATE_USERS_TABLE)
  .enqueue('v002_create_books_table', CREATE_BOOKS_TABLE)
```
```

Next, wrap `createDBobjects` in a single database object creation function (`runMigration`). This will let you map its key to an async event consumer or scheduled trigger, which Forge will use to execute it (this is covered in the [next section](#executeddl)):

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
```



```
export const runMigration = async () => {
  try {
    await applyMigrations();
  } catch (error) {
    console.error('Migration failed:', error);
    throw error;
  }
};

export const applyMigrations = async () => {
  const successfulMigrations = await createDBobjects.run();
  console.log('Migrations applied:', successfulMigrations);
};
```
```

[Creating database objects

Our example app uses DDL operations to define each database object, then orders them in the sequence they should be executed. This sequence is then wrapped in a single database object creation function.

[Refer to sample code](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts)](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts)

## Orchestrate schema updates

Database object creation (that is, your DDL operations) needs to be executed as part of the app installation process. You can orchestrate this through either an [async event consumer](#orchestrate-with-an-async-event-consumer-recommended) or a [scheduled trigger](#orchestrate-with-a-scheduled-trigger). In both cases, Forge SQL manages the lifecycle of creating your database objects.

We recommend orchestrating schema updates through an [async event consumer](/platform/forge/runtime-reference/async-events-api/#event-consumer). The async event handler provides a maximum runtime of 15 minutes, compared to the 55-second standard function timeout. This longer runtime makes it much easier to stay within the [per-install DDL rate limit](/platform/forge/storage-reference/sql/#per-install-limits) (25 DDL requests per minute) when applying a large number of schema changes.

### Orchestrate with an async event consumer (recommended)

To orchestrate schema updates through the [async events API](/platform/forge/runtime-reference/async-events-api/):

1. Define a queue and an event consumer in your manifest that invokes your `runMigration` function. Set `timeoutSeconds` on the function to allow up to 15 minutes (900 seconds) of runtime.
2. Push an event to the queue when your app is installed or upgraded. You can do this from a [product event trigger](/platform/forge/events-reference/) (such as `avi:forge:installed:app`) or from a [scheduled trigger](/platform/forge/function-reference/scheduled-trigger/) that runs periodically to retry any pending or failed migrations.

#### Example

The following manifest declares a queue named `schema-migration-queue` and a consumer that calls `runMigration` with a 15-minute timeout:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
```



```
modules:
  consumer:
    - key: schema-migration-consumer
      queue: schema-migration-queue
      function: runMigration
  trigger:
    - key: app-installed-trigger
      function: enqueueMigration
      events:
        - avi:forge:installed:app
        - avi:forge:upgraded:app
  function:
    - key: runMigration
      handler: index.runMigration
      timeoutSeconds: 900
    - key: enqueueMigration
      handler: index.enqueueMigration
```
```

`avi:forge:upgraded:app` is sent only when the app is upgraded to a new **major version**. It does not trigger on minor or patch version upgrades. If you add new DDL operations in a minor or patch release, use a [scheduled trigger](/platform/forge/function-reference/scheduled-trigger/) or another mechanism to ensure migrations run.

The `enqueueMigration` function pushes an event to the queue:

```
```
1
2
3
4
5
6
7
8
```



```
import { Queue } from '@forge/events';

const queue = new Queue({ key: 'schema-migration-queue' });

export const enqueueMigration = async () => {
  await queue.push({});
};
```
```

The following `runMigration` implementation replaces the one defined in the [Define schema updates](#migrationrunnerexample) section. It adds retry logic suitable for use as an async event consumer.

The consumer function calls `migrationRunner.run()` from within the async event handler. We recommend wrapping the call in [retry logic](#retry-logic-and-idempotency) with a 60-second timeout to gracefully handle transient DDL rate-limit errors:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
```



```
import { migrationRunner } from '@forge/sql';

const RETRY_TIMEOUT_MS = 60000;

export const runMigration = async (event, context) => {
  const deadline = Date.now() + RETRY_TIMEOUT_MS;
  let lastError;

  while (Date.now() < deadline) {
    try {
      const successfulMigrations = await migrationRunner.run();
      console.log('Migrations applied:', successfulMigrations);
      return;
    } catch (error) {
      lastError = error;
      console.warn('Migration attempt failed, retrying:', error);
      // Back off briefly before retrying. Adjust the delay to suit your app.
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }
  }

  // Let the async events API retry the event within the retention window.
  throw lastError;
};
```
```

If the consumer function returns an error, the async events API will [retry the event within the retention window](/platform/forge/runtime-reference/async-events-api/#retries). This means transient failures (such as exceeding the per-install DDL rate limit) will be retried automatically.

### Orchestrate with a scheduled trigger

Alternatively, you can map your database object creation function to a
[scheduled trigger](/platform/forge/function-reference/scheduled-trigger/) module in your manifest. Forge will use the trigger to execute your `migrationRunner` invocation according to your defined `interval` (we recommend `hourly` or `daily`).

Scheduled trigger functions are subject to the standard 55-second function timeout. If your migration cannot reliably complete within this window (for example, because it contains many DDL statements or repeatedly hits the per-install DDL rate limit), use the [async event consumer approach](#orchestrate-with-an-async-event-consumer-recommended) instead.

#### Example

The following declaration triggers the `runMigration` function from the
[previous example](#migrationrunnerexample):

```
```
1
2
3
4
5
6
7
8
9
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

In our sample app, the database object creation function is mapped to a scheduled trigger. This lets Forge manage the lifecycle of your database object creation (and database schema migration later on, if needed).

[Refer to sample manifest](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/manifest.yml#lines-13)](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/manifest.yml#lines-13)

### Retry logic and idempotency

Regardless of which orchestration approach you use, follow these guidelines to make your schema migrations resilient:

* **Retry `migrationRunner.run()` with a 60-second timeout.** The per-install [DDL rate limit](/platform/forge/storage-reference/sql/#per-install-limits) (25 DDL requests per minute) can cause transient failures when applying many schema changes. Wrapping `migrationRunner.run()` in a retry loop with a 60-second timeout gives the rate limit time to reset before the next attempt.
* **Make DDL statements idempotent.** Always use idempotent forms such as `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, and `DROP TABLE IF EXISTS`. Idempotent DDL ensures that retries and re-runs do not fail because an object already exists (or does not exist).
* **Throw on unrecoverable errors.** When using the async event consumer, throw the error after the 60-second retry window expires. The async events API will then retry the event within the [retention window](/platform/forge/runtime-reference/async-events-api/#retention-window).

## Log schema updates

The `migrationRunner.list` method lists all the DDL operations you queued (through `migrationRunner.enqueue`), along with the status of each one. Use it to generate *logs* for your database object creation function; this will allow you to track its progress for each app installation.

Use your [app logs](/platform/forge/view-app-logs/#view-app-logs) in the Developer Console to view these generated logs. From there, you can filter for errors against your database object creation function.

### Example

The following snippet expands on our [earlier example](#migrationrunnerexample) by adding a `migrationRunner.list` invocation to create logs for the `runMigration` function:

```
```
1
2
3
4
5
6
7
8
9
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

Our sample app’s database object creation function generates logs for each operation. These logs let you track the progress of each schema application (and update) for every app installation.

[Refer to sample code](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts#lines-48)](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts#lines-48)

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

For a complete reference of supported data types and how they are returned by the Forge SQL API, see [Forge SQL data types](/platform/forge/storage-reference/sql-data-types/).

## Recommendations

* Orchestrate schema migrations through an [async event consumer](/platform/forge/storage-reference/sql-api-schema/#orchestrate-with-an-async-event-consumer-recommended) so your `migrationRunner.run()` invocation has up to 15 minutes of runtime to complete. This is especially important when applying many DDL statements that may hit the [per-install DDL rate limit](/platform/forge/storage-reference/sql/#per-install-limits).
* Wrap `migrationRunner.run()` in [retry logic](/platform/forge/storage-reference/sql-api-schema/#retry-logic-and-idempotency) with a 60-second timeout to gracefully recover from transient DDL rate-limit errors.
* Make every DDL statement idempotent (for example, use `CREATE TABLE IF NOT EXISTS` and `DROP TABLE IF EXISTS`) so that retries and re-runs are safe.
* Ensure that each change to your SQL database is backwards compatible to all schema versions that are currently in use. Every DDL operation you define should introduce schema changes that won’t block data migrations from previous versions.
* Likewise, each SQL database change should be compatible to all versions of your app currently installed on a customer site. This means, for example, that every SQL query used by previous versions of your app should also work in the latest version of your SQL database.
* Avoid destructive changes to your SQL database, as these risk breaking compatibility between database schema versions.
* Avoid using `AUTO_INCREMENT` fields in your tables, as this could cause
  [*hotspot* issues](https://docs.pingcap.com/tidb/stable/auto-increment/#auto_increment) when used on databases with very large datasets. We recommend either of the following strategies instead:
  * Use `AUTO_RANDOM(S,R)` to limit the size of the integer between `-(2^53)+1` and `(2^53)-1`. This will ensure that the BIGINT column can be represented accurately within Forge SQL's JSON response payload. We also recommend that you review [TiDB documentation](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues/#handle-auto-increment-primary-key-hotspot-tables-using-auto_random) for information on auto-incrementing primary key hotspot tables.
  * Store UUIDs as `BINARY(16)` type (see [TiDB documentation](https://docs.pingcap.com/tidb/stable/uuid/#overview-of-uuids)).

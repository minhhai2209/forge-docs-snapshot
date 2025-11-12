# Migrating from a remote SQL database to Forge SQL

If your app uses an SQL databases hosted on a Forge Remote service, you may be interested in
migrating your data to Forge SQL. In doing so, your app data will be hosted on the Atlassian Cloud,
where it can be managed, stored, and secured on Forge hosted storage. Hosting all of your app data
on Forge hosted storage takes you one step closer to eligibility for
[Runs on Atlassian](/platform/forge/runs-on-atlassian/), among other benefits.

## Expectations

This guide provides general guidance on how to migrate data to Forge SQL from an SQL database hosted on a Forge Remote. If your app is currently implemented on Connect, we strongly recommend that you adopt Forge first. See [Incrementaly adopting Forge from Connect](/platform/adopting-forge-from-connect/) and [Forge Remote](/platform/forge/remote/) for details.

In this guide, we’ll focus on how to plan and execute a data migration with minimal downtime. This assumes that you're migrating all of your app's data, and will control each when stage of the migration, and implement ways to roll back if needed. Migrating with minimal downtime adds complexities not present in a migration with downtime; however, the former may be preferred by developers as it offers the least disruption to customers.

This guide also assumes the following:

* You are well-versed in SQL databases, as your app already uses one.
* You are familiar with the Forge platform.
* You have already familiarised yourself with [Forge SQL](/platform/forge/storage-reference/sql/).

## Considerations

When migrating data to Forge SQL from a remote SQL database, you'll need to consider several factors:

### Platform limits and quotas

The migration process will be affected by some Forge runtime, invocation, and size limits. In particular, [Forge functions have a limited runtime](/platform/forge/platform-quotas-and-limits/#invocation-limits), which affects how long you can migrate data in a single Forge app call. A standard invocation is capped at 25 seconds, but using our Async Events API can extend this to 900 seconds.

It is also essential that you review [Forge SQL's quotas and limits](/platform/forge/platform-quotas-and-limits/#forge-sql-limits), which also affect maximum query and request sizes.

### Forge SQL implementation

You must consider the differences between the target Forge SQL database and your existing database, along with our partitioning model for each installation.

Forge SQL is built on TiDB, and uses MySQL-compatible syntax. Forge SQL's implementation has the following constraints:

* Incomplete support for foreign keys in Forge SQL.
* Only one query statement can be executed at a time.
* Transactions are not yet supported.

See [Forge SQL limitations](/platform/forge/storage-reference/sql/#limitations) for a complete list.

### Customer migration state tracking

The migration process involves monitoring the migration process of each customer. Doing so lets you determine when it’s safe to remove your app’s remote modules and decommission your remote SQL database.

Before you begin this, you'll need to list all of your app's existing customer installations. See [View app installations](/platform/forge/view-app-installations/) for details on how.

### Accessing data from remote

To pull data from the source SQL database, you’ll need to expose additional APIs from its Forge Remote that your app can call. Refer to [Invoke Remote API](/platform/forge/runtime-reference/invoke-remote-api/) for related information on how to do this. Data migration will require exposing 1-2 remote APIs.

### Per-installation database schema

Forge SQL provisions a single database instance per installation. That is, each instance will be associated to a specific installation of your app. As a result, each app installation will have its own dedicated database instance; this instance will store only data specific to its corresponding installation.

If your source is a monolithic SQL database containing all customer data, you must refactor it into a schema that aligns with Forge SQL’s per-installation approach. For details on constructing and implementing schemas for Forge SQL, refer to [Manage database schemas](/platform/forge/storage-reference/sql-api-schema/).

## Components

Planning and executing a migration requires building several components. This section explores those components and their respective roles.

### Migration events queue

The [Async Events API](/platform/forge/runtime-reference/async-events-api/) lets you run background jobs for up to 900 seconds, overcoming the standard 25-second runtime limit for Forge functions. This is essential for handling large or staged data migrations.

Use this API to queue migration events, which will be executed asynchronously. Each async event will also have a corresponding *job ID*, which you can use for tracking its progress.

#### Events logic

When designing your async events implementation, you can choose between two logic types: fan out or single event.

| Fan out | Single event |
| --- | --- |
| A fan out approach maps an async job to a data type, table, or capability of data you are migrating. While this approach is likely faster, it is more complex and risks hitting Forge invocation limits. | You can also use a single event to manage the migration. This is slow, but is less likely to hit rate limits. With this strategy, you’ll need to track syncing specific data types over that period. |

Given that data migration is I/O-bound, consider how you can leverage Javascript async code to get some equivalent parallelisation from your app during data migration.

When implementing your event management logic, you should consider:

* how many events do you need running at once
* how to avoid data concurrency issues
* the platform rate limits you might run into
* your own services rate limits as are called to pull data.
* how you will track progress of the migration.
* whether there are Javascript async tools you can also leverage to make the most use of each event

#### Example async event function

To add an async event function, start with its manifest entry. For example:

```
```
1
2
```



```
modules:
    function:
    - key: data-migrations-function
      handler: migration.handler
      # This enables the maximum runtime of an async events call
      timeoutSeconds: 900
  consumer:
    - key: forge-data-migration-queue-consumer
      queue: forge-data-migration-queue # is the key you will use in your code
      resolver:
        function: data-migrations-function
        method: dataMigrationQueueListener
```
```

You can queue multiple async events and store their job status details on a separate migration state table (more on this in [the next section](#migration-state-table)):

```
```
1
2
```



```
import { Queue } from "@forge/events";
import { dataMigrationDB } from "./data-migration/sql";

// key matches what is defined in the manifest.yml
const dataMigrationQueue = new Queue({ key: "forge-data-migration-queue" });

// You can use a single event to do the data migration
export async function startMigrationJob() {
  const { jobId } = await dataMigrationQueue.push({ body: {} });
  await dataMigrationDB.insertJob(jobId);
}

// OR fan out to multiple ones
const DATA_TYPES = ['users', 'stuff', 'things', 'related_things']
export async function startMigrationJobs() {

  // this will span a new event job for each data type above
  for(const dataType in DATA_TYPES) {
     const { jobId } = await dataMigrationQueue.push({ body: { dataType } });
    await dataMigrationDB.insertJob(jobId);
  }
}
```
```

### Migration state table

You’ll need to track the state of each customer's migration. You can do this on a table on either your source SQL database or the customer’s Forge SQL database. You can also use this table (or have a separate one in Forge SQL itself, if using remote to track customer migration state), to track the migration stages in a given installation.

#### Example state table

The following table shows some useful basics for tracking migration state:

```
```
1
2
```



```
CREATE TABLE IF NOT EXISTS ForgeDataMigrations (
    id BINARY(16) DEFAULT (UUID_TO_BIN(UUID())),
    jobId VARCHAR(256) UNIQUE NOT NULL ,
    status VARCHAR(20) NOT NULL,
    metadata VARCHAR(256),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    finished_at DATETIME
)
```
```

This table contains the following fields:

| Field | Description |
| --- | --- |
| `jobId` | Async events return a `jobId` when created. You can use this to put in some custom fields to track overall progress, without needing a separate table. |
| `id` | Primary key to avoid duplicate `jobIds`. The TiDB documentation recommends the [use of UUIDs as the primary key](https://docs.pingcap.com/tidb/stable/uuid/#overview-of-uuids). |
| `status` | Used to hold the status of the job. Should map to status codes: `READY`, `PENDING`, `IN_PROGRESS`, or `DONE`. |
| `metadata` | This is effectively a free text field to include any information you need. You can replace this with specific fields that make sense for your app migration flow. |
| `*_date` | Used for reporting information for each job. |

To track the overall status of the data migration, you can use a fixed `jobId` value to monitor the overall status of the data migration:

```
```
1
2
```



```
export const DATA_MIGRATION_TRACKING_STATE_ID = "__DATA_MIGRATION__";
```
```

You can then check the status of the overall migration by checking for this specific field:

```
```
1
2
```



```
await sql
      .prepare<{status: String}>("SELECT status FROM ForgeDataMigrations WHERE jobId = ?")
      .bindParams(DATA_MIGRATION_TRACKING_STATE_ID)
      .execute();
```
```

### State tracker function

The migrations status tracker will check the installation’s migration status (`PENDING`, `READY`, `IN_PROGRESS`, or `DONE`) and react accordingly. This function’s logic works as follows:

1. Check the destination Forge SQL database if a migration is `DONE` or `IN_PROGRESS`. This acts as a short circuit for calling your remote service. This could be just remote, but should be as fast, and can help you migrate away from being in the loop.
2. Next, check the source SQL database for the status. Then, either update the status as needed, or re-start the migration as needed.

#### Example migration state tracker function

The following example function demonstrates this logic:

```
```
1
2
```



```
import { invokeRemote } from '@forge/api';
import { dataMigrationDB, DATA_MIGRATION_TRACKING_STATE_ID } from './data-migration/sql';

// This function is called by a scheduled trigger, webhook, or even a user via the UI
// Will be used to start the data migration process
export const migrate = async (req) => {
  const migrationJob = await dataMigrationDB.getJob(DATA_MIGRATION_TRACKING_STATE_ID)

  // Short-circuit if the migration is already completed, don't call remote service
  switch (migrationJob.status) {
    case dataMigrationDB.status.PENDING:
      console.log("Migration is pending, not starting migration");
      // now we can check the remote status
      break;
    case dataMigrationDB.status.COMPLETED:
      console.log("Migration is completed, no action needed");
      return;
    case dataMigrationDB.status.MIGRATING:
      console.log("Migration is in progress, checking status and continuing if needed");
      await checkMigrationJobs();
      return;
  }

  // Check-in to remote service to get migration status
  // This can return a status, or any migration data you need to get started
  const remoteMigrationState = await invokeRemote('get-migration-status')

  switch (remoteMigrationState.status) {
    case dataMigrationDB.status.PENDING:
      console.log("Migration is pending, not starting migration");
      return;
    case dataMigrationDB.status.COMPLETED:
      // update the local state to match
      await dataMigrationDB.updateJob(
        DATA_MIGRATION_TRACKING_STATE_ID,
        dataMigrationDB.status.COMPLETED
      );
      return;
    case dataMigrationDB.status.MIGRATING:
      console.log("Migration is in progress, checking status and continuing if needed");
      await checkMigrationJobs();
      return;
    case dataMigrationDB.status.READY:
      console.log("Migration ready to start, starting migration");
      await dataMigrationDB.updateJob(
        DATA_MIGRATION_TRACKING_STATE_ID,
        dataMigrationDB.status.MIGRATING
      );
      await startMigrationJobs();
      return;
    default:
      console.log(`Unknown migration status ${remoteMigrationState.status}, not starting migration`);
      return;
  }
};
```
```

### Migration trigger

We recommend linking a [Scheduled Trigger](/platform/forge/manifest-reference/modules/scheduled-trigger/) to your migration tasks. These tasks are:

* Starting the data migration for an installation
* Queuing data migration async events
* Re-starting any migration functions that fail (for example, due to Async event cyclical limits, or some unexpected error)
* Validating data migration state
* Re-running data migration jobs to keep data in sync
* Reverse data migration sync

#### Example scheduled trigger

A basic `scheduledTrigger` for our [example migration function](#example-migration-state-tracker-function) would look like:

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: data-migration-trigger
      function: data-migration-function
      interval: hour # Runs hourly
  function:
    - key: data-migration-function
      handler: index.migrate
```
```

We recommend only setting the interval to *hourly*, as this will likely give your function enough time to perform a data migration, check the status, and react accordingly to the status.

### Remote endpoints

Due to Forge's security model, there are no direct methods for sending data from your remote service to a Forge app or Forge SQL database. Instead, you'll need to implement migration logic within a hosted Forge app that calls your remote service to pull data progressively.

You can use the `invokeRemote` to check in with your existing source SQL, copy data into Forge SQL, and support dual-writing. See [Invoke Remote API](/platform/forge/runtime-reference/invoke-remote-api/) for related information.

You’ll need to build endpoints in the Forge Remote service hosting your source SQL for the following purposes:

| Endpoint purpose | Description |
| --- | --- |
| Tracking migration job status | Your source SQL should be able to should return current status and also update it. Your endpoint can also return metadata used for starting the data sync. |
| Data migration | This endpoint will be used to access data, and should only need to  accept input to control what it returns. How this returns data is entirely up to you. You might do it based on some logical layout, or by table. The only common thing is it should have some kind of pagination support. |
| Remote writes (optional) | If you want to add a rollback capability, add an endpoint for remote-writes on each database call.  Alternatively, you can implement a reverse data sync, using the same processes to sync to Forge SQL, but this sends the data back. |

### Data migration endpoint invoker

You’ll also need a data migration invoker to communicate with the remote endpoint you create specifically for data migration. This invoker will be triggered by each job in your [migration events queue](#migration-events-queue). When designing this invoker, consider the following:

* **Data Type Conversion**: Ensure proper conversion for JSON transmission.
* **Pagination**: Implement to manage network and memory limits.
* **Metadata Inclusion**: Include metadata for easier pagination.
* **Data Structure**: Use arrays of arrays for row data to minimize transmission size.
* **Customer-Specific Data**: Return only relevant data for the appropriate customer.

#### Example data migration endpoint invoker

For this, you might call your data migration endpoint to get data with an API similar to the following:

```
```
1
2
```



```
async function getRemoteData<RowData>(dataType: String, after: String): Promise<MigrationData<RowData>> {
  const res = await invokeRemote('my-remote-key', {
    path: `/data-migration/${dataType}/?limit=500&after=${lastSyncId}`,
    method: 'GET'
  });

  if (!res.ok) {
    console.error("Failed to invoke remote", { 
      status: response.status,
      statusText: response.statusText,
      headers: response.headers.raw(),
      body: await res.text(),
      dataType,
      after
    })
    throw new Error("Failed to invoke remote")
  }

  return await res.json();
};
```
```

You could then structure your response to the following:

```
```
1
2
```



```
interface MigrationData<RowData> {
  /** Array matching order of DataRow that indicates the columns **/
  headers: Array<String>;
  /** Array of DataRow indicates the columns **/
  data: Array<RowData>;
  /** Quick info to include in getting next page
    * Useful if you use some other kind of pagination key.
   **/
  pagination: {
    afterId: String | Number;
  }
}
```
```

### Data transfer function

Once you’ve queued an async event invoking your remote service’s data migration endpoint, you can now execute the data transfer. For this, you’ll need a function with the following capabilities:

1. Stick to async function limits
2. Maintain migration state
3. Loop over fetching data
4. Update state
5. Start next job

#### Example data transfer function

The following sample function shows a basic data transfer function:

```
```
1
2
```



```
import Resolver from '@forge/resolver';
import { invokeRemote } from '@forge/api';
import { Queue } from '@forge/events';
import { dataMigrationDB } from './data-migration/sql';
import { dataHandlers } from './data-migration/data-handlers';

// key matches what is defined in the manifest.yml
const dataMigrationQueue = new Queue({ key: 'forge-data-migration-queue' });

// The limit of the async event run time, in milliseconds to match the performance API
const ASYNC_RUNTIME = 900000; // 900 seconds (15 minutes)
const ASYNC_RUNTIME_BUFFER = 20000; // 20 seconds buffer to do start and cleanup
const ASYNC_RUNTIME_LIMIT = ASYNC_RUNTIME - ASYNC_RUNTIME_BUFFER;

const resolver = new Resolver();

// The function that is called by the async event queue, which handles the actual data migration
resolver.define('dataMigrationQueueListener', async ({ payload, context }) => {
  // start timer
  const startTime = performance.now();

  const { pagination, dataType } = payload;
  console.log({ jobId: context.jobId, pagination, dataType }, "Data migration job started");

  // Check if the job is already in progress, and update it if needed
  const currentJob = await dataMigrationDB.getJob(context.jobId);
  if(currentJob.status !== dataMigrationDB.status.MIGRATING) {
    await dataMigrationDB.updateJob(context.jobId, dataMigrationDB.status.MIGRATING);
  }

  // Use a specific handler for each data type for your migration
  const handler = dataHandlers[dataType];

  let nextPage = pagination;
  let done = false;
  do {
    // pull data from remote
    const remoteData = await handler.getRemoteData(nextPage)
    // set the next page details
    nextPage = handler.nextPage(remoteData);
    // determine if we are done or not
    if(handler.done(remoteData)) {
      done = true;
    }
    // convert data to forge sql format
    const forgeSqlParams = handler.toForgeSQL(remoteData);
    // store data in forge sql
    await handler.pushToSQL(forgeSqlParams);
  } while (!done || performance.now() - startTime < ASYNC_RUNTIME_LIMIT);

  if(!done) {
    const { jobId } = await dataMigrationQueue.push({ body: { dataType, pagination } });
    console.log("Next job started", jobId);
    // update all job statuses
    await Promise.allSettled([
      dataMigrationDB.updateJob(context.jobId, dataMigrationDB.status.COMPLETED),
      // this can include the same context information, incase we hit the limit
      dataMigrationDB.insertJob(job.id, dataMigrationDB.status.PENDING, dataType, {
        dataType,
        pagination,
      }),
    ])
  } else {
    // otherwise mark the job as completed!
    await dataMigrationDB.updateJob(context.jobId, dataMigrationDB.status.COMPLETED);
    await markDataMigrationCompleted(dataType);
    console.log("Data migration completed", {dataType, jobId: context.jobId});
  }
});

export const handler = resolver.getDefinitions();
```
```

### Forge SQL data inserter

Upon invoking your data transfer function, you’ll need to transform your source data for insertion into the destination table in Forge SQL.

Forge SQL only supports a single statement per request, so we recommend building a function to generate a single `INSERT` statement with multiple rows. Ensure you leverage passing in parameters separately to your query. This is much safer, and means the data types are handled appropriately by Forge SQL.

#### Example data inserter

Once you’ve retrieved data through your data transfer function, you can use a bulk insert helper to write the data to the Forge SQL database. The following example shows a helper that wraps a specific data type in a bulk insert:

```
```
1
2
```



```
/**
 * Example usage of insertMultipleRows function.
 */
export async function exampleInsert(rows) {
  const tableName = "example_table";
  const columns = ["id", "name", "age"];

  await insertMultipleRows(tableName, columns, rows);
}

// This will generate and execute the following SQL query:
// INSERT INTO `example_table` (`id`, `name`, `age`) VALUES (?, ?, ?), (?, ?, ?), (?, ?, ?);
// Args: [1, 'Alice', 30, 2, 'Bob', 25, 3, 'Charlie', 35];
await exampleInsert([
    [1, "Alice", 30],
    [2, "Bob", 25],
    [3, "Charlie", 35],
  ])
```
```

This will take in the table construction details and columns, then generate an SQL bulk insert statement to use to write it to to Forge SQL:

```
```
1
2
```



```
import { sql } from "@forge/sql";

/**
 * Generates and executes a SQL INSERT query for multiple rows of data.
 *
 * @param {string} tableName - The name of the table to insert data into.
 * @param {string[]} columns - An array of column names for the table.
 * @param {Array<Array<any>>} rows - An array of arrays, where each inner array represents a row of data.
 */
export async function insertMultipleRows(tableName, columns, rows) {
  if (!rows || rows.length === 0) {
    console.log("No rows to insert");
    return;
  }

  // Construct the base SQL query
  const columnList = columns.map((col) => `\`${col}\``).join(", ");
  // Precompute the placeholder for a single row
  const singleRowPlaceholder = `(${columns.map(() => "?").join(", ")})`;
  const query = `INSERT INTO \`${tableName}\` (${columnList}) VALUES ${new Array(
    rows.length
  )
    .fill(singleRowPlaceholder)
    .join(", ")}`;

  // Prepare and execute the SQL query
  await sql.prepare(query).bindParams(rows.flat()).execute();

  console.log(`Inserted ${rows.length} rows into table ${tableName}`);
}
```
```

### Data migration job checker

You’ll need to periodically validate your [migration events queue](#migration-events-queue) to restart any jobs that failed (due to hitting cyclical event limits or any unexpected errors). Build a function to do this, which will also be triggered by the [migration trigger](#migration-trigger) whenever the migration status is set to `IN_PROGRESS`.

You can also use this function to check any data updates that occurred as a result of customer activity during the migration.

#### Example data migration job checker

The following example shows a function that can check job statuses and restart them if needed:

```
```
1
2
```



```
/** Checks existing data migration jobs, and starts them again as needed */
export async function checkMigrationJobs() {
  const jobs = await dataMigrationDB.getJobsByStatus(dataMigrationDB.status.MIGRATING);

  if (jobs.length === 0) {
    console.log("No migration jobs in progress, starting them again");
    await startMigrationJobs();
    return;
  }

  const missingDataTypes = getMissingDataTypes(jobs);
  if (missingDataTypes.size > 0) {
    console.log("Missing data types in migration jobs, starting them again", { missingDataTypes: [...missingDataTypes] });
    await startMigrationJobs(missingDataTypes);
  }

  const jobTasks = jobs.map((job) => processJob(job));
  await Promise.allSettled(jobTasks);
}

/** Identifies missing data types that need to be restarted */
function getMissingDataTypes(jobs) {
  const activeDataTypes = new Set(jobs.map((job) => job.dataType));
  const allDataTypes = new Set(DATA_TYPES);
  return new Set([...allDataTypes].filter((dataType) => !activeDataTypes.has(dataType)));
}


/** Processes an individual job and restarts it if necessary */
async function processJob(job) {
  console.log(`Checking migration job ${job.id} status`);
  const queueJob = dataMigrationQueue.getJob(job.jobId);
  const { success, inProgress, failed } = await jobProgress.getStats();

  if (inProgress) {
    console.log("Job is still in progress", { jobId: job.jobId, dataType: job.dataType });
    return;
  } else if (success) {
    console.log(
      "Job completed, but still marked as migrating. Restarting at last know point",
      { jobId: job.jobId, dataType: job.dataType, pagination: job.pagination }
    );
    await dataMigrationDB.updateJob(job.id, dataMigrationDB.status.COMPLETED);
    await restartJob(job);
  } else if (failed) {
    console.log("Job previously failed, restarting from last known point", {
      jobId: job.jobId,
      dataType: job.dataType,
      pagination: job.pagination,
    });
    await dataMigrationDB.updateJob(job.id, dataMigrationDB.status.FAILED);
    await restartJob(job);
  }
}

/** Restarts a job with the same data type and pagination */
async function restartJob(job) {
  const { newJobId } = await dataMigrationQueue.push({ body: { dataType: job.dataType, pagination: job.pagination } });
  await dataMigrationDB.insertJob(newJobId);
}
```
```

## Data migration flow

Once you’ve built all the components, deploy your app changes and wait for the data migration to start. It’ll unfold as follows for each customer’s installation:

1. The Forge platform calls your [migration trigger](#migration-trigger).
2. This trigger will call the migration’s [state tracker function](#state-tracker-function), to check the current state of the migration (which is saved in the [migration state table](#migration-state-table)).
3. If the migration state table shows a status of `READY`, the tracker function will:
   1. Set the migration status to `IN_PROGRESS`.
   2. Start sending jobs to your [migration events queue](#migration-events-queue). The number of jobs running in this queue at any given time will depend on your implementation.
4. Each migration job in the queue executes a data transfer using the following components:

Once your scheduled trigger’s configured interval has passed, Forge will call your migration trigger again. If the migration state table shows a status of `IN_PROGRESS`, the tracker function will use the [data migration job checker](#data-migration-job-checker) to check your [migration events queue](#migration-events-queue) and restart any failed jobs.

If there’s no data left to transfer, the state tracker function will set update the migration state to `DONE`.

You may want to re-factor your app to write to both the remote SQL source and Forge SQL destination during the migration. Your app can do this asynchronously at the same time, or sequentially based on the response of the remote. Doing so gives you the option to perform a rollback from Forge SQL back to the remote SQL.

## Completing the migration

If your app executes the migration *without* downtime, then customers may still be using the app (and, presumably, writing new data). This means data between your source and destination SQL databases won’t be in sync for long.

In this case, a useful way to determine that the migration is complete (that is, data in Forge SQL is updated) is when all data for all types is migrated within a single run.

This indicates that each subsequent data migration run will only retrieve new data. Consequently, you will need to take action with this information, which may involve updating your database or sending a remote signal.

### Switching to Forge SQL as primary

Upon completing the migration, your app will need to start treating the Forge SQL as its primary database. However, you may want to keep your existing remote SQL source in case you need to roll back. For this reason, you may want to consider dual-writing to both the remote SQL and Forge SQL

## Post-migration

Once all of your customer installation statuses are `DONE`, and you are confident in the data integrity of your Forge SQL, update your app to only write data to Forge SQL. With this update, you can remove all references to the remote SQL database in your manifest and decommission that database.

If your manifest no longer has any `remotes` declarations, your app will become eligible for the [Runs on Atlassian](/platform/forge/runs-on-atlassian/) badge. In addition, storing all data on Forge hosted storage means your app will automatically inherit [data residency features](/platform/forge/data-residency/).

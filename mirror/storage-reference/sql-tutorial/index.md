# Add a Forge SQL database to your app

This tutorial describes how to add a Forge SQL database to your app for the first time. It covers all aspects of implementation, from defining a database schema to writing executable SQL queries.

[Example app

This tutorial uses code samples from an example app, which we published to help
demonstrate the basics of using Forge SQL. This example app includes simple and clear samples for
defining database objects, orchestrating schema migrations, and supported SQL statement syntax.
It may also contain updated code not included in this tutorial.](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/)

## Before you begin

The `sql` package provides the necessary SDKs for interacting with Forge SQL. To start using Forge SQL’s capabilities, you’ll need to install it in your project:

To import the package (including its [error handler](/platform/forge/storage-reference/sql-handling-errors/)) into your app:

```
1
import { sql, errorCodes } from '@forge/sql' ;
```

## Step 1: Define Forge SQL as a module

To enable Forge SQL on your app, you’ll need to define the `sql` [module](/platform/forge/manifest-reference/modules/sql/) in the manifest file:

```
1
2
3
4
modules:
  sql:
    - key: main
      engine: mysql
```

## Step 2: Define database schema via DDL statements

Use Data Definition Language (DDL) statements to create and configure the tables, indexes, and other objects in your database schema. Export each DDL statement as a value, which you can use later.

For example, the following snippet defines two DDL operations for creating tables in your database: `CREATE_USERS_TABLE` and `CREATE_BOOKS_TABLE`.

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
    email VARCHAR(100) UNIQUE NOT NULL
)`;

export const CREATE_BOOKS_TABLE = `CREATE TABLE IF NOT EXISTS Books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    published_date DATE
)`;
```
```

When using the `migrationRunner` SDK, your app should only have one `migrationRunner` invocation.

## Step 3: Invoke DDL operations in one function

Use the `migrationRunner.enqueue` method to invoke your DDL operations. When you do, assign an `operationName` to each statement.

Afterwards, wrap your invocation in a single database object creation function. This will let you map its key to a scheduled trigger, which Forge will use to execute it later (we explain this further in the next section).

For example, the following snippet assigns an `operationName` to the `CREATE_USERS_TABLE` and `CREATE_BOOKS_TABLE` operations in the previous step (`v001_create_users_table` and `v002_create_books_table`, respectively):

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

In this next snippet, `createDBobjects` is wrapped in a single database object creation function (`runMigration`). This makes all your DDL operations executable as one function:

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
}

export const applyMigrations = async () => {
  const successfulMigrations = await createDBobjects.run();
  console.log('Migrations applied:', successfulMigrations);
};
```
```

When `runMigrations` is executed, the `CREATE_USERS_TABLE` operation (paired to `v001_create_users_table`) will be executed first. The `CREATE_BOOKS_TABLE` operation will only be executed once `CREATE_USERS_TABLE` has completed successfully.

## Step 4: Orchestrate execution of DDL operations

Map your database object creation function to a
[scheduled trigger](/platform/forge/function-reference/scheduled-trigger/) module
in your manifest. Forge will use the trigger to execute your `migrationRunner` invocation according to your defined `interval`.

For example, the `scheduledTrigger` declaration here triggers the `runMigration` function (from the previous step):

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

In this case, Forge will execute `runMigration` within an *hour* of app installation. As such, it is possible for customers to have your app already installed, without the database schema applied yet.

## Step 5: Create logs for database object creation

Include a `migrationRunner.list` invocation in your database object creation (namely, `runMigration` in our previous example). This method lets you generate logs for each queued database creation operation in [Step 2](#step2). For example:

```
```
1
2
```



```
export const applyMigrations = async () => {
  const successfulMigrations = await createDBobjects.run();

  console.log('Migrations checkpoint [after running migrations]:');
  await migrationRunner
    .list()
    .then((migration) => migration.map((y) => console.log(`${y.name} migrated at ${y.migratedAt.toUTCString()}`)));
  };
```
```

[Generate logs

Our sample app’s database object creation function generates logs for each operation. These logs let you track the progress of each schema application (and update) for every app installation.](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/sql/migration.ts#lines-48)

## Step 6: Write your SQL operations

For now, Forge SQL accepts prepared statements with positional parameters. We plan to expand parameter support later on based on capacity and EAP feedback.

Use the following method signature for defining your SQL statements:

```
```
1
2
```



```
sql
  .prepare<DataType>(query: string)
  .bindParams(...args: SqlParameters): Promise<Result<DataType>>;
```
```

For example, to create a function for saving data to the `Users` table (defined in the SQL migration script from [Step 2](#step2)):

**interactors/userInteractor.ts**

```
```
1
2
```



```
import { sql, errorCodes } from '@forge/sql';

const CREATE_USER = `INSERT INTO Users (name, email) VALUES (?, ?);`;

export const createUser = async (name: string, email: string) => {
  try {
    return await sql.prepare(CREATE_USER).bindParams(name, email).execute();
  } catch (error) {
    console.error('Error creating user', JSON.stringify(error));
    // @ts-expect-error - Ignore error unknown
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
    if (error.code === errorCodes.SQL_EXECUTION_ERROR && error.debug.code === 'ER_DUP_ENTRY') {
      throw new Error('A user with this email already exists.');
    }
    throw error;
  }
};
```
```

JSON data types may not be supported in future versions of Forge SQL.

### Inserting Date values

Forge SQL lets you store multiple `Date` objects based on data types supported by ANSI SQL.
Ensure that each date type adheres to the specified input format.

| Date type | Format | Example |
| --- | --- | --- |
| DATE | YYYY-MM-DD | 2024-09-19 |
| TIME | HH:MM:SS[.fraction] | 06:40:34 |
| TIMESTAMP | YYYY-MM-DD HH:MM:SS[.fraction] | 2024-09-19 06:40:34.999999 |

The following example uses `moment` to format dates accordingly:

```
```
1
2
```



```
import { sql, errorCodes } from '@forge/sql';
import moment from 'moment';


export const insertLoginDetails = async () => {
  await sql
  .executeRaw(`CREATE TABLE IF NOT EXISTS LoginDetails (
      id INT PRIMARY KEY,
      CreatedAt DATE,
      LastLoginTime TIME,
      LastLoginTimestamp TIMESTAMP);`
  );
  await sql
  .prepare(`INSERT INTO LoginDetails
      (id, CreatedAt, LastLoginTime, LastLoginTimestamp)
    VALUES
      (?, ?, ?, ?);`)
  .bindParams(
    1,
    moment().format("YYYY-MM-DD"),
    moment().format("HH:mm:ss.SSS"),
    moment().format("YYYY-MM-DDTHH:mm:ss.SSS")
  );
};
```
```

## Step 7 Deploy app and track schema migration

You can monitor any failures in DDL operations by viewing your *app logs* in the Developer Console. From there, you can filter for errors against the scheduledTrigger mapped to your migrationRunner invocation. See [Monitoring SQL](/platform/forge/monitor-sql-metrics/) for more information.

SQL operations executed while tunnelling will be directed to your app’s provisioned database. This means that changes to the database from other users will be reflected on any SQL queries performed while tunnelling.

# Execute SQL operations

This page lists the different methods for retrieving, storing, and updating data in databases provisioned by Forge SQL.

## Before you begin

The `sql` package provides the necessary methods for interacting with Forge SQL. To start using Forge SQL’s capabilities, you’ll need to install it in your project:

To import the package (including its [error handler](/platform/forge/storage-reference/sql-handling-errors/)) in your app:

```
1
import { sql, errorCodes } from '@forge/sql' ;
```

## Prepared statements

Use the `sql.prepare` method to prepare a Data Manipulation Language (DML) statement, which will be passed as a parameter and executed:

```
1
sql.prepare<DataType>(query: string): SqlStatement<Result<DataType>>;
```

This returns a `SqlStatement` instance, which provides two methods:

* `.bindParams(...params): this`: Binds parameters to the query, one for each `?` in your query.
* `.execute(): Promise<Result<DataType>>`: Runs the SQL statement against the database

`DataType` refers to a [Typescript Generic](#typescript-support) that you can optionally supply to type the query response.

Forge SQL encodes and decodes responses in JSON, and doesn’t do any translation back to a specific field type. You will need to handle this in your code. For example, Dates will be returned as strings.

To prevent SQL injection attacks, use `?` in place of values which will be substituted in order when you use `bindParams(param1, param2)`.

### Example

The following example shows how to use `sql.prepare` to insert data into a table. The use of `UpdateQueryResponse` is optional here (you can use it if you want to inspect the results of the query execution).

```
```
1
2
```



```
import sql, { UpdateQueryResponse } from '@forge/sql';

const results = await sql
                  .prepare<UpdateQueryResponse>(`INSERT INTO cities VALUES (?, ?)`)
                  .bindParams('New york', 'USA')
                  .execute();
```
```

This example shows how to use `sql.prepare` to query data from a table:

```
```
1
2
```



```
import sql from '@forge/sql';

interface City {
  name: string;
  state?: string;
  country: string;
};

const results = await sql
                  .prepare<City>(`SELECT * FROM cities WHERE name = ?`)
                  .bindParams('New York')
                  .execute();

console.log(results.rows[0].country); // USA
```
```

## Execute statement

Use the `sql.executeRaw` method to execute a DML statement against your database. This method supports any ANSI SQL dialect statement. The `sql.executeRaw` method does not accept any parameters, and will execute the DML statement immediately:

```
```
1
2
```



```
sql.executeRaw<DataType>(query: string): Promise<Result<DataType>>;
```
```

This method is shorthand for `sql.prepare(query).execute()` (that is, preparing a statement without any parameters and immediately executing it).

`DataType` refers to a [Typescript Generic](#typescript-support) that you can optionally supply to type the query response.

## Typescript Support

The `sql` SDK supports [Typescript Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html#generic-types) for the result type, as indicated by `<DataType>`. This assumes the response will be an array format `Array<DataType>`, and does not validate whether the type you supply matches the response. Additionally, all types returned from our API are normalised via JSON, and will need to be converted to a specific object type.

If you are making a DML or DDL query, you can supply `UpdateQueryResponse` as the generic type.
These types are exported and available from the main import:

```
```
1
2
```



```
import sql, { UpdateQueryResponse, Result } from '@forge/sql'
```
```

The types as defined in our code are:

```
```
1
2
```



```
type SqlParameters = any[];

/** Returned when result set is part of a DDL / DML query */
export interface UpdateQueryResponse {
  /** The number of rows affected by the query */
  affectedRows: number;
  /** The number of fields in the result set */
  fieldCount: number;
  /** The information message from the query */
  info: string;
  /** The ID generated for an AUTO_INCREMENT column by the previous query */
  insertId: number;
  /** The server status */
  serverStatus: number;
  /** The warning status */
  warningStatus: number;
}

interface Result<DataType = any> {
  rows: DataType extends UpdateQueryResponse ? UpdateQueryResponse : DataType[];
  metadata?: Record<string, any>;
}
```
```

## SQL statement syntax

Use basic DML statements to retrieve, store, and update data in databases provisioned by Forge SQL. Forge SQL supports MySQL-compatible DML operations like `INSERT`, `SELECT`, `UPDATE`, and `DELETE` (for more details, see [SQL Statement Overview](https://docs.pingcap.com/tidb/stable/sql-statement-overview#data-manipulation-statements-dml) in the TiDB documentation).

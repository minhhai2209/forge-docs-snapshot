# Error handling for Forge SQL

The `@forge/sql` package exports error codes. The following example shows how the package handles a
`QUERY_TIMED_OUT` error:

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
import { sql, errorCodes } from '@forge/sql'; 

try { 
  await sql
    .prepare("INSERT INTO city (id, city, population) VALUES (?, ?, ?)")
    .bindParams(1, "Beijing", 100)
    .execute();
} 
catch (error) { 
  if (error.code === errorCodes.QUERY_TIMED_OUT) { 
    // Handle query timeout
  } 
}
```

## Error codes

| Error code | Description |
| --- | --- |
| `QUERY_TIMED_OUT` | The provided query took more than 2 seconds to execute.  This error means the HTTP connection is being terminated, but the query will continue executing at the database level. |
| `SQL_EXECUTION_ERROR` | The provided query was either incorrect or could not be executed at the database level. More details are present in the `debug` field.   This error code is also returned when the query is empty or cannot be parsed. In that case, the `debug` field mirrors the native TiDB `ER_PARSE_ERROR` response. |
| `INVALID_SQL_QUERY` | The provided query is not compliant with ANSI SQL. |
| `SQL_POLICY_VIOLATION` | The provided query uses a function, statement, or syntax that is restricted by the Forge SQL query policy. See [Forge SQL query policy](/platform/forge/storage-reference/sql-query-policy/) for the list of restricted keywords. |

## Error response shapes

Errors thrown by the `@forge/sql` package include a `code` and `message`. Some
errors include additional fields, such as `suggestion` and `debug`, to help you
diagnose and resolve the issue.

### Policy violations

When a query is rejected by the [Forge SQL query
policy](/platform/forge/storage-reference/sql-query-policy/), the error
response uses the following shape:

```
```
1
2
```



```
{
  "code": "SQL_POLICY_VIOLATION",
  "message": "<reason the query was rejected>",
  "suggestion": "<recommended action to resolve the violation>"
}
```
```

The `suggestion` field provides guidance on how to rewrite the query so that it
complies with the query policy.

### Parse errors

When a query is empty or cannot be parsed, the error response uses the
`SQL_EXECUTION_ERROR` code and includes a `debug` field that mirrors the native
TiDB parse error:

```
```
1
2
```



```
{
  "code": "SQL_EXECUTION_ERROR",
  "message": "Unknown SQL execution error",
  "suggestion": "<recommended action to resolve the parse error>",
  "debug": {
    "code": "ER_PARSE_ERROR",
    "errno": 1064,
    "sqlMessage": "<TiDB parse error message>",
    "sqlState": "42000"
  }
}
```
```

Use the `debug.sqlMessage` field to identify the exact syntax issue reported by
the underlying database.

## Example: handling a policy violation

The following example checks for a query policy violation and falls back to a
permitted alternative:

```
```
1
2
```



```
import { sql, errorCodes } from '@forge/sql';

try {
  await sql
    .prepare("SELECT SLEEP(1)")
    .execute();
} catch (error) {
  if (error.code === errorCodes.SQL_POLICY_VIOLATION) {
    // The query was rejected by the Forge SQL query policy.
    // Log the suggestion and rewrite the query before retrying.
    console.warn(`Query policy violation: ${error.message}. ${error.suggestion}`);
  } else {
    throw error;
  }
}
```
```

[Example app

We published a sample app to help demonstrate the basics of using Forge SQL. This sample also provides sample code that demonstrate how to handle typical errors.](https://bitbucket.org/atlassian/forge-sql-examples/src/main/book-management-typescript/src/resolvers/interactors/)

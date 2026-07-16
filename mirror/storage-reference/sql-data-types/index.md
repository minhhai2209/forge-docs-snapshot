# Forge SQL data types

Forge SQL is built on [TiDB](https://docs.pingcap.com/tidb/stable/dev-guide-overview) and supports MySQL-compatible data types. This page describes the supported types, explains how Forge SQL returns query results, and covers known limitations.

Forge SQL encodes and decodes query results as JSON. All returned values are JSON-normalised, so you must convert them to the correct type in your app code.

## Supported data types

Forge SQL supports all MySQL-compatible data types that TiDB supports. The following table shows the most commonly used types, the format they're returned in, and how to handle them in your app.

### Numeric types

| Type | Description | Returned as | Handling notes |
| --- | --- | --- | --- |
| `INT` / `INTEGER` | 32-bit signed integer | Number | No conversion needed for most values |
| `BIGINT` | 64-bit signed integer | String | Convert with `BigInt()` or a numeric library — see [Handling BIGINT values](#handling-bigint-values) |
| `TINYINT` | 8-bit signed integer | Number | No conversion needed |
| `SMALLINT` | 16-bit signed integer | Number | No conversion needed |
| `MEDIUMINT` | 24-bit signed integer | Number | No conversion needed |
| `DECIMAL` / `NUMERIC` | Exact fixed-point number | String | Parse with a decimal library (such as `decimal.js` or `big.js`) to preserve precision — `parseFloat()` converts to floating-point and does not preserve exact decimal values |
| `FLOAT` | Single-precision floating-point | Number | Subject to standard floating-point precision limits |
| `DOUBLE` | Double-precision floating-point | Number | Subject to standard floating-point precision limits |
| `BIT` | Bit-field value | Number |  |

### String types

| Type | Description | Returned as | Handling notes |
| --- | --- | --- | --- |
| `CHAR` | Fixed-length string | String | No conversion needed |
| `VARCHAR` | Variable-length string | String | No conversion needed |
| `TEXT` | Variable-length text (up to 65,535 bytes) | String | Hidden in the schema viewer — see [Hidden fields](#hidden-fields) |
| `MEDIUMTEXT` | Variable-length text (up to 16 MB) | String | Hidden in the schema viewer — see [Hidden fields](#hidden-fields) |
| `LONGTEXT` | Variable-length text (up to 4 GB) | String | Hidden in the schema viewer — see [Hidden fields](#hidden-fields) |
| `TINYTEXT` | Variable-length text (up to 255 bytes) | String |  |

### Binary types

Binary types are hidden in the Forge SQL schema viewer. You can store and query these types, but the **Table data** tab in the Developer Console won't display them. See [Hidden fields](#hidden-fields).

| Type | Description | Returned as | Handling notes |
| --- | --- | --- | --- |
| `BINARY` | Fixed-length binary data | String | Hidden in schema viewer |
| `VARBINARY` | Variable-length binary data | String | Hidden in schema viewer |
| `BLOB` | Binary large object (up to 65,535 bytes) | String | Hidden in schema viewer |
| `MEDIUMBLOB` | Binary large object (up to 16 MB) | String | Hidden in schema viewer |
| `LONGBLOB` | Binary large object (up to 4 GB) | String | Hidden in schema viewer |

### Date and time types

Forge SQL supports the following date and time types. Each type has a specific input and return format — ensure your values match the format shown below.

| Type | Format | Example | Returned as |
| --- | --- | --- | --- |
| `DATE` | `YYYY-MM-DD` | `2024-09-19` | String |
| `TIME` | `HH:MM:SS[.fraction]` | `06:40:34` | String |
| `DATETIME` | `YYYY-MM-DD HH:MM:SS[.fraction]` | `2024-09-19 06:40:34.999999` | String |
| `TIMESTAMP` | `YYYY-MM-DD HH:MM:SS[.fraction]` | `2024-09-19 06:40:34.999999` | String |
| `YEAR` | `YYYY` | `2024` | Number |

Because Forge SQL returns date and time values as strings, you must parse them in your app code. We recommend using a date library such as [`moment`](https://momentjs.com/) or the native `Date` object:

```
```
1
2
```



```
import sql from '@forge/sql';
import moment from 'moment';

interface LoginDetails {
  id: number;
  CreatedAt: string;
  LastLoginTimestamp: string;
}

try {
  const result = await sql
    .prepare<LoginDetails>('SELECT * FROM LoginDetails WHERE id = ?')
    .bindParams(1)
    .execute();

  if (result.rows.length === 0) {
    throw new Error('No login details found');
  }

  const row = result.rows[0];
  const createdAt = moment(row.CreatedAt, 'YYYY-MM-DD').toDate();
  const lastLogin = new Date(row.LastLoginTimestamp);
} catch (error) {
  console.error('Error fetching login details:', error);
  throw error;
}
```
```

### Boolean type

| Type | Description | Returned as | Handling notes |
| --- | --- | --- | --- |
| `BOOLEAN` / `BOOL` | Alias for `TINYINT(1)` | Number (`0` or `1`) | Convert to boolean with `Boolean(value)` or `value === 1` |

### JSON type

JSON data types may not be supported in future versions of Forge SQL. We recommend storing JSON as a `TEXT` or `VARCHAR` column and serialising/deserialising in your app code instead.

| Type | Description | Returned as |
| --- | --- | --- |
| `JSON` | JSON document | String |

If you store JSON directly in a `JSON` column, the value is returned as a string. Deserialise it with `JSON.parse()`:

```
```
1
2
```



```
import sql from '@forge/sql';

interface Product {
  id: number;
  metadata: string; // raw JSON string
}

const result = await sql
  .prepare<Product>('SELECT id, metadata FROM products WHERE id = ?')
  .bindParams(42)
  .execute();

if (result.rows.length === 0) {
  throw new Error('Product not found');
}

let metadata;
try {
  metadata = JSON.parse(result.rows[0].metadata);
  // Use metadata
} catch (error) {
  console.error('Failed to parse metadata JSON:', error);
  throw new Error('Invalid metadata format');
}
```
```

## Handling BIGINT values

JavaScript's `number` type is a 64-bit floating-point value (IEEE 754). It can only safely represent integers up to `2^53 - 1` (`Number.MAX_SAFE_INTEGER`). `BIGINT` columns can hold values larger than this, so Forge SQL returns `BIGINT` values as **strings** to preserve precision.

To work with large integers, use JavaScript's native `BigInt` type:

```
```
1
2
```



```
import sql from '@forge/sql';

interface Counter {
  id: number;
  count: string; // BIGINT returned as string
}

const result = await sql
  .prepare<Counter>('SELECT id, count FROM event_counters WHERE id = ?')
  .bindParams(1)
  .execute();

if (result.rows.length === 0) {
  throw new Error('Counter not found');
}

const count = BigInt(result.rows[0].count);
const incremented = count + 1n;

await sql
  .prepare('UPDATE event_counters SET count = ? WHERE id = ?')
  .bindParams(incremented.toString(), 1)
  .execute();
```
```

When binding a `BIGINT` parameter, pass the value as a string (for example, `bigIntValue.toString()`). Passing a JavaScript `number` may silently lose precision for values outside the safe integer range.

## Type conversion summary

Because all Forge SQL query results are JSON-normalised, some database types are not returned in their native form. The following table summarises what to expect:

| Database type | Returned as in JavaScript | Conversion needed? |
| --- | --- | --- |
| `INT`, `SMALLINT`, `TINYINT`, `MEDIUMINT` | `number` | No |
| `BIGINT` | `string` | Yes — use `BigInt()` |
| `DECIMAL`, `NUMERIC` | `string` | Yes — use a decimal library (such as `decimal.js` or `big.js`) |
| `FLOAT`, `DOUBLE` | `number` | No (subject to floating-point precision) |
| `VARCHAR`, `CHAR`, `TEXT` | `string` | No |
| `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | `string` | Yes — parse with `Date` or a date library |
| `BOOLEAN` | `number` (`0` or `1`) | Yes — convert with `Boolean()` |
| `JSON` | `string` | Yes — parse with `JSON.parse()` |
| `BLOB`, `BINARY`, `VARBINARY` | `string` | Depends on use case |

## Hidden fields

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

The following types are hidden in the schema viewer:

* `BLOB`, `MEDIUMBLOB`, `LONGBLOB`
* `BINARY`, `VARBINARY`
* `CLOB`
* `TEXT`, `IMAGE`, `XML`, `JSON`

These types are hidden to prevent displaying large data payloads. They are also excluded from data downloaded through the **Download** button in the Developer Console.

`CLOB`, `IMAGE`, and `XML` are not MySQL-compatible data types and are not supported by Forge SQL. They appear in this list because the schema viewer hides them if somehow present, but you should not use these types in your schemas.

## Related pages

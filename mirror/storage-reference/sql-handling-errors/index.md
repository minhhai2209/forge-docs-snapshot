# Handling errors in Forge SQL

`1
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
13``import { sql, errorCodes } from '@forge/sql';
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
}`

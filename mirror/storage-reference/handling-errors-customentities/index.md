# Error handling for the Custom Entity Store

In conjunction with proper HTTP status codes, non-2xx responses will have the following schema:

```
1
2
3
4
{
  code: string; // "INVALID_KEY_FORMAT"
  message: string; // "Invalid key format"
}
```

Each `400 Bad Request` response will be accompanied by an *error code* containing more information. The following tables lists all possible error codes, what they mean, and what you can do to address each one:

## Quota and limit handling

Forge hosted storage capabilities are subject to limits, usage, and syntax constraints. These include limits to the number of operations, key lengths, and object depth. Any request that exceeds a quota or limit will return a
`429` status with an error code of `RATE_LIMIT_EXCEEDED`.

See [Storage quotas](/platform/forge/platform-quotas-and-limits/#storage-quotas) and
[Storage limits](/platform/forge/platform-quotas-and-limits/#storage-limits) for details about relevant constraints.

| Error code | Description |
| --- | --- |
| EMPTY\_KEY | Key cannot be empty. |
| INVALID\_KEY | The provided key does not match the regex: `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` |
| KEY\_TOO\_LONG | The provided key has exceeded the maximum 500 characters. |
| NOT\_FOUND | The specified key does not exist. |

| Error code | Description |
| --- | --- |
| MAX\_SIZE | The provided value has exceeded the maximum size limit. |
| MAX\_DEPTH | The provided value has exceeded the maximum object depth (32) limit. |

| Error code | Description |
| --- | --- |
| ENTITY\_TYPE\_TOO\_SHORT | The provided key needs to be more than 3 characters. |
| ENTITY\_TYPE\_TOO\_LARGE | The provided key has exceeded the maximum 60 characters. |
| INVALID\_ENTITY\_TYPE | The provided key does not match the regex: `/^(?![\.\-])(?!.*\.{2})[a-z0-9:\-.]*(?<![.])$/`. |
| INVALID\_ENTITY\_VALUE | Entity values must match one of the types defined in [Custom Entities](/platform/forge/runtime-reference/custom-entities/#values). |
| INVALID\_ENTITY\_ATTRIBUTE | The specified attribute name is a reserved value and cannot be utilized. |
| INVALID\_ENTITY\_INDEX | The custom entity index provided is invalid. The index name is a reserved value and cannot be utilized. |

| Error code | Description |
| --- | --- |
| COMPLEX\_QUERY\_PAGE\_LIMIT\_NOT\_IN\_RANGE | The page limit must be set between 1 and 100. |
| EMPTY\_FILTER\_OPERATOR | Filter operators "and" and "or" cannot be empty. |
| INVALID\_FILTER\_OPERATORS\_COMBINATION | Filter operators "and" and "or" cannot be present at the same level. |
| INSUFFICIENT\_FILTER\_VALUES | The specified condition needs at least two values. |

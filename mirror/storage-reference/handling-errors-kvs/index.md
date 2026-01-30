# Error handling for the Key-Value Store

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
| KEY\_TOO\_SHORT | The provided key needs to be more than one character. |
| KEY\_TOO\_LONG | The provided key has exceeded the maximum 500 characters. |
| INVALID\_KEY | The provided key does not match the regex: `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` |
| NOT\_FOUND | The specified key does not exist. |

| Error code | Description |
| --- | --- |
| MAX\_SIZE | The provided value has exceeded the maximum size limit. |
| MAX\_DEPTH | The provided value has exceeded the maximum object depth (32) limit. |

| Error code | Description |
| --- | --- |
| INVALID\_FILTER\_CONDITION | The specified condition is not supported for filters. |
| INVALID\_FILTER\_VALUES | The specified number of values are not supported by the given condition. |
| LIST\_QUERY\_LIMIT\_EXCEEDED | Limit for list query should be below 100. |
| QUERY\_WHERE\_INVALID | KVS queries should contain only a single "where" clause. |
| QUERY\_WHERE\_FIELD\_INVALID | The specified field is not supported for filters. |

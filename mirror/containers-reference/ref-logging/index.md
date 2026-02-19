# Forge Containers reference: logging (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

For compatibility with Forge’s developer tools we apply default properties to log lines produced by your app. You can specify values by including the following properties in JSON-formatted log lines (written to standard output):

| **Property** | **Description** | **Type** | **Default** |
| --- | --- | --- | --- |
| `ts` | Time that the log was ingested by the Forge platform. | `number` | Unix epoch timestamp, in milliseconds |
| `level` | Importance of log. | `string`  **values:**  * `INFO` * `TRACE` * `DEBUG` * `WARN` * `ERROR` * `FATAL` | `INFO` |
| `msg` | Arbitrary log message. | `string` | Entire log line |
| `forge_invocation` | Per-request invocation specific metadata such as invocation id, and installation context (encoded in `base64`). From the `x-forge-invocation-log-attributes` header that is [provided on requests to your container](/platform/forge/containers-reference/ref-api/#inbound-requests). | `string` | None.   When possible, [add this property to your logs](#invocation-metadata). |

We strongly advise that you include app invocation metadata to each log, whenever possible. Forge uses invocation IDs to associate logs with the corresponding customer, installation, and request. In addition, customers can only download and share app logs that contain invocation IDs.

For example, consider the following log:

```
```
1
2
```



```
{
    "ts": 1754624452000,
    "level": "WARN",
    "msg": "Something unexpected happened",
    "forge_invocation": "eyJpZCI6IjVmNmM3YjQ2LTY5NjctNGQ4OC05M2YxLWE1NDUyY2U4ZmFiMSIsImN0eCI6ImFyaTpjbG91ZDpqaXJhOmZjOTZjZmYzLTcwMjctNDBiMi1iMDI4LTg3ZjZkZmFmM2UwOTp3b3Jrc3BhY2UvYTg5ODE3ODMtNjk0MS00NmU4LWI2NjgtYzY4ZWZlNTM4NTI2IiwidHJhY2VJZCI6Ijg1M2VjM2JjNGQ0YjQ1MTY4YjNkNjcyMTUxNmFmM2U0In0="
}
```
```

This line would populate the Developer Console with the following entry:

![Developer Consoler sample entry for log line](https://dac-static.atlassian.com/platform/forge/images/containers-logging-invocation.png?_v=1.5800.1863)

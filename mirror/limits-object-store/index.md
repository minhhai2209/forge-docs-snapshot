# Forge Object Store limits

Forge Object Store is now available as part of our Early Access Program (EAP). To start testing this feature, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/3422/group/3571/create/18555).

Forge Object Store is an experimental feature offered for testing and feedback purposes. This feature is unsupported and subject to change without notice. Do not use Forge Object Store in apps that handle sensitive information, including personal data and customer data.

For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#eap).

The [Forge Object Store](/platform/forge/storage-reference/object-store/) is a hosted storage solution that let you manage large items such as data objects or media files. It provides you with a seamless way to efficiently store, retrieve, and manage objects directly from your Forge apps.

### EAP limitations

The Forge Object Store EAP is only available for testing purposes; apps using this feature can't be deployed to production.
In addition, objects stored during EAP will have a time-to-live (TTL) of 90 days.

**All stored objects will be deleted at the end of the EAP.** Atlassian will provide notice before the end of the EAP to ensure you have time to download any stored
data.

### Rate limits per installation

If the following rate limits are exceeded, Forge will return a `TOO_MANY_REQUESTS` error.

| Parameter | Limit |
| --- | --- |
| Object Store requests per second | 5000 |
| Pre-signed URL requests per second | 1000 |

### Operation limits

When building interfaces for object download/uploads, you must use the available
[frontend components](/platform/forge/storage-reference/object-store/#frontend-components)

| Parameter | Limit |
| --- | --- |
| Storage limits | Objects size can be up to 1 GB each. |
| Payload limits | The maximum payload size for all operations is 10 kB. |
| Pre-signed URL validity | Pre-signed URLs are valid for a maximum of 1 hr. |
